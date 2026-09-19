# Harness backlog — what is open

> **This file is what is still broken.** It is not a record of what was fixed: that is in
> `git log`, in the `ENFORCED BY:` line of each `LESSONS.md` entry, and in the tests that now
> assert it. A backlog that is mostly archive is a backlog nobody reads to decide what to do next.
>
> Every defect is ranked by **which video it stops**, not by engineering severity. `H` numbers are
> stable; reorder the work, not the labels. `C` numbers are capabilities the slate needs.

## Closed

**H1–H18** were found by the 2026-09-18 audit of `renders/ad02/generated-wan/` and merged the same
day (PR #1). They are no longer listed here. The findings and the reasoning behind each fix are
preserved in `git log` and, in enforceable form, in `LESSONS.md`; the audit itself is
`docs/strategy/spec.md` Part II.

> **H27–H31 were filed as H26–H30 and moved.** `H26` was taken the same day, by concurrent work that
> could not see this table, for "the licence register is global while the fact ledger is per-video"
> — which is open and listed in Part VI. Commit `9116507` says "Record H26" and means that one, so
> these are the entries that move. Same rule, and the same cause, as H25's own renumbering note.

| | |
|---|---|
| **H23** | For a Markdown script the ledger hash covered the stage directions too — fixed; `tests/test_gates.py` asserts that rewording an editorial note does not move the hash and changing a spoken word does |
| **H24** | The spec could not express an orthographic camera, which S1's area comparison needs — fixed; `tests/h24_projection.py` measures the projection rather than asserting an attribute |
| **H27** | `PassProfile.frame_count` refused an over-long shot and silently **padded** a short one, so a 2 s shot on `wan` played 35% slow and the paid clip was then unshippable — fixed; refuses at both ends |
| **H28** | `assemble` cut the edit in filename order from whatever frame directories were on disk, so a renamed shot re-entered the video and a non-sorting shot id reordered it — fixed; the spec's shot list is the edit order, orphans are refused |
| **H29** | Narration longer than `MAX_TEMPO` allowed was hard-cut mid-sentence by `-t slot` while printing a `fitted:` line that read as success — fixed; refuses and names the shot, the overrun and the shot length that would fit |
| **H30** | Every check in the harness was a threshold check, so nothing could see drift — fixed; `goldens/`, `check.ssim`, `check.check_goldens`, `verify --bless`, calibrated on two real double-renders |
| **H31** | The spin composition — the repo's most expensive bug — had no numeric test, only a WARNING whose thresholds overlap correct behaviour — fixed; `tests/spin_axis.py` |
| **H26** | `deliver --publish` read one hardcoded, global `legal/licences.json` — ep01's engravings — so s01, which generates every object it shows and borrows nothing, could not be published for reasons that had nothing to do with s01 — fixed; the register resolves to `spec/<id>/legal/licences.json` with **no fallback**, an empty `"assets": []` is a positive declaration and a missing `assets` key is refused |
| **H32** | `render --stills` wrote ONE frame per shot and `check_motion` returns early below three, so the cheap pre-flight pass was structurally blind to a frozen shot — the fault that put 3.5 h of s01 frames on disk as still photographs, caught only by `verify` afterwards — fixed; the stills pass renders first, middle and last and checks motion and coverage per shot. **Numbered H32 because H27 is taken twice** (the `frame_count` entry above, and the `check_motion` wiring entry in Part VI); that collision is unresolved, not inherited by this one |

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

**Check.** `tests/test_backend.py` asserts a one-frame benchmark is **refused** and writes no row —
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

**Checks.** `tests/test_spec_validation.py`: `smooth = true` is refused with "expected an angle in DEGREES"
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

### H25 — `GEN cylinder` has a published table to be checked against, and nowhere to put the check

H21 made a cylinder *look* right. This is about making it *measure* right.

> Numbered H25, not H23. This was filed as H23 on 2026-09-18 and a different H23 — the Markdown-script hash fix — was added the same day by concurrent work that could not see it. Commit `2e5a328` says "Fix H23" and means that one, so this is the entry that moves.

S1's cylinder is the first component in this repo whose geometry has a **manufacturer's printed
answer**. Bosch Rexroth RE 17331 publishes, for a 140 mm bore and 100 mm rod, a piston area of
**153.94 cm²** and an annulus area of **75.40 cm²**. Derived independently from the geometry this
session: 153.94 and 75.40, agreeing to 0.002 cm².

Every other generator in `library/` is checked against a dimension (`shield` is 12×3 frames because a
source says so). None is checked against a *derived quantity* a vendor also publishes. `screw` is the
cautionary case — `library/README.md` rule 1 records it as `measured: false`, its pitch chosen to
make the arithmetic work, and that was the honest answer available at the time.

**Blocks:** nothing today; `GEN cylinder` does not exist yet. Recorded now because the check has to
be written with the component, not retrofitted after a render looks plausible.

**The check, precisely.** When `GEN cylinder` lands, `tests/test_scripts.py` builds a 140 × 100 cylinder and
asserts its derived piston and annulus areas match 153.94 cm² and 75.40 cm² within 0.01 cm². It fails
if the generator ever computes an annulus from the bore radius instead of the bore *area*, which is
the single most likely way to get this wrong and produces a number that still looks reasonable.

**Why this is not H7's tautology.** A `[shot.mechanism]` block that restates three hand-written
numbers proves nothing. This compares the generator's output against a figure printed by someone
who does not know this repo exists.


### H27 — `check_motion` cannot run on the shipping path

`verify` calls `check_storyboard`, `check_depth_pass`, `check_clip` and the canary.
**It never calls `check_motion`.** The only call site in the repo is inside `check_depth_pass`
(`harness/check.py:224`), and `verify` reaches that only through `renders/<ep>/*/depth/*` — control
passes, which exist only when a generative backend is being prepared.

So on `local` — which **D1 declares the shipping path** — the check never runs at all.

**This is the third time a check has existed, been tested, and been wired to nothing.** `check_clip`
shipped called from the wrong branch of `cmd_generate` and `ad02`'s payoff shot went out crushed to
black through the gap. `check_motion` was written in response to the windmilling screws — the repo's
most expensive bug, and the one LESSONS.md calls out as structurally invisible to a per-frame check.
It is the single check that exists to see faults *between* frames, and the default pipeline cannot
reach it.

**Found by running it by hand** over s01's 900 finished frames, after `verify` reported
`all 900 artefact(s) pass`:

```
b01    150 frames  nothing moves across the shot (total frame-to-frame change 0.00)
b02    210 frames  nothing moves across the shot (total frame-to-frame change 0.00)
b04    210 frames  nothing moves across the shot (total frame-to-frame change 0.41)
```

Three of six shots were frozen on screen. **The tracks were applied and correct** — the rod really
did stroke 0.55 m. It was invisible: the rod ran off frame, its visible length is a featureless
cylinder, and the piston was hidden inside a solid barrel, so a half-metre of travel changed not one
pixel. The same family as "an object symmetric about its axis cannot show that it is turning", and
3.5 hours of render went into a hook that is a still photograph.

**Blocks:** nothing mechanically - but it let a whole cut render wrong, and `verify` said it passed.

**Fix.** `cmd_verify` groups `renders/<ep>/*/frame_*.png` **by shot directory** and runs
`check_motion` per shot. It must not be run over the flat glob: `check_storyboard` is per-frame and
does not care, but `check_motion` compares adjacent frames and would read the seam between two shots
as a lurch. Note the message interpolates `frames[0].parent.parent.name`, which prints the EPISODE id
for a `renders/s01/b01/frame_*.png` layout - every problem above says `s01:` where it means `b01:`.
Fix that with it or the report names the wrong thing six times.

**Check.** `tests/test_checks.py`: a synthetic shot of identical frames must be reported by `verify`, and a
shot whose frames differ must not be - the same shape as the black-frame test, which is the only
evidence that a check works.

### H28 — Nothing gates a render on a human having looked at the picture — FIXED

`factgate` requires `human_approved` on every fact before `--publish`. There is **no equivalent for
the frames.** `verify` runs `check_storyboard`, `check_coverage`, `check_motion` and the pace check
— all of them technical — and prints "all N artefact(s) pass". That sentence has never meant "this
cut is any good", and twice this week it was read as though it did.

The research is `docs/harness/storyboard-gate.md`. The finding that matters: VFX and animation track
**two separate approval axes**, `VERSION APPROVED` (creative) and `TECH CHECKS APPROVED`
(technical), and the vocabulary even has a state for when they disagree —
`PUBLISHED - ELEMENT IN PIPE`, "internally approved but tech checks failed". Brunel has one axis and
behaves as though it were both.

**Cost paid for not having this:** s01 was rendered four times. A 3.5-hour render went out with
three frozen shots; a 22-hour overnight attempt died carrying a backdrop that had never been
approved as a look. Every fault in `storyboard-gate.md` §3 was visible in a still beforehand. The
storyboard pass ran every time — nobody was ever required to look at it.

**Blocks:** nothing mechanically. It is the reason four renders happened instead of one.

**Fix — three gates, cheapest first.**

1. **LOOK.** One shot at final resolution and samples, approved once per video: materials, lights,
   backdrop, type. A look change after board approval invalidates every board frame and must say so.
2. **BOARD.** `harness board <spec>` writes `spec/<id>/board/<id>.board.json` — one entry per shot
   carrying the still, its measured coverage, a note, and `review: {state, by, at}`. Approval is
   **fingerprint-bound** using the `_fingerprint(ep, shot, ...)` that `render.py` already computes
   for its resume cache: change the camera, a part, a track or a material and that shot silently
   returns to `unreviewed`. Approval that a later edit cannot invalidate is a memory, not approval —
   the argument that already justifies `script_hash_matches_ledger`.
3. **RENDER.** Full quality refuses a shot that is not `approved`. `--fast` and `--stills` are never
   gated, or there is no way to iterate toward approval. `--waive` exists and is reported loudly,
   because a gate with no escape hatch gets routed around rather than used.

**Checks.** `tests/test_gates.py`: a full render is refused when a shot is `unreviewed`; the same
render is allowed once it is `approved`; approval is **dropped automatically** when the shot's
fingerprint changes (move a camera, re-run, assert the state reverted); and `--fast` is never
blocked by any of it. The third is the one that matters — the other two only test bookkeeping.

**Deliberately NOT included:** an automated judgement of whether a shot is good. `check_coverage` is
a floor, not taste, and H22 already records why a "does this frame read" check would cry wolf. This
item adds a *place for a human decision to be recorded and invalidated*, nothing more.

**Built 2026-09-20.** `harness/boardgate.py` plus `harness board`, and a gate inside `cmd_render`.

```bash
harness board spec/s01/s01.toml                                  # the board, with coverage
harness board spec/s01/s01.toml --approve all --approve-look     # sign it
harness render spec/s01/s01.toml                                 # refused until you do
```

**The fingerprint is deliberately NOT `render._fingerprint`.** That one hashes the entire spec text
so any edit invalidates its resume cache — correct for a cache, useless for approval, because a
reworded comment would revoke every sign-off in the film and a gate that revokes itself constantly
gets waived by habit. `boardgate.shot_fingerprint` hashes only that shot: its camera, the parts
visible in it, their transforms and params, its tracks, the materials those parts use, the lights
active in it, and the frame size. **Samples and device are excluded** — they change what a frame
costs, not what it shows.

**Verified surgical, not blanket.** Moving `cam_hero` by 2 cm on `spec/s01` revoked exactly c01–c04,
the four shots that use it, and left c05 and c06 approved.

**Checks.** `tests/test_board_gate.py`. The centrepiece is
`test_approval_is_revoked_when_the_shot_changes`; its mirror,
`test_approval_survives_an_edit_that_cannot_change_the_picture`, is equally load-bearing, because a
gate that fires on a comment edit is one people learn to route around.
`test_the_preview_path_is_never_gated` asserts `returncode != 4` rather than `== 0` on purpose: the
fixture is a flat grey box that fails the *storyboard* check on its own merits, and conflating the
two would make the test green for the wrong reason the day this gate broke.

