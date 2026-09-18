> **SUPERSEDED 2026-09-18 — rolled into [docs/spec.md](spec.md). Do not edit; edit spec.md.**

# Harness Remediation Spec — 2026-09-18

**Status:** proposed, not started
**Scope:** `harness/`, `tests/run.sh`, `spec/ad02`, and the claims in `README.md`
**Trigger:** an audit of `renders/ad02/generated-wan/shield-cycle-480p-captioned.mp4`,
the most recent paid generation, plus a full read of the harness.

This is an engineering spec, not an episode spec. It lives in `docs/` because it
describes work on the compiler, not a scene for the compiler to build.

---

## 0. The finding that frames the rest

The harness has a check that catches a crushed-to-black clip. The check is correct.
The most recent delivered video **fails it**, and the check never ran:

```
$ python -c "from harness import check; ..."
  c05_c00.mp4                          FAIL: mean luminance 10.1 - the clip is crushed to black
  cycle-nocaps.mp4                     FAIL: mean luminance 10.1 - the clip is crushed to black
  shield-cycle-480p-captioned.mp4      FAIL: mean luminance 10.1 - the clip is crushed to black
```

`check_clip` is called in the sequential branch of `cmd_generate`
([harness/__main__.py:430](../harness/__main__.py)) and **not** in the
`submit`/`collect` concurrent branch — which is the branch taken whenever
`len(todo) > 1`, i.e. every real run since the cold-start fix landed.

The defect class this repo was founded to eliminate is "the failure was silent."
The repo has now produced a new instance of it: **the failure was not silent, it
was unlistened-to.** Every item below is ordered by that principle — a defect is
not fixed until a check fires on it.

---

## 1. Audit: `shield-cycle-480p-captioned.mp4`

Measured 2026-09-18 from the delivered file, not from the logs.

### 1.1 The cut is 26.6% longer than the spec, and nothing compared the two numbers

| | Spec | Delivered |
|---|---|---|
| Shot length | 4.00 s × 5 | 5.0625 s × 5 |
| Total | **20.00 s** | **25.31 s** |
| Frames per shot | 64 sent as control | 81 returned |

`renders/ad02/passes.json` records `"seconds": 4.0` and `"frames_total": 64`.
The returned clips are 81 frames. Wan VACE generates its own frame count and does
not honour the control video's length; the harness sends 64 frames of depth and
receives 81 frames of video, the last 17 of which are **unconditioned** — free
model output with no geometry behind it.

Nobody noticed because no code path compares the spec's declared duration to the
delivered duration.

### 1.2 The cost record in `generate.json` is wrong by the same 26.6%

```json
"video_seconds": 20.0,
"estimated_usd": 0.8,
```

fal bills per second of **output**. Output was 25.31 s. True spend ≈ **$1.01**.
`_bundle_seconds()` probes the *control* video's duration
([harness/__main__.py:368](../harness/__main__.py)) — the input, not the product.
The estimate is systematically low by whatever the model decides to add, and it is
written into the manifest as though it were measured.

### 1.3 The captions are on the wrong shots

Captions were built from the spec's 4.0 s/shot timeline and burned onto a
5.0625 s/shot video:

```
  c01: spec   0.00-  4.00s   actual   0.00-  5.06s   drift at end +1.06s
  c02: spec   4.00-  8.00s   actual   5.06- 10.12s   drift at end +2.12s
  c03: spec   8.00- 12.00s   actual  10.12- 15.19s   drift at end +3.19s
  c04: spec  12.00- 16.00s   actual  15.19- 20.25s   drift at end +4.25s
  c05: spec  16.00- 20.00s   actual  20.25- 25.31s   drift at end +5.31s
```

Consequences in the shipped file:

- "Turning them drives the cell forward" (cue 7, 12.35 s) plays over **c03, the
  digging shot**.
- "They push against the brick behind / The tunnel is lined as it goes"
  (cues 9–10, 16.35–19.49 s) play over **c04**, and are gone before c05 — the shot
  they describe — begins at 20.25 s.
- The final **5.06 seconds have no captions at all.**

The narration is the product. It is currently describing the wrong pictures.

### 1.4 The payoff shot is black, end to end

Luminance sampled across each clip (mean of 64×64 grey, `BLACK_MEAN` = 12.0):

| shot | t=0.0 | t=1.25 | t=2.5 | t=3.75 | t=4.9 |
|---|---|---|---|---|---|
| c01 | 23.7 | 23.8 | 23.7 | 24.3 | 24.9 |
| c02 | 40.0 | 39.4 | 34.1 | 32.5 | 34.5 |
| c03 | 22.5 | 24.5 | 26.6 | 26.7 | 26.8 |
| c04 | 41.9 | 42.7 | 48.3 | 44.7 | 45.6 |
| **c05** | **10.8** | **11.4** | **11.1** | **9.9** | **10.1** |

c05 is not a fade — it is uniformly below threshold for its whole duration. It is
"The Advance", the shot the entire cut builds to, and it is the last thing on
screen. The video ends on five seconds of near-black.

Secondary: adjacent shots swing 4× in mean luminance (c04 at 45.6 → c05 at 10.8).
No check measures shot-to-shot consistency, so a cut can pass every per-shot check
and still flicker at every edit point.

### 1.5 The advance did not survive the generation

Motion energy, control depth pass vs delivered clip (summed adjacent-frame
difference over 12 samples):

| shot | control | generated | |
|---|---|---|---|
| c01 | 42.5 | 34.4 | ok |
| c02 | 71.7 | 39.1 | **generated moves 45% less** |
| c03 | 34.6 | 57.6 | generated invents motion |
| c04 | 63.4 | 86.0 | generated invents motion |
| c05 | 31.3 | 14.9 | **generated moves 52% less** |

In c05 the depth control clearly shows the cell travelling. The delivered clip
shows half that movement. The one mechanical fact the shot exists to communicate
is the thing the model attenuated.

Where generated motion *exceeds* control (c03, c04) it is not the animation — it is
grade pumping and an artefact appearing mid-shot (see 1.7).

### 1.6 Every material decision in `spec/ad02` is unreachable on this backend

`ad02.toml` carries extensive, well-reasoned, documented material work: four
separated hues, iron roughness raised 0.42 → 0.62 to kill a specular bloom, crew
moved from `timber` to a dark `cloth` because "a pale wooden figure standing in a
dark tunnel is the one thing the model lit into a glowing capsule", `timber`
darkened to 0.20 because "the model lit it into a glowing slab that appeared
mid-shot."

`WanVaceBackend.requires = ("depth",)`. **The model never receives a colour.**
Base colour, roughness and metallic cannot influence a depth-conditioned
generation. Those fixes were aimed at a channel that is not connected, they are
recorded in `LESSONS.md` as though they worked, and the artefacts they targeted
are still in the delivered file.

This is not an argument for deleting the material work — it is correct and
necessary for `local`, which is still the honest default. It is an argument that
**the spec must say which backend a given decision reaches**, and that `LESSONS.md`
entries must name the path they were verified on.

### 1.7 The output is not period-accurate, and the palette has no continuity

From contact sheets of all five delivered clips:

- **c01** — iron renders as saturated cobalt **blue**, brick as bright terracotta.
  The screw is a modern hex-head machine bolt. The caption over this frame reads
  "The shield is a wall of thirty-six iron cells."
- **c03** — teal-and-orange grade. The miner is a featureless orange mannequin
  holding a bright plank; **there is no clay in frame at all**, while the narration
  says "He cuts the clay away in front of his cell."
- **c04** — monochrome sodium orange. The screws read well — the best geometry in
  the cut. A **bright cream rectangle appears in frames 3–4 and is gone by frame 5**:
  the same "glowing slab that appears mid-shot" artefact recorded as fixed.
- **c05** — near-black, dim orange brick, cell barely legible.

Five shots, four incompatible colour grades: blue, teal/orange, sodium orange,
near-black. There is no continuity, and nothing in the harness asks for any.

### 1.8 Root cause of 1.7: depth alone is a silhouette

Comparing `depth_c04` to `gen_c04` is the clearest evidence in the audit. In the
depth pass the cell is a **featureless white slab** filling the left 40% of frame —
correct, because the depth of a flat plate facing camera is constant. The model
receives no interior structure, and renders that region as a dark void in c04 and
as a blue box in c01.

Every control pass in this cut passes the harness's own depth check:

```
  c01  depth mean  128.7   clean
  c02  depth mean  120.2   clean
  c03  depth mean  113.2   clean
  c04  depth mean  127.3   clean
  c05  depth mean  155.6   clean
```

So `check_depth_pass` answers "is this a valid depth map?" — and it answers
correctly. It does not answer "does this carry enough information for a model to
render the subject", which is the question that decided this video. A large flat
region at constant depth is a perfectly valid depth map and a near-useless control
signal.

**The single-control-pass architecture has a measurable ceiling and this cut is at
it.** `README.md` presents depth-as-the-shared-pass as pure upside. The cost —
that on `wan` you hand the model a silhouette and hope — is not stated anywhere.

---

## 2. Defects in the harness

Ordered by cost. Each carries the acceptance check that closes it.

### D1 — `frame_count()` silently clamps instead of refusing

`PassProfile.frame_count()` applies `max_frames` before `chunks()` ever runs
([harness/passes.py:409](../harness/passes.py)):

```
spec says 4.0s -> 64 frames @ 16fps = 4.00s output
spec says 6.0s -> 81 frames @ 16fps = 5.06s output   <- ad01, all three shots
spec says 9.0s -> 81 frames @ 16fps = 5.06s output   <- ep01 would lose 44%
```

`ad01`'s three 6-second shots were rendered as 81 frames each. `_apply_tracks`
then maps the whole normalised 0→1 track onto those 81 frames, so the shot is not
truncated — **it plays 18% fast**, and its captions drift.

`renders/ad01/passes.json` holds `"seconds": 6.0` and `"frames_total": 81` on the
same object.

**Fix.** Refuse. A shot longer than the backend's window is an authoring decision
(shorten the shot, or chunk it), not something to resolve silently.

**Check.** `PassProfile.frame_count(9.0)` on the wan profile raises rather than
returning 81.

### D2 — Delivered duration is never compared to declared duration

Covers 1.1, 1.2 and 1.3, which are one defect wearing three hats.

**Fix.** After `collect()`, ffprobe the returned clip. Compare to
`shot["seconds"]`. Mismatch beyond ~0.2 s is a hard failure with the delta named.
Write the **measured** output seconds into `generate.json`, and compute
`estimated_usd` from that number. Build caption cues from measured clip durations
when generated clips exist, not from `shot["seconds"]`.

`cmd_deliver` already does exactly this check on the Blender path
([harness/__main__.py:209](../harness/__main__.py)) and aborts on a 0.75 s
discrepancy. The generative path needs the same guard. The pattern is already in
the repo; it was not carried across.

**Check.** A fixture clip whose duration disagrees with its spec shot fails the
run.

### D3 — `check_clip` does not run on the concurrent path

See §0. The check exists and is correct.

**Fix.** Call `check.check_clip` in the `collect()` loop. Promote crushed-to-black
from a `WARN` to a hard failure — a black payoff shot shipped.

**Check.** `tests/run.sh` asserts a synthesised black mp4 is rejected by the
generate path, not merely by the function.

### D4 — Chunking is wrong wherever it is reachable

`offset` is incremented and never read ([harness/passes.py:781](../harness/passes.py)).
Every chunk calls `_apply_tracks(..., count)` and `_apply_camera_move(..., count)`
with its own frame count, so **each chunk renders the entire shot's animation**,
compressed. Two chunks concatenated give you the shot twice.

`edge` and `vis` derive only from `c00` ([harness/passes.py:826](../harness/passes.py)),
so a multi-chunk Cosmos shot fails `bundle.require()` on chunk 1 regardless.

On `wan`, `max_frames == chunk_frames == 81`, so `chunks()` can never return more
than one chunk and the whole path is unreachable.

**Fix.** Delete `chunk_frames`, `offset`, the chunk tag machinery and the
c00-only derive. It is unreachable on the backend you run and wrong on the one you
do not. Re-add it when a real backend forces a shot past its window, at which
point the track re-timing has to be written properly anyway.

**Check.** Deleting it must not change `renders/ad02/passes.json`.

### D5 — The `_control` mux cache has no invalidation

`build_bundles` does `if not dst.exists(): _mux(...)`
([harness/backend.py](../harness/backend.py)). Nothing clears `_control`, and
`generate --force` does not touch it. Fix a `depth_range`, re-run `passes`, run
`generate --force` — and you pay to generate from the **previous** control video.

For a repo whose depth check exists because "a bad control pass is a bad
generation, and the generation costs money", caching by existence is the wrong
primitive.

**Fix.** Name the cached mp4 by a hash of its source frames, or delete a shot's
`_control` entry whenever `passes` rewrites that shot.

**Check.** Re-running `passes` with a changed `depth_range` produces a different
`_control` path.

### D6 — Two `BuildError` classes

`generators.BuildError` and `build.BuildError` are distinct
([harness/generators.py:37](../harness/generators.py),
[harness/build.py:41](../harness/build.py)). A bad `crew` pose raises the former;
`cmd_build` catches the latter. The user gets a traceback instead of
"build FAILED".

The hygiene test in `tests/run.sh` catches shadowing *within* a file. This is
across files.

**Fix.** One `BuildError`, defined once, imported by both.

**Check.** Extend the hygiene test to flag a class name defined in more than one
`harness/*.py`.

### D7 — Smaller, verified

| | |
|---|---|
| [harness/__main__.py:362](../harness/__main__.py) | `_cost()` returns `0.0` and is never called |
| [harness/__main__.py:351](../harness/__main__.py) | `secs = round(b.videos and 0 or 0, 2)` — assigned, never used |
| [harness/__main__.py:556,560](../harness/__main__.py) | `"...mod(n\,{n})..."` raises `SyntaxWarning` on every test run; use a raw string |
| [harness/__main__.py:534](../harness/__main__.py) | `cmd_sheet` hardcodes `startswith("shield") or endswith("nocaps")` to skip hand-made files in its own output dir — see D9 |
| [harness/passes.py:594](../harness/passes.py) | `_swap_material` appends a slot to meshes that had none; `_restore_material` zips over `[]` and never removes it |
| [harness/passes.py:493](../harness/passes.py) | `_depth_range(ep, shot, built)` takes `built` and never uses it |
| [harness/passes.py](../harness/passes.py) docstring | states "**Passes render with Workbench, not Cycles**" as rule 2; depth renders with Cycles at line 904. Only `seg` uses Workbench |

---

## 3. Doctrine with no mechanism behind it

The repo's thesis is that the deliverable is a ratchet. Several teeth are painted on.

### D8 — `factgate` and `licencegate` are wired to nothing

Neither is called by `render`, `generate` or `deliver`. Only `tests/run.sh` invokes
them. Principle 8 — "facts before script; script before render" — is enforced by
remembering.

Worse: `ad01` and `ad02`, the cuts actually making factual claims about the Thames
Tunnel and actually being paid for, **have no fact ledger at all**. The gate
guards `ep01`, which is not shipping.

**Fix.** Either call `factgate` from `deliver` and write a ledger for `ad02`, or
strike principle 8 from `README.md`. Both are defensible. The current state is not.

### D9 — The pipeline stops one step before the deliverable

Nothing assembles `generated-wan/*.mp4`. `assemble()` globs `*/frame_*.png`, which
does not match the `*/plate/c00/frame_*.png` that `passes` writes. The final cut,
its `concat.txt` and its burned captions were made by hand and left in the output
directory — and `cmd_sheet` now carries a hardcoded skip-list for those files
(D7). The tool is working around artefacts it does not manage.

**Fix.** A `deliver --backend wan` that concatenates the generated clips, times
captions off their measured durations (D2), and writes `deliver.json`.

### D10 — The two gate tests are inverted

`tests/run.sh:40` asserts the real ep01 ledger **fails**. `tests/run.sh:66`
asserts the real licence register **blocks**. Both pass today and both go red the
day someone finishes the work they are guarding.

**Fix.** Assert against fixtures. Keep the real ledgers out of the pass/fail path,
or report their status without failing the suite.

### D11 — `[shot.mechanism]` is a tautology

It checks `turns × pitch ≈ advance` against three numbers hand-written in the same
block. Nothing compares them to the tracks.

`ad02` c04 declares `turns = 6.0`, and separately writes `2160.0` degrees in a spin
track and `-0.20` in an unlinked `offset` track. Change the spin to `1440.0` and
forget the mechanism block, and it still passes.

`ad02` c05 advances the cell `-0.26 m` with **no spin track and no mechanism block
at all** — the exact fault the feature exists to catch, one shot later, unflagged.

**Fix.** Derive `turns` from the spin track's total degrees and `advance` from the
offset track's delta, then assert against `pitch`. That is a real invariant. The
current one validates a comment.

**Check.** c05 as written fails validation.

### D12 — Tracks are under-scoped and nothing detects the collision

`ad02` has 9 tracks; only 2 carry `shots`. An unscoped track applies in **every**
shot where any of its parts is visible. Two unscoped `spin` tracks on
`["screw_head", "screw_foot"]` (1440° and 2160°) therefore both key the same
objects in the same shots, at overlapping normalised times, and the last
`keyframe_insert` wins per frame.

**Fix.** Assert at validation time: no two tracks may drive the same
(part, channel) in the same shot.

### D13 — `library.py` duplicates the spec vocabulary and has already drifted

280 lines of hand-maintained metadata mirroring `spec.GENERATOR_PARAMS`, with no
assertion that the two agree — while `build.py` performs exactly that assertion
for spec↔generators at import time.

Measured today: **`screw.bar` exists in the spec and is missing from the
catalogue.** One day old.

**Fix.** Generate the catalogue from `GENERATOR_PARAMS`, or add the same
import-time assert.

**Check.** The assert.

### D14 — Declared structure that does not exist

`README.md`'s Layout section presents these as real: `goldens/` (empty — "canary
renders for regression", with no canary), `mvp/` (empty), `eval/` (a README only —
"the only accepted retrospective evidence"), `qa/` (one rubric of six levels).

**Fix.** Populate or delete. A canary that does not exist cannot die.

---

## 4. Process

### D15 — The generative interface is unversioned

1,543 uncommitted insertions across 13 modified files, plus five entirely
untracked modules: `backend.py`, `check.py`, `library.py`, `passes.py`,
`doctor.py`. The project whose central claim is "measurably better every time"
cannot bisect, roll back, or golden-diff any of it.

**Fix.** Commit before the next change.

### D16 — The prose-to-mechanism ratio is inverted

**11,310 lines of markdown against 3,610 lines of code.** `LESSONS.md` holds 40
entries written in two days, several of which restate one another ("a check that
has never been seen to fail is not a check" / "a rule can be present, correct, and
still not fire" / "a per-frame check cannot see a fault that lives between
frames").

The prose is good, which is the trap: it reads like the work is done. **Four of the
defects audited above are already described in `LESSONS.md` as principles, and
shipped anyway** — D3 (a check that did not fire), D11 (arithmetic in a place
nothing can check), 1.6 (a fix verified on the wrong path), 1.7 (the mid-shot
glowing slab, recorded as fixed).

The metric to track is not lessons written. It is **lessons that became an
assertion**.

**Fix.** Each `LESSONS.md` entry gains one line: the check that enforces it, or
`ENFORCED BY: nothing — prose only`. Count the second kind. Drive it down.

### D17 — The test suite mostly tests argparse

Of ~25 assertions in `tests/run.sh`, 12 are `--help` exit codes. Nothing exercises
`PassProfile.chunks`, `_depth_range`, `check_motion`, `check_depth_pass`,
`get_backend`, or `build_bundles` — all pure functions, all runnable without
Blender, all exactly where the defects in §2 live. `verify`, `sheet` and `library`
are not covered at all.

**Fix.** Drop the `--help` block to one smoke test. Add unit assertions for the
pure functions above, starting with the ones named in D1, D4 and D5.

---

## 5. What `check.py` cannot currently see

Named here so they are not mistaken for gaps nobody noticed. Each is a candidate
check, not a demand for one.

| Fault | Present in the audit | Current status |
|---|---|---|
| Delivered duration ≠ declared duration | 1.1 | D2 |
| Billed seconds ≠ estimated seconds | 1.2 | D2 |
| Caption timeline ≠ picture timeline | 1.3 | D2 |
| A whole shot below `BLACK_MEAN` | 1.4 | check exists, not wired (D3) |
| Shot-to-shot luminance discontinuity | 1.4 | **no check** |
| Generated motion ≪ control motion | 1.5 | **no check** |
| A control pass that is valid but uninformative | 1.8 | **no check, and the hard one** |
| Palette continuity across a cut | 1.7 | **no check** |

The last two are the interesting ones and should not be faked. A large
constant-depth region is measurable — flag a shot where one connected region at
near-constant depth exceeds some fraction of frame, as a WARN pointing at a
contact sheet. Palette continuity is measurable as mean hue/luminance distance
between adjacent shots. Neither should become a hard gate on a first pass; the
repo's own rule about checks that cry wolf applies.

---

## 6. Order of work

1. **D3** — wire `check_clip` into `collect()`. One call site. The black shot shipped.
2. **D1** — refuse instead of clamp. One `if`. It is the live money defect.
3. **D2** — measure delivered duration; fix cost accounting and caption timing off it.
4. **D15** — commit.
5. **D9** — `deliver --backend wan`, so the last mile stops being manual.
6. **D4** — delete the chunking.
7. **D5** — invalidate the control cache.
8. **D11, D12** — make the mechanism check real; detect track collisions.
9. **D8** — wire the gates, or strike the principle.
10. **D13, D6, D7** — the small true things.
11. **D16, D17** — the ratio work: `ENFORCED BY:` lines, and unit tests for the pure functions.

**Not in scope, and deliberately:** `seg`/`edge` are rendered and unused because
VACE takes neither. 1.8 is a real ceiling but the answer is a backend that accepts
more than one control pass, not more passes rendered into a drawer.

---

## 7. Acceptance

This spec is done when:

- `tests/run.sh` fails on today's `renders/ad02/generated-wan/` artefacts.
- `python -m harness verify spec/ad02/ad02.toml --backend wan` reports the black c05.
- A `deliver --backend wan` run produces a captioned cut whose caption timeline
  matches its picture timeline, measured from the file.
- `LESSONS.md` states, per entry, what enforces it.
