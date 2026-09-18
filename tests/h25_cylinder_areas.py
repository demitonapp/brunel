#!/usr/bin/env python
"""H25: the cylinder's geometry must agree with the manufacturer's printed table.

Bosch Rexroth RE 17331 publishes, for a 140 mm bore and a 100 mm rod:

    piston A1 = 153.94 cm2      rod A2 = 78.54 cm2      annulus A3 = 75.40 cm2

Every other generator in this repo is checked against a DIMENSION a source
states. This is the first one whose derived QUANTITIES a vendor also prints, so
it is checked against those - a figure published by someone who does not know
this repo exists.

The specific failure this catches: computing the annulus from the bore RADIUS
instead of the bore AREA. That mistake still produces a plausible number, still
renders, and would put a wrong dimension on screen in a video whose entire
subject is the ratio of these two areas.

Measured from the built mesh, not from the parameters - asserting that
pi/4*d^2 equals pi/4*d^2 would be H7's tautology.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Rexroth RE 17331, "Areas, forces, flows", row piston AL 140 / piston rod MM 100.
PUBLISHED_CM2 = {"piston": 153.94, "rod": 78.54, "annulus": 75.40}
TOLERANCE_CM2 = 0.01

BORE, ROD = 0.140, 0.100


def main() -> int:
    sys.path.insert(0, str(ROOT))
    import bpy

    from harness import generators

    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    coll = bpy.context.scene.collection

    # Build the real piston through the real generator, then measure the disc it
    # actually produced rather than trusting the number that went in.
    generators.gen_cylinder_rod("probe", {"bore": BORE, "rod": ROD, "segments": 512}, coll)
    piston = bpy.data.objects["probe_piston"]
    xs = [v.co.x for v in piston.data.vertices]
    ys = [v.co.y for v in piston.data.vertices]
    measured_bore_m = max(max(xs) - min(xs), max(ys) - min(ys))

    rod_obj = bpy.data.objects["probe_rod"]
    rxs = [v.co.x for v in rod_obj.data.vertices]
    rys = [v.co.y for v in rod_obj.data.vertices]
    measured_rod_m = max(max(rxs) - min(rxs), max(rys) - min(rys))

    # A 512-gon inscribes its circle, so the measured width is a hair under the
    # true diameter. Correct for it rather than loosening the tolerance, which
    # would blunt the check this file exists to make.
    seg = 512
    inscribe = math.cos(math.pi / seg)
    bore_m = measured_bore_m / inscribe
    rod_m = measured_rod_m / inscribe

    a1 = math.pi / 4.0 * bore_m**2 * 1e4
    a2 = math.pi / 4.0 * rod_m**2 * 1e4
    got = {"piston": a1, "rod": a2, "annulus": a1 - a2}

    bad = []
    for key, want in PUBLISHED_CM2.items():
        if abs(got[key] - want) > TOLERANCE_CM2:
            bad.append(f"{key}: built {got[key]:.3f} cm2, Rexroth prints {want} cm2")
    if bad:
        print("cylinder geometry disagrees with the published table:")
        for line in bad:
            print(f"  {line}")
        return 1
    print(f"piston {got['piston']:.2f} / rod {got['rod']:.2f} / annulus {got['annulus']:.2f} cm2 "
          f"- matches RE 17331 within {TOLERANCE_CM2} cm2")
    return 0


if __name__ == "__main__":
    sys.exit(main())
