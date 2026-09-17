# Generative AI 3D Tools — Assessment for a Monetised Historical-Engineering Instagram Channel

**Episode 1: Marc Brunel's Thames Tunnel tunnelling shield, 1825–1843**
**Assessment date: 17 September 2026.** All prices, versions and licence strings read live from vendor pages/raw licence files on this date.

**Operator constraints:** solo, Mac M1 16GB control plane (no Blender), Windows PC + RTX 3080 (10–12GB VRAM) render node, Blender + Python driven by an LLM agent.

**Confidence key:** **H** = read verbatim from a primary vendor file/page or raw licence text. **M** = vendor statement paraphrased, or credible secondary citing a primary. **L** = third-party/community claim, unverified.

> **⚠️ Three corrections that invalidate most published advice:**
> 1. **Hunyuan3D 3.0/3.1 have NO open weights.** They are a paid Tencent Cloud API. Open weights stop at **2.1**.
> 2. **The Hunyuan 3D commercial threshold is 1 million MAU, not 100 million.** The 100M figure belongs to Tencent's *LLM* (HunyuanCustom) licence. Several popular ports and blog comparisons repeat the error.
> 3. **Neither TRELLIS nor TRELLIS.2 fits a 10–12GB RTX 3080** at vendor settings. TRELLIS.2's official floor is 24GB. The only realistic local 3080 path is ComfyUI's INT8 ConvRot checkpoint (5.25GB) plus tiled decode.

---

## 1. THE SHORT ANSWER

| Need | Verdict |
|---|---|
| **Cheapest reliable textured asset via API** | **Tripo H3.1** — $0.30/image-to-3D with texture; $0.45 with quads. Real Python SDK. |
| **Best overall product surface** | **Meshy** — official free Blender addon (Pro+), quad remesh to 300K, 8K textures, MCP + CLI, 3D Agent. |
| **Only licence that is unambiguously safe** | **TRELLIS / TRELLIS.2 — MIT for both code and weights.** No territory clause, no MAU threshold. |
| **Local inference on the 3080** | **TRELLIS.2 via ComfyUI native nodes + INT8 checkpoint.** Hunyuan3D on 12GB is shape-only. |
| **Run locally on the M1 16GB** | **Don't.** M4 Pro 24GB takes 5.7 min shape + 8.5 min texture *with ~8GB of swap*. 16GB will thrash or die. |
| **Precision hard-surface / the shield itself** | **None of them. Model it by hand in Blender.** |
| **Reverse-engineering a part into CAD** | **Backflip AI** — but only "moderate-complexity 3-axis CNC milled and turned parts". |

---

## 2. TRIPO AI (tripo3d.ai / developers.tripo3d.ai)

### 2.1 Model versions (H)
| Model | Version string | Speed | Face limit |
|---|---|---|---|
| **Tripo H3.1** (flagship, default) | `v3.1-20260211`; alias `tripo-v3.1` | ~40s no texture / **~120s with texture** | up to 2,000,000 |
| Tripo P2 (low-poly) | `P2-20260801` | — | tri 48–50,000; quad 48–25,000 |
| Tripo P1 | `P1-20260311` | ~10s / ~60s | 48–20,000 |
| Tripo v3.0 | `v3.0-20250812` | — | 1,000,000 tri |
| Tripo v2.5 | `v2.5-20250123` | — | 500,000 tri |
| **Texture models** | `v3.5-20260815` (Sept 2026), `v3.0-20250812`, `v2.5-20250123` | `fast`/`standard` same size+cost | — |
Source: [developers.tripo3d.ai/en/models/v3-1](https://developers.tripo3d.ai/en/models/v3-1), [changelog](https://developers.tripo3d.ai/en/docs/changelog)

**P2 is only 2 months old** (Aug 2026) and is the only P-series with `quad`; P1 rejects `quad`/`smart_low_poly`/`generate_parts`/`geometry_quality` with HTTP 400.

### 2.2 TripoSR vs TripoSG vs the commercial product — NOT a version ladder (H)
- **TripoSR** (Mar 2024, VAST + Stability AI): image-to-3D only, LRM-based, **<0.5s on A100**, ~6GB VRAM, **MIT**. Vertex colours or `--bake-texture`. [github.com/VAST-AI-Research/TripoSR](https://github.com/VAST-AI-Research/TripoSR)
- **TripoSG** (Mar 2025, VAST): 1.5B rectified-flow MoE Transformer + SDF VAE, 2M image–SDF pairs, **≥8GB VRAM**, image-to-3D **shape only** (no PBR pipeline). Claims parity with Tripo 2.0. arXiv 2502.06608. **HF model card says `License: mit`** (H, from [HF VAST-AI/TripoSG](https://huggingface.co/VAST-AI/TripoSG)).
- **Neither is the commercial flagship.** The paid product is the closed H/P-series at `openapi.tripo3d.ai/v3`. The open models give geometry only — no PBR texturing, no retopology service, no rigging, no SLA.

### 2.3 API pricing (H) — **1 credit = $0.01 USD**
| Operation | Credits | USD |
|---|---|---|
| Image to 3D — H3.1 no / standard / detailed texture | 20 / 30 / 40 | $0.20 / $0.30 / $0.40 |
| Text to 3D — H3.1 no / standard / detailed | 10 / 20 / 30 | $0.10 / $0.20 / $0.30 |
| Multiview to 3D — H3.1 no / standard / detailed | 20 / 30 / 40 | $0.20 / $0.30 / $0.40 |
| Image/Multiview to 3D — P2 no / standard / detailed / extreme | 100 / 110 / 120 / 130 | $1.00 / $1.10 / $1.20 / $1.30 |
| **Retopology v2.0 (Smart)** | 30 | $0.30 |
| Retopology v1.0 (Basic) | 10 | $0.10 |
| Texture Fast / Standard / HD / 8K Ultra | 10 / 10 / 20 / 30 | $0.10 / $0.10 / $0.20 / $0.30 |
| Auto Rig | 25 | $0.25 |
| Segmentation (model / image) | 55 / 85 | $0.55 / $0.85 |
Source: [developers.tripo3d.ai/en/pricing](https://developers.tripo3d.ai/en/pricing)

**Stackable add-ons (H):** HD Texture +10, 8K Ultra Texture +20, **HD Geometry Quality +20, Quad Mesh +5, Smart Low-poly +10, Generate Parts +20.**
→ **Image-to-3D, detailed texture, quad output = 40 + 5 = 45 credits = $0.45.**

**Billing (H):** credits frozen at task creation, **returned on failure** — failed generations are free. `pbr: true` **forces** `texture: true`.

**Subscription tiers (Studio, 2026-09) (H):** Free $0 (200 cr, **public + non-commercial**, exports capped at 15 of the *v2.5* model/month); Pro $20/mo (3,000 cr, 10 concurrent); Max $90/mo (25,000 cr, 100 concurrent); Team $55/seat/mo annual (card also shows $110 — unresolvable, **L**).
*Secondary source (July 2026) lists Pro $19.9 / Max $89.9 / Team $109.9 — superseded.* Credit packs: $10→1,000 cr ($0.0100); $100→12,000 cr ($0.0083); $1,000→130,000 cr ($0.0077).

### 2.4 Python SDK (H)
**Yes, official: `pip install tripo3d` (v0.4.2, 1 Jul 2026, MIT, "Tripo Development Team").**
**But:** it is *"V2 + limited V3"* — the main client targets `https://api.tripo3d.ai/v2/openapi`; V3 coverage only for segmentation. Full V3 SDKs exist for **JS/TS, Go, Rust, Java**. REST base: `https://openapi.tripo3d.ai/v3`, Bearer auth, async (`POST` → `GET /v3/tasks/{id}`), webhooks. Docs: [developers.tripo3d.ai/en/docs/api-reference](https://developers.tripo3d.ai/en/docs/api-reference).

### 2.5 Topology & retopology (H)
`POST /v3/mesh/decimate`:
- **v2.0 "Smart Retopology" (30 cr)** — P-series AI model, rebuilds clean topology with edge preservation. `face_limit` optional: tri 500–20,000 / **quad 500–10,000**. Supports `quad`, `bake` (default true), `part_names`. Output GLB.
- **v1.0 "Basic Decimation" (10 cr)** — pipeline decimation. `face_limit` required: tri up to 2,000,000 / **quad up to 150,000**. No `bake`.
**Quads: yes** — `quad: true` at generation (forces FBX; default 10,000 quads) and in both retopo tiers. Guidance in docs: "Game-ready 50,000–100,000; Web/mobile 10,000–50,000."

### 2.6 PBR output (H)
**Maps: `base_color`, `metallic`, `roughness`, `normal`** (verbatim from the `pbr` parameter description).
Resolution: `texture_quality` = `fast` | `standard` | `detailed` | `extreme`; **`extreme` = 8K**. Standard/detailed pixel sizes **not published (L)**. Free tier capped at 4K, Max unlocks unlimited 8K. `export_uv` (default true) controls UV unwrap at generation.
**Normal map baked? → UNVERIFIED (L).** Tripo's `bake` flag means *"Bake advanced material effects into base textures"* (material flattening) and retopology's `bake` = texture transfer onto low-poly. Neither is a documented high-poly→low-poly **normal** bake. **Treat "normal map is baked" as unsubstantiated.** *What would settle it: generate a detailed-texture asset, inspect whether the normal map correlates with silhouette detail absent from the base colour.*

### 2.7 Licence — VERBATIM (H)
**"Terms of User Agreement", [tripo3d.ai/terms](https://www.tripo3d.ai/terms), Last updated 11 July 2025. Entity: Holymolly Ltd (Hong Kong). Governing law: Hong Kong; HKIAC arbitration.**

> **§5.2.1 Free Users** — "For Users who access and use the Services free of charge ("Free Users"), **Tripo retains all rights**, including without limitation the rights to use, copy, reproduce, modify, adapt, publish, translate, create derivative works from, distribute, promote, transfer, authorize, license, optimize, derive revenue or other remuneration from, communicate to the public, perform, and display the Inputs and Outputs submitted or generated by Free Users, as well as all Intellectual Property rights arising therefrom."

> **§5.2.2 Paid Users** — "...and the consent and authorization to authorize the Company to use and display the Inputs and Outputs as may be necessary for Service provision on **royalty-free, perpetual, irrevocable, worldwide, non-exclusive** basis, Paid Users generally have all rights ... of the Inputs and Outputs ... **For the avoidance of doubt, Company will not use Inputs and Outputs as training data to train, validate, test, or improve any AI Technology.**"

- **Commercial use: paid only.** Free tier = "Public Models · Non-Commercial Use". §3.2 bars using Outputs "to create models or services that directly compete with Holymolly".
- **Ownership:** Free — Tripo owns. Paid — you hold rights, *but only "subject to"* granting Tripo the licence back.
- **Training on your content: paid = expressly excluded** (best-in-class among the paid tiers reviewed).
- **Indemnity: adverse.** §9 is user→Tripo only. §4: *"HOLYMOLLY ASSUMES NO LEGAL LIABILITY ARISING FROM OR RELATING TO THE GENERATED CONTENT."* Liability cap: **greater of 12 months' fees or $500**.
- **§3.2** bars reselling the Service to third parties without written consent — relevant if you productise.
- **Help Center vs ToS mismatch:** the Help Center states the licence-back applies when you set a model "public" and does *not* repeat the ToS's "as may be necessary for Service provision" limiter. **Flag for legal review.**

### 2.8 Latency (H, vendor-measured) 
H3.1 ~40s no texture / **~120s with texture**; P1 ~10s / ~60s; Rigging ~30s; Animation ~5s. **Contradiction:** the Studio pricing page simultaneously advertises *"Game-ready Assets in 2s"* — unqualified marketing inconsistent with the 40s spec. **Rate limit: 3 parallel tasks** (H and P series).

---

## 3. MESHY (meshy.ai)

### 3.1 Versions (H)
- **Meshy 7** (Aug 2026) — **Image-to-3D only**, with **Ultra Mode**; Meshy 7 Texture. Text-to-3D does **not** support Meshy 7.
- **Meshy 6** — current Text-to-3D model. **Meshy 6 Lite** — fastest/cheapest; *replaced Meshy 5 in the picker* (there is no live "Meshy 5").
- **Smart Topology** (Jul 2026) — image-to-3D low-poly with **native part segmentation**; **Meshy T2** (~2s, 5 cr) and legacy **T1** (~3 min, 20 cr).
- API enums: `meshy-6-lite`, `meshy-6`, `meshy-7`, `latest` (=7); Smart Topology `meshy-t2`.

### 3.2 Pricing (H) — official Help Center table
| Plan | Price | Credits/mo | Queue | Retries | Licence |
|---|---|---|---|---|---|
| **Free** | $0 | 100 | 1 | — | **CC BY 4.0** |
| **Pro** | **$20** | 1,000 | 10 | 4 | Private & CC BY 4.0 |
| **Premium** | **$40** | 3,000 | 30 | 12 | Private & CC BY 4.0 |
| **Ultra** | **$100** | 8,000 | 100 | 40 | Private & CC BY 4.0 |
| **Studio** | **$70**/seat | 5,500 pool (1x); $210→16,800 (3x); $350→28,000 (5x) | 60 | 24 | Private & CC BY 4.0 |
| Enterprise | Custom | Custom | 100 | 100 | Custom |
**API asset retention: 3 days (non-Enterprise); 14 days (Studio); forever (Enterprise).**
**⚠️ The Free tier cannot download at all** — the official table marks Model Downloads ❌ for Free. Combined with CC BY 4.0 attribution, **Free is evaluation-only**. New users: 50% off first month; 20% off annual. Credits **do not roll over** (top-up only restores you to the cap); purchased credit packs persist 1 year. There is also a regional **Starter** plan (250 cr).
*Annual per-month USD could not be read (client-rendered toggle) — **L**.*

### 3.3 API credits (H) — pay-before-you-go against the same balance
| API | Credits |
|---|---|
| Text to 3D preview | Meshy-6/low-poly 20; Meshy-7 20 (+5 Ultra); **Smart Topology T2 5**; other 5 |
| Text to 3D refine | 10 (2k/4k); 15 (8k) |
| **Image to 3D** | Meshy-6 20/30/35 (no/tex/8K); **Meshy-7 20/30/35 (+5 Ultra)**; T2 **5/15/20**; other 5/15 |
| Retexture | 10 (2k/4k); 15 (8k) |
| **Remesh** | **5** |
| Convert / Resize | 1 / 1 |
| **UV Unwrap** | **5** |
| **Auto-Rigging** | 5 |
| Animation | 3 per action (max 10 actions) |
Source: [docs.meshy.ai/api/pricing](https://docs.meshy.ai/api/pricing)

**⚠️ Official docs contradict each other (H that the contradiction exists):** the *webapp* pricing page lists **Remesh 0, Rigging 0, Animate 0**, and Meshy-7 image-to-3D at **25** credits, vs the API page's 5/5/3 and 30. **Get a written quote before budgeting.**
**Derived USD (M, Meshy publishes no per-credit rate):** Pro $20/1,000 = **$0.02/credit** → Meshy-7 image-to-3D w/ texture = **$0.60**; with Ultra = $0.70. Ultra tier $100/8,000 = $0.0125/credit → **$0.375**.

### 3.4 API & SDK (H)
REST, base `https://api.meshy.ai/openapi/v1`, Bearer `msy_...`. **20 req/s all paid tiers** (Enterprise 100). **No official Python SDK** — official surfaces are the **MCP server** (`@meshy-ai/meshy-mcp-server`), **CLI** (`npm i -g meshy-cli`), and `llms.txt`. Docs' Python examples are hand-written `requests`. PyPI packages are community. *What would settle it: an `meshy` package published by Meshy LLC on PyPI.*
CLI example from Meshy's own page: text-to-3D preview (20) + refine (10) = 30 credits, **224 s** end-to-end.

### 3.5 PBR, remesh, poly counts (H)
- **Maps: "Albedo, Normal, Roughness, Metallic"** + **emission** (only `meshy-6`, not at 8k). `enable_pbr` defaults **false**.
- **Resolution: `2k` (2048², default) / `4k` (4096²) / `8k` (8192²)** — base colour. 4k/8k unavailable on `meshy-6-lite`.
- **Normal map baked? UNVERIFIED.** `remove_lighting` ≠ a normal bake.
- **Remesh:** `POST /openapi/v1/remesh` — `topology: quad` ("quad-dominant") or `triangle`; **`target_polycount` 100–300,000, default 30,000**; `decimation_mode` 1–4 adaptive. **5 credits.**
- **Smart Topology path:** `model_type: smart-topology` + `meshy-t2` generates *directly* at the target face count, `target_polycount` **100–15,000, default 4,000**, triangle, natively separated parts.
- **Raw (pre-remesh) poly count: NOT PUBLISHED (L).** Only a docs example (~25K faces for a steampunk watch) and the 30,000 remesh default.
- Rigging: humanoid + quadruped, Mixamo-compatible, FBX.

### 3.6 Licence — VERBATIM (H)
**[meshy.ai/terms-of-use](https://www.meshy.ai/terms-of-use), "Last Updated: September 19, 2026" — note: 2 days in the future relative to this assessment. Meshy LLC, Sunnyvale CA. California law, AAA/ICDR arbitration, San Francisco County, class-action waiver.**

> **§3.2** — "Customers using Meshy's Services under the free plan, acknowledge and agree that **Provider owns all right, title, and interest, including all intellectual property rights, in and to the AI Customer Output** and grants such customer a license to the Assets under the Creative Commons Attribution 4.0 International License (CC BY 4.0)..."
> "Customers on a paid Meshy plan have the option to keep their User Content private... paid plan Customers grant Meshy **non-exclusive, royalty-free, worldwide license** to reproduce, distribute, and otherwise use and display the User Content..."

> **§2.9 (THE CRITICAL ONE)** — "Meshy may use Customer Inputs and Customer Outputs from **non Enterprise Customers** ... to **train, validate, test, or improve Services** unless otherwise agreed to in the Order."

> **§8** — "You agree to... defend, indemnify, and hold harmless Meshy... from and against any and all third party claims... **(no reciprocal indemnity to the customer)**."

- **⚠️ Meshy training on your content: YES for every plan below Enterprise.** Pro/Premium/Ultra/Studio are non-Enterprise. **This is the single most consequential difference from Tripo**, whose paid terms expressly exclude training. Enterprise can contract out via the Order.
- **Free-tier commercial use: yes with attribution** (CC BY 4.0), but you cannot download.
- **Ownership contradiction across Meshy's own pages:** the **ToS** vests free-plan output ownership in **Meshy** and contains **no express assignment to paid customers**; the **docs pricing page** says "Output Ownership: User owns output"; the **FAQ** says "you own the assets". **The ToS is the operative contract.** Flag for legal review.
- **§2.4** — output may carry watermarks/identifiers: *"You agree not to remove, alter, disable, or otherwise tamper with such identifiers."*
- **§2.5** — API output deleted after 3 days (non-Enterprise). **Download immediately.**
- **§3.3** — publishing to the Meshy Community page relicenses output under **CC0 1.0** (public domain). **Do not publish to Community.**
- **§2.6(xi)** — may not use output to train competing AI models. **§2.10** — features don't roll over; extra credits expire after 1 year. **§9** — liability capped at prior-12-months fees.

### 3.7 Blender addon (H) — **the differentiator**
**Official, free, [meshy.ai/integrations/blender](https://www.meshy.ai/integrations/blender)**, v0.6.1.
- **Requires a Meshy Pro account or above** to use the DCC Bridge. **Blender 4.2.6+** (tested 4.2.6, 5.0.1, 5.1.0, 5.2.0). **macOS and Windows only — Linux not supported.**
- One-click transfer via local HTTP bridge (GLB or ZIP), preserves materials/textures/colour attributes; **since v0.6.0 no API key needed**.
- Includes print-prep tooling that is genuinely useful as a **mesh-repair stage**: Make Manifold, Delete Small Pieces, normal correction, self-intersection/thickness/overhang analysis, Hollow, Scale to Volume/Bounds.
- **This is the only vendor Blender addon of the set that doubles as a topology-repair tool — and it works on the Mac control plane.**

### 3.8 Latency (H)
Text-to-3D ~1 min; Image-to-3D (Meshy 7) ~1–2 min; Ultra "about a minute, slightly longer"; **Smart Topology T2 ~2 seconds** (down from ~15); T1 ~3 min; Auto Split ~40s.

---

## 4. TENCENT HUNYUAN3D

### 4.1 What actually exists (H)
| Version | Date | Status |
|---|---|---|
| Hunyuan3D-1.0 | 2024-11 | open weights |
| Hunyuan3D-2.0 | 2025-01-21 | open weights |
| Hunyuan3D-2mv / -2mini | 2025-03-18 | open weights |
| **Hunyuan3D-2.1** | **2025-06-13** | **open weights + VAE encoder + all training code** |
| Hunyuan3D **2.5** | 2025-06-23 | **PAPER ONLY** (arXiv 2506.16504). No weights. |
| Hunyuan3D-Omni | 2025-09 | open, 3.3B, 10GB |
| Hunyuan3D-Part / HY3D-Bench | 2025-09 / 2026-02 | open |
| **Hunyuan3D 3.0 / 3.1 / Express** | **2026-02 onward** | **CLOUD API ONLY — no weights, no model licence** |

**Evidence 2.5/3.0 have no weights (H):** HF `tencent/Hunyuan3D-2.5` and `-3.0` return **401** (calibrated against a deliberately fake repo, which also 401s); GitHub `Tencent-Hunyuan/Hunyuan3D-2.5` and `-3.0` return **404**; HF full-text search returns zero. The "Update model card to Hunyuan3D 2.5" commit is on an **unmerged PR branch** (`refs/pr/54`); `main` contains no "2.5".
**Hunyuan3D 3.0 is served via [ComfyUI Partner Nodes](https://docs.comfy.org/tutorials/partner-nodes/hunyuan3d/hunyuan3d-3-0) and 3d.hunyuanglobal.com** (announced 2026-02-13) — Text/Image/Multi-view-to-3D plus paid **3D Parts Decomposition, UV Unwrapping, Smart Topology**. Requires login; *"in some regions, you may need to use a proxy service."*
**⚠️ Name collision:** "Hunyuan 3.0" is *also* Tencent's **LLM**. Do not conflate.
Also paper-only: **Hunyuan3D-Buffalo 1.0** (2026-08-05, arXiv 2608.02711).

### 4.2 Cloud API pricing (H unless noted)
**1 credit = ¥0.12 CNY.** HY-3D-3.0 and HY-3D-3.1: **15–60 credits = ¥1.8–7.2 (≈$0.25–1.01)** per generation. HY-3D-Express: **15–25 credits = ¥1.8–3.0 (≈$0.25–0.42)**. Failed generations not billed. Prepaid packs (1-year validity): 1,000 cr ¥100 (¥0.1/cr); 10,000 ¥980; 50,000 ¥4,750; 100,000 ¥9,000. **New users: 100 free credits, 365-day validity.** HY-3D-3.1 supports **eight-view** image-to-3D; Express completes **within 90 seconds**.
*USD figures are my conversion at ~7.1 CNY/USD — **M**.*

### 4.3 VRAM — the numbers that matter (H, verbatim from vendor READMEs)
- **2.0:** *"It takes 6 GB VRAM for shape generation and 16 GB for shape and texture generation in total."*
- **2.1:** *"It takes 10 GB VRAM for shape generation, 21GB for texture generation and 29GB for shape and texture generation in total."*
- Conflicting third figure: **ComfyUI docs** say *"the complete process (shape + texture) requires only 12GB VRAM."* **Does not reconcile with Tencent's 16GB.** Do not quote either as settled.
- Component sizes: `hunyuan3d-dit-v2-1` **3.3B / 7.37GB**; `hunyuan3d-paintpbr-v2-1` UNet **~2B / 3.93GB**; repo ≈15GB.

**Does it fit the RTX 3080?** **Shape: yes (10GB, tight — ~0.5–1.3GB slack with a monitor attached). Texture/PBR: no (21GB).** Community guidance is explicit: *"Do not instantiate `Hunyuan3DPaintPipeline` on a 12GB card."* `--low_vram_mode` exists (documented in Gradio invocations) but **no vendor statement that it brings 21GB below 12GB (L)**. Community escape hatch: `deepbeepmeep/Hunyuan3D-2GP` (`pip install mmgp`) streams the paint pipeline; unbenchmarked.

### 4.4 Hunyuan3D-Paint: PBR maps, resolution, normal provenance (H — read from source)
From `hy3dpaint/textureGenPipeline.py`:
```python
self.render_size = 1024 * 2      # 2048
self.texture_size = 1024 * 4     # 4096
self.dino_ckpt_path = "facebook/dinov2-giant"
self.realesrgan_ckpt_path = "ckpt/RealESRGAN_x4plus.pth"
```
- **Maps: `albedo` + `mr` (metallic-roughness).** Baked to UV space, masked regions inpainted.
- **Resolution: rendered at 2048, baked texture 4096.** Diffusion runs at 512/view in the documented example. Albedo and MR are **Real-ESRGAN ×4 super-resolved** before baking.
- **The normal map is RENDERED from mesh geometry, not predicted.** The pipeline calls `render_normal_multiview(...)` and `render_position_multiview(...)` — geometric renders used as conditioning. **There is no learned normal head.** This is a meaningful quality signal: the normal is *correct for the mesh you have*, including its errors.
- **2.0's paint model is RGB-only; 2.1's is the PBR one.** ComfyUI's blog claiming 2.0 does "PBR material generation" is loose marketing — trust the repo.

### 4.5 ComfyUI integration (H)
- **Native ComfyUI: `comfy_extras/nodes_hunyuan3d.py`** — shape only. Nodes: `EmptyLatentHunyuan3Dv2` (resolution default **3072**), `Hunyuan3Dv2Conditioning`, `Hunyuan3Dv2ConditioningMultiView`, `VAEDecodeHunyuan3D`, `VoxelToMesh` (`surface net`/`basic`, threshold 0.6). ComfyUI's own docs: *"**does not yet support texture and material generation**."* Corroborated: `Comfy-Org/hunyuan3D_2.1_repackaged` contains exactly one file, **no paint model**.
- **Community (texture-capable):** `visualbruno/ComfyUI-Hunyuan3d-2-1` (linked from Tencent's own README leaderboard; **2.1 with PBR + optional UV mapping**); `kijai/ComfyUI-Hunyuan3DWrapper` (2.0, includes texture); `Yuan-ManX/ComfyUI-Hunyuan3D-2.1`. **All high install complexity** — they require compiling `custom_rasterizer` and `differentiable_renderer` CUDA extensions. kijai ships prebuilt wheels only for Win11/py3.12/torch2.6+cu126.
- **Apple Silicon:** community ports exist — `VladimirTalyzin/hunyuan3d-2.1-mac-rocm`, plus MLX ports (`ddalcu/Hunyuan3D-2.1-MLX-Serve-8bit`). See §9.

### 4.6 LICENCE — VERBATIM (H)
**Per-version agreements: "TENCENT HUNYUAN 3D 2.0 COMMUNITY LICENSE AGREEMENT" (21 Jan 2025) and "...2.1..." (13 Jun 2025). [HF 2.0](https://huggingface.co/tencent/Hunyuan3D-2/raw/main/LICENSE) · [GitHub 2.0](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/LICENSE) · [HF 2.1](https://huggingface.co/tencent/Hunyuan3D-2.1/raw/main/LICENSE). No Hunyuan3D component is Apache-2.0.**

**Header (verbatim, capitals in original):**
> THIS LICENSE AGREEMENT DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA AND IS EXPRESSLY LIMITED TO THE TERRITORY, AS DEFINED BELOW.

**§1.l:**
> "Territory" shall mean the worldwide territory, **excluding the territory of the European Union, United Kingdom and South Korea.**

**§4 — ADDITIONAL COMMERCIAL TERMS (the threshold):**
> If, on the Tencent Hunyuan 3D 2.0 version release date, the monthly active users of all products or services made available by or for Licensee is greater than **1 million monthly active users** in the preceding calendar month, You must request a license from Tencent, which Tencent may grant to You in its sole discretion...

**→ 1 MILLION MAU, NOT 100 MILLION.** (The 100M figure is from the *HunyuanCustom / LLM* licence.) **There is no revenue threshold.** Request channel: `hunyuan3d@tencent.com`.
Note the drafting oddity: the MAU test is anchored to *"on the ... version release date"* — measured against a fixed date, not continuously. **Take legal advice rather than relying on that reading (M).**

**§5.c — DOES THE EXCLUSION REACH OUTPUTS? YES:**
> You must not use, reproduce, modify, distribute, or display the Tencent Hunyuan 3D 2.0 Works, **Output or results of the Tencent Hunyuan 3D 2.0 Works** outside the Territory. Any such use outside the Territory is **unlicensed and unauthorized** under this Agreement.

**§6.d — the tension:**
> Tencent claims no rights in Outputs You generate. You and Your users are solely responsible for Outputs and their subsequent uses.

**These are reconcilable** (no ownership claim ≠ no contractual use restriction) but a reader who finds only §6.d will draw the wrong conclusion. **Both are in the same licence.**
Also: **Exhibit A, item 1** prohibits use *"Outside the Territory"*. HF model cards carry the machine-readable flag **`extra_gated_eu_disallowed: true`** on Hunyuan3D-2, -2.1, -Omni.
**§5.b** blocks using outputs to improve any other AI model. **§3.d** mandates a NOTICE file string on distribution. **§3.e** requires disclosing the actual provider and stating Tencent is not affiliated. **§9:** Hong Kong law, Hong Kong courts. **Exhibit A** also bans military use and high-stakes automated decisions.

**⚠️ Widely-repeated error:** a popular Apple-Silicon port's README states *"Commercial threshold: above 100 million monthly active users"*. **That is wrong for Hunyuan 3D.** The official 2.0/2.1 text says 1 million.

### 4.7 Latency
**Tencent publishes no per-GPU timings for 2.0 or 2.1 (H — that no vendor figure exists).** Cloud HY-3D-Express: *within 90 seconds* (H). Do not extrapolate.

---

## 5. MICROSOFT TRELLIS / TRELLIS.2

### 5.1 Versions (H)
| Release | Date | Params | Repo |
|---|---|---|---|
| **TRELLIS 1.0** `TRELLIS-image-large` | 2024-12 | 1.2B | [HF](https://huggingface.co/microsoft/TRELLIS-image-large) |
| TRELLIS-text base/large/xlarge | 2025-03 | 342M / 1.1B / 2.0B | HF |
| **TRELLIS.2-4B** | **2025-12-01** | **4B** (aggregate across 6 DiT ckpts) | [HF](https://huggingface.co/microsoft/TRELLIS.2-4B) · [GitHub](https://github.com/microsoft/TRELLIS.2) |
Paper: arXiv **2512.14692** *"Native and Compact Structured Latents for 3D Generation"*. **Image-to-3D only.** Repo total 16.24GB. Uses the **O-Voxel** representation.

### 5.2 LICENCE — MIT FOR BOTH CODE **AND** WEIGHTS (H)
Verified across four artefacts: `microsoft/TRELLIS` LICENSE, `microsoft/TRELLIS.2` LICENSE, `TRELLIS-image-large` model-card frontmatter (`license: mit`), `TRELLIS.2-4B` frontmatter (`license: mit`).
> MIT License / Copyright (c) Microsoft Corporation. / Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies...

**No territorial clause. No MAU threshold. No acceptable-use exhibit. No output restriction.**
*Caveats:* third-party submodules carry their own terms — `diffoctreerast` (differentiable octree renderer), modified `FlexiCubes`, `nvdiffrast`, `nvdiffrec`. The **HF Space demo** is a hosted service with its own terms.

### 5.3 VRAM (H, verbatim)
- **TRELLIS 1.0:** *"An NVIDIA GPU with **at least 16GB** of memory is necessary. Verified on NVIDIA A100 and A6000."*
- **TRELLIS.2:** *"An NVIDIA GPU with **at least 24GB** of memory is necessary. Verified on NVIDIA A100 and H100."*
- NVIDIA's GenAI Creator Toolkit TRELLIS.2 module: *"VRAM: 16–24 GB"* — a real discrepancy with Microsoft's 24GB, likely reflecting the int8 checkpoint and/or reduced resolution. **Treat 24GB as the vendor requirement.**
- TRELLIS.2 and Pixal3D share architecture (same DINOv3 encoder, same shape/texture VAEs). ComfyUI's decoder has an explicit memory model: `2 GB fixed + point_count × (896 × dtype_bytes + 108)`, with `surface_point_estimate = resolution² × 5/4` — **decode cost scales with resolution²**, which is why 1536 is the expensive cascade.

**Does it fit the RTX 3080? Not officially — but there is a real path.** ComfyUI ships **`trellis_2_int8_convrot.safetensors` at 5.25GB** vs the bf16 at 10.34GB, and **the INT8 file is what ComfyUI's official workflow downloads by default**. ComfyUI has been actively cutting TRELLIS memory: **v0.34.3 (2026-09-02)** remesh memory, **v0.35.0 (2026-09-09)** peak VRAM+RAM — both *days old*. Community VRAM-bounded option: `Aero-Ex/ComfyUI-Trellis2-TiledDecode` (drop-in tiled decode for 1024–1536 on OOM cards; candid that *"exact tiled equivalence is mathematically out of reach"* for the shape decoder — guarantees structural stitching instead).
**No reported RTX 3080 measurement exists for either TRELLIS generation (L/unverified).**

### 5.4 Output format, UVs, PBR (H)
**TRELLIS 1.0:** outputs **all three** from one SLAT latent — `outputs['gaussian']`, `outputs['radiance_field']`, `outputs['mesh']`. Meshes need conversion via `postprocessing_utils.to_glb(gaussian, mesh, simplify=0.95, texture_size=1024)` — this **UV-unwraps and bakes a 1024 texture**. Gaussians export as `.ply`. **Texture is base colour only — no PBR head.**
**TRELLIS.2:** **mesh with full PBR directly.** From ComfyUI's native texture decoder source, verbatim:
```python
# The texture VAE emits 6: base_color (0:3), metallic (3), roughness (4), alpha (5) — all in [0, 1].
```
→ **base colour, metallic, roughness, alpha are PREDICTED by the model.**
**Normal and AO are BAKED from geometry**, per ComfyUI's docs post-processing stage: *"DC remesh, QEM decimation, UV unwrapping, and baking of base color, **normal**, and ambient occlusion maps."*
→ **Notably parallel to Hunyuan3D-Paint: both predict albedo/MR and derive normals geometrically.**
**Poly count: not published by Microsoft for either version (L).** Knobs: `Trellis2UpsampleStage.target_resolution` (default 1024, max 2048) and QEM decimation.
**Topology:** O-Voxel *deliberately* handles *"open surfaces, non-manifold geometry, and fully-enclosed structures without lossy conversion"* — **TRELLIS.2 output is explicitly NOT guaranteed manifold.** **No quad option in either version.**

### 5.5 ComfyUI integration (H)
- **NATIVE, first-class:** `comfy_extras/nodes_trellis2.py`, added **v0.34.0, 2026-08-26**. Nodes: `Trellis2Conditioning`, `Trellis2ShapeStage`, `EmptyTrellis2LatentStructure`, `Trellis2TextureStage`, `VaeDecodeTextureTrellis`, `VaeDecodeShapeTrellis`, `VaeDecodeStructureTrellis2`, `Trellis2UpsampleStage`, plus Pixal3D variants.
- Official workflow: `3d_pixal3d_trellis2_image_to_model.json`. **Preprocessing includes BiRefNet background removal.** Output to `ComfyUI/output/3d/ComfyUI/`.
- **Switch:** the template defaults to **Pixal3D** (Tencent ARC, SIGGRAPH 2026); a `Boolean (Switch to Trellis2)` node selects TRELLIS.2. Both diffusion checkpoints are required.
- **Community:** `PozzettiAndrea/ComfyUI-TRELLIS2` (**NVIDIA-recommended**, Manager-installable, warns it uses experimental `comfy-env`/pixi); `Aero-Ex/ComfyUI-Trellis2-TiledDecode`; `visualbruno/ComfyUI-Trellis2`; `dmvvilela/ComfyUI-Trellis2Apple`; `daveposh/ComfyUI-IF_Trellis_STL` (TRELLIS 1.0, high install complexity).

### 5.6 Latency (H, H100 only)
| Resolution | Total | Shape + Material |
|---|---|---|
| 512³ | **~3 s** | 2 s + 1 s |
| 1024³ | **~17 s** | 10 s + 7 s |
| 1536³ | **~60 s** | 35 s + 25 s |
Also: *"<10s (single CPU): Textured Mesh → O-Voxel"*; *"<100ms (CUDA): O-Voxel → Textured Mesh."* **TRELLIS 1.0: no latency table published.** **No consumer-GPU figures exist for either — do not extrapolate a 60s H100 figure to a 3080.**

---

## 6. RODIN / HYPER3D (hyper3d.ai, Deemos) — **the strongest quad-topology option**

- **Current generation: Rodin Gen-2.5** (launched **26 May 2026**). Gen-2 and Gen-1/1.5 remain selectable. Documented tier enum: `Gen-2.5-Minimum/-Extreme-Low/-Low/-Medium/-High/-Extreme-High` plus legacy `Sketch/Regular/Detail/Smooth/Gen-2`. **(H)** [docs.hyper3d.ai/en/get-started/features](https://docs.hyper3d.ai/en/get-started/features)
- **Gen-2.5 headline:** top tier returns a **second mesh up to 10M faces**; texture up to **12K**; speed ladder **~4s (Extreme-Low) to ~80s (Extreme-High)** (M). Plus `geometry_instruct_mode` (Faithful vs Creative), `is_symmetric`, `soft`, `detail_level`, `quad_normal`, Bang-to-Parts splitting, Local Edit region regeneration. **(H)**

### 6.1 Credits per generation (H — official docs) — **this is very cheap**
- **Base generation, ALL families = 0.5 credits** (text-to-3D and image-to-3D identical).
- `tier=Gen-2.5-Extreme-High` = **+0.5 credits** (1.0 total).
- `texture_mode=extreme-high` = **+2.0 credits**.
- Charges are additive. **HighPack credit cost not published (L)** — third-party fal lists it at +$0.80.

### 6.2 USD pricing (H — from the pricing page's embedded JSON)
| Plan | Monthly | Credits/mo | $/credit | Notes |
|---|---|---|---|---|
| Free | $0 | pay-on-confirm | — | 10 private assets; export from legacy models |
| **Creator** | **$30** ($24/mo yearly, $288/yr) | 30 (≈60 models) | **$1.00** ($0.80 yearly) | multi-image, Smart Low-Poly, HD texture, **baked normals from high-poly**, redos Geometry ×20/Material ×6. **NO API access.** |
| **Business** | **$120** ($96/mo yearly, $1,152/yr) | 208 (≈416 models) | **$0.58** ($0.46 yearly) | **full API access**, high-res textures, **High-Poly Quads**, 120–240 RPM |
| Business volume | $240 / $480 / $720 / $1,200 | 416 / 832 / 1,248 / 2,080 | — | ~832–4,160 models |
| Enterprise | "Let's Talk" | — | — | on-prem, custom LoRA/fine-tuning |
| Education | ~$12/mo (M) | Creator-tier benefits | — | verification required |
**Direct credit packs: $1.50/credit** (vs $1.00/$0.58 on subscription). Direct credits last longer; **gifted subscription credits expire at the end of the subscription period** (H, ToS §4.1).
**ⓘ ARBITRAGE:** **fal.ai resells Rodin Gen-2.5 at $0.40/generation standard and $0.10/generation fast** (HighPack +$0.80; fast capped ≤20K tris). **(H)** That is **cheaper than the subscription's $1.00/credit** for standard work, with no monthly commitment. [fal.ai](https://fal.ai/models/fal-ai/hyper3d/rodin/v2.5/llms.txt)

### 6.3 Quad topology and high/low-poly modes (H) — **the best in the field here**
- `mesh_mode`: **`Quad`** (quads) or **`Raw`** (triangles). **Gen-2.5 tiers default to `Raw`; every other tier defaults to `Quad`.**
- Face presets: **Gen-1/1.5 Quad** high 50,000 / med 18,000 / low 8,000 / XL 4,000 · **Gen-2 Raw** high 500,000 / med 150,000 / low 20,000 · **Gen-2.5 Raw** high 1,000,000 / med 500,000 / low 60,000.
- `quality_override`: Gen-2.5 **500–2,000,000** (2M only High/Extreme-High); **Quad hard-capped at 200,000**.
- HighPack in Quad mode adds a high-poly mesh ~**16×** the selected face count.
- **⚠️ "Smart Low-Poly" is a Creator-plan feature and "High-Poly Quads" is Business-only — but neither term is defined in the docs (L).**

### 6.4 API (H)
Base URL **`https://api.hyper3d.com/api/v2`**. Endpoints: `POST /rodin` (multipart), `/status`, `/download`, `/balance`, Generate Texture, **Bang** (part splitting). Bearer auth; async submit → poll `jobs.subscription_key` → download by `uuid`. Formats: **glb, usdz, fbx, obj, stl**. Materials: `PBR`, `Shaded`, `Hybrid`, `All`, `None`. **No official Python SDK** — the Quick Start publishes a full `requests` polling workflow instead (H that it's absent from PyPI). **MCP server** advertised. **API access is a plan entitlement (Business+), not separately metered.**

### 6.5 Licence (H) — [hyper3d.ai/legal/terms](https://hyper3d.ai/legal/terms), Deemos Corporation (Wilmington, Delaware)
> **§5(b)** — "If you use Rodin to generate Output, **we will not limit your use of such Output**, subject to any restrictions set forth in these Agreements..."
> **§5** — "we make **no representations, warranties or undertakings of any kind as to the copyrightability** of any Output or the availability of Intellectual Property Rights..."
> **§9** — "The Users accept to defend, indemnify, and hold harmless us..."
- **Most permissive output clause of any commercial vendor reviewed** — but paired with an explicit **no-IP-warranty** disclaimer and a **one-way indemnity** (you indemnify them; they do not indemnify you).
- **⚠️ Free-tier ambiguity:** §2 says users may export content "for private or commercial use **depending on your subscription plan**", and the pricing FAQ says "Paid plans include broader export and usage rights." So **Free is not an unrestricted commercial licence** despite the permissive §5(b). **Flagged.**
- **Training provenance:** Deemos announced a **commercial 3D-asset licence from Shutterstock** (5 Dec 2025) incorporated into model training (H). This is a *provenance* positive — they licensed training data — but it is not a commitment about *your* content.

### 6.6 Quality reputation (M/L — blog consensus, no rigorous benchmark)
Consistently placed in the **top tier for geometric fidelity and hard-surface detail** ("panel lines, bolts, and detailed mechanical features came through cleanly"; "output is consistently quad-dominant — usually the cleanest topology in the field"). Weaknesses cited: **textures are weaker than Meshy's**, generation is **slower than Tripo (3–8 min on older gens)**, and **topology still wants a retopo pass**. **No independent lab benchmark exists.**

---

## 7. OTHERS — current status, with two corrections to the brief

> **⚠️ Naming trap:** the brief lists **"Kaidim (kaidim.com)"**. That domain is a **South Korean AutoCAD dimensioning add-in** (feature extraction, datums, KS/ISO compliance; AutoCAD 2020+, Windows, .NET 4.8; **29,000 KRW/mo** beta). It has **no generative 3D, no mesh output, no API.** The human-in-the-loop generative-3D firm you meant is **Kaedim (kaedim3d.com)**.

| Tool | Sept 2026 status | Key facts |
|---|---|---|
| **Stability AI — SPAR3D / SF3D** | **Alive; the cheapest credible local option** | **SPAR3D** = current 3D model: single image → textured **UV-unwrapped** mesh in **<1s**, predicts **roughness/metallic**, point-cloud diffusion + mesh regression, 512×512 input. **SF3D** still on the API: UV-unwrapped textured GLB, **~0.5s on 7GB VRAM**, **~6GB default per its README**, and — valuable — **an optional quad/triangle remesh** (`--remesh_option`). **Open weights, gated**, on HF. **Licence = Stability AI Community License: free commercial use below US$1,000,000 annual revenue**; at/above that *"any licenses granted to You under this Agreement shall terminate."* You own outputs; you indemnify Stability; outputs "AS IS". API ≈ **$0.10/generation** (M, third-party). Live-probe confirmed both endpoints. |
| **Luma AI Genie** | **Legacy / withdrawn** | `lumalabs.ai/genie` **redirects to the home page**. Current pricing, API and docs cover **image + video only** (Ray 3.2, Uni-1.1); no Genie endpoint. Only a **stale 14 Nov 2024 FAQ** still claims support. **Treat as retired.** Third-party (L): 10–15s, ~30k tris, noisy normals, ideation-only. |
| **CSM / Common Sense Machines** | **DEFUNCT** | **`csm.ai` does not resolve (NXDOMAIN).** **Acquired by Google** — reported 24 Jan 2026, ~12 staff to **Google DeepMind**. Alpha3D's own site markets "CSM is no longer available". **Do not plan around it.** |
| **Kaedim** (kaedim3d.com) | Alive — the honest human-in-the-loop option | AI draft + human artist assurance, unlimited free revisions, ISO 27001. **No public price list** (`/pricing` → 404); sales-led. Third-party estimate **$150–$600/mo, ~24h turnaround (L)**. **Licence: "Your IP. Your assets… full ownership and commercial rights"; never used for training.** This is the *opposite* trade to everything else: you pay humans to fix topology. |
| **Backflip AI** | **Alive — the most interesting 2026 development** | Mesh → **native parametric CAD with a feature tree**, chaining real CAD ops (Extrude/Revolve/Pattern/Chamfer/Fillet). **Inputs STL/OBJ/GLB/GLTF/PLY → outputs ".STEP" or native feature tree.** *"Optimized for 3-axis CNC and turned parts"*; sheet metal and injection moulding "coming soon". Autodesk Fusion add-in + web app. Claims **~$1,500 → ~$10/part in 1–5 min**; **no published dimensional tolerance (L)**. **Fast 10 credits/job, Thinking 50/job.** Free 60 credits; **Builder $20/mo (100cr), Pro $50/mo (300cr), Business $380/mo (2,500cr)**. **⚠️ ToS grants Backflip a broad AI-training + output-redistribution licence by default; opt-outs (Privacy Mode / Private Library Mode) are tier-gated and the qualifying tiers are unspecified.** No vendor indemnity, no public API. |
| **Sloyd** | Alive — **procedural, not diffusion** | Parametric generators + sliders over a fixed catalogue (weapons, furniture, buildings, vegetation). Output **1k–15k tris, correctly UV-mapped, rigging-ready**, quads option, "Ultra" to 500K tris. **The critical limit: if it isn't in their generator catalogue, you cannot make it** — so it is useless for a tunnelling shield, but excellent for generic props. Plus **$15/mo** (commercial use), Pro **$50/mo** (resale). **API: USD 1 = 75 credits**, min $12 = 900 credits; image-to-3D 10cr, texturing +10, text +5, multi-image +10, **quads +5**. |
| **Alpha3D** | Alive, EUR-priced | **Tester €5/mo · Basic €16 (1,000 cr ≈35 models) · Creator €100 (3,200 cr) · Creator Pro €150 (10,000 cr)**. Full pipeline incl. **retopology, UV, AI texturing, format conversion**; drivable from Claude/ChatGPT. Prices extracted from the live JS bundle, not a rendered page (**M**); licence and output formats **unverified (L)**. |
| **Anything World** | Alive → rebranded **Everything Universe** | `anything.world` redirects to `everythinguniver.se`. **Auto-rigging and animation**, not primarily mesh generation; REST API + Python package. **API use requires written authorisation.** Individual $0 (<$100K rev, 1 seat), Micro $50/mo, Pro $250/mo, Enterprise custom. You own creations; **mandatory attribution ("Animated by Anything World")**; no vendor indemnity. |
| **Masterpiece X** | Pivoted → **WorldEngen** | Now an AI scene editor pairing "leading AI models" with Blender/Unity/Unreal; 7-day trial, sales-led. Legacy Generate credit packs still sold (750/$10.99, 1,500/$19.99, 3,000/$36.99). **API is early-access only.** Output-ownership terms unverified. |
| **World Labs — Marble** | **New; the only real world-model with DCC export** | Text/image/pano/video → **persistent 3D worlds**. Outputs **Gaussian splats (.spz/.ply) + collider mesh GLB (~100–200k tris) + visual mesh GLB (~600k textured tris)** + panoramas + camera-path video. **Real Blender/Unreal/Unity/Houdini export.** API **$1 = 1,250 credits, min $5**; **Marble 1.1 Plus = 1,500 + 0–1,500 credits (≈$1.20–2.40)**; Draft = 150 credits (≈$0.12). App: Free / Standard $20 / **Pro $35 (commercial rights)** / Max $95. Latency ~20s (Draft) to ~5 min (full world). |
| **3D AI Studio** | Alive — aggregator | Front-end over Meshy/Tripo/Rodin from **$19/mo**; 1,000 / 3,500 / 18,000 credits tiers; **20 credits per image- or text-to-3D**. Useful as a cheap multi-model API. **(M)** |
| **Krea 3D** | Alive — front-end | Runs **Hunyuan3D 3.1 Pro, Hunyuan3D-2.1, TRELLIS, TRELLIS 2, Tripo** behind one subscription. **GLB only.** No free 3D; 3D starts on **Pro $35/mo**. Commercial licence included. **(M)** |
| **fal.ai** | Alive — router | Pay-per-call HTTP API exposing **Rodin Gen-2.5 ($0.40 standard / $0.10 fast)**, Hunyuan3D, TRELLIS. **The cheapest way to reach Rodin without a subscription.** |

---

## 7A. ADOBE — a clean negative, and it matters

**Adobe ships NO text-to-3D or image-to-3D product in September 2026. This is a correction to the assumption in the brief.** **(H)**

- **Substance 3D Viewer** — the only Adobe product that ever did generative 3D — is **DECOMMISSIONED**. Verbatim: *"As of October 16, 2025, Substance 3D Viewer will no longer be supported or available for installation."* Its "Generate workspace" contained **Text to 3D**, which output **Gaussian splats**, with these verbatim limitations: *"Materials and appearance cannot be edited"*, *"Lighting changes have no effect"*, *"It cannot be exported to most traditional 3D file formats."* **No mesh, no glTF/USD export, no PBR.**
- **Substance 3D Sampler** — **all generative AI features were REMOVED in v5.1.2 (20 Nov 2025)**, and the Generative AI panel was deleted in **6.0**. Verbatim from the 5.1.2 notes: *"[Generative AI] Generative AI features removal. This feature has been removed from the application and the service will stop working in previous versions of Sampler on March 5th."* **3D Capture** (photogrammetry image→mesh) was removed earlier, in 5.1.0 (7 Aug 2025). **Current version: 6.0.3 (24 Aug 2026).** What remains is classical image→material-map extraction ("Image to Material removes shadows, and generates albedo, roughness, normal and displacement maps") — a 2D operation, **not generative 3D**, and still genuinely useful for texturing hand-built geometry.
- **There is no product called "Adobe 3D Generate" or "Firefly 3D"** anywhere in Adobe's plans, help navigation or legal docs **(L for the negative)**. **Project Neo** remains **(Beta)** as of March 2026 and is a 3D design/illustration tool, **not** generative image-to-3D.
- **Two unresolved Adobe pages that are the biggest open questions:** Firefly Boards *"Convert 2D images into 3D assets"* **exists as a docs page but its body could not be retrieved** (output format, GA/beta, credit cost, licence all unknown); and Firefly Creative Production *"Use 3D digital twin workflows"* (same problem). **What would settle it: manual browser read of those two help pages while signed in.**
- **Substance 3D pricing (ADOBE'S OWN published FAQ, effective 25 Mar 2025):** Collection Individual **$59.99/mo** (annual prepaid $599.88); Collection Teams **$119.99/mo/seat** (annual prepaid $1,439.88); **Substance 3D Texturing Individual $24.99/mo** (annual prepaid $249.88). Adobe notes *"The exact price will vary by currency and country."* The live US plans page now presents only Collection tiers — **whether the standalone Texturing plan is still purchasable is unclear (M)**.

### 7A.1 Adobe's IP indemnity does NOT cover 3D output **(H on the quote; M-H on interpretation)**
From Adobe's *Firefly Legal FAQs – Enterprise Customers* (doc header 10 May 2024 — **no 2025/2026 revision found, so currency is itself uncertain**):
> **Q14** — "Adobe's Firefly IP indemnity for eligible offers covers **Firefly GA features that generate imagery**. Terms apply."

**Read plainly: the indemnity is scoped to features that generate *imagery*. Mesh / Gaussian-splat / GLB output is not imagery, so 3D output is not covered on the face of the document.** Adobe has published no 3D-specific carve-out either way.
**Ownership is favourable, though (verbatim):** *"As between Adobe and the customer, the customer owns and controls Firefly outputs"*; *"Adobe does not assert any IP rights in the output."* **Restrictions:** outputs *"cannot be used… in connection with creating, training or otherwise improving AI/ML models"*; Q3: *"Can I use Firefly outputs to train my own AI/ML models? • No."* **Q12 (indemnity availability):** *"Yes, if you have purchased the appropriate entitlement (which will require a new contracting event), subject to the applicable terms, conditions, and exclusions."* **Q13 exclusions that bite:** the indemnity does **not** cover claims arising from *"your modification of the Firefly output using any product or service, including edits made with Creative Cloud products/services"*, *"any other materials that you use in combination with the Firefly outputs"*, or *"the context in which you use the Firefly output."* **Q6 confirms agency/client use is permitted.**
**Practical read: Adobe's indemnity is only valuable if you don't modify or combine the output — which is exactly what a Blender compositing pipeline does.** Adobe is therefore *not* the indemnity safe harbour it is often assumed to be for this use case.

---

## 7B. COMFYUI — native 3D is now extensive, and it changes the local calculus

**ComfyUI core now has a broad native 3D toolchain (H — read from `comfy_extras/` on master, 17 Sept 2026). Repo moved to `Comfy-Org/ComfyUI`; version ≥ v0.35.1.**

**Native model support:** Hunyuan3D **2.0/MV (shape only)**, **TRELLIS.2**, **Pixal3D**, **TripoSplat** (Gaussian splats), **SAM3D-Body**, Stable3D (SV3D/Zero123). **NOT in core:** TripoSR, TRELLIS 1.0, Hunyuan3D 2.1, **Hunyuan3D 3.0** (cloud Partner node only).

**IO and format support (H — read from source):**
- **Load 3D accepts: `.gltf .glb .obj .fbx .stl .spz .splat .ply .ksplat`.** Save writes **`.glb`** for meshes; splat writers emit **ply, ksplat, spz** — **there is no `.splat` writer** (source comment: `TODO: add "splat" when we have a writer for it`).
- `MeshToFile3D` explicitly carries *"UVs, colors, normals, texture, normal/occlusion/emissive maps and material."*

**The post-processing node set is the important part** — it exists precisely because raw generative meshes arrive broken:
`RemeshMesh`, `DecimateMesh`, `FillHoles`, `WeldVertices`, `MeshSmoothNormals`, **`UnwrapMesh`**, `RenderUVAtlas`, **`BakeTextureFromVoxel`**, **`BakeNormalMapFromMesh`**, **`BakeAmbientOcclusion`**, `ApplyTextureToMesh`, `PaintMesh`, `MergeMeshes`, `GetMeshInfo`, plus `SplatToMesh`, `PreviewGaussianSplat`. **ComfyUI's own blog states it plainly: *"Raw generative meshes are rarely production-ready."*** This is vendor-confirmed evidence for the failure modes in §14.

**⚠️ MAJOR LICENSING FINDING (H — ComfyUI's own blog, verbatim):**
> *"Trellis.2's own code and weights are MIT-licensed, but its original pipeline depends on NVIDIA's nvdiffrast … and nvdiffrec …, both distributed under the **NVIDIA Source Code License which restricts usage to non-commercial research and evaluation**. In practice, a studio couldn't ship assets from the reference pipeline without stepping into a legal gray zone. These dependencies have been removed within the native integration."*
ComfyUI also states TRELLIS.2/Pixal3D are *"free to use, including commercially"* and that 3D post-processing was *"reimplemented from scratch in PyTorch and SciPy."* **(H on the quotes; M on the legal conclusion — it is ComfyUI's assertion, not a legal opinion.)**
**→ This materially qualifies the "TRELLIS.2 is MIT" headline: use the ComfyUI native path (or otherwise avoid nvdiffrast/nvdiffrec) if you intend to ship commercially.**

**ComfyUI cloud Partner Node 3D pricing (in ComfyUI "credits"/run, H).** Tripo's docs give the only USD anchor: *"The node converts internal Tripo credits to USD at credits × 0.01."*
| Partner | Cost (credits) |
|---|---|
| **Tripo v3.0/v3.1** | 21.1 → 147.7 depending on texture × geometry quality; **`quad` +10.55**; `smart_low_poly` +21.1. **= $0.21–$1.48** |
| Tripo P2 | 211 / 232.1 / 253.2 / 274.3 (extreme) |
| Tripo post | Retopology 63.3; Rig 52.75; Rig Check free |
| **Rodin** | Gen-2.5 Regular/Fast **158.25**; Extreme-High **316.5**; **HighPack +168.8**; Gen-2 84.4 |
| **Hunyuan3D 3.0** | Geometry **63.3**; Normal 105.5; LowPoly 126.6; **PBR +42.2**; Model to UV 42.2; Smart Topology 211 |
| **Meshy** | Text to Model 241.4; Image to Model 241.4 / 362.1 (2K-4K) / 422.4 (8K); Texture 120.7 |
**⚠️ Do not convert non-Tripo providers' credits to dollars — no general credit→USD rate was verifiable (L).**

**Community node packs (live GitHub data, 17 Sept 2026):** `visualbruno/ComfyUI-Trellis2` (831★, MIT, active, shape+PBR) · `PozzettiAndrea/ComfyUI-TRELLIS2` (573★, MIT, active; NVIDIA-recommended; uses experimental `comfy-env`/pixi) · `kijai/ComfyUI-Hunyuan3DWrapper` (1,042★, **last push 2026-03-16 — slowing**, texturing requires compiling CUDA extensions; prebuilt wheels only for Win11/py3.12/cu126) · `MrForExample/ComfyUI-3D-Pack` (3,870★, **last push 2025-12-29 — stale**) · `VAST-AI-Research/ComfyUI-Tripo` (351★, official cloud nodes) · `Aero-Ex/ComfyUI-Trellis2-TiledDecode` (the low-VRAM escape hatch).
**Direct evidence of native migration:** `niknah/ComfyUI-Hunyuan-3D-2`'s README now opens *"Don't use this one any more. Hunyuan-3D v2 is built into ComfyUI."*
**Do not cite — these 404:** `kijai/ComfyUI-TrellisWrapper`, `visualbruno/ComfyUI-TripoSR`, `stabilityai/ComfyUI-StabilityAI-generative-models`.

**ComfyUI → Blender, what breaks (H on the node set, M on inference):** core ships `UnwrapMesh`, `FillHoles`, `WeldVertices`, `DecimateMesh`, `RemeshMesh`, `BakeNormalMapFromMesh` **because raw output arrives non-manifold, holed, without usable UVs and without a complete material set**. **Axis convention: ComfyUI's Load 3D is documented in-source as "Y-up world space"; Blender is Z-up** — GLB/glTF importers convert automatically, **OBJ/PLY do not**, so expect flipped imports on those paths. ComfyUI exposes **no unit metadata**, so treat scale as a per-import fixup.

---

## 7C. BLENDER ADDONS — the structural facts first

**ⓘ Blender's official extension platform contains ZERO generative-3D vendor addons.** The full live catalogue was pulled and audited: **1,454 extensions**, regex-matched across names, taglines and maintainers for `meshy|tripo|rodin|hyper3d|hunyuan|trellis|substance|generative|text-to-3d|image-to-3d`. Only two surface, both irrelevant (Bonsai, a BIM addon, and a third-party Substance *textures importer*). Direct URL probes for `/add-ons/meshy/`, `/tripo/`, `/rodin/`, `/hunyuan3d/`, `/trellis/`, `/ai-3d/` all 404. **(H)**

**ⓘ Blender itself has NO built-in generative AI, and none is planned.** Verbatim, Francesco Siddi (Chairman, Blender Foundation), 1 May 2026:
> *"Blender is a tool for artists and creators, it's made by humans for humans. **No generative AI functionality is currently available or planned to be integrated in Blender.**"*
Context: Blender had announced Anthropic as a Corporate Patron, drew community criticism, and converted it to a one-time donation. **Current release: Blender 5.2 LTS (14 July 2026)** — headline features are node-powered physics and an online asset library, no AI. **(H)**

| Addon | Official? | Blender | Notes |
|---|---|---|---|
| **Meshy for Blender** | ✅ **Official, free** | **4.2.6+** | v0.6.1. **Requires Meshy Pro+.** **macOS and Windows only.** One-click bridge + **Make Manifold / Delete Small Pieces / normal correction / watertight analysis**. **The best all-round choice for this production.** |
| **Tripo 3D for Blender** | ✅ Official, GitHub | 3.0+ | `VAST-AI-Research/tripo-3d-for-blender`, **v0.7.7 (2025-11-06)**, 67★, MIT. Needs a **Tripo API key**; generation billed to your Tripo account. Text/Image/Multiview-to-Model with texture quality, PBR, face-limit, style options. *(A separate "Tripo DCC Bridge for Blender" is marketed on their blog — Cloudflare-blocked, so **whether it differs from this extension is unresolved (L)**.)* |
| **Hunyuan3D Blender addon** | ✅ Official (Tencent) | — | A single `blender_addon.py` in the Hunyuan3D-2 repo (released 27 Jan 2025). **Requires a locally running Hunyuan3D API server.** **Whether it was ever updated beyond 2.0 is unverified (L)**; the 2.1 README contains no Blender mention. |
| **Rodin** | ⚠️ MCP-based | — | No standalone official addon. `DeemosTech/blender-mcp-rodin-integration` (5★, MIT, under the vendor org — plausibly official but not labelled as such). Rodin is also a ComfyUI cloud Partner node. |
| **TRELLIS** | ❌ Community only | 3.6+ | `FishWoWater/trellis_blender` (69★, **no licence file**, **last push Dec 2025 — ~9 months stale**). Requires a running TRELLIS/TRELLIS.2 API server. Ships an MCP integration. |
| **Adobe Substance 3D add-on for Blender** | ✅ Official | 3.0+ (incl. Mac) | **Version 2.0.0** (Mar 2024; docs refreshed May 2026, no version bump found). **This is a `.sbsar` MATERIAL bridge — it does NOT do image-to-3D or text-to-3D.** Adobe ships no generative-3D Blender bridge. Known issues: socket ordering on Blender 4.0+; Ctrl+Z errors. |
| **Substance Textures Importer** (3rd party) | ❌ | 4.2+ | On the official platform, **25,688 downloads**, GPL-3.0, v7.2.0 (Mar 2026, updated for Blender 5.0.1). Map-name pattern matching, split-RGB channels, normal-map detection, OpenGL↔DirectX green-channel flip. Genuinely useful for the texturing half. |

### 7C.1 `blender-mcp` — the single most relevant tool for this operator **(H)**
**`ahujasid/blender-mcp` — 28,832★, MIT, last push 16 Sept 2026 (one day before assessment).** The dominant AI-in-Blender integration: *"Community plugin to control Blender 3D with any LLM of your choice."* It can export scenes to GLB/FBX, look up node schemas, and **execute arbitrary Python in Blender** — which is exactly the "Blender + Python driven by an LLM agent" architecture described in the brief. Its asset-generation line, verbatim, includes *"AI-generated 3D models via **Hyper3D Rodin and Hunyuan3D**"*, with documented routing for mainland (`AI3D 3.0`, `ap-guangzhou`) vs international (`Hunyuan-to-3D (Professional)`, PBR enabled, `ap-singapore`) Tencent accounts — **and a note that sending international credentials to the mainland endpoint fails with `AuthFailure.SignatureFailure`.**

---

## 8. HARDWARE REALITY — what actually runs where

### 8.1 The RTX 3080 (10–12GB) — the render node
| Model | Shape | Texture/PBR | Verdict |
|---|---|---|---|
| **TRELLIS 1.0** | 16GB floor | base colour only | ❌ |
| **TRELLIS.2** | 24GB vendor floor | full PBR | ⚠️ **only via ComfyUI INT8 ConvRot (5.25GB) + tiled decode**, at reduced resolution |
| **Hunyuan3D 2.0** | 6GB | 16GB combined | ⚠️ shape yes; texture marginal |
| **Hunyuan3D 2.1** | 10GB | 21GB texture / 29GB combined | ⚠️ **shape yes (tight), texture no** |
| TripoSR | ~6GB | — (vertex colour) | ✅ but 2024 quality |
| TripoSG | ≥8GB | — (shape only) | ✅ shape only, MIT |

### 8.2 The Mac M1 16GB — the control plane
**Do not run diffusion 3D inference on this machine.** The best available measurement:
> **Apple M4 Pro, 24GB, macOS 26, torch 2.13** (Hunyuan3D 2.1 via `VladimirTalyzin/hunyuan3d-2.1-mac-rocm`, "Safe" preset):
> **Shape: 5.7 min** (30 steps, octree 192) · **PBR texture: 8.5 min** (6 views @ 256px) · **~8GB of swap at peak.**

**That is a 24GB M4 Pro at 8GB of swap.** An M1 16GB has less compute, less memory bandwidth, and 8GB less unified memory. Expect it to thrash or abort.
**Hard MPS limits (H):** without flash attention the multiview attention matrix is **4.2 GiB at 6 views/256px (works)**, **67.5 GiB at 6 views/512px (refused)**, **607.5 GiB at 8 views/768px (refused)**. The port preflights and refuses rather than crashing; the MPS limit is 40% of `torch.mps.recommended_max_memory()`, floored at 5 GiB. **On MPS/ROCm only the "Safe" preset (6 views, 256px) is usable.** Upstream defaults (8 views @768, 2048² renders, 4096² textures) want ~21GB.
**TRELLIS.2 on Apple Silicon:** community port `shivampkumar/trellis-mac` + ComfyUI nodes `dmvvilela/ComfyUI-TrellisMac` (MIT wrapper). Requires `PYTORCH_ENABLE_MPS_FALLBACK=1`, **two gated HF models** (`facebook/dinov3-vitl16-pretrain-lvd1689m`, `briaai/RMBG-2.0`), **~16GB of weights**, and hits a **macOS GPU watchdog** that kills long Metal kernels in the SLat decoder ("decoder produced an empty mesh"). Workarounds: run headless, `MTL_CAPTURE_ENABLED=1`, `SPARSE_CONV_BACKEND=none`.
**Practical recommendation:** treat the M1 as the **orchestration/API-driving seat** (it runs the LLM agent, the Tripo/Meshy Python clients, and Blender-free GLB inspection fine), and put **all inference on the 3080 or in the cloud**.

---

## 9. COST PER ASSET — and for a 60-second video needing 40–80 assets

**Assumption:** 60s video, 40–80 distinct assets, each needing image→mesh→texture, with **~1.5 generations per usable asset** (one retry).

### 9.1 Per-asset cost
| Path | Per asset (textured) | With quads | With 1.5× retry |
|---|---|---|---|
| **Tripo H3.1 API**, standard texture | **$0.30** | $0.35 | $0.45–0.53 |
| **Tripo H3.1 API**, detailed texture | $0.40 | $0.45 | $0.60–0.68 |
| **Tripo H3.1 API**, detailed + HD geometry + quad | $0.65 | $0.65 | $0.98 |
| **Meshy Meshy-7** (Pro, $0.02/cr) | $0.60 | +remesh/UV $0.20 = $0.80 | $0.90–1.20 |
| **Meshy Meshy-7** (Ultra, $0.0125/cr) | $0.375 | $0.50 | $0.56–0.75 |
| **Meshy Smart Topology T2** (low-poly, 2s) | 15 cr = $0.30 (Pro) | — | $0.45 |
| **Hunyuan3D cloud HY-3D-3.0/3.1** | ¥1.8–7.2 ≈ **$0.25–1.01** | — | ×1.5 |
| **Hunyuan3D cloud HY-3D-Express** | ¥1.8–3.0 ≈ **$0.25–0.42** | — | ×1.5 |
| **TRELLIS.2 local** (3080/cloud GPU) | ~$0 marginal + electricity (~$0.02) | **no quad option** | n/a |
| **Backflip scan-to-CAD** | **~$10/part** (vendor claim, down from ~$1,500) | n/a — outputs parametric CAD | — |

### 9.2 Monthly cost for 40–80 assets
| Plan | Monthly | Credits | Assets/mo at 30–45 cr | Covers 40–80? |
|---|---|---|---|---|
| **Tripo Pro** | **$20** | 3,000 | ~66 (at 45 cr) | 40 yes; 80 needs Max |
| **Tripo Max** | **$90** | 25,000 | ~555 | ✅ comfortably |
| **Tripo pay-as-you-go** | ~$12–36 one-off | — | 40–80 at $0.30–0.45 | ✅ **cheapest for a one-off episode** |
| **Meshy Pro** | **$20** | 1,000 | 25 (at 40 cr) | ❌ |
| **Meshy Premium** | **$40** | 3,000 | 75 | ✅ for 40–80 |
| **Meshy Ultra** | **$100** | 8,000 | 200 | ✅ with headroom |
| **Meshy Studio** | **$70** | 5,500 pool | 137 | ✅ + API retention 14d (vs 3d) |
| **Hunyuan3D cloud** | ~$25–75 one-off | — | 40–80 | ✅ |
| **Local TRELLIS.2** | $0 | — | limited by time, not money | ⚠️ |

### 9.3 The headline number
**For one 60-second episode needing 40–80 textured assets, the total generative-3D spend is approximately $12–$60 of API credits — i.e. one or two months of a single mid-tier subscription.** Tripo pay-as-you-go at $0.30–$0.45/asset is the cheapest reliable route: **$12–$36 for the episode.**
**The binding constraint is not money. It is the retopology and repair labour afterwards** — and that is where the real budget goes.

---

## 10. QUALITY — what these things actually produce

### 10.1 The honest summary
Every tool in this class produces **dense triangle soup with no construction history**. Differences are of degree, not kind.

| Dimension | Reality |
|---|---|
| **Polygon counts** | Raw output is typically **tens of thousands to 2M triangles**. Tripo H3.1 goes to 2M; Meshy raw is unpublished but a docs example shows ~25K; TRELLIS.2 and Hunyuan3D publish **no poly count at all**. All are far denser and far less regular than a hand-modelled game asset. |
| **Topology** | **Triangle soup, irregular valence, no edge loops.** Tripo and Meshy are the **only two with a quad/retopo path** (Tripo `quad`, 150K quad cap; Meshy quad-dominant remesh to 300K, or Smart Topology generated directly at 100–15,000 faces). **Hunyuan3D and TRELLIS have NO quad option — triangles only.** |
| **Hard-surface / mechanical** | **The weakest case across all tools.** Rodin markets quads+PBR and Backflip targets CNC parts, but no vendor demonstrates clean, dimensionally-true mechanical assemblies. Panel lines and thin features sometimes reconstruct (the Hunyuan3D port's own robot example with a few-pixel-wide antenna survived), but that is single-part, single-image, best-case. |
| **Thin-walled geometry** | Mixed. TRELLIS.2's O-Voxel explicitly supports **open surfaces** (cloth, leaves) and non-manifold geometry — a genuine advance. Hunyuan3D handles holes/handles. But thin walls become either blobs or holes. |
| **Does it invent geometry?** | **Yes, always, and confidently.** Single-image methods hallucinate the entire unseen back. The Hunyuan3D port documents this bluntly: *"Note the underside of the seat: surfaces no camera saw are the weakest part of any 6-view bake."* Its documented **failure case** — an owl photographed with a visible floor reconstructed as *"a large flat disc with a small owl sitting on it"* — is exactly the failure mode your reference images will hit if they show ground planes. |
| **Symmetry** | Not enforced. Generated pairs (e.g. two shield frames) will not be mirror-identical. |
| **Dimensional accuracy** | **None.** Nothing in this class outputs real-world scale. Meshy has a `resize` endpoint (1 credit; height/longest-side/AI auto-size) and Blender's "Scale to Volume/Bounds" — these impose scale, they do not recover it. This is the single hardest blocker for anything that must match a drawing. |
| **Manifold / watertight** | **Not guaranteed by any vendor.** TRELLIS.2 *deliberately* supports non-manifold output. Hunyuan3D's README's "watertight" claim applies to the **HY3D-Bench training corpus**, not to model outputs — a distinction frequently conflated. Meshy ships an explicit free "Analyze Printability" (watertightness, holes, non-manifold edges, degenerate faces) **precisely because outputs routinely fail it**, plus a 10-credit Repair. |

### 10.2 Per-tool quality notes
- **Tripo H3.1** — best claims for sharp edges and structured topology (v3.0 Ultra release notes specifically mention *"edges are sharper, double-sided-face structural defects resolved, topology tidied"* — **L**, vendor blog, no benchmark numbers). **P2 is the only genuinely low-poly-native model at 48–25,000 faces.**
- **Meshy** — **Smart Topology T2 is the standout for production**: generates **directly at a target face count with native part segmentation** in ~2 seconds, so you skip the remesh step entirely. This is the single most production-friendly feature reviewed.
- **Hunyuan3D 2.1** — strong geometry quality (best ULIP/Uni3D scores in its own table) and the **normal map is rendered from actual mesh geometry**, so it is honest about surface error rather than hallucinating a smooth surface over a bad one.
- **TRELLIS.2** — highest resolution ceiling (1536³), handles arbitrary topology, and **predicts base colour/metallic/roughness/alpha**. Best-in-class for organic/complex-topology subjects; still no quad output.
- **Rodin** — native quads + PBR is a real differentiator for engine-bound work. **M**

---

## 11. UVs AND PBR OUTPUT

| Tool | UVs | PBR maps | Resolution | Normal provenance |
|---|---|---|---|---|
| **Tripo H3.1** | Unwrapped (`export_uv` default true) | base_color, metallic, roughness, **normal** | 8K max (`extreme`); standard/detailed sizes unpublished | **UNVERIFIED** — `bake` = material flattening, not a documented normal bake |
| **Meshy 7** | Yes; explicit **UV Unwrap** endpoint (5 cr) | Albedo, Normal, Roughness, Metallic (+emission on meshy-6 only) | **2K/4K/8K** (base colour) | **UNVERIFIED** — `remove_lighting` ≠ normal bake |
| **Hunyuan3D 2.1 Paint-PBR** | UV-baked (`bake_mode: back_sample`) | **albedo + metallic-roughness** (no separate normal output) | **render 2048, baked texture 4096**, Real-ESRGAN ×4 | **RENDERED from mesh geometry** (`render_normal_multiview`) — not predicted ✅ honest |
| **TRELLIS.2** | UV unwrapped in post-processing | **base_color, metallic, roughness, alpha** (predicted) + **normal, AO baked** | `texture_size` 512/1024/2048 (Microsoft example uses 4096) | **BAKED from geometry** after DC remesh + QEM decimation ✅ |
| **TRELLIS 1.0** | `to_glb()` unwraps | **base colour only — no PBR** | 1024 (default) | n/a |
| **Rodin Gen 1.5/2** | Yes | PBR, native quad mesh | 4K on Business (claim) | **L** |

**The pattern worth internalising: no consumer-grade tool predicts a normal map from a high-poly source. Two of them (Hunyuan3D, TRELLIS.2) explicitly render/bake it from the geometry they produced — so the normal map encodes the mesh's errors rather than hiding them.** That is more useful than it sounds, and it is why these are usable as *displacement/normal sources on hand-built geometry* (§14).

---

## 12. LICENCE SUMMARY TABLE

| Tool | Free tier commercial? | Who owns output | Licence-back to vendor | Trains on your content? | Indemnity | Territory |
|---|---|---|---|---|---|---|
| **Tripo** | ❌ **No** (Tripo owns) | Paid: you, *"subject to"* licence-back | **Royalty-free, perpetual, irrevocable, worldwide, non-exclusive** | **Paid: NO** (expressly excluded). Free: yes. | ❌ user→vendor only; cap 12mo fees or $500 | None |
| **Meshy** | ✅ CC BY 4.0 — **but you can't download on Free** | **Contradictory across pages**; ToS vests free output in Meshy, no paid assignment | Non-exclusive, royalty-free, worldwide (narrower than Tripo) | ✅ **YES for ALL non-Enterprise plans** | ❌ user→vendor only; cap 12mo fees | None |
| **Hunyuan3D open weights** | ✅ conditional | You (§6.d) | — | §5.b bars using outputs to train other models | ❌ | ⛔ **EU / UK / South Korea excluded — and §5.c reaches OUTPUTS** |
| **TRELLIS / TRELLIS.2** | ✅ **MIT** | You | None | No restriction | ❌ (MIT warranty disclaimer) | ✅ **None** |
| **TripoSR / TripoSG** | ✅ MIT (TripoSG card says `mit`) | You | None | None | ❌ | ✅ None |
| **Stability SF3D / SPAR3D** | ✅ **free below $1M USD annual revenue** | You | — | — | — | ✅ None |
| **Backflip** | — | — | — | — | — | From $20/mo |
| **Rodin** | **UNVERIFIED** | Paid plans: "any use" claim | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** |

**The two facts that should drive the decision:**
1. **If anyone in the EU, UK or South Korea will ever see the output, Hunyuan3D open weights are off the table** — §5.c restricts *"Output or results"* explicitly, and says use outside the Territory is *"unlicensed and unauthorized"*. This is not a distribution-only restriction.
2. **Meshy trains on your inputs and outputs on every plan below Enterprise.** If the channel's look or your reference plates are the asset, that is a real commercial exposure. Tripo's paid terms explicitly do the opposite.

---

## 13. WHERE GENERATIVE 3D GENUINELY WORKS — and where it must not be attempted

### 13.1 USE IT (high confidence, low risk)
| Use | Why it works | Best tool |
|---|---|---|
| **Background filler** | Blurred, occluded, out of focus. Errors are invisible. | Any. Meshy T2 at 2s/$0.30 is ideal. |
| **Distant silhouette geometry** | The silhouette is all that reads. Topology and UVs are irrelevant. | Tripo P2 / Meshy Smart Topology (native low-poly). |
| **Organic props — rope coils, vegetation, rubble, coal heaps** | Organic forms have no construction logic to violate. This is exactly what single-image 3D is trained on. | **TRELLIS.2** (open surfaces, best topology handling) or Tripo H3.1. |
| **Crowds at distance** | Repeated, tiny, low-detail. Generate 5–8 variants, instance them. | Meshy Smart Topology. |
| **Texture / HDRI generation** | **The highest-value use in this entire list.** You can texture *hand-built* geometry — which is the reverse of the usual pipeline and avoids every topology problem. | Hunyuan3D-Paint (works on **handcrafted meshes** — the README says so explicitly), Meshy Retexture (10 cr), Adobe Substance 3D Sampler, Hyper3D AI Texture/HDRI Generator. |
| **Concept exploration / mood boards** | Nothing ships; you're buying ideas per dollar. At $0.30 a look, generate 50. | Tripo/Tripo pay-as-you-go. |
| **Matte painting elements** | 2D compositing tolerates 3D errors completely. | Any image-to-3D, then render to a plate. |
| **Foliage** | Organic, self-similar, forgiving. | TRELLIS.2 (open surfaces) / Tripo. |
| **Cloth** | TRELLIS.2 explicitly supports **open surfaces** (clothing, leaves). | TRELLIS.2. |
| **Rough-form blocking → retopologise in Blender** | See §14. The single most valuable hybrid workflow. | Tripo (quad) or Meshy (quad remesh). |

### 13.2 DO NOT ATTEMPT (these will fail, and they will fail expensively)
| Must not be generated | Why |
|---|---|
| **Precise machinery** | No dimensional accuracy, no parametric control, no construction history. It will look *approximately* right and be *specifically* wrong. |
| **Hard-surface mechanisms with moving parts** | Cannot articulate. No axis, no pivot, no joint definition. |
| **Anything matching a dimensional drawing** | There is no scale path. Brunel's shield was built to drawings; a diffusion model has never seen one. |
| **Riveted iron plate** | Rivet rows are a regular array — exactly the kind of repetitive, high-frequency, semantically-meaningless pattern these models smear into mush. Generates *plausible* rivets in *implausible* places. |
| **Cast-iron segmental lining rings** | The whole point is a precise, repeated, radially-symmetric ring with a known segment count and bolt pattern per Brunel's design. A generative model will produce a wonky ring with the wrong number of segments. **This is the single worst possible subject for this technology.** |
| **Timber centring** | Structural carpentry is defined by member cross-sections and joints. Diffusion invents members that don't connect. |
| **Gear trains** | Teeth must mesh with correct module and centre distance. Generated gears do not mesh, and the error is *visually obvious to exactly the audience you're courting*. |
| **The shield itself** | It is the subject of Episode 1. It must be right. **Hand-model it.** |
| **Anything that must animation-rig or articulate** | Triangle soup with no edge loops deforms catastrophically. |
| **Anything that must match a real museum object** | There is no path from a generative mesh to a verified reproduction. |

### 13.3 The rule of thumb
> **Generative 3D works where the audience cannot measure the result and does not know the object. It fails where the audience is an engineering-literate Instagram following and the object is the subject of the episode.**
>
> Every asset in the shot must be sorted into one of two buckets: **"nobody will measure this"** (background, props, filler) or **"this must be correct"** (the shield, the rings, the plate, the centring). Put bucket 1 through generative 3D. **Model bucket 2 by hand.** There is no third bucket.

---

## 14. SPECIFIC FAILURE MODES — and the workflow that blends both

### 14.1 The failure modes, named
1. **Non-manifold geometry.** Holes, self-intersections, degenerate faces, duplicate vertices. Not guaranteed by any vendor. TRELLIS.2 *by design* can emit non-manifold surfaces (it calls this a feature for open surfaces). **This breaks booleans, 3D printing, and any downstream simulation.** Meshy ships a free "Analyze Printability" and a 10-credit repair because this is endemic.
2. **No construction history.** The output is a frozen triangle list. You cannot say "make this plate 2mm thicker" or "change the segment count". Every revision is a re-generation, and the re-generation will differ everywhere, not just where you wanted.
3. **No parametric control.** Contrast with Sloyd (procedural) and Backflip (feature-tree CAD). This is *the* structural limitation of the diffusion approach and the reason the shield must be hand-modelled.
4. **Inconsistent scale.** Nothing outputs real-world dimensions. Two assets generated in the same session will not be in the same scale. `resize` endpoints impose a size; they do not discover one.
5. **Melted hard edges.** Diffusion smooths sharp features. Vendors claim improvements (Tripo's v3.0 Ultra release notes claim sharper edges; Rodin markets quads) but **no vendor publishes a benchmark**, and the failure is visible on any bevelled, machined, or cast edge.
6. **Hallucinated detail that contradicts engineering drawings.** The dangerous one, because it is *plausible*. It will invent bolt heads, put stiffeners where none existed, and add or omit rivet rows. **A viewer who knows the Thames Tunnel will see it, and the correction will cost you credibility, not just time.**
7. **Watertightness failures.** Blocks 3D printing, booleans, and any cleanup that assumes a closed volume.
8. **UV seams and texture-bake artefacts.** Seams land in arbitrary places; the Hunyuan3D port's own notes flag the **underside of unseen surfaces** as the weakest area of any multi-view bake. Expect visible seams exactly where you cannot hide them, and stretching on any surface the conditioning views did not see.
9. **The ground-plane hallucination.** Documented, reproducible failure: an object photographed with a visible shadow/floor reconstructs *with the floor as geometry*. Background removal keeps the horizon and you get a disc. **Mitigation: shoot/generate against a seamless backdrop, or crop before feeding the model.**
10. **The macOS GPU watchdog** (Apple Silicon only): kills long Metal kernels in the SLat decoder and surfaces as *"The decoder produced an empty mesh."* Not an install bug.

### 14.2 Workflows that blend generative and hand-built — in order of value

**(a) Generative → retopologise in Blender — the workhorse.**
Generate a rough organic form (rope coil, rubble, coal heap) → export GLB → import to Blender on the 3080 → retopo (Blender's QuadriFlow, or the vendor's own quad path) → bake the generated texture onto the retopo'd mesh → rig if needed.
**Why it works:** you keep the *form* and the *texture*, discard the topology. Best served by **Tripo (quad output, $0.45)** or **Meshy (quad remesh to 300K, $0.80)**.
**Caveat:** bake carefully. Neither vendor documents a high-poly→low-poly normal bake, so you are doing that step in Blender yourself.

**(b) Use it as a normal-map / displacement source on hand-built geometry — the highest-leverage trick for this show.**
**Model the shield by hand. Then use generative tools only for surface character.**
- Generate 20 variations of *riveted iron plate*, *pitted cast iron*, *weathered timber*.
- Extract the **normal and AO maps** (TRELLIS.2 bakes both from geometry; Hunyuan3D renders normals from the mesh).
- Apply them as tiling/trim-sheet detail onto your hand-built, dimensionally-correct geometry.
**Why this is the right answer:** it gets you the *visual density* that makes historical engineering look convincing, while every dimension, every rivet row and every segment count stays under your control. **The error that would embarrass you is designed out, because the geometry is yours.** This is where generative 3D earns its money on this production.

**(c) Texturing / retexturing hand-built meshes.**
Hunyuan3D-Paint is explicitly designed to texture **"either generated or handcrafted meshes"** — the README says so. Meshy has a Retexture endpoint (10 cr). **Run it on the 3080 in shape-free mode**: paint alone is 21GB on 2.1 (won't fit), so use the cloud/ComfyUI route or downgrade to a smaller paint config. Adobe Substance 3D Sampler does image→material without any mesh generation at all — **the safest, most controllable half of this technology.**

**(d) Backflip scan-to-CAD — for reference-accurate props, with one big caveat.**
If you can photograph a real object (a surviving shield component, a period tool, a museum replica), Backflip will reverse-engineer it into **editable parametric CAD with a feature tree** for ~$10 and 1–5 minutes, versus ~$1,500 of engineer time.
**Caveat, stated by the vendor's own coverage: it "excels at moderate-complexity 3-axis CNC milled and turned parts."** That describes a machined bracket or a turned fitting. **It does not describe a riveted, bolted, fabricated cast-iron segmental ring, and it certainly does not describe a timber-framed tunnelling shield.** Use it for *fittings and simple components*; do not expect it to reconstruct your hero object.

**(e) ComfyUI as the local pipeline.** If you want local generation on the 3080, the practical stack as of Sept 2026 is **ComfyUI native TRELLIS.2 nodes** (`nodes_trellis2.py`) with the **INT8 ConvRot checkpoint (5.25GB)**, optionally plus `Aero-Ex/ComfyUI-Trellis2-TiledDecode`. Expect reduced resolution. **This is a days-old, actively-changing area** — ComfyUI shipped TRELLIS memory reductions on 2026-09-02 and 2026-09-09.

**(f) The Blender addon loop.** Meshy's official addon (Pro+, Blender 4.2.6+, **macOS supported**) gives one-click generate→Blender plus **Make Manifold / Delete Small Pieces / normal correction** — i.e. it doubles as the cleanup stage you need anyway. Tripo's DCC Bridge covers Blender 4.1+ (8 DCC bridges total). **This is the tightest loop available and it runs on the M1.**

### 14.3 The recommended division of labour
| Stage | Where | Tool |
|---|---|---|
| Shot breakdown, asset list, Blender scripting | M1 | LLM agent + **`blender-mcp`** (28,832★, MIT, updated 16 Sept 2026 — executes arbitrary Python in Blender and already wires up Rodin + Hunyuan3D generation) |
| Hero geometry — **the shield, lining rings, riveted plate, timber centring, gear trains** | 3080 | **Blender by hand, driven by the agent via Python.** No generative 3D. |
| Surface detail for hero geometry | 3080 | **Generative normal/AO/displacement maps** (§14b). Hunyuan3D-Paint renders normals from *your* mesh; TRELLIS.2 bakes normal + AO from geometry. |
| Background filler, distant silhouettes, organic props, crowds, foliage, cloth | API | Tripo H3.1 ($0.30–0.45) / Meshy Smart Topology T2 (~2s, 5cr). **Cheap, forgiving, fast.** |
| Low-poly / quad-native forms for engine or rigging | API | **Rodin Gen-2.5 with explicit `mesh_mode: Quad`** (fal.ai $0.40/gen) or Tripo `quad` (+$0.05) |
| Materials and textures | API or 3080 | **Substance 3D Sampler image→material** (classical, not generative — removed in 5.1.2), Hunyuan3D-Paint / Meshy Retexture, Sloyd for generic props |
| Cleanup and retopo | 3080 or M1 | **Meshy Blender addon** (Make Manifold, Delete Small Pieces, normal correction) — or ComfyUI's native `FillHoles`/`WeldVertices`/`UnwrapMesh`/`DecimateMesh` node set |
| Local generation on the 3080 | 3080 | **ComfyUI native TRELLIS.2 nodes + INT8 ConvRot (5.25GB)**; optional `Aero-Ex/ComfyUI-Trellis2-TiledDecode`. ⚠️ Use the native path, not the reference pipeline (nvdiffrast/nvdiffrec are non-commercial-licensed) |
| Reference-accurate simple fittings | API | **Backflip** (.STEP output) — with the CNC-parts caveat and the tier-gated training opt-out |
| Licence gate | — | **TRELLIS/TRELLIS.2 (MIT, via ComfyUI native)** for anything that must be clean · **Tripo paid** for API convenience (no training on paid content) · **avoid Hunyuan3D open weights** if EU/UK/KR exposure · **know that Meshy and Backflip train on your data below their top tiers** · **do not rely on Adobe for 3D at all** |

---

## 15. OPEN ITEMS / LOW-CONFIDENCE REGISTER

| Claim | Confidence | What would settle it |
|---|---|---|
| **Adobe Firefly Boards "Convert 2D images into 3D assets"** — output format, GA/beta, credit cost, licence | **L — the single biggest gap** | Manual browser read of the help page while signed in (Akamai blocks scripted fetch; the page body truncates inside Adobe's nav). |
| Adobe Firefly Creative Production "3D digital twin workflows" | **L** | Same. |
| Whether Adobe's Firefly legal FAQ (indemnity scoped to *"features that generate imagery"*) has been re-issued since May 2024 | **L** | Adobe legal/indemnification page; no 2025–26 revision found. |
| Rodin HighPack official credit cost; the definition of "Smart Low-Poly"; whether an official Python SDK exists | **L** | Vendor docs (HighPack cost absent); PyPI check confirms no SDK. |
| **Backflip dimensional tolerance** (no ±mm figure published) | **L** | Ask Backflip; or reverse-engineer a known part and measure. |
| Backflip ToS: **which tiers qualify for Privacy Mode / Private Library Mode** training opt-outs | **L** | Backflip sales. **Relevant — the default grants them a training + redistribution licence.** |
| Whether Tripo/Meshy bake the normal map from high-poly geometry | **L** | Generate one asset each at the highest texture tier; compare normal map against silhouette detail absent from base colour. |
| Whether Tripo's "DCC Bridge for Blender" (claimed 4.1+) differs from the GitHub extension `tripo-3d-for-blender` (Blender 3.0+, v0.7.7) | **L** | tripo3d.ai blog is Cloudflare-403 to scripted fetch. |
| Meshy annual per-month USD; Studio seat arithmetic ($70 vs $10/seat) | **L** | Client-rendered pricing toggle / written quote. |
| Meshy raw pre-remesh poly count; Meshy credit-cost conflicts (Remesh 0 vs 5; Animation 0 vs 3) | **L / H that it conflicts** | Script `/openapi/v1/image-to-3d` and count faces; get a written quote. |
| Hunyuan3D generation latency on any consumer GPU | **L** | No vendor figure exists — benchmark locally. |
| Whether `--low_vram_mode` brings Hunyuan3D texture below its 21GB peak | **L** | Run 2.1 paint on a 12GB card with the flag; measure peak. |
| **Official VRAM/latency for native ComfyUI TRELLIS.2 / Pixal3D / TripoSplat** | **L** | ComfyUI publishes none. Benchmark on the 3080. |
| RTX 3080 feasibility for TRELLIS.2 INT8 + tiled decode at usable quality | **L** | Benchmark; no reported 3080 measurement exists. |
| Whether the Tencent Hunyuan3D Blender addon was updated beyond 2.0, or handles PBR | **L** | Repo check; the 2.1 README has no Blender section at all. |
| Alpha3D licence and exact output formats; Anything World poly counts/formats; Masterpiece X generator-output ownership | **L** | Direct vendor terms pages. |
| A general ComfyUI credit→USD rate (only Tripo's own `credits × 0.01` is documented) | **L** | Do not convert other providers' Partner-Node credits to dollars. |
| Stability's own per-generation 3D credit price (≈$0.10 is third-party) | **M** | Stability's API pricing page is client-rendered. |
| BlenderKit AI features (no documentation surfaced) | **L** | Do not claim any. |
| Hunyuan3D 2.5 weights' eventual release | — | **Confirmed absent as of 2026-09-17** (HF 401 / GitHub 404 / zero search hits). |

---

## 16. BOTTOM LINE

1. **Buy Tripo pay-as-you-go for bulk assets.** $0.30–$0.45 each, real Python SDK, **failure-refunded credits**, and — uniquely among the API vendors — a paid-tier commitment **not to train on your inputs and outputs**. For 40–80 assets an episode, budget **$12–$36**. *Or bypass Tripo's ToS entirely by buying through ComfyUI Partner Nodes (Tripo credits × $0.01) if you prefer not to hold an account.*
2. **Buy Rodin by the call, not the subscription, if you need quads.** **Rodin is the only vendor with genuinely native quad output and a 200,000-quad cap**, and **fal.ai resells Gen-2.5 at $0.40/generation standard and $0.10 fast** — cheaper than Rodin's own $1.00/credit with no monthly commitment. Rodin's output clause is also the most permissive reviewed (*"we will not limit your use of such Output"*), offset by a no-IP-warranty disclaimer and a one-way indemnity. **Note Gen-2.5 defaults to `Raw` (triangles) — you must explicitly set `mesh_mode: Quad`.**
3. **Buy one month of Meshy Pro ($20) for the Blender addon.** Official, free, **macOS-supported**, Blender 4.2.6+, and it gives one-click generate→Blender **plus Make Manifold / repair** — the cleanup stage you need regardless. Meshy's quad remesh (to 300K) and Smart Topology (native low-poly, 100–15,000 faces, ~2s) are the best production-topology features reviewed. **But know that Meshy trains on your inputs and outputs on every plan below Enterprise.**
4. **For the agent-driven Blender workflow, use `blender-mcp` (28,832★, MIT, updated 16 Sept 2026).** It is the dominant LLM↔Blender integration, it executes arbitrary Python in Blender, and it already wires up **Hyper3D Rodin and Hunyuan3D** asset generation — which is almost exactly the architecture described. Blender itself has **no** AI and none is planned; there are **zero** generative-3D vendor addons on Blender's official extension platform, so plan on ZIP/repo installs.
5. **Do not run diffusion inference on the M1 16GB.** An M4 Pro 24GB needs **5.7 min shape + 8.5 min texture with ~8GB of swap**. M1 16GB will thrash or abort. Use the Mac to drive APIs, run `blender-mcp`, and inspect GLBs.
6. **On the 3080, TRELLIS.2 via ComfyUI native nodes + the INT8 ConvRot checkpoint (5.25GB) is the only realistic local path** — and accept reduced resolution. **⚠️ Use ComfyUI's native integration specifically:** its own blog states the reference TRELLIS.2 pipeline depends on NVIDIA **nvdiffrast/nvdiffrec**, licensed for *"non-commercial research and evaluation"*, and that *"a studio couldn't ship assets from the reference pipeline without stepping into a legal gray zone"* — ComfyUI removed those dependencies. Hunyuan3D on 12GB is **shape-only**; its 21GB texture stage does not fit.
7. **Prefer TRELLIS/TRELLIS.2 (MIT) whenever output must be commercially clean** — the only reviewed option with no territory clause, no MAU threshold and no output restriction (subject to point 6's nvdiffrast caveat).
8. **Avoid Hunyuan3D open weights if anyone in the EU, UK or South Korea will see the output.** §5.c reaches **outputs**, not just weights, and calls non-Territory use *"unlicensed and unauthorized"*. The 1M-MAU threshold is a separate trigger. If you want Hunyuan3D, use the **paid cloud API**, which is a service contract, not a model licence.
9. **Do not plan around Adobe for 3D.** Adobe has **no shipping text-to-3D or image-to-3D** in Sept 2026: Substance 3D Viewer was **decommissioned 16 Oct 2025**, and **Sampler removed all generative AI in v5.1.2 (20 Nov 2025)**. Adobe's Firefly IP indemnity is scoped to *"features that generate imagery"* — **it does not cover 3D output** — and its exclusions (modification, combination with other materials, "the context in which you use the output") would void it for any Blender composite anyway. Substance remains useful for **image→material/texture extraction only**.
10. **Hand-model every object the audience can measure.** The shield, the segmental lining rings, the riveted plate, the timber centring, the gear trains. Then use generative tools for **normal/AO/displacement maps on that hand-built geometry** — the highest-leverage use of this technology here, and the one that cannot embarrass you.
11. **Dead or irrelevant — do not waste time:** **CSM** (domain dead, acquired by Google DeepMind) · **Luma AI Genie** (withdrawn; Luma is now image/video only) · **Kaidim/kaidim.com** (a Korean AutoCAD dimensioning plugin, not generative 3D) · **Anything World** (now Everything Universe; auto-rigging, API requires written authorisation) · **Masterpiece X** (now WorldEngen; API early-access only).
12. **Never let the tool invent engineering.** The audience for a historical-engineering channel is precisely the audience that can tell a wrong segment count from a right one. Generative 3D buys you speed on things nobody measures, and costs you credibility on things they do.
