"""Frames -> mp4. The edit is a build artefact, not a manual act."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"


class AssembleError(Exception):
    pass


def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise AssembleError(
            f"command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stderr[-2000:]}"
        )


def _shot_dirs(ep_dir: Path) -> list[Path]:
    found = [
        d for d in sorted(ep_dir.iterdir())
        if d.is_dir() and any(d.glob("frame_*.png"))
    ]
    if not found:
        raise AssembleError(f"no rendered frames under {ep_dir}")
    return found


def assemble(
    ep_dir: Path,
    *,
    out_path: Path | None = None,
    fps: int | None = None,
    crf: int = 18,
) -> dict[str, Any]:
    """Encode each shot, then concat. Per-shot encode keeps re-renders cheap."""
    ep_dir = Path(ep_dir)
    manifest_path = ep_dir / "manifest.json"
    if fps is None:
        fps = 24
        if manifest_path.exists():
            fps = int(json.loads(manifest_path.read_text())["fps"])

    tmp = ep_dir / "_parts"
    tmp.mkdir(exist_ok=True)
    parts: list[Path] = []

    for shot_dir in _shot_dirs(ep_dir):
        part = tmp / f"{shot_dir.name}.mp4"
        _run([
            FFMPEG, "-y", "-loglevel", "error",
            "-framerate", str(fps),
            "-i", str(shot_dir / "frame_%04d.png"),
            "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
            "-pix_fmt", "yuv420p", str(part),
        ])
        parts.append(part)

    listing = tmp / "concat.txt"
    listing.write_text("".join(f"file '{p.name}'\n" for p in parts), encoding="utf-8")

    if out_path is None:
        out_path = ep_dir / f"{ep_dir.name}.mp4"
    _run([
        FFMPEG, "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(listing),
        "-c", "copy", str(out_path),
    ])

    probe = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration,size",
         "-of", "json", str(out_path)],
        capture_output=True, text=True,
    )
    info = json.loads(probe.stdout or "{}").get("format", {})
    result = {
        "output": str(out_path),
        "shots": [p.stem for p in parts],
        "fps": fps,
        "duration_s": round(float(info.get("duration", 0.0)), 2),
        "size_mb": round(float(info.get("size", 0)) / 1_048_576, 2),
    }
    print(f"  {out_path}  {result['duration_s']}s  {result['size_mb']} MB  ({len(parts)} shots)")
    return result
