# Brunel — Production Roadmap

> A harness for making engineering-history animation that gets measurably better every episode.
> One person. One Mac. One Windows render node. DeepSeek in the loop.

---

## 0. What this repo is

This is not a video project. It is a **ratchet**: a set of versioned, executable artefacts that
every episode consumes and none rebuilds. Episodes are the symptom; the ratchet is the asset.

The north star: **in twelve months, output that reads as premium factual animation, still run by
one person plus an LLM.** The LOOK is reachable. The studio PROCESS is not — dailies, supervisor
sign-off and layered coupled simulation are an organisation, and one person plus agents is not an
organisation. Say which tier each episode actually holds. The genre's currency is accuracy, and a
channel that overstates its own tier has already spent it.

---

## 1. Thesis

Quality compounds only when the artefacts encoding judgement are versioned, executable and reused.

Three consequences, and they are the opinionated core:

**1. The model is the interchangeable part; the harness is the moat.**
The LLM writes a diffable spec. Only deterministic Python writes `bpy`. This confines Blender API
drift to one file, makes the artifact human-reviewable *before* render, and gives reproducibility
from `hash(spec) + toolchain pin`.

**2. Automate generation, never adjudication.**
A multimodal critic scores renders against written rubrics and proposes an RFC 6902 JSON Patch
against the spec. It is **advisory**. The human gate is mandatory. The human owns the hook, the
last line, and the hero frame — the three things that carry a video.

**3. Score renders, not code.**
A script that runs is not a shot that works. The critic scores output, never "did it execute".

---

## 2. The three visualisation modes

Every episode draws on all three. Episode 1 must exercise all three so all three templates exist.

| Mode | What it does | Blender levers |
|---|---|---|
| **A — Cinematic reconstruction** | "You are there." Period light, human scale, air. | HDRI + motivated practicals, volumetrics, DOF, camera moves with ease |
| **B — Technical cutaway** | Explains the mechanism. Section, exploded, cycle. | Real boolean/knife section, exploded states, joint rigs, orthographic option |
| **C — Diagram / data** | Plans, sections, dimensions, timelines, comparison. | Geometry-node dimension callouts, orthographic cameras, typography |

---

## 3. Machine topology

```
MAC M1 (control plane, 16 GB, ~19 GB free)          WINDOWS PC (render node, RTX 3080)
  - authoring, git (sole committer)                   - Cycles/OptiX final frames
  - spec DSL + compiler + assertions                  - NVENC encode + mux
  - bpy-as-module: build + structural tests           - bounded render queue, resumable
  - factgate, licencegate, critic, captions           - NEVER edits source
  - low-fi preview renders (the MVP path)
```

**Communication, four rules, no exceptions:**

1. **Source travels by git.** Mac compiles `spec -> .blend + manifest.json`, commits, node pulls.
2. **Control travels by SSH.** `brunel render submit` runs a thin, restartable worker on the node.
3. **Frames do not travel.** Small artefacts return; pixel plates stay on the node.
4. **Nothing renders on the Mac except previews.** The M1 is for authoring and adjudication.

---

## 4. Maturity ladder

Observable, checkable exit criteria. You can look at a render and say yes or no.

| Level | Name | Hours/ep | Cash/ep | Adds |
|---|---|---|---|---|
| **L0** | Scrappy | 15 h | ~$8 | A shipped video and a sourced subject. Nothing else. |
| **L1** | Structured | 30 h | ~$20 | Craft discipline as machine-checkable assertions. |
| **L2** | Competent solo Blender | 70 h | ~$55 | Parameterised asset kit + 3D-anchored annotation. |
| **L3** | Strong independent | 160 h | ~$180 | One simulated element per episode; previs before final render. |
| **L4** | Broadcast / premium factual | 380 h | ~$700 | Multi-pass + comp script per shot; light sculpting; 200% crop. |
| **L5** | Hollywood-esque | 900 h | ~$4,000 | A versioned stage pipeline; coupled simulation; formal review. |

### L0 — SCRAPPY (Episode 1)

- [ ] One `.blend` per episode, ≤10 assets, procedural or flat colour, no external textures
- [ ] 6–8 shots per 72 s; every shot static or a single move; no move with BOTH translation and zoom
- [ ] One sun/HDRI plus one fill; no light linking
- [ ] Principled BSDF with base colour + roughness only; no normal maps
- [ ] **1 Blender unit = 1 m**, and every hero dimension within ±10% of a cited primary source
- [ ] ≥1 dead frame per 10 s (a held frame carrying no motion, no VO, no new information)
- [ ] Audio = 2 layers (VO + one music bed); zero SFX
- [ ] Captions burned in, may sit in the bottom 350 px
- [ ] 1080×1920, ≤90 s, H.264, under 50 MB
- [ ] ≥1 primary source cited in the description

### L1 — STRUCTURED

- [ ] A written shot list exists **before** modelling, each shot with stated purpose and duration
- [ ] Every camera move has ease in AND ease out (a Linear handle on a camera move is an automatic fail)
- [ ] 180° shutter honoured (Cycles motion blur shutter = 0.5)
- [ ] One lighting rig reused across a sequence, with a documented unchanged sun angle
- [ ] Materials carry base colour + roughness + a normal, verified against a 1 m reference cube in-scene
- [ ] **Zero dead frames**; every cut motivated by a new fact, a change of scale, or a change of subject
- [ ] Cut points land on VO word boundaries
- [ ] Audio ≥3 layers (VO, music, ≥1 diegetic SFX per on-screen action); VO at −14 LUFS integrated, −1 dBTP
- [ ] Captions confined to the central 1320 px; one typeface, two weights, locked baseline
- [ ] A single declared view transform held for the whole episode
- [ ] `factgate` exits 0

### L2 — COMPETENT SOLO BLENDER

- [ ] Every assembly has a modelled exploded state AND an assembled state — real geometry, not opacity
- [ ] Cutaways are real geometry (boolean or knife), never a clipped viewport
- [ ] Parts named and labelled in 3D; labels parented or tracked, never hand-keyed in the edit
- [ ] Real declared focal lengths on a full-frame-equivalent sensor with a wide/medium/long mix (all-50 mm is a fail); DOF on ≥1 heroic close-up
- [ ] Every light is visible in-scene or justified by the story
- [ ] Every hero surface has ≥1 roughness or normal break-up map
- [ ] Correct scale demonstrated by a human silhouette or dimension callout
- [ ] Average shot length 4–8 s, with match cuts on shape or motion
- [ ] Audio = 4 layers; music ducks −6 to −9 dB under VO
- [ ] A **written colour script**, one palette per act, checked against the render
- [ ] Provenance sidecar for every asset; `licencegate` exits 0

### L3 — STRONG INDEPENDENT

- [ ] Previs as thumbnails/storyboards AND an animatic cut against the REAL VO before any final render
- [ ] Camera animation hand-curated so no two shots share a move
- [ ] ≥1 physically simulated element per episode that interacts with hero geometry
- [ ] Volumetrics where motivated (dust, steam, spray)
- [ ] Repeated elements instanced not duplicated, with LOD discipline holding render in budget
- [ ] ASL 3–6 s with J and L cuts, ≥1 match cut, ≥1 designed reveal; no shot opens on a static frame
- [ ] Audio ≥5 layers with distinct per-location ambience and foley per mechanism
- [ ] ACEScg (or Linear Rec.2020) working space declared at project start, per-act LUT
- [ ] Grade and mix are separate later passes from animation
- [ ] Canary reel ≥7 shots and green

### L4 — BROADCAST / PREMIUM FACTUAL

- [ ] Surfacing holds at the scale the camera sees; no visible tiling at 100% crop
- [ ] Secondary animation everywhere (cables flex, water shows surface tension, dust settles)
- [ ] Lighting motivated AND sculpted — light linking, negative fill, practicals, deliberate per-shot contrast
- [ ] Lens, height and move each carry meaning; handheld/percussive where the story wants tension
- [ ] Every shot survives a **200% crop** for geometry, texture and motion artefacts
- [ ] ASL 2.5–5 s, no repeated composition, designed transitions
- [ ] Full DX/MX/FX/AMB stem mix at −14 LUFS whose dynamic range breathes
- [ ] Per-act colour script, scopes-checked for clipping, graded for sRGB and P3/HDR
- [ ] A comp script per shot and a review log with version notes

### L5 — HOLLYWOOD-ESQUE

- [ ] A published, versioned stage pipeline where assets, looks and shots are separate layers and a shot is **reassembled** rather than hand-built
- [ ] Coupled, layered simulation (FLIP + rigid + vellum interacting) with a cache per layer and a documented iteration budget
- [ ] Subsurface, volumetrics and lens artefacts artistically controlled, not defaulted
- [ ] Show-specific custom tooling (procedural rigs, macros, shot-specific solvers)
- [ ] Formal review — dailies, shot status, version notes, supervisor sign-off
- [ ] Twelve months of eval ledger rows show monotonic improvement in the declared headline metric

---

## 5. The ratchet — artefacts produced and never rebuilt

| Artefact | Purpose | Created |
|---|---|---|
| `toolchain.lock.json` | Pins Blender/bpy/Python/ffmpeg. API drift is the #1 measured failure mode. | Day 1 |
| `harness/` — spec DSL + compiler + assertions | The only thing that writes `bpy`. Localises drift; makes the artifact reviewable pre-render. | Days 2–5 |
| `skills/blender-api/SKILL.md` | Version-stamped list of what actually changed, told to the model rather than expected of its memory. | Day 1–2 |
| `library/GEN/` — parameterised asset kit | The compounding asset. `shield_frame` is parameterised `frames × cells_per_frame` — E1 uses 12×3, and the same shape serves Greathead's 1869 Tower Subway shield. | Episode 1 |
| `library/MAT/` — procedural material masters | Victorian brick, cast iron, wrought iron, oak, pine, hemp rope, canvas, coal smoke, gas flame. Kills the "grey plastic" tell. | Ep 1–3 |
| `library/SHOTS/` — parameterised shot templates | Authorship moves from shots to templates: Episode N's shot 4 becomes a parameter diff. | Ep 1, then 1/quarter |
| `goldens/canary/` | The regression gate. Cycles is not bit-reproducible, so hash testing is a mirage — use SSIM + LPIPS at fixed seed. | Episode 1 |
| `qa/rubrics/*.md` | The tier checklist *is* the rubric. | Episode 1 |
| `facts/epNN.facts.json` + `factgate` | The accuracy product, made mechanical. Written **before** the script. | Episode 1 |
| `render-bench.json` | Replaces every estimated number in this roadmap with a measured one. | Day 3 |
| `legal/licences.json` | Per-asset source, licence, URL, retrieved date, modifications, plus a dated screenshot of the licence page. | Episode 1 |
| `LESSONS.md` | Every entry carries an executable check, or it does not belong here. | Continuous |
| `eval/` | The eval ledger. The only evidence accepted in a retrospective. | Episode 1 |

**Regression rule:** every merge renders the canary. Pass = SSIM ≥ 0.98 AND LPIPS ≤ 0.05 per shot,
with no shot degrading more than 20% of its previous margin.

---

## 6. Episode 1 — Brunel's tunnelling shield, Thames Tunnel (1825–1843)

**Scope:** 8 shots · 72 s · 1080×1920 · 30 fps · **L0 quality, deliberately flat.**

| # | Shot | Mode | Difficulty |
|---|---|---|---|
| 1 | Wapping/Rotherhithe, 1825 — the ferry problem, the docks, the river | A | Low |
| 2 | Shipworm boring submerged timber — the inspiration | B (macro) | Low |
| 3 | The 50 ft iron ring sinking under its own weight; 50,000 bricks piled on when it jams | A | Medium |
| 4 | **The shield in section — 12 frames × 3 levels = 36 cells** | B | **Hero** |
| 5 | One cell's cycle: board out → dig → board in → prop → two screws advance against the brickwork | B | Medium |
| 6 | Miners forward, bricklayers lining behind — simultaneously | B | Medium |
| 7 | 12 January 1828 — the flood, six men dead, Isambard pulled out unconscious | A | Med-high |
| 8 | 1843 pedestrian arcade → 1869 railway → TfL train today | C + A | Low |

**Explicitly OUT of scope for Episode 1:** no faces; no coupled fluid sim (animate the flood +
volume + debris as separate layers); no textured hero assets; no colour script; no crowds; no
voice cloning; no YouTube long-form cut.

**Must ship as reusable assets:** `toolchain.lock.json`, compiler MVP, `GEN_shield_frame`,
`GEN_brick_bond`, `MAT_*` masters, `CHR_worker_scale` (1.70 m reference figure), 2 shot templates,
6-shot canary reel, `facts/ep01.facts.json` + passing `factgate`, `legal/licences.json`.

---

## 7. Twelve-month plan

Cadence is **monthly, not weekly.** See §9 for why.

| Quarter | Ships | Capability goal | Level |
|---|---|---|---|
| **Q1** Oct–Dec 2026 | Ep 1–2 | Harness exists; publishing spine is code | L0 → L1 |
| **Q2** Jan–Mar 2027 | Ep 3–5 | Asset kit pays back; annotation system; first reusable templates | L1 → L2 |
| **Q3** Apr–Jun 2027 | Ep 6–8 | One simulated element per episode; previs loop | L2 → L3 |
| **Q4** Jul–Sep 2027 | Ep 9–12 | Flagship pushed to L4: multi-pass, comp scripts, stem mix | L3 → L4 |

**Definition of done per quarter:** the canary is green, the eval ledger has 3 new rows, and the
benchmark shot has been re-rendered and compared.

---

## 8. The benchmark shot

Shot 4, **"The Board"** — the shield in section.

Re-rendered at the start of every quarter from the *current* asset kit, at fixed camera, fixed
lighting rig and fixed settings. Only the toolchain and the assets improve. Compare SSIM/LPIPS and
put both frames side by side in `eval/`.

This is the compounding proof. Without it, "each video is better" is a feeling.

---

## 9. The constraint that binds the schedule

A 72-second episode at 30 fps is **2,160 frames.**

On an RTX 3080 at 1080×1920, Cycles at 128 samples plus OptiX denoise, a mid-complexity
engineering scene is plausibly **20–45 s/frame** → **12–27 hours of pure GPU time for one final
pass.** Revision is where quality comes from; three iterations is 36–80 hours.

Two hard consequences:

1. **The render node binds the schedule** — not the LLM, not your time on the Mac.
2. **Rendering at exactly 1080×1920 is mandatory.** Never render big and downscale.

Also: a 3080 has 10–12 GB, and tunnel interiors with volumetric dust plus instanced brickwork will
exceed it. On current Blender an OptiX VRAM overrun **falls back to system memory rather than
erroring**, so it presents as a mysterious 10× slowdown, not a failure. Monitor
`--cycles-print-stats` memory per frame and alert on it.

**These numbers are estimates and must be replaced by `render-bench.json` on day 3.**

---

## 10. Budget, year one

| Item | Cost | Cadence |
|---|---|---|
| ElevenLabs Creator (commercial rights + professional voice cloning) | $22 | monthly |
| DeepSeek API | ~$5–15 | per episode |
| Music licence | $180–300 | annual |
| Cloud GPU burst (fallback only) | $100–300 | annual |
| 2 TB SSD for the render node | ~$150 | one-off |
| Blender, FreeCAD/CalculiX, ffmpeg | $0 | — |
| **Cash total** | **~$900–1,300** | |
| **Your time** | **~800 h** | *the real cost* |

Commercial rights start at ElevenLabs **Starter ($5/mo)**, but **professional voice cloning
requires Creator ($22/mo)** — and voice consistency across twelve months is the actual reason to
pay, not marginal naturalness.

---

## 11. Risk register

| Risk | Severity | Mitigation |
|---|---|---|
| Building the harness forever, never shipping | **High** | Episode 1 ships by **day 21** at L0. No exceptions. This is the single biggest risk. |
| Render node kills cadence | **High** | Measure before planning (`render-bench.json`); monthly cadence; EEVEE for all previews; per-shot re-render |
| Instagram deboosts / labels AI content | **High** | Disclose deliberately and consistently; a narrated engineering animation is not an AI persona, but verify exact label mechanics before launch |
| Being confidently wrong about engineering | **High** | Fact ledger + `factgate` + primary sources cited in the caption |
| LLM API drift breaks the generator | Medium | `toolchain.lock.json`, scene DSL, golden fixtures |
| VRAM overrun presenting as a slowdown | Medium | `TdrDelay=60` on Windows; texture cache; monitor per-frame memory |
| Burnout against the ~800-hour reality | Medium | Monthly not weekly; templates; stop at L3 if L4 stops being fun |
| Sunk-cost trap in the DSL | Medium | Count escape hatches per episode; if the count trends up, the DSL is wrong |

---

## 12. Weekly division of labour

**Human owns:** art direction and the hero frame; the hook and the last line; animatic review;
final grade approval; publishing; the `LESSONS.md` entry.

**Agents own:** research and dossier; beat sheet; shot list; spec authoring; compiler runs;
assertion fixes; previs renders; critic pass + JSON patch; caption timing; encode.

---

## 13. First seven days

1. Install Blender 5.2 LTS on Windows. `pip install bpy==5.2.2` on the Mac (needs **Python 3.13
   exactly**). Create the repo. Write `toolchain.lock.json`.
2. Set `TdrDelay=60` under `HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers`. Prove one
   headless OptiX render over SSH.
3. **Measure `render-bench.json`** — real seconds/frame at 16 / 64 / 128 spp. Everything downstream
   reads this file. Do it before anything creative.
4. Spec DSL schema + `compile.py` (meta, parts, cameras, shotlist).
5. `GEN_shield_frame` (12×3) + `GEN_brick_bond`; compile a test scene.
6. `facts/ep01.facts.json` from the verified dossier; run `factgate`.
7. Previs shot 4 at 16 spp. **Look at it.** Then build the other seven.

Then: ship by day 21.

---

## 14. Verification status

Checked against primary/near-primary sources on 2026-09-17.

**Verified:**

- Blender **5.2 LTS** released 14 July 2026, supported to July 2028 — the correct long-arc pin
- Cycles **texture cache** ships in 5.2 (the thing that makes a 10 GB card viable)
- Experimental Geometry Nodes cloth/hair physics in 5.2
- Remote-hosted asset libraries in 5.2 (multi-machine kit distribution)
- `bpy` installable from PyPI (5.2.x)
- ElevenLabs Creator $22/mo, 100k credits, professional voice cloning; commercial rights from $5
- Reels: 1080×1920, 9:16, H.264, 30 fps, 5–8 Mbps; top 250 px / bottom 350 px blocked → central
  1320 px safe zone
- Instagram is actively limiting reach for **undisclosed AI profiles** and has renamed its AI
  creator label

**Corrected from the research pass:**

- Shield dimensions are **37 ft 6 in × 22 ft 3 in** in cast iron (not "38 × 22"). Finished bore is
  35 ft × 20 ft × 1,300 ft, 75 ft below high tide.
- The January 1818 patent was granted to Brunel **and Lord Cochrane**.
- There were **two** floods: 18 May 1827 at 549 ft, and 12 January 1828, which killed **six men**.

**Still unverified — do not repeat publicly:**

- The r = +0.481 / r = +0.956 correlation figures (the benchmarks are real; the numbers are unchecked)
- Blender MCP production-readiness and reliability
- Sketchfab ToS clauses
- 2026 cloud GPU prices per hour
- The specific `bpy` breaking-change list
- **Exact Instagram AI-label mechanics**
- **Every render-time figure in this document** — that is what `render-bench.json` is for
