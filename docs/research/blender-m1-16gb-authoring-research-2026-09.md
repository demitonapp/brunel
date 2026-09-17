# Blender on Apple M1 / 16 GB for AUTHORING — research report

Research date: **September 2026**. Question scope: authoring (modelling, look-dev, light simulation),
**not** final rendering.

Legend: **[VERIFIED]** = read directly from the cited source during this research.
**[INFERENCE]** = my reasoning from verified data. **[UNVERIFIED]** = could not confirm.

---

## 1. Apple Silicon / Metal status in Blender 5.x

### 1.1 Current stable and LTS versions [VERIFIED]

| Item | Value | Source |
|---|---|---|
| Current stable | **Blender 5.2 LTS**, patch release **5.2.2**, dated **September 15, 2026** | [blender.org/download](https://www.blender.org/download/) |
| Current LTS | **5.2 LTS** — released **July 14, 2026**, maintained **until July 2028** | [release notes index](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/index.md) |
| Other maintained LTS | **4.5 LTS** — released July 15, 2025, last updated **4.5.14** on Sept 15, 2026, supported until July 2027 | [blender.org/download/lts](https://www.blender.org/download/lts/) |
| Next release | **Blender 5.3 (alpha)**, targeted **November 2026** | [compatibility index](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/compatibility/index.md) |
| Recently ended LTS | 4.2 LTS released July 16, 2024, support ended July 2026 | release notes index (above) |

Quote (release notes index): *"**[Blender 5.2 LTS](5.2/index.md)** *(current stable release - July 14, 2026)*"*

**macOS requirements [VERIFIED]** — [blender.org/download/requirements](https://www.blender.org/download/requirements/):

> "**Blender 4.5 LTS is the last release to support Intel and macOS 11.2 (Big Sur).** **Blender 5.0** and
> later require **Apple Silicon** running macOS **13** (Ventura) or later."

macOS minimum: 13 (Ventura); recommended macOS 26 (Tahoe). RAM minimum 8 GB, recommended 32 GB.
A 16 GB machine sits exactly between the official minimum and recommendation.
Blender 5.3 raises the hard floor from 11.2 to 13.0, formalising what 5.x already required
([announcement](https://devtalk.blender.org/t/macos-minimum-deployment-target-increased-from-11-2-to-13-0/45786),
cited in the compatibility index). **M1 is an officially supported CPU class** — nothing in the
requirements excludes it.

Download sizes for 5.2.2 [VERIFIED, blender.org/download]: macOS Apple Silicon **330 MB**; Windows x64 348 MB;
Linux 366 MB.

### 1.2 Is Metal the default GPU backend on macOS? [VERIFIED — yes, since Blender 3.5]

The specific commit is **`87e5d7212c218b5bf476f292848d4379abf8b7ac`**, authored by **Jeroen Bakker**,
committer date **2023-02-20**, retrievable from the Blender repo:

- Commit: https://projects.blender.org/blender/blender/commit/87e5d7212c218b5bf476f292848d4379abf8b7ac
- (Gitea API, which returned the metadata: `https://projects.blender.org/api/v1/repos/blender/blender/git/commits/87e5d7212c218b5bf476f292848d4379abf8b7ac`)

Commit message, quoted:

> "Mac: Enable Metal as default gpu backend.
>
> Currently Metal is more stable then the OpenGL backend on apple devices. Also the Metal backend
> supports more features then the OpenGL backend. For example the viewport compositor and rendering
> of production files.
>
> This has been validated with users and studios.
>
> This patch will default to the Metal backend when starting **Blender 3.5** for the first time or
> when loading factory startup. It is still possible to switch to OpenGL via the user preferences."

Corroboration in released docs: the Blender 5.0 release notes' example startup log shows Metal being
chosen with no user override — *"Using GPU "Apple M3 Max Metal API 1.2" / Using Backend "Metal""*
([5.0/core.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.0/core.md)).

**[INFERENCE]** For any 5.x build, Metal is the default and Metal is *not* an experimental/opt-in path.
Metal being default does **not** mean it is the fastest backend: Blender 5.3 makes **Vulkan** the default on
Windows (non-ARM) and Linux, but makes no equivalent change for macOS — Vulkan is not the macOS default
([5.3/eevee.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.3/eevee.md)):
> "Vulkan backend is now default on Windows (not ARM) and Linux. Existing user preferences will not be migrated."

### 1.3 Is Cycles Metal production-ready, or still experimental? [VERIFIED — production-ready, no experimental flag]

Manual page: https://docs.blender.org/manual/en/5.2/render/cycles/gpu_rendering.html
(raw source: https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cycles/gpu_rendering.rst)

Full Metal section, quoted verbatim:

> **Metal — Apple (macOS)**
>
> Metal for GPU acceleration is supported on Apple computers with Apple Silicon.
> macOS 13.0 or newer is required to support all features.
>
> GPU accelerated ray-tracing and denoising is available on Apple Silicon.

Findings:
- **The word "experimental" does not appear anywhere in the GPU Rendering page.** Metal is documented as a
  first-class backend alongside CUDA, OptiX, HIP and oneAPI. **[VERIFIED]** by reading the full manual source.
- Metal is listed in Preferences → System as a normal Cycles compute device:
  *"If the system has a compatible Apple Metal device, it will be available as an option for rendering with Cycles."*
- `MetalRT` (hardware ray tracing) is exposed with `Off` / `On` / `Auto`:
  *"MetalRT for ray tracing uses less memory for scenes which use curves extensively, and can give better
  performance in specific cases."*
  ([system preferences source](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/editors/preferences/system.rst))
- No "Experimental" or "Beta" badge on Metal in the 5.2 manual.
- **Failure mode caveat [VERIFIED]**: the manual notes that on CUDA/OptiX/HIP/Metal, *"if the GPU memory is
  full Blender will automatically try to use system memory. This has a performance impact, but will usually
  still result in a faster render than using CPU rendering."* On a unified-memory Mac this means overflow is
  slow rather than a hard OOM.

**[VERIFIED] It is not bug-free.** The most recent Render & Cycles meeting notes (2026-09-15, posted Sept 16 2026)
list live Metal issues — [devtalk 45814](https://devtalk.blender.org/t/2026-09-15-render-cycles-meeting/45814):
- *"Currently facing a compile problem under MacOS + Metal (endless compile loop)"* — on the OpenPBR "weighted thin film" feature.
- *"Metal issues with shadows on older macOS versions [#162544]: Unable to reproduce ourselves and conditions are unclear."*
- *"Michael saw the report about block shadows on M5. Could not reproduce yet, but keeps looking into it."*

Apple staff participate in these meetings (a "Michael" reports on Metal issues; attendees include Apple-side
contributors), which is [INFERENCE]-level evidence of continued vendor investment. Note this is an
**M5** shadow report, not M1.

### 1.4 Does EEVEE (Next) work on Apple Silicon via Metal in 5.x? [VERIFIED — yes, with shader-compile stalling]

**Verdict: yes.** EEVEE works through the Metal backend; there is no macOS/Apple-Silicon exclusion for EEVEE in
the 5.2 manual, and the 5.3 release notes describe Metal-specific workbench features being *added*
(*"Hardware raytraced shadows in Workbench (Metal and Vulkan)"*), i.e. Metal is a first-class EEVEE target.

**Known, quantified Apple-Silicon-specific EEVEE weakness: shader/material compilation latency.**
Blender 5.1 release notes, `barbershop_interior`, seconds ([5.1/eevee.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.1/eevee.md)):

| Version | Backend | Scene | Cold | Warm |
|---|---|---|---|---|
| 5.0.1 | OpenGL | barbershop_interior | 44.19 | 5.68 |
| 5.1 | OpenGL | barbershop_interior | 30.39 | 6.51 |
| 5.0.1 | Vulkan | barbershop_interior | 24.87 | 5.22 |
| 5.1 | Vulkan | barbershop_interior | 11.67 | 5.93 |
| **5.0.1** | **Metal** | barbershop_interior | **55.50** | **1.18** |
| **5.1** | **Metal** | barbershop_interior | **37.20** | **2.72** |

Quoted note: *"Tests have been conducted on NVIDIA RTX 6000 Ada ... **For Metal, tests have been conducted on a
Apple M1 Ultra on macOS Tahoe 26.2.**"* and *"The overhead of the warm case will be addressed in the next release."*

Reading: on Metal, **cold** (no shader cache) material compilation is the **slowest of the three backends**
(37.20 s vs 11.67 s Vulkan); **warm** (cached) it is the **fastest** (2.72 s vs 5.93 s Vulkan). This is the
mechanism behind the widely reported "first-load stall / recompile hitch" on Apple Silicon. Note the test
hardware is an **M1 Ultra**, so a base M1 will be slower still. 5.1 also added parallel material pipeline
compilation and a shader source preprocessor specifically to attack this.

Blender 5.2 EEVEE improvements relevant to a weak GPU [VERIFIED, [5.2/eevee.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.2/eevee.md)]:
> "EEVEE now supports the same instancing optimizations as Workbench and Overlay. Instancing-heavy scenes
> (CPU bottlenecked) can be up to twice as fast."

5.2 also reworked Screen Space Raytracing and fixed Fast GI/AO. **5.2's headline feature for a 16 GB machine
is in Cycles, not EEVEE: the Texture Cache** (see 2.3).

**[UNVERIFIED]** I could not find an official statement that EEVEE on Metal is *performance-parity* with Vulkan
on other platforms. Data above suggests it is competitive once cached.

### 1.5 M1-specific known issues

What I can verify:

- **Shader compilation stalls: confirmed and quantified** — see the 5.1 table above (M1 Ultra, cold 37.20 s).
- **The 16 GB unified-memory ceiling is real, but there is no fixed "VRAM limit" in Blender** [VERIFIED].
  Metal on Apple Silicon is unified memory; the manual describes spill-to-system-memory rather than a VRAM
  partition, and Blender exposes no "VRAM limit" preference for Metal. Apple's own GPU memory cap is a macOS
  driver behaviour, not a Blender setting, and it is **not documented on blender.org**.
  **[UNVERIFIED]** — I found no official Blender source stating a default Metal VRAM/wired limit figure.
  What would settle it: an Apple developer-documentation page on `recommendedMaxWorkingSetSize` for M1, or a
  `MTLDevice` query run on the machine (`sysctl iogpu.wired_limit_mb`). On a 16 GB M1 the commonly-cited
  default wired limit is ~10.67 GB (2/3 of RAM), but **I could not verify this from an official source in this
  research** — treat the number as UNVERIFIED.
- **Manual error guidance for memory pressure [VERIFIED]** — texture sizes:
  *"8k, 4k, 2k, and 1k image textures take up respectively 256MB, 64MB, 16MB and 4MB of memory."*
  So ~40 4K textures exhaust a ~2.5 GB budget; this is the practical look-dev wall on 16 GB shared memory.
- **Real user report on a 16 GB Apple Silicon Mac (2026)** — BlenderNation, 27 May 2026, summarising a
  hands-on stress test comparing a low-end Apple laptop (8 GB), **an M1 Pro MacBook Pro with 16 GB RAM**, and
  a 128 GB + RTX 5090 desktop ([blendernation.com](https://www.blendernation.com/2026/05/27/macbook-neo-blender-sculpting-honest-polycount-and-memory-performance-test/)):
  > "In this video I push the MacBook Neo from 200,000 to 12 million polygons ... At **6 million polys the memory
  > pressure goes red, Blender starts swapping to disk, and eventually the process has to be killed.** But dial it
  > back to around **3 million and the experience is surprisingly smooth** across draw, crease, snake hook, and smooth brushes."
  > "**The bottleneck is RAM, not the CPU.**"
- **Known M1/M2-specific Blender bug (community-reported)** — Blender Artists thread:
  *"Be careful with VideoTexture: If you're on M1 or M2 powered Macs, do not use ImageMirror"*
  ([blenderartists.org](https://blenderartists.org/t/be-careful-with-videotexture-if-youre-on-m1-or-m2-powered-macs-do-not-use-imagemirror/1476805/2)).
  This is a narrow VSE/VideoTexture issue, **[UNVERIFIED]** as to whether still present in 5.2.

Open macOS/Metal issues in the public tracker as of Sept 2026 (from the Blender Gitea issues API,
`https://projects.blender.org/api/v1/repos/blender/blender/issues?state=open`), selected:
- **#163955** — "Cycles GPU: Viewport does not update when moving object" (2026-09-15)
- **#163670** — "Cycles: Viewport does not register that the render device is changed with factory startup on macOS" (2026-09-08)
- **#163210** — "`GPUOffScreen` depth from `draw_view3d` does not work on Metal" (2026-08-27)
- **#163457 / #163456** — macOS colour/object eye-dropper broken across windows (2026-09-03)
- **#162698** — "macOS Fullscreen problems" (2026-08-15)
- **#163586** — "PyGPU: Creating GPUTexture above hardware texture limit fails with useless 'unknown error'" (2026-09-06)

**[VERIFIED]** — these are open, current macOS/Metal bugs; none is M1-exclusive.

### 1.6 Blender Open Data benchmark figures [VERIFIED — queried live]

Method: the site's own JSON endpoint used by its search page,
`https://opendata.blender.org/benchmarks/query/?compute_type=...&blender_version=...&group_by=device_name&response_type=datatables`
(the AJAX URL is visible in the page's inline script on https://opendata.blender.org/benchmarks/query/).
**Median Score** is defined officially as ([opendata.blender.org/about](https://opendata.blender.org/about/)):
> "The Blender benchmark Score is a measure of how quickly Cycles can render path tracing samples on one CPU or
> GPU device. ... In particular it's the **estimated number of samples per minute, summed for all benchmark scenes.**"

So the score **is** the aggregate of per-scene samples/minute the task asked for — not a normalised index.

**Blender 4.5.0 (largest sample sizes; the most trustworthy row):**

| Device | Median Score | # Benchmarks | vs RTX 3080 |
|---|---|---|---|
| **Apple M1 (GPU – 8 cores)** | **260.4** | 27 | **17.4× slower** |
| Apple M1 (GPU – 7 cores) | 232.9 | 6 | 19.4× |
| Apple M1 Pro (14 cores) | 442.9 | 22 | 10.2× |
| Apple M1 Pro (16 cores) | 482.9 | 43 | 9.4× |
| Apple M1 Max (24 cores) | 794.0 | 26 | 5.7× |
| Apple M1 Max (32 cores) | 955.5 | 50 | 4.7× |
| Apple M1 Ultra (48 cores) | 1440.3 | 4 | 3.1× |
| Apple M1 Ultra (64 cores) | 1656.7 | 6 | 2.7× |
| **NVIDIA GeForce RTX 3080** | **4529.2** | 579 | 1× (baseline) |
| NVIDIA GeForce RTX 3080 Ti | 5315.5 | 207 | 0.85× |
| NVIDIA GeForce RTX 3080 Laptop GPU | 2857.5 | 53 | 1.6× |

**Blender 4.2.0:**

| Device | Median Score | # | vs RTX 3080 |
|---|---|---|---|
| Apple M1 (8 cores) | 265.9 | 30 | 16.8× slower |
| Apple M1 Pro (16 cores) | 482.1 | 64 | 9.3× |
| Apple M1 Max (32 cores) | 949.4 | 51 | 4.7× |
| Apple M1 Ultra (64 cores) | 1725.7 | 6 | 2.6× |
| NVIDIA GeForce RTX 3080 | 4459.4 | 410 | 1× |

**Blender 5.2.0 (thin data — treat with caution):**

| Device | Median Score | # | vs RTX 3080 |
|---|---|---|---|
| Apple M1 (7 cores) | 244.1 | **1** | 17.1× slower |
| Apple M1 (8 cores) | 269.5 | **1** | 15.5× slower |
| Apple M1 Pro (14/16 cores) | 510.7 / 533.5 | 4 / 12 | 8.2× / 7.8× |
| Apple M1 Max (24/32 cores) | 915.6 / 1079.1 | 6 / 9 | 4.6× / 3.9× |
| Apple M1 Ultra (48 cores) | 1541.7 | 1 | 2.7× |
| NVIDIA GeForce RTX 3080 | 4184.1 | 48 | 1× |

**Per-scene breakdown (monster / junkshop / classroom):** **[UNVERIFIED — could not obtain]**.
The Open Data query API exposes `group_by` only over `compute_type`, `device_name`, `operating_system` and
`blender_version` (confirmed from the page's `groupable-columns-json` block). Per-scene samples are only shown
in individual submission detail views, which are not enumerable via that endpoint. What would settle it:
downloading the **daily full dataset snapshot** linked from https://opendata.blender.org/download/ (CC0 licence)
and filtering to the M1 device rows. I did not download it in this session.

**Headline [VERIFIED]:** a base **M1 (8-core GPU) is ≈15–17× slower than an RTX 3080** in Cycles, across
Blender 4.2, 4.5 and 5.2 data. The M1's absolute throughput is ~260 samples/minute summed across all seven
benchmark scenes — i.e. roughly **3 samples/minute per scene in aggregate terms**, which is the number that
makes clear this is not a render box.

---

## 2. Authoring viability on an M1 / 16 GB

### 2.1 Realistic limits [VERIFIED where cited]

| Constraint | Figure | Source / basis |
|---|---|---|
| Sculpt mode, smooth | **≤ ~3 million polygons**; degrades at 6 M | M1 Pro 16 GB hands-on test, [BlenderNation 2026-05-27](https://www.blendernation.com/2026/05/27/macbook-neo-blender-sculpting-honest-polycount-and-memory-performance-test/) |
| Sculpt mode, failure | ~6 M polys → memory pressure red, **swapping, process killed** | same |
| Dyntopo | works "at manageable polycounts"; *"dynamic topology at 50 million polys consumed nearly 100GB of RAM"* on a 128 GB desktop | same |
| Texture memory | 8K=256 MB, 4K=64 MB, 2K=16 MB, 1K=4 MB per image | [Cycles GPU manual](https://docs.blender.org/manual/en/5.2/render/cycles/gpu_rendering.html) |
| RAM | 16 GB installed; official minimum 8 GB, **recommended 32 GB** | [requirements](https://www.blender.org/download/requirements/) |
| Viewport FPS | **[UNVERIFIED]** — no official or reliable artist figure found | see below |

For **brick/iron/timber engineering scenes** (lots of geometry, a few lights, light simulation — the stated
use case): geometry-heavy but texture-light scenes are the *best* case for this machine. Vertex/face data is
dense and compact compared with image textures, and the M1's ~3 M-poly practical ceiling for interactive
sculpting is roughly an order of magnitude above what a typical engineering/architectural asset needs.
**[INFERENCE]** Modelling, look-dev and light placement should be usable; the risks are (a) long EEVEE cold
shader compiles when lighting setups change, and (b) memory pressure if the scene leans on many high-resolution
PBR textures.

**[UNVERIFIED] — viewport FPS figures.** I could not find a credible, dated, M1-16 GB-specific viewport FPS
measurement for a comparable engineering scene on blender.org, devtalk, or Open Data. What would settle it:
(a) running `window.cursor_warp`-free FPS instrumentation via Blender's own 5.1+ **performance timing statistics
overlay for the 3D viewport** (added in 5.1: *"Added a performance timing statistics overlay for the 3D viewport"*)
on the actual scene, or (b) an Open Data submission for the exact scene. Treat any FPS number quoted to you
without a scene description as meaningless.

### 2.2 The M1 as a fallback renderer, and the ratio vs an RTX 3080

**Yes — the M1 Mac can act as a fallback renderer. [VERIFIED]** Cycles Metal is production-supported on Apple
Silicon, including hardware ray tracing and denoising. It is not blocked or experimental.

**Ratio [VERIFIED, from Open Data median scores above]:**
- **Base M1 (8-core GPU) ≈ 15–17× slower than an RTX 3080.**
- M1 Pro (16-core) ≈ **9.4×** slower; M1 Max (32-core) ≈ **4.7×** slower; M1 Ultra (64-core) ≈ **2.7×** slower.

Caveats on that ratio, so it is not over-read:
- It is a **Cycles path-tracing** ratio. It does **not** transfer to EEVEE (different workload, and EEVEE is
  often CPU/scene-graph-bound — 5.2's instancing optimisation was explicitly described as *"CPU bottlenecked ...
  up to twice as fast"*).
- It is a median of community submissions, not a controlled benchmark.
- The 3080 column includes many desktop submissions; laptop-3080 is ~1.6× slower than desktop-3080, so the
  M1 is ~**10×** slower than a *laptop* 3080.
- The M1's 5.2.0 sample size is **1**, so the 15.5× figure is weak; the 4.5.0 figure (n=27) at **17.4×** is
  the one to quote.

### 2.3 The two features that most change the 16 GB calculus [VERIFIED]

**(a) Cycles Texture Cache — new in 5.2 LTS.** From the 5.2 Cycles release notes
([5.2/cycles.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.2/cycles.md)):
> "On scenes with many image textures, the texture cache significantly reduces memory usage and startup time.
> This comes at the cost of a small rendering performance impact, **and increase disk space usage.**"
> "For every image, a corresponding `tx` file will be generated in the `blender_tx/` folder next to the image file."

It is enabled via Performance → Texture Cache → Auto Generate, and there is a `--command maketx` CLI, plus a
new Simplify → Texture Resolution percentage *"particularly useful for viewport rendering of complex scenes with
the texture cache."* Note the **disk-space tradeoff** (see section 3), and that the manual documents
*"By default, files are stored in the `blender_tx/` folder next to the image file"*
([Cycles performance manual](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cycles/render_settings/performance.rst)).

**(b) EEVEE instancing performance — new in 5.2**, up to **2× faster** on instancing-heavy scenes (quoted in 1.4).

**[INFERENCE]** Together these are the difference between "16 GB is painful" and "16 GB is workable": texture
cache trades disk for RAM (relevant if disk is also tight — a real tension for a low-disk setup), and instancing
helps exactly the repeated-element geometry that brick/timber/structural scenes are made of.

---

## 3. Disk footprint on macOS

### 3.1 Blender.app install size — **measured, not estimated** [VERIFIED]

I downloaded the official **Blender 5.2.2 macOS Apple Silicon** disk image from the official mirror and
mounted it with `hdiutil`, then measured the bundle:

- **DMG file:** `blender-5.2.2-macos-arm64.dmg`, **346,286,611 bytes ≈ 330 MiB** (matches the 330 MB listed on
  [blender.org/download](https://www.blender.org/download/)); HTTP `content-length: 346286611`
- **Installed `Blender.app` on disk: 907 MiB** (`du -sm` → 907; `du -sk` → 928,300 KiB)

Breakdown of the installed bundle [VERIFIED]:

| Path | Size |
|---|---|
| `Blender.app` total | **907 MB** |
| `Contents/Resources` | 730 MB |
| `Contents/MacOS` | 175 MB |
| `Contents/_CodeSignature` + `PlugIns` + plist | ~5 MB |
| — `Contents/Resources/lib` | 350 MB (shared libraries) |
| — `Contents/Resources/5.2/python` | 218 MB |
| — `Contents/Resources/5.2/datafiles` | 127 MB |
| — `Contents/Resources/5.2/scripts` | 33 MB |
| — `Contents/Resources/5.2/extensions` | 1 MB |
| `Contents/MacOS/Blender` (single executable) | 174 MB |
| — `datafiles/locale` | 77 MB |
| — `datafiles/colormanagement` | 20 MB |
| — `datafiles/fonts` | 15 MB |
| — `datafiles/assets` (bundled **Essentials** library) | **12 MB** (brushes 7 MB, nodes 5 MB) |
| — `datafiles/studiolights` | 4 MB |

**[INFERENCE]** ~907 MB ≈ **0.9 GB** per installed version. There is only one architecture in the bundle
(a single 174 MB `Blender` executable — Blender 5.x is Apple-Silicon-only, so there is no universal-binary
doubling). Keeping multiple versions (e.g. 5.2 LTS + 4.5 LTS + a 5.3 alpha) costs ~0.9 GB each.

### 3.2 Portable / minimal install [VERIFIED]

From [Blender's Directory Layout](https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html)
(raw source: https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/advanced/blender_directory_layout.rst):

> "**Portable Installation** — When running Blender from a portable drive, it's possible to keep the
> configuration files on the same drive to take with you. To enable this, create a folder named `portable`
> at the following locations: ... **macOS: Inside the application bundle at `Blender.app/Contents/Resources`**
> This folder will then store preferences, startup file, installed extensions and presets."

Also [VERIFIED]:
> "The `BLENDER_USER_RESOURCES` environment variable can be set to a custom directory to replace the default
> user directory."

And the download page sells this as a feature ([requirements page](https://www.blender.org/download/requirements/)):
> "**Truly Portable** ... **No installation needed**, **no Internet connection required.**"

The macOS install manual confirms the normal flow ([installing/macos](https://docs.blender.org/manual/en/latest/getting_started/installing/macos.html)):
> "To make the installation and configuration fully self-contained, set up a Portable Installation."

**[INFERENCE] Minimal-install recipe:** drag `Blender.app` to `/Applications` (or anywhere), then create
`Blender.app/Contents/Resources/portable/` — config, startup file, extensions and presets then live *inside*
the bundle, so the whole install is one movable ~907 MB directory plus whatever you install into it. Note that
writing inside the bundle requires the app not be in a read-only/signed location (dragging out of the DMG first
is required — the DMG itself is read-only). `BLENDER_USER_RESOURCES` achieves the same without touching the bundle.

### 3.3 Where config and cache live on macOS [VERIFIED]

**User config**, from the directory-layout manual (exact path, with the version number substituted):
```
/Users/$USER/Library/Application Support/Blender/<BLENDER_VERSION>/
```
Confirmed independently by a real startup log in the Blender 5.0 release notes
([5.0/core.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.0/core.md)):
```
Read prefs: "/Users/blender/Library/Application Support/Blender/5.0/config/userpref.blend"
Read startup: "/Users/blender/Library/Application Support/Blender/5.0/config/startup.blend"
```
Contents of `./config/`: `userpref.blend` (preferences), `startup.blend`, `bookmarks.txt`,
`recent-files.txt` — all [VERIFIED] from the path-layout section.

**System (bundled) resources on macOS**, from the same manual:
```
./Blender.app/Contents/Resources/<BLENDER_VERSION>/
```

**Local cache directory** [VERIFIED] — section `Local Cache Directory` of the directory-layout manual:
> "The cache directory is used to store persistent caches locally. Currently it is only used for the indexing
> of Asset Libraries. The operating system is not expected to clear this automatically."

**[UNVERIFIED]** The manual states *"The following path will be used:"* but the resolved macOS path string was
cut off in the source I read. **[INFERENCE]** On macOS this is conventionally
`~/Library/Caches/Blender/`, but I did not verify the literal string.
What would settle it: reading the remainder of the `local-cache-dir` anchor in
`manual/advanced/blender_directory_layout.rst`.

**Benchmark launcher cache** [VERIFIED] — [opendata.blender.org/about](https://opendata.blender.org/about/):
> "macOS: `~/Library/Caches/blender-benchmark-launcher`"

Note this is a *separate* multi-hundred-MB cache if you run Blender Open Data (it downloads scenes and Blender
binaries) — relevant on a low-disk machine.

### 3.4 A working project — typical sizes

**[UNVERIFIED — no official figures exist.]** Blender publishes no guidance on project sizes; `.blend` size is
entirely content-dependent. I found no official number to cite, so any figure here would be invention. What
would settle it: sampling the actual scene files. The one *official* adjacent number is Blender's own
[Demo Files](https://www.blender.org/download/demo-files/) download, whose archive sizes bound a full production
scene — that is the honest proxy to measure if a number is needed.

The *official* figures I can give that bound project disk use:
- **Embedded/packed textures [VERIFIED]:** the remote-asset manual requires assets be *"self-contained within a
  single .blend file"* with textures packed — so a look-dev asset's `.blend` carries its image data. Combined
  with the manual's texture-size table (8K = 256 MB uncompressed in RAM; on disk a PNG/EXR is typically a
  fraction of that), a texture-heavy look-dev file can plausibly reach hundreds of MB to several GB.
  **[INFERENCE]**
- **Texture Cache `.tx` files [VERIFIED, and this is the important one for a low-disk setup]:** Cycles 5.2
  writes *"a corresponding `tx` file ... in the `blender_tx/` folder next to the image file"* and the release
  notes explicitly warn of *"increase[d] ... disk space usage"*. These are tiled+mipmapped derivatives, so they
  are typically **larger than the source images**, and they land **next to your project textures**, doubling
  (or more) the texture footprint, plus they are *"automatically updated when the image file is modified."*
  **[INFERENCE]** — for a disk-constrained setup, do **not** enable Texture Cache globally; it trades exactly
  the resource that is scarce here.
- **Autosave / recovery [VERIFIED]:** `./autosave` is *"Located in user directories"* on macOS and now also
  stores image information for files edited inside Blender (5.2 core notes), so autosaves are larger in 5.2.

### 3.5 Bundled / optional asset libraries — size and can they be skipped? [VERIFIED]

- The bundled **Essentials** asset library ships inside the app and measured **12 MB** on disk
  (`Contents/Resources/5.2/datafiles/assets/`: brushes 7 MB, nodes 5 MB) — [VERIFIED by measurement].
  This is small and is part of the 907 MB install; it cannot be removed via Blender's UI.
- Blender 5.2 also moved asset library configuration to a **dedicated Asset Libraries preferences page**
  and the library list now includes *"All Libraries"* and *"Essentials"* entries [VERIFIED, 5.2 assets notes].
- **Optional asset libraries can be skipped entirely.** They are user-configured paths, not part of the install.
  The 4.2 release notes describe the model: most add-ons *"that used to ship with Blender, are now available on
  the Extensions Platform"*, browsed and installed on demand [VERIFIED].
- **Remote Asset Libraries (5.2) directly address the low-disk case** — see section 4.

---

## 4. Blender "Remote Asset Libraries"

### 4.1 The blog post exists [VERIFIED]

**"Remote Asset Libraries" — Blender Developers Blog, by Julian Eisel, July 22nd, 2026.**
URL: **https://code.blender.org/2026/07/remote-asset-libraries/**

(The task asked me to say plainly if I could not find it. I found it, and it is dated exactly in the stated
window. It is categorised "General Development" and links to companion notes at
https://notes.blender.org/s/rAgFm9k1bs.)

### 4.2 What the feature is [VERIFIED — quoted]

> "Remote Asset Libraries let Blender discover assets stored on remote servers and **download them only when
> needed**. This enables integrated support for online asset services, better sharing of libraries, and an
> extended *Essentials* library **while keeping Blender fully usable offline**."

> "This is an important step towards the long-term goals of Blender's asset system ... where online asset
> services integrate directly into Blender's built-in asset features, instead of every add-on implementing its own."

### 4.3 Which Blender version, and is it experimental? [VERIFIED — shipped in 5.2 LTS, not experimental]

- **Shipped in Blender 5.2 LTS.** The blog states: *"Blender 5.2 LTS expands the *Essentials* library with
  optional online content including base meshes, materials, high-resolution HDRIs, compositing effects and more,
  **without increasing Blender's download size.**"*
- Confirmed in the 5.2 release notes, [5.2/assets.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.2/assets.md):
  > "**Online Asset Libraries** — It is now possible to register remotely hosted asset libraries, browse them
  > from within Blender, and download assets as needed. This requires *Allow Internet Access* to be enabled in
  > the Preferences."
  > "**Online Essentials** — The *Essentials* asset library that comes with Blender was extended with a number
  > of online hosted assets."
- **Is it experimental? [VERIFIED — no.]** There is no "experimental"/"beta" label on it in the 5.2 release
  notes, the manual, or the blog. It is a normal, documented 5.2 LTS feature. It is **opt-in by enabling
  *Allow Internet Access***, which is a privacy/network switch rather than an experimental flag.
- **Available in 5.2 specifically: yes.** The blog and both the 5.2 manual pages cite
  `docs.blender.org/manual/en/5.2/...` as the reference documentation, and the manual page exists for 5.2.
- The feature was blogged **July 22, 2026** — eight days after the 5.2 LTS release on **July 14, 2026**.

### 4.4 How it works [VERIFIED — quoted from the manual]

Manual: https://docs.blender.org/manual/en/5.2/files/asset_libraries/remote_asset_libraries.html
(raw source: https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/files/asset_libraries/remote_asset_libraries.rst)

**Download on demand:**
> "Assets can be downloaded from wherever they are shown, for example:
> - Asset Browser: right-click and choose "Download Asset".
> - Asset Shelf: click the download button shown when you hover the mouse over the asset.
> - 'Add' menu for Compositor Nodes: right-click the menu item for the asset, and choose 'Download Asset'."

**Caching behaviour:**
> "Assets are downloaded to the **local cache directory**. They are typically not meant for editing, as they are
> typically stripped down of all niceties to make the download as small as possible. To browse the asset cache,
> for example to **remove asset files you once downloaded but no longer want**, right-click on an asset in the
> Asset Browser and choose 'Open File Location'."

From the asset-library introduction page:
> "Downloaded assets are stored in Blender's local cache so they only need to be downloaded once. If an asset has
> already been downloaded, Blender will reuse the cached copy instead of downloading it again."

**Listing refresh cadence** (blog): *"When internet access is enabled, the remote assets listings will
automatically be updated once per day."*

**Offline behaviour** (blog):
> "Disabling *Allow Internet Access* disables all remote asset libraries. Asset Browsers and Asset Shelves also
> provide an *Offline Only* filter to show only locally available assets. To make a remote library available
> offline, open it in the Asset Browser, press *A* to select all assets, then choose *Download Assets* from the
> context menu. Once downloaded, assets can be accessed fully offline too, even with *Allow Internet Access* disabled."

**Hosting** (blog + manual, [Remote Asset Libraries: Creating & Hosting](https://notes.blender.org/p/8x7VqWQAZ9)):
- No special server software: *"No special server software is required; a standard HTTP server is sufficient."*
- A library is JSON listings + exported WebP/PNG previews + `.blend` files.
- Generator CLI: `blender -c asset_listing generate /path/to/asset-library` (blog shows `blender -c asset_listing generate /home/myname/my_library`; manual shows `blender -b -c asset_listing generate .`).
- Web server requirements: must send `Content-Length`, and *"Ignore query string parameters when serving static files"*; conditional requests (`ETag`/`Last-Modified`) *"highly recommended"* to make the daily listing sync cheap.
- Optional `access token` per library for authenticated services.
- Version targeting: an asset can be superseded for a given Blender version by naming the file e.g.
  `my_asset@b5_3.blend`.

**Known limitations [VERIFIED — quoted]:**
> "- Each `.blend` file should be **independent**. Any external dependency, such as `.png` files for textures,
> must be packed into the blend file. ... **importing any single asset from that file requires downloading the
> entire file.**"
> "- Blender does not have the concept of **asset versions**. This means that after downloading an asset,
> Blender can only detect whether the remote library has the same or a different file. It could be an updated
> version, or they may have rolled back to an older version. ... The only thing Blender knows is whether they are
> the same or not."

There is also an **open bug**, filed 2026-09-08: **#163648 "Remote Asset Library never Append (always Pack)"** —
i.e. remote assets may currently always pack rather than append, which matters for `.blend` growth
([issue](https://projects.blender.org/blender/blender/issues/163648)). And **#162741 "Asset Libraries: Multi-File
Support"** (2026-08-17) tracks the self-contained-file limitation.

### 4.5 Does it genuinely help a LOW-DISK setup? [assessed]

**Partly — and only if you are disciplined. It is not a pure win.**

**Where it genuinely helps [VERIFIED]:**
1. **It does not increase the installer size.** The blog is explicit: the online Essentials content ships
   *"without increasing Blender's download size."* The bundled Essentials library is 12 MB and stays 12 MB.
2. **Nothing is downloaded until you ask for it.** Download is a per-asset explicit action. A Blender install
   with no remote libraries touched costs zero extra bytes.
3. **You can delete what you downloaded.** The manual explicitly documents removing cached assets via
   *'Open File Location'*, and notes *"They are typically not meant for editing, as they are typically stripped
   down of all niceties to make the download as small as possible"* — so cached assets are small by construction.
4. **Offline mode is a first-class citizen** — you lose nothing locally by never enabling it.

**Where it does NOT help / the catch [VERIFIED and INFERENCE]:**
1. **It still caches everything locally — it is "download-on-demand", not "stream-from-remote".**
   Once downloaded, an asset lives in the local cache *"so they only need to be downloaded once"* and is
   *"reused"* rather than re-fetched. There is **no streaming, no automatic eviction, no LRU trim, and no
   on-demand re-fetch** — you must manually find and delete cached files. **[VERIFIED]** by the absence of any
   such mechanism in the manual and blog, both of which document manual removal as the way to reclaim space.
2. **The daily listing sync writes to disk** — listing JSON files are downloaded and cached, and are not
   expected to be cleared by the OS.
3. **A graceful degradation you cannot control:** the *"global"* `Download Assets` gesture the blog recommends
   for offline use downloads an **entire library** at once. If you use that, you have just recreated the large
   local footprint the feature was meant to avoid. Likewise, downloading one asset from a multi-asset `.blend`
   fetches the whole file.
4. **[INFERENCE] The real risk is the Online Essentials library in the Asset Browser.** These assets appear
   *"together with other essentials assets"* (5.2 release notes) whenever internet access is on. Browsing a
   HDRIs category and clicking download puts a *"high-resolution HDRI"* on disk — the single worst asset class
   for disk footprint. There is no documented size cap. On a genuinely tight disk, leaving
   *Allow Internet Access* **off** is the safe configuration; the feature is then inert and costs nothing.

**Bottom line [INFERENCE]:** Remote Asset Libraries are the right feature for a low-disk Mac *because* they move
the default from "ship/host a big library locally" to "fetch individual assets, cached, deletable". But they are
a **discipline-dependent** saving, not an architectural one: nothing stops a user from filling the cache, and
nothing prunes it for them. The unconditional wins are (a) the installer stays ~330 MB / ~907 MB installed, and
(b) a fully offline Blender remains completely functional.

---

## Summary answers

1. **Versions:** current stable **5.2 LTS** (5.2.2, 2026-09-15; LTS until July 2028); other maintained LTS
   **4.5 LTS** (4.5.14); next in development **5.3 (alpha)**, ~November 2026.
2. **Metal:** default GPU backend on macOS since **Blender 3.5** (commit 2023-02-20). Cycles Metal on Apple
   Silicon is **production-ready** — the 5.2 manual documents it as a normal backend, lists GPU-accelerated
   ray tracing and denoising, and **never calls it experimental**. It is not bug-free: live Metal issues were
   discussed on 2026-09-15.
3. **EEVEE** works on Apple Silicon via Metal. Its quantified weakness is **cold shader compilation**:
   37.20 s vs 11.67 s (Vulkan) on the Blender 5.1 `barbershop_interior` test on an **M1 Ultra** — but warm
   compilation on Metal is the fastest of the backends (2.72 s).
4. **M1 performance:** Open Data median scores (4.5.0, n=27 for the M1) — **Apple M1 (8-core GPU) 260.4** vs
   **NVIDIA RTX 3080 4529.2**, i.e. the M1 is **≈17× slower**. Fallback rendering: **yes**, viable; not fast.
5. **Authoring on M1/16 GB:** works, with a real ceiling — smooth to **~3 M polygons** in sculpt, degrading and
   eventually OOM-killing at ~6 M; the bottleneck is RAM, not CPU. Blender 5.2's **Cycles Texture Cache** and
   **EEVEE instancing optimisations** are the two features that most improve this; the texture cache trades disk
   for RAM.
6. **Disk:** measured **907 MB installed** from a **330 MB DMG** (5.2.2 macOS arm64). Portable install =
   create `portable/` inside `Blender.app/Contents/Resources`. Config at
   `~/Library/Application Support/Blender/5.2/`. Bundled Essentials library = 12 MB.
7. **Remote Asset Libraries:** real, blogged **2026-07-22**, shipped in **5.2 LTS**, not experimental,
   download-on-demand with a **local cache that is never auto-evicted**. Genuinely helps low-disk setups because
   it adds nothing to the installer and downloads per-asset — but it caches locally and requires manual cleanup.

## The three things I could not verify

1. **Per-scene Open Data breakdown** (monster / junkshop / classroom separately) — the query API exposes only
   `compute_type`/`device_name`/`operating_system`/`blender_version` groupings. Settle it by downloading the CC0
   daily dataset snapshot from https://opendata.blender.org/download/.
2. **Viewport FPS for an engineering scene on M1 16 GB** — no source. Settle it by measuring on the actual
   scene, ideally using the 3D viewport performance timing overlay added in Blender 5.1.
3. **A documented Metal/VRAM limit figure on 16 GB Apple Silicon** — no official Blender source. Settle it by
   querying `MTLDevice.recommendedMaxWorkingSetSize` / `sysctl iogpu.wired_limit_mb` on the machine itself.
   Any "10.67 GB default VRAM limit" figure should be treated as **UNVERIFIED**.
