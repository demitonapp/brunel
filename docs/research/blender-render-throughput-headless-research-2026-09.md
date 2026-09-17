# Blender render throughput, EEVEE/Cycles, headless rendering, determinism, storage, and Mac M1 role

**Scope.** Solo 3D creator: Windows PC with an NVIDIA RTX 3080 (10 GB or 12 GB) + strong CPU, controlled from a Mac M1 16 GB. Target output: vertical 9:16 Instagram Reels (1080x1920), occasional 4K. Research date: September 2026.

**Method.** Primary sources: Blender 5.2 LTS manual and release notes, Blender developer docs, Blender Open Data (site JSON endpoint + the CC0 daily snapshot, mined programmatically), the official Blender Benchmark script source, Blender Stack Exchange API, Blender Artists (Discourse) API, Flamenco and CrowdRender sites, OpenEXR/OpenVDB docs.

**Tags.** `[V]` = verified, with URL. `[I]` = inference / arithmetic / judgement. `[NF]` = not found.

**Companion files in this workspace:** `blender-pipeline-research-2026-09.md`, `blender-storage-capacity-research.md`, `blender-m1-16gb-authoring-research-2026-09.md`.

> **Delivery note.** This report was produced by a delegated research subagent. The attempt to send it to the delegating agent via `send_message` failed with *"direct parent is not live; the message was not delivered"*, so it is persisted here as the durable record.

---

## 1. Blender Cycles benchmarks on RTX 3080

### 1.1 What the published score actually means

`[V]` Official definition — https://opendata.blender.org/about/ :

> "The Blender benchmark Score is a measure of how quickly Cycles can render path tracing samples on one CPU or GPU device. The higher the number, the better. In particular it's the estimated number of samples per minute, summed for all benchmark scenes."

`[V]` It is a **throughput** measure, not a frame time. The benchmark script sets:

```python
scene.cycles.use_adaptive_sampling = False
scene.cycles.samples = 1 << 24      # maximum supported value
scene.cycles.time_limit = 30        # render flat out for 30 seconds
scene.cycles.use_auto_tile = False
```

Source: `render.py` in https://opendata.blender.org/cdn/BlenderBenchmark2.0/script/blender-benchmark-script-3.1.1.tar.gz — "We are measuring average time per sample, which is not compatible with adaptive sampling."

### 1.2 RTX 3080 measured scores

`[V]` `NVIDIA GeForce RTX 3080`, **OPTIX**, median score by Blender version (samples/minute summed across monster + junkshop + classroom), pulled live from
`https://opendata.blender.org/benchmarks/query/?device_name=GeForce+RTX+3080&compute_type=OPTIX&group_by=blender_version&response_type=datatables`

| Blender version | Median score (samples/min) | n |
|---|---|---|
| 5.2.0 | 4208.40 | 91 |
| 5.1.1 | 4467.51 | 236 |
| 5.1.0 | 4483.01 | 96 |
| 5.0.0 | 4060.23 | 40 |
| 4.5.0 | 4575.24 | 869 |
| 4.4.0 | 4510.16 | 639 |
| 4.2.0 | 4532.61 | 709 |
| 4.0.0 | 4642.92 | 829 |
| 3.6.0 | 5314.22 | 889 |

`[V]` Full device page (all versions): median 4792, n=6887 — https://opendata.blender.org/devices/NVIDIA%20GeForce%20RTX%203080/

`[NF]` **Per-scene** monster/junkshop/classroom sample rates are not obtainable. The query UI groups only by `compute_type` / `device_name` / `operating_system` / `blender_version`, and the CC0 snapshot stores `device_peak_memory` and `render_time_no_sync` but **no sample counts**. Settle it by running the benchmark locally.

### 1.3 Peak VRAM per benchmark scene

`[V]` Mined from the CC0 snapshot (`https://opendata.blender.org/snapshots/opendata-latest.zip`, 1.87 GB JSONL): RTX 3080 + OptiX + Windows + Blender 5.2.0, n=35 per scene.

| Scene | Median peak VRAM | Max peak VRAM |
|---|---|---|
| monster | 1190 MB | 1209 MB |
| junkshop | 4716 MB | 4734 MB |
| classroom | 1264 MB | 1283 MB |

The entire 3-scene benchmark fits under ~4.8 GB — well inside a 10 GB card.

### 1.4 OptiX status on the RTX 3080 in Blender 5.x

`[V]` Fully supported, not deprecated — https://docs.blender.org/manual/en/5.2/render/cycles/gpu_rendering.html :

> "OptiX is supported on Windows and Linux and requires a NVIDIA graphics cards with compute capability 5.0 and higher and a driver version of at least 575."

RTX 3080 = Ampere, compute capability 8.6. The same page confirms:

> "GPU acceleration for OpenImageDenoise is available for compute capability 7.0 and higher, which includes all NVIDIA RTX cards."

So OptiX rendering **and** GPU OpenImageDenoise are both available on the 3080 in Blender 5.2.

### 1.5 10 GB vs 12 GB — what actually breaks

`[V]` Official out-of-memory behaviour — same manual page:

> "With CUDA, OptiX, HIP and Metal devices, if the GPU memory is full Blender will automatically try to use system memory. This has a performance impact, but will usually still result in a faster render than using CPU rendering."

It does **not** crash, and it does **not** silently fall back to CPU.

`[NF]` **No measured slowdown factor for Cycles out-of-core exists** in Puget Systems, CGDirector, Techgage, Blender Artists or Blender Stack Exchange. The manual gives only the qualitative statement above. What would settle it: render the same scene just under and just over 10 GB VRAM and time both with `--cycles-print-stats`.

`[V]` VRAM-reduction levers documented in https://docs.blender.org/manual/en/5.2/render/cycles/render_settings/performance.html :

- **Tile Size** — default 2048. "When running out of memory, lowering to 1024 or 512 pixels helps reduce memory usage, typically at a small performance cost."
- **Texture Cache** — `.tx` files. "Reduce memory usage and startup time on scenes with many image textures, at the cost of a small rendering performance impact and increased disk space usage."
- **Use Compact BVH**, **Use Curves BVH** (off), **BVH Time Steps**.
- Note: "The Acceleration Structure panel will not be present when using an Optix compute device."

`[I]` The 12 GB variant (launched 11 January 2022; 8960 CUDA cores and a 384-bit bus vs the 10 GB's 8704 / 320-bit — https://www.techpowerup.com/290790/nvidia-launches-geforce-rtx-3080-12gb-graphics-card ) buys **headroom, not speed**. Cycles throughput is essentially identical between the two; only the OOM threshold moves. For a 1080x1920 diffuse-heavy engineering scene the 10 GB is not a practical constraint.

### 1.6 Translating to render time per frame

`[I]` **Derived, not measured.** Treat as a planning band.

The benchmark scenes render at 1920x1080. I confirmed an aligned 1920/1080 integer pair inside the render-data region of the official `monster` `.blend` (from https://opendata.blender.org/cdn/BlenderBenchmark2.0/scenes/ ), but Blender does not document the resolution — **high confidence, not officially verified**.

Critical point: **1080x1920 = 2,073,600 px = the same pixel count as 1920x1080**, so samples/minute transfers on pixel count to first order.

At Blender 5.2's 4208 samples/min summed over 3 scenes:

- ~1403 samples/min per scene average → ~23.4 samples/second
- 64 samples ≈ 2.7 s | 128 samples ≈ 5.5 s | 256 samples ≈ 11.0 s — for a scene of *benchmark-average* cost
- For a scene 2–4× heavier (dense brick geometry, more indirect bounces): 64 ≈ 5–11 s, 128 ≈ 11–22 s, 256 ≈ 22–45 s
- Add ~0.5–2 s/frame for OptiX/OIDN denoise `[I]`

**Planning band for the stated scene** (1080x1920, historical-engineering, lots of brick/geometry, few lights, mostly diffuse, OptiX + denoise):

| Samples | Time per frame | Frames per hour |
|---|---|---|
| 64 | ~5–15 s | ~240–720 |
| 128 | ~15–40 s | ~90–240 |
| 256 | ~30–80 s | ~45–120 |

Caveats that push toward the fast end: diffuse-only with few lights is Cycles' cheapest case; adaptive sampling with a 0.01 noise threshold usually lands well below the max sample count. Denoising means 128–256 is normally unnecessary at Reels resolution — **64–128 with OIDN is the sweet spot**.

---

## 2. EEVEE (Next) vs Cycles in Blender 5.x

### 2.1 Version and identity

`[V]` The rewritten EEVEE shipped in **Blender 4.2 LTS**, which removed legacy EEVEE — https://developer.blender.org/docs/release_notes/4.2/eevee/ . There is **no "EEVEE 2.0" version number**; Blender 5.2 LTS (released 14 July 2026, supported to July 2028 — https://www.blender.org/press/blender-5-2-lts-release/ ) simply calls it EEVEE.

`[V]` Python engine identifier in the current API is `'BLENDER_EEVEE'` — **not** `'BLENDER_EEVEE_NEXT'`. Default value of `scene.render.engine` per https://docs.blender.org/api/current/bpy.types.RenderSettings.html .

### 2.2 What 5.2 changed in EEVEE

`[V]` https://developer.blender.org/docs/release_notes/5.2/eevee/ :

- Screen Space Raytracing overhaul — new **Backface** option; "Due to fixes in energy conservation, some scenes might render darker than in 5.1."
- Fast GI / Ambient Occlusion fixes — "This changes the look of existing files using this option."
- Reflection denoiser preserves contact sharpness better.
- **Instancing performance:** "EEVEE now supports the same instancing optimizations as Workbench and Overlay. Instancing-heavy scenes (CPU bottlenecked) can be up to twice as fast." Directly relevant to repeated brick/timber/structural geometry.
- New 1.5 GB and 2 GB shadow pool size options.
- EEVEE Lights now support camera ray visibility.
- "EEVEE now uses slightly less video memory during rendering."

### 2.3 Current limitations

`[V]` From https://docs.blender.org/manual/en/5.2/render/eevee/limitations/limitations.html — the ones that matter here:

**Refraction / water / glass**
> "Only one refraction event is correctly modeled. An approximation of the second refraction event can be achieved using the Thickness workflow."
> "Blended materials are not compatible with raytracing."
> "Only dithered materials not using Raytrace Refractions can be refracted."

**Volumetrics**
> "Only single scattering is supported."
> "Volumetrics are rendered only for the camera 'rays'. They don't appear in reflections/refractions and probes."
> "Volumetric shadowing only work in volumetrics. They won't cast shadows onto solid objects in the scene."
> "Volumetric shadowing only works for volumes inside the view frustum."

**Screen-space effects**
> "Ray-triangle intersection is not currently supported. Instead of this, EEVEE uses the depth buffer as an approximated scene representation."
Effects disappear at the screen border (partly mitigated by overscan), lack thickness information, ignore occluded objects, and exclude blended surfaces.

**Shadows**
Shadow Map Raytracing can leak light with overlapping casters; thin (zero-thickness) walls can leak on the shadowed side. Mitigations: lower step count, enable jitter, reduce light shape size, lower Resolution Limit.

**Lights**
One colour per light, no light node trees. Spot light `Size` does not change cone softness. ≤128 active light probe spheres, ≤16 planes inside the view frustum. "Light probe capture does not support specular reflections. Specular energy is treated as diffuse."

**Materials**
"Only 14 attributes from Geometry Nodes are supported in a material."

**Precision**
> "EEVEE generally performs all calculations using half-precision (16-bit) floating point numbers… The render output subsequently also only has the precision of half-precision (16-bit) floating point numbers."

**Other**
No multi-GPU support. GPU memory is managed by the driver — "using too much GPU memory can make the GPU driver crash, freeze, or kill the application." And: **"Headless rendering is not supported on headless Windows systems."** (see §3).

### 2.4 Reported EEVEE speed

`[V]` Real measured comparison — Blender Artists, 2024-07-26, Blender 4.2.0, 1920x1080, same scene, three shots. Cycles: 512 samples, 0.01 noise threshold, 8 bounces, GPU OpenImageDenoise → **1:26 / 1:14 / 1:22**. EEVEE: 128 samples, shadows + raytracing on default settings → **0:06 / 0:06 / 0:06**. The poster judged the difference to be mainly colour balance plus slight transparent-material defects. https://blenderartists.org/t/1540799

`[I]` Applying that ~12–14× ratio to the Cycles numbers in §1.6 puts EEVEE at roughly **0.3–1.5 s/frame** at 1080x1920 → thousands of frames/hour. The binding constraint becomes shader-compile stalls, not per-frame render time.

### 2.5 EEVEE volumetrics remain a real problem in 5.x

`[V]` Blender Artists, 2026-07-01, Blender 5.1.1, RTX 5070:

> "I can't figure out how to reduce this unique yet ugly noise pattern that Volume Scattering has in EEVEE… I try raising samples up to 64 but it still persists and that it adds too much more time."

Workarounds offered in-thread: use an object-based volume rather than the world volume ("When you use volume scatter in world shader you are putting a heavy load on your PC"), or render the volume as a separate pass and blur it in post. https://blenderartists.org/t/1646681

### 2.6 Verdict for this use case

`[I]` "80% of the look at 5% of the time" is **defensible for brick, iron and timber** — hard-surface, opaque, diffuse/glossy. That is exactly what EEVEE's rasteriser plus screen-space GI handles well, and 5.2's instancing optimisation is a direct win for repeated brick and timber elements.

It is **not** defensible for **water or glass** (one refraction event; no blended-material raytracing) or for **volumetric fog and smoke** (single scattering, camera rays only, persistent visible noise).

**Recommended split:** EEVEE for all brick/iron/timber shots; Cycles for anything with water, glass or volumetrics. Also budget for the 16-bit output precision if you plan heavy grading.

---

## 3. Headless rendering

**Official pages (both Blender 5.2 LTS):**
- https://docs.blender.org/manual/en/5.2/advanced/command_line/render.html
- https://docs.blender.org/manual/en/5.2/advanced/command_line/arguments.html

### 3.1 Core invocations

`[V]` Verbatim from the manual:

```bash
blender -b file.blend -f 10
blender -b file.blend -o /project/renders/frame_##### -F OPEN_EXR -f -2
blender -b file.blend -a
blender -b file.blend -E CYCLES -s 10 -e 500 -t 2 -a
```

- `-b` — "Run in background (often used for UI-less rendering)." The audio device is disabled in background mode.
- `-f -2` — second-to-last frame. `+<frame>` / `-<frame>` are relative.
- `-o` — supports `//` (blend-relative), `#` for zero-padded frame numbers, and `{blend_name}` path templating. "When the filename does not contain `#`, the suffix `####` is added."
- `-a` — "Render frames from start to end (inclusive)."
- `-s` / `-e` — start / end frame, both accepting `+` / `-` relative values.
- `-t` — thread count, 1–1024, 0 = system processor count.
- `-E help` lists available engines.

### 3.2 Ordering rules — the most common failure

`[V]` "Arguments are executed in the order they are given!"

```bash
# WRONG - output and extension are set after Blender is told to render
blender -b file.blend -a -x 1 -o //render

# RIGHT
blender -b file.blend -x 1 -o //render -a
```

> "Always position `-f` or `-a` as the last arguments."
> "Arguments are case sensitive! `-F` and `-f` are not the same."

Also documented: `blender --background test.blend --render-frame 1 --render-output /tmp` will not render to `/tmp`, and `blender --background --render-output /tmp test.blend --render-frame 1` will not either, "because loading the blend-file overwrites the render output that was set."

### 3.3 New and useful in 5.2

`[V]`

- `-f` accepts a **comma-separated list** (no spaces) and a `..` range, e.g. `-f 1,5,10..20`.
- `-j`, `--frame-jump <frames>` — "Set number of frames to step forward after each rendered frame."
- `-S`, `--scene <name>` — set the active scene for rendering.
- `--disable-depsgraph-on-file-load` — background mode: skip building/evaluating view-layer depsgraphs on file load. "Scripts requiring evaluated data then need to explicitly ensure that an evaluated depsgraph is available (e.g. by calling `depsgraph = context.evaluated_depsgraph_get()`)." Flagged as temporary.
- `--gpu-backend vulkan|metal|opengl`, `--gpu-vsync`, `--profile-gpu`.

### 3.4 Cycles options and the `--` separator

`[V]` "Cycles add-on options must be specified following a double dash."

```bash
blender -b file.blend -f 20 -- --cycles-device OPTIX
```

Valid options: `CPU CUDA OPTIX HIP ONEAPI METAL`. Append `+CPU` to a GPU device to render on both, e.g. `--cycles-device OPTIX+CPU`. Also `--cycles-print-stats` — "Log statistics about render memory and time usage."

### 3.5 Python: `--python-expr`, `-P`, and passing arguments after `--`

`[V]`

| Flag | Meaning |
|---|---|
| `-P`, `--python <filepath>` | Run the given Python script file. |
| `--python-text <name>` | Run the given Python script text block. |
| `--python-expr "<expression>"` | "Run the given expression as a Python script. The expression may be a complete multi-line script; you are limited only by the platform's maximum argument length." |
| `--python-console` | Interactive console. |
| `--python-exit-code <0..255>` | "Set the exit-code in [0..255] to exit if a Python exception is raised (only for scripts executed from the command line), zero disables." |
| `--python-use-system-env` | Allow `PYTHONPATH` and user site-packages. |
| `-y`, `--enable-autoexec` | Enable automatic Python script execution. Note `-Y`/`--disable-autoexec` is the **default**. |
| `--addons <a,b>` | Comma-separated, no spaces. |

`[V]` **Passing arguments to a script** — `--` :

> "End option processing, following arguments passed unchanged. Access via Python's `sys.argv`."

Canonical pattern (this is literally what the official Blender Benchmark script does — `main.py` in the benchmark script tarball):

```python
import sys
argv = sys.argv[sys.argv.index('--') + 1:]
# then argparse-parsable:
parsed = parser.parse_args(argv)
```

Full example:

```bash
blender -b scene.blend -P render.py -o //out_ -F PNG -- --engine cycles --samples 128 --device OPTIX
```

### 3.6 Setting engine, samples and device from a script

`[V]` Pattern taken from the official benchmark script's `render.py`:

```python
import bpy

scene = bpy.context.scene
scene.render.engine = 'CYCLES'                 # or 'BLENDER_EEVEE'
scene.cycles.device = 'GPU'
scene.cycles.samples = 128
scene.cycles.use_adaptive_sampling = True
scene.cycles.use_denoising = True
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.image_settings.file_format = 'PNG'

prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'OPTIX'            # must be set BEFORE per-device flags
for d in prefs.devices:
    d.use = (d.type == 'OPTIX')
```

The usual failure mode is setting per-device `use` flags before selecting `compute_device_type` — the device list is rebuilt when the backend changes.

### 3.7 `bpy.ops.render.render` and `bpy.ops.wm.save_as_mainfile` in background mode

`[V]` `https://docs.blender.org/api/current/bpy.ops.render.html`

```
bpy.ops.render.render(*, animation=False, write_still=False, use_viewport=False,
                      use_sequencer_scene=False, layer='', scene='',
                      frame_start=0, frame_end=0)
```

- `animation=True` renders the scene's animation range.
- `frame_start` / `frame_end` — "Frame to start rendering animation at. If not specified, the scene start frame will be assumed. **This should only be specified if doing an animation render.**" So a background script **can** override the range without editing the `.blend`.
- `write_still=True` saves a single image — "(used only when animation is disabled)".
- `scene=''` selects which scene to render.

`[V]` `https://docs.blender.org/api/current/bpy.ops.wm.html`

```
bpy.ops.wm.save_as_mainfile(*, filepath='', ..., compress=False,
                            relative_remap=True, copy=False,
                            show_save_modified_images_dialog=False)
```

- `copy=True` writes the file **without** making it the current session file — use this in headless scripts so you do not rebind the running session.
- `compress=True` gzips the `.blend`.
- In background mode there is no UI, so no exit prompt: the operator writes and returns.

`[V]` **Save before rendering if you rely on a rigid-body cache.** The manual (https://docs.blender.org/manual/en/5.2/physics/rigid_body/world.html): "If you have not saved the blend-file, the cache is created in memory, so save your file first or the cache may be lost."

### 3.8 Can Blender run headless with no GPU / no display?

`[V]` **Cycles: yes, unconditionally.** The manual's stated rationale for the command line is:

> "One advantage of using the command line is that we do not need a graphical display (no need for X server on Linux for example) and consequently we can render via a remote shell (typically SSH)."

Cycles CPU needs no GPU at all.

`[V]` **EEVEE:** the 5.2 limitations page states **"Headless rendering is not supported on headless Windows systems."** The same page: EEVEE "only uses the power of the GPU to render. There is no plan to support CPU (software) rendering as it would be very inefficient. CPU power is still needed to handle high scene complexity as the geometry must be prepared by the CPU before rendering each frame."

`[V]` On **Linux**, EEVEE headless *does* work when the driver exposes EGL. A real user rendered EEVEE headless on an Ubuntu VM with an NVIDIA A100 — "I am able to run everything headless on my VM (no docker). I can render with EEVEE and it renders REALLY fast." Inside Docker it failed with `ERROR (gpu.shader): eevee_shadow_tag_usage_transparent Linking: Too many vertex shader storage blocks (9/8)` until they enabled the `graphics` capability: "When using docker not all nvidia capabilities are enabled by default. If you want to use eevee inside docker you need to enable also the graphics capability. By default cuda is enabled and thats why cycles works out of the box." https://blenderartists.org/t/1551491

`[I]` **Practical implication:** keep EEVEE renders on the interactive Windows desktop session (or accept the risk), and do all headless/farm work with Cycles.

### 3.9 Distributed / network rendering

`[V]` **Blender's built-in Network Render add-on was removed in the 2.8x line and never replaced.** Contemporaneous confirmation, Blender Artists, April–May 2020 — https://blenderartists.org/t/1224660 :

> "Has all native (built in) network render support been removed from Blender 2.8?"
> "Looks like nobody does network rendering anymore… Yes, it has in fact been removed, been promised back, but that message is very old now, it might be a long time till we see the feature back (likely a low priority)."

There is **no current official Blender network-render feature**.

`[V]` **Flamenco** — https://flamenco.blender.org/ — is the official, Blender-Foundation-developed answer and "is used in production at Blender Studio." GPL 3.0. Core built in Go + SQLite. Self-hostable, Windows/Linux/macOS (including macOS ARM).

- **Current release: 3.9.3 stable. 3.10-beta1 experimental.** https://flamenco.blender.org/download/
- Architecture per the quickstart: one machine runs **Flamenco Manager**, one or more run **Flamenco Worker**, each worker needs Blender installed "in the same place everywhere", and:
  > "A local network with file sharing already set up, so that the above computers can all reach the same set of files."
  > "Create a directory on some storage, like a NAS, and make sure it's available at the same path on each computer."
- The Blender add-on is downloaded from the Manager's web UI after setup. Jobs are submitted from Blender's Output Properties panel. https://flamenco.blender.org/usage/quickstart/

`[V]` **CrowdRender** — note the hyphen: **crowd-render.com** (the un-hyphenated `crowdrender.com` is NXDOMAIN). It is an add-on rather than a manager/worker pair, and it is still alive. **Important compatibility limit as of September 2026** — https://www.crowd-render.com/ :

> "As of right now, support for versions of Blender 3.0 to 5.1 is available for supporters of our development fund. There is a free version for evaluation which has support up to Blender 4.3."

So the paid tier does **not** yet list Blender 5.2, and the free tier caps at 4.3.

`[I]` **For a two-machine setup (Mac + Windows PC), neither tool is a clean win.** Flamenco is designed around shared storage at identical paths and a manager/worker topology — real setup cost for two nodes. CrowdRender's version gap blocks current Blender. The pragmatic 2026 approach is manual range splitting, run as two independent background Blender processes writing to the same shared folder:

```bash
# Machine A
blender -b scene.blend -o //renders/frame_##### -F PNG -s 1 -e 125 -a
# Machine B
blender -b scene.blend -o //renders/frame_##### -F PNG -s 126 -e 250 -a
```

`--frame-jump` does **not** distribute work by itself — it only steps frames within one process. It is useful for quick low-density previews (`-j 10 -a`), not for parallelism.

---

## 4. Determinism and scripted simulation

`[V]` **Bottom line: nothing in Blender's physics is contractually deterministic except a completed bake.** The manual's only reproducibility claim is attached to baking — https://docs.blender.org/manual/en/5.2/physics/baking.html :

> "It is generally recommended to bake your physics simulations before rendering. Aside from no longer needing to go through the time-consuming process of simulating again, baking can help prevent potential glitches and ensure that the outcome of the simulation remains exactly the same every time."

### 4.1 Rigid body has no random seed

`[V]` Read from source:

- `RB_dworld_new()` builds a plain `btSequentialImpulseConstraintSolver`; only `RB_dworld_set_solver_iterations()` and `RB_dworld_set_split_impulse()` touch solver info. No `setRandSeed`, no `m_solverMode` change. https://projects.blender.org/blender/blender/raw/branch/main/intern/rigidbody/rb_bullet_api.cpp
- Bullet's constructor sets `m_btSeed2 = 0`, and the only consumer of that LCG is gated on `SOLVER_RANDMIZE_ORDER` inside `solveSingleIteration()` — which Blender never sets. https://projects.blender.org/blender/blender/raw/branch/main/extern/bullet2/src/BulletDynamics/ConstraintSolver/btSequentialImpulseConstraintSolver.cpp
- `rigidbody.cc` contains no `rand`/`srand`/`seed`/clock call anywhere. https://projects.blender.org/blender/blender/raw/branch/main/source/blender/blenkernel/intern/rigidbody.cc

`[V]` The widely repeated "**the random seed is generated per session**" explanation — asserted by a Blender Artists moderator at https://blenderartists.org/t/rigid-body-simulations-change-between-sessions/1548362 — is **not supported by the source**.

`[V]` The underlying drift is real and reported:

> "my simulation results change between Blender sessions… When I open it again and start my simulation via the timeline, I get a different result than before with completely different coordinates. I have already set the substeps per frame and the solver iterations … to 30 to avoid errors."

`[I, medium]` The actual mechanism is step-history and ordering: warm-starting is enabled, the sim only advances one frame at a time (`can_simulate = (ctime == rbw->ltime + 1)`), the body/constraint collection cache is rebuilt from runtime data per session, and any change in contact-manifold order changes the warm-start impulses — enough to diverge a chaotic stack. Note the user's own observation that the result is stable *within* a session fits this explanation.

`[V]` A second corroborating community answer (Blender SE 278943, answer by Nathan):

> "Blender's physics are not deterministic. Or, perhaps more carefully, they depend upon variables that, intuitively, they shouldn't depend upon… If we want them to behave the same way whenever we scrub through the timeline, we need to bake the physics."

(The clock-seed part of that answer is unverified; no clock-seeded RNG exists in the rigid-body path.)

### 4.2 Cloth — the multithreading bug was fixed

`[V]` Developer commit, Luca Rood, 19 September 2018:

> "Multithreading makes collisions be detected in different orders, causing the clustering step of collision resolution to generate possibly slightly different results on each run. This commit makes collision order consistent."

https://archive.blender.org/lists/bf-blender-cvs/2018-September/114364.html — and the fix is present in current `main`: `collision.cc` uses `COLLISION_INACTIVE` with a stable index swap and the comment "Collision math is currently not symmetric, so ensure a stable order for each pair." https://projects.blender.org/blender/blender/raw/branch/main/source/blender/blenkernel/intern/collision.cc

### 4.3 Mantaflow — no seed, no statement

`[V]` No developer statement either way was found, and **the domain exposes no seed**. Grepping the full `rna_fluid.cc` for "seed" returns nothing, and `FluidDomainSettings` has no seed member. The "Randomness"-sounding fields are magnitudes, not seeds — Flow → `particle_randomness`: "Higher values will sample the liquid particles more randomly in inflow regions. With a value of 0.0 all new particles will be sampled uniformly." https://docs.blender.org/manual/en/5.2/physics/fluid/type/domain/settings.html

### 4.4 Is there a fixed random seed anywhere?

`[V]` **No.** There is no random seed for rigid body, cloth, or the Mantaflow domain, and **no "Random Seed" field on a Blender fluid domain**. There is nothing to set to a fixed value. Reproducibility must come from baking, or from pinning build + platform.

### 4.5 Substeps and "Steps per Second" — accuracy, not determinism

`[V]` Note on wording: the rigid-body panel no longer has a field named "Steps per Second". Blender 5.2 labels it **"Substeps Per Frame"** — https://docs.blender.org/manual/en/5.2/physics/rigid_body/world.html :

> "**Substeps Per Frame** — Number of simulation steps taken per frame (higher values are more accurate but slower). This only influences the accuracy and not the speed of the simulation."
> "**Solver Iterations** — Amount of constraint solver iterations made per simulation step (higher values are more accurate but slower). Increasing this makes constraints and object stacking more stable."
> "**Split Impulse** — Enable/disable reducing extra velocity that can build up when objects collide (lowers the simulation stability a little so use only when necessary)… makes the simulation less stable (especially when stacking many objects)."

Source mapping confirms: `const float substep = timestep / rbw->substeps_per_frame;` looping `RB_dworld_step_simulation(world, substep, 0, substep)`.

`[V]` **Cloth has no "Substeps" and no "Solver" field.** Its equivalents — https://docs.blender.org/manual/en/5.2/physics/cloth/settings/index.html and `.../collisions.html`:

> "**Quality Steps** — Set the number of simulation steps per frame. Higher values result in better quality, but will be slower."
> "**Collision Quality** — How many collision iterations should be done (higher is better quality but slower)."
> "**Impulse Clamping** — Clamp collision impulses to avoid instability."

(The Soft Body "Solver" Edge/Goal dropdown is a different system.)

`[I]` These are **accuracy/stability controls, not determinism controls** — but they change the numeric answer (different step size and iteration count), so they change *which* reproducible value you get. Higher values make a simulation more **robustly reproducible** by moving it away from knife-edge divergence. They do not make it deterministic by decree.

### 4.6 Cross-machine determinism

`[V]` **Not safe to assume, and there is a hard reason.** Bullet selects its constraint kernel at runtime based on CPU features:

```cpp
if ((cpuFeatures & CPU_FEATURE_FMA3) && (cpuFeatures & CPU_FEATURE_SSE4_1)) {
  m_resolveSingleConstraintRowGeneric = gResolveSingleConstraintRowGeneric_sse4_1_fma3;
  ...
}
```

That kernel uses fused multiply-add (`_mm_fmadd_ps`), which rounds differently from the scalar/SSE2 path. Same Blender binary, different CPU, different trajectory. https://projects.blender.org/blender/blender/raw/branch/main/extern/bullet2/src/BulletDynamics/ConstraintSolver/btSequentialImpulseConstraintSolver.cpp

`[V]` Blender already documents cross-platform floating-point non-determinism elsewhere — issue #163764 (Blender 5.2.1 LTS): "Geometry Nodes: Matrix SVD result is non-deterministic across platforms… a different `U` result computed from the `Matrix SVD` node between Linux and Mac/Windows platforms." Also #158971: "`Points to Curves` is non-deterministic above 1024 points" (thread-order dependent above a parallelisation threshold).

`[NF]` **No measured cross-machine or cross-version physics comparison exists publicly.** Settle it with a scripted A/B harness: export evaluated transforms per frame and compare across 1 vs 32 threads, Intel/AMD/Apple Silicon, Windows/Linux/macOS, and 3.6 vs 4.x vs 5.2.

### 4.7 Baked caches and what invalidates them

`[V]` The manual is explicit:

> "If you bake the simulation the cache is protected, and you will be unable to change the simulation settings until you clear the baked frames by clicking Delete Bake."

> "The system is protected against changes after baking. If for example the mesh changes the simulation is not calculated anew."

> "The cache is cleared automatically on changes. But not on all changes, so it may be necessary to delete it manually, e.g. if you change a force field."

Cloth (https://docs.blender.org/manual/en/5.2/physics/cloth/settings/cache.html):
> "You cannot change Start or End without clearing the bake simulation."
> "If you move or edit the cloth object after you have already run the simulations, you must clear the cache…"
> "A bake/cache is done for every subdivision level so please use the equal subdivision level for render and preview."

Fluid cache format is versioned: `#define FLUID_CACHE_VERSION "C01"`.

Point caches (rigid body / cloth / particles) write `.bphys` files named `name_frame_index.bphys` into `blendcache_[filename]/` beside the `.blend`.

`[V]` ⚠ **High-value trap: the default fluid cache directory name is per-session.** Commit `0f1f75178571d9e2644f3b4dd697a5c876bf3ea2` (Jacques Lucke, 10 March 2020), "Fix T74525: Fluid caches overwrite each other by default", added:

```c
void BKE_fluid_cache_new_name_for_current_session(int maxlen, char *r_name)
{
  static int counter = 1;
  BLI_snprintf(r_name, maxlen, FLUID_DOMAIN_DIR_DEFAULT "_%x", BLI_hash_int(counter));
  counter++;
}
```

The function still exists in current `main` (https://projects.blender.org/blender/blender/raw/branch/main/source/blender/blenkernel/BKE_fluid.h ), and `physics_fluid.c` resets a missing cache directory to a fresh session name and reports an error.

**Consequence:** if Cache Directory is left empty/unset — or the folder goes missing — **each Blender session gets a different `cache_fluid_<hash>` folder, the previous bake is not found, and the simulation silently re-runs.**

`[V]` **"Bake once, reuse" is the documented recommendation.** The modern equivalent for point caches: "**External** — Allows you to read the cache from a drive using a user-specified file path… The cache files name format is `name_frame_index.bphys`" and "**Use Library Path** — Share the disk cache when the physics object is linked into another blend-file."

### 4.8 Cache formats and on-disk layout

`[V]` Formats defined in `DNA_fluid_types.h`:

```
FLUID_DOMAIN_EXTENSION_UNI    ".uni"
FLUID_DOMAIN_EXTENSION_OPENVDB ".vdb"
FLUID_DOMAIN_EXTENSION_RAW    ".raw"
FLUID_DOMAIN_EXTENSION_OBJ    ".obj"
FLUID_DOMAIN_EXTENSION_BINOBJ ".bobj.gz"
```

Manual (https://docs.blender.org/manual/en/5.2/physics/fluid/type/domain/cache.html):

> "**Uni Cache:** Blender's own caching format with some compression. Each simulation object is stored in its own `.uni` cache file."
> "**OpenVDB:** Advanced and efficient storage format. All simulation objects (i.e. grids and particles) are stored in a single `.vdb` file per frame."

**OpenVDB is the default** for data, noise and particles; meshes default to binary object (`.bobj.gz`).

`[V]` Directory constants:

```
FLUID_DOMAIN_DIR_DEFAULT   "cache_fluid"   FLUID_DOMAIN_DIR_CONFIG    "config"
FLUID_DOMAIN_DIR_DATA      "data"          FLUID_DOMAIN_DIR_NOISE     "noise"
FLUID_DOMAIN_DIR_MESH      "mesh"          FLUID_DOMAIN_DIR_PARTICLES "particles"
FLUID_DOMAIN_DIR_GUIDE     "guiding"       FLUID_DOMAIN_DIR_SCRIPT    "script"
FLUID_NAME_CONFIG "config"  FLUID_NAME_DATA "fluid_data"  FLUID_NAME_NOISE "fluid_noise"
FLUID_NAME_MESH "fluid_mesh"  FLUID_NAME_PARTICLES "fluid_particles"
```

`BKE_fluid_cache_free()` deletes exactly these subdirectories on invalidation. https://projects.blender.org/blender/blender/raw/branch/main/source/blender/blenkernel/intern/fluid.cc

`[I]` Illustrative layout (directories and file prefixes are verified; the `%04d` numbering and per-format suffix are inferred from the manual's "single .vdb per frame" statement):

```
<Cache Directory>/
  config/     config…                       (cache metadata / .uni)
  data/       fluid_data_0001.vdb …         (grids)
  noise/      fluid_noise_0001.vdb …        (gas high-res noise)
  mesh/       fluid_mesh_0001.bobj.gz …     (liquid only; or .obj)
  particles/  fluid_particles_0001.vdb …    (FLIP / spray / foam / bubble / tracer)
  guiding/    fluid_guiding_0001.vdb …      (velocity guiding)
  script/     smoke_script.py | liquid_script.py   (only with "Export Mantaflow Script")
```

A smoke cache is the same layout restricted to `config/ data/ noise/ guiding/`. A user reading a real fire cache reports `fire-cache/data` plus a `config` item (https://blender.stackexchange.com/questions/277778 ).

### 4.9 Rendering a baked cache without re-simulating

`[V]` **Yes.** The manual: "The Cache panel is used to Bake the fluid simulation and stores the outcome of a simulation so it does not need to be recalculated."

Cache Type semantics, verbatim:

> "**Replay:** The cache will be baked as the simulation is being played in the viewport."
> "**Modular:** The cache will be baked step by step: The bake operators for this type are spread across various panels within the domain settings."
> "**All:** The cache will be baked with a single tool. All selected settings will be considered during this bake."

> "'Replay' only works when the Playback Sync mode is set to 'Play Every Frame'."
> "It is not possible to pause or resume a Bake All process as only the most essential cache files are stored on drive."
> "**Resumable** — Extra data will be saved so that you can resume baking after pausing."

`[I]` For a farm/render-only pipeline use **All** (or Modular + Bake Data/Mesh) with an explicit stable Cache Directory. **Never rely on Replay** for anything that must reproduce.

`[V]` A baked cache can also be consumed with no domain at all via `Add > Volume > Import Open VDB` on the `data/*.vdb` files — the standard "loop a fire" workflow.

`[V]` **Blockers to "bake once, render later":** the session-named default Cache Directory when unset; cache-version mismatch; a moved or deleted cache folder (path reset and silent re-simulation); using Replay; and changing Start/End.

---

## 5. Storage and disk

### 5.1 Rendered frame sizes

`[V]` Format facts: OpenEXR HALF = 16 bits = 2 bytes per channel per pixel. OpenEXR technical introduction: "photographic images with significant amounts of film grain tend to shrink to somewhere between 35 and 55 percent of their uncompressed size." https://openexr.com/en/latest/TechnicalIntroduction.html

`[V]` Blender codecs: ZIP/ZIPS (zlib on 16-row blocks), PIZ (lossless wavelet, "effective for noisy/grainy images"), DWAA/DWAB, and B44 which is a fixed 2.3:1 ratio. https://docs.blender.org/manual/en/latest/files/media/image_formats.html

`[I]` Arithmetic — 1080x1920 = 2,073,600 px; 4K = 8,294,400 px (exactly 4x):

| Output | Uncompressed | Realistic on disk |
|---|---|---|
| 1080x1920 PNG 8-bit RGBA | 8.29 MB | **3–8 MB** `[I, LOW]` |
| 1080x1920 EXR half RGBA + Z | 24.88 MB | **9–14 MB** |
| 4K PNG | 33.18 MB | **12–30 MB** `[I, LOW]` |
| 4K EXR half RGBA | 66.36 MB | **23–55 MB** |
| 4K EXR **multilayer** (full pass list + denoising + Z = 110 B/px) | 912 MB | **150 MB – 1 GB, typical 300–500 MB** |

`[V]` Real anchors for multilayer EXR:

- A Blender Artists codec chart for **one** half-float multilayer frame: B44 346,789 KB / B44A 260,472 / RLE 219,562 / PIZ 185,234 / ZIP **135,049** / ZIPS 134,723 / DWAA **89,051** KB. Resolution and pass count not recorded. https://blenderartists.org/t/multilayer-exr-file-sizes-chart/1325498
- A real 30-frame test: "file size for all multilayer-exr's = 506mb … none-multilayer exr's = 70mb" → **16.9 MB/frame multilayer vs 2.3 MB split, same frames.** https://blenderartists.org/t/1458370
- A vendor rule-of-thumb `[LOW]`: 4K 16-bit half 10–25 MB; 32-bit beauty 20–50 MB; 12-AOV multichannel 80–150 MB.

`[I]` **Practical rule: do not write multilayer EXR for every frame.** Write beauty single-layer or PNG, and multilayer only for hero shots that need relighting.

### 5.2 Mantaflow fluid (FLIP) and smoke cache sizes

`[V]` Real measurements:

| Cache | Scene | Figure | Source |
|---|---|---|---|
| FLIP liquid | 115 frames, 2021 | "115 frames and I already have 50GB of cache" → **~435 MB/frame** | https://blenderartists.org/t/1318962 |
| FLIP liquid **with particles** | low domain resolution, 2024 | "~3 GB of disk space… majority caused by `cache_fluid/particles/*.vdb`"; 100 GB ≈ 35 frames → **~3 GB/frame** | https://blender.stackexchange.com/questions/317303 |
| Smoke (pre-Mantaflow 2.78b) | 360 frames, 2017 | "nearly 390 GIGABYTES" → **~1.08 GB/frame** | https://blenderartists.org/t/684546 |
| Smoke | 130 frames high-res, 2009 | 1.4 GB total (~11 MB/frame, small domain) | https://blenderartists.org/t/449957 |
| Mantaflow fire+smoke | 200 frames, 2026 | "5–30 GB of VDB data" — **vendor estimate, no measurement shown** `[LOW]` | https://vfxrendering.com/best-render-farm-for-blender-smoke-and-fire-mantaflow-simulation-on-cloud/ |

`[V]` Cache-size multipliers from a Blender SE accepted answer (https://blender.stackexchange.com/questions/288475):

- Smallest configuration = OpenVDB + Blosc + **Half** precision
- "**Is Resumable**" makes the cache "**more than twice as big**"
- Enabling **Noise** is "easily **2.5 times** larger"
- "Doubling the divisions results in quadrupling the smoke voxels (but fortunately just about **tripling** the smoke cache size)"

`[I]` **250-frame shot budget:** PNG ~1.0 GB · single-layer EXR ~3 GB · multilayer EXR ~30 GB (range 10–60) · smoke VDB 6–38 GB · FLIP liquid ~109 GB · FLIP + particles ~750 GB.

### 5.3 OpenVDB

`[V]` OpenVDB is explicitly sparse — "designed specifically to work efficiently with sparse volumetric data"; the tree "given sparse unique values, minimizes the overall memory footprint"; per-grid metadata stores the active voxel count and memory usage in bytes; supports saving float as half. https://www.openvdb.org/documentation/doxygen/overview.html

`[I]` **Size tracks ACTIVE voxels, not the domain box.** Doubling resolution along each axis means 8× the voxels, though the measured Blender behaviour is nearer 3× cache growth per resolution doubling (above). My model for an N=128 cube across ~7 float32 grids is roughly 15–60 MB/frame with Half + Blosc and a 10–50% active fraction; N=256 lands around 100–470 MB/frame. `[NF]` **No published per-frame Blender smoke `.vdb` benchmark exists.**

### 5.4 Install and project footprint

`[V]` Official download sizes for **Blender 5.2.2 LTS (15 September 2026)** — https://www.blender.org/download/ :

| Platform | Size |
|---|---|
| Windows x64 `.msi` | 348 MB |
| Windows ARM `.msi` | 227 MB |
| **Windows PORTABLE `.zip`** | **386 MB** |
| macOS Apple Silicon `.dmg` | 330 MB |
| Linux `.tar.xz` | 366 MB |

`[V]` **Measured installed size on macOS ARM:** DMG 346 MB → `Blender.app` **907 MiB** (Resources/lib 350 MB, 5.2/python 218 MB, datafiles 127 MB, scripts 33 MB, extensions 1 MB). No universal-binary doubling because 5.x is Apple-Silicon-only. Budget **~0.9–1.6 GB per installed version**; every retained version costs another ~0.9 GB.

`[V]` **Portable install** — https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html#portable-installation : create a folder literally named `portable` next to the executable (Windows: beside `blender.exe` in the unzipped portable build; macOS: `Blender.app/Contents/Resources`). "This folder will then store preferences, startup file, installed extensions and presets." Alternative: the `BLENDER_USER_RESOURCES` environment variable. blender.org's requirements page: "No installation needed… Truly portable."

`[V]` Default user directories (for cleanup): Windows `%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\<ver>\`; macOS `/Users/$USER/Library/Application Support/Blender/<ver>/`. Local cache: Windows `%USERPROFILE%\AppData\Local\Blender Foundation\Blender\Cache\`; macOS `~/Library/Caches/Blender/`. The TEMP dir holds "render layers, physics cache, copy-paste buffer and crash logs" — point **File Paths → Temporary Files** at the big disk.

`[V]` **Asset libraries.** The bundled "Essentials" library **ships with Blender and is only ~12 MB** (brushes 7 MB, nodes 5 MB) — it is part of the install, not an extra. Separately downloadable asset bundles are optional: Human Base Meshes 49 MB, Ellie Pose Library 24 MB, Cube Diorama 11 MB. https://www.blender.org/download/demo-files/ and https://docs.blender.org/manual/en/latest/editors/preferences/asset_libraries.html

`[V]` ⚠ **5.2's new Cycles Texture Cache trades disk for RAM.** It writes `.tx` files next to your images, and they are typically **larger** than the sources, regenerating when images change. On a disk-tight Mac do **not** enable it globally. On the 16 GB side it is a genuine RAM win. Same feature, opposite verdict per machine.

### 5.5 Recommended storage layout and budget

`[I]` **Assumptions:** 1080x1920 at 30 fps; 20 reels/month averaging 20 s = **400 finished seconds = 12,000 frames**; deliverable PNG ~4 MB/frame; Cycles on the Windows/RTX 3080; Blender temp and cache dirs on the Windows NVMe; Mac is control/edit only; master ~1.5 MB per finished second; 2 multilayer hero shots + 2 smoke shots + 1 FLIP shot per month.

**Per finished second of Reels:** PNG ~120 MB/s · single-layer EXR ~360 MB/s · multilayer EXR ~3.6 GB/s · master ~1.5 MB/s.

**Per 250-frame shot:** PNG ~1.0 GB · single-layer EXR ~3.0 GB · multilayer ~30 GB · smoke VDB 6–38 GB · FLIP ~109 GB · FLIP+particles ~750 GB.

**Monthly:** PNG 48 GB + single-layer EXR 36 GB + 2 multilayer 60 GB + 2 smoke 75 GB + 1 FLIP 109 GB + masters/project 5–15 GB = **~160–220 GB typical**; heavy month 300–350 GB; heavy 4K month 0.5–1 TB.

**Layout:**

| Tier | Role | Contents |
|---|---|---|
| **Mac, 23 GB free** | Control only | `.blend`, scripts, reference, H.264/ProRes **proxy** review copies, finished masters. **Keep under ~15 GB**, leave ~8 GB headroom. **No caches, no frame sequences, no `.tx` texture cache.** |
| **Windows PC, 1 TB NVMe** | Working set | Active working copies, Blender temp dir, explicit fluid Cache Directory, in-flight VDB/FLIP caches, live render output, preview encodes. Peak concurrent demand ~110 GB (FLIP), ~75 GB (smoke), ~60 GB (4K multilayer). |
| **External USB-C SSD, 4 TB** | Archive | Raw PNG/EXR sequences, cache snapshots for hero shots, versioned `.blend` backups, asset libraries, masters. ~18–24 months at 160–220 GB/month. |
| **Cloud / offsite** (optional) | Safety | Finished masters + project `.blend` only, <10 GB/month. |

**Operational rules:** point Blender *File Paths → Temporary Files* and the fluid *Cache Directory* at the big NVMe. For sims use OpenVDB + Blosc + **Half**; keep **Is Resumable OFF** (>2× size) and **Noise OFF** while iterating (~2.5×). For 4K do not default to multilayer EXR on every frame. Move caches and sequences to the external drive per shot — treat the 1 TB internal as a working set, not an archive.

---

## 6. Mac M1 16 GB role

### 6.1 Versions and Apple Silicon support

`[V]` **Current stable and current LTS: Blender 5.2 LTS** (patch 5.2.2, 15 September 2026; released 14 July 2026; maintained until **July 2028**). **4.5 LTS** (4.5.14) is also maintained, until July 2027. **4.2 LTS support ended** July 2026. Blender **5.3 = alpha**, targeted ~November 2026. https://www.blender.org/download/ and https://www.blender.org/press/blender-5-2-lts-release/

`[V]` macOS requirements — https://www.blender.org/download/requirements/ : "Blender 4.5 LTS is the last release to support Intel… Blender 5.0 and later require Apple Silicon running macOS 13 (Ventura) or later." Minimum RAM 8 GB, recommended 32 GB — 16 GB sits between. **The M1 is officially supported.**

`[V]` **Metal became the default macOS backend in Blender 3.5**, not recently. Commit `87e5d7212c218b5bf476f292848d4379abf8b7ac` (Jeroen Bakker, 2023-02-20):

> "This patch will default to the Metal backend when starting Blender 3.5 for the first time or when loading factory startup… Currently Metal is more stable then the OpenGL backend on apple devices."

https://projects.blender.org/blender/blender/commit/87e5d7212c218b5bf476f292848d4379abf8b7ac

### 6.2 Is Cycles Metal production-ready?

`[V]` **Yes — it is documented as a first-class backend, not experimental.** The word "experimental" appears **nowhere** on https://docs.blender.org/manual/en/5.2/render/cycles/gpu_rendering.html . Exact text:

> "Metal for GPU acceleration is supported on Apple computers with Apple Silicon. macOS 13.0 or newer is required to support all features. GPU accelerated ray-tracing and denoising is available on Apple Silicon."

MetalRT is exposed as Off / On / Auto. The same page confirms that on CUDA/OptiX/HIP/Metal, GPU-memory overflow falls back to system RAM (slow, not fatal).

`[V]` **But not bug-free.** The 2026-09-15 Render & Cycles meeting (posted 16 September 2026, https://devtalk.blender.org/t/2026-09-15-render-cycles-meeting/45814 ) records: "Currently facing a compile problem under MacOS + Metal (endless compile loop)"; "Metal issues with shadows on older macOS versions [#162544]: Unable to reproduce ourselves"; "Michael saw the report about block shadows on M5. Could not reproduce yet." Open macOS/Metal tracker issues include #163955 (Cycles GPU viewport not updating when moving an object, 2026-09-15), #163210 (GPUOffScreen depth broken on Metal), #162698 (macOS fullscreen).

### 6.3 EEVEE on Metal — and its real weak spot

`[V]` EEVEE works on Apple Silicon via Metal. Its measurable weakness is **cold shader compilation**. Blender 5.1 release notes, `barbershop_interior`, seconds:

| Backend | Cold | Warm |
|---|---|---|
| Metal 5.0.1 | 55.50 | 1.18 |
| Metal 5.1 | 37.20 | 2.72 |
| Vulkan 5.1 | 11.67 | 5.93 |

(Tested on an **M1 Ultra** on macOS Tahoe 26.2.) So Metal is the **slowest backend cold** and the **fastest warm** — that is the "first-load stall" people report. A base M1 will be worse than the M1 Ultra tested. Blender 5.1 added parallel material compilation and a shader preprocessor to address it.

### 6.4 Fallback render capability and the speed ratio

`[V]` **Yes, it can render, and here is the ratio.** Blender Open Data, Blender 4.5.0 (M1 n=27, RTX 3080 n=579):

| Device | Median score (samples/min) | Relative to RTX 3080 |
|---|---|---|
| **Apple M1 (8-core GPU)** | **260.4** | **~17.4× slower** |
| Apple M1 (7-core GPU) | 232.9 | ~19.4× |
| Apple M1 Pro (16-core) | 482.9 | ~9.4× |
| Apple M1 Max (32-core) | 955.5 | ~4.7× |
| Apple M1 Ultra (64-core) | 1656.7 | ~2.7× |
| **NVIDIA GeForce RTX 3080** | **4529.2** | 1× |
| RTX 3080 **Laptop** GPU | 2857.5 | — |

The M1 is ~10× slower even than a *laptop* RTX 3080. Source: `https://opendata.blender.org/benchmarks/query/?compute_type=METAL&blender_version=4.5.0&group_by=device_name&response_type=datatables`

Blender 5.2.0 shows M1 8-core 269.5 vs RTX 3080 4208.4 (~15.6×), but the M1 sample size in 5.2 is n=1 — quote the 4.5 figure.

`[I]` At the planning band from §1.6 (128 samples ≈ 15–40 s/frame on the 3080), the M1 would need roughly **4–12 minutes per frame** at 1080x1920. Viable for the odd hero frame overnight; not viable as a routine renderer.

### 6.5 Authoring viability on 16 GB

`[V]` Hands-on test, BlenderNation, 27 May 2026, M1 Pro 16 GB MacBook Pro (https://www.blendernation.com/2026/05/27/macbook-neo-blender-sculpting-honest-polycount-and-memory-performance-test/ ):

> "At 6 million polys the memory pressure goes red, Blender starts swapping to disk, and eventually the process has to be killed. But dial it back to around 3 million and the experience is surprisingly smooth."
> "The bottleneck is RAM, not the CPU."

`[I]` A brick/iron/timber engineering scene is the **best case** for this machine: geometry is dense and compact compared with image textures, and a ~3M-polygon interactive ceiling comfortably covers typical engineering assets. The risks are EEVEE cold shader compiles and texture-heavy look-dev.

`[V]` Texture memory reference (manual): 8K = 256 MB, 4K = 64 MB, 2K = 16 MB, 1K = 4 MB each.

`[V]` **Two Blender 5.2 features materially help the 16 GB case:**
1. **Cycles Texture Cache** — "significantly reduces memory usage and startup time… at the cost of a small rendering performance impact, and increase disk space usage." (See the disk warning in §5.4.)
2. **EEVEE instancing** — "Instancing-heavy scenes (CPU bottlenecked) can be up to twice as fast." Directly helps repeated brick/timber/structural geometry.

`[NF]` No credible source for viewport FPS on a comparable engineering scene at 16 GB, and **no documented Metal VRAM / wired limit for 16 GB**. The widely-cited "~10.67 GB (2/3 of RAM)" should be treated as **unverified**. Settle it by querying `MTLDevice.recommendedMaxWorkingSetSize` or `sysctl iogpu.wired_limit_mb`.

### 6.6 Disk footprint and low-disk workflow on the Mac

`[V]` macOS install **907 MiB measured**. Each retained version costs another ~0.9 GB (5.2 + 4.5 + 5.3-alpha ≈ 2.7 GB). `~/Library/Application Support/Blender/<ver>/` holds config, `startup.blend`, bookmarks and `recent-files.txt` — negligible. The bundled Essentials asset library is only **12 MB**. The Blender Benchmark launcher cache at `~/Library/Caches/blender-benchmark-launcher` is **multi-hundred-MB** if you ever run Open Data — **do not run it on the Mac**.

`[I]` **Legitimate low-disk workflow:**
- Use the **Windows-style portable build** on macOS: `Blender.app` with a `portable` folder in `Contents/Resources`, or set `BLENDER_USER_RESOURCES`. Keep `~/Library/Application Support` free of Blender state.
- Retain **only 5.2 LTS**. Delete 4.5 or 5.3-alpha unless a project needs them.
- Keep asset libraries off-disk: use Remote Asset Libraries on demand (below) with internet access off by default.
- Never enable Cycles Texture Cache on the Mac.
- Keep `.blend` + proxies + masters only; all caches and frame sequences live on the Windows box or the external drive.

### 6.7 Remote Asset Libraries

`[V]` The code.blender.org post exists exactly as described: **"Remote Asset Libraries", Julian Eisel, 22 July 2026** — https://code.blender.org/2026/07/remote-asset-libraries/ (companion notes: https://notes.blender.org/s/rAgFm9k1bs ).

`[V]` **It shipped in Blender 5.2 LTS and is NOT experimental** — no experimental/beta label in the blog, the 5.2 release notes, or the manual. Confirmed in the 5.2 release notes: "**Online Asset Libraries** — It is now possible to register remotely hosted asset libraries, browse them from within Blender, and download assets as needed. This requires Allow Internet Access to be enabled in the Preferences." The 5.2 press release adds: "Asset Libraries now support remote hosting, enabling users to access the Blender Online Essentials library on demand as well as host their own."

`[V]` **Mechanism:** per-asset download (right-click in the Asset Browser / hover button in the Asset Shelf / right-click in the Add menu); listings auto-update once per day when internet access is on; hosting needs only a static HTTP server (must send `Content-Length`, ignore query strings, `ETag` recommended); listing generator CLI `blender -c asset_listing generate /path`; optional per-library access token; version targeting via filenames like `my_asset@b5_3.blend`; first-class offline mode with an "Offline Only" filter.

`[V]` **Does it help a low-disk setup? Partly, and it depends on discipline.**

*Genuine wins:* the blog is explicit that online Essentials content ships "without increasing Blender's download size" (the installer stays 330 MB / 907 MB installed); nothing downloads until you ask; cached downloads are deletable via 'Open File Location' and are "stripped down of all niceties to make the download as small as possible"; Blender remains fully usable offline.

*The catch:* it is **download-on-demand, not stream-from-remote** — "Downloaded assets are stored in Blender's local cache so they only need to be downloaded once… Blender will reuse the cached copy." There is **no streaming, no automatic eviction/LRU, and no size cap**; cleanup is **manual**. Multi-asset `.blend` files require downloading the whole file to use one asset, and a daily listing sync also writes to disk. Open bugs: #163648 "Remote Asset Library never Append (always Pack)" (2026-09-08) and #162741 multi-file support (2026-08-17).

`[I]` **Safest configuration on a tight disk: leave "Allow Internet Access" OFF.** The feature is then fully inert, costs zero bytes, and Blender behaves exactly as before. Turn it on only to fetch a specific asset, then delete the cache entry via 'Open File Location'.

---

## What could not be found

Stated plainly rather than estimated:

1. **Per-scene (monster/junkshop/classroom) Open Data sample rates for the RTX 3080.** No endpoint or published table exposes them, and the CC0 snapshot stores render time and peak VRAM but **not** sample counts. Settle by running the benchmark locally.
2. **A measured out-of-core slowdown factor for Cycles** when a scene exceeds 10 GB VRAM. Only the qualitative official statement exists.
3. **Any measured cross-machine or cross-version physics determinism comparison.**
4. **A published per-frame Blender smoke `.vdb` benchmark.** Only user measurements and vendor estimates.
5. **Official Blender figures for fluid/smoke cache size per frame.** Do not quote one as official.
6. **Viewport FPS and a documented Metal VRAM limit for an M1 16 GB.**
7. **A photographic-PNG compression benchmark** for realistic 1080x1920 / 4K PNG sizes — those ranges are inference.

---

## Decision-relevant bottom lines

- **The RTX 3080 10 GB is fine.** The heaviest official benchmark scene peaks at 4.7 GB; Cycles falls back to system RAM rather than failing; and the manual's tile-size and compact-BVH levers buy headroom. The 12 GB model buys threshold, not speed.
- **At 1080x1920 with OptiX + OIDN, plan 128 samples at roughly 15–40 s/frame (90–240 frames/hour).** Denoised 64–128 samples is the Reels sweet spot; 256 is usually waste at that resolution.
- **EEVEE is an honest 12–14× speedup and a genuine fit for brick / iron / timber.** It is **not** a fit for water, glass or volumetrics — keep those on Cycles. Watch the 16-bit output precision.
- **Headless is solved for Cycles everywhere**, and for EEVEE everywhere **except headless Windows systems**. Keep EEVEE on the interactive Windows desktop session.
- **Blender's Network Render is gone.** Flamenco 3.9.3 is the official answer but needs shared storage at identical paths; CrowdRender's paid tier only lists Blender 5.1. With two machines, manual `-s`/`-e` range splitting is the pragmatic path.
- **Bake every simulation to an explicit, stable Cache Directory with Type = All before rendering.** Rigid body has no seed (the "per-session seed" story is false); Mantaflow's default cache folder is session-named and will silently re-simulate if left unset.
- **The Mac M1 16 GB is a legitimate authoring machine** (~3M-poly interactive ceiling; Metal default since 3.5; Cycles Metal production-ready but not bug-free; ~17× slower than the 3080 as a fallback renderer) **but must hold zero caches, frame sequences or `.tx` texture caches.** Remote Asset Libraries (5.2, non-experimental) helps only if you keep internet access off by default and clean the cache manually.
