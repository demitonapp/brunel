# Generative Video Backends for Brunel — Seedance, Wan, LTX, and the Open-Weights Route

**Research date:** 18 September 2026. Every claim below was checked against a live source on that
date unless marked otherwise. Vendor pricing and model line-ups change monthly; re-verify before
relying.

**Subject:** whether a generative video model can serve as a render backend for a deterministic
Blender pipeline producing vertical 9:16 engineering-history animation (Episode 1: Marc Brunel's
tunnelling shield, Thames Tunnel 1825–1843).

**Confidence convention.** `HIGH` = verbatim text fetched from the primary source this session.
`MEDIUM` = fetched from an authoritative secondary source, or fetched with an unresolved ambiguity.
`LOW` = inferred or single weak source. `INFERENCE:` = reasoning, not a citation. `UNVERIFIED` =
could not confirm; asserted nowhere.

**Companion files in this workspace:**
- `docs/research/generative-3d-assessment-2026-09-17.md` — the same question for *3D assets*
  (image-to-3D). Its verdict — "hand-model every object the audience can measure" — is the premise
  this document inherits.
- `docs/research/blender-pipeline-research-2026-09.md` — §D4 prices the AI image/video market.
  This document supersedes its video-model coverage.
- `ROADMAP.md` §1 ("the model is the interchangeable part; the harness is the moat") and §9 (the
  render-node constraint).

---

## EXECUTIVE VERDICT

**No generative video backend accepts scene, geometry, or diagram semantics. Not one.** Every one of
them accepts a prompt plus loose reference media (images, video, audio, documents) plus optionally a
first and/or last frame. The structured engineering content — parts, camera rigs, dimensions,
section/exploded/cutaway intent — must be baked into *pixels* by Blender before any of them can see
it, and even then it is a reference the model *interprets*, not a constraint it *obeys*.

This is not a temporary limitation of one vendor. It is the structural gap described in §6: the
deterministic rendering world solved renderer interchange with USD + Hydra, and the generative world
has no equivalent, because diffusion models do not consume declarative scene descriptions.

| Backend | Structured 3D input? | Geometric conditioning | Vertical 9:16 | Commercial route | Cost / 72 s @1080p |
|---|---|---|---|---|---|
| **Wan 3.0** (API-only) | **No** | **None exposed** (prompt + refs + frames only) | Yes (`9:16`) | Cloud service contract | ~$7–20 (see §3) |
| **Wan 2.2** (open, self-host) | **No** | **Yes** — depth/pose/edge via ComfyUI | Yes (pipeline-dependent) | Apache 2.0, but **24 GB VRAM** | ~$0 + GPU time |
| **Seedance 2.5** (closed) | No | Clay-render *reference* (proprietary) | Yes | BytePlus/aggregator | ≈$41 |
| **LTX-2.5** (open) | No | Limited | Pipeline-dependent | LTX-2 Community Licence | ~$0 + GPU time |
| **Veo 3.1** (closed) | No | ≤3 reference images, first/last frame | Yes | Google API | $5.76–8.64 (8 s cap) |

**The consequence for the harness is the important part.** Wan 3.0 — and every closed hosted API —
is a *polish and atmosphere* backend operating on frames Blender already produced. It is not a
renderer of the scene, and it cannot be allowed to become one. The truth layer stays deterministic.
That conclusion is unchanged from `generative-3d-assessment-2026-09-17.md`; what is new here is that
it now holds for the *video* stage too, and for a harder reason: there is no input channel to put the
geometry through.

---

## 1. The requirement, stated as a test

Any backend must pass all four before it is considered:

1. **Geometric control (non-negotiable).** Must accept the deterministic scene's geometry or a
   faithful projection of it (depth, edges, normals, clay render) so it cannot invent the shield,
   the segmental rings, or the rivet rows. This is the whole thesis: `factgate` + hand-modelled
   hero geometry are the product.
2. **Format.** Vertical 9:16, 1080×1920, 30 fps, shot lengths ~6–12 s (Episode 1 is 8 shots / 72 s).
3. **Commercial licence** for a monetised Instagram Reels channel, with a deliverable that survives
   a vendor changing terms.
4. **Cost** that survives iteration — the real number is rate × attempts-per-keeper, not rate.

---

## 2. What each backend actually accepts

### 2.1 Wan 3.0 — the full documented input surface `HIGH`

Fetched from Alibaba Cloud Model Studio, *Wan3.0 Video Generation*, last updated 17 Sep 2026
([docs](https://www.alibabacloud.com/help/en/model-studio/wan3-video-generation-guide)).

`wan3.0-video` / `wan3.0-video-prime` is an "All-in-One" model: one model name, task type selected by
the `type` field in `input.media` plus prompt intent. Documented capabilities: **up to 30 s per
generation, 30 fps output, native dialogue/BGM/SFX, up to 20 multimodal reference materials per
request, first/last-frame control, video editing and video extension.**

**The complete list of accepted inputs:**

| Input | Accepted values / limits |
|---|---|
| `prompt` | text |
| `resolution` | `480P` / `720P` / `1080P` (default) |
| `ratio` | `21:9` / `16:9` / `4:3` / `1:1` / `3:4` / **`9:16`** / `adaptive` |
| `duration` | 2–30 s, or `-1` (smart duration) |
| `first_frame` | one image |
| `last_frame` | one image |
| `reference_image` | **≤10 images, ≤20 MB each** |
| `reference_video` | **≤5 clips, total ≤15 s, ≤100 MB each** |
| `reference_audio` | **≤5 clips, total ≤15 s, ≤15 MB each** |
| `file` | **≤1 document** (the documented examples are `.pptx` and `.xlsx`) |
| `link` | **≤1 web page** |

**There is no mesh, no USD/glTF, no point cloud, no camera path, no depth map, no normal map, no pose,
no edge map, no segmentation, and no per-part or per-measurement field anywhere in that table.**

**Two constraints that bite a production pipeline `HIGH`:**

1. **Task types cannot be mixed.** "The `type` values of different task types cannot be mixed. For
   example, the first-last frame mode only supports `first_frame` and `last_frame`, and cannot accept
   `reference_audio` or other types at the same time." So anchoring a shot on rendered frames and
   also passing reference materials is **not** a legal combination. Choose one per generation.
2. **Documents and links must be public.** "Documents and web links only support publicly accessible
   pages that do not require login." A drawing or PPTX used as input has to be hosted publicly.

**What "document-to-video" actually is.** It parses a document (or web page) and generates a video
*about* it. The documented Excel example invents a four-segment animated business presentation with
charts, voiceover and sound design, reading cell values from named cells. That is a genuinely useful
capability — and it is **not** a geometry path. The model is told what the document says and then
composes pixels. `INFERENCE:` it is a content-summarisation feature, not a scene-rendering feature,
and should not be mistaken for one.

**Residual gap.** I read the capability table and the documented media types, not the full API
reference parameter list
([wan3-video-generation-api-reference](https://www.alibabacloud.com/help/en/model-studio/wan3-video-generation-api-reference)),
which was truncated in this session. A control-map parameter could in principle exist there. The
capability table's own wording ("only supports the `type` values listed in the table below") is
strong evidence it does not, but treat "no conditioning" as **HIGH-confidence, not exhaustively
verified**.

### 2.2 Wan 2.2 + ComfyUI — the control surface that does exist `MEDIUM`

This is the counter-intuitive finding. **The hosted Wan 3.0 API is *less* controllable than the older
open Wan 2.2 run locally.** ComfyUI ships first-class Wan control workloads:

- **Wan2.2 Fun Control** — depth/pose/edge video control
  ([ComfyUI docs](https://docs.comfy.org/tutorials/video/wan/wan2-2-fun-control))
- **Wan2.2 Fun Camera** — camera-motion control
- **Wan2.2 Fun Inp** — inpainting
- **Wan2.2 Animate** — character animation from a driving video
- **Control LoRA and Depth Control** in `kijai/ComfyUI-WanVideoWrapper`, plus a `VideoToDepth` node

`INFERENCE:` for Brunel this matters more than model generation does. Depth/edge conditioning from
*the Blender scene's own render passes* is a tighter constraint than any prompt-level reference,
because it constrains per-pixel structure instead of asking the model to interpret a picture. It is
also the closest thing the market has to a standard conditioning interface (§6).

The cost is real: see §4 — the open model is a 2025 generation, 720p/24 fps/5 s, and wants 24 GB.

### 2.3 Seedance 2.5 — clay-render reference `MEDIUM`

ByteDance's 2.5 accepts up to 30 reference images, 10 reference videos and 10 reference audio clips,
and documents a **clay render** reference mode: build blocking and camera with textureless 3D, and the
model generates from that structure
([announcement](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5)).
This is the richest *turnkey* control available from a hosted API — and it is still a reference the
model interprets, not a scene it renders. It is also the most expensive option on the board.

### 2.4 The rest

Veo 3.1: up to 3 reference images plus first/last frame. Kling 3.0: multi-shot, native 4K, but the
free/basic tier is non-commercial. MiniMax-H3: reference images free for the first 5, reference video
billed per input second. None accepts structured geometry.

---

## 3. Pricing `MEDIUM` (vendor and aggregator pages; re-verify)

**Official Wan 2.2** (Alibaba Model Studio, `wan2.2-t2v-plus`,
[source](https://help.aliyun.com/zh/model-studio/wan2-2-t2v-plus)) — **Text input only**:

| Resolution | Beijing | Singapore |
|---|---|---|
| 480P | ¥0.14 / s | ¥0.146785 / s |
| 1080P | ¥0.70 / s | ¥0.733924 / s |

≈ **$0.019/s at 480P, $0.097/s at 1080P**, i.e. ≈$7 for a 72 s episode.

**Seedance 2.5** is token-billed, not per-second. ByteDance publishes the formula
`(input video duration + output video duration) × width × height × fps / 1024` at $10.70/M tokens
(480p/720p) and $11.70/M (1080p), which reconciles to **$0.103/s (480p), $0.231/s (720p),
$0.569/s (1080p)** — ≈**$41** for a 72 s episode
([audit](https://ofox.ai/blog/seedance-2-5-price-audit-bytedance-formula-2026/)). A separate
normalisation puts Seedance 2.x at ≈$1.40 per 10 s 1080p clip, which is a looser approximation that
does not reconcile to ByteDance's own worked examples; prefer the token-derived figure.

**Normalised 10 s / 1080p / with audio** (invideo, Aug 2026, citing official rate cards;
[source](https://invideo.io/blog/ai-video-model-pricing/)):

| Model | 10 s bill | Note |
|---|---|---|
| Pruna P-Video | $0.40 | draft-tier fidelity by design |
| LTX-2.3 Fast | $0.60 | |
| LTX-2.3 Pro | $0.80 | open weights |
| Grok Video 1.5 | $0.80 | |
| Veo 3.1 Fast | $0.96 | **8 s generation cap** |
| Kling 3.0 Turbo | ~$1.10 | 720p only at the published rate |
| MiniMax-H3 | $1.30 | **at 2K**, not 1080p |
| Seedance 2.x | ≈$1.40 | token-billed approximation |
| Veo 3.1 | $3.20 | **8 s cap** |
| Sora 2 Pro | $8.40 | **API sunsets 24 Sep 2026** |

`INFERENCE:` the 8 s cap on the Veo rows is disqualifying for Episode 1's ~9 s shots unless shots are
split, which reintroduces the continuity problem the model was bought to solve.

---

## 4. The open-weights route — verified, and worse than it is usually described

### 4.1 The last open Wan is 2.2 `MEDIUM/HIGH`

[8frame ran the Hugging Face API query on 2026-08-28](https://www.8frame.co/blog/is-wan-3-open-source)
and printed the command and its output:

```bash
curl "https://huggingface.co/api/models?author=Wan-AI&sort=createdAt&direction=-1"
```

Newest repositories: `Wan2.2-Animate-2-14B-*` (2026-08-06), `Wan-Dancer-14B` (2026-07-10), then the
2025 Wan 2.2 and 2.1 releases. **No 2.5. No 3.0.** Their conclusion: *"the last Wan you can actually
download is Wan 2.2, released under Apache 2.0"*, and Wan 2.5 *"shipped as an API-only preview in
September 2025 and never published."* They print this as a correction of their own earlier claim,
which is the kind of provenance worth trusting.

**This conflicts with** [OneInfer's family page](https://oneinfer.ai/models/family/wan), which lists
Wan 2.5, 2.6 **and 2.7** as open weights. OneInfer is an aggregator's marketing page and shows no
method; 8frame shows its working. **Treat 2.6/2.7 open-weights claims as UNVERIFIED** and re-run the
curl before betting on them. `INFERENCE:` the confusion is plausibly a conflation with the
*Wan2.7-Image* release, which is a different modality.

### 4.2 Wan 2.2's hardware reality `MEDIUM`

Per the `Wan2.2-TI2V-5B` model card as reported by 8frame: **720p (1280×704 or 704×1280), 24 fps,
5-second clips, 24 GB minimum VRAM** (an RTX 4090-class card).

**This does not fit the RTX 3080.** The ROADMAP's render node is a 10–12 GB 3080. So the "self-host
for ~$0 marginal cost" argument does not hold at the published spec — it needs quantisation (no
vendor guarantee) or a larger card, and even then it delivers 720p/24 fps/5 s against Brunel's
1080×1920/30 fps/~9 s target. The escape hatch exists; it is a **downgrade**, not an equivalent.

### 4.3 The better open pick may be LTX `MEDIUM`

8frame's 2026 shortlist for open weights puts **LTX-2.5** ahead of Wan 2.2 — newer generation, native
audio, **LTX-2 Community Licence: free commercially under $10M revenue**. Wan 2.2 wins only on
licence permissiveness (Apache 2.0). For a solo operator well under the revenue threshold, LTX-2.5 is
the stronger open candidate. `UNVERIFIED`: the exact LTX-2.5 checkpoint licence text; the org has
published under more than one arrangement.

---

## 5. Lock-in

Choosing a closed API introduces lock-in at six layers, in descending severity:

| Layer | Severity | Detail |
|---|---|---|
| **The model** | **Hard** | Wan 3.0 has no published weights. It cannot be taken with you at any price. |
| **Unique features** | **Sharpest in practice** | 30 s native, single-pass audio, document-to-video. Build on any of these and nothing else can replace them. |
| **Rights** | Real | See §5.1. |
| **Look / prompt dialect** | Medium | Art-directing to one model's look means re-establishing it elsewhere. |
| **Vendor / price** | Soft | Wan 3.0 is served by Alibaba first-party plus fal, Replicate and others. You can change provider without changing model — but Alibaba can change terms for all of them at once. |
| **API plumbing** | Low | `DashScope VideoSynthesis` / one REST shape. A thin adapter. |

### 5.1 Model Studio terms `HIGH`

From the [service-specific terms](https://help.aliyun.com/en/model-studio/bailian-service-notes):

- **No warranty on generated content.** "Alibaba Cloud Model Studio makes no commitments or
  warranties regarding the content... generated during your use of application tools or trial
  services."
- **Your input is collected.** "You acknowledge that we collect your user content."
- **AI labels must not be removed.** "You must not remove or tamper with labels such as 'AI-generated'
  added by the trial service."
- **Trial output is non-commercial.** "The content you generate through model trials may only be used
  to evaluate the model's performance... You are prohibited from providing it to any third party in
  any form or from using or distributing it on any third-party platform."

The trial clause is the trap worth naming: any evaluation you do on free/trial quota **cannot appear
in a published episode**, and the AI label cannot be stripped. Both interact directly with
`ROADMAP.md` §11 ("Instagram deboosts / labels AI content — disclose deliberately").

### 5.2 Deprecation is documented, not hypothetical

- **Sora 2's API sunsets 24 September 2026** — six days after this document's date. Anyone who built
  on it migrates on OpenAI's schedule.
- **ByteDance rotates Seedance model IDs** (`-260128`-style suffixes), so even staying inside one
  family requires configuration-driven IDs.
- **Wan 2.5's weights never shipped** despite being widely described as open. "We may release weights
  later" is not a migration plan.

### 5.3 The mitigation `INFERENCE:` — this is the actionable part

The harness already has the right shape:

1. **Put the video model behind a `video_backend` adapter** with a normalised interface, exactly as
   Blender sits behind `harness/render.py`. The call is one function; the swap is one module.
2. **Express model-specific capability as a flag, never as spec vocabulary.** `harness/spec.py`
   already refuses unknown keys — that closed vocabulary is the lock-in firewall. A
   `document_reference` key in a shot spec would be the first foothold; keep it out.
3. **Emit conditioning in standard formats from your side.** The vendor's endpoint is proprietary;
   the bytes need not be. Render depth/edge/normal passes to OpenEXR/PNG and hand those over. This
   costs almost nothing and is what makes the Wan 2.2/ComfyUI route substitutable for a hosted API.
4. **Art-direct from the spec** — colour script, lighting rig — not by tuning a vendor's prompt style.
5. **Keep the canary renderable on two backends.** `goldens/canary/` plus SSIM/LPIPS already exist;
   re-rendering the benchmark shot on a second backend turns migration cost into a measurement.
6. **Never let document-to-video become load-bearing.** It is Wan 3.0's sharpest differentiator and
   simultaneously the one thing no alternative can replace. That is the definition of lock-in.

---

## 6. The standards gap

**There is no standard for video generation.** What exists sits on either side of it.

**Standardised — the scene/geometry input side:** OpenUSD (Alliance for OpenUSD / Linux Foundation),
glTF 2.0 (ISO/IEC 12113), MaterialX (ASWF), Alembic, OpenVDB, OSL; and for engineering, STEP
(ISO 10303), JT (ISO 14306), QIF (ISO 23952), IFC (ISO 16739).

**Standardised — the diagram semantics** (which is the surprise):
- **ISO 128** — technical drawing representation
- **ASME Y14.3** — orthographic and pictorial views, **including section and exploded views**
- **ASME Y14.5** — dimensioning and tolerancing (the "dimension callout")
- **ISO 10209** — the vocabulary that formally defines *section*, *cutaway*, *exploded view*
- **S1000D** — the international technical-publication specification, codifying illustration types
  and callout conventions

So *cutaway*, *section*, *exploded state* and *dimension callout* are all standardised concepts — as
**drawings**, not as generation.

**Standardised — the output side:** OpenEXR, ACES (SMPTE ST 2065), OpenColorIO, OpenTimelineIO, IMF
(SMPTE ST 2067), AS-11/DPP.

**Standardised — provenance and labelling:** C2PA Content Credentials (now with an
[implementation guide](https://c2pa.org/a-new-implementation-guide-for-content-credentials/)), the
EU AI Act Article 50 transparency obligation, and the European Commission's Code of Practice on
Marking and Labelling AI-Generated Content (June 2026). The industry standardised how to *disclose*
AI-generated video before it standardised how to *generate* it.

**Not standardised:** video-generation interchange, vendor-neutral video APIs, conditioning
interfaces. Depth/canny/pose/normal/segmentation are a *de facto* ControlNet convention with no
ISO/IEC backing; "clay render reference" is proprietary.

**The precedent that makes the gap legible.** The deterministic world solved renderer interchange:
**USD scene + Hydra render delegate** lets any renderer plug into any scene through one abstraction.
There is no Hydra equivalent for generative video, and the reason is structural — Hydra requires a
declarative scene description, and diffusion models do not consume those. **The moment intent is
expressible as a scene graph you are in standards territory; the moment it needs a diffusion model,
you leave it.**

---

## 7. Recommendation

1. **Blender remains the renderer of record for every shot the audience can measure.** The shield in
   section (shot 4, the benchmark), the cell cycle, the exploded states, the dimension callouts. No
   backend on this list can be trusted with them, and none can even accept them.
2. **If a generative backend is used at all, use it for atmosphere and period reconstruction only** —
   volumetric dust, gaslight, river haze, crowd silhouettes — fed by rendered frames, never as the
   source of structure.
3. **For that layer, prefer the open route** (Wan 2.2 + ComfyUI depth/edge control, or LTX-2.5) on
   licence and control grounds, accepting lower fidelity and — for Wan 2.2 — a hardware gap against
   the 3080.
4. **If paying, pay for Wan 3.0 or Seedance 2.5, not Wan 2.2.** Wan 2.2's hosted price is attractive
   (~$7/episode) but it is the family's oldest tier; the same money class buys a much better model.
   Wan 3.0 gives 9:16, 1080p, 30 fps and 30 s native — the format fits Episode 1 exactly.
5. **Keep the model non-load-bearing.** If the backend disappears, the episode should lose polish,
   not existence. That is what converts lock-in from an existential risk into a quality question.

---

## 8. Open items / low-confidence register

| Claim | Confidence | What would settle it |
|---|---|---|
| Wan 3.0 exposes no depth/pose/edge conditioning | HIGH, not exhaustive | Read the full `wan3-video-generation-api-reference` parameter list; search for a control-map parameter. |
| Wan 2.6 / 2.7 are open weights (OneInfer) | **Contradicted** | Re-run the Hugging Face `author=Wan-AI` curl; enumerate repos. |
| Wan 2.2 TI2V-5B = 720p / 24 fps / 5 s / 24 GB | MEDIUM | Fetch the `Wan2.2-TI2V-5B` model card directly. |
| LTX-2.5 exact licence text and checkpoint coverage | LOW | Fetch the LTX-2.5 repository licence and model card. |
| Wan 3.0 per-second effective price | UNVERIFIED | No per-second rate was read from a primary page this session; the ~$7–20/episode band is inferred from Wan 2.2 official pricing plus the Prime premium. |
| Whether Wan 3.0 accepts a non-public document via some upload path | LOW | The docs say otherwise, but only for the documented `file`/`link` types. |
| Sora 2 API availability after 2026-09-24 | MEDIUM | Moot after that date; treat the model as unavailable for planning. |

---

## 9. Sources

- Alibaba Cloud Model Studio, *Wan3.0 Video Generation* (last updated 2026-09-17) —
  https://www.alibabacloud.com/help/en/model-studio/wan3-video-generation-guide
- Alibaba Cloud Model Studio, *wan2.2-t2v-plus* pricing —
  https://help.aliyun.com/zh/model-studio/wan2-2-t2v-plus
- Alibaba Cloud Model Studio, *service-specific terms* —
  https://help.aliyun.com/en/model-studio/bailian-service-notes
- 8frame, *Is Wan 3.0 Open Source? The 2026 Answer* (2026-08-28) —
  https://www.8frame.co/blog/is-wan-3-open-source
- OneInfer, *Alibaba Wan Models: 7 Versions, Open vs API-Only* —
  https://oneinfer.ai/models/family/wan
- ComfyUI, *Wan2.2 Fun Control* — https://docs.comfy.org/tutorials/video/wan/wan2-2-fun-control
- ByteDance Seed, *Seedance 2.5* —
  https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5
- Ofox, *Seedance 2.5 Pricing: Audit Any Provider With ByteDance's Own Formula* —
  https://ofox.ai/blog/seedance-2-5-price-audit-bytedance-formula-2026/
- invideo, *AI Video Model Pricing (Aug 2026): Official Per-Second Rates, Normalized* —
  https://invideo.io/blog/ai-video-model-pricing/
- C2PA, *A New Implementation Guide for Content Credentials* —
  https://c2pa.org/a-new-implementation-guide-for-content-credentials/
