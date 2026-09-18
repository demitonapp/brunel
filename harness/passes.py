"""Control-pass exporter - the model-neutral half of the generative interface.

The scene graph never leaves Blender. What leaves is a set of *rasterised
control passes* that every generative video backend already accepts:

    depth   near/far-normalised depth, one range for the whole shot
    seg     flat colour per part - part identity, the closest thing to
            handing over the scene graph
    edge    edge map derived from the beauty pass
    vis     blurred RGB
    plate   the beauty render itself, unmodified

Why it is built this way
------------------------
No video model takes a mesh, a USD stage or a scene graph (see
`docs/research/video-api-geometric-control-comparison-2026-09-18.md` §9). But
every control-capable model takes *some* subset of the passes above. So the
harness rasterises its own scene graph into those modalities and keeps the
scene graph authoritative. That makes this module the durable asset: swapping
Cosmos for Wan for whatever ships next year is a backend config change, not a
rewrite.

Two rules that are not negotiable
---------------------------------
1. **Depth is normalised ONCE per shot, never per frame.** The stock
   preprocessors (VideoX-Fun's `VideoToDepth`) recompute a 2-85 percentile
   range on every frame, which makes the depth histogram pump and the model
   faithfully reproduces the breathing. Lightricks' own IC-LoRA guidance says
   the opposite - "Use consistent depth range across all frames" - and names
   "Blender/3D software" as the recommended source of synthetic depth renders.
   We take the whole-shot range from the camera's clip planes and the scene's
   measured bounds.
2. **A control pass is not a beauty render; it needs no path tracing.** `seg`
   renders with Workbench, in a fraction of a second. `depth` renders with
   Cycles at 1 sample and no denoising - not Workbench, because the depth
   override needs `Camera Data > View Z Depth`, a shader node Workbench's
   pipeline does not evaluate - but "no path tracing" still holds: 1 spp with
   denoising off costs nothing like a beauty frame at the delivery spec's 32.

fps and resolution come from the *backend*, not the spec. A backend declares a
`PassProfile`; the exporter re-times the shot's normalised animation tracks onto
that frame count, which is why tracks are stored as 0.0-1.0 of a shot in the
first place.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from collections.abc import Collection, Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import build as build_mod
from . import spec as spec_mod

# The pass names that exist. `plate` is the beauty render; it is the source for
# `edge` and `vis`, which are derived rather than rendered.
PASS_NAMES = ("plate", "depth", "seg", "edge", "vis")

# Cosmos Transfer2.5 accepts 93-480 frames per request. Staying inside that
# window is the backend's business, not this module's, but chunking is applied
# here because the frames are what we are producing.
COSMOS_FRAME_MIN = 93
COSMOS_FRAME_MAX = 480


@dataclass(frozen=True)
class PassProfile:
    """What a backend needs its control passes to look like.

    A shot is always one chunk. Multi-chunk generation existed here once and
    was wrong: each chunk re-applied the WHOLE shot's animation at its own
    frame count (see git history), so two chunks concatenated played the shot
    twice, not once split in half. It was also unreachable on `wan`, where
    `max_frames` already equalled the old `chunk_frames`. Deleted rather than
    fixed - re-add it when a real backend forces a shot past its window, and
    write the per-chunk track re-timing properly this time.
    """

    width: int
    height: int
    fps: int
    min_frames: int = 1
    max_frames: int | None = None

    def frame_count(self, seconds: float) -> int:
        """Frames this profile needs for a shot of this length.

        Refuses rather than clamps at the top end. A silent clamp here once
        rendered a 6 s shot as 81 frames at 16 fps - 5.06 s of picture - and
        `_apply_tracks` played the whole normalised animation into that
        shorter window, so the shot ran 18% fast with nothing to say so.
        """
        n = int(round(seconds * self.fps))
        n = max(self.min_frames, n)
        if self.max_frames is not None and n > self.max_frames:
            raise PassError(
                f"a {seconds}s shot needs {n} frames at {self.fps}fps, which "
                f"exceeds this backend's {self.max_frames}-frame limit. "
                "Shorten the shot, or split it into two shots - a silent "
                "clamp here plays the shot fast instead of failing."
            )
        return max(1, n)

    def chunks(self, seconds: float) -> list[int]:
        """A shot is one chunk. Kept so callers do not have to special-case it."""
        return [self.frame_count(seconds)]


class PassError(RuntimeError):
    """Raised when a pass cannot be rendered."""


# --- scene preparation ----------------------------------------------------


def _palette(index: int) -> tuple[float, float, float, float]:
    """A deterministic, well-separated colour per part index.

    Golden-angle hue stepping: no two adjacent indices land on similar hues, and
    the sequence is stable across runs, machines and Blender versions - which is
    the point. A segmentation map that changes between renders would make the
    backend's output change for no reason.
    """
    import colorsys

    hue = (index * 0.618033988749895) % 1.0
    sat = 0.55 + 0.35 * ((index * 7) % 3) / 2.0
    val = 0.65 + 0.35 * ((index * 5) % 2)
    r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
    return (r, g, b, 1.0)


def _object_colors(built: dict[str, dict[str, Any]]) -> dict[str, tuple[float, float, float, float]]:
    """Assign every object a flat colour, keyed by the part that owns it."""
    out: dict[str, tuple[float, float, float, float]] = {}
    for i, pid in enumerate(sorted(built)):
        entry = built[pid]
        col = _palette(i)
        for obj in entry.get("objs", []):
            out[obj.name] = col
    return out


def _set_engine_workbench(scene: Any) -> None:
    """Flat, unlit, object-coloured output - a segmentation map."""
    try:
        scene.render.engine = "BLENDER_WORKBENCH"
    except TypeError as exc:  # pragma: no cover - engine list differs by build
        raise PassError(f"Workbench is unavailable in this Blender build: {exc}") from exc
    shading = getattr(scene.display, "shading", None)
    if shading is not None:
        # FLAT kills the studio light so a part's colour is its identity, not
        # its shading. Outlines would add edges we did not ask for.
        for attr, value in (
            ("light", "FLAT"),
            ("color_type", "OBJECT"),
            ("show_object_outline", False),
            ("show_specular_highlight", False),
            ("show_shadows", False),
            ("show_cavity", False),
        ):
            if hasattr(shading, attr):
                try:
                    setattr(shading, attr, value)
                except (TypeError, AttributeError):
                    pass


def _depth_range(
    ep: spec_mod.Episode,
    shot: dict[str, Any],
) -> tuple[float, float]:
    """A fixed near/far for the whole shot, derived from the camera.

    **Not from geometry bounds.** Two attempts at that failed, and the failures
    are worth recording because they are the obvious thing to try:

    1. Including every part let the 240 m ground plane and a 34 m tunnel bore
       set the range, which compressed the whole subject into a sliver of grey.
    2. Excluding the enclosures let the ground plane win instead, and the map
       came out uniformly white.

    A scale derived from the camera's distance to what it is looking at is
    boring, predictable, and independent of whichever scenery happens to be in
    the file. A subject roughly at the look-at point lands mid-range; anything
    much behind it falls to black, which is what fal's own reference depth looks
    like (subject near-white, distant buildings mid-grey, sky black).

    The important property is not which constant: it is that the range is set
    **once per shot, never per frame**, so geometry entering or leaving frame
    cannot move the mapping.
    """
    cam = next((c for c in ep.cameras if c["id"] == shot["camera"]), None)
    if cam is None:
        return (0.1, 100.0)

    loc, target = cam["loc"], cam["look_at"]
    dist = sum((a - b) ** 2 for a, b in zip(loc, target, strict=True)) ** 0.5 or 1.0

    # An explicit range in the shot wins. The heuristic below is a default.
    if shot.get("depth_range"):
        near, far = shot["depth_range"]
        return (max(0.01, float(near)), max(float(near) + 0.1, float(far)))

    # Do NOT read `clip_start` / `clip_end` off the camera dict. They are not in
    # the spec's camera vocabulary, so any values present are Blender's own
    # defaults (0.1 to 100+) rather than authored intent - and preferring them
    # produced a 0.1-184.5 range in which a subject four metres away mapped to
    # 2% of the ramp, i.e. pure white. Measure from the camera instead.
    #
    # The near side is deliberately generous. Foreground context - the clay
    # face in ad02 - can sit much closer than the subject does, and if it falls
    # inside `near` it clamps to pure white and swamps the frame. Measured: at
    # 0.4 the ad02 section shots saturated to a mean of 208 of 255.
    return (max(0.01, dist * 0.22), max(dist * 0.22 + 0.1, dist * 1.9))


def _depth_override_material(near: float, far: float) -> Any:
    """An unlit emission material whose colour IS normalised view-Z depth.

    This is how the depth pass is produced, and the reasoning matters because
    the obvious approaches do not work in Blender 5.2:

    * The compositor lost `CompositorNodeComposite`, `MapRange`, `MapValue` and
      `Math`, so a Z-pass -> MapRange -> Composite graph cannot be built.
    * `CompositorNodeOutputFile` now accepts only `OPEN_EXR_MULTILAYER`.
    * Toggling `use_pass_combined = False` / `use_pass_mist = True` does **not**
      make `write_still` emit the mist pass - an earlier version of this module
      assumed it did, on the strength of a test against a plain grey cube whose
      beauty render is also grey. A confounded test produced a wrong belief;
      `LESSONS.md` records it.

    What does work is putting the depth into the beauty pipeline itself, using
    shader nodes (which still have `MapRange`). `Camera Data > View Z Depth` is
    true per-pixel camera-space depth, mapped through a **fixed** near/far set
    once per shot - which is exactly the "consistent depth range across all
    frames" rule, made mechanical rather than remembered.
    """
    import bpy

    mat = bpy.data.materials.new("brunel_depth_override")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()

    out = nt.nodes.new("ShaderNodeOutputMaterial")
    emit = nt.nodes.new("ShaderNodeEmission")
    mr = nt.nodes.new("ShaderNodeMapRange")
    cam = nt.nodes.new("ShaderNodeCameraData")

    # NEAR IS WHITE, FAR IS BLACK. Verified by rendering fal's own reference
    # depth video (the walking-woman example) and looking at it: the subject is
    # near-white, distant buildings mid-grey, sky black. An earlier version had
    # this inverted, which told the model the subject was infinitely far away
    # and produced a flat silhouette with a colour wash instead of a render.
    mr.inputs["From Min"].default_value = float(near)
    mr.inputs["From Max"].default_value = float(max(far, near + 1e-3))
    mr.inputs["To Min"].default_value = 1.0
    mr.inputs["To Max"].default_value = 0.0
    if hasattr(mr, "clamp"):
        mr.clamp = True

    nt.links.new(cam.outputs["View Z Depth"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], emit.inputs["Color"])
    nt.links.new(emit.outputs["Emission"], out.inputs["Surface"])
    return mat


def _swap_material(
    built: dict[str, dict[str, Any]], mat: Any
) -> tuple[dict[str, list[Any]], set[str]]:
    """Point every mesh at `mat`, remembering what it had.

    Returns the undo record and the names of meshes that had NO material slot
    before the override - `_restore_material` needs both, because a slot
    created here to carry the depth material has to be removed on restore, not
    zipped against an empty saved list. Restoring it as "no change" once left
    those meshes with a slot forever pointed at a material that had already
    been deleted underneath them.
    """
    saved: dict[str, list[Any]] = {}
    added_slot: set[str] = set()
    for entry in built.values():
        for obj in entry.get("objs", []):
            if getattr(obj, "type", None) != "MESH":
                continue
            saved[obj.name] = [slot.material for slot in obj.material_slots]
            if not obj.material_slots:
                obj.data.materials.append(mat)
                added_slot.add(obj.name)
            else:
                for slot in obj.material_slots:
                    slot.material = mat
    return saved, added_slot


def _restore_material(
    saved: dict[str, list[Any]], added_slot: Collection[str] = frozenset()
) -> None:
    import bpy

    for name, mats in saved.items():
        obj = bpy.data.objects.get(name)
        if obj is None:
            continue
        if name in added_slot:
            if obj.data.materials:
                obj.data.materials.pop()
            continue
        # strict=False, deliberately. A restore runs as cleanup, and raising
        # part-way through would leave every object after this one still
        # swapped to a pass material - a worse fault than a partial restore,
        # and one that would silently contaminate the next shot's render.
        for slot, mat in zip(obj.material_slots, mats, strict=False):
            slot.material = mat


def _restore_render_passes(scene: Any) -> None:
    """Put the view layer back to writing a normal combined render."""
    view_layer = scene.view_layers[0]
    if hasattr(view_layer, "use_pass_mist"):
        view_layer.use_pass_mist = False
    if hasattr(view_layer, "use_pass_combined"):
        view_layer.use_pass_combined = True


def _run_ffmpeg(args: Sequence[str]) -> None:
    exe = shutil.which("ffmpeg")
    if not exe:
        raise PassError("ffmpeg is required for the edge and vis passes")
    proc = subprocess.run([exe, "-y", "-hide_banner", "-loglevel", "error", *args],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise PassError(f"ffmpeg failed ({proc.returncode}): {proc.stderr.strip()[:400]}")


def _derive_edge(src_dir: Path, dst_dir: Path, frames: int) -> int:
    """Edge map from the beauty pass, via ffmpeg's edgedetect.

    Deliberately not Freestyle and deliberately not OpenCV: Freestyle needs a
    second full render configuration, and cv2 is not a dependency of this repo.
    ffmpeg already is.
    """
    dst_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in range(1, frames + 1):
        src = src_dir / f"frame_{f:04d}.png"
        if not src.exists():
            continue
        _run_ffmpeg(["-i", str(src), "-vf", "edgedetect=low=0.05:high=0.20",
                     str(dst_dir / f"frame_{f:04d}.png")])
        n += 1
    return n


def _derive_vis(src_dir: Path, dst_dir: Path, frames: int) -> int:
    """Blurred RGB. Cosmos can auto-extract this from RGB, but supplying it is
    cheaper than letting each backend guess."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in range(1, frames + 1):
        src = src_dir / f"frame_{f:04d}.png"
        if not src.exists():
            continue
        _run_ffmpeg(["-i", str(src), "-vf", "gblur=sigma=6",
                     str(dst_dir / f"frame_{f:04d}.png")])
        n += 1
    return n


# --- the exporter ---------------------------------------------------------


def render_passes(
    ep: spec_mod.Episode,
    *,
    out_root: Path,
    profile: PassProfile,
    passes: Iterable[str] = PASS_NAMES,
    shots: Sequence[str] | None = None,
    device: str | None = None,
    quiet: bool = False,
    frames_override: int | None = None,
) -> dict[str, Any]:
    """Render the requested control passes for the requested shots.

    Returns a manifest describing exactly what was written, including the depth
    range used per shot - which is the number a reviewer needs to know was held
    constant.
    """
    import bpy

    wanted = tuple(p for p in PASS_NAMES if p in set(passes))
    unknown = set(passes) - set(PASS_NAMES)
    if unknown:
        raise PassError(f"unknown pass(es): {sorted(unknown)}; known: {list(PASS_NAMES)}")

    if device:
        ep = ep.with_overrides()
        ep.meta["device"] = device

    ep_dir = Path(out_root) / ep.id
    ep_dir.mkdir(parents=True, exist_ok=True)

    built = build_mod.build_scene(ep)
    scene = bpy.context.scene
    cameras = {c["id"]: c for c in ep.cameras}
    colors = _object_colors(built) if "seg" in wanted else {}

    # Spec frame-rate animation is re-timed by the renderer; the profile's fps
    # only decides how many frames we sample it at.
    selected = [s for s in ep.shots if not shots or s["id"] in set(shots)]
    if not selected:
        raise PassError(f"no shots matched {shots!r}")

    manifest: dict[str, Any] = {
        "episode": ep.id,
        "profile": {
            "width": profile.width, "height": profile.height,
            "fps": profile.fps, "max_frames": profile.max_frames,
        },
        "spec_fps": int(ep.meta["fps"]),
        "passes": list(wanted),
        "shots": [],
    }

    saved = {
        "x": scene.render.resolution_x,
        "y": scene.render.resolution_y,
        "pct": scene.render.resolution_percentage,
    }

    try:
        scene.render.resolution_x = profile.width
        scene.render.resolution_y = profile.height
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = "PNG"

        for shot in selected:
            seconds = float(shot["seconds"])
            # A shot is one chunk (see PassProfile). frame_count() raises if the
            # shot does not fit the backend's window - fail here, before any
            # pixel is rendered, not after.
            count = profile.frame_count(seconds)
            if frames_override:
                # A smoke-test cap. Iterating on a storyboard should not require
                # the full frame count before you can see whether the staging
                # is right - the same reason `render --stills` exists.
                count = max(1, int(frames_override))
            chunk_tag = "c00"
            shot_dir = ep_dir / shot["id"]
            shot_dir.mkdir(parents=True, exist_ok=True)

            near, far = _depth_range(ep, shot)
            record: dict[str, Any] = {
                "shot": shot["id"],
                "name": shot["name"],
                "seconds": seconds,
                "chunks": [count],
                "frames_total": count,
                "depth_range": [round(near, 4), round(far, 4)] if "depth" in wanted else None,
                "passes": {},
            }

            if not quiet:
                print(f"  {shot['id']:<4} {shot['name'][:26]:<28} "
                      f"{count:>4} fr @ {profile.fps} fps  "
                      f"{profile.width}x{profile.height}")

            # Tracks are 0.0-1.0 of a shot, so the same spec animates correctly
            # at 16 fps as at 30 - that is why they are stored normalised.
            from . import render as render_mod

            render_mod._reset_parts(ep, built)
            render_mod._set_visibility(ep, built, shot["id"])
            render_mod._apply_tracks(ep, built, shot["id"], count)

            cam = cameras[shot["camera"]]
            cam_obj = bpy.data.objects[shot["camera"]]
            cam_obj.animation_data_clear()
            cam_obj.location = tuple(cam["loc"])
            build_mod.aim(cam_obj, cam["look_at"])
            scene.camera = cam_obj
            render_mod._apply_camera_move(cam_obj, shot, count)

            scene.frame_start = 1
            scene.frame_end = count

            for pass_name in wanted:
                if pass_name in ("edge", "vis"):
                    continue  # derived from plate below
                started = time.time()
                n = _render_one_pass(
                    scene, built, shot_dir, chunk_tag, pass_name, count,
                    colors=colors, near=near, far=far,
                )
                record["passes"].setdefault(pass_name, {})[chunk_tag] = {
                    "frames": n,
                    "dir": str(shot_dir / pass_name / chunk_tag),
                    "seconds": round(time.time() - started, 2),
                }
                if not quiet:
                    print(f"        {pass_name:<6} {n:>4} frames  "
                          f"{time.time() - started:>6.1f}s")

            # Derive edge and vis from the plate once, per shot.
            for derived in ("edge", "vis"):
                if derived not in wanted or "plate" not in record["passes"]:
                    continue
                total = record["passes"]["plate"].get("c00", {}).get("frames", 0)
                if not total:
                    continue
                started = time.time()
                src = shot_dir / "plate" / "c00"
                dst = shot_dir / derived / "c00"
                fn = _derive_edge if derived == "edge" else _derive_vis
                n = fn(src, dst, total)
                record["passes"][derived] = {
                    "c00": {"frames": n, "dir": str(dst),
                            "seconds": round(time.time() - started, 2)}
                }
                if not quiet:
                    print(f"        {derived:<6} {n:>4} frames  "
                          f"{time.time() - started:>6.1f}s")

            manifest["shots"].append(record)

    finally:
        _restore_render_passes(scene)
        scene.render.resolution_x = saved["x"]
        scene.render.resolution_y = saved["y"]
        scene.render.resolution_percentage = saved["pct"]
        try:
            scene.render.engine = ep.meta["engine"]
        except TypeError:
            pass

    (ep_dir / "passes.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def _render_one_pass(
    scene: Any,
    built: dict[str, dict[str, Any]],
    shot_dir: Path,
    chunk_tag: str,
    pass_name: str,
    frames: int,
    *,
    colors: dict[str, tuple[float, float, float, float]],
    near: float,
    far: float,
) -> int:
    """Render one pass over `frames` frames. Returns the count written."""
    import bpy

    dst = shot_dir / pass_name / chunk_tag
    dst.mkdir(parents=True, exist_ok=True)

    original_engine = scene.render.engine
    original_film = scene.render.film_transparent
    original_view = getattr(scene.view_settings, "view_transform", None)
    saved_mats: dict[str, list[Any]] = {}
    added_slot: set[str] = set()
    depth_mat = None
    saved_world = None

    # A control pass is DATA, not a picture. The episode's AgX view transform is
    # right for the beauty render and wrong for depth and segmentation: AgX is a
    # filmic curve, so it compresses and bends the range. Depth through AgX came
    # out spanning 0.48-0.77 instead of 0-1, which is not a linear function of
    # distance - and a warped depth map is a warped scene as far as the model is
    # concerned. Standard keeps the encoding linear.
    if pass_name in ("depth", "seg") and original_view is not None:
        try:
            scene.view_settings.view_transform = "Standard"
        except TypeError:
            pass

    if pass_name == "depth":
        # Add a white emission material to the world cost nothing to undo.
        mat = _depth_override_material(near, far)
        depth_mat = mat
        scene.render.engine = "CYCLES"
        try:
            scene.cycles.samples = 1
            scene.cycles.use_denoising = False
        except AttributeError:
            pass
        scene.render.film_transparent = False
        # No geometry means infinitely distant, and far is BLACK under the
        # near-white convention above.
        world = getattr(scene, "world", None)
        if world is not None and world.use_nodes and world.node_tree:
            bg = world.node_tree.nodes.get("Background")
            if bg is not None:
                saved_world = tuple(bg.inputs["Color"].default_value)
                bg.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
                if "Strength" in bg.inputs:
                    bg.inputs["Strength"].default_value = 1.0
        saved_mats, added_slot = _swap_material(built, mat)
        if not saved_mats:
            raise PassError("no mesh objects were found to carry the depth override")

    elif pass_name == "seg":
        _set_engine_workbench(scene)
        scene.render.film_transparent = False
        for name, col in colors.items():
            obj = bpy.data.objects.get(name)
            if obj is not None:
                obj.color = col

    elif pass_name == "plate":
        scene.render.engine = original_engine

    else:  # pragma: no cover - guarded by PASS_NAMES
        raise PassError(f"unknown pass {pass_name!r}")

    try:
        written = 0
        for f in range(1, frames + 1):
            scene.frame_set(f)
            scene.render.filepath = str(dst / f"frame_{f:04d}")
            bpy.ops.render.render(write_still=True)
            written += 1
    finally:
        _restore_render_passes(scene)
        if saved_mats:
            _restore_material(saved_mats, added_slot)
        if depth_mat is not None:
            try:
                bpy.data.materials.remove(depth_mat)
            except (RuntimeError, ReferenceError):
                pass
        if saved_world is not None:
            world = getattr(scene, "world", None)
            if world is not None and world.use_nodes and world.node_tree:
                bg = world.node_tree.nodes.get("Background")
                if bg is not None:
                    bg.inputs["Color"].default_value = saved_world
        scene.render.engine = original_engine
        scene.render.film_transparent = original_film
        if original_view is not None:
            try:
                scene.view_settings.view_transform = original_view
            except TypeError:
                pass
    return written


__all__ = [
    "PASS_NAMES", "PassProfile", "PassError",
    "render_passes", "COSMOS_FRAME_MIN", "COSMOS_FRAME_MAX",
]
