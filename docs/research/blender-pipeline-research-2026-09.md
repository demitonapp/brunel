# 3D Animation Production Pipeline — Fact-Gathering Research
**As of 17 September 2026.** Every figure is sourced. Items that could not be verified are marked **UNVERIFIED**. Where a vendor page was client-rendered or Cloudflare-blocked and no price could be read, that is stated explicitly rather than guessed.

Research method: primary vendor/Blender pages fetched directly wherever reachable; secondary sources flagged. Sections C, D and E were additionally researched by dedicated sub-agents, whose primary-source work is incorporated below. All five sections are now complete; residual gaps are listed in the consolidated unverified register at the end.

---

# A) BLENDER CORE

## A1. Release train (exact dates)

| Release | Date | Status 17 Sep 2026 |
|---|---|---|
| Blender 5.0 | 18 Nov 2025 | superseded |
| Blender 5.1 | 17 Mar 2026 | superseded |
| Blender 5.2 LTS | 14 Jul 2026 | **current LTS** |
| Blender 5.2.2 LTS | 15 Sep 2026 | **latest stable / current download** |
| Blender 5.3 | planned November 2026 | **NOT released** |

- **Latest stable = Blender 5.2.2 LTS.** blender.org/download serves 5.2.2 LTS (Windows x64/ARM, macOS Apple Silicon, Linux, Steam, source) dated 15 Sep 2026.
- **Latest LTS = 5.2 LTS, supported until July 2028.**
- Other maintained LTS: **4.5 LTS** — last updated to **4.5.14** on 15 Sep 2026, supported until July 2027. **4.2 LTS** ended July 2026 (last 4.2.23). 3.6 LTS and 3.3 LTS are historical.

Sources: https://developer.blender.org/docs/release_notes/5.0/ · https://developer.blender.org/docs/release_notes/5.1/ · https://developer.blender.org/docs/release_notes/5.2/ · https://www.blender.org/download/lts/ · https://www.blender.org/download/ · https://www.blender.org/development/projects-to-look-forward-to-in-2026/ · https://www.blender.org/press/blender-5-2-lts-release/

## A2. Python / library versions
- **Blender 5.1 upgraded to Python 3.13** (VFX Platform 2026): OpenColorIO 2.5, OpenEXR 3.4, OpenVDB 13.0.
- Blender 5.2 therefore ships **Python 3.13**.
- Exact Python minor in Blender 5.0: **UNVERIFIED** (5.0 predates the 3.13 bump).

Source: https://developer.blender.org/docs/release_notes/5.1/

## A3. What's new that matters for mechanical / architectural visualisation

### Blender 5.0 (18 Nov 2025)
- **Geometry Nodes:** Bundles (Combine/Separate/Join Bundle) and Closures (Closure Zone / Evaluate Closure); full volume-grid and SDF node set (Mesh to SDF Grid, Points to SDF Grid, SDF Grid Boolean, SDF Grid Fillet/Offset/Median/Mean/Laplacian, Voxelize/Prune Grid, Grid to Mesh, Advect Grid); **UV Tangent** node (MikkTSpace); richer Viewer node; new built-in **Array** and **Scatter on Surface** modifiers.
- **Cycles:** unbiased null-scattering volume sampling is the new default (Biased ray marching still selectable); NanoVDB for smoke/fire; stochastic cubic/linear volume interpolation; multi-bounce subsurface scattering; physically-based metallic thin-film iridescence on Principled/Metallic BSDF; **adaptive subdivision is no longer experimental** and is always available in Subdivision Surface, with a new **Object-space edge-length** mode explicitly designed so instancing uses little memory; `undisplaced_n` / `undisplaced_tangent`; new **Render Time pass**; OptiX denoiser quality fix; minimum NVIDIA compute capability now **sm_50**; minimum Windows AMD driver Adrenalin 24.9.1 / Radeon Pro 24.Q4.
- **Lighting / camera:** Cycles OSL camera parameters gained metadata-driven UI (`string unit = "m"`, `vecsemantics = "POINT"/"NORMAL"`, `widget = "filename"`, `widget = "mapper"`). **BREAKING:** the aperture position no longer depends on focal length — OSL shaders must now multiply by `focal_length * 1e-3`. **Light Linking is now editable/overridable in library overrides.**
- **EEVEE / Vulkan:** engine identifier changed **`BLENDER_EEVEE_NEXT` → `BLENDER_EEVEE`**; View Layer Overrides (Material, World, Sample); curve drawing rewritten — **a default hair system now renders ~15× more geometry and can OOM old scenes**; MatCaps reworked with a specular layer; simple materials ~**4× faster to compile on NVIDIA OpenGL**; Workbench/Overlay instancing up to **3× fps**; **HDR and wide-gamut display via Vulkan** on Windows and Linux/Wayland.
- **Pipeline:** Collada (`.dae`) import/export **REMOVED**; the new C++ FBX importer is default (add-ons should call `bpy.ops.wm.fbx_import`, not `import_scene.fbx`); USD NURBS import/export improved; multilayer OpenEXR now writes **multi-part** files by default; HDR/wide-gamut video read/write; OBJ material name collision + apply transforms options.

### Blender 5.1 (17 Mar 2026)
- **Cycles:** GPU rendering **+5–10%** on benchmark scenes; CPU on Windows **+5–20%**; **AMD hardware ray tracing (HIP RT) on by default**; Normal Map can apply to the smooth undisplaced mesh or the displaced mesh; improved denoise with textured transparency/roughness.
- **EEVEE:** new **screen-space Raycast shader node** (NPR styling, X-ray, line rendering); **Light Path Intensity** controls for indirect/direct contribution; planar reflections now support **glossy reflections and refraction**; max AOV raised to **128**; lookdev HDRI view-space lighting option returns; transparency evaluation for Shader to RGB.
- Measured EEVEE performance (barbershop_interior, RTX 6000 Ada): cold shader compile **OpenGL 44.19 s (5.0.1) → 30.39 s (5.1); Vulkan 24.87 s → 11.67 s; Metal 55.50 s → 37.20 s**. Texture pool on *Mr. Elephant*: **406 MB → 291 MB (OpenGL) / 245 MB (Vulkan)**.
- **Geometry Nodes:** more volume-grid nodes (Cube Grid Topology, Grid Dilate & Erode, Grid Mean/Median, Clip Grid, Grid to Points); String to Curves fully socketed with a Font socket; Get/Store Bundle Item with computed bundle paths; Bone Info node; Matrix SVD; UV Unwrap SLIM (minimum stretch).
- **Pipeline:** USD UsdPreviewSurface transparency/translucency; indexed UV export; `get_prim_map` export hook; **AVIF** support; OpenEXR HTJ2K lossless; OCIO 2.5 `interop_id` / `icc_profile`.

### Blender 5.2 LTS (14 Jul 2026) — the release to build on
- **Cycles Texture Cache (headline):** enable **Performance → Texture Cache** + **Auto Generate**; writes tiled, mipmapped **`.tx`** files into `blender_tx/` next to each image; loads only the tiles and mip levels needed. Works on CPU and **all GPU backends**. CLI: `blender scene.blend --command maketx` and `blender --command maketx image.png --colorspace sRGB`; OIIO `maketx` files are recognised. **Ray differentials widened on indirect bounces reduce texture-cache memory by ~30%.**
- **Cycles (other):** Raycast node can return **attributes at the intersection point** (Cycles only; zero in EEVEE); SSS supports negative anisotropy and Random-Walk rescaling (old files auto-converted to Legacy); world **Cast Shadows** option; reduced geometry memory via sharing with Blender; **NVIDIA OptiX minimum driver now 575**; OpenImageDenoise no longer GPU-accelerated on AMD RDNA2; Intel min drivers Windows XX.X.101.8306 / Linux XX.XX.37435.3.
- **Geometry Nodes:** experimental **hair and cloth physics**; **Geometry Bundles** (attach bundles, fields and closures to geometry across modifier/object boundaries); **Lists** as a new core data type (Field to List, Closure to List, List Length, Get List Item, Filter List, Sort List); **Collection Children**; **Sample Sound Frequencies**; GN modifiers now allowed on **Empty objects and collection instances**; long-awaited **Mesh Bevel** node; Merge Points / Cluster by Distance / Cluster by Connected; Transfer Attributes, Rename Attribute, Get Attribute Names; **4D float vector attributes**; NURBS order/weight nodes; string fields (but not string attributes); bundled 3D-to-Screen/Screen-to-3D projection nodes and PCA nodes.
- **Grease Pencil:** new **Delaunay fill solver is default** (exact geometry from boundary strokes, automatic gap detection, inverse fill, zoom-independent, supports holes; pixel flood-fill still available under Advanced); **Dots/Squares line-material placement** (Count/Density/Radius) with size/opacity/colour randomisation at render time; `fill_id` and `hide_stroke` stroke attributes; draw-tool curve type (Bézier / Catmull-Rom / NURBS); updated bundled brushes plus online textured brushes.
- **Rendering / lighting:** new **Time node**; Principled BSDF **Thin Wall** mode (thin glass and thin subsurface); render output can be disabled; light/shadow linking copy-to-selection; colour spaces organised into **OCIO Family menus**; new camera input spaces (Apple, ARRI, Blackmagic, Canon, Sony) and Adobe RGB / wide-gamut / common-gamma spaces.
- **EEVEE:** screen-space raytracing pipeline overhaul with a new **Backface** option (some scenes render **darker** than 5.1 due to energy-conservation fixes); Fast GI / AO bug fixes (changes existing look; `Far Thickness` removed); reflection denoiser preserves contact sharpness; **EEVEE instancing up to 2× faster**; new **1.5 GB / 2 GB shadow pool** options; **Lights now support camera-ray visibility**; Raycast visibility toggle; 8-object-attribute limit removed.
- **Pipeline / assets:** **USD colour space support**; USD NURBS Surface export (as mesh); glTF point clouds, EXT/KHR_meshopt_compression, iridescence and dispersion; Alembic animated camera and visibility import; STL viewport-vs-render eval option; **Hydra implementation updated to the Hydra 2.0 API** (OpenUSD abstracts versions, existing render delegates keep working); remote/online asset libraries (Blender Online Essentials); VR location scouting.
- Press summary explicitly names: texture cache, Thin Wall, GN experimental hair/cloth physics, remote asset libraries, Grease Pencil fill algorithm, EEVEE usability fixes, VR location scouting.

Sources: https://code.blender.org/2026/05/cycles-texture-cache/ · https://developer.blender.org/docs/release_notes/5.2/cycles/ · /geometry_nodes/ · /eevee/ · /grease_pencil/ · /pipeline_io/ · /rendering/ · /python_api/

## A4. `bpy` / `bpy.ops` status and breaking API changes
**YES — Blender 5.2 still ships `bpy` and `bpy.ops`.** The 5.2 API reference lists operator modules for Camera, Cycles, Render, Object, World, Geometry, Node, Material, Wm and more. https://docs.blender.org/api/5.2/bpy.ops.html

### Breaking changes relevant to scripted scene construction
**5.0:**
- EEVEE engine identifier `BLENDER_EEVEE_NEXT` → `BLENDER_EEVEE`.
- Render passes renamed from abbreviations ('DiffCol' → 'Diffuse Color', 'IndexMA' → 'Material Index', 'Z' → 'Depth').
- `scene.node_tree` **REMOVED** → use `scene.compositing_node_group`; `scene.use_nodes` deprecated (removal planned 6.0).
- `material.use_nodes` and `world.use_nodes` deprecated (always on).
- Compositor File Output node: `file_slots` / `layer_slots` / `base_path` removed → `directory` / `file_name` / `file_output_items`.
- USD: `bpy.ops.wm.usd_import` options renamed (`import_subdiv`→`import_subdivision`, `attr_import_mode`→`property_import_mode`); `bpy.ops.wm.usd_export` lost `export_textures` (use `export_textures_mode`) and `visible_objects_only`.
- `Scene.alembic_export` removed; Alembic `visible_objects_only` export option removed.
- Sky Texture lost `sun_direction`, `turbidity`, `ground_albedo` inputs.
- Deprecated compositor combine/separate nodes removed; Point Density texture node removed.
- Annotations/Grease Pencil RNA renamed (`bpy.data.grease_pencils_v3` → `bpy.data.grease_pencils`; `GreasePencilv3` → `GreasePencil`; annotation types renamed to `Annotation*`).
- Legacy Action API removed: `action.fcurves` / `action.groups` / `action.id_root` → channelbags / `action_slot.target_id_type`.
- `mathutils` native buffer protocol now exposes float32 (numpy interop change: non-contiguous buffers).
- Brush enums: `brush.sculpt_tool` → `brush.sculpt_brush_type`; `unified_paint_settings` moved into the mode-specific Paint struct.
- Boolean solver "FAST" renamed to "FLOAT".
- Addition: `bpy.ops.render.render()` now accepts `frame_start` / `frame_end`.

**5.1:**
- Python 3.13.
- Brush `use_airbrush`/`use_anchor`/`use_space`/`use_line`/`use_curve`/`use_restore_mesh` folded into `brush.stroke_method`.
- VSE strip time properties renamed (`frame_final_start`→`left_handle`, `frame_final_end`→`right_handle`, `frame_final_duration`→`duration`, etc.; old names deprecated to 6.0).
- `sculpt.sample_color` removed (merged into `paint.sample_color`).
- Node Tools now require a globally unique idname.

**5.2 LTS:**
- **Geometry Nodes modifier API changed (biggest for scripted GN):** custom properties are gone — use `modifier.properties.inputs.<id>.value`, `.type`, `.attribute_name` and `modifier.properties.outputs.<id>.attribute_name`.
- Compare and Random Value node socket identifiers changed.
- `paint.eraser_brush` / `paint.eraser_brush_asset_reference` removed.
- Sculpt automasking moved to `MeshAutomaskingSettings` (`mesh_automasking_settings.*`).
- IDProperties nesting capped at **1024 levels**.
- New: `bpy.data.all_ids` iterator; `Window.screenshot`; `gpu.init()` for background mode; `frame.strokes.new()` etc.; path-iterator options `EXPAND_TOKENS` / `EXPAND_SEQUENCES` / `EXPAND_CACHES`.

**No camera-operator or light-operator renames** were found in the 5.0/5.1/5.2 Python API notes. The only camera-specific breaking change is the Cycles OSL aperture-position change. Lighting changes are property-level (light linking overrides, EEVEE camera-ray visibility, world Cast Shadows).

Sources: `.../docs/release_notes/5.0/python_api.md`, `5.1/python_api.md`, `5.2/python_api.md` on projects.blender.org (`/raw/branch/main/`).

## A5. Cycles VRAM behaviour on a 10–12 GB GPU (RTX 3080)

**Out-of-core:** the current (5.2) manual states that with **CUDA, OptiX, HIP and Metal, "if the GPU memory is full Blender will automatically try to use system memory. This has a performance impact, but will usually still result in a faster render than using CPU rendering."** A hard `Error: Out of memory` is still possible. https://docs.blender.org/manual/en/5.2/render/cycles/gpu_rendering.html

Settings that matter (Render → Performance / Simplify):
- **Performance presets:** Default / Faster Render / Lower Memory.
- **Tile Size** — default **2048 px**. Tiles are cached to disk during render. **Lower to 1024 or 512 when running out of memory** ("typically at a small performance cost"). Lower tile size also reduces texture-cache memory, because only the textures needed by each tile are loaded.
- **Texture Cache + Auto Generate** (new in 5.2) — the single biggest lever for texture-heavy scenes; `.tx` files in `blender_tx/`.
- **Simplify:** Max Subdivision, Child Particles, **Texture Resolution (%)** — new in 5.2, replaces Texture Limit, works with and without the texture cache — Texture Size Limit, **Camera Cull** (+margin), **Distance Cull** (+margin).
- **Acceleration Structure:** Use Spatial Splits, Use Curves BVH, BVH Time Steps, **Use Compact BVH**. NOTE: **this panel is not present when using an OptiX device**, so "Use Compact BVH" is unavailable on a 3080 running OptiX.
- **Persistent Data** — keeps render data between renders for faster animation re-renders but costs memory; disable if VRAM is tight.
- **Reference VRAM cost of textures:** 8K = **256 MB**, 4K = **64 MB**, 2K = **16 MB**, 1K = **4 MB** per image.
- NVLink shared memory exists but does not apply to a single RTX 3080.
- Texture-cache savings are explicitly **"highly scene dependent"** — Blender published only graphs, no absolute numbers.

**Practical 12 GB recipe:** Texture Cache + Auto Generate on; Simplify → Texture Resolution 25–50% for lookdev; Tile Size 1024; Camera/Distance Cull on; Persistent Data off; prefer instancing (5.0 object-space adaptive subdivision) over duplicated mesh; check smaller textures first before assuming geometry is the culprit.

Sources: https://docs.blender.org/manual/en/5.2/render/cycles/render_settings/performance.html · .../simplify.html · .../gpu_rendering.html · https://code.blender.org/2026/05/cycles-texture-cache/

---

# B) LLM → BLENDER AGENTIC TOOLING

## B1. ahujasid — now `mcp-for-blender` (formerly `blender-mcp`)
- **RENAMED.** PyPI package is now **`mcp-for-blender`**, current version **2.0.0**, uploaded **2026-09-16**. Prior: 1.9.4 (same day), 1.9.1 / 1.9.0 (2026-09-01/02). `uvx blender-mcp` still works. Repo remains github.com/ahujasid/blender-mcp; github.com/ahujasid/mcp-for-blender redirects there. **MIT.**
- **Blender 3.0+**, Python 3.10+ (README recommends pinning 3.11).
- **Install:** install `uv` → MCP client `{"command":"uvx","args":["mcp-for-blender"]}` → `uvx mcp-for-blender install-addon` (writes `blender_mcp.py`) → enable "Interface: MCP for Blender" → N-panel → **Start MCP Server**. TCP JSON socket, default `localhost:9876`; env `BLENDER_HOST` / `BLENDER_PORT`; CLI `--host` / `--port`; multi-instance via different ports; Docker and pipx supported.
- **`BLENDER_MCP_SAFE_MODE=1`** validates scripts before execution. Socket has **no auth or encryption**. Telemetry **ON by default** (`DISABLE_TELEMETRY=true` to disable).
- **31 MCP tools + 1 prompt** in 2.0.0 (read from `src/blender_mcp/server.py`):
  `get_addon_status`, `disable_telemetry`, `get_scene_info`, `get_object_info`, `get_viewport_screenshot`, `execute_blender_code`, `describe_node_type`, `bpy_api_lookup`, `get_polyhaven_categories`, `search_polyhaven_assets`, `download_polyhaven_asset`, `set_texture`, `get_polyhaven_status`, `get_hyper3d_status`, `get_sketchfab_status`, `search_sketchfab_models`, `get_sketchfab_model_preview`, `download_sketchfab_model`, `get_polypizza_status`, `search_polypizza_models`, `download_polypizza_model`, `generate_hyper3d_model_via_text`, `generate_hyper3d_model_via_images`, `poll_rodin_job_status`, `import_generated_asset`, `get_hunyuan3d_status`, `generate_hunyuan3d_model`, `poll_hunyuan_job_status`, `import_generated_asset_hunyuan`, `export_scene`, `record_trajectory_feedback`. Prompt: `asset_creation_strategy`.
- **Documented limitations:** `execute_blender_code` runs arbitrary Python; **Blender must be open with a GUI — `blender -b` headless "commands never execute"** (use xvfb-run); 180 s socket timeout; complex operations must be decomposed; Poly Haven behaviour "sometimes erratic"; Poly Pizza CDN blocks datacenter/VPN IPs; only one server instance at a time.
- Hunyuan3D endpoints differ by account: mainland `ai3d` 2025-05-13 ap-guangzhou vs international `hunyuan` 2023-09-01 ap-singapore.

Sources: https://pypi.org/pypi/mcp-for-blender/json · https://raw.githubusercontent.com/ahujasid/blender-mcp/main/README.md

## B2. Official Blender MCP server (Blender Lab) — the major 2026 change
- **Blender Foundation now ships an official MCP server**: https://www.blender.org/lab/mcp-server/ — source https://projects.blender.org/lab/blender_mcp — add-on **v1.0.3** as listed on the page (v1.0.0 was current April 2026). **Requires Blender 5.1 or newer.**
- Three external components must be installed manually: Blender add-on, LLM client, and the MCP server (offered as an **`.mcpb` bundle** or from source; llama.cpp documented).
- Positioning: "a natural-language interface with Blender's Python API, improving access to documentation, and allowing users to explore and understand complex setups" — scene analysis, debugging, documentation, Data-block renaming, Geometry Nodes explanation.
- **Official security warning:** "The MCP server will execute LLM generated code in Blender without any guards in place to protect your data from removal or being sent to a remote location." A bundled `weak_sandbox.py` blocked `bpy.ops.wm.read_factory_settings` in one test, but does not prevent file deletion or exfiltration.
- Announced **28 Apr 2026** as part of Anthropic's "Claude for Creative Work" (one-click Blender connector in Claude Desktop, connector id `ant.dir.gh.blender.blender-mcp`). Claude Code users must register manually because `claude mcp add-from-claude-desktop` does not import `.mcpb` bundles.
- **Governance:** on **1 May 2026** Blender converted Anthropic's Corporate Patron membership into a **one-time donation** and stated: **"No generative AI functionality is currently available or planned to be integrated in Blender."**

Sources: https://www.blender.org/lab/mcp-server/ · https://www.blender.org/development/blender-lab-activity-report-q1-2026/ · https://www.anthropic.com/news/claude-for-creative-work · https://www.blender.org/news/upcoming-blender-development-fund-and-ai-policies/ · https://dev.classmethod.jp/en/articles/claude-blender-connector-desktop-and-code/

## B3. Other 2026 Blender MCP projects
- **carlosh7/blender-mcp ("blender-mcp-ultra")** — MIT, Blender **4.2+/5.x**, headless-ready, stdio/SSE/HTTP, VLM feedback loop, AST code blocklist + auth token + localhost-only binding. **Tool count is inconsistent in its own README (badge says 239, text says 248) — treat the exact number as UNVERIFIED.** https://github.com/carlosh7/blender-mcp
- **HoldMyBeer-gg/blend-ai** — **AGPL-3.0**, **164 tools across 24 modules**, 12 expert prompts, Blender **4.2+** (tested against 5.1 for EEVEE identifier, Annotation API, sculpt `stroke_method`, SLIM unwrap, Raycast node, EEVEE light-path intensity). Zero telemetry. Sandboxed `execute_blender_code` (blocks 25 imports + dangerous builtins). Documented limitations: single client connection; most mesh edits are all-or-nothing (no per-index vertex/edge/face selection); sculpt strokes cannot be simulated; node graphs must be built one node/connection at a time; **no MCP-level undo**; headless viewport screenshots may not work; **no real-time/streaming feedback**. https://github.com/HoldMyBeer-gg/blend-ai
- **PatrykIti/blender-ai-mcp** — **Apache-2.0**, Blender **4.0+** (E2E tested on 5.0), Python 3.11+, goal-first router with macro tools (`macro_cutout_recess`, `macro_relative_layout`, `macro_attach_part_to_surface`, `macro_align_part_with_contact`, `macro_place_symmetry_pair`, `macro_cleanup_part_intersections`, `macro_finish_form`) plus a deterministic measure/assert truth layer. Its README is the best statement of fail modes (quoted in B6). https://github.com/PatrykIti/blender-ai-mcp
- Also present: `yuri-schmaltz/mcp_blender`, `bakaroart/blender-chatgpt-mcp` (both carry SECURITY.md docs).

## B4. Benchmarks / reliability evidence
**3DCodeBench** (Google DeepMind + Google Research + USC) is the current reference benchmark: **arXiv:2606.01057** (submitted 31 May 2026), https://www.3dcodebench.com, code https://github.com/gaoypeng/3dcodebench, data https://huggingface.co/datasets/YipengGao/3DCode.
- Measures models writing **Blender 5.0 Python** to procedurally build **212 object categories** (from Infinigen); **12 frontier VLMs**; **81,605 generated scripts across 82,042 trials** + **2,767 coding-agent transcripts**; scored on executability, SigLIP-2 / DINOv3 image similarity, Chamfer, Uni3D, LLM-judge, plus human-preference 3DCodeArena Elo.

Single-shot **text → 3D** top rows (Exec. = Blender 5.0 pass rate | Elo | mean list price/query):

| Model | Exec. | Elo | Cost |
|---|---|---|---|
| GPT-5.5 | 0.873 | 1167 | $0.25 |
| Claude Opus 4.7 | 0.881 | 1008 | $0.14 |
| GPT-5.4 | 0.863 | 1074 | $0.17 |
| Claude Sonnet 4.6 | 0.792 | 1022 | $0.30 |
| Gemini 3.1 Pro | 0.693 | 1149 | $0.16 |
| Gemini 3 Flash | 0.608 | 1034 | $0.02 |
| Gemini 3.1 Flash Lite | 0.599 | 880 | $0.01 |
| Gemini 3.5 Flash | 0.410 | 1112 | $0.05 |

- **Documented fail modes (paper abstract):** "(1) Failures mostly arise from **API mismatches**, while successful renders still suffer from **disconnected or floating 3D geometric components**. (2) **Test-time scaling**, such as higher thinking budgets and multi-turn refinement, improves performance overall."
- Project page: **"Physical Plausibility supersedes Executability"** … "Models frequently produce disconnected parts and misaligned structures"; "effective procedural 3D modeling requires a robust execution environment that provides high-fidelity feedback for iterative refinement."
- **Executability correlates only r = +0.481 with human-preference Elo** — code that runs is not code that looks right.
- Other named systems: **BlenderRAG** (retrieval-augmented Blender code synthesis), **Vision-as-Inverse-Graphics / ViGA** (ECCV 2026), **BlenderLLM** (arXiv 2412.14203), **SceneCraft**, **3D-GPT**, **gd3kr/BlenderGPT** (GPT-4-era, superseded). No live "BlenderBench" was found — 3DCodeBench is the current benchmark.

## B5. LLM systems that output USD
- **BowerBot** (binary-core-llc/bowerbot) — Apache-2.0, Python 3.12+, **OpenUSD 26.x**; runs as its own LLM agent **or** as an MCP-mode tool provider; authors **ASWF-compliant asset folders**, `references` / `defaultPrim` / `metersPerUnit` / `upAxis`, UsdLux lighting, MaterialX / UsdPreviewSurface materials, USD variant sets, USD physics, **`UsdValidation` / usdchecker**-based validation, USDZ packaging; multi-LLM via litellm. Self-describes as block-out, **not** final scene generation. https://github.com/binary-core-llc/bowerbot
- NVIDIA publishes Omniverse / NanoUSD agent skills.

## B6. Honest limitations (documented)
- **API drift across Blender versions** breaks hardcoded enum identifiers and node names (blender-ai-mcp calls it failure mode #1; mcp-for-blender's own server instructions tell the model to read enums from `bl_rna` and look nodes up by `type`, not localised name).
- **Context-sensitive operators fail** when the active object/mode/selection is wrong (blender-ai-mcp).
- **Hallucinated / incorrect APIs dominate** the only large public benchmark (3DCodeBench: "failures mostly arise from API mismatches").
- **Executability ≠ quality:** successful scripts still produce floating/disconnected geometry and physically implausible assemblies (3DCodeBench; r = 0.481 vs human Elo).
- **Viewport feedback is weak or absent:** mcp-for-blender is request/response with a 180 s timeout; blend-ai documents "no real-time feedback … no streaming of viewport updates or render progress" and headless viewport capture may not work; the official add-on executes code with "no guards".
- **Headless trap:** mcp-for-blender states commands "never execute" under `blender -b` — a GUI (or `xvfb-run`) is required.
- **Security:** all these servers execute arbitrary LLM-written Python inside Blender. Only blend-ai (AST blocklist/allowlist), blender-mcp-ultra and mcp-for-blender safe mode offer any script validation; the official Blender server explicitly does not and recommends a VM or a machine with no sensitive data.

---

# C) RENDER + CLOUD BURST
All figures fetched/scraped 17 Sep 2026 unless dated otherwise.

## C1. Render farms that accept Blender

### SheepIt (free / peer-to-peer)
- **Pricing: FREE.** No subscription, no credit card, no per-frame fee; funded by donations (AdSense discontinued May 2026). https://www.sheepit-renderfarm.com/faq · https://www.sheepit-renderfarm.com/news/1779036336
- **Blender 5.2 LTS: CONFIRMED** — "Blender 5.2 is available!" news post dated 15 July 2026. https://www.sheepit-renderfarm.com/news/1784135430
- **Cycles: CONFIRMED** — "Cycles, Eevee, and Workbench included." https://www.sheepit-renderfarm.com/home
- **Officially supported: Yes** — Blender-only distributed farm; only stable Blender releases added, project version user-selectable.
- **Priority/credit model (the real "price"):** earn **38 points per CPU render-minute**, **684 points/min at 100% GPU** (GPU = 18× CPU); project owner **spends 10 points/min (CPU) or 180 points/min (GPU)**. Points scaled to a reference machine = Intel i5-9600 (CPU) / NVIDIA RTX 3060 (GPU). Non-transferable. No minimum spend; a project deprioritises/pauses if points go negative.
- **Constraints:** 3 concurrent projects; 2,048 MB max project; EXR capped 4096×2160 (animations only); no beta/daily builds; one GPU per client session.
- Contributor hardware bar raised to "capable of running Blender 5.1" (10 Aug 2026); AMD + Apple GPU rendering re-enabled 10 Aug 2026 as a large-scale test that may be reverted by end-2026. https://www.sheepit-renderfarm.com/news/1786381217
- Live network at fetch time: 430 connected clients, ~7,419 frames/hour, 33 active projects, 76,443 frames remaining.

### RenderStreet
- **Pricing:** subscription (unlimited) OR pay-as-you-go per server-hour, billed per minute; no setup/transfer/hidden fees; no minimum stated. https://render.st/plans-pricing/
  - **RenderStreet One (unlimited Blender CPU): $59.97/month.** $1.00 one-day trial. https://render.st/one/
  - **On-demand CPU: from $3.00/server-hour** (48/72-thread servers).
  - **On-demand GPU: $4.49/server-hour on NVIDIA L40S (48 GB VRAM), CUDA + OptiX.** https://render.st/engine-blender-cycles/
  - Studio plan: custom quote, "1,000+ hours per month", volume discounts.
- **Blender 5.2 LTS: CONFIRMED explicitly** — "Blender 5.2 with Cycles X, plus 5.1, 5.0, 4.5, 4.4, 4.3 LTS, 3.6 LTS, 2.93 LTS, 2.83 LTS." https://render.st/engine-blender-cycles/
- **Cycles: CONFIRMED** (dedicated Cycles engine page, CPU+GPU, auto job routing). **Officially supported: Yes** — Blender+Modo only, founded 2012 as the first Blender-dedicated farm.

### GarageFarm
- **Pricing:** prepaid credits, pay-as-you-go per GHz-hour (CPU) / OctaneBench-hour (GPU); tiered by queue priority; **$50 free credits for Blender users**, no credit card. https://garagefarm.net/pricing · https://garagefarm.net/blender-render-farm
  - **CPU:** $0.024/GHz·h Low Priority (≤100 nodes); $0.036/GHz·h Medium (≤150); $0.072/GHz·h High (≤300).
  - **GPU:** $0.004/OB·h Low (15 nodes, up to 48 GB VRAM); $0.006/OB·h Medium (30 nodes, up to 96 GB); $0.012/OB·h High (60 nodes, up to 96 GB).
  - **Per-GPU-hour equivalent: UNVERIFIED** — bills by OctaneBench-hour and does not publish node OB ratings.
- **Cycles: CONFIRMED**, CPU and GPU modes both supported. **Officially supported: Yes** — 33% Blender-artist discount, Corporate Member of the Blender Development Fund, 13,000+ Blender artists.
- **Blender 5.2 LTS: UNVERIFIED** — the Blender page shows only "we support almost every version released by the Blender Foundation"; 5.2 is not named.

### Fox Renderfarm
- **Pricing:** prepaid credits tiered by accumulated recharge; billed per node per hour; $25 free trial; first-recharge bonus up to 40%. https://www.foxrenderfarm.com/pricing.html
  - **GPU nodes:** Ordinary **$1.224**, Silver **$1.102**, Gold **$0.979**, Platinum **$0.857**, Diamond **$0.734** per node per hour (Silver ≥$500, Gold ≥$2,000, Platinum ≥$5,000, Diamond ≥$10,000 cumulative recharge).
  - **GPU node model/VRAM: UNVERIFIED.** **CPU unit price: UNVERIFIED** (page gives the formula but not the numeric unit price in rendered HTML). Default 64 GB RAM per node; more RAM costs extra; certain engines surcharge.
- **Cycles: CONFIRMED** — "Optimized for Cycles, EEVEE, supporting both CPU and GPU rendering at scale." https://www.foxrenderfarm.com/blender-render-farm.html
- **Blender 5.2 LTS: UNVERIFIED** — no version list rendered.

### RebusFarm
- **Pricing:** prepaid RenderPoints; no minimum turnover; upload/download and data storage free. https://rebusfarm.net/buy/products
  - **CPU 2.21 JPY/GHz·h; GPU 0.83 JPY/OB·h.** 1 RenderPoint = 184.09 JPY. Free trial **25 RenderPoints = 4,602.25 JPY** (English Blender page shows "$29.38 Free Trial").
  - **USD per-GHz·h: UNVERIFIED** — site geo-served JPY on every attempt.
  - Volume discounts 5% (500 RP) to 60% (50,000 RP); 50% student discount.
- **Cycles: CONFIRMED** — "Cycles CPU, Cycles GPU and EEVEE" plus Standard. **Officially supported: Yes.**
- **Blender 5.2 LTS: NOT LISTED** — supported-version list ends at "Blender 5.0, Blender 5.1". https://rebusfarm.net/3d-software/blender-render-farm

### iRender
- **Pricing:** IaaS — rent a dedicated multi-GPU cloud workstation with remote desktop (not a template farm); billed per node per hour, per minute, no minimum, 100% first-deposit bonus. https://irendering.net/price/
  - **RTX 4090 nodes:** 1× $8.2, 2× $15, 4× $30, 8× $52 per node/hour; 3h+ prepay → $7.38 / $13.5 / $27 / $46.8.
  - **RTX 5090 (32 GB) nodes:** 1× $10.8, 2× $20, 4× $38, 8× $62 per node/hour; 3h+ → $9.72 / $18 / $34.2 / $55.8.
  - **Derived per-GPU:** RTX 4090 **$8.20 → $6.50/GPU/hr**; RTX 5090 **$10.80 → $7.75/GPU/hr**.
- **Cycles: CONFIRMED**; Blender a named solution. **Blender 5.2 LTS:** implicitly yes (you install your own build) but iRender publishes no version matrix — explicit 5.2 statement **UNVERIFIED**.
- Node specs: 256 GB RAM, 2 TB NVMe, Windows or Ubuntu, Threadripper PRO.

## C2. Cloud GPU rental — on-demand $/hour per GPU (17 Sep 2026)

**RunPod** (per-second billing, no egress fees; storage extra; default spend limit $80/hr). Official JSON-LD offers scraped from https://www.runpod.io/pricing:

| GPU | Community | Secure |
|---|---|---|
| RTX 4090 24GB | $0.34 | $0.74 |
| RTX 5090 32GB | $0.69 | $0.99 |
| A100 PCIe 80GB | $1.19 | $1.59 |
| A100 SXM 80GB | $1.39 | $1.59 |
| L40S 48GB | $0.79 | $1.09 |
| H100 SXM | $2.69 | $3.49 |
| H100 PCIe | $1.99 | $2.89 |
| H100 NVL | $2.59 | $3.19 |
| H200 | $3.59 | $4.59 |
| B200 | $5.98 | $6.79 |
| B300 | $6.94 | $7.89 |
| RTX 6000 Ada | $0.74 | $0.84 |
| L40 | $0.69 | $0.82 |
| L4 | $0.44 | $0.49 |
| RTX 3090 | $0.22 | $0.50 |

- Storage: container disk $0.10/GB/mo running; volume disk $0.10/GB/mo running / $0.20/GB/mo stopped; network volume $0.07/GB/mo (<1TB) or $0.05/GB/mo (>1TB). No egress fees. 31 global regions. https://docs.runpod.io/pods/pricing
- Caveat: RunPod's docs say to find latest pricing in the console during deployment — static page rates can drift.

**Vast.ai** (marketplace; supply/demand across 40+ data centres; per-second billing; on-demand / interruptible / reserved; no minimums). Live API snapshot 17 Sep 2026, on-demand, full-GPU offers only (min / median $/hr):

| GPU | min | median | n |
|---|---|---|---|
| RTX 4090 | $0.136 | $1.030 | 16 |
| RTX 5090 | $0.213 | $1.650 | 25 |
| A100 SXM4 80GB | $0.536 | $0.696 | 17 |
| A100 PCIe | $0.535 | $2.668 | 23 |
| L40S | $0.476 | $2.401 | 19 |

Source: public search API `https://console.vast.ai/api/v0/bundles/` (model described at https://vast.ai/pricing). Vast publishes no fixed rate card; the live table is JS-rendered. Vast's own dated comparison (checked 20 Jul 2026): RunPod H100 $2.99, H200 $4.39, B200 $5.89, B300 $7.39; Lambda H100 $3.99, B200 $6.69; CoreWeave H100 $6.16, H200 $6.31, B200 $8.60. https://vast.ai/article/how-much-does-it-cost-to-rent-a-gpu-in-the-cloud-live-pricing-guide (third-party; treat as such).

**Lambda** (per-minute billing, "no egress fees"; data-centre GPUs only — no RTX 4090/5090). https://lambda.ai/instances

| GPU | $/GPU/hr |
|---|---|
| B200 SXM6 180GB | $6.69 |
| H100 SXM 80GB | $3.99 |
| A100 SXM 80GB | $2.79 |
| A100 SXM 40GB | $1.99 |
| Tesla V100 16GB | $0.79 |

Storage pricing / whether persistent storage is extra: **UNVERIFIED**.

**Paperspace / DigitalOcean** (hourly; now owned by DigitalOcean). https://www.paperspace.com/pricing
- H100 **$5.95/hr on-demand promo**; $2.24/hr is a 3-year commitment. A100-80G: $1.15/hr is a 3-year commitment; **on-demand A100-80G price UNVERIFIED.**
- A6000 $1.89 · A5000 $1.38 · A4000 $0.76 · V100 $2.30 · RTX5000 $0.82 · P6000 $1.10 · P5000 $0.78 · RTX4000 $0.56 · P4000 $0.51 · M4000 $0.45 per hour.
- Plans: Free $0; Pro $8/mo (a second card block shows $12/mo); Growth $39/mo — all plus utilisation costs; storage overage $0.29/GB.
- Region **UNVERIFIED**; RTX 4090/5090 availability **UNVERIFIED**. Page card layout is jumbled (H100 card body lists A100 specs) — treat individual labels with care.

**Modal** (serverless; per-second billing; region multipliers 1.15–1.75×; non-preemptible 3×). https://modal.com/pricing

| GPU | $/hr (computed ×3600) |
|---|---|
| B300 | $7.10 |
| B200 | $6.25 |
| H200 SXM | $4.54 |
| H100 SXM5 | $3.95 |
| RTX PRO 6000 | $3.03 |
| A100 80GB | $2.50 |
| A100 40GB | $2.10 |
| L40S | $1.95 |
| A10 | $1.10 |
| L4 | $0.80 |
| T4 | $0.59 |

- CPU $0.0000131/core/s (min 0.125 core/container); memory $0.00000222/GiB/s; volumes $0.09/GiB/mo (first 1 TiB/mo free). Plans: Starter $0 (+ $30/mo free compute, 10 GPU concurrency); Team $250/mo (+ $100/mo free compute, 50 GPU concurrency); Enterprise custom.

**Azure VM** (East US, Linux, pay-as-you-go; official Retail Prices API, queried 17 Sep 2026). Storage and egress additional.
- NC-series A100: `Standard_NC24ads_A100_v4` (1× A100 80GB) **$3.673/hr**; Spot $0.67877; Low Priority $0.735
- NC-series H100: `Standard_NC40ads_H100_v5` (1× H100 94GB) **$6.98/hr**; Spot $1.289904; Low Priority $1.396
- ND-series A100: `Standard_ND96asr_v4` (8× A100 40GB) $27.197/hr = **$3.3996/GPU/hr**; Spot $5.904469
- ND-series H100: `Standard_ND96isr_H100_v5` (8× H100 80GB) $98.32/hr = **$12.29/GPU/hr**; Spot $18.169536
- Source: `https://prices.azure.com/api/retail/prices?$filter=armSkuName eq '...' and armRegionName eq 'eastus'`

**AWS EC2** (us-east-1, Linux, on-demand; official pricing feed, manifest hawkFilePublicationDate 2026-09-10). EBS and egress additional.
- g6.xlarge (1× L4) $0.8048 = **$0.8048/GPU/hr**; g6.12xlarge (4× L4) $4.6016 = $1.1504; g6.48xlarge (8× L4) $13.3504 = $1.6688
- g6e.xlarge (1× L40S) $1.8610; g6e.12xlarge (4× L40S) $10.4926 = $2.6232; g6e.48xlarge (8×) $30.1312 = $3.7664
- g7.48xlarge (8× RTX PRO 4500) $28.5133 = $3.5642; g7e.2xlarge (1× RTX PRO 6000) $3.3631; g7e.48xlarge (8×) $33.1443 = $4.1430
- p4d.24xlarge (8× A100 40GB) $21.9576 = $2.7447; p4de.24xlarge (8× A100 80GB) $27.4471 = **$3.4309**
- p5.4xlarge (1× H100 80GB) $6.8800; p5.48xlarge (8×) $55.0400 = **$6.88/GPU/hr**
- p5en.48xlarge (8× H200 141GB) $63.2960 = $7.912; p6-b200.48xlarge (8× B200) $113.9328 = $14.2416
- Sources: AWS pricing feed `.../ec2/USD/current/ec2-ondemand-without-sec-sel/US East (N. Virginia)/Linux/index.json`; GPU counts https://docs.aws.amazon.com/ec2/latest/instancetypes/ac.html
- **Anomaly flagged:** AWS docs list g6.16xlarge as 1× L4 and g6e.16xlarge as 1× L40S, but they price higher than the 4-GPU 12xlarge. Use the 12xlarge/48xlarge rows for clean per-GPU maths.

### Quick comparison — $/GPU-hour, on-demand (17 Sep 2026)

| Provider | RTX 4090 | RTX 5090 | A100 80GB | L40S | H100 80GB | B200 |
|---|---|---|---|---|---|---|
| RunPod Community | 0.34 | 0.69 | 1.39 (SXM) | 0.79 | 2.69 (SXM) | 5.98 |
| RunPod Secure | 0.74 | 0.99 | 1.59 (SXM) | 1.09 | 3.49 (SXM) | 6.79 |
| Vast.ai (min/median) | 0.136 / 1.030 | 0.213 / 1.650 | 0.536 / 0.696 (SXM4) | 0.476 / 2.401 | not verified | not verified |
| Lambda | not offered | not offered | 2.79 | not offered | 3.99 | 6.69 |
| Paperspace | not listed | not listed | unverified | not listed | 5.95 (promo) | not listed |
| Modal | not offered | not offered | 2.50 | 1.95 | 3.95 (SXM5) | 6.25 |
| AWS us-east-1 | not offered | not offered | 3.4309 (p4de) | 1.861 (g6e.xlarge) | 6.88 (p5) | 14.2416 (p6) |
| Azure East US | not offered | not offered | 3.673 (NC24ads) | not offered | 6.98 (NC40ads) | not offered |

## C3. RTX 3080-class render time, 1080×1920, 64–128 samples, denoised

**Method.** Blender Open Data score = "estimated number of samples per minute, summed for all benchmark scenes" (https://opendata.blender.org/about/). The benchmark measures **average time per sample** (it sets `cycles.samples = 1<<24` with a 30-second time limit and disables adaptive sampling), so seconds-per-sample is the raw measurement (benchmark script `render.py`, https://opendata.blender.org/cdn/BlenderBenchmark2.0/script/blender-benchmark-script-3.1.1.tar.gz). Current benchmark scene sample counts: classroom = 300, junkshop = 240, monster = 256.

**RTX 3080 (10 GB) measured figures** derived from Blender Open Data medians (checked Jun 2026):

| Scene | OptiX s/sample | OptiX s/frame | CUDA s/frame |
|---|---|---|---|
| classroom (300 spp) | 0.05059 | 15.18 | 26.42 |
| junkshop (240 spp) | 0.04415 | 10.60 | 18.31 |
| monster (256 spp) | 0.02646 | 6.77 | 9.91 |

Blender Benchmark score 4,812.41. Source: https://www.renderjuice.com/gpus/compare/rtx-3080-vs-rtx-5060 (states these "are derived from Blender Open Data benchmark medians and should be treated as comparative estimates, not guaranteed real-project render times"). Comparators: RTX 3090 OptiX 12.67/8.78/5.56 s (score 5,825); RTX 4090 OptiX 6.21/5.06/2.58 s (11,687); RTX 5090 OptiX 4.81/3.64/2.10 s (15,016). Primary query UI: https://opendata.blender.org/benchmarks/query/

Independent cross-check from the raw Open Data snapshot (CC0, 17 Sep 2026), RTX 3080 medians on older full-render scenes (dominantly Blender 2.90 submissions — indicative only): **bmw27 (the classic hard-surface/mechanical car) OptiX 11.55 s (n=366), CUDA 27.03 s (n=686)**; fishy_cat 21.31 s; koro 45.36 s; pavillon_barcelona 54.89 s; victor 81.37 s; classroom 43.02 s. Source: https://opendata.blender.org/snapshots/opendata-latest.zip

**Estimate for a moderately complex mechanical scene at 1080×1920 on an RTX 3080.** Assumptions, all explicit:
(a) 1080×1920 = 2,073,600 px, exactly the same pixel count as 1920×1080; Cycles cost is approximately linear in pixel count at fixed samples, and orientation does not change cost.
(b) A "moderately complex mechanical scene" sits between the light monster scene and the heavy junkshop/classroom interiors: bracket **0.03–0.05 s/sample OptiX**, 0.04–0.09 CUDA.
(c) Denoising (OptiX/OIDN) adds roughly **0.5–1.5 s/frame** at this resolution.
(d) Adaptive sampling off or nominal; with it on, the nominal sample count is an upper bound.

Results:
- **64 samples, OptiX: ~3–5 s/frame** (1.9–3.2 s render + ~1 s denoise)
- **128 samples, OptiX: ~5–8 s/frame**
- 64 samples, CUDA-only: ~2.6–5.8 s/frame + denoise
- 128 samples, CUDA-only: ~5.1–11.5 s/frame + denoise
- Point anchors at 256/240/300 samples OptiX: monster 6.8 s, junkshop 10.6 s, classroom 15.2 s.

Qualitative corroboration that 64–128 samples + OptiX denoiser is the normal interior target: https://1001ferramentas.com/en/tools/tempo-render-blender-cycles-resolucao

**UNVERIFIED in C3:** the **render resolution of the Blender Benchmark scenes** is not stated on any official page fetched (Open Data About/Download/Query, benchmark script, launcher). If they are 1920×1080 the s/sample figures transfer directly to 1080×1920; otherwise scale by pixel count per assumption (a). No single benchmark was found that is simultaneously a mechanical/CAD scene, 1080×1920 or 1080p, and 64/128 samples with denoising — the numbers are a stated derivation, not one cited measurement.

## C — bottom-line decisions
1. **Blender 5.2 LTS + Cycles explicitly confirmed** at SheepIt (free), RenderStreet; Cycles confirmed at Fox (version unverified) and RebusFarm (only up to 5.1 listed); GarageFarm (Cycles yes, 5.2 unverified); iRender (self-installed, so 5.2 effectively available but unstated).
2. **Cheapest metered Blender GPU rendering** is Vast.ai on-demand (marketplace, volatile) and RunPod Community Cloud. The fully-managed farms bill on server-hour / GHz·hour / OB·hour / node-hour, so true apples-to-apples $/GPU-hr exists only at **iRender ($6.50–$10.80/GPU/hr)** and **RenderStreet GPU ($4.49/server-hour L40S)**.
3. **RTX 3080-class 1080×1920 Cycles at 64–128 samples + denoise: budget ~3–8 s/frame (OptiX)**; CUDA-only is roughly **1.5–1.8× slower**. The benchmark scene resolution is the one open item.

---

# D) AI VOICE + CAPTIONS + VIDEO
All figures fetched **17 September 2026**. Vendor's own page unless marked SECONDARY/unverified.

## D1. ElevenLabs
Current flagship TTS = **Eleven v3** (`eleven_v3`, `eleven_v3_conversational`, `eleven_ttv_v3`). **No v4 in the docs.**

| Tier | $/month | Credits/month | ≈ TTS min | Seats |
|---|---|---|---|---|
| Free | $0 | 10,000 | ~10 | 1 |
| Starter | $6 | 30,000 | ~30 | 1 |
| Creator | $22 (first month $11) | 121,000 | ~121 | 1 |
| Pro | $99 | 600,000 | ~600 | 1 |
| Scale | $299 | 1,800,000 | ~1,800 | 3 |
| Business | $990 | 6,000,000 | ~6,000 | 10 |
| Enterprise | custom | custom | custom | custom |

Annual = monthly × 10 (two months free); effective monthly **$5 / $18.33 / $82.50 / $249.17 / $825**. https://elevenlabs.io/pricing

**Eleven v3 availability: checked on ALL tiers including Free.** Other table rows:

| Row | Free | Starter | Creator | Pro | Scale | Business |
|---|---|---|---|---|---|---|
| Commercial use | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Eleven v3 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Instant Voice Cloning | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Professional Voice Cloning | ✗ | ✗ | 1 | 1 | 3 | 10 |
| WAV/PCM 44.1 kHz | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| Custom voice slots | 3 | 10 | 30 | 160 | 660 | 2,200 |
| Audio quality | 128 | 128 | 128/192 | 128/192 | 128/192 | 128/192 |
| Extra minute | ~$0.36 | ~$0.20 | ~$0.18 | ~$0.17 | ~$0.17 | ~$0.17 |
| Concurrent requests | 2 | 3 | 5 | 10 | 15 | 25 |

**API rates (USD, separate from credits):** v3 **$0.10/1K chars = $100/1M**; v3 Conversational $0.05/1K = **$50/1M**; v2 Multilingual $0.10/1K; Flash/Turbo $0.05/1K. Scribe STT $0.22/hr ($0.39 realtime); Music $0.15/min; Voice Changer/Isolator $0.12/min; Dubbing v2 $2.20/min. Credits: 1/char TTS, 0.5–1/char Flash/Turbo API, STT 330/min; rollover up to 2 months (max balance 3×), none on Free. **Commercial use requires Starter+; Free is non-commercial with no cloning.**

**UNVERIFIED — Eleven v4:** an i18n key `tts_eleven_v4` exists in the page payload and press covered a Summit 2026 demo, but v4 is absent from docs and no row renders. Treat as announced-only.

## D2. Alternatives
- **PlayHT / PlayAI — SHUT DOWN.** Meta acquired the team Jul 2025; API offline ~26 Jul 2025; full sunset **31 Dec 2025** (accounts, audio and voice clones deleted). **`play.ht` and `play.ai` no longer resolve.** No 2026 pricing exists. https://inworld.ai/resources/migrate-from-playht
- **Cartesia — Sonic-3.6** (GA ~27 Aug 2026), STT **Ink-2**. Plans: Free $0 (20K credits ~27 min) · **Pro $5** (100K ~133 min) · Startup $49 (1.25M) · Scale $299 (8M) · Enterprise. **1 credit = 1 character; 1 min ≈ 750–800 credits.** Overage per 1M credits: **Pro $65 · Startup $45 · Scale $38**. Instant cloning from Pro; Professional cloning at Startup (2) / Scale (4). **Commercial licence starts at Pro; Free has none.** STT $0.39/audio hour on Scale. https://www.cartesia.ai/pricing
- **OpenAI TTS:** **tts-1 $15/1M chars; tts-1-hd $30/1M chars; gpt-4o-mini-tts $0.60/1M text tokens in + $12/1M audio tokens out.** 13 voices, no cloning. Commercial use permitted, no ownership claim. (Sora 2 $0.10/s 720p; Sora 2 Pro $0.30/s 720p → $0.70/s 1080p.) https://developers.openai.com/api/docs/pricing
- **Google (two products):**
  - Gemini API TTS (**Preview**): Gemini 3.1 Flash TTS Preview $1/1M text tokens in + $20/1M audio tokens out (batch $0.50/$10); Gemini 2.5 Flash TTS $0.50/$10; Gemini 2.5 Pro TTS $1/$20. Audio = **25 tokens/second** → 2.5 Flash TTS ≈ $0.50/min (derived).
  - Cloud TTS: **Chirp 3: HD $30/1M chars; Instant custom voice $60/1M** (the cloning path); Studio $160/1M; Neural2/Polyglot $16/1M; **WaveNet/Standard $4/1M**. Free tiers 1M (Chirp3/Studio/Neural2) or 4M (WaveNet/Standard) chars/month.
- **MiniMax — Speech 2.8.** **speech-2.8-hd $100/1M chars; speech-2.8-turbo $60/1M**; ASR $0.38/hr; **Rapid Voice Cloning $1.50/voice** (charged on first synthesis); Voice Design $3/voice. Audio subscriptions: Starter $5/100K points → Business $999/20M (yearly 20% off: $48/$288/$950/$2,390/$9,590). https://platform.minimax.io/docs/guides/pricing-paygo
- **Fish Audio — S2.1** (`s2.1-pro`, `s2.1-pro-free`) and **S2-pro**. Plans: Free $0 (8,000 credits ~7 min) · Plus $11/mo ($132/yr) · Pro $75/mo ($900/yr, 2M credits, 3 seats) · Max $749/mo ($8,988/yr) · Enterprise. **API: $15.00 per 1M UTF-8 bytes** (~180,000 English words ≈ 12 h speech) for s2.1-pro / s2-pro / s1; **s2.1-pro-free $0**. ASR $0.36/audio hour. ~600–625 credits/min. **Licence caveat:** the plan page lists commercial use on Free, but the FAQ says Free is personal/non-commercial only — **treat Free as non-commercial.** https://fish.audio/plan/

## D3. Captions / subtitles / editors
| Tool | Version | Date | Licence |
|---|---|---|---|
| **whisper.cpp** | **v1.9.4** | 2026-09-11 | MIT |
| **faster-whisper** | **v1.2.1** | 2025-10-31 | MIT |
| **WhisperX** | **v3.8.6** | 2026-05-25 | BSD-2-Clause |
| openai-whisper (reference) | PyPI 20250625 | — | MIT |
| **Remotion** | **v4.0.525** | 2026-09-15 | see LICENSE.md |

All three Whisper forks are free and permissive — no per-seat or per-minute cost.

**Remotion licensing (page updated 16 Sep 2026): https://www.remotion.dev/docs/license/pricing**
- **Free License** — individuals and companies of **up to 3 people**; all features; **unlimited commercial use**; must upgrade when the org grows.
- **Company License** (4+ people): **"Remotion for Creators" $25/month per seat** (3 seats = $75); **"Remotion for Automators" $0.01 per render with a $100/month minimum** (developers on automation projects do not need a seat); includes $250 Mux credits.
- **Enterprise from $500/month.**
- **≈ $300 per seat per year.**

**CapCut** — publishes **no price sheet**; `/pricing`, `/plans`, `/pro`, `/vip` 404 or absent. SECONDARY: Free $0 · Standard ≈ $9.99/mo · Pro ≈ $19.99/mo or $179.99/yr · Team ≈ $15–30/seat/mo. Pro roughly doubled from ~$9.99/mo in the late-2025/early-2026 restructure. **Licence trap: CapCut's ToS (updated 15 Apr 2026) grants CapCut a broad perpetual sub-licensable licence over uploaded/created content on free and paid plans alike, and grants NO rights to its built-in sound recordings/music — not cleared for commercial delivery on any tier.**

**Adobe After Effects** — adobe.com plan pages are fully client-rendered (no prices reachable). SECONDARY "verified Sep 2026": single-app **$22.99/mo annual billed monthly**, $19.99/mo annual prepaid, $34.49/mo month-to-month; CC All Apps $59.99/mo. **SECONDARY/UNVERIFIED.**

**Alternatives:** DaVinci Resolve free / **$295 one-time** Studio; Final Cut Pro **$299.99 one-time**.

## D4. AI image / video generation
- **Midjourney — current model V8.2** (24 Jul 2026; V8.1 alpha 14 Apr 2026; latest alpha changelog 16 Sep 2026; V8 series still on `alpha.midjourney.com`). *Pricing SECONDARY (Cloudflare 403 on midjourney.com):* Basic $10, Standard $30, Pro $60, Mega $120 per month. *Licence:* free trial CC BY-NC 4.0; paid plans commercial; **companies >$1M prior-year gross revenue must be on Pro or Mega**; Stealth (private) Pro+ only — below that images are public by default; **no IP indemnification on any plan**. Verdict: usable for matte paintings/textures; budget Pro.
- **Black Forest Labs FLUX — family FLUX 3 (video) + FLUX.2 [max]/[pro]/[flex]/[klein] (image).** 1 credit = $0.01. Per image: **klein 4B from $0.014; klein 9B from $0.015; pro from $0.03 (t2i) / $0.045 (edit); flex from $0.05; max from $0.07.** FLUX 3 video per second: t2v/i2v **$0.17 hd / $0.29 fhd / $0.40 qhd / $0.80 uhd / draft $0.06**; v2v $0.41–$0.95. **Weights: klein 4B + 4B Base = Apache 2.0 (commercial); klein 9B / 9B Base and FLUX.2 [dev] = non-commercial.** Commercial weight tiers: Builder (klein, 10K images/mo, 1 domain, 10 users), Platform (klein 9B + dev), Professional (dev, up to 3 domains, agencies, per-client fees beyond 3), Enterprise — **prices not published (UNVERIFIED)**. https://bfl.ai/pricing · https://bfl.ai/licensing
- **Runway — Gen-4.5**, Aleph 2.0, plus hosted Kling 3.0, Seedance 2.0/2.5, Nano Banana Pro. Plans: Free $0 (125 one-time credits); **Standard $15/mo ($12 annual, 625 credits); Pro $35/mo ($28 annual, 2,250); Max $95/mo ($76 annual, 9,500)**. Credit costs: **Gen-4.5 60 credits/5 s = 12 credits/sec**; Aleph 2.0 140/5 s; Gen-4 Image 1080p 8 credits/image, Turbo 2; Nano Banana Pro 2K 20. **$/credit NOT published (UNVERIFIED).** Licence (ToS updated 15 Sep 2026 §4.4): Runway does not claim ownership and does not restrict commercial use, **but Inputs/Outputs may be used to train its models, and API apps must display "Powered by Runway"**. https://runwayml.com/pricing
- **Kling AI — VIDEO 3.0 / 3.0 Omni**, 3–15 s, native audio, multi-shot, native 4K. Basic **$0 free forever, NOT for commercial use**; Standard **$6.99** (list $10) 660 credits; Pro **$25.99** (list $37) 3,000; Premier **$64.99** (list $92) 8,000; Ultra **$127.99** (list $180) 26,000. Standard+ = commercial use, 1080p, watermark removal. **4K = 30 credits/second.** https://klingai.com/blog/kling-video-3-0-credit-cost-guide
- **Google Veo — Veo 3.1** (`veo-3.1-generate-preview` / `-fast-` / `-lite-`), 8 s, up to 4K, native audio, up to 3 reference images, first/last-frame. Per second: **Standard $0.40 (720p/1080p), $0.60 (4k); Fast $0.10 / $0.12 / $0.30; Lite $0.05 / $0.08 / n/a.** 8 s ≈ $3.20 (Standard 1080p), $0.80 (Fast 720p). Charged only on success. **No Veo 4 as of 17 Sep 2026.** Related image models: Nano Banana Pro (Gemini 3 Pro Image), Nano Banana 2, Nano Banana 2 Lite.
- **Luma — Ray3.2, Uni-1, Ray3.14**, plus orchestrated Veo 3.1, Kling 3.0/Omni, Seedance 2.0, Nano Banana Pro, GPT Image 2, Seedream, ElevenLabs v3. Plans: **Plus $30/mo (10,000 credits, commercial use), Pro $90 (40,000), Ultra $300 (150,000)**; yearly up to 20% off. **Per-generation $ NOT published (UNVERIFIED).** Production-relevant: **"Export for Production — deliver high-quality EXR files"**.

### Production decision summary
- **Voice:** ElevenLabs v3 (Creator $22 / Pro $99) is the only mainstream option with per-tier commercial licence + professional cloning; cheapest commercial cloning is Cartesia Pro $5; cheapest high volume is MiniMax speech-2.8-turbo $60/1M or Fish S2.1 $15/1M UTF-8 bytes; enterprise/BAA path is Google Chirp 3 HD $30/1M + Instant Custom Voice $60/1M. **PlayHT is not an option.**
- **Captions:** free (whisper.cpp / faster-whisper / WhisperX). Remotion is the only paid piece: free ≤3 people, else $25/seat/mo (~$300/seat/yr) or $0.01/render with a $100/mo floor.
- **Plates/textures/matte paintings:** best cost+rights is FLUX.2 (klein 4B $0.014 Apache-2.0; pro $0.03; max $0.07). Midjourney V8.2 for aesthetics but Pro $60/mo required >$1M, public by default below Pro, no indemnity. Moving backplates: Veo 3.1 Lite/Fast $0.05–$0.12/s; Runway Gen-4.5 12 credits/s; Kling 3.0 4K 30 credits/s; FLUX 3 draft $0.06/s for previs. Luma is the only tool advertising EXR delivery.
- **Licence red flags:** Midjourney (no indemnity, $1M rule, public below Pro) · Kling Basic (non-commercial) · Fish Free (non-commercial) · Cartesia Free (no commercial licence) · ElevenLabs Free (no commercial licence) · Runway (training on outputs; "Powered by Runway" for API apps) · FLUX.2 [dev] and [klein] 9B (non-commercial weights) · CapCut (broad content licence; no rights to bundled music).

### Section D — explicitly UNVERIFIED
ElevenLabs v4 pricing/availability · Midjourney plan prices from primary · CapCut exact prices · Adobe AE exact price from adobe.com · Runway $/credit · Luma $/generation · BFL open-weights tier prices · Cartesia embedded effective $/1M chars · Kling derived 720p per-clip credit cost · Gemini TTS derived $/minute.

---

# E) DIGITAL ASSET SOURCES (verified 17 September 2026)

## E1. Quixel Megascans — **no longer a free library**
- Epic announced (Sept 2024) that free access would end: *"In 2025, we will begin charging for Quixel Megascans … the majority of Megascans will no longer be available for free unlimited use in Unreal Engine projects."*
- **Legacy library access ended 1 January 2025:** *"As of January 1, 2025, new users can no longer access the legacy Megascans library to acquire or download new assets."* (Epic forum, 25 Aug 2025)
- **Not UE-only.** Since 2025, Megascans on Fab are governed by the **Fab Standard License**, which is engine/DCC-agnostic. The old UE-only "Unreal Unlimited" licence survives only for assets **not** re-downloaded from Fab: *"If not re-downloaded, these assets will remain subject to the Content EULA and will be considered UE-only content."*
- **2026 state:** Quixel's April 2026 news describes **"premium Megascans collections"** on Fab (Medieval Farm, New Wood, European Rural Furniture, Nordic Rauk Coast, Urban Ruin, European Broadleaf Forest) and states **Megaplants are "free to use under the Fab Standard License"**. So: a paid core catalogue plus a free subset (all Megaplants, some packs).
- **Fab EULA (last updated 1 Oct 2024):** Standard tiers Personal–Reference Only / Personal / Professional; you are eligible for Personal tiers only if you (with commonly-controlled entities) have **not generated more than $100,000 USD gross revenue from commercial activity in the digital content industry in the last 12 months**. Source assets available only on Personal/Professional. No standalone redistribution; NoAI-tagged content barred from generative-AI training.
- **Quixel Bridge / Quixel.com are slated for retirement** once Fab fully replaces Bridge (Quixel, 15 Sept 2025).
- **UNRESOLVED/UNVERIFIED:** free-vs-paid asset counts; whether a >$100k-revenue user must select Professional even for a *free* Megascans download (Epic forum thread is ambiguous; support reportedly advised consulting a lawyer).

Sources: https://quixel.com/news/quixel-on-fab-new-megascans-and-megaplants · https://80.lv/articles/epic-games-to-launch-tool-for-free-megascans-downloads-in-fab · https://forums.unrealengine.com/t/megascans-license/2081542 · https://forums.unrealengine.com/t/why-can-i-only-subscribe-and-not-download/2650156 · https://www.fab.com/eula · https://quixel.com/news/fab-in-launcher-brings-quixel-bridge-features-to-the-epic-games-launcher

## E2. Fab marketplace
- Epic's unified "open marketplace" replacing the UE Marketplace, Sketchfab's marketplace, ArtStation Marketplace and Quixel.com (~2.5M assets at launch).
- **Publishers receive 88% of revenue**; payments ~30 days after month end; **minimum $100 USD** (under $100 rolls over; unpaid revenue older than a year is paid regardless). Refunds deducted from next payout.
- **Licence types:** CC-BY (free) and Standard (Free or For Sale), with Personal / Professional price tiers. Buyers pick by revenue: **Personal ≤ $100,000 USD** gross commercial revenue in the last 12 months; **Professional > $100,000**.
- **Price ladder:** $0–100 in $1 steps; $100–150 in $5; $150–250 in $10; $250–500 in $25; $500–1,500 in $100; all end in .99; above $1,500 by request; VAT may be added. Code plugins are sold **per-seat**.
- **Fab EULA restrictions:** no standalone redistribution of Content; no combining Standard-licensed Content with GPL/LGPL/CC-BY-SA code or content; no use in world/level-editing tools that allow export; NoAI content barred from generative-AI datasets; liability capped at the greater of **$1,000 or 12 months' fees**.

Sources: https://dev.epicgames.com/documentation/fab/publisher-get-started-in-fab · https://dev.epicgames.com/documentation/fab/licenses-and-pricing-in-fab · https://www.fab.com/eula

## E3. Poly Haven
- **All assets CC0** — commercial use, **no attribution required**, redistribution allowed. Site ToS separately prohibits web scraping/data mining without permission.
- **Live API counts (17 Sep 2026): 997 HDRIs, 861 textures, 521 3D models** (~2,379 assets). HDRIs up to 24K (some 29–30K); models often max 4K textures. Free; optional Patreon.
- **UNVERIFIED:** exact current licence wording beyond the above; stats page showed 996 HDRIs at the same time (rolling).

Sources: https://polyhaven.com/license · `api.polyhaven.com/assets?t=hdris|textures|models` · https://polyhaven.com/stats

## E4. BlenderKit → **Blendkit**
blenderkit.com now redirects to **blendkit.com**; site self-describes as "Blendkit (formerly BlenderKit)".
- **Free $0/mo:** 23,228 models, 40,130 materials, 1,008 scenes, 4,929 HDRIs, 1,272 brushes; upload; 200 MiB private storage.
- **Full $17.90/mo or $118.80/yr ($9.90/mo equivalent):** full database (82,445 models, 40,130 materials, 4,482 scenes, 14,680 HDRIs, 6,946 brushes), 2 GiB storage, extra add-ons; 50% student discount.
- **Business $48/mo or $348/yr ($29/mo equivalent), per seat:** for entities with ≤5 employees and ≤$100k yearly revenue; 100 GiB storage.
- The annual totals **$118.80 / $348.00** appear in checkout metadata; the monthly-billing figures **$17.90 / $48** are reported by CG Channel (8 Jan 2026) — monthly figures are the less certain of the two.
- **Licences: only Royalty Free and CC0.** Both allow commercial use and selling higher-level derivative works, but **Royalty Free forbids reselling 3D models even if modified**. Subscription gives **70% to creators**. Free-tier assets are confirmed usable in commercial projects. DCC support now extends beyond Blender to Godot, Rhino and Maya.

Sources: https://www.blendkit.com/plans/pricing/ · https://www.blendkit.com/docs/licenses/ · https://www.cgchannel.com/2026/01/get-over-1000-free-3d-sculpting-brushes-from-blenderkit/

## E5. True Terrain (True-VFX)
- **Current version: True Terrain 5, build 5.1.4** (29 Mar 2026; requires Blender 5.1+). Not discontinued. Sold on True-VFX's own store and as "True Terrain 5" on Superhive.
- **Vendor-store pricing:** **TrueTERRAIN 5 (Early Access incl. full release) $99 USD**, described as reduced to **$75** until full release; **Lifetime upgrades $349**.
- **Conflicting third-party:** $59.99, LITE $9.99, upgrades $299.99 — **UNVERIFIED / possibly promotional or regional.** Superhive's own page was Cloudflare-blocked (403), so its price is **unverified**.

Sources: https://truevfx.gumroad.com/l/TrueTerrain · https://store.true-vfx.xyz/l/True-Terrain-Lifetime · https://www.lookae.com/true-terrain-514/

## E6. Gaea (QuadSpinner)
- **Current stable: Gaea 2.3** (15 June 2026) — adds a macro system and 16K baking. **Gaea 2.4 and Gaea 3.0 release dates were pushed back.** **Gaea 3.0 is in Early Access** (CyberWeek 2025 pre-orderers); **public beta estimated October 2026**; Gaea 3.0 is a **free upgrade with Gaea 2 purchases**. **Gaea 2 remains supported through end 2027.**
- **Perpetual licences (no subscription):**
  - **Community — Free.** Learning/evaluation only; **commercial use: No**; 1024×1024 builds; no tiling, no macros, no UE integration.
  - **Indie — $99.** Node-locked (one named user, up to 2 computers); revenue **< $100K**; 8K; tiling; Gaea2Unreal bridge; macros.
  - **Professional — $199.** Node-locked; revenue **< $1M**; 16K (256K with tiles); Regions; limited automation; Gaea2Houdini; create macros.
  - **Enterprise — $299.** **Movable** licence; **revenue > $1M**; automation workflows; optional Offline and Floating add-ons.
- Perpetual; major upgrades optional and paid; **30% loyalty discount** for major-version upgrades; free minor updates; no refunds; **PayPal no longer supported**.

Sources: https://www.cgchannel.com/2026/06/quadspinner-releases-gaea-2-3/ · https://quadspinner.com/Gaea3 · https://quadspinner.com/Order/ · https://quadspinner.com/Legal

## E7. Blender Market → **Superhive**
- Rebranded to **Superhive** (superhivemarket.com), in place by **April 2025** (attributed to the "Blender" trademark). Same entity as CGCookie/Superhive — a name change, not a change of ownership.
- Creator-set, per-product one-off purchases (no platform-wide subscription); bundles sold. Licence documentation distinguishes standard/royalty-free asset licences from extended commercial licences, with GPL guidance for code add-ons.
- **UNVERIFIED:** typical price bands; exact default commercial licence clause text (support site Cloudflare-403 to automated fetch).

Sources: https://blenderartists.org/t/superhive-formerly-blendermarket-detected-as-a-theat-by-bitdefender-antivirus/1590320 · https://support.superhivemarket.com/article/226-understanding-product-license-types · /article/54-available-licensing-options · /article/249-gpl-myths-and-misunderstandings

## E8. Industrial / engineering asset sources

### Free CAD libraries (pipes, valves, fittings, plant components)
| Source | Licence (verified) | Price |
|---|---|---|
| **TraceParts** | Data *"may only be used for the purposes of computer-aided design or viewing data"*; **no redistribution** as an external service, no copying/posting to a website, no distribution on any storage medium, no competitive use, without prior written consent; website "commercial utilization" prohibited. **GTU last updated 10 June 2026.** | Free |
| **GrabCAD Library** | **Private use by default.** Non-commercial public use requires creator attribution + link. **Commercial public use requires the original designer's explicit permission plus attribution of GrabCAD and the user; if the creator does not respond, commercial use is NOT permitted.** | Free |
| **3D ContentCentral (Dassault/SOLIDWORKS)** | Downloader use governed by the 3D ContentCentral Terms of Use; contributor terms grant Dassault a worldwide, irrevocable, royalty-free, sublicensable licence. | Free |
| **CADENAS PARTcommunity / 3Dfindit** | Per-locale terms; the English terms URL now 404s; Japanese terms page exists. **English terms UNVERIFIED.** | Free |
| **McMaster-Carr** | Provides CAD downloads; **explicit licence text not published / UNVERIFIED.** | Free |
| **3D Warehouse (Trimble/SketchUp)** | Official ToS FAQ exists but is JS-rendered; **exact commercial-use clause text UNVERIFIED.** Check per model. | Free |

### Paid marketplaces
| Source | Licence | Price |
|---|---|---|
| **TurboSquid** | **Royalty Free:** perpetual, worldwide, non-exclusive; commercial + client work permitted; **Editorial-marked models restricted to news/editorial use**; **no ML/AI training or AI-generated content without written authorisation**; corporate licences available. | Per asset; typical industrial **$10–$200 UNVERIFIED** |
| **CGTrader** | Royalty-Free (commercial, client work, no attribution) vs Editorial (no commercial use; minor edits only). | Per asset, **from $5** |
| **Sketchfab** | Free models under per-model CC licences (CC0/CC-BY commercial; CC-BY-NC not). Paid Store assets royalty-free from $5. Subscriptions: **Basic free; Pro $15/mo billed yearly; Premium $79/mo billed yearly; Enterprise custom.** | Per asset / plans above |
| **Fab (Epic)** | CC-BY or Standard (Personal/Professional), engine-agnostic. | Publisher-set |
| **KitBash3D** | **Full commercial licence included on all plans**; may modify/integrate into works; **cannot resell/redistribute standalone assets; cannot use in NEW projects after subscription ends; cannot train AI/ML; cannot claim ownership.** | **GSG Library $39/mo ($468/yr); KitBash3D Library $59/mo ($708/yr); Everything Bundle $79/mo (from $99) ($948/yr); Teams $99/user/mo, 4-seat minimum** |
| **Poliigon** | Subscription; **NOT CC0** (no redistribution). | **Free $0; Unlimited $27/mo; Business $59/mo** — these are **yearly-billing** rates; monthly rates UNVERIFIED |

### Brickwork & timber (PBR)
- **ambientCG — CC0**, free for any purpose including commercial, no attribution. ~1,000,000 monthly downloads; brick, construction, timber/rubble categories; new *Ground111* (brick/rubble ground) 12 Sep 2026.
- **Poly Haven — CC0**, 861 textures including brick/timber, no attribution.
- **Poliigon — subscription, not CC0.**
- **LotPixel Hub — 1,300+ free PBR texture sets** reported Jan 2026; **licence UNVERIFIED.**

### Scaffolding
**No dedicated CC0 or free scaffolding library was found.** Only per-asset purchases or marketplace packs: CGTrader (Industrial Pipe Kitbash Pack; Ultimate Industrial Pipeline & Connector Kit), TurboSquid, Sketchfab per-model, Superhive kitbash packs (Industrial Kitbash V1), Fab/KitBash3D industrial kits, and an Envato Elements construction/scaffolding kitbash pack (Envato pricing/licence UNVERIFIED). **Expect to buy per-asset or build a kitbash.**

### 19th-century machinery / historic industrial
- **Smithsonian Open Access — the strongest verified free source: 2,000+ 3D models under CC0**, downloadable as OBJ/glTF, commercial use without attribution; includes historic-machinery scans (Oliver Evans 1804 steam engine model; steam-engine piston patent models). (`si.edu` blocked automated access; CC0 status documented by CG Channel and Smithsonian's Open Access programme.)
- **TurboSquid** per-asset historic machinery (e.g. Porter-Allen steam engine, 1890) — royalty-free, editorially restricted where flagged; **price UNVERIFIED.**
- **Sketchfab** historic-machinery scans under per-model CC licences (some CC0/CC-BY, some NC) — check each.
- **Małopolska's Virtual Museum** (Polish museums) — 1,000–2,000+ free cultural-heritage 3D models including instruments and machinery; **exact licence tier (CC-BY vs CC0) UNVERIFIED.**
- **Plainly: there is no comprehensive, purpose-built "19th-century industrial machinery" library.** Practical 2026 answer: Smithsonian CC0 scans (free) plus per-asset purchases on TurboSquid/Sketchfab/CGTrader; GrabCAD is useful for *shape reference* only, because its default terms bar commercial use without the designer's permission.

### CAD-to-3D pipeline notes
- TraceParts / 3D ContentCentral / CADENAS supply native CAD (STEP, IGES, native) that can be decimated/retopologised for rendering — but TraceParts' GTU explicitly limits data to CAD/viewing use and bars redistribution.
- KitBash3D/Cargo integrates assets into Blender/UE/Maya/Houdini/3ds Max/C4D via USD/MaterialX with a commercial licence — the most production-ready paid option for industrial *kitbash* environments.

## E9. Cross-cutting 2026 ownership/status changes
- **Sketchfab and ArtStation were acquired by KitBash (KitBash3D/Greyscalegorilla) from Epic Games on 10 August 2026.** Sketchfab pricing and licensing are unchanged and enterprise agreements continue to be honoured.
- **BlenderKit → Blendkit** (blenderkit.com redirects to blendkit.com).
- **Blender Market → Superhive** (April 2025).
- **Quixel Bridge / Quixel.com** slated for retirement once Fab fully replaces Bridge.

Sources: https://gamesbeat.com/kitbash-acquires-artstation-and-sketchfab-art-platforms-from-epic-games/ · https://digitalproduction.com/2026/08/12/kitbash-buys-artstation-and-sketchfab/

## Section E — explicitly UNVERIFIED
Free-vs-paid Megascans split/counts; whether >$100k users need Professional for *free* Megascans; Superhive typical price bands and exact default commercial clause text; Superhive's True Terrain 5 price; TurboSquid typical industrial prices and the Porter-Allen 1890 listing price; Poliigon monthly-billing rates; 3D Warehouse, McMaster-Carr, CADENAS English, and 3D ContentCentral downloader terms; Małopolska licence tier; Envato Elements pricing/licence; LotPixel licence.

---

# CONSOLIDATED UNVERIFIED REGISTER
Do not quote any of these as fact:
1. ElevenLabs v4 pricing/tiers/availability.
2. Midjourney plan prices from a primary source.
3. CapCut exact prices; Adobe After Effects exact price from adobe.com.
4. Runway $/credit; Luma $/generation; BFL open-weights tier prices.
5. Cartesia embedded effective $/1M chars; Kling derived 720p per-clip credit cost; Gemini TTS derived $/minute.
6. **Within Section C (the rest is now verified):** GarageFarm and Fox per-GPU-hour equivalents (billed by OctaneBench-hour / node-hour without published node ratings or GPU models); RebusFarm USD per-GHz-hour (only JPY served) and its lack of a listed Blender 5.2 version; Blender 5.2 version support at GarageFarm and Fox (unstated); Lambda persistent-storage pricing; Paperspace on-demand A100-80G price, region, and RTX 4090/5090 availability; Vast.ai's dated vendor-comparison table (third-party); and the **render resolution of the Blender Benchmark scenes**, which is the one open assumption behind the C3 RTX 3080 per-frame estimate.
7. Megascans free-vs-paid split; >$100k Professional-tier question for free downloads.
8. Superhive price bands and default commercial clause; Superhive True Terrain 5 price.
9. TurboSquid industrial prices; Poliigon monthly rates; 3D Warehouse / McMaster-Carr / CADENAS English / 3D ContentCentral downloader terms; Małopolska licence tier; Envato Elements pricing; LotPixel licence.
10. Blender 5.0's exact Python minor version.
11. carlosh7/blender-mcp exact tool count (README self-contradicts: 239 vs 248).
