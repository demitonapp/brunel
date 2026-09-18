"""Automated output checks - the part of the harness that looks at the result.

Every entry in `LESSONS.md` that can be enforced belongs here. The ones that
cannot stay prose, and say so. This module exists because this project's most
expensive failures were all **silent**: a render that was black, a depth map
that was saturated to white, a colour map with no colour, a screenshot of a
frame that never changed.

None of them raised an error. All of them were visible in the pixels, and
nobody was looking at the pixels automatically.

The three checks below are the ones with the best ratio of caught-bugs to
false-positives, measured against the two production passes that produced them
(2026-09-18). Each is calibrated rather than absolute - the thresholds are
recorded with the observation that set them, because a threshold nobody can
trace back to a measurement is a taste.
"""

from __future__ import annotations

import shutil
import subprocess
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any

# --- thresholds, each traced to the observation that set it ---------------

#: A frame whose mean grey is below this is effectively black. Set from the ad02
#: m01 establish shot, which rendered at mean ~4 (of 255) because the camera sat
#: outside the tunnel bore looking at its outer wall. A legitimately dark frame
#: in this project's period-tunnel work measured 22-30.
BLACK_MEAN = 12.0

#: A frame with less tonal spread than this carries no image. A correctly
#: exposed tunnel interior measured 60+; a flat plate filling the frame and
#: blown out measured under 20.
MIN_SPREAD = 24

#: A depth pass must use most of its range. The saturated failure this catches
#: measured a mean of 248 of 255 with the subject at 2% of the ramp; the
#: corrected pass measured 121, and fal's own reference depth video measures 82.
DEPTH_MEAN_MIN = 25.0
DEPTH_MEAN_MAX = 205.0
DEPTH_SPREAD_MIN = 90


class CheckError(RuntimeError):
    """Raised when a check cannot run at all - distinct from a failed check."""


def _ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if not exe:
        raise CheckError("ffmpeg is required for output checks")
    return exe


def grey_stats(path: Path, *, size: int = 64) -> dict[str, Any]:
    """Luminance statistics for one frame, downscaled to `size` x `size`.

    Downscaling is deliberate: every check here is about whether an image
    exists at all, not about its detail, and 4096 samples answer that as well as
    400,000 while being fast enough to run on every storyboard frame.
    """
    if not path.exists():
        raise CheckError(f"no such frame: {path}")
    raw = subprocess.run(
        [_ffmpeg(), "-v", "error", "-i", str(path),
         "-vf", f"scale={size}:{size}", "-pix_fmt", "gray",
         "-f", "rawvideo", "-"],
        capture_output=True,
    ).stdout
    if not raw:
        raise CheckError(f"ffmpeg produced no pixels for {path}")
    vals = list(raw)
    n = len(vals)
    mean = sum(vals) / n
    return {
        "frame": path.name,
        "mean": round(mean, 1),
        "min": min(vals),
        "max": max(vals),
        "spread": max(vals) - min(vals),
        "dark_fraction": round(sum(1 for v in vals if v < 8) / n, 3),
    }


def is_greyscale(path: Path, *, size: int = 64, tolerance: int = 2) -> tuple[bool, float]:
    """True when R == G == B on every sampled pixel, and the worst deviation.

    A depth or segmentation-adjacent pass must be neutral. This is what caught
    the depth pass that was silently rendering the beauty image instead.
    """
    raw = subprocess.run(
        [_ffmpeg(), "-v", "error", "-i", str(path),
         "-vf", f"scale={size}:{size}", "-pix_fmt", "rgb24",
         "-f", "rawvideo", "-"],
        capture_output=True,
    ).stdout
    if not raw:
        raise CheckError(f"ffmpeg produced no pixels for {path}")
    worst = 0
    for i in range(0, len(raw), 3):
        r, g, b = raw[i], raw[i + 1], raw[i + 2]
        worst = max(worst, max(r, g, b) - min(r, g, b))
    return (worst <= tolerance, float(worst))


def _frames(directory: Path) -> list[Path]:
    return sorted(directory.glob("frame_*.png"))


# --- the checks -----------------------------------------------------------


def check_storyboard(frames: Iterable[Path]) -> list[str]:
    """Every storyboard frame must contain a picture.

    This is the cheapest and highest-value check in the file. The project's
    single most common failure is a camera in the wrong place, and a camera in
    the wrong place almost always produces a frame that is black, or flat, or
    both. Two shots have now been lost to it - one camera inside a water box,
    one outside the tunnel bore it was supposed to be standing in.
    """
    problems: list[str] = []
    for f in frames:
        s = grey_stats(f)
        if s["mean"] < BLACK_MEAN:
            problems.append(
                f"{f.parent.name}/{f.name}: mean luminance {s['mean']} - the frame is "
                f"effectively black. The camera is probably inside solid geometry, "
                f"outside the enclosure the shot is set in, or unlit."
            )
        elif s["spread"] < MIN_SPREAD:
            problems.append(
                f"{f.parent.name}/{f.name}: tonal spread {s['spread']} - the frame is "
                f"flat. Something is filling it (a plate, a wall, a lens too close)."
            )
        elif s["dark_fraction"] > 0.92:
            problems.append(
                f"{f.parent.name}/{f.name}: {s['dark_fraction']:.0%} of the frame is "
                f"near-black - only a sliver is lit."
            )
    return problems


def check_depth_pass(frames: Sequence[Path]) -> list[str]:
    """A depth pass must be neutral, use its range, and not drift frame to frame.

    Three distinct failures, all of which happened:

    * **Neutral** - a depth pass that renders the beauty image is not a depth
      pass. Caught by R != G != B.
    * **Range** - a range set far too wide compresses the subject to a few
      levels near one end. The saturated version of this measured a mean of 248
      of 255 with the subject at 2% of the ramp.
    * **Stability** - the whole reason depth is normalised once per shot. If the
      mean moves materially between frames, the range is being recomputed
      per-frame (the stock preprocessors' behaviour) and the model will render
      the "breathing".
    """
    problems: list[str] = []
    if not frames:
        return ["no frames found to check"]

    greyscale, worst = is_greyscale(frames[0])
    if not greyscale:
        problems.append(
            f"depth is not neutral at {frames[0].name}: worst channel spread {worst:.0f}. "
            f"A depth pass must have R == G == B; this looks like a beauty render."
        )

    stats = [grey_stats(f) for f in frames]
    mean = sum(s["mean"] for s in stats) / len(stats)
    spread = max(s["max"] for s in stats) - min(s["min"] for s in stats)

    if mean > DEPTH_MEAN_MAX:
        problems.append(
            f"depth mean {mean:.0f} of 255 is saturated toward white - the near/far range "
            f"is far too wide, so the subject occupies only the bottom of the ramp."
        )
    elif mean < DEPTH_MEAN_MIN:
        problems.append(
            f"depth mean {mean:.0f} of 255 is saturated toward black - the range is "
            f"too narrow, or the polarity is inverted."
        )
    if spread < DEPTH_SPREAD_MIN:
        problems.append(
            f"depth uses only {spread} grey levels - the range does not fit the subject."
        )

    # Motion: a shot with no movement at all is a missing track, and a shot that
    # lurches is how a wrong Euler order announces itself.
    problems += check_motion(frames)

    # Stability across the shot: sample up to 6 frames and compare means.
    if len(stats) > 2:
        step = max(1, len(stats) // 6)
        sampled = [stats[i]["mean"] for i in range(0, len(stats), step)]
        swing = max(sampled) - min(sampled)
        if swing > 40:
            problems.append(
                f"depth mean swings by {swing:.0f} across the shot (samples {sampled}) - "
                f"the range is being recomputed per frame. Normalise once per shot."
            )
    return problems


def frame_diff(a: Path, b: Path, *, size: int = 48) -> float:
    """Mean absolute luminance difference between two frames, 0-255."""
    def grey(path: Path) -> list[int]:
        return list(subprocess.run(
            [_ffmpeg(), "-v", "error", "-i", str(path),
             "-vf", f"scale={size}:{size}", "-pix_fmt", "gray",
             "-f", "rawvideo", "-"],
            capture_output=True,
        ).stdout)
    ga, gb = grey(a), grey(b)
    if len(ga) != len(gb) or not ga:
        raise CheckError(f"cannot compare {a.name} and {b.name}")
    return sum(abs(x - y) for x, y in zip(ga, gb, strict=True)) / len(ga)


#: Calibrated from measurement, and honest about its limit.
#:
#: Before the fix, the windmilling screws measured 18.1 and 19.5 while the three
#: camera-only shots measured 6.8-7.8. After the fix - screws turning in place
#: and the cell travelling along them, which is correct - the same two shots
#: measure 14.3 and 16.3. **The bug and the correct animation now overlap in
#: magnitude**, so magnitude alone can separate "busy" from "quiet" but not
#: "right" from "wrong". Pretending otherwise would be a check that lies.
#:
#: So: over `MOTION_BUSY` is a WARNING - go and look at it - and only a frozen
#: shot (nothing moves at all) is a hard failure. The contact sheet is the
#: adjudicator, exactly as the storyboard stills are for staging.
MOTION_BUSY = 12.0
MOTION_MAX_STEP = 60.0


def check_motion(frames: Sequence[Path], *, max_step: float = MOTION_MAX_STEP,
                 min_total: float = 0.5) -> list[str]:
    """The animation must move, and must not lurch.

    **This is the check that would have caught the windmilling screws.** Every
    check in this file before it looked at individual frames: is this one black,
    is it flat, is the depth neutral. A screw swinging end-over-end through a
    full circle passes all of them, because each frame on its own is a perfectly
    good picture. The fault only exists *between* frames.

    Two failure modes, and they are opposites:

    * **Frozen** - nothing changes across the shot. Usually a track that was
      written but never applied, or a part that is not visible in this shot.
      `min_total` is low on purpose: a slow push-in moves very little.
    * **Lurching** - a large change between adjacent frames. A part sweeping
      through space rather than turning about its own axis does this, and so
      does a wrong Euler order - which is exactly how the screws got here. The
      threshold is set well above a camera move and well below a part swinging
      through 45 degrees in one frame.
    """
    problems: list[str] = []
    if len(frames) < 3:
        return problems

    step = max(1, len(frames) // 12)
    sampled = list(frames)[::step]
    diffs = [frame_diff(sampled[i], sampled[i + 1]) for i in range(len(sampled) - 1)]
    if not diffs:
        return problems

    total = sum(diffs)
    worst = max(diffs)
    if total < min_total:
        problems.append(
            f"{frames[0].parent.parent.name}: nothing moves across the shot "
            f"(total frame-to-frame change {total:.2f}). A track is missing or not applied."
        )
    if worst > max_step:
        problems.append(
            f"{frames[0].parent.parent.name}: a large jump between frames "
            f"(worst step {worst:.1f}, limit {max_step:.0f}) - a part is sweeping "
            f"rather than turning in place, or the animation is out of order."
        )
    elif worst > MOTION_BUSY:
        # Not a fault. A signal that this is the kind of shot where a wrong
        # Euler order hides, and worth a contact sheet before it is paid for.
        problems.append(
            f"WARN: {frames[0].parent.parent.name}: busy motion (worst step "
            f"{worst:.1f}) - check a contact sheet of this shot before generating."
        )
    return problems


def check_clip(path: Path) -> list[str]:
    """A finished clip must not be crushed to black.

    The first real Wan VACE generation came back at a mean of ~20 of 255 and the
    second pass was darker still, because the prompt asked for "deep shadow" and
    the model obliged. Cheap to detect, and it is the difference between an asset
    and a black rectangle.
    """
    if not path.exists():
        return [f"no such clip: {path}"]
    problems: list[str] = []
    # Sample the middle of the clip, not frame 0 - the first frame of a generated
    # shot is often a fade.
    probe = subprocess.run(
        [_ffmpeg(), "-v", "error", "-sseof", "-1", "-i", str(path),
         "-vf", "scale=64:64", "-pix_fmt", "gray", "-f", "rawvideo", "-"],
        capture_output=True,
    ).stdout
    if not probe:
        return [f"could not read any pixel from {path}"]
    vals = list(probe)
    mean = sum(vals) / len(vals)
    if mean < BLACK_MEAN:
        problems.append(f"{path.name}: mean luminance {mean:.1f} - the clip is crushed to black")
    return problems


__all__ = [
    "CheckError", "grey_stats", "is_greyscale",
    "check_storyboard", "check_depth_pass", "check_clip",
    "BLACK_MEAN", "MIN_SPREAD", "DEPTH_MEAN_MIN", "DEPTH_MEAN_MAX", "DEPTH_SPREAD_MIN",
]
