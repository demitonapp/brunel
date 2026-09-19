"""Backend windows, and what `deliver --backend` must refuse.

`ad02`'s real generated clips shipped a crushed-to-black payoff shot and a
duration mismatch (see docs/strategy/spec.md Part II). The fixtures here prove
`deliver --backend` refuses both faults on synthetic clips it controls, then
that a clean, correctly-timed set is accepted.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from conftest import ROOT, harness, output

from harness.backend import WanVaceBackend
from harness.passes import PassError, PassProfile

SHOTS = ("c01", "c02", "c03", "c04", "c05")
SHOT_SECONDS = 4.0


def test_frame_count_refuses_past_max_frames() -> None:
    p = PassProfile(width=1, height=1, fps=16, min_frames=1, max_frames=81)
    assert p.frame_count(4.0) == 64
    assert p.chunks(4.0) == [64]
    with pytest.raises(PassError):
        p.frame_count(9.0)


@pytest.mark.parametrize("seconds", [1.0, 2.0, 3.0])
def test_a_shot_below_min_frames_is_refused_not_padded(seconds: float) -> None:
    """The SAME fault at the other end, and worse.

    `wan`'s real profile has min_frames=49, and a silent pad there rendered a
    2.0s shot as 49 frames (3.06s) - the whole normalised animation stretched
    over it, so the shot played 35% SLOW. `deliver --backend` then correctly
    refuses the clip for being the wrong length, so the generation is paid for
    and unusable.
    """
    wan = WanVaceBackend.profile
    assert wan.min_frames == 49
    assert wan.frame_count(4.0) == 64
    try:
        n = wan.frame_count(seconds)
    except PassError:
        return
    pytest.fail(f"frame_count({seconds}) returned {n} - a shot below min_frames was "
                f"padded instead of refused; it will play "
                f"{(n / wan.fps) / seconds:.2f}x slow")


def _clip(ffmpeg: str, dest: Path, seconds: float, source: str = "testsrc=s=64x64") -> None:
    subprocess.run([ffmpeg, "-y", "-v", "error", "-f", "lavfi",
                    "-i", f"{source}:d={seconds}", "-r", "16", str(dest)], check=True)


@pytest.fixture
def clips(ffmpeg: str, tmp_path: Path) -> Path:
    """A clean, correctly-timed generated clip set for ad02."""
    out = tmp_path / "ad02" / "generated-testbackend"
    out.mkdir(parents=True)
    for sid in SHOTS:
        _clip(ffmpeg, out / f"{sid}_c00.mp4", SHOT_SECONDS)
    return tmp_path


def _deliver(root: Path) -> str:
    return output(harness("deliver", str(ROOT / "spec/ad02/ad02.toml"),
                          "--out", str(root), "--backend", "testbackend", "--no-voice"))


def test_deliver_refuses_a_crushed_to_black_clip(ffmpeg: str, clips: Path) -> None:
    # Black at the CORRECT duration - isolates this from the duration check.
    _clip(ffmpeg, clips / "ad02" / "generated-testbackend" / "c05_c00.mp4",
          SHOT_SECONDS, source="color=c=black:s=64x64")
    assert "crushed to black" in _deliver(clips)


def test_deliver_refuses_a_duration_the_spec_does_not_declare(ffmpeg: str, clips: Path) -> None:
    _clip(ffmpeg, clips / "ad02" / "generated-testbackend" / "c01_c00.mp4", 5.06)
    blob = _deliver(clips)
    assert "c01: delivered" in blob and "but the spec declares 4.00s" in blob, blob


def test_deliver_accepts_a_clean_correctly_timed_set(clips: Path) -> None:
    proc = harness("deliver", str(ROOT / "spec/ad02/ad02.toml"), "--out", str(clips),
                   "--backend", "testbackend", "--no-voice")
    assert proc.returncode == 0, f"a clean clip set was wrongly refused:\n{output(proc)}"


def test_a_one_frame_benchmark_is_refused_and_records_nothing(tmp_path: Path) -> None:
    """The number every schedule claim rests on must not be quotable from a
    warm-up run. render-bench.json already carries one bad row measured that way.
    """
    bench_file = tmp_path / "bench.json"
    proc = harness("bench", str(ROOT / "spec/ad01/ad01.toml"), "--shots", "a01",
                   "--res", "64x64", "--samples", "1", "--frames", "1", "--device", "CPU",
                   "--out", str(tmp_path), "--bench-file", str(bench_file))
    assert "bench REFUSED" in output(proc), \
        f"a one-frame benchmark was accepted as throughput:\n{output(proc)}"
    assert not bench_file.exists(), "a refused benchmark still wrote a row"
