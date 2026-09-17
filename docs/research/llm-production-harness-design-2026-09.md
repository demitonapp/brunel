# LLM-Driven Production Harness — Design
### Client: solo creator, historical-engineering Instagram channel. Episode 1 = Marc Brunel's tunnelling shield, Thames Tunnel 1825–1843.
As-of: **17 September 2026**. Companion to `blender-pipeline-research-2026-09.md` (facts), `gpu-pricing-2026.md` and `.dsh-research/blender-render-economics-2026.md` (render economics).

Confidence tags: **[H]** primary source or own computation · **[M]** derived/reasoned · **[L]** judgement or unverified.

---

## 0. The one architectural decision everything else follows from

**The MCP servers are for interactive authoring. The batch pipeline must never use them.**

Every Blender MCP server in existence drives a *live, GUI Blender session over a socket*. `mcp-for-blender` (the renamed `blender-mcp`, 27.2k stars) states plainly that under `blender -b` headless, commands "never execute" — a GUI or `xvfb-run` is required. The protocol is request/response with a 180 s socket timeout. `HoldMyBeer-gg/blend-ai` documents "no real-time feedback … no streaming of viewport updates or render progress" and no MCP-level undo. **[H]**

That is a fatal profile for a 7,200-frame batch render. So:

- **Interactive path (control plane, M1):** MCP server + Blender GUI when the creator is art-directing by hand, or when an agent is doing exploratory blocking. `blender-ai-mcp` (PatrykIti) is the one to use here — it is the only server built around *deterministic truth* (`scene_measure_*`, `scene_assert_*`, `scene_view_diagnostics`) rather than free-form code.
- **Batch path (render node, Windows PC):** bare `blender --background --python compile.py -- spec.yaml`, then `blender -b scene.blend -a`. No MCP, no socket, no GUI, no timeout. **[H]** for the CLI form; **[M]** for the recommendation.

Everything below assumes that split.

---

## 1. (a) State of AI-agent control of Blender, September 2026

### 1.1 The servers that actually exist

| Project | Scale / status | Blender | What it actually is | Verdict |
|---|---|---|---|---|
| **Blender Lab official MCP** — `projects.blender.org/lab/blender_mcp`, blender.org/lab/mcp-server | Add-on **v1.0.3**; `.mcpb` bundle | **requires 5.1+** | Scene analysis, debugging, doc lookup, datablock renaming, GN explanation | Toy for authoring; **explicitly unguarded** |
| **`mcp-for-blender`** (ahujasid, formerly `blender-mcp`) | **~27.2k stars**, PyPI pkg renamed, **v2.0.0 (2026-09-16)**, 31 tools + 1 prompt | 3.0+ (Blender 3.0+, recommends pinning Python 3.11) | Socket addon (`localhost:9876`) + `uvx` MCP. `execute_blender_code`, viewport screenshot, Poly Haven / Sketchfab / Poly Pizza / Hyper3D Rodin / Hunyuan3D asset pulls, GLB/FBX export, `bpy_api_lookup` | **Toy for production.** GUI-only, 180 s timeout, no auth |
| **`blender-ai-mcp`** (PatrykIti) | Apache-2.0, FastMCP **3.2.4** + pydocket **0.19.x**, Python 3.11+ | **E2E tested on 5.0**, addon min 4.0 | Goal-first router (`router_set_goal`), macro tools, **deterministic measure/assert truth layer**, pluggable VLM runtimes (MLX Qwen3-VL-4B local; OpenRouter; Gemini) | **Closest thing to production-shaped** |
| **`blend-ai`** (HoldMyBeer-gg) | AGPL-3.0, **164 tools / 24 modules**, 12 expert prompts | 4.2+, tested against 5.1 | Sandboxed code exec (25 blocked imports), zero telemetry | Good tooling, **no undo, no streaming** |
| **`carlosh7/blender-mcp`** ("ultra") | MIT; tool count self-inconsistent (239 vs 248) | 4.2+/5.x | **Headless-ready**, stdio/SSE/HTTP, VLM feedback loop, AST blocklist + auth token | Best headless story |
| `sandraschi/blender-mcp`, `RFingAdam/mcp-blender` (218 atomic tools), `zorak1103`, `djeada`, `bpype`, `bpy-dev` | various | various | — | Not evaluated |

**[H]** for B1/B2 rows (primary READMEs + PyPI JSON). Not one of these is production-viable as a *render pipeline*; the official one is honest about it.

### 1.2 The benchmark evidence — 3DCodeBench

The current reference is **3DCodeBench** (Google DeepMind + Google Research + USC) — **arXiv:2606.01057**, https://www.3dcodebench.com. It scores models writing **Blender 5.0 Python** to build **212 procedural object categories**: **81,605 scripts across 82,042 trials**, 12 frontier VLMs, plus 2,767 coding-agent transcripts.

| Model | Blender 5.0 executability | Human-preference Elo | Mean list price/query |
|---|---|---|---|
| Claude Opus 4.7 | **0.881** | 1008 | $0.14 |
| GPT-5.5 | 0.873 | **1167** | $0.25 |
| GPT-5.4 | 0.863 | 1074 | $0.17 |
| Claude Sonnet 4.6 | 0.792 | 1022 | $0.30 |
| Gemini 3.1 Pro | 0.693 | 1149 | $0.16 |
| Gemini 3.5 Flash | **0.410** | 1112 | $0.05 |
| Gemini 3.1 Flash Lite | 0.599 | 880 | $0.01 |

Three findings from that paper govern this whole design **[H]**:

1. **"Failures mostly arise from API mismatches."** Not geometry, not intent — the model invents or mis-remembers `bpy`.
2. **Successful renders still suffer from "disconnected or floating 3D geometric components."** The code ran; the object is in pieces.
3. **"Physical Plausibility supersedes Executability."** Executability correlates with human-preference Elo at only **r = +0.481**. Code that runs is not code that looks right.

### 1.3 Failure modes, ranked, with severity for *this* pipeline

| # | Failure | Evidence | Severity here |
|---|---|---|---|
| 1 | **API hallucination / version drift** | 3DCodeBench abstract; blender-ai-mcp failure mode #1 | **Critical.** Blender 5.0 removed `scene.node_tree`, renamed `BLENDER_EEVEE_NEXT`→`BLENDER_EEVEE`, deleted the legacy Action API (`action.fcurves`/`action.groups`/`action.id_root` → channelbags + `action_slot.target_id_type`); 5.1 renamed VSE strip time props and moved to Python 3.13; **5.2 changed the Geometry Nodes modifier API** — custom props are gone, use `modifier.properties.inputs.<id>.value` |
| 2 | **Context-sensitive operator failure** — `bpy.ops` needs the right active object / mode / selection | blender-ai-mcp | High; kills scripted construction silently |
| 3 | **Disconnected / floating geometry** | 3DCodeBench | **Critical for a machine** — a shield whose 36 jacks float off the frame is worthless |
| 4 | **No real-time feedback; 180 s socket timeout; no MCP-level undo; headless traps** | mcp-for-blender, blend-ai READMEs | High |
| 5 | **Arbitrary code execution, no auth** | Official Blender MCP: "will execute LLM generated code in Blender without any guards"; mcp-for-blender socket has no auth/encryption | High if the render node holds anything |
| 6 | **Context explosion** | RFingAdam's 218 atomic tools; blender-ai-mcp ships `llm-guided` as a deliberately tiny search-first surface for exactly this reason | High |

### 1.4 Verdict

**Toys for authoring. Nothing here is production-viable for rendering.** The only defensible architecture is: use a truth-layer MCP server for interactive work, and drive batch renders through `blender --background` from a compiled scene. Reward the one thing the ecosystem got right — blender-ai-mcp's insight that **"vision assists interpretation, while deterministic measurement and assertions provide the final truth layer."**

---

## 2. (b) Domain-specific scene DSL — **FOR, decisively**

### 2.1 The argument

The case for free-form `bpy` is that it has no ceiling. The case against it wins on five specific points, each grounded in the evidence above:

1. **API drift is the #1 failure (3DCodeBench).** A DSL compiler absorbs version churn in *one* file. A free-form generator absorbs it in every prompt, every cached example, and every model's pretraining.
2. **Executability ≠ quality (r = 0.481).** A spec is reviewable by a human *before* render; 800 lines of generated `bpy` is not. The art director must be able to read and diff the artifact the LLM edits.
3. **Determinism is impossible without a stable input.** Regression testing needs `hash(spec) + toolchain-pin` to reproduce a `.blend`. Free-form code has no canonical form — two runs differ in variable names, ordering, and float formatting.
4. **No idempotence, no partial recompile.** A spec compiler can recompile *one shot*, or *one part*, without touching the rest. A monolith script cannot.
5. **Schema is the mitigation for hallucination.** See §4.3.

**The honest counter-argument:** DSLs cap the ceiling, and a real shot sometimes needs a bespoke effect. The resolution is that the DSL *is* Python — a typed pydantic model graph, expressed in YAML for review — with a bounded `escape_hatch` block that must carry a written justification, is compiled to a pinned blob, and is flagged for review. Escape hatches are allowed but *visible and counted*. If escarpment count per episode rises, the DSL is wrong and gets extended.

### 2.2 Sketch: what the DSL must contain for engineering machinery

Design rules: every length carries a unit; every placement is **relative to a named parent** (never an absolute world coordinate computed by the model); every part has an identity that survives to the render and into the QA report; nothing is derivable — anything the compiler can compute, the compiler computes.

```yaml
# episodes/ep01-thames-shield/scene/shield.yaml
spec_version: "1.3.0"          # compiler contract; mismatched major => refuse to build
meta:
  episode: ep01
  title: "Brunel's Tunnelling Shield, 1825"
  historical_sources: [sms-cc0-oliver-evans-1804, brunel-collection-icelib]
  accuracy_notes: "Dimensions from [source]; cell count commonly given as 36 in 3 tiers of 12."
  licence: {models: CC0, textures: CC0, audio: "ElevenLabs commercial"}

units: {system: metric, angle: degrees, up_axis: Z}
accuracy_profile: docudrama    # strict | docudrama | stylised — drives which QA gates apply

# ---- 1. PARTS -------------------------------------------------------------
# Every part is either procedural (parametric), cad (CadQuery/Build123d via
# blendquery), instanced (from the component library), or imported (CC0 scan).
parts:
  - id: shield_frame
    source: {kind: cad, model: "cad/shield_frame.py", driver: build123d}
    params:                       # the ONLY numbers a human/LLM should argue about
      width_m: 11.5               # [M] verify against Brunel archives
      height_m: 6.8
      tiers: 3
      cells_per_tier: 12
      cell_w_m: 0.95
      cell_h_m: 2.05
      frame_section_mm: 150
      material_ref: cast_iron
    produce: [cells, jack_bosses, bolt_flanges]
    evidence: {claim: "36 cells, 3 tiers x 12", confidence: medium,
               would_settle: "ICELIB Brunel letterbook + shield elevation drawing"}

  - id: screw_jack
    source: {kind: procedural, module: "lib/mech/screw_jack.py",
             params: {stroke_mm: 300, thread: "acme_2in", body_len_mm: 620}}
    material_ref: wrought_iron
    reusable: true                # => promoted to the component library on pass

  - id: poling_board
    source: {kind: procedural, module: "lib/timber/poling_board.py",
             params: {len_mm: 2400, width_mm: 230, thick_mm: 75}}
    material_ref: oak_green

  - id: thames_silt
    source: {kind: procedural, module: "lib/geo/silt_volume.py",
             params: {grid_m: 40, depth_m: 12, noise_seed: 4101}}
    material_ref: river_silt_wet

# ---- 2. HIERARCHY --------------------------------------------------------
# Explicit parent/child. The compiler emits real Blender collections AND
# parent relationships, so "floating geometry" is a compile error, not a
# surprise at render.
hierarchy:
  root: shield_rig
  tree:
    shield_rig:
      - shield_frame
      - jacks:  {from: screw_jack, count: 36, pattern: grid, of: shield_frame.cells,
                 transform: {axis: +Y, local_offset_mm: [0, 0, 250]}}
      - poling: {from: poling_board, count: 24, pattern: fan, of: shield_frame.cells.top_row}
      - lining: {from: cast_iron_ring, count: 12, pattern: along_path, path: tunnel_axis}
  attach_rules:                   # hard constraints the compiler MUST assert
    - {child: jacks, parent: shield_frame, rule: contact, tolerance_mm: 2}
    - {child: poling, parent: shield_frame, rule: supported_pair}

# ---- 3. JOINTS -----------------------------------------------------------
# Kinematic intent. Drives both animation authoring and geometric assertion.
joints:
  - {id: jack_advance, type: prismatic, part: jacks, axis: +Y,
     limits_mm: [0, 300], default_mm: 0}
  - {id: ring_lower_1, type: hinge, part: lining[0],
     axis: [1,0,0], limits_deg: [0, 8]}
  - {id: shield_body, type: rigid, part: shield_rig}
# joints are compiled to: (a) object constraints for animation,
# (b) scene_assert_* checks that run in CI.

# ---- 4. MATERIALS --------------------------------------------------------
materials:
  cast_iron:   {model: pbr_principled, base_color_srgb: [0.09,0.09,0.10],
                metallic: 0.85, roughness: 0.62, bump: {texture: "CC0 iron_cast", scale: 2.0},
                age_ramp: {rust: 0.15, soot: 0.0}}
  wrought_iron:{model: pbr_principled, metallic: 0.90, roughness: 0.45}
  oak_green:   {model: pbr_principled, base_color_srgb: [0.22,0.18,0.11],
                roughness: 0.78, moisture: 0.35}
  river_silt_wet: {model: pbr_principled, base_color_srgb: [0.10,0.08,0.06],
                roughness: 0.28, displacement: {scale_m: 3.2, strength: 0.4}}
lighting_rig:                     # a reusable, versioned rig, not per-shot ad hoc
  hdri: {ref: "CC0 polyhaven industrial_basement_4k", strength: 0.9}
  practicals:
    - {type: area, id: lamp_oil_row, count: 8, pattern: along_path, path: shield_front,
       power_w: 40, color_k: 2200, falloff_m: 6}
    - {type: spot, id: hero_rake, target: shield_frame, azimuth_deg: 38,
       elevation_deg: 22, power_w: 800, color_k: 5200, size_m: 1.8}

# ---- 5. CAMERAS ----------------------------------------------------------
cameras:
  - {id: cam_wide_43, lens_mm: 32, sensor_mm: 36, aperture_f: 4.0,
     position: {relative_to: shield_frame, offset_m: [-6.5, -7.2, 2.4]},
     aim: {target: shield_frame, framing: "leading_lines_low"}}
  - {id: cam_cell_mcu, lens_mm: 65, aperture_f: 2.8,
     position: {relative_to: jacks[17], offset_m: [0.55, -0.9, 0.1]},
     aim: {target: jacks[17].boss, framing: "over_shoulder_miner"}}
  # RULE: cameras are positioned relative to *named parts*. Absolute world
  # coordinates are never authored by the LLM — that is where spatial
  # reasoning fails (§4.1).

# ---- 6. SHOT LIST --------------------------------------------------------
# Single source of truth for editorial. Compiles to: Blender timeline markers
# AND an OpenTimelineIO (.otio) timeline for the edit.
shotlist:
  - {id: sh010, dur_s: 4.2, cam: cam_wide_43, move: {type: slow_push, dolly_m: 1.2},
     beat: "the machine revealed", narration_cue: n010,
     references: [ref_thames_shield_elevation, ref_icelib_plate_04],
     render: {samples: 128, denoise: optix, priority: hero}}
  - {id: sh011, dur_s: 3.0, cam: cam_cell_mcu, move: {type: handheld_sway, amp_mm: 12},
     beat: "one man, one cell", narration_cue: n011, render: {samples: 64, priority: standard}}

# ---- 7. ANNOTATIONS ------------------------------------------------------
# Burned-in captions + on-screen labels. Machine-readable so timing can be
# validated against the audio, not eyeballed.
annotations:
  captions:
    source: asr                       # whisper.cpp v1.9.4 forced-align on ElevenLabs audio
    style: {font: "Inter SemiBold", size_px: 58, fill: "#FFFFFF",
            outline_px: 4, outline: "#000000", safe_area: reel_9x16}
    max_chars_per_line: 32
  labels:                             # period-correct engineering callouts
    - {text: "cast-iron frame, 36 cells", at_shot: sh010, enter_s: 0.8, hold_s: 2.4,
       anchor: {part: shield_frame, offset_mm: [0, 0, 400]}}
    - {text: "screw jack", at_shot: sh011, anchor: {part: jacks[17]}}

# ---- 8. TIMING -----------------------------------------------------------
timing:
  fps: 30
  motion_blur: {enabled: true, shutter_deg: 180}
  shot_frame_math: "dur_s * fps, rounded to nearest frame"
  narration_track: audio/vo_ep01.wav
  sync_policy: {narration_authority: script, picture_conforms: true}

# ---- 9. RENDER -----------------------------------------------------------
render:
  resolution: [1080, 1920]
  engine: cycles
  device: optix
  samples: {hero: 256, standard: 64, previs: 16}
  denoise: {method: optix, prefilter: accurate}
  performance: {use_auto_tile: true, tile_size: 1024,
                texture_cache: auto_generate, persistent_data: false}
  bounces: {diffuse: 4, glossy: 4, transmission: 4, volume: 2}
  output: {format: png_16, filename: "{shot}_{frame:04d}", to: render_node}
  budget: {max_s_per_frame_hero: 45, max_s_per_frame_standard: 12}

# ---- 10. QA (see §3) -----------------------------------------------------
qa:
  rubric_ref: "rubrics/rubric.docudrama.v4.yaml"
  views: six_view_rgb              # 3D-DefectBench's cost-effective default
  hard_gates: [manifold, no_float, camera_coverage, frame_budget, caption_fit]
  soft_gates: [silhouette_legibility, material_plausibility,
               historical_fidelity, composition, temporal_stability]

# ---- 11. ESCAPE HATCHES (counted, reviewed) ------------------------------
escape_hatches: []   # each entry: {id, reason, bpy_blob_sha256, reviewer}
```

### 2.3 Compiler outputs

One spec in, five artifacts out, all content-addressed:

| Output | Consumer |
|---|---|
| `shield.blend` | render node |
| `shield.manifest.json` — every part id → object name, world bbox, tri count, material, and the assertion results | QA, regression diff, caption anchoring |
| `shield.otio` | edit / assembly (ASWF OpenTimelineIO) |
| `shotlist.csv` + `editorial_notes.md` | producer review |
| `compile.log` + `spec.sha256` + `toolchain.lock` | determinism ledger |

**Refuse-to-build rule:** unknown key, unknown enum, unit missing, parent cycle, or `spec_version` major mismatch ⇒ the compiler exits non-zero with a structured error list. It does not guess. That is the entire point.

### 2.4 Engineering machinery specifically

A tunnelling shield is a *machine*, not an environment. Two consequences:

- **Parts must be parametric CAD first.** `blendquery` (uki-dev) integrates **CadQuery and Build123d** directly into Blender. The shield's cast-iron frame is a plate with a 3×12 grid of cells and bolt flanges — trivially expressible in Build123d, miserable to express as "make me a thing with holes." **The LLM's job is `width_m`, `tiers`, `cells_per_tier`, `frame_section_mm`** — a handful of typed numbers with units and stated ranges. That is exactly the shape of task LLMs are good at (§4.1).
- **Instancing is the whole game.** 36 screw jacks, 24 poling boards, 12 lining rings. Author once, instance N times, driven by `pattern`. This is simultaneously the cheapest thing for the render (instances share geometry memory in Cycles) and the thing the 3DCodeBench "floating components" failure destroys if done per-part.

---

## 3. (c) The episode loop, end to end

| # | Stage | Input | Output | Tool | Review criteria | Gate |
|---|---|---|---|---|---|---|
| 1 | **Brief** | creator's one-line pitch | `brief.yaml` (angle, audience, length, 3 mandatory claims, tone) | human + LLM interview | Is the hook a *question*? Is the length 4–8 min? | **Human** |
| 2 | **Research** | brief + source list | `dossier/` — per-claim facts with citation, confidence, and `would_settle`; image/plate references | DeepSeek V4.1-Flash (1M ctx) over fetched primary sources; Smithsonian CC0 / Poly Haven / BlenderKit lookups | Every factual claim cited; every low-confidence claim flagged; **no claim from model memory** | Auto: citation coverage = 100% |
| 3 | **Beat sheet** | dossier | `beats.yaml` — 6–10 beats, each with dramatic function + the 1–2 facts it carries | LLM, creator edits | Does each beat carry a fact? Is there a turn? | **Human** |
| 4 | **Shot list** | beats | `shotlist` block in spec + `.otio` | LLM; validated by compiler frame math | Shot-length distribution (mean 3–5 s); coverage: no beat >45 s on one camera | Auto + human spot-check |
| 5 | **Scene spec** | shot list + component library + LESSONS | one `*.yaml` per scene | LLM writes **DSL, never `bpy`**; retrieves templates and lessons | Schema valid; every part resolves; every camera parent named; escape-hatch count = 0 | Auto (schema) + **human reads the diff** |
| 6 | **Compile → .blend** | spec | `.blend` + manifest + assertions | `blender --background --python compile.py` (Blender **5.2.2 LTS**) | All `attach_rules` assertions pass; **zero floating/unparented meshes**; manifold check; tri budget; VRAM estimate < 9 GB | Auto — **hard fail stops the line** |
| 7 | **Previs render** | `.blend` | 16-spp 540×960 animatic, ~4 h → ~20 min | RTX 3080, OptiX, 16 spp | Motion reads at thumbnail size; camera moves not nauseating | Auto + VLM |
| 8 | **Automated QA** | animatic + frames | `qa_report.json` + `patch.json` | **two layers** — see §3.2 | Hard gates must all pass; soft gates scored against rubric | Auto |
| 9 | **Art-director gate** | contact sheets + animatic + qa_report | approve / revise / kill | **human**, on the M1, ~20–40 min | The only aesthetic authority in the system | **Human — mandatory** |
| 10 | **Revision** | `patch.json` + creator notes | new spec revision | LLM applies **RFC 6902 JSON Patch** to the spec; recompile from stage 6 | Diff is bounded and readable; no escape hatch added silently | Auto + human |
| 11 | **Hero render** | approved `.blend` | 7,200 PNG frames | render node (or RenderStreet / RunPod burst) | Per-frame budget met; no failed frames; no VRAM spill | Auto |
| 12 | **Assembly** | frames + VO + captions | `ep01.mp4` 1080×1920 | VO: ElevenLabs v3. Captions: whisper.cpp v1.9.4 or WhisperX v3.8.6 forced-align. Burn-in: ffmpeg `ass` filter (or Remotion). Edit: Blender VSE (`context.sequencer_scene` — **note the 5.0 VSE context change**) or Resolve | Captions inside 9:16 safe area; ≤32 chars/line; no frame longer than the VO beat; LUFS target | Auto + human |
| 13 | **Ship & archive** | `ep01.mp4` | publish + frozen record | — | Regenerate the next episode's LESSONS from this run's failures | Auto |

### 3.1 Why stage 7 (previs) is the highest-ROI invention in the loop

A 16-spp animatic costs **~20 minutes** on the 3080 versus ~8–12 hours for the final. It is the only way to catch the failures that matter (bad camera move, unreadable silhouette, wrong pacing) *before* spending the render budget. Every hour of agent time and every dollar of tokens should be spent making the previs loop fast, because that is the loop that iterates.

### 3.2 The multimodal critic — concrete design

Grounded in three 2026 papers:

**3D-DefectBench** (arXiv:2607.10826) — a controlled factorial study, 4 pipeline factors (VLM, camera protocol, visual input, prompt schema), **84 inference designs, ~3.2 million scored defect decisions**, 9 fine-grained binary defects. Findings **[H]**:
- **"A compact six-view RGB protocol performs comparably to denser multi-view settings and inputs augmented with depth or surface normals."** → Use six-view RGB. Cheap and as good.
- **Model choice is the largest determinant**, but camera protocol still matters, *interacts with model selection, and can change which configuration is best.* → The camera protocol is part of the pipeline spec, versioned, not ad hoc.
- **"The best of 12 VLM judges still lag behind trained human labelers."** → The VLM is an *assistant*, never the final authority. This is the formal justification for stage 9.
- **"Texture agreement drops sharply when expert-consensus labels are replaced by noisier silver labels."** → Your rubric labels must be creator-authored, not LLM-generated.

**FIRM-Video** (arXiv:2608.21839) — **"check-before-score"**: build dimension-specific checklists, verify each criterion against visual evidence, then **aggregate only verified decisions**. Prevents "incomplete inspection, unfaithful justification, and entangled attribution." **[H]** — adopt this verbatim.

**3DCodeBench** — executability vs human Elo r = 0.481. Anything that measures only "did it run" is measuring the wrong thing. **[H]**

**Implementation:**

```
for each shot:
  1. DETERMINISTIC PASS (no LLM, must pass first)
     - manifest assertions: attach_rules, manifold, no unparented mesh,
       bbox dims within tolerance, camera coverage %, NaN check
     - frame budget, black-frame check, temporal jitter (mean abs diff of
       consecutive-frame histograms)
  2. RENDER 6 VIEWS at 512x512 -> contact sheet (front, back, left, right,
     top, and THE SHOT CAMERA). Plus, for animation, a 3-frame temporal strip
     (start/mid/end of the shot).
  3. VLM CHECKLIST PASS (DeepSeek V4.1-Flash, native vision, 1M ctx)
     For each rubric criterion, emit BEFORE any score:
       {criterion, verdict: pass|fail|unverifiable,
        evidence: "<what in which view>", confidence}
     Never emit a holistic score. Never accept "looks good".
  4. AGGREGATE only verified verdicts -> weighted score + ranked defect list
  5. PATCH: emit RFC 6902 JSON Patch against the SPEC (not prose, not bpy)
```

The patch is the critical output shape. `{"op":"replace","path":"/shotlist/12/cam/lens_mm","value":40}` is reviewable, testable, and re-compilable. "The camera feels a bit tight" is not.

**Cost of the critic:** 6 views + 3 temporal frames = 9 images per shot per pass. 60 shots × 3 passes × 9 = 1,620 images. At ~800 tokens per 512² image that is ~1.3 M image tokens — trivial against a 1M-context model, and ~$0.20–$1.20 depending on tier.

---

## 4. (d) What LLMs are good and bad at — with a concrete mitigation each

| | Strength | Why | Mitigation if over-trusted |
|---|---|---|---|
| S1 | **Parameter reasoning** | Typed numbers with units and stated ranges is the shape of task LLMs do best | Constrain every parameter: `{value, unit, min, max}`. Reject unitless numbers at schema level. |
| S2 | **Code generation** | 3DCodeBench: 0.88 executability for top models | Pin Blender **5.2.2 LTS** + `bpy` 5.2.2 + compiler semver in `toolchain.lock`. Lint the generated Python against `bl_rna` **before** it touches Blender. |
| S3 | **Narration / script** | Cheap, high quality, human-editable | Human rewrites the hook and the last line. Those two carry the video. |
| S4 | **Variation explosion** | Generate 30 arm poses, 12 camera framings, 6 lighting rigs | **Deterministic seeds.** Best-of-N with a scored rubric, not one-shot. This is the single most reliable win. |
| S5 | **Tedious repetition** | 36 jacks, 7,200 frames, 1,500 captions, per-shot reframes | Procedural loops + instancing. Never let the model hand-author instance #27. |
| | **Weakness** | | **Mitigation** |
| W1 | **Spatial reasoning** | The model places objects "approximately"; 3DCodeBench: "misaligned structures" | **Never author an absolute world coordinate.** All placement is relative to a named parent via `offset_mm` + `pattern`. Enforce with compiler assertions (`scene_measure_gap`, `scene_assert_contact/containment/symmetry`). Deterministic measurement is the truth layer. |
| W2 | **Hidden-surface reasoning** | The model cannot know what the camera cannot see, and cannot see what it occludes | **Never ask.** Render the actual view. Occlusion is discoverable only by rendering — hence 6-view QA and per-shot camera renders. Do not let the model reason about occlusion in the abstract. |
| W3 | **Aesthetic judgement** | 3D-DefectBench: best of 12 VLM judges < trained humans; LLM-judge bias is a documented, measurable phenomenon | Human art-director gate is **mandatory, not optional** (stage 9). Rubrics calibrated against creator-authored labels, never silver labels. VLM scores are advisory. |
| W4 | **API hallucination** | **The #1 failure mode** (3DCodeBench) | **Closed vocabulary.** The LLM writes DSL; only the compiler writes `bpy`. Where `bpy` is unavoidable (escape hatch), validate every attribute against the live `bl_rna` and reject unknowns with a structured error. Ship a version-stamped API cheat-sheet as a skill and use `bpy_api_lookup` / `describe_node_type`. |

### 4.1 The single highest-leverage mitigation

Not prompting. **A closed vocabulary.** 3DCodeBench says failures are *mostly API mismatches*. A schema that enumerates every legal verb and parameter converts "invent an API" into "choose from a list," and a compiler that refuses to build on an unknown key converts a hallucination into a one-line error message the model can act on. This is worth more than any amount of prompt engineering.

---

## 5. (e) The compounding layers

Five registers, all in git, all versioned, all content-addressed.

### 5.1 Skills & prompt library — `skills/`
One directory per capability, each with a `SKILL.md`, a machine-readable `skill.yaml` (name, inputs, outputs, preconditions, failure modes), and a golden example.
```
skills/
  blender-5.2-api/SKILL.md              # version-stamped cheat-sheet: everything 5.0/5.1/5.2 broke
  scene-dsl-authoring/SKILL.md          # the DSL, with 5 worked specs (incl. shield.yaml)
  cad-parametric/SKILL.md               # CadQuery/Build123d via blendquery
  camera-language/SKILL.md              # framing vocabulary -> DSL camera blocks
  lighting-rigs/SKILL.md
  otio-editorial/SKILL.md
  caption-timing/SKILL.md
  qa-rubric-reading/SKILL.md
```
Retrieval is explicit: the harness loads skill bodies referenced by the current stage (not all of them), plus the top-k LESSONS by tag.

### 5.2 Component & shot template library — `library/`
Blender-native, because Blender already has the right primitives:
- `.blend` asset files with **Asset Browser** marking, consumed via **library overrides / linking** so a component fix propagates to every episode that uses it.
- `library/mech/` — screw_jack, cast_iron_ring, bolt_flange, timber_brace, pump, winch
- `library/timber/`, `library/geo/`, `library/lighting/rigs/`, `library/cameras/moves/`, `library/materials/`
- `library/shots/` — **shot templates**, not models: `reveal_push_9x16`, `macro_detail_rack`, `scale_wide_low`, each a parameterised camera + move + light rig.
- Every component carries `component.yaml` with provenance and licence. **Renderer rule: components used in a published episode must be CC0 or commercially licensed and recorded in the manifest.** (Smithsonian Open Access: 2,000+ CC0 models incl. historic machinery. Poly Haven: 997 HDRIs / 861 textures / 521 models, all CC0. Quixel Megascans is **no longer free**; GrabCAD default terms bar commercial use without the designer's permission — both are traps.)

Promotion rule: any `reusable: true` part that passes QA twice gets promoted into `library/` and its ad-hoc definition deleted from the episode.

### 5.3 Rubric library — `rubrics/`
Versioned YAML. One rubric per `accuracy_profile` (strict / docudrama / stylised). Each criterion: `{id, layer: hard|soft, weight, question, evidence_required, calibration: {human_labels_n, agreement}}`.
Critically: **rubrics are calibrated, not asserted.** Every rubric carries a measured agreement rate against creator labels on a held-out set of shots. A rubric whose VLM agreement falls below threshold is retired. (3D-DefectBench: rendering protocol and prompt schema interact with model choice — so a rubric is a *pipeline*, and changing it invalidates its calibration.)

### 5.4 LESSONS — `LESSONS.yaml`, machine-readable, fed into every run

```yaml
- id: L-0042
  date: 2026-09-21
  tags: [compile, geometry, cad]
  trigger: "Build123d boolean on the shield frame produced non-manifold points at cell corners"
  lesson: "Do not boolean-subtract cell voids from a single plate; build 3x12 cell frames and join."
  applies_to: [parts.cad, lib/mech]
  check: "compile.assert_manifold == true"          # <-- makes it executable
  counter: {episodes_since_recurrence: 14}
  evidence: [ep01/compile.log#L218, ep01/qa_report.json#defect_7]
- id: L-0117
  date: 2026-10-04
  tags: [qa, lighting]
  trigger: "VLM flagged 'flat' on shots 22, 31, 44; all were cam_wide_43 with the same rig"
  lesson: "cam_wide_43 + rig_oil_row alone under 1.0 strength produces a flat histogram. Add hero_rake >= 400W."
  check: "render.rig_energy_ratio >= 0.35"
  counter: {episodes_since_recurrence: 6}
```

**The `check` field is what makes this compound rather than rot.** A lesson without an executable check is a note, and notes do not survive. Every lesson becomes either (a) a compiler lint, (b) a rubric criterion, or (c) a template change. Lessons whose `episodes_since_recurrence` stays high get archived. Lessons whose counter resets get escalated into a hard gate.

### 5.5 Determinism & regression testing

**The uncomfortable empirical fact:** Cycles is **not bit-reproducible**. BVH construction, OptiX version, driver version, GPU atomics, and out-of-core host-memory fallback all change results. Do not build regression testing on `.blend` or PNG hashes — it will fail for reasons that have nothing to do with your change. **[H]** for the mechanisms (out-of-core, OptiX BVH, adaptive sampling), **[M]** for the conclusion.

Instead, three layers:

```
LAYER 1 — STRUCTURAL (exact, fast, free)
  Recompile the spec; diff shield.manifest.json against the committed one.
  Assert: part ids identical; object count identical; every attach_rule passes;
  bbox dims within 0.1%; tri count within 1%; no unparented meshes.
  -> runs in seconds on the M1 (bpy 5.2.2 headless, no GPU), no render needed.

LAYER 2 — CANARY REEL (perceptual, cheap, the real gate)
  A frozen set of 6 shots at 64 spp / 512x512 / fixed CYCLES_SEED.
  Rendered on every change. Compare to golden PNGs with SSIM + LPIPS.
  Accept if: SSIM >= 0.98 AND LPIPS <= 0.05 for EVERY canary shot,
  AND no shot's score degrades by more than 20% of its previous margin.
  Goldens are 512px PNGs (~200 KB each) -> ~1.2 MB total.
  (23 GB free disk means goldens must never be EXR.)

LAYER 3 — FULL-EPISODE LEDGER
  Every episode writes eval/ep01/eval.json: per-shot hard-gate pass/fail,
  soft-gate scores, render seconds, token cost, creator minutes, revision count.
  Episode N+1 must beat episode N on the declared headline metric
  ("every subsequent video must be measurably better" -> pick ONE metric and
  put it in the ledger, or the claim is unfalsifiable).
```

**The rule that makes it safe:** *a change improves shot A only if Layer 1 passes globally and Layer 2's canary reel shows no regression beyond tolerance.* Because the canary reel pins the spec hash, changing one shot's spec physically cannot alter another's render. That is the property free-form `bpy` cannot give you — it is the strongest practical argument for §2.

Write `eval.json` and `LESSONS.yaml` diffs into the same commit as the spec change. The commit message is machine-generated from the eval delta.

---

## 6. (f) Cost model per episode

Assumptions: **4-minute episode**, 240 s at 30 fps = **7,200 frames**, ~60 shots, mean shot 4 s. 1080×1920 (= same pixel count as 1080p, so no resolution penalty). RTX 3080, OptiX, 64 spp + OptiX denoise ≈ **4–8 s/frame** (from Open Data medians: 3080 5.x OptiX = 1,151–1,462 spp/min; 1,000 spp @ 1080×1920 = 46–52 s → 64 spp ≈ 3 s + denoise 1–4 s). **[M]**

### 6.1 Render

| Scenario | Frames × s/frame | GPU-hours on 3080 | Cloud equivalent |
|---|---|---|---|
| Previs (16 spp, 540×960) | 7,200 × ~0.8 s | **~1.6 h** | — |
| Final, all shots 64 spp | 7,200 × ~6 s | **~12 h** | RunPod RTX 4090 @ $0.34/hr ≈ **$3** (3090 ≈ $0.22/hr ≈ $2) |
| Final, hero shots 256 spp (15 shots) | +1,800 × ~24 s | **+12 h** | +$3 |
| With BVH rebuilds, failed frames, retries (×1.5) | — | **~18–36 h** | **$5–15** |
| RenderStreet L40S @ $4.49/server-hr | — | — | **$80–160** |
| iRender RTX 4090 @ $8.20/node-hr | — | — | **$150–300** |
| SheepIt | — | — | **$0** (points economy) |

**The finding: cloud render burst is almost never the right first purchase.** The render node is idle overnight; 12 hours of 3080 time costs $0. RunPod Community at $0.34/hr for a 4090 (≈2× a 3080) is worth it only to compress a deadline, and RenderStreet/iRender at the managed-farm price point are 20–50× the raw-GPU price for convenience you don't need. **[M/H]**

### 6.2 LLM tokens

~**20 M input, 2.5 M output** per episode: research over long context (2 M in), beat sheet (1 M), 60 scene specs at ~40 K context each + 3 revisions (≈12 M in / 1.5 M out), compile-error repair loops (≈3 M in), 6-view VLM QA (1.3 M image tokens + text), narration/caption work (2 M in).

| Tier | Model mix | Input (80% cached) | Output | **$/episode** |
|---|---|---|---|---|
| **Frugal** | DeepSeek V4.1-Flash only, off-peak | 4 M × $0.15 + 16 M × $0.003 = $0.65 | 2.5 M × $0.60 = $1.50 | **≈ $2.15** |
| **Frugal, peak hours** | same (DeepSeek peak = 2×: Mon–Fri 01:00–04:00 and 06:00–10:00 UTC) | $1.30 | $3.00 | **≈ $4.30** |
| **Standard** | Flash for bulk; frontier for spec authoring + hero QA (12 M in / 1.5 M out on GPT-5.6 Sol @ $4/$0.40/$20) | $9.60 + $3.84 | $30.00 | **≈ $44** |
| **Standard, Claude** | as above on Claude Opus 5 @ $5/$0.50/$25 | $12.00 + $4.80 | $37.50 | **≈ $55** |
| **Frontier everywhere** | Opus 5 / GPT-5.6 for all stages | — | — | **≈ $90–120** |

DeepSeek V4.1-Flash list rate is $0.30 in / $0.006 cached / $1.20 out; off-peak is half — $0.15 / $0.003 / $0.60. **Cache discipline is the single biggest lever:** at $0.003/M cached vs $0.15/M miss, a 50× difference. Skills, DSL schema, LESSONS, and the spec template belong in the cached prefix of every call. **[H]** for prices, **[M]** for the token volumes.

### 6.3 Voice, captions, assets

| Item | Cost/episode |
|---|---|
| ElevenLabs v3 (600 words ≈ 3,600 chars) | API $100/1M chars → **$0.36**; or ~3% of Creator $22/mo (121 k credits) |
| Captions | **$0** — whisper.cpp v1.9.4 / faster-whisper v1.2.1 / WhisperX v3.8.6, all free & permissive |
| Burn-in / assembly | ffmpeg `ass` filter — free. Remotion only if you go programmatic: free ≤3 people |
| Assets (Ep1) | **$0** if CC0 only: Smithsonian Open Access (2,000+ CC0, incl. historic machinery), Poly Haven (997 HDRI / 861 tex / 521 models, CC0). Budget $40–200/mo for Blendkit Full ($17.90) or KitBash3D if kitbash is needed |

### 6.4 Creator time — the number that actually matters

| Stage | Ep1 (hrs) | Ep6 (hrs) | Ep12 (hrs) |
|---|---|---|---|
| Brief + research review | 3 | 1.5 | 1 |
| Beat sheet + shot list approval | 3 | 1.5 | 1 |
| Art-director gate (stage 9), per revision round | 1.5 × 3 rounds | 0.75 × 2 | 0.5 × 1.5 |
| Hero frame selection | 2 | 1 | 0.5 |
| Assembly / caption / publish QA | 2 | 1 | 0.5 |
| Firefighting (compile errors, VRAM, re-renders) | 6 | 2 | 0.5 |
| **Total** | **~20.5 h** | **~8.5 h** | **~5 h** |

At $75/hr opportunity cost: **Ep1 ≈ $1,500**; Ep6 ≈ $640; Ep12 ≈ $375.

### 6.5 Where agentic automation is genuinely cheaper — and where it is not

**Cheaper (by a wide margin):**
- **Best-of-N variation.** 20 camera framings cost ~$0.02 of cached-prefix tokens and 20 minutes of previs; a human doing 20 framings takes hours. This is the strongest case.
- **Repetition:** 36 jacks, 7,200 frames, 1,500 caption cues, per-shot 9:16 reframe/crop, LUFS normalisation, filename hygiene.
- **QA sweeps.** A VLM pass over 60 shots costs ~$0.20–$1.20 and catches floaters, flat lighting, and caption overflow before the creator ever looks. Cheaper than the creator's 20 minutes.
- **Compile-and-assert.** Free and instant, and it eliminates the class of error (floating geometry) that would otherwise reach render.

**Not cheaper — do it by hand or accept the cost:**
- **The hero shot.** The one image that sells the episode. A human in Blender does it in 10 minutes; an agent spends 40 minutes and $2 fighting compile errors. **Hand-author it via the interactive MCP path and freeze it.**
- **Historical accuracy verification.** The model cannot be trusted to adjudicate a claim about 1825 cast-iron sections; it can only retrieve and cite. The creator signs off. (This is why every `evidence` block carries a `would_settle` field.)
- **Aesthetic judgement.** 3D-DefectBench: best of 12 VLM judges < trained humans. The gate is human.
- **Cloud render burst**, unless a deadline is at risk — see §6.1.
- **Anything the creator would finish in under 4 minutes.** Break-even: at DeepSeek off-peak rates, $0.50 of tokens ≈ 4 minutes of creator time at $75/hr. Any loop that saves ≥4 minutes per dollar is worth it; the loop that saves 30 seconds is not.

---

## 7. Two-machine architecture (the 23 GB / 16 GB / no-Blender constraint)

```
CONTROL PLANE — Mac M1, 16 GB RAM, 23 GB free, no Blender
  authoring · git · orchestration · browsing · MCP host
  ┌──────────────────────────────────────────────────────────────┐
  │  bpy 5.2.2 from PyPI  (requires-python ==3.13.*, GPL-3.0)    │
  │  ~208–235 MB wheel  -> installs to a pinned uv venv          │
  │  Used ONLY to: compile spec -> .blend, run structural         │
  │  assertions, produce the manifest. NO rendering.             │
  │  Caveat: bpy-the-module has no GUI; EEVEE needs a GL context. │
  │  Cycles CPU works but the M1 GPU path is not the pipeline.    │
  └──────────────────────────────────────────────────────────────┘
  Disk discipline (23 GB): uv cache, wheels, and .blend files add up.
    Pin ONE Python (3.13) and ONE bpy version. Purge uv cache after
    install. Keep only the current episode's .blend on the M1.

RENDER NODE — Windows PC, RTX 3080 (10–12 GB), strong CPU
  Blender 5.2.2 LTS installed natively (NOT the bpy wheel)
  blender --background --python compile.py -- spec.yaml
  blender -b scene.blend -a
  - OptiX, tile_size 1024, texture cache + auto-generate  (5.2 LTS headline)
  - persistent_data off when VRAM is tight
  - Watch WDDM TDR on long frames; OptiX is not immune
  - Out-of-core fallback exists (CUDA/HIP/oneAPI/OptiX) but costs
    20–30% if textures spill, ~10x if working data spills
  - 100 x 4K textures = 6.4 GB before any geometry: the dominant OOM cause

TRANSFER: spec + goldens travel (KB–MB). Frames do NOT come back.
  Render PNG-16 sequences, assemble + burn captions ON THE WINDOWS BOX,
  return only ep01.mp4 + the contact sheets + qa_report.json.
  Do not pull 7,200 frames over the network. Do not archive EXR on the M1.
```

---

## 8. Recommended build order

1. **Week 1** — Pin Blender 5.2.2 LTS + bpy 5.2.2 + Python 3.13. Write `compile.py` for a 1-part, 1-shot spec. Prove: spec → `.blend` → manifest → structural assertions, headless, on both machines.
2. **Week 2** — `shield.yaml` with the CAD frame + 36 instanced jacks. Hard-gate assertions (`attach_rules`, manifold, no-floaters). This is where "floating geometry" gets killed.
3. **Week 3** — Previs loop + six-view contact sheets + the deterministic QA pass. Ep1 shot at 16 spp end-to-end.
4. **Week 4** — VLM checklist critic (FIRM-Video "check-before-score" shape) + JSON Patch output + the human gate UI on the M1.
5. **Week 5** — Canary reel + `eval.json` ledger + `LESSONS.yaml` with the `check` field. First frozen commit.
6. **After Ep1** — promote passing components into `library/`, calibrate rubric v1 against creator labels, and only then consider a frontier model for spec authoring.

**Do not** start with the MCP server, prompt-engineering the model, or cloud GPU. Start with the compiler and the assertions. The compiler is the thing that makes every later step cheap; the model is the interchangeable part.
