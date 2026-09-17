# library/ — the compounding asset kit

Nothing in here is episode-specific. Everything here pays back across every future episode.

```
GEN/      parametric geometry generators (shield frames, brick bonds, iron rings,
          timber centring, scaffolding, rope, chain)
DET/      reusable detail geometry (rivet fields, bolt patterns, plate seams)
CHR/      scale witnesses and figures
MAT/      procedural material masters (brick, cast iron, wrought iron, timber,
          rope, canvas, coal smoke, gas flame)
SHOTS/    parameterised shot templates, not models
```

## Rules

1. **Every asset carries a provenance sidecar** (`<asset>.json`) with generator, calibrated
   dimensions, `measured: true|false`, and a source list with a licence per entry.
   `licencegate` fails the build on a missing sidecar.
2. **`shield_frame` is parameterised by `frames x cells_per_frame`.** Episode 1 uses 12 x 3. The
   same shape serves Greathead's 1869 Tower Subway shield and the 1884 City & South London
   shields. Never fork it for a new episode — add a parameter.
3. **A fix propagates.** Correct a generator and every episode linking it improves. That is the
   entire point.
4. **1 Blender unit = 1 metre.** No exceptions, no scale factors, no "it looked right".

## Not yet built

The kit is empty. Episode 1 seeds it. That seeding cost is the deliberate 2–3x premium on
Episode 1 and it is the reason Episode 7 is cheaper *and* better than Episode 1.
