"""Frames -> mp4. The edit is a build artefact, not a manual act."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .tools import duration_seconds, ffmpeg, run


class AssembleError(Exception):
    pass


def _run(cmd: list[str]) -> None:
    run(cmd, error=AssembleError)


def _shot_dirs(ep_dir: Path, order: list[str] | None = None) -> list[Path]:
    """The shot directories to cut, IN EDIT ORDER.

    `order` is the spec's shot list, which `manifest.json` already records. It
    matters for two reasons, and this function used to get both wrong by
    globbing the directory and sorting the result:

    * **Filesystem sort is not edit order.** It agrees with the spec only while
      every shot id happens to sort the way it is listed. Ids `s1, s2, s10` cut
      in the order 1, 10, 2; narrative ids (`open`, `dig`, `advance`) cut
      alphabetically. Silently, into the deliverable.
    * **A directory is not a shot list.** Rename or drop a shot and its old
      frames stay on disk; the glob put them straight back into the cut. Only
      the spec knows which shots exist, so an unexpected frame directory is a
      hard error, not something to quietly include.
    """
    on_disk = {d.name: d for d in ep_dir.iterdir()
               if d.is_dir() and any(d.glob("frame_*.png"))}
    if not on_disk:
        raise AssembleError(f"no rendered frames under {ep_dir}")
    if order is None:
        # No manifest to read: the old behaviour, and still wrong for the two
        # reasons above. Say so rather than presenting the guess as an edit.
        print(f"  warn: no manifest.json in {ep_dir} - cutting in filename order, "
              f"which is not necessarily the spec's shot order")
        return [on_disk[name] for name in sorted(on_disk)]

    missing = [sid for sid in order if sid not in on_disk]
    if missing:
        raise AssembleError(
            f"{ep_dir}: the spec declares shot(s) {missing} but there are no "
            f"frames for them. Re-run `render` - it resumes from the last "
            f"completed frame. Cutting without them would ship a short video."
        )
    orphans = sorted(set(on_disk) - set(order))
    if orphans:
        raise AssembleError(
            f"{ep_dir}: frame directories {orphans} are not shots in this spec - "
            f"left over from a renamed or deleted shot, or from a `--shots` run "
            f"that rewrote manifest.json with a partial list. They would have "
            f"been cut into the video. Delete them, or re-render the whole spec."
        )
    return [on_disk[sid] for sid in order]


def assemble(
    ep_dir: Path,
    *,
    out_path: Path | None = None,
    fps: int | None = None,
    crf: int = 18,
    shots: list[str] | None = None,
) -> dict[str, Any]:
    """Encode each shot, then concat. Per-shot encode keeps re-renders cheap.

    `shots` is the spec's shot list, in spec order - the authoritative edit
    order. A caller that has the `Episode` should pass it; `manifest.json` is
    the fallback for a bare `harness assemble <dir>`, and is only as complete as
    the last render that wrote it.
    """
    ep_dir = Path(ep_dir)
    manifest_path = ep_dir / "manifest.json"
    # The manifest already carries a shot list, in spec order, written by
    # `build.write_manifest`. Reading the order from it costs nothing and is
    # what stops the cut being assembled in filename order - see `_shot_dirs`.
    order = list(shots) if shots else None
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        if fps is None:
            fps = int(manifest["fps"])
        if order is None:
            order = list(manifest.get("shots") or []) or None
    if fps is None:
        fps = 24

    tmp = ep_dir / "_parts"
    tmp.mkdir(exist_ok=True)
    parts: list[Path] = []

    for shot_dir in _shot_dirs(ep_dir, order):
        part = tmp / f"{shot_dir.name}.mp4"
        _run([
            ffmpeg(), "-y", "-loglevel", "error",
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
        ffmpeg(), "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(listing),
        "-c", "copy", str(out_path),
    ])

    # Size comes from the filesystem, not from ffprobe. A second subprocess to
    # ask how big a file we just wrote is, is a subprocess that can fail and
    # report 0 MB for a cut that exists.
    result = {
        "output": str(out_path),
        "shots": [p.stem for p in parts],
        "fps": fps,
        "duration_s": round(duration_seconds(out_path), 2),
        "size_mb": round(out_path.stat().st_size / 1_048_576, 2),
    }
    print(f"  {out_path}  {result['duration_s']}s  {result['size_mb']} MB  ({len(parts)} shots)")
    return result
