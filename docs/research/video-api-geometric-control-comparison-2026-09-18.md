# Generative Video APIs vs Brunel's Standards — Which Accept Deterministic Geometry?

**Research date:** 18 September 2026. Vendor pages, Hugging Face / GitHub APIs and ComfyUI docs were
fetched live on that date. Model line-ups and prices change monthly; re-verify before relying.

**Question.** Brunel's truth lives in deterministic Blender geometry: hand-modelled, dimensionally
accurate, bound to a fact ledger. The question this document answers is narrow and specific — **which
generative video APIs accept our own scene, geometry, or control maps as input, so the model is
constrained by our geometry rather than inventing it?**

**"Our standards" means:** a scene graph, mesh/CAD/glTF/USD/STEP, camera path, depth map, normal map,
canny/edge map, pose/skeleton, segmentation mask, motion brush, dense point trajectories — and
diagram semantics (section, exploded view, dimension callouts).

**Confidence convention.** `HIGH` = verbatim from a primary source fetched this session. `MEDIUM` =
authoritative secondary or fetched-with-ambiguity. `LOW` = weak/single source. `INFERENCE:` =
reasoning, not a citation. `UNVERIFIED` = could not confirm; asserted nowhere.

**Companion files:** `docs/research/video-generation-backends-2026-09-18.md` (Seedance/Wan 3.0 pricing
and the lock-in analysis), `docs/research/generative-3d-assessment-2026-09-17.md` (the same question
for 3D assets — its verdict, "hand-model every object the audience can measure," is inherited here).

---

## EXECUTIVE VERDICT

**The field splits cleanly in two, and nobody bridges it.**

- **Creative/frontier models** — Veo, Sora, Kling, Seedance, Runway, Luma, Wan 3.0, MiniMax, Grok —
  have the best aesthetics and **no geometric control of any kind**. Their entire input surface is a
  prompt plus loose reference media (images, video, audio, documents) plus optionally a first and/or
  last frame.
- **Industrial/world-simulation and open-weights models** — Cosmos-Transfer, Wan VACE, Wan Fun
  Control, LTX IC-LoRA — accept **real geometric control**, and are a generation behind on aesthetics.

**Exactly four backends accept deterministic geometry, and only one of them is cheap and hosted:**

| Backend | Control accepted | Hosted? | Cost | Verdict |
|---|---|---|---|---|
| **Alibaba Wan VACE** | **depth, pose** (+ canny/MLSD/trajectory in the Fun variant) | **Yes** — fal.ai, Alibaba | **$0.10/s** ≈ $7.20/ep | **The one to use** |
| **Wan2.1-VACE-1.3B** | depth, pose, flow, scribble, masks, **bbox/track layout** | Open weights | **8.19 GB official** | **Start here** — only owner-published sub-12 GB control model |
| **Wan 2.2 Fun Control** | canny, depth, OpenPose, MLSD, trajectory | Open weights | ~$0 + GPU | Widest control set; **5B is 24 GB official**, not 8 GB |
| **NVIDIA Cosmos-Transfer1/2.5** | segmentation, depth, edge, blur, LiDAR, HDMap + MultiControlNet | Self-host / NIM | GPU | Richest control; **65.4 GB VRAM**, datacenter |
| **LTX IC-LoRA (2.3)** | depth, pose, edges (Union Control) | Open weights | **32 GB VRAM floor** | Strong control, **not 3080-viable**; $10M-revenue licence |

**Two corrections to the table above, both verified after first publication of this document:**

- **LTX-2.x is *not* runnable on a 3080.** Lightricks' own system requirements state a **"minimum
  32GB+ VRAM"**, recommending an A100 80GB or H100. Only the older LTX-Video 0.9.x line fits
  consumer cards, and it is a generation behind on control.
- **A 3080 cannot use the FP8/NVFP4 fast paths at all.** `torch._scaled_mm` (FP8 tensor-core GEMM)
  needs compute capability ≥ 8.9 (Ada); NVFP4 needs Blackwell. Ampere `sm_86` can *store* fp8 weights
  but gets **no speedup** — so the `fp8_scaled` Wan and `-fp8` LTX builds are storage savings, not
  acceleration. **Budget for GGUF (Q4/Q5) as the real 3080 path.**

**The one exact format match in the entire field is Wan 3.0** — 1080P, **30 fps**, **9:16**, 30 s
native, at **$0.20/s** (Singapore) ≈ $2.40 for a 12 s shot. It offers **no** geometric control, but it
is the only backend that natively matches Brunel's delivery spec without a conform.

**The single most important actionable finding** (§7.1): the open Wan control path does **not** accept
a Blender depth pass. It expects 8-bit, near/far-**inverted**, per-frame 2–85-percentile-normalised
depth. A raw Blender Z-pass will not match and must be remapped — and normalising once across the
whole shot instead of per-frame is a concrete advantage the deterministic pipeline has over the
stock preprocessor. **Lightricks' own documentation says the same thing as a rule** — see §1.1.

---

## 1. The measured state of the art on mechanical subjects

Before comparing control surfaces, it is worth recording what the research literature says about how
well *any* video model handles machinery — because it reframes the whole question.

**MechVerse: Evaluating Physical Motion Consistency in Video Generation Models** (arXiv 2605.14843,
Jain et al., submitted 2026-05-14) `HIGH` is the only rigorous benchmark of video models on
mechanical assemblies: **21,156 synthetic clips from 1,357 mechanical assemblies across 141
categories**, in three tiers of increasing kinematic complexity — independent articulation, pairwise
coupling, and densely coupled multi-part mechanisms.

Its findings, verbatim from the abstract:

> *"They often fail to generate motion governed by kinematic and geometric constraints. In these
> settings, object parts must remain rigid, maintain contact or coupling with neighboring components,
> and transfer motion consistently across connected parts... A generated video may therefore appear
> plausible while violating the intended mechanism, such as **rotating a part that should translate,
> deforming a rigid component, breaking coupling between parts, or failing to move downstream
> components**."*

> *"Results show that current models can preserve appearance and smoothness while failing to generate
> mechanically admissible motion, with **errors increasing as coupling complexity grows**."*

Reported scores (human judgment, out of 5): **HunyuanVideo 1.5 2.91**, Horse 2.89, Wan 2.7 2.78,
**fine-tuned Wan 2.2 2.65**.

**Four consequences for Brunel:**

1. **The best model in the world scores 2.91 out of 5 on mechanical correctness.** Nobody has solved
   this. The premise that accuracy is the product is not paranoia — it is the measured weakest axis
   of the state of the art.
2. **Perceptual quality is uncorrelated with mechanical correctness** (the paper's stated finding).
   A beautiful render can still rotate a part that should translate. That is precisely the failure
   that would destroy an engineering-history film, and no amount of prompt care prevents it.
3. **Fine-tuned Wan 2.2 (2.65) is competitive with closed models**, which argues that deterministic
   conditioning plus a fine-tune is the right architecture — rather than chasing each new closed model.
4. **The paper's own conclusion is that models need *"more explicit representations of parts, joints,
   and dependency structures."*** That is literally the scene graph the Blender pipeline already has.

`INFERENCE:` MechVerse's three tiers are a ready-made internal test suite, and its structured prompts
(part identities, stationary supports, moving components, motion primitives, direction, speed, and
inter-part dependencies) could be generated automatically from Brunel's scene graph.

**A vendor describes the same failure independently.** Lightricks' own blog names the artefact
"warble": *"Objects may subtly deform, wobble, or drift **even when they should remain rigid**,"* plus
*"swirling/'crawling' surface details... when they should be static."* Their prescribed fix is
Canny/Depth IC-LoRA anchoring. `MEDIUM`

### 1.1 Also verified: a vendor recommends Blender as the depth source `HIGH`

From Lightricks' official open-source docs (`docs.ltx.io` → IC-LoRA usage guide), under *Depth Maps →
Tools*, verbatim:

> * **Blender/3D software — For synthetic depth renders**

and their stated best practice for that control signal, verbatim:

> * **Use consistent depth range across all frames**
> * Ensure smooth temporal transitions (avoid flickering)

This is a vendor explicitly inviting the deterministic-Blender-to-depth-control workflow, and it
independently corroborates §7.1: because the stock `VideoToDepth` node percentile-normalises per
frame, it violates "consistent depth range across all frames." **Rendering depth in Blender and
normalising once for the whole shot is the correct approach, with vendor guidance behind it.**

---

## 2. The requirement, stated as a test

A backend must pass all four:

1. **Geometric control (non-negotiable).** Accept the scene's geometry, or a faithful projection of it
   (depth / edges / normals / clay render / point cloud), so it cannot invent the shield, the
   segmental rings, or the rivet rows.
2. **Format.** Vertical 9:16, 1080×1920, **30 fps**, shots ~6–12 s.
3. **Licence** permitting commercial social distribution, with a deliverable that survives a vendor
   changing terms.
4. **Cost** that survives iteration — rate × attempts-per-keeper.

---

## 3. Tier 1 — backends that accept explicit geometric control

### 3.1 Alibaba Wan VACE — the practical answer `HIGH`

VACE ("Video All-in-one Creation and Editing") is the only control-capable model that is **both
hosted and cheap**.

- **Alibaba official** `wan2.1-vace-plus`: *"All-in-One Video Creation and Editing model... supports
  multimodal conditional control through text, images, and videos."* Input modalities **Text / Image /
  Video**. **Price: $0.10 per second** (Singapore, std) — ≈**$7.20** for a 72 s episode. RPM 120.
  [model page](https://www.alibabacloud.com/help/zh/model-studio/wan2-1-vace-plus)
- **fal.ai hosted endpoints**, both marked **Commercial use**:
  - `fal-ai/wan-vace-14b/depth` — *"Endpoint for generating video from depth maps."* Input:
    `prompt` + `video_url` (the depth video).
  - `fal-ai/wan-vace-14b/pose` — *"Endpoint for generating video from pose data."*
  - `fal-ai/wan-22-vace-fun-a14b/depth` — the Wan 2.2 variant.
    [depth API](https://fal.ai/models/fal-ai/wan-vace-14b/depth/api)
- **Open weights** also exist (`Wan2.1-VACE-1.3B/14B`), Apache 2.0, ComfyUI `WanVaceToVideo`.

**The exact parameters (the single most useful finding in this document)** `HIGH` — from the official
Model Studio API reference for the legacy `wan2.1-vace-plus`:

| Parameter | Values | Purpose |
|---|---|---|
| **`control_condition`** | **`posebodyface`** \| **`posebody`** \| **`depth`** \| **`scribble`** | **The geometric control signal.** This is the only vendor-documented depth / pose / line-art control channel found anywhere in this research. |
| `strength` | 0.0–1.0 | How hard the conditioning is applied |
| `mask_image_url` / `mask_video_url` | image / video | White = edit, black = preserve |
| `mask_type` | `tracking` \| `fixed` | Whether the mask follows motion |
| `mask_frame_id` | int | Reference frame for a tracked mask |
| `expand_ratio` | float | Mask dilation |

**Caveats, stated honestly:** it is filed under *"Wan – legacy video models"* and **duration is fixed
at 5 s** — too short for a 6–12 s shot without stitching. Alibaba's own guidance on that page
recommends `prompt_extend: false` for accuracy-critical prompts, because prompt extension is LLM
rewriting of your carefully worded technical text.

`INFERENCE:` for Brunel this routes around the entire VRAM problem — you render the depth pass in
Blender, POST it, and pay $0.10/s. No 4090, no 65 GB requirement. The 5 s ceiling is the real cost:
it means three stitched generations per 12 s shot, with continuity risk at each seam.

### 3.2 Wan 2.2 Fun Control — the widest control vocabulary `HIGH`

Accepts **Canny, Depth, OpenPose, MLSD and trajectory** control, plus an optional separate
`ref_image`. Native ComfyUI node `Wan22FunControlToVideo`; inputs include `width` (default 832),
`height` (480), `length` (**81, step 4**), and optional `ref_image` / `control_video` (both `IMAGE`).

**VRAM is the decisive split:**

| Variant | VRAM | Max spec |
|---|---|---|
| **Wan2.1-VACE-1.3B** | **8.19 GB** — official, owner-published (`Wan-Video/Wan2.1` README) | 480P, ~5 s native; chain via `firstclip` |
| **Wan2.2-Fun-5B-Control** | **24 GB minimum** — official README, *with* `--offload_model True` applied. ComfyUI's *"should fit well on 8GB vram"* is a tooling claim the model owner does not support: **contingent, test before relying** | 121 frames @ 24 fps ≈ 5.0 s |
| Wan2.2-Fun-A14B-Control | ~20–21 GB fp8 (83 % of a 24 GB 4090D) | 81 frames @ 16 fps ≈ 5.1 s |

GGUF quants exist for both. **Licence: Apache 2.0**, and the Wan 2.2 README states verbatim *"The
models in this repository are licensed under the Apache 2.0 License. We claim no rights over the your
generated contents."* — the cleanest terms in this entire document.

A practitioner comparison rates Fun Control below VACE on consistency: *"It's not top tier quality...
feels like a research preview rather than a production tool,"* and *"if the first frame has a totally
different pose or position from the reference, Fun Control falls apart."* VACE *"keeps the character's
outfit consistent... animates smoothly without morphing."*
([wanimate.net](https://wanimate.net/wan-fun-control-vs-wan-21-vace))

**Fun Camera is a downgrade, not an upgrade** — it offers only preset moves (Pan Up/Down/Left/Right,
Zoom In/Out). It discards a solved Blender camera path.

### 3.3 Wan Uni3C — conceptually the best fit for Blender `MEDIUM`

Uni3C is the only mechanism found that consumes a **rendered point cloud produced by a camera
trajectory**. The ComfyUI node documentation says verbatim: *"using a rendered guidance video (e.g.,
warped point cloud renders)"* and *"the guidance video rendered from the camera trajectory, most
commonly warped point cloud renders of the input image."*

Node `WanUni3CControlnetApply`: inputs `model`, `model_patch`
(`comfy.ldm.wan.uni3c.WanUni3CControlnet`), `vae`, `render_video` (RGB `IMAGE`, first 3 channels),
`strength` (-10..10, default 1.0), `start_percent`, `end_percent`. Docs state **"This node is
experimental."** `UNVERIFIED`: checkpoint location, licence, VRAM.

`INFERENCE:` depth→point-cloud→warp is a projection computable exactly from Blender, so this is the
closest thing to "hand the model my scene and camera path." The blocker is that the weights are
unlocated and the node is experimental.

### 3.4 LTX IC-LoRA — richest named control set, revenue-limited licence `HIGH`

- **LTX-2 (19B)**: `IC-LoRA-Depth-Control`, `IC-LoRA-Pose-Control`, `IC-LoRA-Union-Control`, plus
  `LoRA-Camera-Control-{Dolly-In, Dolly-Out, Dolly-Left, Dolly-Right, Jib-Up, Jib-Down, Static}`.
  ComfyUI templates `video_ltx2_depth_to_video`, `video_ltx2_canny_to_video`, `video_ltx2_pose_to_video`.
- **LTX-2.3 (22B)**: `IC-LoRA-Union-Control` (depth, pose, edges from "various preprocessors") +
  `IC-LoRA-Motion-Track-Control`. ComfyUI `video_ltx2_3_ic_lora`.
- **LTX-2.5 is a regression for this need.** It is **gated** (`gated: auto`), and its published
  IC-LoRAs are **editing** tasks (Ingredients, Colorization, Deblur, Clean-Plate, Day-To-Night,
  Water-Simulation) — **no structural depth/pose/edge control LoRA was found.** Its headline specs
  (native 4K HDR, up to 50 fps, native multishot) are irrelevant to the control requirement.
- **Licence is the catch:** **LTX-2 Community License** (5 Jan 2026), *not* Apache. Verbatim:
  *"Entities with annual revenues of at least $10,000,000... are required to obtain a paid commercial
  use license."* Below $10M, commercial use is permitted. Derivatives must ship under the same
  agreement, and Lightricks reserves the right to *"modify the Output of LTX-2 based on updates."*
- **The camera-control LoRAs are presets, not trajectories** — for fidelity, the Depth-Control IC-LoRA
  is the more faithful path, because rendered depth encodes the true geometry.

### 3.5 Also-rans with real control `MEDIUM`

| Model | Control | Note |
|---|---|---|
| **MiniMax H3 + `MiniMax-H3-Fun-Controlnet-Union`** | canny, depth, HED, MLSD, pose + mask inpainting | **Will not run on a 3080** — needs a `qwen3vl_32b` text encoder |
| **CogVideoX-Fun V1.1 2B/5B Control** | canny, depth, pose, MLSD | Apache 2.0, small — but **49 frames @ 8 fps** (~6.1 s), weak by 2026 standards |
| **Wan-Move** | dense point trajectories | **5 s @ 480 p** only |
| **Wan ATI** (ByteDance) | "Any Trajectory Instruction" — object, region **and camera** | ComfyUI `video_wan_ati`; trajectory, not full geometry |
| **`TheDenk/wan2.2-ti2v-5b-controlnet-depth-v1`** | depth (MiDaS) on the **5B** base | Apache 2.0, low-VRAM candidate, but a **community** model (880 downloads, single author) — experimental |
| **`TencentARC/SCoPE`** | **camera trajectory** (sightline-coordinate positional encoding) | **The only Apache-2.0, no-territory camera-trajectory model found.** Base `Wan2.2-I2V-A14B`; card verbatim: *"Given a first frame, a text prompt, and a camera trajectory, it generates a video that follows the requested camera motion"*. **~67 GB checkpoint — cloud GPU only.** `UNVERIFIED:` whether arbitrary trajectories are accepted vs the shipped named presets |
| **Luma `ray-3.2` `video_edit`** | `depth/normals/pose/trajectory/face` **enable-flags** | The model **derives** the signals from your `source` video — you cannot upload a depth map. Best workflow: render Blender to a video, pass as `source`, `strength: "adhere_1"`, `blur: 0`, `augmentation: 0`. **No seed**; 24 fps |
| **`TencentARC/VerseCrafter`** | 4D: camera trajectory + 3D Gaussian object trajectories | **DISQUALIFIED — `license: other` + `extra_gated_eu_disallowed: true`, academic/research only** |

---

## 4. Tier 2 — semantic reference only (model interprets, can still invent)

### Seedance 2.5's "3D clay-model reference" is NOT geometric control `HIGH`

This corrects an earlier claim in this workspace. The capability is real and official — BytePlus's
Seedance 2.5 prompt guide lists *"3D clay-model reference/rendering"* — but:

- **There is no `clay_render` parameter.** It rides the ordinary
  `content[].type="video_url"` + `content[].role="reference_video"` slot.
- **The vendor scopes it to motion and framing, explicitly not geometry**: camera movement, shot
  rhythm, shot-size changes, subject trajectory — with materials/light/colour taken from *separate*
  images. It recommends *"simple geometric primitives"* and warns to keep the clay video free of
  *"trajectory lines, coordinate lines, camera cones."*

`INFERENCE:` anything dimensionally correct in the output is the model's **reconstruction**, which the
fact gate would have to re-verify from scratch. It is a stylistic/structural prior, not a constraint.

### 4.1 "Structure enters as pixels" — the nearest patterns in the frontier set `HIGH`

None of the frontier models has a geometry channel, but two accept *your rendered frame* in a way that
is more useful than a prompt. Ranked by fidelity:

1. **Runway Aleph 2.0 — video-to-video only.** Pass your deterministic Blender render as `videoUri`
   and have Aleph restyle/relight/edit it, with up to **5 timestamped `keyframe` images** pinning
   appearance at chosen seconds and an optional `range` window limiting the edit. Input 2–30 s,
   480p–1080p, ≤10 cuts; `targetAspectRatio` includes `9:16`. **$0.28/s, 56-credit minimum.**
   This is the closest thing to "structure in" in the entire frontier set — but it still regenerates
   pixels, so it can move geometry, and every frame still needs fact-gate treatment.
   `UNVERIFIED:` Aleph's output resolution and fps are not documented at all.
2. **Veo 3.1 — the only model in the set with BOTH first and last frame** (`image` + `lastFrame`, and
   `lastFrame` must be combined with `image`). That is genuinely useful for locking the start and end
   pose of a mechanism; the interpolation between them is model-invented. 9:16 works up to 4K — the
   strongest vertical output here — but 1080p/4k force 8 s, and native generations are **4/6/8 s
   only**, a poor fit for 6–12 s shots. Extension past 8 s is **720p-only** and accepts only prior Veo
   output.
3. **Runway Gen-4.5's real differentiator is delivery format, not control.** `outputFormat` supports
   `prores`, `png_sequence`, `hdr10`, `hlg`, `sdr_rec709_10bit`, a 12-bit 4:4:4 PQ master, HDR ProRes,
   16-bit PNG sequences, half-float OpenEXR, and **scene-referred ACEScg EXR** with a colorimetry
   sidecar. For a Blender-composited pipeline that is unusually well-aligned with `ROADMAP.md`'s
   ACEScg intent — but it is output-side only, Gen-4.5 itself is capped at **720p/24–25 fps/2–10 s**,
   and each format carries a **+5 to +40 credits/s** surcharge.

**Provenance is standardised here, unlike generation:** Veo embeds **SynthID** in all output; Sora
embeds **C2PA metadata** plus (at launch) a visible watermark. Relevant to `ROADMAP.md` §11.

---

## 5. Tier 3 — no geometric control (the negatives)

The entire control surface is: text, images (frame or reference roles), video (reference or
motion-drive), audio. **No depth, normal, canny/edge, segmentation, pose keypoint, motion brush,
camera-trajectory, scene graph, mesh, USD, glTF, STEP or document input.**

| Model | Confirmed absent | Note |
|---|---|---|
| **Wan 3.0 / 3.0 Prime** | verified from Alibaba's own capability table | Hosted only; no weights |
| **Seedance 2.0 / Fast / Mini** | verified from BytePlus API ref | Fps **24** |
| **Kling 3.0 / 3.0 Omni** | verified | Motion Control 3.0 is video-driven mocap requiring "one person", "head clearly visible" — unfit for machinery, and it *forbids* camera movement in the motion video |
| **MiniMax H3 / H3 Max / Hailuo legacy** | verified | First/last-frame and reference roles are **mutually exclusive** |
| **HunyuanVideo 1.5** | no ControlNet/depth/pose — T2V/I2V only | **Licence void in EU/UK/South Korea** |
| **Bernini-R** (ByteDance) | reference images/videos only | Structure preservation via v2v only |
| **Google Veo 3.1 / Fast / Lite** | ≤3 `referenceImages` (style/content) + `image` + `lastFrame` + `video` (extension only) | **Only model in the set with BOTH first and last frame.** 4/6/8 s native; 24 fps |
| **OpenAI Sora 2 / 2 Pro** | 1 `input_reference` (opening frame only); **no last frame** | **API shuts down 2026-09-24 with no replacement.** Blocks human-face inputs |
| **Runway Gen-4.5** | 1 `promptImage` (`position: "first"`) only; no last frame | **Verified by keyword-searching the full published `openapi.json` (58 ops)** for depth/normal/canny/pose/segmentation/mask/brush/trajectory/mesh/glTF/USD/STEP/ControlNet/OpenPose/LiDAR → **zero hits.** 720p max |
| **Alibaba HappyHorse 1.1** | no geometric parameter across all four task types | **No `last_frame` at all**; 24 fps; **`watermark` defaults `true`** stamping "Happy Horse" |
| **Luma `ray-3.2`** | `video_edit` only: `depth/normals/pose/trajectory/face` | **Enable-flags, not data inputs** — the model *derives* them from your source video. **No seed** ("Not deterministically"); 24 fps; `duration` only `"5s"`/`"10s"` |
| **xAI Grok Imagine Video** (`grok-imagine-video`, `-1.5`) | verified against the machine-readable `openapi.json` — **zero** geometric matches | T2V invents its own first frame; **fps undocumented** |
| **PixVerse V6 / C1** | no `brush` matches anywhere; **no Motion Brush in the API** | Mimic requires "a person as the primary focus"; masks are **server-generated**, not uploadable |
| **Vidu Q3 / Q2 / Q1** | EN+CN sweep, all 7 video endpoints — **zero** geometric matches | Only `movement_amplitude`, which **"does not take effect on q2/q3"**; 24 fps |

**Also settled, and relevant:** **30 fps is available nowhere.** Seedance documents 24 fps explicitly
(its `frames` formula is `25 + 4n`); Kling and MiniMax do not document output fps at all.

---

## 6. The Wan open-weights question — RESOLVED `HIGH`

The claim "the last downloadable Wan is 2.2, and 2.5+ never shipped weights" is **correct**; the claim
that 2.6/2.7 are open is **false**. Five independent checks on 2026-09-18:

```bash
curl "https://huggingface.co/api/models?author=Wan-AI&sort=createdAt&direction=-1"
# 27 repos. Newest: Wan2.2-Animate-2-14B (2026-08-06). Nothing numbered above 2.2.
```

1. `author=Wan-AI` → 27 repos, **nothing above 2.2**.
2. Hub-wide search: `Wan2.7` → 0 results; `Wan2.6`/`Wan2.5` → only **empty squatter repos**
   (`.gitattributes` only, 0 downloads).
3. GitHub `orgs/Wan-Video` → 6 repos, **no 2.5/2.6/2.7/3.x**, so no inference code either.
4. Official `Wan-Video/Wan2.2` README: *"licensed under the Apache 2.0 License. We claim no rights
   over the your generated contents."*
5. **Decisive:** ComfyUI's router schemas list `wan2.5-i2v-preview`, `wan2.6-t2v/i2v/r2v`,
   `wan2.7-*`, `wan3.0-video` — but all require `BearerAuth`/`ApiKeyAuth` against `/v2/models/wan/...`.
   They exist **only as paid hosted API models.**

**Consequence: Wan 2.2 is the ceiling for local, licence-clean work.** Do not plan around 2.5+.
`INFERENCE:` the false "2.7 is Apache 2.0" claim originates from affiliate/SEO domains; the release
announcements never said "open source," and SEO filled that silence with the prior that Wan = open.

---

## 7. The three practical walls

### 7.1 The depth convention does not match Blender's `HIGH` — the critical finding

The stock `VideoToDepth` preprocessor (VideoX-Fun `comfyui/annotator/nodes.py`) does, in source:
resize-with-pad to **512** → run **ZoeDepth** (`ZoeD_M12_N.pt`) → `vmin = percentile(depth, 2)`,
`vmax = percentile(depth, 85)` → `depth -= vmin`, `depth /= vmax - vmin` → **`depth = 1.0 - depth`** →
`* 255.0` as **uint8**, replicated to RGB.

So the expected input is **8-bit, near/far-inverted, per-frame 2–85-percentile-normalised** relative
depth. **A raw Blender Z-pass (linear camera-space, physical units) will not match** and must be
remapped into this convention.

`INFERENCE:` because `vmin`/`vmax` are recomputed **every frame**, a shot whose depth histogram changes
over time (a dolly-in, an object entering frame) gets a *different* mapping each frame — producing
depth-map "breathing"/contrast pumping the model may faithfully reproduce. **If you supply your own
Blender depth you can normalise once across the whole shot and avoid this entirely.** That is a
concrete, measurable advantage of the deterministic pipeline.

Pose format is OpenPose-style via DWPose ONNX (`yolox_l.onnx` + `dw-ll_ucoco_384.onnx`). Canny is
`cv2.Canny` on grayscale with integer thresholds.

### 7.2 Off-bucket resolution and frame rate `HIGH`

Wan Fun Control is trained at **512/768/1024** multi-resolution, at **16 fps** (A14B, 81 frames) or
**24 fps** (5B, 121 frames). Brunel targets **1080×1920 @ 30 fps** — outside the trained bucket
entirely on both axes.

`INFERENCE:` generate at a trained bucket (e.g. 768×1024 or 576×1024), then upscale and retime to
1080×1920@30 in the deterministic pipeline, rather than generating out-of-distribution.

### 7.3 VRAM `HIGH`

| Path | Fits a 3080 (10–12 GB)? |
|---|---|
| **Wan2.1-VACE-1.3B** | **Yes** — **8.19 GB**, official |
| Wan2.2-Fun-5B-Control | **Uncertain** — official says **24 GB**; ComfyUI claims 8 GB with offloading. Test it |
| Wan2.2-Fun-A14B-Control | No — ~20–21 GB fp8 |
| Wan VACE 14B (self-host) | No — but the **hosted** route removes this |
| LTX-2 19B / 2.3 22B | **Questionable.** fp8 tensor cores are Ada/Hopper; **nvfp4 is Blackwell-only** — both may fall back or fail on Ampere. Test before committing. |
| HunyuanVideo 1.5 | Official minimum **14 GB** with offloading |
| Cosmos-Transfer2.5-2B | No — **65.4 GB** |

---

## 8. Licence and lock-in

| Route | Output commercial? | Training on your inputs | Note |
|---|---|---|---|
| **Wan 2.2 (open)** | **Yes** — Apache 2.0, *"we claim no rights over your generated contents"* | N/A (self-host) | Cleanest terms in this document |
| **Alibaba Wan VACE (hosted)** | Yes, per Alibaba service terms | Model Studio collects user content | No warranty on generated content; AI labels non-removable |
| **Kling 3.0** | **Yes — unrestricted**; IP in output stays with you | **Explicitly does not train on your data** | 30-day prompt logging; output URLs purged at 30 days; liability capped at 6 months' fees |
| **LTX-2 / 2.3** | Yes **only under $10M revenue** | — | Derivatives must ship under the same licence |
| **MiniMax** | Yes | — | **Contractual AI-labelling obligation** ("prominent mark") |
| **HunyuanVideo 1.5** | Yes, but **only inside the Territory** | — | **Void in EU / UK / South Korea**; §5(c) reaches *outputs* |
| **BytePlus / Seedance** | Yes | **UNVERIFIED** — ToS grants a broad licence over uploaded data; **US$500 aggregate liability cap** | No explicit no-training clause found; worth a lawyer's read |
| **xAI Grok Imagine** | **Yes — strongest in the set** | **"xAI never trains on your API inputs or outputs without your explicit permission"** | Customer owns Output "in perpetuity"; xAI assigns all rights. **Contract under Enterprise terms** — the consumer ToS is far broader |
| **Runway** | Yes — "does not restrict your commercial use of your Outputs" | **Trains on Inputs *and* Outputs** — perpetual, irrevocable, transferable licence | Weakest terms here. Also requires apps to "prominently display 'Powered by Runway'". A real problem for unpublished CAD-accurate renders |
| **Luma** | Yes — requires an active paid subscription permitting it | **Contradictory:** API Terms §10 promises no training; the pricing table says pay-as-you-go "No-train guarantee: **No**"; general ToS §4.2(a) licenses Input for training | Get it in writing before feeding hand-verified geometry |
| **Vidu** | Yes — "We don't restrict your use for commercial purposes" | No training clause found | **AI label mandatory and non-removable** |
| **PixVerse** | **Contradictory:** §5.3 says commercial use "not restricted"; §1.4 prohibits API use for "commercial profit-making activities" without written authorization | §5.2 grants them rights for "technological improvement" | Get written clarity for a monetised channel |

**Deprecation is documented, not hypothetical:** Sora 2's API sunsets **24 September 2026**; ByteDance
rotates version-suffixed model IDs; Wan 2.5+ weights never shipped despite being widely described as
open. **Wan 2.2's Apache 2.0 weights are the only genuinely durable asset in this table** — everything
else is a service that can change terms or disappear.

---

## 9. The standards gap (unchanged, and now confirmed at API level)

**There is no standard for video generation.** Standards exist on both sides:

- **Scene input:** OpenUSD, glTF 2.0 (ISO/IEC 12113), MaterialX, Alembic, OpenVDB, OSL; and for
  engineering, STEP (ISO 10303), JT (ISO 14306), QIF (ISO 23952), IFC (ISO 16739).
- **Diagram semantics:** **ISO 128** (technical drawing), **ASME Y14.3** (orthographic/pictorial,
  **including section and exploded views**), **ASME Y14.5** (dimensioning/tolerancing), **ISO 10209**
  (vocabulary defining *section*, *cutaway*, *exploded view*), **S1000D** (technical publications,
  illustration types and callout conventions).
- **Output:** OpenEXR, ACES (SMPTE ST 2065), OpenColorIO, OpenTimelineIO, IMF (SMPTE ST 2067).
- **Provenance:** C2PA Content Credentials; EU AI Act Art. 50 and the European Commission's Code of
  Practice on Marking and Labelling AI-Generated Content (June 2026).

**Not standardised:** video-generation interchange, vendor-neutral video APIs, **and the conditioning
interface itself.** Depth/canny/pose are a *de facto* ControlNet convention with no ISO/IEC backing —
and as §7.1 shows, even the *de facto* convention is inconsistent enough that Blender's depth must be
remapped to match one implementation.

**The precedent that makes the gap legible:** USD scene + Hydra render delegate lets any renderer plug
into any scene through one abstraction. There is no Hydra equivalent for generative video, because
Hydra requires a declarative scene description and diffusion models do not consume those. **The moment
intent is expressible as a scene graph you are in standards territory; the moment it needs a diffusion
model, you leave it.**

---

## 10. The direction of travel — is the market moving toward geometric control?

**Short answer: the market is bifurcating, not converging.** Two camps are moving in opposite
directions, and they have only just begun to touch.

### 10.1 The creative frontier is moving *away* from control `HIGH`

- **Wan closed as it improved.** Wan 2.1/2.2 shipped open weights *with* control (Fun Control, VACE,
  Uni3C). **2.5 shipped no weights at all.** 3.0 is API-only **with no geometric parameter
  whatsoever**. Geometric control survives only in the *legacy* tier (`wan2.1-vace-plus`, 5 s fixed).
- **LTX regressed on structural control at the frontier.** LTX-2 shipped Depth / Pose / Union
  IC-LoRAs. **LTX-2.5's IC-LoRAs are *editing* tasks** (Deblur, Colorization, Clean-Plate,
  Day-To-Night), and the control path documented for 2.5 is *reusing 2.3's LoRAs*.
- **Runway has no plan.** Its full published `openapi.json` — 58 operations — contains zero
  depth/pose/edge/segmentation/trajectory/mesh parameters.
- **Sora's API is withdrawn** 2026-09-24 with no replacement.

Instead, the frontier's control is migrating to **loose reference conditioning**: images, reference
video, documents. Wan 3.0's `reference_video` edit/extend, Runway Aleph 2.0 (video-to-video only),
Luma `video_edit`, Seedance's clay-render-as-`reference_video`. **The emerging de facto interface is
"hand it a video, get a restyled video" — not "hand it a scene."**

### 10.2 Physical AI is moving *toward* control, and it has the money `HIGH`

- **NVIDIA Cosmos** is the clearest directional signal: a sustained multi-generation investment in
  exactly this capability — **Transfer 1 → Transfer 2.5 → Cosmos 3** (31 May 2026). Transfer 2.5 is
  documented as *"Multi-control video generation supporting RGB, depth, segmentation, edge, and
  visual blur."*
- Cosmos 3 is **open weights under OpenMDW-1.1**, Mixture-of-Transformers, at 4B/16B/64B, with
  **9:16 support, 10/16/24/30 FPS, 5–300 frames**, and **action conditioning including camera motion
  (9D)**.
- There is a **hosted endpoint** (`cosmos-transfer2.5-2b` on build.nvidia.com) — this is not
  self-host-only.
- NVIDIA's own framing ties it to Omniverse: *"Omniverse builds the simulated environment; Cosmos
  provides the foundation models. **Omniverse renders can be fed into Cosmos Transfer** to produce
  photorealistic synthetic data."* That is a vendor-sanctioned DCC→control pipeline.

### 10.3 The two camps are starting to touch `HIGH`

The **NVIDIA Cosmos Coalition**, launched alongside Cosmos 3, has founding members **Agile Robots,
Black Forest Labs, Generalist, LTX, Runway and Skild AI**. Two of those — **LTX and Runway** — are
creative-frontier vendors.

`INFERENCE:` geometric-control capability is being built in the physical-AI camp, and the creative
vendors are being pulled toward it by partnership rather than building it themselves. That makes the
Coalition membership list the single best forward indicator to watch.

### 10.4 The research frontier is *teaching* geometry, not just conditioning it `MEDIUM`

- **World-R1** (arXiv 2604.24764, Jan 2026, Zhejiang University + Microsoft Research) aligns video
  generation to 3D constraints via **reinforcement learning** (Flow-GRPO) using 3D-foundation-model
  rewards (Depth Anything 3 → 3D Gaussian Splatting) and VLM critics — improving 3D consistency by
  **10.23 dB PSNR** with *no architectural change*. **Its backbones are Wan 2.1 1.3B and 14B.**
- **SCoPE** (TencentARC, Aug 2026) — new Apache-2.0 camera-trajectory control.
- **MiniMax H3 Fun ControlNet Union** (Aug 2026) — a new canny/depth/HED/MLSD/pose control union.

`INFERENCE:` the significance of World-R1's backbone choice is that **new geometric methods land on
the open Wan line first.** That is the substrate to build on — not the 5 s-capped legacy API.

### 10.5 Who to follow

| | Direction | Evidence | Call |
|---|---|---|---|
| **NVIDIA Cosmos** | **Toward** — it is the product thesis | Transfer 1→2.5→Cosmos 3; OpenMDW-1.1 weights; hosted control endpoint; Omniverse→Transfer pipeline | **Primary** |
| **Open Wan (1.3B/14B) + research** | **Toward** — the substrate new methods use | Apache 2.0; sub-12 GB; World-R1's backbone; SCoPE and Uni3C build on Wan | **Build here** |
| **LTX / Runway** | **Ambiguous** — Coalition members | Coalition founding members, but their own frontier moved away from structural control | **Watch** |
| **Seedance / Kling / Veo / PixVerse / Vidu / HappyHorse** | **Away or flat** | No geometric parameter; no announced roadmap | **Do not wait on** |

### 10.6 The strategic read

**Do not adopt the legacy 5 s VACE API as the destination — adopt its input format.** The durable
move is to **rasterise the scene graph into the modalities every camp already accepts** — depth,
canny, per-part masks, bounding-box tracks, camera path. That input contract is the same for Cosmos
Transfer, Wan VACE and Wan-Fun, so it is **model-neutral and survives whichever vendor wins**.

Then build on **open Wan 1.3B/14B**: Apache-2.0, sub-12 GB, and the backbone the research community
post-trains geometric consistency onto. That is the opposite of a legacy bet — it is the substrate.

Track **Cosmos** as the vendor most likely to deliver genuine geometric control at usable cost, since
it is the only one whose product thesis *is* geometric control.

### 10.7 Why not Cosmos? — the Wan/Cosmos tradeoff, stated honestly

If Cosmos is the vendor whose thesis is geometric control, why build on open Wan? **Not purely cost —
only one of five reasons is money, and on licence Cosmos is actually *better*.**

**First, the correction: Cosmos's licence is the cleanest in this entire document.** Cosmos 3 weights
ship under **OpenMDW-1.1**, a Linux Foundation permissive licence which grants permission *"to deal in
the Model Materials without restriction, including under all copyright, patent, database, and trade
secret rights"* — and, decisively for a monetised channel:

> *"This agreement does not impose any restrictions or obligations with respect to any use,
> modification, or sharing of any outputs generated by using the Model Materials."*

That is **stronger than Apache 2.0** (which is silent on outputs), and far stronger than LTX's $10M
revenue cap or Hunyuan's territory ban. Caveat: licence terms vary per model card — `Cosmos-H-Surgical`
carries a commercial/non-commercial clarification — so check each card.

**Then the four real reasons, in order of weight:**

1. **Nothing in the Cosmos line runs on your hardware.** `Cosmos-Transfer2.5-2B` requires **65.4 GB
   VRAM**. Cosmos 3 tiers are Edge 4B (Jetson AGX Orin / Thor / RTX PRO 6000), Nano 16B (RTX PRO 6000
   / H100 / B200) and Super 64B (H200 / B200 / GB200). A 10–12 GB 3080 is out of every tier, so Cosmos
   means **renting cloud GPUs for every iteration**.
2. **The iteration loop collapses, and Brunel's method depends on it.** Transfer 2.5 at 720p/16 fps/
   93 frames: **B200 286 s, H100 NVL 719 s, H100 PCIe 870 s, H20 2,327 s** — up to ~39 minutes for a
   5-second clip. The repo's whole discipline is "storyboard cheap, iterate, then commit"; a 39-minute
   loop kills it. `Wan2.1-VACE-1.3B` does 480p/5 s in ~4 minutes on consumer hardware.
3. **It cannot reach your delivery resolution.** Cosmos 3 supports **256p / 480p / 720p — no 1080p.**
   So it misses 1080×1920 as well, and would need upscaling. (9:16, 30 fps and 5–300 frames *are*
   supported, and Transfer 2.5 ships a 720p→4K upscaler.)
4. **The training distribution is the wrong world.** Cosmos's own cookbook recipes are *"photorealistic
   agricultural images for robot perception training"*, *"Sim2Real for simulator videos"* (CARLA) and
   *"robotics domain adaptation"*, and its action conditioning is robot embodiments (DROID, UR,
   dual-arm, humanoid). Its aesthetic target is **photoreal modern real-world simulation**. Brunel's
   Mode A wants 1825 London — Victorian brick, gaslight, river — which is not in that distribution —
   and Modes B/C want a *diagrammatic* register, which is the opposite of photoreal. Cosmos has no
   stylisation path.

`INFERENCE:` there is one genuine point of contact. Transfer 2.5's **Sim2Real recipe takes simulator
renders and makes them photoreal** — that *is* a DCC→Cosmos pipeline, and it would suit a
photoreal Mode A. What it will not do is give you a stylised, engraved-diagram look.

**The honest framing — it is not either/or, and the exporter is what makes it not matter:**

| | Bet | Risk |
|---|---|---|
| **Open Wan 1.3B/14B** | Legal + technical **permanence** — Apache 2.0 weights that cannot be withdrawn; the backbone new geometric research post-trains on | Its owner **abandoned control** at 2.5. You would be building on a line the vendor left behind |
| **NVIDIA Cosmos** | Strategic **trajectory** — the only vendor actively improving geometric control, licence-clean, with a documented DCC→control recipe | **Datacenter hardware, 39-minute clips, 720p ceiling, wrong distribution** |

**The resolution: because you are rasterising the scene graph into neutral control passes, the same
depth / edge / mask / bbox-track data feeds either backend.** Build on Wan now for the iteration loop;
keep the exporter model-agnostic so Cosmos is a config change rather than a rewrite. And test Cosmos
cheaply via the hosted `cosmos-transfer2.5-2b` endpoint on build.nvidia.com — one shot, no datacenter.

**What would flip the recommendation to Cosmos:** a stylised or DCC-artistic transfer checkpoint; a
lower hardware tier (RTX PRO / consumer); materially better hosted throughput; or evidence that
conditional generation closes the MechVerse mechanical-fidelity gap that uncontrolled generation does
not.

### 10.8 Hosted Cosmos, and the construction-simulation reframe `HIGH`

**Hosted Cosmos exists, and the multi-control model specifically has a free endpoint.** From
`build.nvidia.com` (fetched 2026-09-18):

| Endpoint | Description | Access |
|---|---|---|
| **`cosmos-transfer2.5-2b`** | *"Generates physics-aware video world states for physical AI development using text prompts and **multiple spatial control inputs** derived from real-world data or simulation."* | **Free Endpoint**, plus "Download and Post-Train" |
| `cosmos3-nano` | Physics-aware video from text or image prompts | **Downloadable + Free Endpoint** |
| `cosmos3-nano-reasoner` | Physical-world VLM | **Downloadable + Free Endpoint** |

Beyond build.nvidia.com: Cosmos deploys as **NIM microservices** for cloud, data center or
workstation, with launch partners **Baseten, Classmethod, CoreWeave, Deep Infra, Microsoft Azure and
Nebius**. So the 65.4 GB VRAM barrier is a *self-hosting* barrier only.

**The exact `cosmos-transfer2.5-2b` contract:**

| | |
|---|---|
| **Control inputs** | **Up to four control videos**: **Canny edge, blurred RGB, segmentation mask, depth map**. Edge and blur can be auto-extracted from an RGB video alone |
| **Output** | **720P at 16 FPS**; same temporal length and resolution as the control input |
| **Input format** | Text (<300 words) + control video(s) as `.mp4` |
| **Frame lengths** | Multiples of **93 frames** perform best (93 ≈ 5.8 s, 186 ≈ 11.6 s, 279 ≈ 17.4 s at 16 fps) |
| **Critical constraint** | Multiple controls **must be derived from the same source video** with identical spatio-temporal dimensions |
| **Architecture** | Diffusion transformer (2.36 B params); control branches replicate transformer blocks and are combined via **spatiotemporal weight maps** |
| **Self-host** | 65.4 GB VRAM; Ampere/Blackwell/Hopper; BF16 only |
| **Latency (self-host, 720p/16 fps/93 frames)** | B200 286 s · H100 NVL 719 s · H100 PCIe 870 s · H20 2,327 s |

**NVIDIA's own stated limitations, verbatim:**

> *"...they struggle to generate long, high-resolution videos without artifacts. Common issues include
> temporal inconsistency, camera and object motion instability, and imprecise interactions. The models
> may inaccurately represent 3D space, 4D space-time, or physical laws... applying these models for
> applications that **require simulating physical law-grounded environments or complex multi-agent
> dynamics remains challenging**."*

**The reframe that resolves that — Cosmos Transfer is a *renderer*, not a *simulator*.** The physics
limitation only binds if you ask it to invent the world. Its actual job is to take control passes
**derived from a simulator you already trust** and make them photoreal — which is precisely the Sim2Real
recipe NVIDIA documents. **The simulation comes from your deterministic scene; Cosmos supplies the
photorealism.** That division of labour is exactly what a construction-site pipeline wants.

**This also supplies the scene-graph path §9 said did not exist**, via a three-step chain rather than
a single input:

```
USD / IFC / CAD  →  Blender or Omniverse  →  depth + segmentation + canny passes  →  Cosmos Transfer2.5
   (scene graph)        (authoritative)            (1280×720, ×93 frames)              (photoreal)
```

The scene graph never enters the model directly — but it fully determines the output.

`INFERENCE:` for the stated direction (marketing video now; construction-site and engineering-project
simulation in one to two years) this makes **Cosmos the right long-term bet and not the wrong-domain
tool** §10.7 described. That section's four objections collapse to two:

| Objection in §10.7 | Status |
|---|---|
| Wrong training distribution (photoreal modern, not 1825 London) | **Void** — construction and industrial simulation *is* the target domain |
| 720p ceiling | **Void** — accepted |
| Datacenter hardware | **Largely void** — hosted endpoint, NIM, and six cloud partners |
| Iteration cost/latency | **Stands** — 286 s to 2,327 s per clip self-hosted; hosted latency unmeasured |

**Remaining caveats, all real:**

1. **The free endpoint runs under the NVIDIA API Trial Terms of Service**, with the model itself under
   the NVIDIA Open Model License. Free to *try* is not free to *ship* — verify commercial terms. Note
   also that **Cosmos licences differ across generations**: the Transfer2.5 card cites the NVIDIA Open
   Model License, while Cosmos 3's page cites **OpenMDW-1.1**. Check per model card.
2. **16 fps, not 24/30.** Plan a frame-interpolation step (RIFE/FILM) in the deterministic pipeline.
3. **Hosted-endpoint latency and rate limits are UNVERIFIED.** Self-hosted figures suggest this is not
   an interactive loop; storyboard cheaply and batch the photoreal pass.
4. **Vendor-admitted instability on long or high-resolution output.** Keep generations at the ×93-frame
   granularity and chain.
5. **Strategic tension worth naming:** if these videos market Demiton — whose brand standard is *"no
   fabricated UI as product"* and "every frame is the real product" — then photoreal *simulated*
   construction footage cannot carry a product claim. It can carry atmosphere. Keep the two registers
   separate, and keep claims on real footage (`ROADMAP.md` §11 already flags Instagram's AI-label risk).

---

## 11. Recommendation for Brunel

1. **Blender remains the renderer of record** for every shot the audience can measure — shot 4 (the
   shield in section), the cell cycle, exploded states, dimension callouts. No backend here can be
   trusted with them.
2. **If a generative backend is used, use it as a control-conditioned re-render of a Blender frame**,
   not as a source of structure. **Hosted Wan VACE** (`fal-ai/wan-vace-14b/depth`, ~$0.10/s) is the
   only option that is cheap, hosted, commercial, and genuinely depth-driven.
3. **Emit the depth map to VACE's convention, normalised once per shot** — not per frame (§7.1). This
   is the one place where the deterministic pipeline measurably beats the stock preprocessor.
4. **If self-hosting on the 3080, start with `Wan2.1-VACE-1.3B` — not the 5B.** Correction to an
   earlier draft of this document: the official `Wan-Video/Wan2.2` README says the **5B needs at
   least 24 GB** (with `--offload_model True` already applied), so ComfyUI's claim that it *"should
   fit well on 8GB"* is a **tooling-vendor claim the model's own owner does not support** — treat it
   as contingent, not safe. The only model in the survey with an owner-published sub-12 GB figure is
   **`Wan2.1-VACE-1.3B` at 8.19 GB**, Apache 2.0. It gives depth, pose, flow, scribble, masks,
   **`layout_bbox` / `layout_track`** and reference tasks, and `firstclip` chaining solves the 6–12 s
   need against a ~5 s native window. It has **no canny and no normal** — use the Wan-Fun family
   (`Wan2.1-Fun-V1.1-1.3B-Control`) for those.
5. **Budget for GGUF, not FP8.** `sm_86` has no FP8 compute path, so fp8 weights are a storage saving
   with zero speedup. `wanBlockSwap` also appears to have been **removed from current ComfyUI**, so
   the RAM-offload fallback may no longer exist in stock builds.
5. **Watch Wan Uni3C.** Point-cloud + camera-trajectory conditioning is the closest thing to handing
   over the scene itself. Experimental and unlocated today; worth a re-check each quarter.
6. **Never let the model invent engineering.** §5's negative list is the whole point of this document:
   the frontier models with the best aesthetics have no way to receive your geometry at all.
7. **Keep the model non-load-bearing.** If the backend disappears, the episode should lose polish, not
   existence. Prefer Apache 2.0 Wan 2.2 weights for anything you would be sad to lose.
8. **Expect to lose on mechanism fidelity whichever model you pick.** MechVerse puts the best model in
   the world at 2.91/5 on mechanical correctness, and finds perceptual quality uncorrelated with it.
   Your deterministic geometry is the mitigation, and the literature explicitly names the missing
   ingredient — "explicit representations of parts, joints, and dependency structures" — which is
   precisely what the Blender scene graph already holds. **That is the moat, not the renderer.**
9. **Do not put LTX-2.x on the 3080 shortlist** (32 GB official floor). Keep it as a rented-cloud
   option, or use the older 0.9.x line.
10. **Add SCoPE to the cloud shortlist** if you need real camera-trajectory control rather than Fun
    Camera's presets — Apache 2.0 with no territory clause, cloud-only at ~67 GB.
11. **For delivery-format work, Runway Gen-4.5's ACEScg EXR output is worth knowing about** even
    though its generation control is nil — but its training-on-inputs clause argues against feeding
    it unpublished work.

---

## 12. UNVERIFIED / could not confirm

| Item | Confidence | What would settle it |
|---|---|---|
| **Failure modes on mechanical/hard-surface subjects** | **RESOLVED by MechVerse** (§1) — best model 2.91/5; perceptual quality uncorrelated with mechanical correctness | Still worth a local test: condition on a Blender depth pass of the shield and measure structural drift against the source |
| Wan Uni3C checkpoint location, licence, VRAM, max resolution | UNVERIFIED | Locate the downloadable weights |
| Wan Fun Control **trajectory input format** | UNVERIFIED (capability is documented and demoed in `guiji.mp4`; no code path exposed it) | Read the example scripts |
| **LTX-2.x VRAM on a 3080** | **RESOLVED — not viable.** Vendor floor is **32 GB+**; recommended A100/H100 | — |
| LTX-2.5 licence text (2.3 = Jan 5 2026 `LICENSE-2`; 2.5 reportedly `ltx-2.x-community-license-agreement`, Aug 11 2026) | MEDIUM — treat as separate documents; both non-Apache with a **$10M revenue** commercial threshold | Fetch the 2.5 licence text |
| Whether any **structural** IC-LoRA exists or is planned for LTX-2.5 | **No** — target LTX-2.3 for control work; 2.5-native IC-LoRAs are editing tasks | Re-check the org listing |
| MiniMax H3 Fun ControlNet Union licence + minimum VRAM | UNVERIFIED | Vendor terms; benchmark |
| **SCoPE** — arbitrary trajectories vs named presets; VRAM; max resolution/duration | UNVERIFIED | Read the repo; benchmark |
| Whether **Ampere fp8** gives any speedup | **RESOLVED — no.** `torch._scaled_mm` needs ≥ 8.9 (Ada); NVFP4 needs Blackwell | — |
| BytePlus training-on-inputs | UNVERIFIED | Read ModelArk Service Specific Terms + Customer Agreement (ToS text was truncated) |
| **Alibaba commercial-use terms for *paid* (non-trial) inference** | **Material gap** — the restrictions located apply explicitly to *"trial services"*; no equally explicit paid-inference ownership clause was found | Verify before publishing a monetised episode |
| Exact pixel dimensions for 1080p 9:16 (Alibaba / Vidu / Luma) | INFERENCE only — ratios are named, dimensions are not | API response `width`/`height` on a real call |
| **LTX 9:16 dimension constraint** | MEDIUM-HIGH — width/height must be divisible by 32, so **1080 is invalid; use 1088×1920**. Frames must be 8n+1, so 30 fps never lands on whole seconds | Confirm against the LTX API docs |
| Whether **Wan 3.0 Prime** differs from standard beyond speed/price | MEDIUM — parameter parity inferred from shared documentation | Prime-specific API reference page |
| "Kling O3" | **Does not exist in the official API** — documented models are `kling-3.0-turbo`, `kling-v3`, `kling-v3-omni`, `kling-video-o1`, `kling-v2-6`, `kling-v2-5-turbo`. Reseller marketing only. | — |

---

## 13. Sources

Primary, fetched this session:

- [NVIDIA Cosmos-Transfer1](https://docs.nvidia.com/cosmos/latest/transfer1/) ·
  [Transfer2.5 model matrix](https://docs.nvidia.com/cosmos/latest/transfer2.5/model_matrix.html) ·
  [licence](https://docs.nvidia.com/cosmos/latest/license.html) ·
  [prerequisites](https://docs.nvidia.com/cosmos/latest/prerequisites.html) ·
  [Cosmos 3 model matrix](https://docs.nvidia.com/cosmos/latest/cosmos3/model_matrix.html)
- [Alibaba `wan2.1-vace-plus`](https://www.alibabacloud.com/help/zh/model-studio/wan2-1-vace-plus) ·
  [`wan2.2-t2v-plus`](https://help.aliyun.com/zh/model-studio/wan2-2-t2v-plus) ·
  [Wan3.0 video generation](https://www.alibabacloud.com/help/en/model-studio/wan3-video-generation-guide) ·
  [Model Studio service terms](https://help.aliyun.com/en/model-studio/bailian-service-notes)
- [fal.ai `wan-vace-14b/depth`](https://fal.ai/models/fal-ai/wan-vace-14b/depth/api) ·
  [`wan-vace-14b/pose`](https://fal.ai/models/fal-ai/wan-vace-14b/pose/api)
- [ComfyUI Wan Fun Control](https://docs.comfy.org/tutorials/video/wan/wan2-2-fun-control) ·
  [WanUni3CControlnetApply](https://docs.comfy.org/built-in-nodes/WanUni3CControlnetApply) ·
  [LTX-2](https://docs.comfy.org/tutorials/video/ltx/ltx-2)
- [BytePlus create video task](https://docs.byteplus.com/en/docs/ModelArk/1520757) ·
  [Seedance 2.5 prompt guide](https://docs.byteplus.com/en/docs/ModelArk/2607689) ·
  [ModelArk pricing](https://docs.byteplus.com/en/docs/ModelArk/1544106)
- [Kling capability map](https://kling.ai/document-api/guides/capability-map/video) ·
  [Kling Motion Control](https://kling.ai/document-api/api/video/motion-control)
- [MiniMax video generation guide](https://platform.minimax.io/docs/guides/video-generation)
- Hugging Face: `Wan-AI` org listing, `alibaba-pai/Wan2.2-Fun-5B-Control`,
  `Lightricks/LTX-2-19b-IC-LoRA-Depth-Control`, `tencent/HunyuanVideo-1.5`
- [8frame, *Is Wan 3.0 Open Source?*](https://www.8frame.co/blog/is-wan-3-open-source) ·
  [wanimate.net, Fun Control vs VACE](https://wanimate.net/wan-fun-control-vs-wan-21-vace) ·
  [C2PA implementation guide](https://c2pa.org/a-new-implementation-guide-for-content-credentials/)
