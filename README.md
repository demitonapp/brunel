# Brunel

A harness for making video that gets **measurably better every time** — starting with Marc Brunel's
tunnelling shield for the Thames Tunnel (1825–1843), and built to grow into engineering-project and
construction-site simulation.

**One person art-directs. An LLM writes specs. Deterministic Python writes Blender. A pluggable
generative backend renders it photoreal.**

> The deliverable of the first cut is not a video. It is a **ratchet**.

See **[ROADMAP.md](ROADMAP.md)** for the thesis, the maturity ladder and the render plan, and
**[docs/](docs/README.md)** for everything else — it is indexed, and the four directories mean
different things:

| | |
|---|---|
| **[docs/strategy/](docs/strategy/)** | what we are making and why — the [product spec](docs/strategy/spec.md), the [slate](docs/strategy/slate.md), the [reach audit](docs/strategy/reach-audit-2026-09-18.md) |
| **[docs/videos/](docs/videos/)** | one directory per video: the brief and the script |
| **[docs/harness/](docs/harness/)** | the [backlog](docs/harness/backlog.md) (H1–H20, C1–C6) and the [decisions](docs/harness/decisions.md) (D1–D4) |
| **[docs/research/](docs/research/)** | the evidence base — every vendor claim with its source and confidence |
| **[docs/archive/](docs/archive/)** | superseded, kept for the audit trail, never cited as current |

---

## The direction

The original framing was "an engineering-history animation harness." The direction is wider and more
commercially deliberate:

1. **Marketing video now.** Short, compelling cuts about how things work — the shield, the dig, the
   advance. Made by one person, at a cost that survives iteration.
2. **Engineering simulation later.** The same architecture scales to construction sites and
   real-world engineering projects, because the simulation lives in the deterministic scene and the
   model only supplies the photorealism.

That second step is the reason for the architecture below, and the reason the generative backend is
deliberately swappable rather than chosen.

---

## The architecture: three layers, and only the middle one is uncertain

```
  TRUTH                    CONTROL                        RENDER
  ─────                    ───────                        ──────
  spec/*.toml              depth, segmentation,           local  (deterministic, free)
  hand-modelled geometry   edge, blurred RGB,             cosmos (Cosmos Transfer 2.5)
  fact ledger + factgate   beauty plate                   wan    (Alibaba Wan VACE)
        │                        │                              │
        └── Blender ─────────────┴──── harness passes ──────────┴── harness generate
            (authoritative)          (model-neutral)              (swappable)
```

**The scene graph never leaves Blender.** No video model accepts a mesh, a USD stage or a scene
graph — that is a structural gap in the industry, not a temporary limitation
([evidence](docs/research/video-api-geometric-control-comparison-2026-09-18.md) §9). What leaves is a
set of *rasterised control passes* that every control-capable backend already accepts. The scene
graph stays authoritative; the model constrains itself to the passes.

**Why that is the durable decision.** It is a 2026 finding that the vendors with the best aesthetics
have no geometric control, and the vendors with geometric control are a generation behind on looks —
Wan *closed* its control line at 2.5, LTX moved its frontier LoRAs to editing tasks, and Runway's
entire published API has zero geometric parameters. So the passes are the portability hedge: swapping
Cosmos for Wan for whatever ships next year is a backend config change, not a rewrite.

**What does not move.** Shield geometry, the 12×3 cell count, the screw pitch, the advance distance,
every dimension callout — all deterministic, all fact-gated, all composited on top. A diffusion model
garbles text, and a mis-rendered dimension is a fact-gate failure, not a cosmetic one.

---

## Status

Honest, as of 2026-09-18.

| | State |
|---|---|
| **`spec/ep01`** — the 8-shot, 72 s documentary | renders end to end as a low-fi animatic |
| **`spec/ad01`** — the 3-beat, 18 s marketing cut | validates and renders; storyboard now reads (see below); **not usable with `wan`** as written — its 6 s shots exceed the 81-frame limit (see the generative interface, below) |
| **`spec/ad02`** — the 5-beat, 20 s marketing cut | validates and renders; the current, fuller replacement for `ad01` |
| **`spec/s01`** — the 30 s hydraulic-cylinder Short | **fact ledger only.** Numbers sourced off manufacturer datasheets; 9/11 `factgate` checks pass. No `.toml` yet |
| **`harness passes`** — the control-pass exporter | **works**: all five passes verified, depth confirmed linear and greyscale |
| **`harness backends`** — the pluggable interface | **works**: local / cosmos / wan registered |
| **Cosmos hosted API** | **does not exist** — see the evidence in [docs/strategy/spec.md](docs/strategy/spec.md) §8.6/8.7 and [docs/research](docs/research/video-api-geometric-control-comparison-2026-09-18.md). Self-host only. |
| **Wan** | **called for real** on `ad02`; the delivered clip does not reliably match the requested length or duration (measured 81 frames returned for a 64-frame request) — `generate` and `deliver --backend` now measure and refuse on this rather than trust the request. See [docs/strategy/spec.md](docs/strategy/spec.md) Part II. |

### What the storyboard taught us

The first stills pass on the ad failed its own test, and the failures are the reason `ad01` exists in
its current shape. The shield read as a **flat fence**; the screws were **hidden behind the board**;
there was **nothing being dug** (no clay geometry at all, despite the narration promising it); there
was **no tunnel** — just an infinite grey plane; and the cameras were **dead-on symmetrical**.

All six are fixed in `spec/ad01/ad01.toml` and documented inline. The camera-placement lesson is
worth repeating here because it bit twice: **every camera must sit inside the bore radius**, and the
un-excavated clay must be **roof and invert, never a wall between camera and subject**.

---

## Quick start

```bash
cd brunel
uv venv --python 3.13
uv pip install -r requirements.txt -r requirements-dev.txt   # bpy==5.2.2, ruff, mypy
python -m harness doctor                # verify the toolchain lock
```

**Always storyboard before you render.** Eight stills cost about a minute and catch the framing,
staging and lighting disasters that a full render would otherwise hide for an hour:

```bash
python -m harness validate spec/ad01/ad01.toml
python -m harness render   spec/ad01/ad01.toml --fast --stills
```

Then the generative interface — two commands, deliberately separate because the first is
deterministic and free and the second costs money:

```bash
python -m harness backends                                    # what is available
python -m harness passes spec/ad01/ad01.toml --backend cosmos  # rasterise the scene graph
python -m harness generate spec/ad01/ad01.toml --backend local # hand it to a model
```

| Command | Does |
|---|---|
| `doctor` | verify the toolchain lock against what is actually installed |
| `validate` | load and validate a spec, no Blender required |
| `build` | spec -> `.blend`, run the assertion layer, write `manifest.json` |
| `render` | frames to `renders/<ep>/<shot>/`; `--stills` for the storyboard pass |
| `assemble` | frames -> silent mp4 |
| `captions` | narration -> SRT + ASS, respecting the Reels safe zone |
| `voice` | scratch VO via macOS `say`, aligned to the shot timeline |
| `pipeline` | build + render + assemble |
| `deliver` | assemble + captions + voice -> finished file; `--backend <name>` delivers from generated clips instead of Blender frames, timed on their measured length; `--publish` refuses without a passing fact ledger and licence register |
| **`passes`** | **rasterise the scene graph into control passes for a backend** |
| **`generate`** | **send those passes to a backend and collect the frames** (concurrent, costed) |
| **`backends`** | **list backends and the control-pass profile each one needs** |
| **`sheet`** | **contact sheets — a shot's motion in one image** |
| **`library`** | **browse the reusable engineering components** |
| **`verify`** | **run every output check over what exists** |
| **`bench`** | **measure s/frame at a real delivery resolution and record it** |

---

## The generative interface

A backend is anything that turns control passes into finished frames. It declares three things:

```
name       what to call it on the command line
profile    the resolution / fps / frame-count it needs
requires   which control passes it consumes
```

| Backend | Control passes it takes | Profile | Cost |
|---|---|---|---|
| `local` | plate | 1080×1920 @ 30 fps | **free, offline** |
| **`wan`** | **depth** | 1280×720 @ 16 fps, 81-frame limit | **~$0.08/s at 720p** |
| `cosmos` | plate, depth, seg, edge, vis | 1280×720 @ 16 fps, 93–480-frame limit | self-hosted NIM, 65.4 GB VRAM |

**"limit", not "chunk".** A shot longer than a backend's frame limit is refused at `passes` time,
not split — an earlier version chunked a long shot by re-applying its whole animation to each
chunk, which played the shot's full arc once per chunk instead of splitting it once. Shorten the
shot, or split it into two shots in the spec, if it needs to run longer than a backend's window.

### Start with `wan`, not `cosmos`

Cosmos is the better long-term destination and the worse first step. A hosted Cosmos API **does not
exist** — the only path is a self-hosted NIM on **65.4 GB** of VRAM, with an NGC key, a Docker
container and a 20 GB+ model pull. Nothing about that is "today."

**fal.ai's Wan VACE is the same shape and works in minutes:**

- **Sign up:** <https://fal.ai/login> — one key, a card, pay-as-you-go. **No minimum, no prepaid bundle.**
- **Price:** **$0.08/s at 720p**, $0.06/s at 580p, $0.04/s at 480p, billed at 16 fps of *delivered*
  video — see the caveat below before trusting a cost estimated from the request.
- **Licence:** marked commercial use.
- **Speed:** roughly a minute per generation.

Put the key in the gitignored `.env.local`:

```bash
printf 'FAL_KEY=your-key-here\n' > .env.local
```

**Why this is not a detour.** VACE and Cosmos Transfer both take a **depth control video** and return
a photoreal video. `depth` is the one pass the two share — which is why the harness renders it
first-class, and why the pipeline built on VACE ports to Cosmos without changing a spec, a pass, or a
line of the exporter. Only the backend name changes:

```bash
python -m harness passes   spec/ad02/ad02.toml --backend wan             # rasterise (depth only)
python -m harness generate spec/ad02/ad02.toml --backend wan --dry-run   # check setup, spend nothing
python -m harness generate spec/ad02/ad02.toml --backend wan             # actual spend printed after
```

`passes` has to run first — `generate` (dry-run or not) reads the control videos `passes` wrote and
refuses if they are missing. `--dry-run` then checks credentials and shows exactly what would be
submitted, without spending anything. An API you cannot smoke-test before paying is an API you will
pay to debug.

`ad01` is not usable with `wan` as written: its 6 s shots need 96 frames at 16 fps, and `wan`'s
81-frame limit is a hard refusal, not a clamp (see the limit note above) — `ad02`'s 4 s shots fit.

**A generated clip's length is not guaranteed to match what was asked for.** The first real `wan`
generation returned 81 frames (5.06 s) for a 64-frame (4.00 s) request — VACE does not appear to
honour the control video's own length. `generate` now measures every delivered clip and prints the
**actual** spend from that measurement, not from the request; `deliver --backend wan` refuses to
ship a clip whose measured length disagrees with the spec rather than burn captions timed for the
wrong duration onto it.

**`local` remains the default**, and not as a consolation prize: MechVerse measured the best video
model in the world at **2.91 out of 5** on mechanical correctness, and found perceptual quality
uncorrelated with it. A deterministic render is still the strongest engineering-explainer asset
available — the generative backend is for atmosphere, not for mechanism.

Adding a backend is one class in `harness/backend.py` and one entry in `BACKENDS`. No spec changes,
no pass-exporter changes.

---

## The harness looks at the result

Every expensive failure in this project has been **silent**. A camera outside the tunnel bore rendered
black. A depth map was inverted. Another saturated to white. A colour map had no colour. A screenshot
showed a frame that never changed when the code did. **None of them raised an error, and all of them
were visible in the pixels.**

So the harness checks the pixels, at the points where checking is cheap:

| Check | Runs | Catches |
|---|---|---|
| **storyboard** | `render --stills` | frames that are black, flat, or 92% dark — i.e. a camera in the wrong place, which is this project's most common failure |
| **depth pass** | `passes` | a depth map that is not neutral, is saturated to one end of its range, or whose mean drifts across the shot (the per-frame normalisation the stock preprocessors do) |
| **clip** | `generate`, `deliver --backend` | a generated clip crushed to black, or delivered at a length that does not match the spec |

`python -m harness verify <spec>` runs all of them over whatever exists. `tests/run.sh` proves the
storyboard check fires on a black frame *and* stays quiet on a real one — a check that has never been
seen to fail is not a check.

**The clip check shipped once without actually running.** It existed, was tested, and was called in
the wrong branch of `generate` — the one taken only when a single shot is generated, not the
concurrent submit-then-collect branch every real multi-shot run takes. The payoff shot of `ad02`
went out crushed to black through the gap. Both `generate` and `deliver --backend` now run it
unconditionally, and `docs/strategy/spec.md` records the audit that found it.

**The depth check pays for itself.** On `ad02` it blocked a paid generation because three of four
depth passes were saturated, and the fix was to let a shot declare its own range:

```toml
[[shot]]
id = "m01"
depth_range = [1.2, 9.5]   # near, far — overrides the camera-derived default
```

That is the shape of the ratchet: the check found the fault, the fault produced a spec capability,
and the capability is now available to every future shot.

**A part can ask for smooth shading, and it is an angle, not a flag.**

```toml
[[part]]
id = "barrel"
gen = "cylinder"
smooth = 30                                   # degrees; sharper edges stay sharp
params = { radius = 0.070, depth = 0.90, segments = 64 }
```

There was no mesh smooth shading in the harness at all until 2026-09-18 — `render._smooth()` is
f-curve easing, not `shade_smooth`. Flat is right for the shield's boxes and bricks and wrong for a
turned steel surface. It is an **angle** because shading every polygon smooth turns a cylinder's end
cap into a dome, and an end cap is exactly what an exploded mechanism shot is showing. Opt-in per
part, so no existing frame changes. `segments` is new for the same reason: `_cyl` always took it and
no spec could set it, so every cylinder in the repo was 24-sided whatever it was for.

**A per-frame check cannot see a fault that lives between frames.** The windmilling screws — a
`.z` Euler track that swung the whole shaft round like a propeller — passed `storyboard`, `depth`
and `clip` without a murmur, because every individual frame was a perfectly good picture.
`check_motion` now samples across the shot and measures adjacent differences: a frozen shot is a
hard failure, a busy one is a warning to go and look. **And the check is honest about its limits:**
after the fix, correct rotation measured 14.3–16.3 against the bug's 18.1–19.5, so a single
threshold cannot separate them. Both numbers are recorded in `harness/check.py`.

**The spec can now declare a mechanism, and the harness can check it.** `turns x pitch == advance`
is asserted at *validation* time — no Blender, no render, no money:

```toml
[shot.mechanism]
turns = 6.0
pitch = 0.033    # m per turn
advance = 0.20   # 6 x 0.033 = 0.198, within tolerance
```

A jack that turns six times and moves nothing is not a subtle animation error; it is a machine that
cannot exist, and it shipped once with the arithmetic written in a comment where nothing could
check it.

Also in `tests/run.sh`: **no shadowed top-level definitions.** A scripted rewrite left a duplicate
`_depth_range` in `passes.py`, and Python takes the last one — so two rounds of careful fixes changed
nothing, and the same broken number came back three times to three decimal places. The test found
four more dead copies of the same mistake in the same file.

---

## Measured, not estimated

`render-bench.json` holds real numbers from this machine. On the M1 (Cycles, CPU):

| Scene | Resolution | spp | s/frame | Notes |
|---|---|---|---|---|
| `spec/ep01/ep01.toml` | 384×682 | 8 | **1.97** | 864 frames, 1442 objects — the number to trust |
| `spec/mvp/mvp.toml` | 384×682 | 8 | 3.00 | over 48 frames, so ~half of it was scene build |
| `spec/mvp/mvp.toml` | 384×682 | 8 | 3.91 | Metal — *slower* than CPU on the M1 |

**Measured at delivery resolution**, 2026-09-18, by `harness bench` — because everything above is a
384×682 render and every schedule claim used to be a pixel-and-sample extrapolation from it:

| Scene | Resolution | spp | s/frame | |
|---|---|---|---|---|
| `spec/ad01/ad01.toml` a01 | 1080×1920 | 8 | **26.86** | 24 frames, M1 CPU, build time excluded |

The extrapolation predicted 62.4 s/frame at 32 spp — 15.6 scaled to 8 spp — so the real cost is
**1.7× the estimate**. Which is the point: a 30 s Short is **6.7 h** (one overnight) and a 7-minute
long-form is **94 h and ~29 GB** against 12 GiB free. See H19/H20 in
[docs/harness/backlog.md](docs/harness/backlog.md).

**Run a bench on an idle machine.** The same 24 frames measured 31.98 s/frame with other work on the
same 8 cores and 26.86 idle — a 19% spread. One row is a measurement with an error bar.

The **RTX 3080 / OptiX row is still `not_measured`**, and it governs Phase 1.

**Control passes are far cheaper than beauty frames**, which is what makes the generative loop viable
at all. Measured on the M1 at 320×180: depth **0.13 s/frame** (Cycles, 1 sample, unlit emission),
edge and blur **~0.25 s/frame** (ffmpeg), segmentation **~1.5 s/frame** (Workbench). The beauty plate
is the expensive one, and it is the one a generative backend replaces.

**Two measured traps, both recorded in `LESSONS.md`:**

- **Short benchmark runs lie.** Scene construction is a fixed cost independent of frame count, so a
  48-frame benchmark overstates per-frame time by about half. Measure over hundreds of frames.
- **AgX destroys a depth map.** Rendering depth through the episode's AgX view transform compressed
  it into 0.48–0.77 instead of 0–1. A control pass is data, not a picture: depth and segmentation
  render with the Standard transform.

---

## Layout

```
harness/          the compiler - the only thing that writes bpy
  spec.py         spec loading + validation (closed vocabulary, refuses to guess)
  generators.py   geometry generators
  build.py        scene graph, assertion layer, manifest
  render.py       per-shot staging, visibility, tracked animation
  passes.py       scene graph -> control passes (depth/seg/edge/vis/plate)
  backend.py      the pluggable video backends (local / cosmos / wan)
  captions.py     narration -> SRT/ASS, burn-in
  audio.py        scratch voiceover via macOS say
  factgate.py     accuracy gate (--publish blocks)
  assemble.py     frames -> mp4
spec/             episode specs (TOML), shot lists, fact ledgers
docs/strategy/    what we are making and why - spec, slate, reach audit
docs/videos/      one dir per video - brief + script. Facts, script, spec, render, in that order
docs/harness/     backlog (what is broken) and decisions (what is settled, and what reopens it)
docs/research/    the evidence base - every vendor claim, with sources and confidence
docs/archive/     superseded documents, kept for the trail
library/          the compounding asset kit (GEN / MAT / SHOTS)
goldens/          canary renders for regression - EMPTY as of 2026-09-18, no canary yet
qa/               rubrics, one per maturity level - only L0's is written
legal/            per-asset licence register
eval/             the eval ledger - the only accepted retrospective evidence -
                  README only as of 2026-09-18, no ledger entries yet
renders/          gitignored output
```

---

## Principles

1. **The model is interchangeable; the harness is the moat.** The LLM writes a diffable spec; only
   deterministic Python writes `bpy`; the generative backend is one class with three attributes.
2. **The scene graph never leaves Blender.** What leaves is control passes. That is what makes the
   backend swappable and the geometry authoritative at the same time.
3. **Automate generation, never adjudication.** The critic is advisory. The human gate is mandatory.
4. **Score renders, not code.** "The script ran" is not "the shot works".
5. **Storyboard before you render.** Eight stills are cheaper than an hour of wrong frames — and this
   project's own storyboard has now caught two rounds of staging failures before a frame of quality
   render.
6. **A control pass is data, not a picture.** Linear, full-range, consistent across frames. Depth
   normalised once per shot, never per frame.
7. **1 Blender unit = 1 metre.** Always. Hero dimensions within ±10% of a cited source.
8. **Facts before script; script before render.** The fact ledger is bound to the narration by hash,
   and `factgate` evaluates 11 rules against it.

---

## Requirements

- Python **3.13** exactly (bpy 5.2.2 requires it)
- `ffmpeg` (present: 8.0.1) — now also required for the `edge` and `vis` passes
- `ruff` and `mypy` — HARD dependencies of `tests/run.sh`, for the same reason as `jsonschema`
  below. `requirements-dev.txt` pins both. mypy is what catches a top-level definition shadowed
  by a later one — the defect that once made two rounds of careful fixes change nothing, because
  Python takes the last definition. `tests/fixtures/shadowed_def.py` exists to prove it fires.
- `jsonschema` — a HARD dependency of the fact gate. A gate that silently skips schema validation
  when a library is missing is not a gate.
- Optional: a Windows box with an NVIDIA GPU for final frames
- Optional: a GPU with **65.4 GB VRAM** for a self-hosted Cosmos NIM — the hosted endpoint does not
  exist, so this is the only Cosmos path
