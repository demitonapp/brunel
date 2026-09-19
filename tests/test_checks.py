"""The output checks, each proven in BOTH directions.

A check that only ever reports a fault it cannot also stay quiet about is a
check that will be switched off the first time it cries wolf.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import NamedTuple

import pytest
from conftest import FIXTURES, harness, output

from harness import check
from harness.spec import Episode, load


def _frame(ffmpeg: str, dest: Path, *source: str) -> Path:
    subprocess.run([ffmpeg, "-v", "error", *source, "-frames:v", "1", str(dest)], check=True)
    return dest


def test_an_almost_empty_frame_is_reported(ffmpeg: str, tmp_path: Path) -> None:
    """S1's first cut measured 1.9% subject coverage - 98% empty background -
    and every check in the old suite passed it. A FLOOR, not the ceiling H22
    rejected: no deliberate shot puts its subject at 2% of a 1080x1920 frame.
    """
    # A 20x20 white mark on a 1080x1920 field is ~0.02% of frame.
    tiny = _frame(ffmpeg, tmp_path / "tiny.png",
                  "-f", "lavfi", "-i", "color=c=0x2b2f36:s=1080x1920",
                  "-f", "lavfi", "-i", "color=c=white:s=20x20",
                  "-filter_complex", "overlay=500:900")
    big = _frame(ffmpeg, tmp_path / "big.png",
                 "-f", "lavfi", "-i", "color=c=0x2b2f36:s=1080x1920",
                 "-f", "lavfi", "-i", "color=c=white:s=700x900",
                 "-filter_complex", "overlay=190:500")

    reported = check.check_coverage([tiny], label="tiny")
    assert reported and "invisible at thumb scale" in reported[0], \
        f"a 0.02%-coverage frame was NOT reported: {reported}"
    assert not check.check_coverage([big], label="big")


def test_a_black_frame_is_reported_and_a_real_one_is_not(ffmpeg: str, tmp_path: Path) -> None:
    black = _frame(ffmpeg, tmp_path / "black.png",
                   "-f", "lavfi", "-i", "color=c=black:s=64x64")
    grey = _frame(ffmpeg, tmp_path / "grey.png", "-f", "lavfi", "-i", "testsrc=s=64x64")

    assert check.check_storyboard([black]), \
        "a black frame was NOT reported - the storyboard check cannot fire"
    assert not check.check_storyboard([grey])


def test_verify_runs_the_motion_check(ffmpeg: str, tmp_path: Path) -> None:
    """H27. The regression risk is not that check_motion is wrong; it is that
    nothing CALLS it.

    Its only call site used to be inside check_depth_pass, reachable only when
    control passes exist, so on `local` it never ran - and s01 rendered three
    frozen shots while verify reported all 900 frames passing.
    """
    # testsrc genuinely animates across frames; a single colour does not.
    moving = tmp_path / "selftest_clear" / "moving"
    moving.mkdir(parents=True)
    subprocess.run([ffmpeg, "-v", "error", "-f", "lavfi", "-i", "testsrc=s=64x64:r=6",
                    "-frames:v", "6", str(moving / "frame_%04d.png")], check=True)
    frozen = tmp_path / "selftest_clear" / "frozen"
    frozen.mkdir(parents=True)
    for i in range(1, 7):                       # the SAME frame, six times
        shutil.copy(moving / "frame_0001.png", frozen / f"frame_{i:04d}.png")

    blob = output(harness("verify", str(FIXTURES / "camera_clear.toml"), "--out", str(tmp_path)))
    assert "frozen: nothing moves" in blob, f"verify did NOT report the frozen shot:\n{blob}"
    assert "moving: nothing moves" not in blob, \
        f"verify wrongly reported the moving shot as frozen:\n{blob}"


def test_the_storyboard_pass_can_see_a_frozen_shot(ffmpeg: str, tmp_path: Path) -> None:
    """Both directions, across frames that are SECONDS apart.

    `render --stills` used to write one frame per shot, and `check_motion`
    returns early below three - so the cheap pass could not, even in principle,
    see the fault that rendered three of s01's six hooks as still photographs.
    It now writes first, middle and last.

    The second half is the more important one. Spread that far apart, adjacent
    stills differ enormously, so the lurch threshold and the busy warning would
    fire on every correctly animated shot. A check that reports a fault on
    correct work is a check that gets switched off.
    """
    from harness.__main__ import _motion

    spread = tmp_path / "spread"
    spread.mkdir()
    subprocess.run([ffmpeg, "-v", "error", "-f", "lavfi", "-i", "testsrc=s=64x64:r=12",
                    "-frames:v", "36", str(spread / "f_%04d.png")], check=True)
    moving = [spread / "f_0001.png", spread / "f_0018.png", spread / "f_0036.png"]
    frozen = []
    for i, _ in enumerate(moving, 1):
        dest = tmp_path / f"frozen_{i}.png"
        shutil.copy(moving[0], dest)
        frozen.append(dest)

    reported = _motion(frozen, "b01")
    assert reported and "nothing moves" in reported[0], \
        f"three identical stills were NOT reported as frozen: {reported}"
    assert "b01" in reported[0], f"the report names the wrong thing: {reported[0]}"
    assert not _motion(moving, "b02"), \
        f"three stills seconds apart were reported as a fault: {_motion(moving, 'b02')}"


def test_the_stills_pass_renders_enough_frames_to_check_motion(tmp_path: Path) -> None:
    """The wiring, not the check. `check_motion` returns early below three
    frames, so a stills pass that writes fewer silently stops running it -
    which is how this fault shipped the first time.

    camera_clear.toml is a box that does not move, so the pass must also REFUSE
    it. That is the fixture being honest, not the fixture being wrong: it is a
    positive control for the camera-inside assertion, not for animation.
    """
    proc = harness("render", "--stills", str(FIXTURES / "camera_clear.toml"),
                   "--out", str(tmp_path))
    frames = sorted((tmp_path / "selftest_clear" / "s01").glob("frame_*.png"))
    assert len(frames) >= 3, \
        f"the stills pass wrote {len(frames)} frame(s) - check_motion cannot run below 3"
    assert proc.returncode == 3, f"a motionless shot was not refused:\n{output(proc)}"
    assert "nothing moves" in output(proc), output(proc)


class _Usage(NamedTuple):
    """As much of `shutil.disk_usage`'s answer as the guard reads."""

    free: int


def _episode(frames: int, fps: int = 30) -> Episode:
    """A real Episode of a given length, at the delivery profile.

    Not a stand-in object: `_disk_guard` asks the episode how long each shot is
    and how big a frame is, and a stub would let those two answers drift from
    what the loader actually produces.
    """
    ep = load(str(FIXTURES / "camera_clear.toml"))
    ep.meta.update(width=1080, height=1920, fps=fps)
    ep.shots[0]["seconds"] = frames / fps
    assert ep.frame_count(ep.shots[0], fps) == frames
    return ep


def test_a_render_that_cannot_fit_on_the_disk_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """H20. `render` writes every frame before `assemble` reads any, so a cut
    that does not fit fails on disk before it fails on patience - silently, and
    hours in. 12 GiB free on the authoring Mac against ~29 GB for a 7-minute cut
    at 1080x1920.

    Both directions, because a storage guard that fires early is a guard that
    gets switched off: the second half is an ordinary 30 s Short at ~2.1 GB,
    which must start.
    """
    from harness import render as render_mod
    from harness.render import RenderError, _disk_guard

    # H20's actual reading, pinned so the assertion means the same thing on a
    # laptop with a terabyte free as on the machine the finding came from.
    twelve_gib = 12 * 1024**3
    monkeypatch.setattr(render_mod.shutil, "disk_usage",
                        lambda path: _Usage(free=twelve_gib))

    # A 7-minute long-form is 12,600 frames: ~29 GB, and it does not fit.
    with pytest.raises(RenderError) as exc:
        _disk_guard(_episode(12_600), tmp_path, 30, False, None)
    message = str(exc.value)
    assert "GB free" in message, f"the refusal does not name what is available: {message}"
    assert "1080x1920" in message, f"the refusal does not name the profile: {message}"

    # A 30 s Short is 900 frames: ~2.1 GB, and it starts.
    _disk_guard(_episode(900), tmp_path, 30, False, None)


def test_the_disk_guard_does_not_count_frames_already_on_disk(
    ffmpeg: str, tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    """A resume needs only what is missing.

    Costing the whole cut again would refuse a render that is one shot from
    finishing, over frames that are already paid for and already on the disk it
    is worried about.
    """
    from harness.render import _disk_guard

    shot = tmp_path / "s01"
    shot.mkdir()
    _disk_guard(_episode(3), tmp_path, 30, False, None)
    assert "3 frame(s) to write" in capsys.readouterr().out

    # 256x256, not 64x64: `_frame_ok` treats anything under 1 KiB as the stub a
    # killed run leaves behind, and a 64x64 testsrc PNG is 531 bytes.
    _frame(ffmpeg, shot / "frame_0001.png", "-f", "lavfi", "-i", "testsrc=s=256x256")
    _disk_guard(_episode(3), tmp_path, 30, False, None)
    assert "2 frame(s) to write" in capsys.readouterr().out


def test_the_canary_fires_on_a_changed_frame_and_not_an_unchanged_one(
    ffmpeg: str, tmp_path: Path,
) -> None:
    """The ONLY comparison check in the harness.

    Every other one is a threshold and so cannot see drift. Calibrated against
    two actual double-renders of ad02; see GOLDEN_SSIM_MIN in harness/check.py.
    """
    golden = tmp_path / "ad02" / "c01.png"
    golden.parent.mkdir(parents=True)
    _frame(ffmpeg, golden, "-f", "lavfi", "-i", "testsrc=s=128x128")
    same = tmp_path / "same.png"
    shutil.copy2(golden, same)
    # A real picture change: the same pattern, cropped and rescaled. SSIM on
    # ad02's smallest TRUE regression (a 5 cm camera move) measured 0.827, so a
    # synthetic change has to be at least that visible to be a fair proxy.
    drift = tmp_path / "drift.png"
    subprocess.run([ffmpeg, "-v", "error", "-i", str(golden),
                    "-vf", "crop=120:120:8:8,scale=128:128",
                    "-frames:v", "1", str(drift)], check=True)

    identical = check.ssim(same, golden)
    assert identical >= 0.9999, \
        f"two identical frames scored {identical} - the canary cannot recognise an unchanged render"
    changed = check.ssim(drift, golden)
    assert changed < check.GOLDEN_SSIM_MIN, \
        f"a visibly changed frame scored {changed}, at or above the " \
        f"{check.GOLDEN_SSIM_MIN} floor - the canary cannot fire"

    # And through the check the CLI actually calls, not just the metric.
    assert not check.check_goldens({"c01": same}, tmp_path, "ad02")
    found = check.check_goldens({"c01": drift}, tmp_path, "ad02")
    assert [p for p in found if not p.startswith("WARN:")], \
        f"a changed frame was NOT reported as a regression: {found}"


def test_a_shot_with_no_canary_warns_it_does_not_fail(ffmpeg: str, tmp_path: Path) -> None:
    """Or the first run of a new spec is red for having no history yet."""
    golden = tmp_path / "ad02" / "c01.png"
    golden.parent.mkdir(parents=True)
    _frame(ffmpeg, golden, "-f", "lavfi", "-i", "testsrc=s=128x128")
    unblessed = check.check_goldens({"c99": golden}, tmp_path, "ad02")
    assert unblessed and all(p.startswith("WARN:") for p in unblessed), \
        f"a shot with no canary was treated as a failure: {unblessed}"


def test_a_corrupt_frame_names_the_reason_it_could_not_be_read(tmp_path: Path) -> None:
    """Five decode sites open-coded the same ffmpeg call and not one of them
    looked at its exit status - each tested only whether stdout was empty, so
    the reason ffmpeg gave was thrown away and every failure read the same.
    """
    junk = tmp_path / "corrupt.png"
    junk.write_bytes(b"\x89PNG\r\n\x1a\n" + b"garbage" * 20)
    with pytest.raises(check.CheckError) as exc:
        check.grey_stats(junk)
    assert "corrupt.png" in str(exc.value)
    # ffmpeg's own diagnosis, not just "produced no pixels".
    assert len(str(exc.value)) > len(f"ffmpeg produced no pixels for {junk}")


def test_check_clip_reports_an_unreadable_clip_rather_than_raising(tmp_path: Path) -> None:
    """It is called per shot over a whole episode; one unreadable clip must not
    stop the rest from being checked."""
    junk = tmp_path / "corrupt.mp4"
    junk.write_bytes(b"not an mp4 at all")
    problems = check.check_clip(junk)
    assert problems and "corrupt.mp4" in problems[0]
