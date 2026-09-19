"""Finding the external tools, and the one question everything asks ffprobe.

Seven modules resolved ffmpeg for themselves, in two incompatible ways.
`assemble`, `captions` and `audio` used a module constant:

    FFMPEG = shutil.which("ffmpeg") or "ffmpeg"

which does not fail when ffmpeg is absent - it defers to `subprocess`, which
raises `FileNotFoundError: 'ffmpeg'` from inside whichever helper ran first.
`check`, `passes` and `backend` each raised their own readable error instead,
and `__main__` printed its own message and returned 2. One behaviour, four
spellings, and the worst of them was the default in three files.

`doctor` deliberately does NOT use this module. Reporting that a tool is
missing is its entire job, so `shutil.which` returning None is the answer
there, not an error.
"""
from __future__ import annotations

import shutil
import subprocess
from functools import cache
from pathlib import Path


class ToolError(Exception):
    """A required external tool is missing, or could not answer.

    Distinct from a failed check: nothing was measured, so nothing passed.
    `main()` catches it and exits 2.
    """


@cache
def _resolve(name: str) -> str:
    exe = shutil.which(name)
    if not exe:
        raise ToolError(f"{name} is required and is not on PATH")
    return exe


def ffmpeg() -> str:
    return _resolve("ffmpeg")


def ffprobe() -> str:
    return _resolve("ffprobe")


def duration_seconds(path: Path) -> float:
    """A media file's duration in seconds.

    Raises rather than returning 0.0 on failure, which is what all three
    previous copies of this function did. In `__main__` that default was
    harmless - every caller compares the result against the spec and refuses a
    mismatch, so 0.0 fails safe. In `audio.synthesise` it was not: `spoken =
    0.0` makes `spoken > slot` false, the tempo branch is skipped, and the
    segment is shipped at whatever length it happens to be. A number that means
    both "empty" and "unreadable" cannot be compared against anything.
    """
    proc = subprocess.run(
        [ffprobe(), "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, errors="replace",
    )
    try:
        return float(proc.stdout.strip())
    except ValueError:
        raise ToolError(
            f"ffprobe could not read a duration from {path}: "
            f"{(proc.stderr or proc.stdout).strip()[:200] or 'no output'}"
        ) from None
