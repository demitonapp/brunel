"""Headless rendering. Spec in, PNG frames out."""

from __future__ import annotations

import shutil
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


def _apply_camera_move(camera: Any, shot: dict[str, Any], last_frame: int) -> None:
    """Keyframe a camera push, with ease in AND ease out.

    A Linear interpolation handle on a camera move is an automatic L1 failure,
    so it is set correctly here rather than caught in review.
    """
    if not shot.get("move_from") or not shot.get("move_to"):
        return
    camera.location = tuple(shot["move_from"])
    camera.keyframe_insert(data_path="location", frame=1)
    camera.location = tuple(shot["move_to"])
    camera.keyframe_insert(data_path="location", frame=last_frame)

    action = camera.animation_data.action if camera.animation_data else None
    if action is None:
        return
    for fc in _fcurves(action):
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
            kp.handle_left_type = "AUTO_CLAMPED"
            kp.handle_right_type = "AUTO_CLAMPED"


def render(
    ep: spec_mod.Episode,
    *,
    out_root: Path,
    device: str | None = None,
    quiet: bool = False,
) -> dict[str, Any]:
    """Build the scene and render every shot to ``out_root/<episode>/<shot>/``."""
    if device:
        ep = ep.with_overrides()  # defensive copy
        ep.meta["device"] = device

    ep_dir = out_root / ep.id
    ep_dir.mkdir(parents=True, exist_ok=True)

    build_mod.build(
        ep,
        blend_path=ep_dir / f"{ep.id}.blend",
        manifest_path=ep_dir / "manifest.json",
    )

    scene = bpy.context.scene
    fps = int(ep.meta["fps"])
    cameras = {c["id"]: c for c in ep.cameras}
    results: list[dict[str, Any]] = []

    for shot in ep.shots:
        cam_obj = bpy.data.objects[shot["camera"]]
        # Re-aim from the spec each time; a move overrides the static aim.
        cam_obj.animation_data_clear()
        cam_obj.location = tuple(cameras[shot["camera"]]["loc"])
        build_mod._aim(cam_obj, cameras[shot["camera"]]["look_at"])
        scene.camera = cam_obj

        frames = ep.frame_count(shot, fps)
        _apply_camera_move(cam_obj, shot, frames)
        scene.frame_start = 1
        scene.frame_end = frames

        shot_dir = ep_dir / shot["id"]
        if shot_dir.exists():
            shutil.rmtree(shot_dir)
        shot_dir.mkdir(parents=True, exist_ok=True)
        if not quiet:
            print(
                f"  shot {shot['id']:<5} {shot['name'][:28]:<30} "
                f"{frames:>4} frames @ {ep.meta['width']}x{ep.meta['height']} "
                f"{ep.meta['samples']}spp ({ep.meta['engine']})"
            )

        for f in range(1, frames + 1):
            scene.frame_set(f)
            # write_still writes to the literal filepath and only appends the
            # extension - it does NOT substitute the frame number. Put the
            # frame number in the path ourselves or every frame overwrites
            # the last one and you render 48 frames to get 1 file.
            scene.render.filepath = str(shot_dir / f"frame_{f:04d}")
            bpy.ops.render.render(write_still=True)

        results.append(
            {
                "shot": shot["id"],
                "name": shot["name"],
                "frames": frames,
                "dir": str(shot_dir),
                "seconds": frames / fps,
            }
        )

    total = sum(r["frames"] for r in results)
    if not quiet:
        print(f"  rendered {total} frames across {len(results)} shot(s) -> {ep_dir}")
    return {"episode": ep.id, "fps": fps, "shots": results, "frames_total": total}
