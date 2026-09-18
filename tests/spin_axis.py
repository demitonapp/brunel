#!/usr/bin/env python
"""The screw turns about its OWN axis, for any base orientation.

This is the repo's most expensive bug, given a number. `spin` was written into
the `.z` slot of the part's Euler; Blender's XYZ order is R = Rz.Ry.Rx, so Z is
applied **last**, and a shaft already laid along Y by `rot = [90, 0, 0]` got
swung round the *world* Z axis like a propeller. It shipped, it cost a paid
generation, and it passed `storyboard`, `depth` and `clip` without a murmur -
every individual frame was a perfectly good picture. The fault only existed
between frames.

`check_motion` was the response, and `harness/check.py` is honest that it cannot
finish the job: after the fix, correct rotation measured 14.3-16.3 against the
bug's 18.1-19.5, so a single threshold cannot separate right from wrong. That
leaves the numeric core of the bug guarded by a WARNING. This file guards it
with an assertion instead.

**The invariant.** Turning a screw does not move the axis it turns about. So the
local Z axis of `R_base @ R_spin` must equal the local Z axis of `R_base`, for
every base orientation and every spin angle. A propeller sweep moves it.

Note the angles below deliberately include non-multiples of 360. At a whole
number of turns the buggy composition lands back on the correct answer - the
`ad02` track ran 0 -> 2160 degrees and agreed with the fix at *both* keyframes.
It is the interpolated angles in between that were wrong, which is precisely why
a per-frame check could never see it.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# `mathutils` is not a wheel on disk - it is registered as a builtin module by
# importing bpy, so `import bpy` has to come first and cannot be dropped as
# unused. The sort order below happens to satisfy that on its own.
import bpy  # noqa: E402, F401 - registers the `mathutils` builtin
from mathutils import Euler  # noqa: E402

from harness.render import spin_euler  # noqa: E402

#: Base orientations: unrotated, the ad02 screw laid along Y, that screw also
#: rolled, and an arbitrary compound rotation with no symmetry to hide behind.
BASES = ([0.0, 0.0, 0.0], [90.0, 0.0, 0.0], [90.0, 0.0, 45.0], [12.0, -30.0, 7.0])
#: Spin angles, in degrees. 90 and 137 are the ones that matter - see the note
#: above about whole turns agreeing by accident.
SPINS = (0.0, 90.0, 137.0, 360.0, 2160.0, -1440.0)
TOLERANCE = 1e-6


def local_z(euler_deg: list[float] | tuple[float, ...]):
    """The part's own Z axis, in world space, for an XYZ Euler in degrees."""
    return Euler([math.radians(x) for x in euler_deg], "XYZ").to_matrix().col[2]


def main() -> int:
    failures: list[str] = []

    for base in BASES:
        want = local_z(base)
        for deg in SPINS:
            got = [math.degrees(a) for a in spin_euler(base, deg)]
            drift = (local_z(got) - want).length
            if drift > TOLERANCE:
                failures.append(
                    f"base={base} spin={deg}: the spin moved the part's own axis "
                    f"by {drift:.4f} - it is sweeping, not turning in place"
                )

    # The control. Prove the invariant can FAIL, on the exact bug it describes:
    # the spin written into the .z Euler slot. A test whose assertion has never
    # been observed to fail is not a test.
    bug = [90.0, 0.0, 90.0]
    bug_drift = (local_z(bug) - local_z([90.0, 0.0, 0.0])).length
    if bug_drift <= TOLERANCE:
        failures.append(
            f"the .z-slot bug measured a drift of {bug_drift:.4f} - the invariant "
            f"cannot distinguish the propeller sweep from a correct turn, so it "
            f"is not guarding anything"
        )

    if failures:
        for f in failures:
            print(f)
        return 1
    print(f"  {len(BASES) * len(SPINS)} base/spin pairs hold the axis "
          f"(control: the .z-slot bug drifts {bug_drift:.3f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
