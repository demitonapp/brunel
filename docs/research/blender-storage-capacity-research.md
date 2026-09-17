# Blender Rendering Pipeline — Realistic File Sizes for Capacity Planning

Research date: **September 2026**. Current Blender release: **5.2.2 LTS, released 15 September 2026** ([blender.org/download](https://www.blender.org/download/)).

Convention used below:
- **[VERIFIED]** = exact figure quoted from the linked source.
- **[INFERENCE]** = my arithmetic or extrapolation, not a published figure.
- **[LOW]** = weak/indirect evidence.
- **[NOT FOUND]** = no hard data located; the measurement that would settle it is stated.

Pixel-count arithmetic used throughout:
- 1080×1920 = **2,073,600 px**
- 3840×2160 (4K) = **8,294,400 px** — exactly **4×** the 1080×1920 pixel count.

---

## 1. Rendered image frame sizes

### 1.1 Format definitions (verified)

| Fact | Value | Source |
|---|---|---|
| OpenEXR `HALF` channel | 16-bit floating point = **2 bytes/channel/pixel** | [openexr.com Technical Introduction](https://openexr.com/en/latest/TechnicalIntroduction.html) |
| OpenEXR `FLOAT` / `UINT` | 32-bit = **4 bytes/channel/pixel** | same |
| OpenEXR lossless compression, photographic | shrinks to **35–55 %** of uncompressed | [openexr.com](https://openexr.com/en/latest/TechnicalIntroduction.html): *"photographic images with significant amounts of film grain tend to shrink to somewhere between 35 and 55 percent of their uncompressed size."* |
| Blender EXR codecs | ZIP = Zlib on 16-row blocks; PIZ = lossless wavelet, *"effective for noisy/grainy images"*; B44 = *"fixed 2.3:1 ratio"*; ZIPS; RLE; DWAA/DWAB/Pxr24 lossy | [Blender Manual — Supported Image Formats](https://docs.blender.org/manual/en/latest/files/media/image_formats.html) |
| Blender PNG | 8 or 16 bit, alpha supported, lossless | same |
| PNG format | lossless only (no quality/ratio guarantee) | [W3C PNG spec / PNG](https://en.wikipedia.org/wiki/Portable_Network_Graphics) |

### 1.2 Uncompressed arithmetic [INFERENCE, arithmetic only]

| Output | bytes/px | 1080×1920 | 4K (3840×2160) |
|---|---|---|---|
| PNG 8-bit RGBA | 4 | 8,294,400 B = **8.29 MB** | 33,177,600 B = **33.18 MB** |
| OpenEXR half RGBA (4 ch) | 8 | **16.59 MB** | **66.36 MB** |
| OpenEXR half RGBA + Z as float32 | 12 | **24.88 MB** | **99.53 MB** |
| OpenEXR half RGBA + Z as half | 10 | **20.74 MB** | **82.94 MB** |
| Multilayer (see 1.4) | 110 | **228.10 MB** | **912.38 MB** |

### 1.3 Realistic compressed sizes

| Output | 1080×1920 realistic | 4K realistic | Basis |
|---|---|---|---|
| PNG 8-bit RGBA | **3–8 MB** [LOW/INFERENCE] | **12–30 MB** [LOW/INFERENCE] | lossless only; ratio depends on noise. **[NOT FOUND]** any official/benchmarked ratio for photographic PNG. Measurement: render 20 varied frames, `du -b`, average. |
| OpenEXR half RGBA | 6–9 MB [INFERENCE] | 23–37 MB [INFERENCE] | 35–55 % of raw (OpenEXR doc) |
| OpenEXR half RGBA + Z float | 9–14 MB [INFERENCE] | 35–55 MB [INFERENCE] | 35–55 % of raw |
| OpenEXR half RGBA + Z float (real-world anchor) | ~12 MB [INFERENCE from VERIFIED 2K figure] | — | FFmpeg VFX wiki: *"a 16bit EXR is about 14MB in size"* for 2K (2048×1152) — [trac.ffmpeg.org/wiki/Encode/VFX](https://trac.ffmpeg.org/wiki/Encode/VFX). Scaled to 2.07 Mpx ≈ 12 MB. |
| Vendor rule of thumb, 16-bit half at 4K | — | **10–25 MB** [LOW] | [vfxrendering.com EXR page](https://vfxrendering.com/best-render-farm-for-exr-rendering-high-dynamic-range-vfx-on-cloud/) |
| Vendor rule of thumb, 32-bit beauty at 4K | — | **20–50 MB** [LOW] | same |

### 1.4 Multilayer EXR — the important one

**Channel model for the pass list you specified** [INFERENCE]:
Combined RGBA (4) + Diffuse Direct/Indirect/Color (9) + Glossy (9) + Transmission (9) + Emission (3) + Environment (3) + Shadow (3) + AO (3) = **43 half channels**, plus Mist (1 float32), Denoising Normal + Albedo (6 half), Denoising Depth (1 float32), Z (1 float32) = **6 half + 3 float32**.

Totals: **49 half channels (98 B/px) + 3 float32 channels (12 B/px) = 110 bytes/pixel uncompressed.**

| | 1080×1920 | 4K |
|---|---|---|
| Uncompressed | **228 MB** | **912 MB** |
| at 15 % of raw (flat/black passes compress away) | 34 MB | 137 MB |
| at 35 % of raw | 80 MB | 319 MB |
| at 55 % of raw (noisy, dense passes) | 126 MB | 502 MB |

**Real reports:**
- **[VERIFIED]** kkar, Blender Artists, Sept 2021 — same half-float multilayer frame written with 8 codecs: B44 **346,789 KB**, B44A **260,472 KB**, RLE **219,562 KB**, PIZ **185,234 KB**, ZIP **135,049 KB**, ZIPS **134,723 KB**, Pxr24 **98,797 KB**, DWAA **89,051 KB** ([blenderartists.org/t/multilayer-exr-file-sizes-chart/1325498](https://blenderartists.org/t/multilayer-exr-file-sizes-chart/1325498)). Resolution and pass count were **not stated** — this is the main weakness of this data point. Using the manual's verified B44 = 2.3:1 rule, the implied uncompressed size of that frame is **~817 MB**, and the same frame came out at **17 % (ZIP), 23 % (PIZ), 11 % (DWAA)** of uncompressed. That is much better than the 35–55 % photographic figure because most passes are flat or black.
- **[VERIFIED]** Blender Artists, April 2023 — *"just did a test on a 30 frame animation, file size for all multilayer-exr's = 506mb (grant it has all the cryptomatte info) and for what i posted here saved as none-multilayer exr's = 70mb (all the same passes, but only two selected cryptomattes)."* → **16.9 MB/frame multilayer** ([blenderartists.org/t/1458370](https://blenderartists.org/t/mist-light-glossy-etc-passes-how-do-you-work-with-them-addon-opinions-insight/1458370), post 6). Resolution not stated.
- **[LOW]** Vendor: *"With 12 AOVs in multi-channel EXR: 80–150 MB per frame"* at 4K ([vfxrendering.com](https://vfxrendering.com/best-render-farm-for-exr-rendering-high-dynamic-range-vfx-on-cloud/)).
- **[VERIFIED]** Blender caps the *uncompressed* size of an EXR it will write: *"It used to be 32G but was increased to 80G in version 4.4"*, and a default-ish file was described as *"30000x38000, 19-channel float"* ([blender.stackexchange.com/q/339393](https://blender.stackexchange.com/questions/339393)). Confirms both the many-channel reality and a hard per-frame ceiling.

**Answer for a 4K multilayer frame with your pass set: plan 150 MB – 1.0 GB per frame, typical ~300–500 MB** [combined VERIFIED anchors + INFERENCE]. For 1080×1920 the same setup is **~40–250 MB, typical ~80–130 MB**. The dominant variable is not resolution but how much of each pass is non-black (a shadow or AO pass on a mostly-empty frame compresses to near nothing; a noisy transmission pass does not).

---

## 2. Mantaflow fluid (FLIP) and smoke cache size

### 2.1 Where the cache lives and what controls size [VERIFIED]

Blender Manual, Fluid Domain → Cache ([docs.blender.org/manual/en/latest/physics/fluid/type/domain/cache.html](https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/cache.html)):
- *"Inside this directory each simulation type (i.e. mesh, particles, noise) will have its own directory containing the simulation data."*
- Format **Uni Cache**: *"Each simulation object is stored in its own `.uni` cache file."*
- Format **OpenVDB**: *"All simulation objects (i.e. grids and particles) are stored in a single `.vdb` file per frame."*
- Compression: **Zip** (effective but slower), **Blosc** (*"Multi-threaded... similar in size and quality to Zip"*), **None**.
- Precision: **Full** (32-bit), **Half** (16-bit), **Mini** (8-bit where possible).
- **Resumable**: *"Extra data will be saved so that you can resumed baking... recommended to avoid enabling this option when baking at high resolutions."*

Blender's temporary directory (used for *"render layers, physics cache, copy-paste buffer and crash logs"* if the cache path is left at default) is documented at [Blender's Directory Layout](https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html#temp-dir). Users report real cache layouts as `cache_fluid/particles/*.vdb`, and `<sim>-cache/data/*.vdb` with `<sim>-cache/config/*.uni` ([blender.stackexchange.com/q/317303](https://blender.stackexchange.com/questions/317303/render-liquid-fluid-simulation-scene-with-low-disk-space); [blender.stackexchange.com/q/277778](https://blender.stackexchange.com/questions/277778/is-it-possible-to-repeatedly-loop-through-cache-data)).

### 2.2 Real measured numbers

| Measurement | Value | Per frame | Source / confidence |
|---|---|---|---|
| Mantaflow **liquid with particles enabled**, low domain resolution — *"Each frame of fluid simulation takes about 3 GB of disk space at a low domain resolution, with the majority caused by `cache_fluid/particles/*.vdb`"*; 100 GB ⇒ ~35 frames | **~3 GB/frame** | 3 GB | [SE q/317303](https://blender.stackexchange.com/questions/317303/render-liquid-fluid-simulation-scene-with-low-disk-space) (Apr 2024) — **[VERIFIED]**, single user, particles dominate |
| Mantaflow **liquid**, 115 frames baked ⇒ *"50GB of cache"* | **50 GB / 115 frames** | **~435 MB/frame** | [blenderartists.org/t/mantaflow/1318962](https://blenderartists.org/t/mantaflow/1318962) (Jul 2021) — **[VERIFIED]** |
| Legacy (pre-Mantaflow) fluid, final resolution 200, 1000 frames; `/tmp/blender_lFkZps/` = **179 G** | 179 GB total | ~179 MB/frame avg (cache **plus** render temp) | [SE q/53178](https://blender.stackexchange.com/questions/53178/understanding-fluid-dynamics-ridiculously-large-tmp-folder) (2016) — **[VERIFIED]**; old solver, folder contains more than just cache |
| Vendor estimate, Mantaflow fire, 200 frames | **5–30 GB** | 25–150 MB/frame | [vfxrendering.com Mantaflow page](https://vfxrendering.com/best-render-farm-for-blender-smoke-and-fire-mantaflow-simulation-on-cloud/) — **[LOW]**, marketing/SEO page |

### 2.3 Multipliers (the levers that actually matter) — [VERIFIED]

From Gordon Brinkmann, Blender Stack Exchange ([answer 288520 to q/288475](https://blender.stackexchange.com/questions/288475), accepted):
- Smallest cache: **OpenVDB + Blosc + Half** precision.
- *"enabling [Is Resumable] also makes the smoke cache more than twice as big as without it."* → **>2×**
- *"a smoke cache with noise is easily 2.5 times larger than without noise."* → **~2.5×**
- *"Doubling the divisions results in quadrupling the smoke voxels (but fortunately just about tripling the smoke cache size)."* → **~3×** (his empirical figure; the pure cubic expectation is 8× voxels, so treat his voxel wording as approximate)
- Adaptive Domain reduces cache; Dissolve reduces cache; open boundaries reduce cache.

### 2.4 250-frame shot totals

| Scenario | Per frame | 250 frames |
|---|---|---|
| Smoke/fire VDB, moderate res, defaults | 25–150 MB [LOW] | **6–38 GB** |
| Mantaflow liquid, no particles (2021 measurement) | ~435 MB [VERIFIED] | **~109 GB** |
| Mantaflow liquid + particles, low res (2024 measurement) | ~3 GB [VERIFIED] | **~750 GB** |

**Bottom line:** a 250-frame shot is *not* a single number. It is ~10 GB for a modest smoke plume and ~0.75 TB for a particle-heavy FLIP liquid. Budget caches per shot, not per project.

---

## 3. OpenVDB smoke/volume size

### 3.1 Why VDB is sparse [VERIFIED — openvdb.org]

From the [OpenVDB Overview](https://www.openvdb.org/documentation/doxygen/overview.html):
- *"OpenVDB is designed specifically to work efficiently with sparse volumetric data locally sampled at a high spatial frequency."*
- The tree is *"specially designed... given sparse unique values, minimizes the overall memory footprint."*
- Values exist as **voxel values**, **tile values** (a constant covering a whole node's block) and one **background value**; `prune` *"replaces with tile values any nodes that subsume voxels with the same values"*.
- Default leaf node = **8×8×8 voxels**; nodes subdivide index space with fixed branching factors.
- Grids support a **"save float as half"** setting so *"it can be written more compactly using 16-bit floating point values rather than full-precision values."*
- **Per-grid metadata stored in the file includes the active voxel count and the grid's memory usage in bytes**, retrievable without loading pixels.

**Consequence:** VDB size is proportional to the number of **active** voxels (the narrow band where smoke exists), not to the domain bounding box. An empty region costs one tile value, not N³ floats. This is why a VDB sequence can be far smaller than a naive full-grid calculation.

### 3.2 Scaling with voxel resolution

| Claim | Value | Status |
|---|---|---|
| Cubic scaling (2× resolution on each axis) | 8× voxels | [INFERENCE], geometry |
| User-measured smoke cache scaling | *"Doubling the divisions results in quadrupling the smoke voxels (but fortunately just about tripling the smoke cache size)"* | [VERIFIED quote], empirical, [LOW] precision — [SE 288520](https://blender.stackexchange.com/questions/288475) |
| Half vs Full precision | ~50 % of the data (16-bit vs 32-bit) | [VERIFIED mechanism] from manual: Precision Full/Half/Mini ([cache.rst](https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/cache.html)) |
| Adaptivity | active-voxel fraction, not domain size, sets size | [VERIFIED mechanism] openvdb.org overview |

My worked estimate for a Blender gas domain [INFERENCE]: a cube at resolution N carries on the order of 6–8 float32 grids (density, heat, fuel, flame, velocity XYZ). At N=128 that is ~2.1 M voxels × 4 B × 7 ≈ **59 MB/frame uncompressed**; with Half precision and Blosc, and a realistic 10–50 % active fraction, expect roughly **15–60 MB/frame**. At N=256 the same model gives ~**100–470 MB/frame**. Do not treat these as measured.

### 3.3 Real numbers

No independent, published, per-frame Blender smoke `.vdb` benchmark was found. **[NOT FOUND]** — flagged LOW. The measured numbers in §2.2 are the best available, and when Format = OpenVDB those caches *are* `.vdb` files (manual: one `.vdb` per frame). The vendor figure of **5–30 GB per 200-frame fire** (25–150 MB/frame) is the only sequence-level VDB figure located and is **[LOW]**.

**Measurement that would settle it:** bake one production smoke shot at three resolutions (e.g. 64/128/256 divisions) with OpenVDB + Blosc + Half, no Noise and then with Noise, `du -sb` the `data/` folder each time, and record frames. That gives real per-frame MB and the empirical resolution exponent in about an hour.

---

## 4. Blender install + project disk footprint

### 4.1 Official download sizes — [VERIFIED]

From [blender.org/download](https://www.blender.org/download/) (Blender **5.2.2 LTS**, 15 September 2026):

| Package | Size |
|---|---|
| Windows x64 installer (`.msi`) | **348 MB** |
| Windows ARM64 installer (`.msi`) | **227 MB** |
| **Windows portable (`.zip`)** | **386 MB** |
| Windows ARM64 portable (`.zip`) | **261 MB** |
| macOS Apple Silicon (`.dmg`) | **330 MB** |
| Linux x64 (`.tar.xz`) | **366 MB** |
| Source code | 89 MB |
| Source + libraries | 1.7 GB |

**Installed / extracted size:** no official figure is published ([NOT FOUND] on both [blender.org/download/requirements](https://www.blender.org/download/requirements/) and the manual install pages). Best available measured data point: Blender **3.5.1 uncompressed is roughly 1250 MB** on Linux, broken down as *executable 250 MB, `lib/` 315 MB, `<version>/python` 280 MB* for the official release ([SE q/293513 "Taming big bad Blender"](https://blender.stackexchange.com/questions/293513/taming-big-bad-blender)) — **[VERIFIED]** for 3.5.1. **Extrapolating to 5.2.2: expect ~1.2–1.6 GB installed** on Windows/macOS/Linux [INFERENCE].

### 4.2 Portable install — [VERIFIED, official]

[Blender's Directory Layout → Portable Installation](https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html#portable-installation):

> *"To enable this, create a folder named `portable` at the following locations: Windows: Next to the Blender executable, in the unzipped folder; Linux: Next to the Blender executable, in the unzipped folder; macOS: Inside the application bundle at `Blender.app/Contents/Resources`. This folder will then store preferences, startup file, installed extensions and presets."*

Also official: the `BLENDER_USER_RESOURCES` environment variable *"can be set to a custom directory to replace the default user directory."* System paths are overridable with `BLENDER_SYSTEM_SCRIPTS` / `BLENDER_SYSTEM_EXTENSIONS` / other `BLENDER_SYSTEM_*` variables.

Note: the current (5.2) manual documents **`BLENDER_USER_RESOURCES`** as the single user-directory override. The older per-area variables `BLENDER_USER_CONFIG` / `BLENDER_USER_SCRIPTS` / `BLENDER_USER_DATAFILES` are **not** listed on that page in 5.2 — do not build a workflow on them without testing.

[blender.org/download/requirements](https://www.blender.org/download/requirements/) confirms the design intent: *"No installation needed, no Internet connection required. Truly portable, take it with you wherever you go!"* and links that manual section.

**Space needed for portable mode:** the extracted zip (~1.2–1.6 GB [INFERENCE]) plus whatever the user config, extensions and asset libraries add. A 4–8 GB USB stick is comfortable.

### 4.3 Default user / cache directories — [VERIFIED]

| Path | Windows | macOS |
|---|---|---|
| User config, startup, extensions, presets | `%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\<version>\` | `/Users/$USER/Library/Application Support/Blender/<version>/` |
| Local cache (asset-library indexing) | `%USERPROFILE%\AppData\Local\Blender Foundation\Blender\Cache\` | `/Library/Caches/Blender/` |
| System/install dir | installer: `%ProgramFiles%\Blender Foundation\Blender\<version>\`; zip: `./<version>/` | `./Blender.app/Contents/Resources/<version>/` |

Source: [Blender's Directory Layout](https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html). The **temporary directory** (render layers, physics cache, crash logs) is chosen from Preference → File Paths, then `TEMP`, then `/tmp/`.

### 4.4 Asset libraries / asset bundle — [VERIFIED]

- The built-in **Essentials** asset library ships with Blender and provides *"assets that are included with Blender"*; an **"Include Online Essentials"** toggle adds *"additional assets hosted online"* and requires Online Access ([manual: Asset Libraries](https://docs.blender.org/manual/en/latest/editors/preferences/asset_libraries.html)). So: **core Essentials = part of the install (not separable); online extras = optional.**
- Essentials live under the install's `datafiles/assets/` (e.g. `blender/4.3/datafiles/assets/brushes`) — user report with official path layout: [blenderartists.org/t/1577011](https://blenderartists.org/t/essentials-asset-library-fully-missing-debian-sid/1577011) + [directory layout](https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html). **[LOW]** for the exact sub-path.
- **Downloadable asset bundles are optional and separately sized** ([blender.org/download/demo-files](https://www.blender.org/download/demo-files/)): Human Base Meshes v1.4.1 **49 MB**, Ellie Pose Library v2.0.0 **24 MB**, Cube Diorama **11 MB**. The old "Blender Asset Bundle" concept still surfaces as these per-bundle downloads.
- Demo splash `.blend` files on the same page range from 7 MB to 1.4 GB (e.g. Blender 5.2 Panthera Spelaea 141 MB, Blender 5.1 Singularity 670 MB). These are optional and are *not* installed with Blender.
- **[NOT FOUND]**: an official size for the bundled Essentials library. It is included in the download/install size above; that is the number to plan with.

### 4.5 Typical project directory

No official figure exists. [INFERENCE] breakdown for a solo vertical-video project:

| Component | Typical size |
|---|---|
| `.blend` file (no packed sims) | 5–150 MB |
| `.blend` backups (`blend1`, etc.) | ~2× the blend |
| Textures (4K PBR sets, 20–40 maps) | 100 MB – 1 GB |
| Reference / stock footage | 0.5–5 GB |
| Fluid/smoke cache | 0.5 GB – 750 GB (see §2) |
| Rendered frames | 0.75 GB (PNG) – 100 GB+ (multilayer EXR) |
| Deliverable masters | 1–3 MB per finished second |
| Proxies/previews | ~10–20 % of source |

---

## 5. Storage budget — solo Reels creator, Cycles on RTX 3080, Mac with 23 GB free

### 5.1 Explicit assumptions

1. Deliverables are **1080×1920, 30 fps, 10–30 s**; 20 reels/month averaging 20 s = **400 finished seconds = 12,000 frames/month**.
2. Deliverable frames are **PNG 8-bit RGBA at 4 MB/frame** (mid of the 3–8 MB inference band, §1.3).
3. Renders happen on the **Windows/RTX 3080** box; Blender's temp dir and cache dir are both pointed at the Windows NVMe.
4. The **Mac is a control/edit surface only** — it must never hold caches or frame sequences.
5. Masters: H.264/H.265 at ~**1.5 MB per finished second** [INFERENCE].
6. Of ~12 re-rendered shots in a month, **2 are multilayer-EXR hero shots** (120 MB/frame) and **2 use smoke VDB** (150 MB/frame upper band), **1 uses FLIP liquid** (435 MB/frame).
7. Renders are archived to external storage and pruned from the Windows NVMe after delivery.

### 5.2 Per-second-of-finished-video

| Stream | Per finished second (30 frames) |
|---|---|
| PNG deliverables @4 MB | **120 MB/s** |
| Single-layer half EXR RGBA+Z @12 MB | **360 MB/s** |
| Multilayer EXR @120 MB | **3.6 GB/s** |
| Video master @1.5 MB/s | **1.5 MB/s** |

Caches are **per shot, not per second** — see below.

### 5.3 Per 250-frame shot (~8.3 s at 30 fps)

| Component | 250 frames |
|---|---|
| PNG deliverable frames | **~1.0 GB** |
| Single-layer half EXR (RGBA+Z) | **~3.0 GB** |
| Multilayer EXR (your pass list, mid estimate) | **~30 GB** (range 10–60 GB) |
| Smoke VDB cache | **6–38 GB** |
| FLIP liquid cache (no particles) | **~109 GB** |
| FLIP liquid + particles | **~750 GB** |

### 5.4 Monthly budget (assumptions of §5.1)

| Line item | Size |
|---|---|
| Deliverable PNGs (12,000 frames × 4 MB) | 48 GB |
| Single-layer EXR for 12 shots × 250 frames | 36 GB |
| 2 multilayer hero shots × 250 frames @120 MB | 60 GB |
| 2 smoke VDB shots × 250 frames @150 MB (upper band) | 75 GB |
| 1 FLIP liquid shot × 250 frames @435 MB | 109 GB |
| Masters + project + textures + previews | 5–15 GB |
| **Total, typical month** | **~160–220 GB** |
| **Total, heavy month (liquid + multilayer + 4K)** | **~300–350 GB** |

A 4K month multiplies the frame-based lines ×4 (PNG 12–30 MB, multilayer 150 MB–1 GB per frame), so a heavy 4K month is comfortably **0.5–1 TB**.

### 5.5 Recommended layout

| Location | What lives there | Budget |
|---|---|---|
| **Mac (23 GB free)** | `.blend` project files, scripts/add-ons, reference, **H.264/ProRes-proxy review copies**, final deliverable masters. **No caches, no EXR/PNG sequences.** | **keep under 15 GB** (leave ~8 GB headroom) |
| **Windows box — NVMe (internal)** | Active `.blend` working copies; Blender temp dir and cache dir on this drive; VDB/FLIP caches for in-flight shots; live render output; preview encodes. | **1 TB NVMe** (peaks: ~110 GB for a FLIP shot, ~75 GB for smoke, ~60 GB of multilayer EXR) |
| **External USB-C SSD/NVMe** | Archive of raw PNG/EXR sequences, cache snapshots for hero shots, versioned `.blend` backups, masters, asset libraries. | **4 TB** (~18–24 months at 160–220 GB/month) |
| **Cloud/offsite (optional)** | Finished masters + project `.blend` only (small). | <10 GB/month |

Operational rules that follow from the numbers:
- Never let Blender's temp/cache dir sit on the Mac or on the boot SSD — set Preference → File Paths → Temporary Files and the fluid Cache Directory to the big NVMe ([temp-dir doc](https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html#temp-dir)).
- For fluid/smoke shots use **OpenVDB + Blosc + Half**, leave **Is Resumable off** (>2× saving) and **Noise off during iteration** (~2.5×) — [SE 288520](https://blender.stackexchange.com/questions/288475).
- For 4K hero shots, do **not** default to multilayer EXR for every frame: write beauty as single-layer (or PNG) and multilayer only for the frames that need it, or split passes into separate files as the Blender Artists workflow did (506 MB → 70 MB for a 30-frame test, §1.4).
- Move caches and frame sequences off the Windows NVMe to external storage on a per-shot basis; the 1 TB internal is a working set, not an archive.

---

## Confidence summary

| Claim | Confidence |
|---|---|
| Blender 5.2.2 LTS download sizes; portable-mode mechanism and paths; directory layout; asset-bundle optionality | **HIGH — official** |
| OpenEXR HALF/FLOAT byte sizes and 35–55 % lossless ratio; Blender EXR codec definitions incl. B44 2.3:1 | **HIGH — official** |
| kkar multilayer codec-size chart and the 30-frame multilayer/mono comparison | **HIGH that the reports exist; MEDIUM on absolute per-frame size (resolution unstated)** |
| FLIP liquid cache ~435 MB/frame (2021) and ~3 GB/frame with particles (2024); 179 GB legacy temp dir | **MEDIUM–HIGH — real user measurements, unspecified scene detail** |
| Smoke cache multipliers (Resumable >2×, Noise ~2.5×, ~3× per resolution doubling) | **MEDIUM — single expert answer, empirical** |
| Smoke VDB MB/frame and resolution exponent | **LOW — no published benchmark; model is INFERENCE** |
| PNG 1080×1920/4K file sizes | **LOW — INFERENCE from raw size; no benchmark found** |
| 4K multilayer EXR per-frame size | **MEDIUM — anchored by two real data points plus vendor estimate; resolution mismatch remains** |
| Monthly storage budget | **INFERENCE built on the above, with assumptions stated** |

### Measurements that would close the remaining gaps
1. Render 20 varied frames at each required size/format, `du -b` them, average — settles PNG and single-layer EXR in 30 minutes.
2. One multilayer 4K frame with the exact pass list at ZIP and PIZ, with the frame's resolution recorded — settles §1.4.
3. Bake one smoke shot at 64/128/256 divisions × (Half/Full) × (Blosc/Zip) × (Noise on/off), `du -sb` each `data/` folder — settles §3 with a real exponent.
