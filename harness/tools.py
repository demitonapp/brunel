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

import shlex
import shutil
import subprocess
from collections.abc import Sequence
from functools import cache
from pathlib import Path

#: How much of a failed command's stderr to quote. The four wrappers this
#: replaced used 400, 1500, 1500 and 2000 with no reason recorded for any of
#: them; ffmpeg's own errors are a line or two, and the generous limit only
#: matters when something unexpected is talking.
STDERR_TAIL = 2000


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


def run(cmd: Sequence[str], *, error: type[Exception], cwd: Path | None = None) -> str:
    """Run a command, raise `error` on a non-zero exit, return its stdout.

    `assemble`, `audio`, `captions` and `passes` each had their own copy of
    this, identical but for the exception type and an arbitrary stderr limit,
    and `backend._mux` plus two sites in `__main__` open-coded it again. The
    exception type stays a parameter because `main()` catches each module's
    error separately to decide an exit code - that distinction is real, and it
    is the only thing that differed.

    `shlex.join` rather than `" ".join`: a path with a space in it made the old
    message look like a different command than the one that ran.
    """
    proc = subprocess.run(
        [str(c) for c in cmd], capture_output=True, text=True, errors="replace", cwd=cwd,
    )
    if proc.returncode != 0:
        raise error(
            f"command failed ({proc.returncode}): {shlex.join(str(c) for c in cmd)}\n"
            f"{proc.stderr[-STDERR_TAIL:]}"
        )
    return proc.stdout


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
    out = run(
        [ffprobe(), "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        error=ToolError,
    )
    try:
        return float(out.strip())
    except ValueError:
        raise ToolError(
            f"ffprobe gave no duration for {path}: {out.strip()[:200] or 'no output'}"
        ) from None
