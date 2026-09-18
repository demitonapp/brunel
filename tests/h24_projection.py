#!/usr/bin/env python
"""H24: prove an orthographic camera actually removes perspective scaling.

Two IDENTICAL 1 m cubes sit at different distances from the camera. Under
`ortho_scale` they must project to the same width; under `lens_mm` the nearer
one must be measurably bigger. That difference is the whole reason the feature
exists: S1's Beat 3 compares a 153.94 cm2 disc against a 75.40 cm2 ring, and a
perspective lens makes the comparison argue for whichever figure is closer.

Asserting `camera.type == "ORTHO"` would only prove an attribute was set. This
measures the projection, which is the thing the spec author is actually buying.

Each fixture is measured in its OWN process, deliberately. Measuring both in one
bpy session returned 2.77778 for near AND far under perspective - a confidently
wrong number, identical for both, with no error raised. Stale evaluated geometry
between two builds in one session is exactly the silent-failure shape this repo
keeps finding, so the isolation is load-bearing, not tidiness.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Ortho must be flat to within a rounding error; perspective must be obviously
# not flat. The measured values are 1.0000 and 1.5722, so neither bound is tight.
ORTHO_TOLERANCE = 0.002
PERSP_MINIMUM = 1.30


def measure(which: str) -> dict[str, float]:
    """Build one fixture and return each cube's projected width, 0..1 of frame."""
    sys.path.insert(0, str(ROOT))
    import bpy
    from bpy_extras.object_utils import world_to_camera_view

    from harness import build as build_mod
    from harness import spec as spec_mod

    build_mod.build_scene(spec_mod.load(str(ROOT / "tests" / "fixtures" / f"camera_{which}.toml")))
    scene = bpy.context.scene
    cam = next(o for o in bpy.data.objects if o.type == "CAMERA")
    scene.camera = cam
    dg = bpy.context.evaluated_depsgraph_get()
    out: dict[str, float] = {"is_ortho": float(cam.data.type == "ORTHO")}
    for pid in ("near", "far"):
        obj = bpy.data.objects[pid].evaluated_get(dg)
        xs = [world_to_camera_view(scene, cam, obj.matrix_world @ v.co).x for v in obj.data.vertices]
        out[pid] = max(xs) - min(xs)
    return out


def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--measure":
        print(json.dumps(measure(sys.argv[2])))
        return 0

    results: dict[str, dict[str, float]] = {}
    for which in ("ortho", "persp"):
        proc = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--measure", which],
            capture_output=True, text=True,
        )
        if proc.returncode != 0:
            print(f"measuring {which} failed:\n{proc.stderr}")
            return 1
        results[which] = json.loads(proc.stdout.strip().splitlines()[-1])

    o, p = results["ortho"], results["persp"]
    if o["is_ortho"] != 1.0:
        print("the ortho fixture did not build an ORTHO camera")
        return 1
    if p["is_ortho"] != 0.0:
        print("the perspective fixture built an ORTHO camera")
        return 1

    o_ratio = o["near"] / o["far"]
    p_ratio = p["near"] / p["far"]
    if abs(o_ratio - 1.0) > ORTHO_TOLERANCE:
        print(f"ortho did NOT remove perspective scaling: near/far = {o_ratio:.4f}, "
              f"expected 1.0 +/- {ORTHO_TOLERANCE}")
        return 1
    if p_ratio < PERSP_MINIMUM:
        print(f"the perspective control measured {p_ratio:.4f}, under {PERSP_MINIMUM} - the "
              f"fixture no longer demonstrates the problem ortho solves, so the ortho "
              f"result proves nothing")
        return 1
    print(f"ortho near/far = {o_ratio:.4f}; perspective near/far = {p_ratio:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
