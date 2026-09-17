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
from pathlib import Path
from typing import Any

import bpy

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
    ep: spec_mod.Episode, shot: dict[str, Any], frames: int, stills_only: bool
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
        root = built[t["part"]]["root"]
        chan = t["channel"]
        for frac, v in zip(t["frames"], t["values"]):
            f = 1 + round(frac * span)
            if chan == "location":
                root.location = tuple(v)
                root.keyframe_insert(data_path="location", frame=f)
            elif chan == "rotation":
                root.rotation_euler = tuple(math.radians(x) for x in v)
                root.keyframe_insert(data_path="rotation_euler", frame=f)
            elif chan == "scale":
                root.scale = tuple(v)
                root.keyframe_insert(data_path="scale", frame=f)
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
) -> dict[str, Any]:
    """Build the scene and render every shot to ``out_root/<episode>/<shot>/``.

    ``stills_only`` renders just the middle frame of each shot - the cheap
    storyboard pass you run BEFORE committing an hour to the full render.
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

        # Per-shot resume. A run that dies at frame 800 must not re-render the
        # 799 in front of it, and a spec change must invalidate the cache
        # rather than silently mix frames from two different scenes.
        stamp_path = shot_dir / ".render.json"
        fingerprint = _fingerprint(ep, shot, frames, stills_only)
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
    return {"episode": ep.id, "fps": fps, "shots": results, "frames_total": total,
            "frames_rendered": done, "duration_s": round(total / fps, 2)}
