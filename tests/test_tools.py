"""One duration probe, and it refuses to answer 0.0 when it does not know.

Three near-identical copies of this function existed - in `__main__`,
`audio` and inline in `assemble` - and all three returned 0.0 on any failure.
In `__main__` that was harmless: every caller compares the result against the
spec's declared length and refuses a mismatch, so 0.0 fails safe. In
`audio.synthesise` it was not. `spoken = 0.0` makes `spoken > slot` false, the
time-compression branch never runs, and the segment ships at whatever length it
happens to be - silently, in the deliverable.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from harness.__main__ import DURATION_TOLERANCE
from harness.tools import ToolError, duration_seconds, ffprobe


def test_a_real_clip_measures_its_real_length(ffmpeg: str, tmp_path: Path) -> None:
    """Against the tolerance `deliver` actually applies.

    `testsrc=d=4.0 -r 16` lands at 4.125s - 66 frames, not 64 - which is an
    ffmpeg container quirk rather than a measurement error, and is exactly the
    slack DURATION_TOLERANCE exists to absorb.
    """
    clip = tmp_path / "four.mp4"
    subprocess.run([ffmpeg, "-y", "-v", "error", "-f", "lavfi",
                    "-i", "testsrc=s=64x64:d=4.0", "-r", "16", str(clip)], check=True)
    assert abs(duration_seconds(clip) - 4.0) < DURATION_TOLERANCE


def test_an_unreadable_file_raises_rather_than_measuring_zero(tmp_path: Path) -> None:
    """0.0 is a real duration. A number that also means "I could not tell" is
    not comparable against anything."""
    junk = tmp_path / "not-a-video.mp4"
    junk.write_bytes(b"this is not an mp4")
    with pytest.raises(ToolError):
        duration_seconds(junk)


def test_a_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(ToolError):
        duration_seconds(tmp_path / "nothing-here.mp4")


def test_the_resolvers_agree_with_the_path(ffmpeg: str) -> None:
    from harness import tools

    assert tools.ffmpeg() == ffmpeg
    assert Path(ffprobe()).name.startswith("ffprobe")
