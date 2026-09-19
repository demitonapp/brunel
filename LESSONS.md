# LESSONS

Every entry carries an **executable check**, or it does not belong here. A lesson that cannot be
checked is a feeling, and feelings do not compound.

Format:

```
## YYYY-MM-DD — <one-line lesson>
- **Context:** what happened
- **Check:** the assertion, golden, or rubric item that should enforce it
- **Where:** the file that implements the check
- **ENFORCED BY:** what actually runs it today, or `nothing — prose only`
```

**Why `Check:` and `ENFORCED BY:` are separate.** A 2026-09-18 audit found that `Check:` alone had
drifted into aspiration in several entries — describing what *should* catch a regression, not what
*does*. Four defects it named ("Two channels that are one mechanism", the crushed-to-black clip,
and two others) were already recorded here as solved and shipped anyway. `ENFORCED BY:` is the
line that gets re-verified against the current code, not copied from the `Check:` bullet that
inspired it — "nothing — prose only" is a legitimate, honest answer, and every entry below states
one or the other.

---

## 2026-09-17 — A spec key the compiler silently ignores is a bug, not a convenience

- **Context:** An early spec set `depth` on a wall where the generator expected `brick_d`. The
  build succeeded and produced the wrong geometry. Nothing failed; the render was simply wrong.
- **Check:** The compiler raises `SpecError` on any key not in the schema's closed vocabulary.
- **Where:** `harness/spec.py` (top-level keys and `[part.params]` via `GENERATOR_PARAMS`).
- **ENFORCED BY:** `harness/spec.py` (`_unknown`), exercised by `tests/test_spec_validation.py` ("an unknown spec key is refused") via `tests/fixtures/unknown_key.toml`.

## 2026-09-17 - The closed vocabulary had a hole, and only a test found it

- **Context:** The check above was believed comprehensive, but `[part.params]` tables were
  free-form, so `depht = 3.0` (a typo for `depth`) was accepted and silently ignored. This file
  claimed a guarantee the code did not provide - the same false-guarantee pattern the roadmap
  warns about, written by the hand that wrote the warning.
- **Check:** `spec.py` declares `GENERATOR_PARAMS`, the allowed keys per generator, and refuses any
  others. `build.py` raises at import time if a generator has no declared schema.
- **Where:** `harness/spec.py`, `tests/fixtures/unknown_key.toml`.
- **ENFORCED BY:** `harness/spec.py` (`GENERATOR_PARAMS`), `harness/build.py` (import-time assert that every generator has a declared param schema), `tests/test_spec_validation.py` ("an unknown spec key is refused").

## 2026-09-17 - A chained job is a delayed-action failure

- **Context:** The render and the deliver step ran as one shell job (`render ; deliver`). A
  duplicate `--force` argument made argparse raise at startup, which would have killed `deliver`
  only AFTER the render finished - an hour spent for nothing.
- **Check:** `tests/test_cli.py` checks that every subcommand parses. Anything a chained job will invoke
  must be proven to START before the expensive step begins.
- **Where:** `tests/test_cli.py`.
- **ENFORCED BY:** `tests/test_cli.py` ("cli parses" loop - every subcommand's `--help` must exit 0).

## 2026-09-17 - A check that has never been seen to fail is not a check

- **Context:** The camera assertion and the closed vocabulary were both written, believed, and
  never exercised against a known-bad input. The vocabulary one was wrong.
- **Check:** Every assertion gets a negative fixture that MUST fail, plus a positive control that
  MUST pass. `pytest` runs both directions.
- **Where:** `tests/`, `tests/fixtures/`.
- **ENFORCED BY:** the suite itself - this is the rule the whole file follows, not one assertion in it.
## 2026-09-17 — Score renders, not code

- **Context:** "The script ran" and "the shot works" are different claims, and only the second one
  is the product.
- **Check:** Each shot's storyboard still is compared against a blessed canary frame by SSIM, with a
  floor of `GOLDEN_SSIM_MIN`. Hash equality is not used - see the 2026-09-18 entry for what was
  actually measured about reproducibility, which is more specific than the reason first given here.
- **Where:** `goldens/<episode>/<shot>.png`, `harness/check.py`, `harness/__main__.py` (`verify`).
- **ENFORCED BY:** `harness/check.py` (`check_goldens`) via `harness verify`, and `tests/test_checks.py`
  ("the canary scores 1.0 on an unchanged frame and fires on a changed one"). **Built 2026-09-18**,
  having sat here as `nothing - prose only` since the first commit while `goldens/` stayed empty -
  which is exactly the pattern the entry two below warns about. The numbers in the original
  `Check:` line were aspirational and are now replaced by measured ones: the floor is **0.995**, not
  0.98, and **LPIPS is not implemented** - it needs a dependency this repo does not have. Claiming
  it here for a year did not make it exist. `goldens/ad02` is blessed; `goldens/ep01` is not.

## 2026-09-17 — Archived evidence only

- **Context:** Web sources rot. A citation that no longer resolves is not a citation.
- **Check:** `factgate` warns on every source without `archived: true`.
- **Where:** `harness/factgate.py`.
- **ENFORCED BY:** `harness/factgate.py` (rule `every_web_source_has_an_archive_url`) - runs on every `factgate` invocation.

## 2026-09-17 — Blender's Action API is mid-transition; do not bet on one shape

- **Context:** Blender 4.4+ introduced slotted actions and the legacy `action.fcurves` accessor is
  being retired. Camera keyframe interpolation silently did nothing.
- **Check:** `_fcurves()` enumerates both the legacy and the slotted layout.
- **Where:** `harness/render.py` — `_fcurves()`.
- **ENFORCED BY:** `harness/render.py` (`_fcurves`) - runs on every render; no fixture regression-tests the slotted-action code path specifically (would need a Blender 4.4+ file authored with one).

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
- **ENFORCED BY:** `harness/build.py` (`_assert_cameras_clear`), `tests/test_spec_validation.py` ("camera inside geometry is rejected" / "camera clear of geometry is accepted") via `tests/fixtures/camera_inside.toml` / `camera_clear.toml`.

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
- **ENFORCED BY:** nothing, by design - the entry itself states why (a check here cries wolf on correct work). The storyboard pass is the control, not a check.

## 2026-09-17 - Storyboard before you render

- **Context:** A full render is roughly an hour. The stills pass is about a minute and caught five
  broken shots out of eight.
- **Check:** `render --stills` renders the middle frame of each shot. Run it, build a contact
  sheet, and look at it before starting a full render.
- **Where:** `harness/render.py` (`stills_only`), `harness/__main__.py` (`--stills`).
- **ENFORCED BY:** `harness/__main__.py` (`cmd_render` calls `check.check_storyboard` after `--stills`), and `check_storyboard` itself is unit-tested in `tests/test_checks.py` ("a black frame is reported, a real frame is not").

## 2026-09-17 - Track time must be normalised, not frame-numbered

- **Context:** Animation keyed to absolute frames silently breaks the moment the preview profile
  changes: the same spec at 12 fps and 30 fps would need re-timing by hand.
- **Check:** Track `frames` are 0.0-1.0 of the shot; the renderer scales them to the shot's actual
  frame count, and the validator rejects anything outside that range.
- **Where:** `harness/spec.py`, `harness/render.py` (`_apply_tracks`).
- **ENFORCED BY:** `harness/spec.py` (the 0.0-1.0 range check on `track.frames`, and the ascending-order check) - runs on every spec load; no dedicated negative fixture, but every real spec (`ep01`, `ad01`, `ad02`) exercises the positive case.

## 2026-09-17 - A generator in the schema but not the registry is silent drift

- **Context:** `spec.py` keeps the canonical generator list so `validate` works without Blender,
  which means the list can drift from `generators.py`.
- **Check:** `build.py` raises `ImportError` at import time if the two disagree.
- **Where:** `harness/build.py`, module level.
- **ENFORCED BY:** `harness/build.py` (module-level `_missing` assert, raises `ImportError`) - unconditional: the module cannot be imported if the two lists disagree.

## 2026-09-17 - `set -e` does not fail on a pipeline

- **Context:** The render and the deliver step were chained as
  `python -m harness render ... | grep -v Saved:` inside a `set -e` script. Without
  `set -o pipefail`, a pipeline's status is the LAST command's, so a render crash was swallowed by
  a successful `grep` and `deliver` would have run anyway on a partial frame set - producing a
  short video and reporting success.
- **Check:** `deliver` compares the assembled duration against the sum of the spec's shot
  durations and aborts on a mismatch. Validate the OUTPUT, not the exit status.
- **Where:** `harness/__main__.py` (`cmd_deliver`), which returns 3 on a short assembly.
- **ENFORCED BY:** `harness/__main__.py` (`cmd_deliver`'s duration check, `abs(got - expected) > 0.75`) - runs on every frame-based `deliver`; no fixture forces a partial render to exercise it.

## 2026-09-17 - A benchmark that includes fixed costs is not a benchmark

- **Context:** `render-bench.json` reported 3.00 s/frame from a 48-frame run. Scene construction is
  a fixed cost, so roughly half that number was build time. The real steady-state figure, measured
  over 864 frames, is 1.97 s/frame - which changes the Episode 1 estimate from 57 hours to 37.
- **Check:** Benchmark over hundreds of frames, or subtract the build explicitly, and record which
  of the two a number is.
- **Where:** `render-bench.json` (`kind: steady_state` vs `includes_build`).
- **ENFORCED BY:** nothing mechanical - `render-bench.json`'s `kind` field is a human-maintained convention (correctly followed as of 2026-09-18), not validated by code.
## 2026-09-17 - The pipeline trap, again, in the test harness

- **Context:** A lesson about `set -e` and pipelines was written earlier the same day. Hours
  later the identical mistake appeared in `tests/run.sh`, which ran under `set -uo pipefail`.
  `factgate ... | grep -q PASS` fails when factgate exits 1 - because grep matched, but pipefail
  returns the rightmost non-zero status. The check reported FAIL for a rule that had passed.
- **Check:** Capture the output into a variable, then grep the variable. Never pipe a
  deliberately-failing command into a matcher.
- **Where:** was `tests/run.sh`, fact-gate section; the runner is now Python.
- **ENFORCED BY:** the language, as of 2026-09-20. This was a coding convention for a year and was
  re-violated twice - once hours after the lesson was written, once again while adding the
  "deliver --backend" tests on 2026-09-18 - which is what a discipline rather than an enforcement
  looks like. The bash runner is gone: `subprocess.run(..., capture_output=True)` returns the
  output and the exit status as separate fields, so there is no pipeline whose status can be
  silently substituted. The port also surfaced a second instance of the same family that the
  convention did NOT catch: `grep -q "PASS. script_hash_matches_ledger"` was matching
  `[PASS] script_hash_matches_ledger`, because `.` is a regex wildcard that happens to match `]`.
  A literal `in` does not, and the two assertions had to be corrected to `[PASS]` / `[FAIL]` to
  keep passing. A shell matcher is a regex matcher whether or not you wanted one.

## 2026-09-17 - A rule can be present, correct, and still not fire

- **Context:** The inherited gate checked `not source.get("quote")` to force verbatim retrieval.
  Every strong source in the ledger had `"quote": "PLACEHOLDER - retrieve and paste verbatim"`,
  which is truthy, so the rule passed while enforcing nothing.
- **Check:** A quote containing "placeholder" does not count as a quote.
- **Where:** `harness/factgate.py` (`_has_quote`), fixture-backed in `tests/test_gates.py`.
- **ENFORCED BY:** `harness/factgate.py` (`_has_quote`, the `PLACEHOLDER` regex), `tests/test_gates.py` ("a PLACEHOLDER quote does not count as a quote").

---

# 2026-09-18 — the generative-interface pass

## 2026-09-18 - A control pass is data, not a picture

- **Context:** The depth pass was rendered through the episode's AgX view transform, because that is
  what `reset_scene` sets and nothing changed it. AgX is a filmic curve: it compressed a linear
  0-1 depth range into **0.48-0.77**. The map was no longer a linear function of distance, which
  means a model consuming it would read a warped scene. Nothing errored; the file looked like a
  plausible grey image.
- **Check:** `depth` and `seg` render with the Standard view transform, restored afterwards. The
  observable is the histogram: a depth pass of a scene with real depth spread must span most of
  0-1, not sit inside half of it.
- **Where:** `harness/passes.py` (`_render_one_pass`, the `original_view` save/restore).
- **ENFORCED BY:** `harness/passes.py` (`_render_one_pass`'s view-transform override) - runs on every depth/seg pass; the effect is checked indirectly via `check_depth_pass`'s range assertions, not by a dedicated view-transform test.

## 2026-09-18 - A confounded test produced a wrong belief, and it shipped into the design

- **Context:** The first depth implementation assumed that setting `use_pass_combined = False` and
  `use_pass_mist = True` makes `write_still` emit the mist pass. It was "verified" against a plain
  grey cube — whose **beauty render is also grey**, so the test could not distinguish the two cases.
  The belief survived into a working-looking implementation and was only caught when the real scene's
  depth pass came out with colour in it (mean channel spread 0.095).
- **Check:** A pass test must use a subject whose beauty render and control pass are **different in
  the property being tested**. For depth that means checking R==G==B across all pixels, not eyeballing
  "does it look like a gradient". `harness/passes.py` now verifies greyscale purity, and the numbers
  are quoted in the README.
- **Where:** recorded here and in the `_depth_override_material` docstring; verified by the
  greyscale-outlier count (0 of 57,600 pixels) reported in the README.
- **ENFORCED BY:** `harness/check.py` (`is_greyscale`, used inside `check_depth_pass`) - runs on every real `passes` invocation that requests depth; not covered by an isolated fixture in `tests/`.

## 2026-09-18 - Blender 5.2 removed the compositor's arithmetic

- **Context:** The obvious way to normalise a Z pass is a compositor graph: `Render Layers -> Map
  Range -> Composite`. In Blender 5.2 **none of those three nodes exist.** `CompositorNodeComposite`,
  `CompositorNodeMapRange`, `CompositorNodeMapValue` and `CompositorNodeMath` are all gone;
  `CompositorNodeOutputFile` now accepts only `OPEN_EXR_MULTILAYER`; and the compositor node tree
  moved from `scene.node_tree` to `scene.compositing_node_group`. Four separate API breaks in one
  small feature.
- **Check:** The depth pass does not use the compositor at all. It puts the depth into the beauty
  pipeline as an unlit emission shader driven by `Camera Data > View Z Depth -> Map Range`
  (shader nodes still have Map Range), which renders through machinery that is known to work.
- **Where:** `harness/passes.py` (`_depth_override_material`). Related: the existing
  "Blender's Action API is mid-transition" entry above — the same class of failure, one subsystem over.
- **ENFORCED BY:** `harness/passes.py` (`_depth_override_material`) - the sole implementation; there is no compositor code path left to regress to.

## 2026-09-18 - A check that fires correctly can still be wrong about the geometry

- **Context:** Adding a brick tunnel bore to the ad spec made the camera assertion fire on every
  shot: "camera is INSIDE part 'bore'". The check is right in general — a camera inside a solid
  renders its interior — but a **ring is a hollow tube**, and the bounding box of a 34 m tube is a
  solid slab. The camera standing inside the tunnel was exactly where it should be.
- **Check:** None added, deliberately. The check already offers `camera_inside_ok = true`, and the
  right response is to use it **with a comment saying why**, so the next reader does not "fix" the
  problem by moving the camera out of the tunnel the shot is about.
- **Where:** `spec/ad01/ad01.toml` (`bore`), asserted by `harness/build.py` (`_assert_cameras_clear`).
- **ENFORCED BY:** nothing new - covered by `_assert_cameras_clear`'s existing `camera_inside_ok` opt-out (see the entry above), plus a spec comment for the next reader.

## 2026-09-18 - The un-excavated face must be roof and invert, never a wall

- **Context:** Building "the dig" as a first-class beat, a clay block was placed ahead of the shield
  to be the thing being cut. It was placed at the shield's own height, spanning z 3.25-6.85 — i.e.
  directly **between the camera and the shield**, because the camera is ahead of the shield in the
  direction of drive. The shot rendered a wall. Two successive rounds of camera repositioning failed
  to fix it because the camera was never the problem.
- **Check:** None automatic. The rule is geometric and stated inline: material ahead of the shield
  belongs above and below the frame's subject, leaving the cells visible in the gap. Found by the
  storyboard pass, which is what it is for.
- **Where:** `spec/ad01/ad01.toml` (`face_upper`, `face_lower`).
- **ENFORCED BY:** nothing - deliberately manual, per Context. The storyboard pass is the control.

## 2026-09-18 - Two channels that are one mechanism must share a time window

- **Context:** In `spec/ep01/ep01.toml` shot 5, the jack screws rotated across the *whole* shot
  (2160 degrees, six turns) while the cell frame only advanced in the last third. Four of the six
  turns moved nothing — a screw jack cannot do that. The spec validated, rendered, and was
  physically nonsense.
- **Check:** In `ad01` both channels share one window, and the invariant is stated as a number: 0.30 m
  over six turns is a **50 mm pitch**. A future assertion should read the advance and the rotation at
  the frame where motion starts and assert they agree within tolerance.
- **Where:** `spec/ad01/ad01.toml` (`cell_frame` and `screw_*` tracks); the ep01 version is still
  wrong and is annotated as such in `docs/archive/mvp-shield-ad-plan.md` §2.
- **Status update (2026-09-18):** The "future assertion" above was written as `[shot.mechanism]` in
  `spec.py`, and it checked `turns x pitch == advance` against three numbers hand-written in the same
  block — internally consistent, and never compared to what the `spin`/offset tracks actually did.
  `ad02` shipped with that gap twice over: c04's block matched its own arithmetic while the tracks
  driving it were unscoped and colliding with every other shot's tracks (see `docs/strategy/spec.md` H11, `docs/harness/backlog.md`), and
  c05 advanced the cell 0.26 m with no mechanism block and no spin track at all, one shot after the
  block that *was* checked. Fixed the same day: `_check_mechanisms` in `harness/spec.py` now derives
  `turns` and `advance` from the tracks actually applying to the shot and checks the declared numbers
  against those. ENFORCED BY: `tests/test_spec_validation.py` ("mechanism blocks are checked against tracks").

## 2026-09-18 - Blender's AREA lights default to pointing straight down

- **Context:** The ad's "tunnel work lights" were placed at head height and given no rotation. An
  AREA light's emission direction is its -Z axis, so both lights aimed at the floor. The subject was
  black. Nothing warned; the render was just dark, which is easy to mistake for a lighting-design
  problem rather than a bug.
- **Check:** A light may now declare `look_at`, exactly as a camera does, and `build.aim` is reused.
  A light aimed at a point is what a spec author means; an Euler rotation is an implementation detail
  they will get wrong.
- **Where:** `harness/spec.py` (`LIGHT_KEYS`), `harness/build.py` (`build_lights`).
- **ENFORCED BY:** `harness/spec.py` (`LIGHT_KEYS` includes `look_at`), `harness/build.py` (`build_lights` reuses `aim`) - runs whenever a light declares `look_at`; no fixture test.

## 2026-09-18 - A free hosted endpoint that does not exist is not a plan

- **Context:** The Cosmos plan assumed a hosted API at `build.nvidia.com`. There isn't one: the model
  page is a scenario-locked demo with **no code sample and no endpoint URL**, `cosmos-transfer2.5-2b`
  is absent from the `/v1/models` catalogue, every plausible hosted path returns 404, and the
  self-hosted NIM's health paths 404 on both NVIDIA hosts. The only path is a self-hosted NIM on
  **65.4 GB** of VRAM. Several turns were spent probing for an endpoint that was never there.
- **Check:** The access path is recorded as resolved-and-negative in
  `docs/archive/mvp-shield-ad-plan.md` §4, with the probe results, so nobody re-runs the search. A backend
  that needs a host says so via `missing_credentials` and its `note` field, and `harness backends`
  prints it.
- **Where:** `docs/archive/mvp-shield-ad-plan.md` §4, `harness/backend.py` (`CosmosNimBackend.note`).
- **ENFORCED BY:** `harness/backend.py` (`CosmosNimBackend.note`, printed by `harness backends`) - a documentation guard, not a code assertion; nothing stops someone re-pointing `COSMOS_NIM_URL` at a hosted endpoint that still does not exist.

## 2026-09-18 - A key pasted into a transcript is disclosed

- **Context:** An API key was pasted into a chat session rather than read from a file. Whatever else
  is true, it now exists in that transcript, and a transcript can be shared, forked or exported.
- **Check:** `.gitignore` gained `.env` / `.env.*` (with `!.env.example`) — the repo had **no** env
  pattern at all, so a key file would have been committable by default. Secrets are read at call time
  from a gitignored file and never echoed.
- **Where:** `.gitignore`, `harness/backend.py` (`load_env`, `ENV_FILE`). The key in question should
  be rotated.
- **ENFORCED BY:** `.gitignore` (`.env`, `.env.*`, `!.env.example`) - mechanically verified this session (`git check-ignore -v .env.local` confirms it stays untracked).

## 2026-09-18 - The best backend is the one you can run today, if it is shaped like the one you want

- **Context:** The plan was built around Cosmos because Cosmos is the right long-term destination —
  multi-control conditioning, an open licence, a documented Sim2Real pipeline. Then it turned out
  there is no hosted Cosmos API, and the only path is a self-hosted NIM on **65.4 GB** of VRAM with
  an NGC key, a Docker container and a 20 GB model pull. That is not a first step; it is a project.
- **Check:** The initial backend is chosen on **shape plus reachability**, not on destination
  quality. fal.ai's Wan VACE is depth-conditioned — the *same control pass* Cosmos Transfer takes —
  and costs $0.08/s behind one key with no minimum. So the pipeline built on it ports to Cosmos by
  changing one string. `harness backends` prints each backend's cost and its honest status, and
  `generate --dry-run` verifies setup without spending.
- **Where:** `harness/backend.py` (`DEFAULT_WAN_URL`, the `wan` backend docstring), README
  "Start with `wan`, not `cosmos`".
- **ENFORCED BY:** `harness/__main__.py` (`cmd_backends`, `--dry-run` in `cmd_generate`) - both runnable and confirmed working this session.

## 2026-09-18 - The one pass that two backends share is the one worth making first-class

- **Context:** Five control passes are rendered. Cosmos takes four of them (depth, seg, edge, blur);
  Wan VACE takes depth and pose and has **no canny and no normal** (verified from its control
  registry). The intersection of the two is **depth alone**.
- **Check:** `depth` is the pass prioritised for correctness — linear, full-range, normalised once
  per shot, verified greyscale — because it is the only one that survives a backend swap. A pipeline
  built around `seg` or `edge` would be locked to Cosmos and would have to be rebuilt to move.
- **Where:** `harness/passes.py` (depth is the pass with the most verification effort),
  `harness/backend.py` (`WanVaceBackend.requires = ("plate", "depth")`).
- **ENFORCED BY:** `harness/check.py` (`check_depth_pass`) - the most thorough of the pixel checks, wired into `cmd_passes`; runs on every real `passes` invocation that requests depth.

## 2026-09-18 - Depth polarity is a convention, and guessing it wrong looks like a model failure

- **Context:** The first real Wan VACE generation preserved the scene's structure almost perfectly
  and still came out as a flat amber silhouette. The cause was not the model: **depth was inverted.**
  This repo's map was near=black/far=white; VACE expects **near=white/far=black**. Downloading fal's
  own reference depth video and *looking at it* settled it in one minute — the woman is near-white,
  the buildings mid-grey, the sky black.
- **Check:** The polarity is asserted in the code as a comment with its evidence, and the observable
  is quotable: a correct depth pass of a subject at the look-at point has a mid-range **mean**
  (measured 120.9 of 255), not a saturated one (248.4 before the fix). Compare against the reference,
  never against intuition.
- **Where:** `harness/passes.py` (`_depth_override_material`, `To Min = 1.0 / To Max = 0.0`).
- **ENFORCED BY:** `harness/check.py` (`DEPTH_MEAN_MIN`/`DEPTH_MEAN_MAX` in `check_depth_pass`) - would flag a re-inverted polarity as saturated toward one end; all five `ad02` shots measured 113-156 (in range) when re-checked 2026-09-18.

## 2026-09-18 - Two attempts at "derive the near/far from geometry" both failed

- **Context:** Setting the depth range from the scene's measured bounds is the obvious approach and
  it was wrong twice. Including every part let the **240 m ground plane** and a **34 m tunnel bore**
  set the range, compressing the subject into a sliver. Excluding the enclosures just let the ground
  plane win instead, and the output was uniformly white.
- **Check:** The range comes from the **camera's distance to its look-at point** (`× 0.4` to `× 2.5`).
  Boring, predictable, and independent of whichever scenery happens to be in the file. What matters
  is not the constant but that it is set **once per shot, never per frame**.
- **Where:** `harness/passes.py` (`_depth_range`).
- **ENFORCED BY:** `harness/passes.py` (`_depth_range`) - the sole implementation. Note: the multipliers have since moved to `x0.22`/`x1.9` (from the `x0.4`/`x2.5` this entry recorded) as more shots were staged; the constant was never the point, only that it is set once per shot.

## 2026-09-18 - Blender's default camera clip planes are not authored intent

- **Context:** `_depth_range` preferred the camera dict's `clip_start` / `clip_end` when present.
  They were present — as Blender's own defaults, **0.1 to 184.5** — because they are not in the spec's
  camera vocabulary and so could not have been authored. The result: a subject four metres away mapped
  to 2% of the ramp, i.e. pure white. The code was faithfully honouring a number nobody wrote.
- **Check:** Do not read keys the spec's schema does not define. If a value cannot have been authored
  in the spec, it is a default, and treating a default as intent is the same class of error as the
  closed-vocabulary rule at the top of this file.
- **Where:** `harness/passes.py` (`_depth_range`), `harness/spec.py` (`CAMERA_KEYS`).
- **ENFORCED BY:** `harness/spec.py` (`CAMERA_KEYS` - `clip_start`/`clip_end` are not declared keys, so `_unknown()` would reject them if ever added to a camera table).

## 2026-09-18 - A duplicate function definition is silent, and Python takes the last one

- **Context:** Rewriting `_depth_range` with a scripted string replace inserted the new version
  **without removing the old**. Python resolved to the *later* definition, so two rounds of careful
  fixes changed nothing at all — the same broken number came back three times to three decimal
  places, which is what finally gave it away. A render that does not change when you change the code
  is not a stubborn model, it is a shadowed function.
- **Check:** `grep -c "^def <name>"` after any scripted rewrite. An unchanged measurement across a
  changed input is the signal; treat identical results after a fix as a bug in the fix.
- **Where:** `harness/passes.py` — the duplicate was removed (67 lines).
- **ENFORCED BY:** `tests/test_static.py` ("harness hygiene" - an AST pass that fails on any shadowed top-level definition) - the automated form of the manual `grep` this entry describes.

## 2026-09-18 - urllib has no CA bundle on this machine; curl does

- **Context:** Downloading the finished video from fal's CDN failed with
  `CERTIFICATE_VERIFY_FAILED: self-signed certificate in certificate chain` — under the *system*
  Python, while `curl` on the same box succeeded. Not a fal problem and not a network problem: the
  interpreter has no trust store configured.
- **Check:** `harness/backend.py` downloads via `curl`, which is already a hard dependency for the
  `edge` and `vis` passes. One fewer thing that depends on how Python was installed.
- **Where:** `harness/backend.py` (`_download`).
- **ENFORCED BY:** `harness/backend.py` (`_download` uses `curl`) - architectural: there is no `urllib` download path left for the final video fetch to regress to.

## 2026-09-18 - fal's queue has a cold start measured in minutes, and that is not a failure

- **Context:** The first generation attempt was killed at a 600 s timeout with no output, which read
  as a hang. It was not. Polling two jobs in parallel showed both sitting at `IN_QUEUE` with
  `queue_position: 0` for roughly **two and a half minutes** before moving to `IN_PROGRESS`, then
  completing almost immediately. Three sequential shots exceeded the shell timeout on queue time
  alone.
- **Check:** `generate` reports fal's queue state as it polls, so `IN_QUEUE` is visible rather than
  silent, and long runs belong in the background. Untested corollary: submitting the shots
  concurrently would cut wall-clock time roughly three-fold, and should be the next change.
- **Where:** `harness/backend.py` (`WanVaceBackend._poll`), and `--dry-run` in
  `harness/__main__.py` for checking setup before spending.
- **ENFORCED BY:** `harness/backend.py` (`WanVaceBackend._poll` status printing). The "untested corollary" about submitting concurrently is no longer a corollary - `cmd_generate`'s submit-all-then-collect-all branch (`harness/__main__.py`) implements it.

## 2026-09-18 - In Blender's XYZ Euler, Z is applied LAST, so a spin belongs on the axis the shaft lies along

- **Context:** A screw laid along +Y by `rot_x = -90` was animated to turn by writing
  0→2160° into the `.z` rotation slot. Blender's XYZ order is **R = Rz·Ry·Rx**, so Z is the
  outermost rotation: it took the *already-laid* shaft and swung it about the world Z axis. The
  screws swept round like a propeller. The user's note was four words long — "the screws are
  screwing all weird" — and the contact sheet showed it immediately: horizontal, tipping, vertical.
- **Check:** A `spin` channel that means "turn about this part's own axis". The harness composes it
  as `R_base @ R_spin` and writes the resulting Euler, so a spec author never has to know Blender's
  axis order. With the shaft along +Y, `Ry` leaves +Y unchanged — which is exactly why `.y` is the
  slot that works and `.z` is the slot that produced a windmill.
- **Where:** `harness/render.py` (`_apply_tracks`, the `spin` branch), `spec.py` (`CHANNELS`).
- **ENFORCED BY:** `harness/render.py` (`_apply_tracks`, `spin` branch) - the sole implementation; no numeric regression test, but `check_motion`'s worst-step threshold (see two entries below) would flag a regression to the old propeller-sweep magnitude.

## 2026-09-18 - An object that is symmetric about its axis cannot show that it is turning

- **Context:** The first fix attempt moved the spin to the right Euler slot. Nothing changed
  visibly, because the screw was a plain cylinder — rotationally identical at every angle. The
  animation had been trying to show something the geometry could not express, which is *why* the
  original bug went unnoticed: writing a spin into the wrong slot looked like it was doing
  something, because the geometry gave no feedback either way.
- **Check:** `gen_screw` takes a `bar` parameter and draws a tommy bar through the head — which is
  what these jacks were actually turned with. The rule: if an animation is supposed to be visible,
  the geometry must be asymmetric about the axis being animated.
- **Where:** `harness/generators.py` (`gen_screw`).
- **ENFORCED BY:** `harness/generators.py` (`gen_screw`, `bar` param) - and, as of 2026-09-18, `harness/library.py`'s import-time drift assert against `spec.GENERATOR_PARAMS`, which is what caught `bar` missing from the catalogue in the first place.

## 2026-09-18 - A per-frame check structurally cannot see a fault that lives between frames

- **Context:** The windmilling screws passed every check in the harness. `check_storyboard` saw a
  good picture. `check_depth_pass` saw a neutral, in-range, stable depth map. `check_clip` saw a
  clip that was not black. Each frame was fine; the *motion* was nonsense. Nine checks guarded
  appearance and none guarded motion.
- **Check:** `check_motion` — frames sampled across the shot, adjacent differences measured. A
  frozen shot (nothing changes) is a hard failure; a busy one is a warning to go and look. Wired
  into `check_depth_pass`.
- **Where:** `harness/check.py` (`check_motion`, `frame_diff`).
- **ENFORCED BY:** `harness/check.py` (`check_motion`, called from `check_depth_pass`) - runs on every real depth-pass check; not covered by a synthetic fixture in `tests/test_checks.py` (see H18, `docs/harness/backlog.md`).

## 2026-09-18 - A threshold calibrated on the bug cannot separate the bug from the fix

- **Context:** `check_motion` first flagged the windmill at a worst-step of 18.1 and 19.5 against
  6.8–7.8 for clean shots — a clean separation. After the fix, the *correct* animation measured 14.3
  and 16.3. **The bug and the correct behaviour now overlap.** Any single threshold either passes the
  fault or fails the fix.
- **Check:** Two tiers, and an honest one: `MOTION_BUSY` (12.0) is a warning, `MOTION_MAX_STEP`
  (60.0) is a failure. The contact sheet is the adjudicator. A check that pretends to a precision it
  does not have is worse than a smoke alarm that says it is a smoke alarm.
- **Where:** `harness/check.py` (the threshold block, with both measurements recorded).
- **ENFORCED BY:** `harness/check.py` (`MOTION_BUSY`, `MOTION_MAX_STEP`) - same as above, real but not fixture-tested.

## 2026-09-18 - A scripted string replace that matches nothing does nothing, silently

- **Context:** The mechanism assertion was written, "added", and reported as added — and never
  appeared. The replacement targeted `shots.append(shot)`; the code says `shots.append(s)`. This is
  the **second** time in one session that a scripted edit silently no-op'd (the first left a
  duplicate `_depth_range` that shadowed the fixed one). In both cases the giveaway was a fix that
  changed nothing.
- **Check:** After any scripted rewrite, `grep` for a string that only the new code contains and
  assert a non-zero count. An unchanged result after a fix is the signal.
- **Where:** this file's sibling in `tests/test_static.py` — "no shadowed top-level definitions" — catches
  the duplicate half of this class; the no-op half is caught only by grepping after the edit.
- **ENFORCED BY:** `tests/test_static.py` ("harness hygiene") catches the duplicate-definition half; the no-op-replacement half remains a manual `grep`-after-edit discipline, same as the entry above.

## 2026-09-18 - A documented check is not an enforced check

- **Context:** A full audit of `harness/` and of the most recent paid generation
  (`renders/ad02/generated-wan/shield-cycle-480p-captioned.mp4`) found that `check_clip` — written,
  tested, and described in this file's own docstrings — was called in the sequential branch of
  `cmd_generate` and never called in the `submit`/`collect` branch, which is the branch taken
  whenever more than one shot is generated, i.e. every real run. The payoff shot of `ad02` shipped
  crushed to black, and the check that would have caught it never ran. Three more findings from the
  same audit — the mechanism check above, a fix aimed at a colour channel `wan` does not consume, and
  a "fixed" mid-shot artefact still visible in the delivered clip — were each already written down
  somewhere in this file as a lesson learned, and shipped anyway. The full audit is
  `docs/strategy/spec.md` Part II-III.
- **Check:** `deliver --backend` now refuses a crushed-to-black or mistimed generated clip before it
  ships (`harness/__main__.py`, `_deliver_from_backend`), `cmd_generate`'s `_accept` refuses one
  before counting it as delivered, and `docs/strategy/spec.md` §16 states the acceptance criteria the fix is
  measured against. Going forward: a lesson recorded here without a line naming what enforces it is a
  lesson that can ship again.
- **Where:** `harness/__main__.py` (`cmd_generate`'s `_accept`, `cmd_deliver`'s
  `_deliver_from_backend`), `tests/test_backend.py` ("deliver --backend" section), `docs/strategy/spec.md`.
- **ENFORCED BY:** `harness/__main__.py` (`_accept`, `_deliver_from_backend`), `tests/test_backend.py`
  ("deliver --backend" section - a synthetic black clip and a synthetic mistimed clip are both
  proven refused). Every other entry in this file was given this same line the day this one was
  written: annotating all 40 in one pass was first tried and rejected as "asserting enforcement
  for lessons nobody had just re-verified" - then done anyway, deliberately re-checking each
  "Check:" bullet against the current code rather than trusting it, which is what turned the
  batch pass from the trap it would have been into the same discipline this entry asks for.

## 2026-09-18 - An unsourced number can be arithmetically perfect and still describe a part that does not exist

- **Context:** S1's brief specified a 120 mm bore, 80 mm rod cylinder at 350 bar, derived 395.8 kN
  extending and 219.9 kN retracting, and correctly marked all three inputs `SOURCE NEEDED`. The
  arithmetic was checked and re-checked and was never wrong. When the datasheets were actually
  pulled, 350 bar was confirmed verbatim from Caterpillar's own 320 spec sheet - and **120 x 80 does
  not exist.** The Cat 320 boom cylinder ships in five bore/rod pairs and none of them is 120/80; the
  120 mm one has an **85 mm rod**. A correct sum over invented inputs is indistinguishable, on the
  page, from a correct sum over real ones. `SOURCE NEEDED` was doing the only work.
- **The sourcing improved the video, which is the part worth remembering.** The unsourced number
  made the point as "44% weaker" - a figure that sits between two manufacturer standards, which is
  the exact shape of a number picked to sound impressive. The sourced answer is **half**: the
  standard rod is bore / sqrt(2), so the rod covers half the piston and the annulus is half, and
  Rexroth sells it as the phi = 2 series with the ratio printed in its own catalogue column.
  Sourcing is not a compliance step applied to a finished script. It changed the script.
- **Check:** every number in `docs/videos/s01-hydraulic-cylinder/` now carries a ledger key, and
  `spec/s01/facts/s01.facts.json` carries bore and rod as F002 with two independent sources. The one
  fact that rests on a weak source - that this specific cylinder is a Cat 320 boom cylinder, F003 -
  is `status: unknown` with `treatment: omit`, so the script says "an excavator" and never names the
  machine. The claim the evidence cannot carry is not made to the viewer.
- **Where:** `docs/research/hydraulic-cylinder-datasheets-2026-09-18.md`,
  `spec/s01/facts/s01.facts.json`, `docs/videos/s01-hydraulic-cylinder/{brief,script}.md`.
- **ENFORCED BY:** `harness/factgate.py`, rule `every_fact_has_a_tier_1_to_3_source_or_declared_status`
  - a fact with no TIER-1..3 support must declare an honest status, which is what forces F003 to say
  `unknown` rather than quietly asserting a machine model. Verified this session: the gate passes 9
  of 11 checks on the s01 ledger and names the two it fails.

## 2026-09-18 - A rate-limited archive is a failing check, not a licence to invent a snapshot URL

- **Context:** `factgate` requires an `archive_url` on every web source, because "a rotted citation
  is indistinguishable from a fabricated one". While building the s01 ledger, `archive.org` returned
  **HTTP 429** and kept returning it. Three sources therefore have no snapshot. The tempting move was
  to write `https://web.archive.org/web/2026/<url>` for each - a URL of that shape is well-formed,
  passes the rule, and reads as a citation. It is also a URL nobody has confirmed resolves, and a
  well-formed link to a snapshot that does not exist is strictly worse than no link, because it
  *looks* checked.
- **Check:** the three sources carry no `archive_url`, `every_web_source_has_an_archive_url` **fails**,
  and `--publish` stays blocked. The failure is recorded as the top row of the "Known gaps" table in
  the research document, with the exact remaining action: submit five URLs to the Wayback Machine and
  paste the snapshots back in. A gate failure that names its own fix is a working gate.
- **A rule of shape only checks shape.** Rule 4 tests that the field is non-empty; it cannot test
  that the URL resolves. Any `web.archive.org/web/<year>/...` string satisfies it. That is not an
  argument for weakening the rule - it is the reason the field must never be filled in by hand
  from a pattern rather than from a response.
- **Where:** `spec/s01/facts/s01.facts.json` (sources S001-S003),
  `docs/research/hydraulic-cylinder-datasheets-2026-09-18.md` §8.
- **ENFORCED BY:** `harness/factgate.py`, rule `every_web_source_has_an_archive_url` - observed
  failing on this ledger this session, which is the only evidence that a check works.

## 2026-09-18 - An annulus does not look like its area, and no amount of correct arithmetic fixes that

- **Context:** S1's whole reveal is that a cylinder's retract face is half its extend face. The
  numbers are sourced, published and cross-checked: 153.94 cm2 against 75.40 cm2, a ratio of 0.490.
  A storyboard probe rendered the two figures front-on and to scale before the generator was
  written, and **the ring reads as about a third of the disc, not a half**
  (`scratchpad/probe/areas_01.png`). Human area perception is poor for annuli and biased low. The
  script asked the viewer to see a fact that the picture does not show.
- **The fix was available because the geometry is real.** The piece removed - the rod's circle,
  78.54 cm2 - and the piece left - the ring, 75.40 cm2 - are near enough the same size. So Beat 3
  now gathers the ring into a solid circle and sets it beside the rod's circle: 98.0 mm against
  100.0 mm, visibly equal. The halving is demonstrated instead of asserted, and the 4% it is off by
  is exactly the gap between 49% and 50%, which is the reason the narration says "half" and never
  "exactly half".
- **This is the storyboard rule paying out on an editorial claim, not a staging one.** "Storyboard
  before you render" has so far caught cameras in the wrong place. Here it caught **a true sentence
  that the frame does not support** - which no render check can ever find, because the frame is
  correct, well-lit, and wrong only as an argument.
- **Where:** `docs/videos/s01-hydraulic-cylinder/script.md` Beat 3 (restaged, with the superseded
  staging kept above it), open question 3 (answered "no").
- **ENFORCED BY:** nothing automatic, and it cannot be - `check_storyboard` correctly passes the
  frame that fails. The enforcement is procedural and is now written into the script: Beat 3 carries
  the probe frames by path, so the next person to restage it has to look at the evidence that the
  obvious version does not work. `docs/videos/README.md` already requires facts before script; this
  adds that a claim about what the viewer will SEE is not settled until a frame exists.

## 2026-09-18 - A camera inside geometry does not error, it hangs

- **Context:** An axial probe put the camera 0.071 m from the cylinder axis. The barrel wall spans
  0.070-0.085 m, so the camera sat **inside the wall** - a closed, metallic, double-sided shell.
  Cycles did not warn, did not error and did not render. It bounced rays inside the shell until the
  job was killed at several minutes for a frame its neighbours rendered in 23 seconds.
- **This is the sibling of the repo's oldest failure.** "Every camera must sit inside the bore
  radius" was learned from cameras placed OUTSIDE the tunnel, which rendered black. The same class
  of fault placed inside solid geometry does not render black - it does not render at all, and the
  symptom is a slow machine rather than a bad frame.
- **CORRECTION, same day.** This entry first said no check existed and the harness had the same
  hole. **That was wrong, and wrong in the worst direction** - it told a future reader a guard was
  missing when it is there and tested. `build._assert_cameras_clear` refuses a camera whose position
  falls inside any part's bounds unless that part sets `camera_inside_ok`, and `tests/test_spec_validation.py` proves
  it fires (`tests/fixtures/camera_inside.toml`, "camera inside geometry is rejected") and does not
  over-fire (`camera_clear.toml`). It was written after a camera inside the flood-water box rendered
  s07 black.
- **So the actual lesson is smaller and sharper:** the probe hung **because it was a throwaway script
  that bypassed the harness.** The guard exists; nothing outside `harness build` runs it. Scratch
  scripts get none of the repo's accumulated protections, which is an argument for probing through
  the harness wherever a fixture can carry the question, and for not trusting a scratch render's
  silence.
- **Where:** `scratchpad/probe/section_probe.py` (throwaway, bypassed the check),
  `harness/build.py` (`_assert_cameras_clear`), `tests/test_spec_validation.py`.
- **ENFORCED BY:** `harness/build.py` (`_assert_cameras_clear`) and `tests/test_spec_validation.py` ("camera inside
  geometry is rejected" / "camera clear of geometry is accepted") - both re-read this session rather
  than assumed, which is how the original claim in this entry was found to be false.

---

## 2026-09-18 — A threshold check cannot see drift. Only a comparison can.

- **Context:** Every automated check in the harness asked a question about **one artefact in
  isolation** — is this frame black, is it flat, is this depth map in range, is this clip crushed.
  Not one asked whether the render matched the last known good one. Threshold checks catch
  catastrophes and are structurally blind to gradual change, and "video that gets measurably better
  every time" is a claim about change. `goldens/` had been declared in the README as "canary renders
  for regression" since the first commit and was **empty**; `LESSONS.md` itself already recorded
  that, with `ENFORCED BY: nothing - prose only`, and the response had been to write more prose.
- **The calibration, because a threshold nobody can trace is a taste.** Measured on `spec/ad02` at
  480x854 / 8 spp / CPU Cycles, 2026-09-18:

  | Comparison | SSIM |
  |---|---|
  | same spec, same code, two separate runs, all five shots | **1.000000** |
  | `lens_mm` 40.0 -> 41.0 (a 2.5% focal change) | 0.859949 |
  | camera moved 0.05 m of a 4 m throw | 0.826597 |

  The smallest change a human would call a change costs about 0.14 of SSIM, so the gap is wide and
  the exact floor is not load-bearing. `GOLDEN_SSIM_MIN = 0.995` sits *below* today's noise floor to
  leave headroom for the render node — GPU Cycles will not match CPU — without being anywhere near
  a real regression. **Re-measure when the render node lands; do not just relax it.**
- **Why SSIM and not a hash, and a correction I had to make to my own claim.** `ROADMAP.md` said
  "Cycles is not bit-reproducible, so hash testing is a mirage". I first wrote the opposite, on the
  strength of five SSIM scores of 1.000000. Both statements were too coarse, and checking properly
  split them apart: two clean runs are **pixel-identical** — the decoded RGB of all five shots
  hashes the same — while the **PNG files differ every single run** in their container bytes. So
  hashing the file is a mirage (the ROADMAP's conclusion was right), hashing decoded pixels would
  work today (its stated reason was not), and neither survives a GPU render node, where the pixels
  themselves will drift. SSIM is correct in all three cases.
- **The near-miss worth recording.** The first comparison I ran said c01's pixels differed, and I
  was one step from writing that into the docs as a measured fact. They differed because an earlier
  step in the same session had copied a deliberately-perturbed frame over that directory to prove
  the canary fires. A measurement taken from a directory something else has written to is not a
  measurement — the re-render into a clean directory is what made it one.
- **Two design decisions worth keeping.** A shot with no golden **warns, it does not fail** — the
  first run of a new spec must not be red for having no history. And blessing is **never
  automatic**: a canary that seeded itself on first sight would lock in whatever happened to be on
  disk, including the regression it exists to catch.
- **Check:** `harness verify` scores each shot's storyboard still against `goldens/<ep>/<shot>.png`
  and fails below the floor. `tests/test_checks.py` proves the metric reads 1.0 on an unchanged frame and
  fires on a changed one, and that an unblessed shot only warns.
- **Where:** `harness/check.py` (`ssim`, `check_goldens`, `GOLDEN_SSIM_MIN`),
  `harness/__main__.py` (`_canary`, `_canary_stills`, `verify --bless`), `goldens/ad02/`.
- **ENFORCED BY:** `tests/test_checks.py` ("the canary scores 1.0 on an unchanged frame and fires on a
  changed one", "a shot with no canary warns, it does not fail") — and, on real renders,
  `harness verify`, which was confirmed this session to exit 3 on a genuine 5 cm camera move and 0
  on a clean re-render. `goldens/ad02` is blessed; **`goldens/ep01` is not**, so ep01 has no canary.

## 2026-09-18 — A fix that names the end it fixed is naming the end it did not

- **Context:** H3 made `PassProfile.frame_count` **refuse** a shot past a backend's `max_frames`,
  because the old silent clamp rendered a 6 s shot as 81 frames and played it 18% fast. The
  docstring that recorded the fix said *"Refuses rather than clamps **at the top end**."* The line
  immediately above it, `n = max(self.min_frames, n)`, went on silently clamping the bottom end for
  another day. On `wan`'s real profile (`min_frames=49`) a 2.0 s shot rendered as 49 frames — 3.06 s
  of picture — and `_apply_tracks` stretched the whole normalised animation across it, so the shot
  played **35% slow**.
- **It is worse than the fault it mirrors.** An over-long shot plays fast and ships. A short one
  plays slow, and then `deliver --backend` correctly refuses the clip for a duration that disagrees
  with the spec: the generation is paid for **and** unusable. The two guards were four lines apart.
- **The general form:** a docstring that scopes itself ("at the top end", "on the Blender path",
  "for a TOML spec") is documenting a boundary the author was standing on. Read it as a map of where
  the fix stops. The same shape produced H23 — `factgate.narration_text` hashed the whole file "for
  any other suffix" than `.toml` — and H1, where `check_clip` ran on the single-shot branch only.
- **Check:** `frame_count` raises on either side of a backend's window, naming the seconds that
  would fit.
- **Where:** `harness/passes.py` (`PassProfile.frame_count`).
- **ENFORCED BY:** `tests/test_backend.py` ("a shot below a backend's min_frames is refused, not silently
  padded") — asserted against `WanVaceBackend.profile` itself, not a hand-made profile, so it
  tracks the real backend if its window changes.

## 2026-09-18 — The most expensive bug had the cheapest available test, and did not have it

- **Context:** The windmilling screws — `spin` written into the `.z` slot of a part's Euler, so a
  shaft laid along Y swung about the *world* Z axis like a propeller — shipped, cost a paid
  generation, and passed `storyboard`, `depth` and `clip` without a murmur because every individual
  frame was a good picture. The response was `check_motion`, which is **honest that it cannot
  adjudicate**: after the fix, correct rotation measures 14.3–16.3 against the bug's 18.1–19.5, so a
  single threshold cannot separate right from wrong. That left the repo's worst bug guarded by a
  WARNING. The entry recording the fix said, accurately, "the sole implementation; no numeric
  regression test."
- **A numeric test was available the whole time, in six lines.** Turning a screw does not move the
  axis it turns about. So the local Z axis of `R_base @ R_spin` must equal that of `R_base`, for
  every base orientation and every angle. It needs `mathutils` and no Blender scene, and runs in
  milliseconds. The bug violates it by 1.414.
- **The trap in the fixture.** At a whole number of turns the buggy composition lands back on the
  correct answer — `ad02`'s track ran 0 -> 2160 degrees and the two agree at **both** keyframes. Only
  the interpolated angles between them were wrong, which is precisely why no per-frame check could
  ever see it. A test using only 360-multiples would have passed on the broken code.
- **The general form:** when a check is downgraded to advisory because it cannot separate right from
  wrong, that is a signal to go looking for the **invariant** underneath, not to accept the warning
  as the guard. "What does this operation promise not to change?" is usually cheaper to assert than
  the effect is to measure.
- **Check:** `spin_euler` holds the part's own Z axis for 24 base/spin pairs, with the `.z`-slot bug
  as the control that proves the assertion can fail.
- **Where:** `harness/render.py` (`spin_euler`, extracted from `_apply_tracks` so the test exercises
  shipped code rather than a copy that can drift), `tests/spin_axis.py`.
- **ENFORCED BY:** `tests/test_scripts.py` ("a spin turns the part about its own axis, for every base
  rotation").

## 2026-09-18 — The edit order came from the filesystem, not from the spec

- **Context:** `assemble._shot_dirs` globbed the episode directory for anything containing
  `frame_*.png` and `sorted()` the result. Two faults rode in it, both silent, both in the
  deliverable. **Filename order is not edit order** — it agrees with the spec only while every shot
  id happens to sort the way it is listed, so ids `s1, s2, s10` cut in the order 1, 10, 2 and
  narrative ids (`open`, `dig`, `advance`) cut alphabetically. And **a directory is not a shot
  list** — rename or drop a shot and its old frames stay on disk, and went straight back into the
  cut. `deliver`'s duration guard catches a surplus shot; it cannot catch a reordered one.
- **It was live, not hypothetical.** `renders/ep01/manifest.json` currently reports **3 shots** at
  480x854 because a later `render --shots` run overwrote it with a partial list, while the delivered
  `ep01.mp4` is 8 shots at 384x682. The two disagree in the repo as it stands.
- **Note which path had it right.** `_deliver_from_backend` iterates `ep.shots`; the Blender path
  globbed. The correct pattern was already in the file — the same shape as H2, where `cmd_deliver`'s
  duration check existed and was not carried across to the generated path.
- **Check:** the spec's shot list is the edit order; a declared shot with no frames is refused, and a
  frame directory that is not a shot in the spec is refused rather than cut in.
- **Where:** `harness/assemble.py` (`_shot_dirs`, `assemble(shots=...)`), `harness/__main__.py`
  (`cmd_pipeline`, `cmd_deliver` pass `[s["id"] for s in ep.shots]`).
- **ENFORCED BY:** `tests/test_assemble.py` ("the cut follows the spec's shot order, not the filesystem's",
  "a leftover or missing shot directory is refused, not cut in"). The fixture uses ids `s1, s2, s10`
  deliberately, and asserts that they do **not** already sort into spec order — a fixture whose ids
  sort correctly would pass on the broken code, which is the same trap the spin test's whole-turn
  angles set.

## 2026-09-18 — "Fitted" printed a success line over a truncation

- **Context:** `audio.synthesise` time-compresses a VO take that overruns its shot, capped at
  `MAX_TEMPO = 1.35` because "truncating narration mid-sentence is a defect; a 1.1–1.2x tempo shift
  is not" — the module comment says exactly that. Past the cap it clamped the tempo anyway and let
  the trailing `-t slot` hard-cut the remainder, printing `fitted: c03: VO 4.00s in a 2.00s slot ->
  tempo 1.35x`. Narration is the product. The code removed words and reported it in the vocabulary
  of success.
- **The check the repo already believes in, applied to audio.** Every pixel check here exists
  because a failure was silent; this was a silent failure in the one track nobody looks at, since
  reviewing a cut means watching the picture.
- **Consequence to watch.** `cmd_deliver` catches `AudioError` and continues **without a voice
  track**, which is correct when `say` is simply absent (not a Mac) and wrong-looking when the script
  does not fit. The warning now reads `WARNING: delivering with NO VOICEOVER` so it cannot be read
  past. Splitting the two causes into two exceptions is the real fix and is not done.
- **Check:** an overrun past `MAX_TEMPO` raises, naming the shot, the seconds that would be cut, and
  the shot length that would fit.
- **Where:** `harness/audio.py` (`synthesise`), `harness/__main__.py` (both `AudioError` handlers).
- **ENFORCED BY:** the raise in `harness/audio.py`, on every `voice` and every `deliver` that
  synthesises — **no fixture test.** It needs macOS `say`, so it cannot run on the render node; a
  test would have to inject a duration rather than speak. Honest answer: unguarded by the suite.

## 2026-09-19 - A track can be applied, correct, and completely invisible

- **Context:** s01's hook is a cylinder extending and retracting. The track was written, validated,
  applied, and moved the rod 0.55 m. `frame_diff` between the first frame of the stroke and the last
  is **0.0000** - every pixel identical across 150 frames. The rod ran off the right edge of frame,
  its visible length is a featureless cylinder, and the piston was hidden inside a solid barrel, so
  the only features that could have revealed the travel were all out of shot. 3.5 hours of render
  went into a hook that is a still photograph.
- **This is the sibling of the windmilling screws, from the other side.** That entry says an object
  symmetric about its axis cannot show that it is *turning*. This one: an object symmetric about its
  axis cannot show that it is *sliding along that axis* either - unless an end, a shoulder or a mark
  is in frame. The fix was not the track. It was shortening the rod from 1.50 m to 1.20 m and
  widening the camera so the **tip** stays in shot through the whole stroke, because the tip is the
  only feature the motion has.
- **Also found: three of six shots were frozen and the harness said the render passed.** `verify`
  reported `all 900 artefact(s) pass`. It runs `check_storyboard`, `check_depth_pass`, `check_clip`
  and the canary - and `check_motion` only ever existed as a call inside `check_depth_pass`,
  reachable only when control passes exist. On `local`, the shipping path, it had never run. See
  **H27**, now fixed.
- **And the check's own report named the wrong thing.** `frames[0].parent.parent.name` is the
  EPISODE for `renders/<ep>/<shot>/frame_*.png` and the literal string `"depth"` for a control pass.
  Every motion problem this repo has ever printed said `s01:` where it meant `b01:`. `check_motion`
  now takes an explicit `label`.
- **Where:** `harness/check.py` (`check_motion`), `harness/__main__.py` (`cmd_verify`),
  `spec/s01/s01.toml`, `docs/harness/backlog.md` H27.
- **ENFORCED BY:** `harness/__main__.py` (`cmd_verify` now runs `check_motion` per shot directory -
  grouped, because over a flat glob the seam between two shots reads as a lurch) and `tests/test_checks.py`
  ("verify reports a frozen shot and not a moving one"), which builds six identical frames and six
  animating ones and asserts the report distinguishes them. The test was written wrong first - it
  synthesised "moving" frames that were all the same colour - and failed, which is how it earned
  being believed.

## 2026-09-19 - Three hypotheses, all wrong, killed by one control

- **Context:** s01 draft 4 rendered at **43.5 s/frame** against draft 2's 9.8. Something in the Tier
  2/3 rework had quadrupled the cost. The obvious suspect was the new backdrop: a 26 m diffuse plane
  at roughness 1.0, brightly lit, bouncing global illumination into every ray.
- **Hypothesis 1, shrink it.** 26 m -> 7 m. Measured **49.6 s/frame** - slightly *worse*.
- **Hypothesis 2, make it emissive** so camera rays return on first hit. Measured **47.4**. Emission
  turned a 16 m plane into a 16 m area light, which every shading point then samples. One expensive
  thing traded for a different expensive thing.
- **Hypothesis 3, it must be the new geometry** - the `label` text meshes, `crew`, the load rig.
  `harness build` prints per-part polygons: the entire scene is **5,672 polys across 50 objects**.
  The two text meshes are 630 and 447. Nothing here is heavy.
- **The control settled it: 41.4 s/frame with NO backdrop at all.** All four numbers are within noise
  of each other. The backdrop cost about 5%, not 4x, and had been innocent from the first guess.
- **The real cause is the improvement.** Draft 2 filled **1.9-2.4%** of frame, so ~98% of rays hit
  the free world background and cost nothing. Draft 4 fills **43.6%** with `metallic = 1.0` steel and
  chrome, and every one of those rays takes glossy bounces. The 4x is what filling a frame with metal
  costs. It is not a regression to be fixed; it is a price to be decided on.
- **So the lever was samples, and only samples.** 32 -> 16 spp measured 43.5 -> 24.5 s/frame, and
  with denoising on this geometry the two are visually indistinguishable. 10.9 hours -> 6.1.
- **The reason this took three wrong turns is that I never measured the control first.** Each
  hypothesis was tested against the *previous variant* rather than against the scene with the
  suspect removed entirely, so every result was consistent with the suspect being guilty. The control
  is the cheapest measurement of the set and it should have been the first.
- **And it invalidates a planning number.** `docs/strategy/slate.md` budgets ~210 hours for a
  7-minute Phase 1 cut, extrapolated from a render whose frames were 98% empty. At draft 4's density
  that estimate is low by roughly 4x. Recorded here rather than silently corrected, because the
  slate's number is load-bearing for when L1 gets scheduled.
- **Where:** `spec/s01/s01.toml` (`samples = 16`, with the measurement inline), `docs/strategy/slate.md`
  (unchanged, flagged), `harness/spec.py` + `harness/build.py` (`emission` material property - kept,
  because it is a legitimate feature even though it was not the fix).
- **ENFORCED BY:** nothing automatic, and honestly nothing should be - this is a judgement about what
  a frame is worth, not a rule. What IS enforced is `harness bench`, which exists precisely so
  throughput claims are measured; the failure here was not using it before committing a machine to
  an eleven-hour job.

## 2026-09-20 — Half the suite's pass cases could not fail

- **Context:** `tests/run.sh`'s `check()` helper ran the harness, captured the combined output, and
  grepped it. For an expect-**fail** case it asserted the phrase was present. For an expect-**pass**
  case it asserted only that the phrase was *absent* — and never looked at the exit status at all.
  So `check "camera clear of geometry is accepted" pass ...` stayed green if the build crashed for
  any reason whatsoever. Demonstrated on a nonexistent path: exit 2, `spec error: spec not found`,
  verdict `pass`. Three of the six cases were pass-expecting. The positive control this repo
  insists on for every negative fixture was, for a year, an assertion that could not fail.
- **Check:** A pass case asserts `returncode == 0` **first**; the absence of a phrase is the second
  assertion, never the only one. Absence of evidence is what a crashed process also produces.
- **Where:** `tests/test_spec_validation.py` (`test_build_accepts_a_clear_camera`).
- **ENFORCED BY:** `tests/test_spec_validation.py` — every `harness(...)` call site now asserts on
  `proc.returncode`, which is a field rather than something that has to be remembered.

## 2026-09-20 — 337 lines of the test suite were invisible to every tool that checks code

- **Context:** `tests/run.sh` was 702 lines, of which 337 were Python inside `<<'PY'` heredocs.
  `ruff check harness/ tests/` could not see them because they were not `.py` files; `mypy` could
  not see them because `files = ["harness"]`; nothing syntax-checked them until the block ran, at
  which point a typo printed a traceback that the `if` read as a failed assertion — indistinguishable
  from a real regression. Extracting the blocks and running the repo's **own** ruff config over them
  found 39 errors, including `E401`, `E402` and four `I001`. The project had spent an entire
  decisions entry (D-2026-09-18) on wiring up ruff and mypy, and half the suite was outside both.
- **Check:** Test code is code. It lives in `.py` files, it is linted, and it is type-checked.
  `mypy.files` includes `tests`.
- **Where:** `tests/test_*.py`, `pyproject.toml` (`files = ["harness", "tests"]`).
- **ENFORCED BY:** `tests/test_static.py` — `test_ruff` and `test_mypy` now cover `tests/` as well
  as `harness/`, and `test_the_suite_has_no_python_hidden_in_shell_heredocs` fails if a `<<'PY`
  block reappears under `tests/`. The port itself was the proof: turning the heredocs into modules
  immediately surfaced two live defects (the exit-status hole above, and `grep -q "PASS. x"`
  matching `[PASS] x` because `.` is a regex wildcard) that the bash form had hidden.
