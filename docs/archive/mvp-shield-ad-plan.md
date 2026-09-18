> **SUPERSEDED 2026-09-18 — rolled into [docs/strategy/spec.md](../strategy/spec.md). Do not edit.**
>
> Kept, when the rest of `docs/archive/` was deleted, because `LESSONS.md` and `spec/ad01/ad01.toml`
> still cite §1a, §2 and §4 — §4 in particular holds the Cosmos endpoint probe results, recorded so
> nobody re-runs that search. A superseded document that nothing points into gets deleted; this one
> is load-bearing.

# MVP — The Shield Ad: dig the dirt, then advance inch by inch

**Scope:** a ~25 s marketing piece in three beats, built from shots that already exist in
`spec/ep01/ep01.toml`. Written 2026-09-18.

**The three beats the ad needs, and where they already live:**

| Beat | Shot | What already exists |
|---|---|---|
| 1. The shield | **s04 "The Board"** | 12 frames × 3 levels = 36 cells; `cam_board` 40 mm |
| 2. The diggers move the dirt | **s05 "One Cell's Cycle"** | `cell_board` track: withdraw → cut → push forward |
| 3. Forward inch by inch | **s05 + s06** | `cell_frame` + both screws advance 0.30 m; screws rotate 2160° |

The narration is already written for s05, verbatim from the spec:

> *"A miner drew back his board and cut into the clay behind it. Then two screws, one at his head and
> one at his feet, pushed the cell forward against the finished brickwork."*

**This is not a new build. It is a carve-out, a physical-plausibility fix, and one new pass exporter.**

---

## 1. Track A — the animatic, today, no new code

The harness already supports everything needed. The `render` subcommand takes `--shots`.

```bash
python -m harness validate spec/ep01/ep01.toml
python -m harness render   spec/ep01/ep01.toml --shots s04,s05,s06 --fast --stills
python -m harness render   spec/ep01/ep01.toml --shots s04,s05,s06 --fast --res 480x854
python -m harness deliver  spec/ep01/ep01.toml --shots s04,s05,s06 --fast
```

**Do the `--stills` pass first, and look at it.** `LESSONS.md` records that the stills pass costs
about a minute and caught **five broken shots out of eight** on the last run — two of them unusable for
two *different* reasons (a camera inside a water box; an 85 mm lens 0.9 m from the subject). Eight
stills before an hour of frames is the cheapest check in this repo.

**This proves the story and the staging. It does not prove the mechanism reads** — see §5.

---

## 1a. FIRST RESULT — the storyboard does not yet read (run 2026-09-18)

Ran for real: `doctor: ok`, `validate: ok` (24 parts, 8 shots, 13 tracks), then

```bash
.venv/bin/python -m harness render spec/ep01/ep01.toml --shots s04,s05,s06 --fast --stills
# 3/3 frames in 29 s — s04 14.30 s/frame, s05 7.02, s06 4.18
```

The **pipeline works**. The **content does not yet read as an ad.** Looking at the three stills
(`renders/ep01/s0{4,5,6}/frame_0054.png`):

| # | Finding | Evidence |
|---|---|---|
| 1 | **The shield reads as a flat fence, not a tunnelling shield.** Dead-on symmetrical framing, no depth, no cutting edge, no hood. A viewer who does not already know what a shield is would not learn it here | s04 is a grid of vertical slots seen straight-on from 14 m |
| 2 | **s05 hides the very thing it is about.** The timber board occludes the screws — and the screws *are* the advance mechanism | s05 is a large tan panel with brick floating disconnected to its right |
| 3 | **There is nothing being dug.** Despite the narration — *"cut into the clay behind it"* — s05's parts are `cell_board, cell_frame, cell_lining, screw_foot, screw_head`. **No clay or earth geometry at all.** `clay` exists as a material in the spec but is unused in this shot | verified from the parsed spec |
| 4 | **No tunnel.** All three shots are the shield standing on the 240 m `ground` plane under a dark sky — no bore, no arch, no underground | s04/s05/s06 part lists |
| 5 | **The crew is not people, by design.** `gen_crew`'s own docstring: *"A reference figure... The scale witness in every hero frame."* It is a cylinder body, a sphere head and two legs — **no arms** | `harness/generators.py:161` |
| 6 | **Lighting is flat.** One sun at 1.55 plus a 0.45 fill, no contrast and no warmth | spec `key_tunnel` / `fill_tunnel` |

**`INFERENCE:` the consequence is sequencing, and it matters.** Testing Cosmos now would render a
beautiful photoreal **fence** — which answers nothing about whether the approach works. The
storyboard is the cheap, deterministic, account-free half; Cosmos is the constrained half. **Fix the
staging first, then spend API budget on the photoreal test.**

This is the stills pass doing exactly its job: `LESSONS.md` records that it caught five broken shots
out of eight on the last run. It has now caught one before a single frame of the ad was rendered at
quality.

### What the staging fix needs (all deterministic, no accounts)

1. **Earth.** Add clay/face geometry in front of the shield so there is something to dig — the
   narration already promises it.
2. **Move the board.** Stage s05 so the withdrawn board reveals the screws, and orient the camera to
   read the jack *and* the lining in one frame (§5).
3. **A tunnel.** `gen_ring` already builds a tunnel bore — shot 8 uses `legacy_bore`. Put the shield
   *inside* a bore so it has a place.
4. **Reframe for depth.** An oblique three-quarter view beats the dead-on symmetrical one; the
   `ROADMAP.md` L1 rule "every camera move has ease in AND ease out" applies, and L2 wants a declared
   focal-length mix rather than one lens.
5. **Lighting.** Period tunnel working light: a warm key at the face, cold falloff behind, some
   contrast to give the iron edges something to catch.
6. **Deal with the crew.** Either accept them as abstract scale witnesses (defensible, and honest) or
   replace them — but do not pretend the current pegs are people in a marketing cut.

Items 1–3 are geometry the generators can already make. None of this needs Cosmos.

---

## 2. The bug to fix before anything else: the advance is not physically synced

In `spec/ep01/ep01.toml`, s05 currently reads:

| Track | Frames | Values |
|---|---|---|
| `cell_board` location | 0.0 / 0.22 / 0.68 / 1.0 | −0.42 → −0.16 → **−0.98** → −0.98 |
| `cell_frame` location | 0.0 / 0.68 / 1.0 | 0.0 → 0.0 → **−0.30** |
| `screw_head` / `screw_foot` location | 0.0 / 0.68 / 1.0 | 0.0 → 0.0 → **−0.30** |
| `screw_head` / `screw_foot` **rotation** | 0.0 / **1.0** | 90° → **2160°** (6 full turns) |

**The screws turn for the whole shot but the frame only advances in the last third.** Four of the six
turns produce no movement. A screw jack cannot do that — the two channels are one mechanism.

`INFERENCE:` the fix is to sync them. 0.30 m over 6 turns is a **50 mm pitch**, which is physically
plausible for a jack, so keep the 6 turns and move the advance to match:

```toml
# both channels over the same window
[[track]]
part = "cell_frame"
channel = "location"
frames = [0.0, 0.22, 0.30, 0.68, 1.0]
values = [[0,0,3.39], [0,0,3.39], [0,0,3.39], [0,-0.05,3.39], [0,-0.30,3.39]]
```

This is exactly the class of defect `LESSONS.md` is for — a spec that validates, renders, and is
wrong. **Add a check**: at the frame where the frame first moves, assert the rotation channel is
within tolerance of `advance / pitch`.

---

## 3. The core problem: "inch by inch" is the hardest thing in the ad

0.30 m on an 11.43 m-wide shield is **~2.6 % of frame width**, played over roughly three seconds. At
that scale the motion is nearly imperceptible, and *more fidelity makes it worse* — a photoreal pass
adds texture and lighting noise that hides a 2.6 % translation.

**Nothing about a better renderer fixes this.** What communicates an incremental advance is the
**Mode C (diagram / data)** register your own `ROADMAP.md` §2 calls for and Episode 1 never built:

1. **A cutaway/section view** of the cell with the jack and the lining in one frame, so the gap closing
   is legible.
2. **The rotation made visible** — six turns of a screw is the *why*; show the thread.
3. **A dimension callout** pinned to the gap, ticking as it closes. `ROADMAP.md` §2 already specifies
   "geometry-node dimension callouts, orthographic cameras, typography" for this.
4. **A scale reference** — the `CHR_worker_scale` 1.70 m figure the ROADMAP already lists as a
   must-ship asset.
5. **Compression** — the tool the repo already uses: `maxWorkMs` / `speedUp` in the moments-style
   vocabulary collapses dead time. Show 6 turns in 2 s, not 6 s.

`INFERENCE:` the ad that works is **Mode B/C for the mechanism and Mode A for atmosphere** — cut to the
diagram when the mechanism matters, cut to the reconstruction when the *place* matters. That is how
every credible engineering explainer is cut.

---

## 4. Track B — the photoreal pass, and the one constraint that decides the format

The Cosmos route, per `docs/research/video-api-geometric-control-comparison-2026-09-18.md` §10.8:

| | |
|---|---|
| Endpoint | **`cosmos-transfer2.5-2b`**, free endpoint on build.nvidia.com |
| Control inputs | **up to 4**: canny, blurred RGB, segmentation mask, depth — all **derived from the same source video** |
| Output | **720P @ 16 FPS**; same length and resolution as the control input |
| Frame chunks | multiples of **93** do best (93 ≈ 5.8 s, 186 ≈ 11.6 s, 279 ≈ 17.4 s) |
| Control video spec | **1280×720** for the 720P model |

### ⚠ The constraint to test first `UNVERIFIED`

**The 720P model's control video is 1280×720 — landscape.** A 9:16 Reels ad is 1080×1920. A 9:16 crop
of a 1280×720 frame is only **405×720** — unusable for delivery.

Three ways out, in order of preference:

1. **Test whether the endpoint accepts a portrait control video** (720×1280). The model card specifies
   1280×720, but the underlying model may not care. **This is a five-minute test and it decides the
   whole pipeline.**
2. **Generate 16:9 and reframe to 9:16 in the finish** — accept the crop loss, or design the shots so
   the subject is centred and the crop is safe. The repo already has output-shape machinery
   (`cropWindow` / `OUTPUT_SIZES` in the moments harness) for exactly this.
3. **Ship the MVP as 16:9** for site/YouTube, and reframe for Reels as a second deliverable.

Do not design the ad until (1) is answered.

### Access paths — and why the *free* endpoint is for testing, not shipping

Yes, the hosted endpoint needs an account. More importantly, the four paths carry **different
licences governing your output**, and only one of them is a trial:

| Path | Signup | What governs the output | Hardware |
|---|---|---|---|
| **Blender only** | none | yours | Mac / 3080 |
| **Open Wan, local** | none (HF is ungated, Apache 2.0) | **Apache 2.0** — *"we claim no rights over your generated contents"* | 3080 — `Wan2.1-VACE-1.3B` at 8.19 GB |
| **Cosmos, self-hosted weights** | HF (repo is public, not gated) + a cloud GPU account | **NVIDIA Open Model License** — verified on the HF card | 65.4 GB → rented cloud GPU |
| **Cosmos, hosted endpoint** | **NVIDIA account + API key** | **NVIDIA API Trial Terms of Service** — `UNVERIFIED` (see below) | none |

**The signup is not the real cost — the trial terms are.** `build.nvidia.com` free endpoints are
*trial* services. Comparable platform trials restrict output to evaluation; Alibaba's Model Studio
trial clause, which *was* verified verbatim, says the output *"may not be used for any other purpose,
including any commercial purpose."* **`UNVERIFIED`: I could not read the NVIDIA API Trial Terms of
Service — the PDF returned `unsupported content type` and search did not surface the text. This must
be read before any output is published.**

**The practical split that follows:**

1. **Use the free hosted endpoint for the test only.** Answering "does photoreal period engineering
   work at all?" is *evaluation* — precisely what a trial is for, and free.
2. **Ship from a licensed path.** Either self-host the weights (the HF repo
   `nvidia/Cosmos-Transfer2.5-2B` is public under `nvidia-open-model-license`, separate from the trial
   ToS), or buy it as a commercial service from a launch partner (Baseten, CoreWeave, Deep Infra,
   Microsoft Azure, Nebius) where it is a service contract rather than a trial.
3. **Develop on open Wan locally**, because it needs no signup, no trial, and no commercial-terms
   question — Apache 2.0 on your own hardware. That is the substrate, not the destination.

### The verified request schema `HIGH`

From NVIDIA's own NIM for Cosmos documentation
(`docs.nvidia.com/nim/cosmos/3.0.0/quickstart-guide.html`), the `cosmos-transfer2.5-2b` inference
body is:

```json
{
  "prompt": "…",
  "video": "<url or base64>",          // the source RGB video
  "resolution": "480",
  "edge":  {"control_weight": 1.0, "control": "<url or base64>"},
  "seg":   {"control_weight": 1.0, "control": "<url or base64>"},
  "vis":   {"control_weight": 1.0, "control": "<url or base64>"},   // blurred RGB
  "depth": {"control_weight": 1.0, "control": "<url or base64>"}
}
```

Returns `{"b64_video": "<base64>", "seed": 42}`.

**Three constraints that change the pass exporter:**

- **`resolution` is `"480"` in the documented example** — the model card claims 720P. Confirm which
  values the endpoint actually accepts; it may be `"480"` and `"720"`.
- **Input video must be between 93 and 480 frames** — so the chunking range is wider than "multiples
  of 93", but 93, 186, 279, 372 still sit inside it.
- **All four controls take a `control_weight`** — which is where the spatiotemporal weighting from the
  model architecture surfaces in the API.

### Access blocker — unresolved as of 2026-09-18 `UNVERIFIED`

The API key is **valid**: `GET https://integrate.api.nvidia.com/v1/models` returns **HTTP 200** with
82 models. But the *hosted* endpoint for `cosmos-transfer2.5-2b` could not be located
programmatically:

| Probe | Result |
|---|---|
| `cosmos-transfer2.5-2b` in the `/v1/models` catalogue | **absent** — only `nvidia/cosmos-reason2-8b` and `nvidia/ai-synthetic-video-detector` appear |
| `/v1/health/ready`, `/v1/metadata`, `/v1/manifest` on both `integrate.api.nvidia.com` and `ai.api.nvidia.com` | **404** — those are self-hosted-NIM-only paths |
| Plausible hosted video paths (`/v1/video/…`, `/v1/genai/…`) | **404** |

**And the build.nvidia.com page's own UI is a warning sign.** Its *Experience* tab reads:

> *"Step 1: Select a Scenario — Select one of the Scenarios to enhance. Step 2: Generate Video."*

with presets **"AV Simulation and Real Fleet Scenarios"** and **"Robotics Scenarios"**.

`INFERENCE:` the free hosted access is very likely a **scenario-locked demo**, not a raw inference API
that accepts your own control videos. If so, **the Cosmos test cannot run on the free endpoint at
all** — it would need the **self-hosted NIM** (`nvcr.io/nim/nvidia/cosmos-transfer2.5-2b:1.2.0`, per
the NGC docs) on a **65.4 GB** GPU, i.e. a rented cloud instance.

**What settles it:** the code sample in the logged-in build.nvidia.com page shows the exact base URL.
Until that is read, the hosted path is `UNVERIFIED` and should not be guessed at — a blind POST would
spend credits and minutes on a path that may not exist.

### RESOLVED 2026-09-18 — there is no hosted API for Cosmos Transfer `HIGH`

A live key was used to probe the account. **No code sample or endpoint URL is offered on the
build.nvidia.com page for `cosmos-transfer2.5-2b`** — its *Experience* tab is the preset-scenario demo
and nothing else. The API probes agree:

| Probe | Result |
|---|---|
| Key validity — `GET /v1/models` | **HTTP 200**, 82 models listed |
| `nvidia/cosmos-reason2-8b` chat completion | **404** — `"Function 'e199b43b-…': Not found for account"` |
| `meta/llama-3.1-8b-instruct` | **410 Gone** — *"reached its end of life on 2026-08-26"* |
| `nvidia/llama-3.3-nemotron-super-49b-v1` | **410 Gone** — same EOL date |
| `cosmos-transfer2.5-2b` anywhere in the API surface | **absent** |

The catalogue is **stale** — it lists models that return 410. The key authenticates (these are proper
API errors, not 401s) but **the account has no usable inference access**, and critically
**`cosmos-transfer2.5-2b` is not reachable by API under any path**. The web UI is a scenario demo.

**`INFERENCE:` the hosted Cosmos route for our test does not exist. There is exactly one path left.**

### The remaining path: self-host the NIM on a rented GPU

Per NVIDIA's NGC documentation:

```bash
# NGC API key — a DIFFERENT credential from the nvapi- catalogue key
# Generate at https://org.ngc.nvidia.com/setup (select "NGC Catalog" service)
export NGC_API_KEY=<value>
echo "$NGC_API_KEY" | docker login nvcr.io --username '$oauthtoken' --password-stdin

docker run -it --rm --name=cosmos-transfer2-5-2b \
    --runtime=nvidia --gpus all \
    --shm-size=32GB --ulimit nofile=65536:65536 \
    -e NGC_API_KEY=$NGC_API_KEY \
    -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
    -p 8000:8000 \
    nvcr.io/nim/nvidia/cosmos-transfer2.5-2b:1.2.0

# then POST to http://localhost:8000/v1/infer with the schema above
```

| Requirement | Value |
|---|---|
| VRAM | **65.4 GB** → H100 80 GB, A100 80 GB, or RTX PRO 6000 96 GB |
| Where | any GPU cloud — RunPod, Vast.ai, Lambda, CoreWeave, Nebius, Baseten, Azure |
| Credential | **NGC API key** (not the `nvapi-` catalogue key) |
| Rough cost | ~$1–4/hr; container + weights download, a few inferences → **≈$5–25 for a test** |

**The cost is not the blocker — the setup is.** Which means the sequencing decision is now stark: a
cloud rental is only worth spending on a storyboard that reads. It currently renders a fence (§1a).

---

## 5. The new capability: a control-pass exporter

This is the only real code the MVP needs. Blender already knows the scene graph; the job is to
rasterise it into the exact modalities Cosmos accepts — **and this is the model-neutral asset that
survives whichever vendor wins** (§10.6 of the comparison doc).

New module: `harness/passes.py`, invoked as `python -m harness passes <spec> --shots ...`.

| Pass | Blender source | Notes |
|---|---|---|
| **Depth** | `use_pass_z` (Cycles) or Workbench depth | **Normalise once across the whole shot**, not per frame — `VideoToDepth`'s per-frame 2–85-percentile normalisation causes depth "breathing", and Lightricks' own guidance is *"use consistent depth range across all frames"* |
| **Segmentation** | material-index or object-index pass → flat colour per part | This is where the shield, the board, the screws and the crew become *distinguishable* to the model — the closest thing to handing over part identity |
| **Canny / edges** | Freestyle line render, or `cv2.Canny` on the beauty pass | Freestyle keeps it deterministic and in-Blender |
| **Blurred RGB** | a heavily blurred beauty pass | Cosmos auto-extracts edge + blur from RGB alone, so this is optional |

**Use Workbench or EEVEE for the passes, not Cycles.** The measured Cycles figure is 1.97 s/frame at
384×682/8spp on the M1, extrapolating to ~62 s/frame at 1080×1920/32spp. Passes do not need path
tracing — they should render in **seconds per frame**, which is what makes the iteration loop survive.
**Measure this before assuming it; `render-bench.json` currently has no EEVEE or pass-render row.**

Output contract: **1280×720 (or 720×1280 if the test in §4 passes), 16 fps, in 93-frame chunks.**

---

## 6. What must stay deterministic — never let Cosmos render the numbers

Cosmos adds **atmosphere**. Blender keeps **truth**. The split:

| Element | Where |
|---|---|
| Shield geometry, 12×3 = 36 cells, dimensions | **Blender** — fact-gated |
| Screw rotation, advance distance, gap | **Blender** — fact-gated |
| Dimension callouts, scale bar, labels | **Blender / composited in the finish** |
| Period brick, iron, gaslight, river haze, dust, crowd | **Cosmos** — atmosphere only |

`HIGH` diffusion models garble text — Luma's own docs admit *"long text may be partially garbled"* —
and a mis-rendered dimension is a fact-gate failure, not a cosmetic one. **Composite every number in
the finish, over the top of the photoreal plate.** That also means the numbers survive a model swap.

---

## 7. Test-first list, in order

| # | Test | Cost | Decides |
|---|---|---|---|
| 1 | `render --shots s04,s05,s06 --fast --stills`, then **look at it** | ~1 min | Does the staging work at all? |
| 2 | Does `cosmos-transfer2.5-2b` accept a **720×1280 portrait** control video? | 5 min | 9:16 vs 16:9 for the whole ad |
| 3 | Render one **93-frame** chunk of depth+segmentation+canny passes; time it | ~30 min | Is the pass loop fast enough to iterate? |
| 4 | Push that one chunk through Cosmos | ~? | **Does photoreal period engineering work at all?** The single biggest unknown |
| 5 | Fix the s05 advance/rotation sync (§2) and re-storyboard | ~1 h | Does the mechanism read? |
| 6 | Interpolate 16 → 30 fps, composite callouts, cut to ~25 s | ~1 h | — |

**Stop at 4 if the answer is bad.** If Cosmos renders generic photoreal materials that read as "wrong
era" — Victorian brickwork is not in its AV/robotics/agriculture training distribution — then the
photoreal track is dead for period work, and the ad should be a **stylised Blender piece with Mode C
callouts**, which is a perfectly good marketing asset and needs no model at all.

That risk is real and it is the reason test 4 comes before any production work.

---

## 8. Effort and cost

| | |
|---|---|
| Track A (animatic, existing code) | half a day, $0 |
| Pass exporter (`harness/passes.py`) | 1–2 days |
| Cosmos pass (free endpoint) | $0 to test; commercial terms of the **NVIDIA API Trial ToS** must be verified before publishing |
| Interpolation + composite + cut | half a day |
| **Total to a reviewable MVP** | **~3 days**, and it is genuinely a *pipeline* MVP — the exporter is reusable for every later episode and every construction-simulation use case |

---

## 9. Why this is the right MVP

It is not "make an ad." It proves the three things that decide the whole direction:

1. **The mechanism reads** — the dig-and-advance is legible to someone who does not know the shield.
2. **The pass exporter works** — scene graph → depth/segmentation/canny → model, model-neutrally.
3. **The photoreal pass is viable for period engineering** — the go/no-go on Cosmos for this content.

Each is falsifiable in a day, and each is worth knowing regardless of which vendor wins.

**And the fallback is already good.** Even if every generative backend fails, you are left with a
deterministic 25-second Blender piece with real dimension callouts and correct mechanism — which,
per MechVerse (§1 of the comparison doc — best model in the world at 2.91/5 on mechanical
correctness), is a better engineering-explainer asset than anything a video model would produce.
