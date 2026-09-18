# Harness backlog — ranked by what it blocks

> Extracted from `docs/strategy/spec.md` Parts III–IV on 2026-09-18, unchanged in substance.
> The spec says what the channel is; this file says what stops it shipping.
>
> Every defect is ranked by **which video it stops**, not by engineering severity. `H` numbers
> are stable; reorder the work, not the labels. `C` numbers are capabilities the slate needs.
>
> **H1–H18 were implemented and merged 2026-09-18** (PR #1). Parts III–IV below are kept as the
> record of what was found and why each fix exists — not as a live to-do list. What is still
> open is in Parts V and VI, and in the spec's status note.
>
> The evidence behind every ranking is `docs/strategy/spec.md` Part II (the 2026-09-18 audit of
> `renders/ad02/generated-wan/`). The reach argument that reordered the slate is
> `docs/strategy/reach-audit-2026-09-18.md`.

---

# Part III — The harness, ranked by what it blocks

**All of H1–H18 below are implemented and merged (2026-09-18, PR #1).** Kept as written — as
findings, not a checklist with boxes ticked — because the evidence and reasoning behind each fix
is the part worth keeping; the fix itself is in the code and in `git log`. `LESSONS.md` carries the
per-entry `ENFORCED BY:` line for what's actually wired in today.

Every defect below is ranked by **which video it stops**, not by engineering severity. `H` numbers
are stable; reorder the work, not the labels.

## 9. Blocking every video

### H1 — `check_clip` does not run on the path in use

See §7. **Blocks:** everything. A black payoff shot shipped and the check that catches it was never
called.
**Fix.** Call `check.check_clip` in the `collect()` loop; promote crushed-to-black to a hard failure.
**Check.** `tests/run.sh` asserts a synthesised black mp4 is rejected by the generate path, not
merely by the function.

### H2 — Delivered duration is never compared to declared duration

Covers §8.1, §8.2, §8.3 — one defect wearing three hats. **Blocks:** every video, because it puts the
narration on the wrong picture, and narration is the product.
**Fix.** After `collect()`, ffprobe the returned clip and compare to `shot["seconds"]`; a mismatch
beyond ~0.2 s fails with the delta named. Write **measured** seconds into `generate.json` and compute
cost from that. Build caption cues from measured clip durations whenever generated clips exist.
`cmd_deliver` already does exactly this on the Blender path and aborts at 0.75 s — the pattern is in
the repo and was not carried across.
**Check.** A fixture clip whose duration disagrees with its spec shot fails the run.

### H3 — `frame_count()` clamps silently instead of refusing

```
4.0s -> 64 frames = 4.00s output
6.0s -> 81 frames = 5.06s output   <- ad01, all three shots
9.0s -> 81 frames = 5.06s output   <- ep01 would lose 44%
```

`ad01`'s three 6-second shots were rendered as 81 frames; `_apply_tracks` maps the whole normalised
track onto them, so the shot is not truncated — **it plays 18% fast.** `renders/ad01/passes.json`
holds `"seconds": 6.0` and `"frames_total": 81` on the same object. **Blocks:** any video with a shot
longer than a backend window, which at 10–18 min is all of them.
**Fix.** Refuse. A shot past the window is an authoring decision, not something to resolve silently.
**Check.** `frame_count(9.0)` on the wan profile raises.

### H4 — The pipeline stops one step before the deliverable

Nothing assembles `generated-*/*.mp4`. `assemble()` globs `*/frame_*.png`, which does not match the
`*/plate/c00/frame_*.png` that `passes` writes. The ad02 cut, its `concat.txt` and its burned captions
were made **by hand** and left in the output directory — and `cmd_sheet` now carries a hardcoded
skip-list for those files. The tool is working around artefacts it does not manage.
**Blocks:** the 2–3 week cadence. A manual last mile does not survive 26 videos a year.
**Fix.** `deliver --backend <name>`: concatenate generated clips, time captions off their measured
durations (H2), write `deliver.json`.

## 10. Blocking the moat

### H5 — `factgate` and `licencegate` are wired to nothing

Neither is called by `render`, `generate` or `deliver`; only `tests/run.sh` invokes them. Worse:
**`ad01` and `ad02` have no fact ledger at all** — the cuts making factual claims and costing money.
The gate guards `ep01`, which is not shipping.

§2.5 stakes the channel's differentiation on a **public** ledger per video. That makes this not a
hygiene issue but the moat:

**Blocks:** the fact-as-trust device, i.e. the wedge in §1.
**Fix.** Call `factgate` from `deliver`, blocking on `--publish`. Write a ledger for every shipped
cut. Add the per-video public ledger page as a deliverable artifact.
**Check.** `deliver --publish` on a spec with no ledger fails.

### H6 — The two gate tests are inverted

`tests/run.sh` asserts the real ep01 ledger **fails** and the real licence register **blocks**. Both
pass today and both go red the day someone finishes the work they guard. A test that breaks on
success trains you to ignore the suite.
**Fix.** Assert against fixtures; report real-ledger status without failing the run.

### H7 — `[shot.mechanism]` is a tautology

It checks `turns × pitch ≈ advance` against three numbers hand-written in the same block. Nothing
compares them to the tracks. `ad02` c04 declares `turns = 6.0` while separately writing `2160.0`
degrees in a spin track and `-0.20` in an unlinked offset track; change the spin and forget the block
and it still passes. `ad02` **c05 advances the cell −0.26 m with no spin track and no mechanism block
at all** — the exact fault the feature exists to catch, one shot later, unflagged.
**Blocks:** "nothing guessed." A mechanism that cannot exist is the worst thing this channel can ship.
**Fix.** Derive `turns` from the spin track's total degrees and `advance` from the offset delta, then
assert against `pitch`.
**Check.** c05 as written fails validation.

### H8 — Nothing records which backend a spec decision reaches

§8.6. Material work aimed at a path that cannot see it, recorded as a fix.
**Fix.** `LESSONS.md` entries name the backend they were verified on. Spec comments that justify a
value against model behaviour name the backend. `backends` output states plainly what each path
ignores.

## 11. Blocking the slate's capabilities

### H9 — Chunking is wrong wherever it is reachable

`offset` is incremented and never read; every chunk calls `_apply_tracks(..., count)` with its own
frame count, so **each chunk renders the entire shot's animation**, compressed — two chunks
concatenated give the shot twice. `edge`/`vis` derive only from `c00`, so a multi-chunk Cosmos shot
fails `bundle.require()` regardless. On `wan`, `max_frames == chunk_frames == 81`, so the path is
unreachable.
**Blocks:** long-form. A 10–18 minute video is nothing but long shots.
**Fix.** Delete `chunk_frames`, `offset`, the chunk tag machinery and the c00-only derive. Re-add
when a backend forces it, at which point the track re-timing must be written properly anyway.
**Check.** Deleting it must not change `renders/ad02/passes.json`.

### H10 — The `_control` mux cache has no invalidation

`build_bundles` does `if not dst.exists(): _mux(...)`. Nothing clears `_control` and `--force` does
not touch it. Fix a `depth_range`, re-run `passes`, run `generate --force`, and you **pay to generate
from the previous control video.**
**Fix.** Name the cached mp4 by a hash of its source frames, or drop a shot's `_control` when
`passes` rewrites it.

### H11 — Tracks are under-scoped and nothing detects collisions

`ad02` has 9 tracks; 2 carry `shots`. An unscoped track applies in **every** shot where any of its
parts is visible, so two unscoped `spin` tracks on the same screws (1440° and 2160°) both key the
same objects at overlapping times and the last `keyframe_insert` wins per frame.
**Fix.** Assert at validation: no two tracks may drive the same (part, channel) in the same shot.

### H12 — `library.py` duplicates the spec vocabulary and has drifted

280 lines mirroring `spec.GENERATOR_PARAMS` with no assertion they agree — while `build.py` performs
exactly that assertion for spec↔generators at import. Measured today: **`screw.bar` exists in the
spec and is missing from the catalogue.** One day old.
**Fix.** Generate the catalogue from `GENERATOR_PARAMS`, or add the same import-time assert.

### H13 — Two `BuildError` classes

`generators.BuildError` and `build.BuildError` are distinct. A bad `crew` pose raises the former;
`cmd_build` catches the latter, so the user gets a traceback instead of "build FAILED." The hygiene
test catches shadowing within a file, not across files.
**Fix.** One `BuildError`. Extend the hygiene test to flag a class defined in more than one
`harness/*.py`.

### H14 — Smaller, verified

| | |
|---|---|
| `__main__.py:362` | `_cost()` returns `0.0`, never called |
| `__main__.py:351` | `secs = round(b.videos and 0 or 0, 2)` — assigned, never used |
| `__main__.py:556,560` | `"...mod(n\,{n})..."` raises `SyntaxWarning` every test run; use a raw string |
| `__main__.py:534` | `cmd_sheet` hardcodes `startswith("shield") or endswith("nocaps")` to skip hand-made files in its own output dir — see H4 |
| `passes.py:594` | `_swap_material` appends a slot to meshes that had none; `_restore_material` zips over `[]` and never removes it |
| `passes.py:493` | `_depth_range(ep, shot, built)` takes `built`, never uses it |
| `passes.py` docstring | states "**Passes render with Workbench, not Cycles**" as rule 2; depth renders with Cycles at line 904. Only `seg` uses Workbench |

## 12. Structural

### H15 — The generative interface is unversioned

1,543 uncommitted insertions across 13 modified files, plus five untracked modules: `backend.py`,
`check.py`, `library.py`, `passes.py`, `doctor.py`. The project whose central claim is "measurably
better every time" cannot bisect, roll back, or golden-diff any of it.
**Fix.** Commit before the next change.

### H16 — Declared structure that does not exist

`README.md`'s Layout presents as real: `goldens/` (empty — "canary renders for regression"), `mvp/`
(empty), `eval/` (a README only), `qa/` (one rubric of six levels). A canary that does not exist
cannot die. `eval/audience.md` (§6) does not exist either and is needed before the first upload.
**Fix.** Populate or delete.

### H17 — The prose-to-mechanism ratio is inverted

**11,310 lines of markdown against 3,610 lines of code.** `LESSONS.md` holds 40 entries written in
two days, several restating one another. The prose is good, which is the trap: it reads like the work
is done.

**Four of the defects audited above are already in `LESSONS.md` as principles and shipped anyway** —
H1 (a check that did not fire), H7 (arithmetic where nothing can check it), §8.6 (a fix verified on
the wrong path), §8.7 (the mid-shot glowing slab, recorded as fixed).

The metric is not lessons written. It is **lessons that became an assertion.**
**Fix.** Every `LESSONS.md` entry gains one line: the check that enforces it, or
`ENFORCED BY: nothing — prose only`. Count the second kind and drive it down.

### H18 — The test suite mostly tests argparse

Of ~25 assertions, 12 are `--help` exit codes. Nothing exercises `PassProfile.chunks`,
`_depth_range`, `check_motion`, `check_depth_pass`, `get_backend` or `build_bundles` — all pure, all
runnable without Blender, all exactly where the defects above live. `verify`, `sheet` and `library`
are uncovered.
**Fix.** Drop `--help` to one smoke test; add unit assertions for the pure functions, starting with
H3, H9, H10.

## 13. What `check.py` cannot currently see

Named so they are not mistaken for gaps nobody noticed. Candidates, not demands.

| Fault | Evidence | Status |
|---|---|---|
| Delivered ≠ declared duration | §8.1 | H2 |
| Billed ≠ estimated seconds | §8.2 | H2 |
| Caption timeline ≠ picture timeline | §8.3 | H2 |
| A whole shot below `BLACK_MEAN` | §8.4 | check exists, unwired (H1) |
| Shot-to-shot luminance discontinuity | §8.4 | **no check** |
| Generated motion ≪ control motion | §8.5 | **no check** |
| A control pass that is valid but uninformative | §8.7 | **no check, and the hard one** |
| Palette continuity across a cut | §8.7 | **no check** |

The last two matter most and must not be faked. A large constant-depth region is measurable — WARN
when one connected near-constant-depth region exceeds a fraction of frame, pointing at a contact
sheet. Palette continuity is measurable as mean hue/luminance distance between adjacent shots.
Neither becomes a hard gate on a first pass; the repo's own rule about checks that cry wolf applies.

---

# Part IV — Order of work

**Done, 2026-09-18 (H1–H18; kept as the record of the order actually followed).** What's left is
the capability roadmap (C1–C6, below) and the content work named in the Status line at the top of
this document — neither is "next up" in this list, both are separate, larger efforts.

**Ranked by what unblocks the slate, not by engineering interest.**

### Now — stop shipping broken video (days)

1. **H1** — wire `check_clip` into `collect()`. One call site. A black shot shipped.
2. **H3** — refuse instead of clamp. One `if`. The live money defect.
3. **H2** — measure delivered duration; fix cost accounting and caption timing from it.
4. **H15** — commit.

### Next — make the cadence possible (weeks)

5. **H4** — `deliver --backend`, so the last mile stops being manual. Without this there is no
   two-week cadence.
6. **C4** — dual aspect from the spec. The Shorts funnel is the growth engine and must not be a
   second production.
7. **H9, H10** — delete the chunking, invalidate the control cache.

### Then — protect the moat (weeks)

8. **H5** — wire the gates; write ledgers for anything shipped; stand up the public ledger page.
9. **H7, H11** — make the mechanism check real; detect track collisions.
10. **H6, H8** — de-invert the gate tests; record which backend a decision reaches.

### Then — build what Episode 1 is made of (months)

11. **C1** Mode C, **C2** terrain input, **C3** diagrammatic water flow. This is the largest build in
    the plan and the Snowy flagship cannot exist without it.
12. **C5** thumbnail render, **C6** "as of" facts.
13. **H12, H13, H14** — the small true things.
14. **H16, H17, H18** — `eval/audience.md` before the first upload; `ENFORCED BY:` lines; unit tests
    for the pure functions.

### Not in scope, deliberately

`seg` and `edge` are rendered and unused because VACE takes neither. §8.7 is a real ceiling, and the
answer is a backend that accepts more than one control pass — **not** more passes rendered into a
drawer. Until such a backend exists, `local` ships and generative supplies atmosphere only.

---


---

# Part V — Capabilities, re-ranked against the 2026-09-18 slate

**Supersedes the C-table in `docs/strategy/spec.md` §5.** That table was ranked against a Snowy
flagship opening the channel. The slate now opens on eight Shorts and three mechanism long-forms
(`docs/strategy/slate.md`), which changes which capability is first and which are a year out.

| # | Capability | Needed by | Was | Now |
|---|---|---|---|---|
| **C1** | **Mode C — diagram/data**: dimension callout, leader line, annotated arrow | **S3** (the moment-arm reveal) | 1st | **1st**, and much smaller |
| **C4** | **Dual aspect from the spec** — 9:16 and 16:9 from one spec | **L1**, not S1 | 2nd | 2nd |
| C5 | Thumbnail render from the same scene | L1 | 5th | 3rd |
| C2 | Geospatial terrain input — DEM heightfield | Phase 3 | 2nd | deferred |
| C3 | Diagrammatic water flow | Phase 3 | 3rd | deferred |
| C6 | "As of" facts in the fact gate | Phase 3 | 4th | deferred |

**C4 is NOT needed by S1 — corrected 2026-09-18.** An earlier version of this table said "needed
by S1, i.e. immediately". That was wrong: every Phase 0 Short is 1080×1920, which is already the
default and already renders. C4 is about getting 16:9 *as well*, from the same spec, and the first
video that needs it is **L1**. Acting on the old line meant building a capability before the video
that needs it — the exact inversion this file exists to prevent.

**C1 shrank.** Against a Snowy flagship, Mode C meant terrain maps and cross-sections — a large
build. Against S3 it means one animated dimension callout with a leader line. Build that much, and
let the slate pull the rest.

**C2 and C3 left the critical path entirely.** They existed to serve a flagship that is now Phase 3.
Nothing before then needs a heightfield or a water sheet.

---

# Part VI — New items, 2026-09-18

### H19 — Render throughput at delivery resolution was extrapolated, not measured

`render-bench.json`'s `extrapolation` block scaled a 384×682 measurement by pixel count and sample
count to claim 62.4 s/frame at 1080×1920 @ 32 spp. It is the number under every schedule claim in
the repo, and it had never been checked against a render at that resolution.

**Fixed 2026-09-18.** `render()` now records the per-shot elapsed time it was already measuring and
printing — `render_seconds` and `sec_per_frame` land in `render.json`. `harness bench` renders a
capped number of frames at a real delivery resolution and appends a measured row.

```bash
python -m harness bench spec/ad01/ad01.toml --shots a01 \
    --res 1080x1920 --samples 8 --device CPU --frames 24
```

**Check.** `tests/run.sh` asserts a one-frame benchmark is **refused** and writes no row —
`MIN_BENCH_FRAMES = 8`. The timer starts after `build_scene`, so build cost is excluded by
construction; the floor exists for sampler warm-up and BVH build, which the first frame still pays.

**Measured 2026-09-18:** `spec/ad01/ad01.toml` a01, 24 frames, 1080×1920 @ 8 spp, M1 CPU Cycles —
**26.86 s/frame**. The extrapolation claimed 62.4 s/frame at 32 spp; scaled to 8 spp that is 15.6,
so the real cost is **1.7× the extrapolation**, not 0.25× as the first (contended) run suggested.

> **A second trap, found the same day.** The first run of this benchmark measured 31.98 s/frame for
> identical work, because doc edits were running on the same 8 cores. A ~19% spread between two
> runs of one workload. **Nothing else may run during a benchmark**, and a single bench row is a
> measurement with an error bar, not a constant. Same family as the existing
> "short benchmark runs lie" finding.

> **And a third.** The first row recorded `"device": "OPTIX"` while the render actually ran on
> CPU: `render()` applies `--device` to its own copy of the episode, so `cmd_bench` read the
> spec's value afterwards and recorded a measurement against hardware that never ran it. `render()`
> now returns the device, resolution and samples it used, and `cmd_bench` reads them from there.
> A benchmark that cannot say which machine produced it is not evidence.

**Open:** the OptiX row for the render node is still `not_measured`. Per
`docs/strategy/slate.md`, that number is not needed until Phase 1.

### H20 — `render` writes every frame before `assemble` reads any

12 GiB free on the authoring Mac. At ~2.3 MB per 1080×1920 PNG (measured, `ad01/a01`):

| | frames | disk |
|---|---|---|
| 30 s Short | 900 | ~2.1 GB — fits (6.7 h render) |
| 7 min long-form | 12,600 | **~29 GB — does not fit** (94 h render) |

Long-form fails on disk before it fails on patience, and it fails silently and late — after hours
of render. **Blocks:** Phase 1, on this machine.
**Fix.** Assemble per shot and drop the frames, or write to a scratch volume declared in the spec.
**Check.** Refuse a render whose projected frame bytes exceed free space, naming both numbers.
Not needed until Phase 1 — recorded now so it is not rediscovered at 3 a.m. on frame 9,000.

### H21 — A hero cylinder could not be made to look like one

Found by building S1's cylinder from primitives and **looking at the frame** before writing the
spec — the repo's own "score renders, not code" rule, applied to a capability question.

**Two faults, both one line, both fixed 2026-09-18.**

`_cyl()` has always taken a `segments` argument, and `GENERATOR_PARAMS["cylinder"]` was
`{"radius", "depth"}` — so no spec could ever set it and every cylinder in the repo was 24-sided
whatever it was for. Fine for a screw shaft at 30 m; visibly faceted on a chrome barrel filling a
1080×1920 frame. **A parameter the spec cannot set is not a parameter.**

There was also **no mesh smooth shading anywhere in the harness.** `render._smooth()` is f-curve
easing ("Ease in AND out"), not `shade_smooth`, and nothing else touched mesh shading. Correct for
the shield — boxes and bricks *should* be flat — and wrong for a turned steel surface.

**Fix.** `segments` added to the cylinder's params. `smooth` added to `PART_KEYS` as an **angle in
degrees**, not a flag: shading every polygon smooth turns a cylinder's end cap into a dome, and the
end caps are exactly what Beat 3 of S1 is showing. Applied per part, opt-in, so no existing `ep01`
or `ad01` frame changes. `bpy.ops.object.shade_smooth_by_angle` is the supported path in Blender 5.x
(`MeshPolygon.use_smooth` was removed in 4.x and `Mesh.shade_auto_smooth` does not exist), and it
needs a selection, so `_shade_smooth` saves and restores it — a build that leaks selection makes the
next part's operator do something else, which is an order-dependent bug that will not reproduce.

**Checks.** `tests/run.sh`: `smooth = true` is refused with "expected an angle in DEGREES"
(`tests/fixtures/smooth_not_an_angle.toml`), and an 8-segment and a 64-segment cylinder must not
have the same polygon count (`tests/fixtures/cylinder_segments.toml`).

### H22 — `check_storyboard` cannot see "unreadable"

The first S1 probe rendered three disconnected objects floating in near-darkness — `rot` had been
written in radians against a schema that takes degrees, and the spec declared no lights. The frame
was meaningless. `check_storyboard` passed it: *"1 frame(s), all carry a picture."*

The check is not wrong. It answers "is this frame black, flat, or 92% dark", and the answer was no.
It does not answer "does this frame show the thing the shot exists to show" — the same shape as
§8.7, where every depth pass was a valid depth map and none carried the subject.

**Blocks:** nothing today. The stills pass exists to be looked at by a human, and it was.
**Candidate check:** a frame whose subject pixels occupy less than some fraction of frame, or whose
parts project to disjoint clusters, is a WARN pointing at a contact sheet — never a hard gate. The
repo's own rule about checks that cry wolf applies, and this one would.
**Recorded so it is not mistaken for a gap nobody noticed.**

### H23 — For a Markdown script, the ledger hash covers the stage directions too

`factgate.narration_text()` extracts `^narration = "..."` lines from a **TOML** spec — "the spec is
the approved script, so the hash tracks the words". For any other suffix it returns
`path.read_text()`: **the entire file.**

`spec/s01/facts/s01.facts.json` sets `narration_source` to
`docs/videos/s01-hydraulic-cylinder/script.md`, which is the right place for a script to live. The
consequence is that `script_hash_matches_ledger` fails on **any** edit to that file — a reworded
stage direction, a corrected caption-policy note, a typo in an open question. Observed 2026-09-18:
editing Beat 3's *Picture* block and the caption policy, touching no narration line, invalidated the
ledger.

The gate is then wrong in the direction that matters most. A ledger revision should mean "the words
changed, re-approve the facts". Here it means "the file changed", so it fires on edits that cannot
possibly affect a factual claim — and a gate that cries wolf is one people learn to re-stamp without
reading. That is H6's lesson arriving from the other side.

**Blocks:** nothing yet, but it will make the per-video public ledger (§2.5, the wedge) annoying
enough to route around, which is the failure mode that matters.
**Fix.** Extract the quoted narration from Markdown the same way TOML extracts it — the `> "..."`
lines, in order — so the hash tracks the words in both formats. Three lines in `narration_text`.
**Check.** Editing a non-narration line of a fixture script must NOT change the hash; editing a
quoted line must.
