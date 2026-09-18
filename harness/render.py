"""Headless rendering. Spec in, PNG frames out.

Owns per-shot staging: which parts are visible, what each part's transform is
doing over time, and where the camera is looking.
"""

from __future__ import annotations

import hashlib
import json
import math
import shutil
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import bpy
from mathutils import Euler

from . import build as build_mod
from . import spec as spec_mod


def _fcurves(action: Any) -> list[Any]:
    """Enumerate F-curves across both the legacy and the slotted Action API.

    Blender 4.4+ introduced slotted actions and the legacy ``action.fcurves``
    accessor is on its way out. Handle both rather than betting on one.
    """
    fcs = getattr(action, "fcurves", None)
    if fcs is not None:
        try:
            return list(fcs)
        except (AttributeError, TypeError, RuntimeError):
            pass
    out: list[Any] = []
    for layer in getattr(action, "layers", None) or []:
        for strip in getattr(layer, "strips", None) or []:
            for bag in getattr(strip, "channelbags", None) or []:
                out.extend(list(getattr(bag, "fcurves", None) or []))
    return out


def _smooth(obj: Any) -> None:
    """Ease in AND out. A Linear handle on a camera move is an automatic fail."""
    action = obj.animation_data.action if obj.animation_data else None
    if action is None:
        return
    for fc in _fcurves(action):
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
            kp.handle_left_type = "AUTO_CLAMPED"
            kp.handle_right_type = "AUTO_CLAMPED"


def _frame_ok(path: Path) -> bool:
    """A rendered frame is a real file, not a zero-byte stub from a killed run."""
    try:
        return path.stat().st_size > 1024
    except OSError:
        return False


def _fingerprint(
    ep: spec_mod.Episode, shot: dict[str, Any], frames: int, stills_only: bool,
    max_frames: int | None = None,
) -> str:
    """Everything that can change the pixels, hashed.

    Including the whole spec text means any spec edit invalidates the cache for
    every shot. That is deliberately conservative: silently mixing frames from
    two different scenes is far worse than re-rendering.
    """
    spec_text = ""
    if ep.source and Path(ep.source).exists():
        spec_text = Path(ep.source).read_text(encoding="utf-8")
    payload = json.dumps(
        {
            "spec": spec_text,
            "episode": ep.id,
            "shot": shot,
            "frames": frames,
            "stills_only": stills_only,
            "max_frames": max_frames,
            "width": ep.meta["width"],
            "height": ep.meta["height"],
            "samples": ep.meta["samples"],
            "engine": ep.meta["engine"],
            "device": ep.meta["device"],
            "fps": ep.meta["fps"],
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _reset_parts(ep: spec_mod.Episode, built: dict[str, dict[str, Any]]) -> None:
    """Return every part to its spec pose and drop any leftover animation."""
    for entry in built.values():
        root = entry["root"]
        root.animation_data_clear()
        p = entry["spec"]
        root.location = tuple(p["loc"])
        root.rotation_euler = tuple(math.radians(v) for v in p["rot"])
        root.scale = tuple(p["scale"])


def _set_visibility(
    ep: spec_mod.Episode, built: dict[str, dict[str, Any]], shot_id: str
) -> int:
    """Hide parts that do not belong to this shot.

    Hiding a parent Empty does NOT hide its children in Blender's renderer, so
    the mesh objects are flagged directly.
    """
    visible = 0
    for entry in built.values():
        show = (not entry["shots"]) or (shot_id in entry["shots"])
        for obj in entry["objs"]:
            obj.hide_render = not show
        if show:
            visible += 1

    # Lights are scoped per shot too: daylight above ground, near-darkness
    # inside the tunnel. At L0 that IS the lighting design.
    for li in ep.lights:
        obj = bpy.data.objects.get(li["id"])
        if obj is None:
            continue
        scope = li["shots"]
        obj.hide_render = bool(scope) and shot_id not in scope
    return visible


def spin_euler(base_deg: Sequence[float], degrees: float) -> tuple[float, float, float]:
    """The part's own orientation, turned `degrees` about its OWN Z axis.

    Turning about its own axis is the only thing a screw can do, and the one
    thing a raw Euler track cannot express. Blender's XYZ order is
    R = Rz.Ry.Rx, so Z is applied **last**: writing the spin into the `.z` slot
    rotates the already-laid shaft about the *world* Z axis and the screw sweeps
    round like a propeller. That bug shipped once, cost a paid generation, and
    passed every per-frame pixel check because each individual frame was a
    perfectly good picture.

    The composition is `R_base @ R_spin` - a rotation about local Z applied
    *before* the part's own orientation - which is what "turn the screw" means
    for any base rot. The invariant that distinguishes it from the bug, and the
    one `tests/run.sh` asserts: **the part's local Z axis is unchanged by the
    spin.** A propeller sweep moves it.

    Public (no underscore) because it is the numeric core of the repo's most
    expensive bug, and a test that re-implemented it would drift from it.
    """
    r_base = Euler([math.radians(x) for x in base_deg], "XYZ").to_matrix()
    r_spin = Euler((0.0, 0.0, math.radians(degrees)), "XYZ").to_matrix()
    e = (r_base @ r_spin).to_euler("XYZ")
    return (e.x, e.y, e.z)


def _apply_tracks(
    ep: spec_mod.Episode,
    built: dict[str, dict[str, Any]],
    shot_id: str,
    total_frames: int,
) -> int:
    """Key a part's transform over the shot.

    Track time in the spec is normalised 0.0-1.0, so it is scaled to this
    shot's actual frame count here.
    """
    n = 0
    span = max(1, total_frames - 1)
    for t in ep.tracks_for_shot(shot_id):
        chan = t["channel"]
        # A track may drive one part or an assembly. `part = ["a","b","c"]` is
        # the difference between remembering to track all six pieces of a moving
        # cell and forgetting one. The key existed; nothing used it.
        parts = t["part"] if isinstance(t["part"], list) else [t["part"]]
        offset = t.get("mode") == "offset"
        for pid in parts:
            entry = built[pid]
            root = entry["root"]
            # With mode = "offset" the track values are a DELTA from the part's
            # declared location, so one track can drive an assembly whose pieces
            # sit in different places. Without it, moving six parts of a cell
            # together needs six tracks with six different absolute vectors -
            # and forgetting one leaves a piece behind, which is exactly the bug
            # class this removes.
            base = entry["spec"].get("loc") or [0.0, 0.0, 0.0]
            # strict=True: spec.py already refuses a track whose frames and
            # values differ in length, so this asserts that invariant at the
            # point of use rather than silently dropping a keyframe.
            for frac, v in zip(t["frames"], t["values"], strict=True):
                f = 1 + round(frac * span)
                if chan == "location":
                    got = [b + d for b, d in zip(base, v, strict=True)] if offset else list(v)
                    root.location = tuple(got)
                    root.keyframe_insert(data_path="location", frame=f)
                elif chan == "rotation":
                    root.rotation_euler = tuple(math.radians(x) for x in v)
                    root.keyframe_insert(data_path="rotation_euler", frame=f)
                elif chan == "scale":
                    root.scale = tuple(v)
                    root.keyframe_insert(data_path="scale", frame=f)
                elif chan == "spin":
                    root.rotation_euler = spin_euler(
                        entry["spec"].get("rot") or [0.0, 0.0, 0.0], v[2])
                    root.keyframe_insert(data_path="rotation_euler", frame=f)
            _smooth(root)
            n += 1
    return n


def _apply_camera_move(camera: Any, shot: dict[str, Any], last_frame: int) -> None:
    if not shot.get("move_from") or not shot.get("move_to"):
        return
    camera.location = tuple(shot["move_from"])
    camera.keyframe_insert(data_path="location", frame=1)
    camera.location = tuple(shot["move_to"])
    camera.keyframe_insert(data_path="location", frame=last_frame)
    _smooth(camera)


def render(
    ep: spec_mod.Episode,
    *,
    out_root: Path,
    device: str | None = None,
    quiet: bool = False,
    stills_only: bool = False,
    force: bool = False,
    max_frames: int | None = None,
) -> dict[str, Any]:
    """Build the scene and render every shot to ``out_root/<episode>/<shot>/``.

    ``stills_only`` renders just the middle frame of each shot - the cheap
    storyboard pass you run BEFORE committing an hour to the full render.

    ``max_frames`` caps how many frames of each shot are rendered. It exists for
    `harness bench`: measuring s/frame at delivery resolution must not mean
    rendering the whole cut. It is part of the cache fingerprint, so a capped
    run can never be mistaken for a complete one.
    """
    if device:
        ep = ep.with_overrides()
        ep.meta["device"] = device

    ep_dir = Path(out_root) / ep.id
    ep_dir.mkdir(parents=True, exist_ok=True)

    built = build_mod.build_scene(ep)
    build_mod.write_manifest(ep, built, ep_dir / "manifest.json")
    bpy.ops.wm.save_as_mainfile(filepath=str(ep_dir / f"{ep.id}.blend"), compress=True)

    scene = bpy.context.scene
    fps = int(ep.meta["fps"])
    cameras = {c["id"]: c for c in ep.cameras}
    results: list[dict[str, Any]] = []

    for shot in ep.shots:
        frames = ep.frame_count(shot, fps)

        _reset_parts(ep, built)
        n_parts = _set_visibility(ep, built, shot["id"])
        n_tracks = _apply_tracks(ep, built, shot["id"], frames)

        cam = cameras[shot["camera"]]
        cam_obj = bpy.data.objects[shot["camera"]]
        cam_obj.animation_data_clear()
        cam_obj.location = tuple(cam["loc"])
        build_mod.aim(cam_obj, cam["look_at"])
        scene.camera = cam_obj

        _apply_camera_move(cam_obj, shot, frames)
        scene.frame_start = 1
        scene.frame_end = frames

        shot_dir = ep_dir / shot["id"]
        # Stills pass renders the MIDDLE frame of each shot - the moment the
        # staging is most representative.
        frame_list = [max(1, frames // 2)] if stills_only else list(range(1, frames + 1))
        if max_frames is not None:
            frame_list = frame_list[:max_frames]

        # Per-shot resume. A run that dies at frame 800 must not re-render the
        # 799 in front of it, and a spec change must invalidate the cache
        # rather than silently mix frames from two different scenes.
        stamp_path = shot_dir / ".render.json"
        fingerprint = _fingerprint(ep, shot, frames, stills_only, max_frames)
        prior: dict[str, Any] = {}
        if stamp_path.exists():
            try:
                prior = json.loads(stamp_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                prior = {}

        if force or prior.get("fingerprint") != fingerprint:
            if shot_dir.exists():
                shutil.rmtree(shot_dir)
            shot_dir.mkdir(parents=True, exist_ok=True)
            pending = frame_list
        else:
            shot_dir.mkdir(parents=True, exist_ok=True)
            pending = [f for f in frame_list
                       if not _frame_ok(shot_dir / f"frame_{f:04d}.png")]

        cached = len(frame_list) - len(pending)
        if not quiet:
            print(
                f"  {shot['id']:<4} {shot['name'][:26]:<28} {frames:>4} fr  "
                f"{n_parts:>2} parts  {n_tracks} tracks  "
                f"{len(pending):>4} to render"
                + (f"  ({cached} cached)" if cached else "")
            )

        started = time.time()
        for n, f in enumerate(pending, 1):
            scene.frame_set(f)
            # write_still writes to the literal filepath and only appends the
            # extension - it does NOT substitute the frame number. Put the
            # frame number in the path ourselves or every frame overwrites
            # the last one and you render 48 frames to get 1 file.
            scene.render.filepath = str(shot_dir / f"frame_{f:04d}")
            bpy.ops.render.render(write_still=True)
            step = max(1, len(pending) // 4)
            if not quiet and n % step == 0:
                elapsed = time.time() - started
                rate = elapsed / n
                print(f"        {n:>4}/{len(pending)}  {rate:.2f}s/frame  "
                      f"elapsed {elapsed:.0f}s  eta {rate * (len(pending) - n):.0f}s")

        render_seconds = round(time.time() - started, 2)

        stamp_path.write_text(
            json.dumps(
                {
                    "fingerprint": fingerprint,
                    "frames": len(frame_list),
                    "stills_only": stills_only,
                    "resolution": [ep.meta["width"], ep.meta["height"]],
                    "samples": ep.meta["samples"],
                    "fps": fps,
                },
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )

        results.append(
            {
                "shot": shot["id"],
                "name": shot["name"],
                "frames": frames,
                "frames_rendered": len(pending),
                "frames_cached": cached,
                "seconds": round(frames / fps, 3),
                # Measured, and measured AFTER build_scene - so this is a
                # steady-state per-frame cost, not a short run with the
                # scene-construction cost smeared through it. render-bench.json
                # was wrong about mvp for exactly that reason.
                "render_seconds": render_seconds,
                "sec_per_frame": round(render_seconds / len(pending), 3) if pending else None,
                "dir": str(shot_dir),
                "parts_visible": n_parts,
                "tracks": n_tracks,
                "narration": shot.get("narration", ""),
            }
        )

    total = sum(r["frames"] for r in results)
    done = sum(r["frames_rendered"] for r in results)
    kept = sum(r["frames_cached"] for r in results)
    if not quiet:
        print(f"  rendered {done}/{total} frames across {len(results)} shot(s)"
              + (f", {kept} reused from cache" if kept else "")
              + f" -> {ep_dir}")
    # Report the device that was USED, not the one the spec asked for. render()
    # applies --device to its own copy of the episode, so a caller reading
    # ep.meta["device"] afterwards gets the spec's value and records a
    # measurement against hardware that never ran it.
    return {"episode": ep.id, "fps": fps, "shots": results, "frames_total": total,
            "frames_rendered": done, "duration_s": round(total / fps, 2),
            "device": ep.meta["device"], "resolution": [ep.meta["width"], ep.meta["height"]],
            "samples": ep.meta["samples"]}
