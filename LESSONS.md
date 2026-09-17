# LESSONS

Every entry carries an **executable check**, or it does not belong here. A lesson that cannot be
checked is a feeling, and feelings do not compound.

Format:

```
## YYYY-MM-DD — <one-line lesson>
- **Context:** what happened
- **Check:** the assertion, golden, or rubric item that now enforces it
- **Where:** the file that implements the check
```

---

## 2026-09-17 — A spec key the compiler silently ignores is a bug, not a convenience

- **Context:** An early spec set `depth` on a wall where the generator expected `brick_d`. The
  build succeeded and produced the wrong geometry. Nothing failed; the render was simply wrong.
- **Check:** The compiler raises `SpecError` on any key not in the schema's closed vocabulary.
- **Where:** `harness/spec.py` (top-level keys and `[part.params]` via `GENERATOR_PARAMS`).

## 2026-09-17 - The closed vocabulary had a hole, and only a test found it

- **Context:** The check above was believed comprehensive, but `[part.params]` tables were
  free-form, so `depht = 3.0` (a typo for `depth`) was accepted and silently ignored. This file
  claimed a guarantee the code did not provide - the same false-guarantee pattern the roadmap
  warns about, written by the hand that wrote the warning.
- **Check:** `spec.py` declares `GENERATOR_PARAMS`, the allowed keys per generator, and refuses any
  others. `build.py` raises at import time if a generator has no declared schema.
- **Where:** `harness/spec.py`, `tests/fixtures/unknown_key.toml`.

## 2026-09-17 - A chained job is a delayed-action failure

- **Context:** The render and the deliver step ran as one shell job (`render ; deliver`). A
  duplicate `--force` argument made argparse raise at startup, which would have killed `deliver`
  only AFTER the render finished - an hour spent for nothing.
- **Check:** `tests/run.sh` checks that every subcommand parses. Anything a chained job will invoke
  must be proven to START before the expensive step begins.
- **Where:** `tests/run.sh`.

## 2026-09-17 - A check that has never been seen to fail is not a check

- **Context:** The camera assertion and the closed vocabulary were both written, believed, and
  never exercised against a known-bad input. The vocabulary one was wrong.
- **Check:** Every assertion gets a negative fixture that MUST fail, plus a positive control that
  MUST pass. `./tests/run.sh` runs both directions.
- **Where:** `tests/run.sh`, `tests/fixtures/`.
## 2026-09-17 — Score renders, not code

- **Context:** "The script ran" and "the shot works" are different claims, and only the second one
  is the product.
- **Check:** The canary reel is compared with SSIM >= 0.98 and LPIPS <= 0.05 per shot. Hash
  equality is not used, because Cycles is not bit-reproducible across driver or OptiX versions.
- **Where:** `goldens/canary/` (not yet populated).

## 2026-09-17 — Archived evidence only

- **Context:** Web sources rot. A citation that no longer resolves is not a citation.
- **Check:** `factgate` warns on every source without `archived: true`.
- **Where:** `harness/factgate.py`.

## 2026-09-17 — Blender's Action API is mid-transition; do not bet on one shape

- **Context:** Blender 4.4+ introduced slotted actions and the legacy `action.fcurves` accessor is
  being retired. Camera keyframe interpolation silently did nothing.
- **Check:** `_fcurves()` enumerates both the legacy and the slotted layout.
- **Where:** `harness/render.py` — `_fcurves()`.

## 2026-09-17 - A camera can sit inside the geometry, and nothing will tell you

- **Context:** Two of eight shots were unusable on the storyboard pass, for two DIFFERENT reasons.
  In s07 the water box spanned y -21..+9 while the camera sat at y -9.5, so the camera was
  submerged *inside* the box and the shot rendered black. In s02 an 85 mm lens 0.9 m from a 2.6 m
  baulk of timber was not inside it at all - it was simply far too close, and rendered as a flat
  brown rectangle. Neither raised an error.
- **Check:** A camera inside the world-space bounds of any visible solid part is a HARD build
  failure. Parts opt out with `camera_inside_ok = true`. Flat parts are skipped: a plane has no
  volume to be inside of.
- **Where:** `harness/build.py` (`_assert_cameras_clear`).

## 2026-09-17 - Do NOT try to automate "is the framing good"

- **Context:** The s02 failure looked automatable, so a check was written that flagged any part
  subtending more than twice the frame. It immediately fired on legitimate work: the mvp tight
  close-up on the shield face (2.5x) and the s08 tunnel you are looking into (1.4x). The shipworm
  case it was meant to catch was 3.2x. The margin between "wrong" and "deliberately tight" is too
  thin to encode.
- **Check:** None. This is deliberately NOT automated. A check that cries wolf on correct work
  trains people to ignore it, which is worse than having no check. Framing is judged in the
  storyboard pass, by a human, on eight stills that cost a minute.
- **Where:** recorded in the `_assert_cameras_clear` docstring.

## 2026-09-17 - Storyboard before you render

- **Context:** A full render is roughly an hour. The stills pass is about a minute and caught five
  broken shots out of eight.
- **Check:** `render --stills` renders the middle frame of each shot. Run it, build a contact
  sheet, and look at it before starting a full render.
- **Where:** `harness/render.py` (`stills_only`), `harness/__main__.py` (`--stills`).

## 2026-09-17 - Track time must be normalised, not frame-numbered

- **Context:** Animation keyed to absolute frames silently breaks the moment the preview profile
  changes: the same spec at 12 fps and 30 fps would need re-timing by hand.
- **Check:** Track `frames` are 0.0-1.0 of the shot; the renderer scales them to the shot's actual
  frame count, and the validator rejects anything outside that range.
- **Where:** `harness/spec.py`, `harness/render.py` (`_apply_tracks`).

## 2026-09-17 - A generator in the schema but not the registry is silent drift

- **Context:** `spec.py` keeps the canonical generator list so `validate` works without Blender,
  which means the list can drift from `generators.py`.
- **Check:** `build.py` raises `ImportError` at import time if the two disagree.
- **Where:** `harness/build.py`, module level.

## 2026-09-17 - `set -e` does not fail on a pipeline

- **Context:** The render and the deliver step were chained as
  `python -m harness render ... | grep -v Saved:` inside a `set -e` script. Without
  `set -o pipefail`, a pipeline's status is the LAST command's, so a render crash was swallowed by
  a successful `grep` and `deliver` would have run anyway on a partial frame set - producing a
  short video and reporting success.
- **Check:** `deliver` compares the assembled duration against the sum of the spec's shot
  durations and aborts on a mismatch. Validate the OUTPUT, not the exit status.
- **Where:** `harness/__main__.py` (`cmd_deliver`), which returns 3 on a short assembly.

## 2026-09-17 - A benchmark that includes fixed costs is not a benchmark

- **Context:** `render-bench.json` reported 3.00 s/frame from a 48-frame run. Scene construction is
  a fixed cost, so roughly half that number was build time. The real steady-state figure, measured
  over 864 frames, is 1.97 s/frame - which changes the Episode 1 estimate from 57 hours to 37.
- **Check:** Benchmark over hundreds of frames, or subtract the build explicitly, and record which
  of the two a number is.
- **Where:** `render-bench.json` (`kind: steady_state` vs `includes_build`).