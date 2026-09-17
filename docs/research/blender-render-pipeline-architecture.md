# Blender Render Pass / Compositing Pipeline Architecture

Research report for a stylised engineering/historical animation production (Cycles, Blender 4.5 LTS or 5.x).
Every non-obvious claim carries a source URL. Where I am inferring rather than quoting, I mark
**[high] / [med] / [low]** confidence.

Method note: the Blender Manual is also available as plain reStructuredText, which is far denser than the
rendered HTML (whose navigation sidebar floods a fetch) and is the actual source of truth:

- 5.x (dev/`main`): `https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/<path>.rst`
- 4.5 LTS: `https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/<path>.rst`
  (branch name carries a `v`: `blender-v4.5-release`. Branch list:
  `https://projects.blender.org/api/v1/repos/blender/blender-manual/branches`)

---

## 0. Version map used throughout

| | 4.5 LTS | 5.0 | 5.1 | 5.2 | main (5.3dev) |
|---|---|---|---|---|---|
| Cycles denoise UI location | Render → Sampling → Denoising | same | same | same | same |
| Denoise `Quality` (High/Balanced/Fast) | yes (added 4.2) | yes | yes | yes | yes |
| `Use GPU` (denoise) | yes | yes | yes | yes | yes |
| Denoising Data passes | Noisy Image, Denoising Albedo, Denoising Normal | same | same | **+ Specular Albedo, Roughness, Depth** | same |
| Denoising Data on EEVEE | Cycles only | Cycles only | Cycles only | Cycles only | **Cycles + EEVEE** |
| `Render Time` debug pass | no | yes | yes | yes | yes |
| Depth pass UI label | `Z` | `Depth` | `Depth` | `Depth` | `Depth` |
| Bundled OpenImageDenoise | 2.3.3 | 2.5.0 (main) | — | — | 2.5.0 |
| Output `Media Type` (Image / Multi-Layer EXR / Video) | **no** | yes | yes | yes | yes |
| File Output node sidebar | Base Path / File Format + Slots | redesigned: Node Format, Images/Layers, Output Paths | same | same | same |
| Compositor `Composite` node | exists | **removed** → Group Output | Group Output | Group Output | Group Output |

Sources for the table: manual raw `.rst` diffs across branches
([4.5 passes](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/render/layers/passes.rst),
[main passes](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst),
[5.2 passes](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v5.2-release/manual/render/layers/passes.rst));
[5.0 compositor release notes](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.0/compositor.md);
[4.5 compositor release notes](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/4.5/compositor.md);
OIDN pins read from `build_files/build_environment/cmake/versions.cmake` per branch,
e.g. [4.5](https://raw.githubusercontent.com/blender/blender/blender-v4.5-release/build_files/build_environment/cmake/versions.cmake)
(`set(OIDN_VERSION 2.3.3)`) and
[main](https://raw.githubusercontent.com/blender/blender/main/build_files/build_environment/cmake/versions.cmake)
(`set(OIDN_VERSION 2.5.0)`; upstream repo moved `OpenImageDenoise/oidn` → `RenderKit/oidn`).

---

## A) TRANSPARENT FILM AND BACKGROUND COMPOSITING

### A.1 The `Transparent` checkbox — exactly what it does

- **Exact location:** `Render Properties → Film → Transparent`.
  Python: `bpy.types.RenderSettings.film_transparent`.
- **Manual wording (4.5 and 5.x identical):** *"Render the background transparent, for compositing the
  image over another background after rendering."*
  [4.5 film.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/render/cycles/render_settings/film.rst) ·
  [5.x film.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cycles/render_settings/film.rst)
- **RNA tooltip wording (slightly more precise):** *"World background is transparent, for compositing the
  render over another background"* —
  [`rna_scene.cc`](https://raw.githubusercontent.com/blender/blender/main/source/blender/makesrna/intern/rna_scene.cc).

What it actually does, per the manual + source:

1. **The world is excluded from the final render.** Manual, Environment pass description: *"When the Film is
   set to Transparent (meaning the world is excluded from the final render)…"* — [passes.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst). **[high]**
2. **Alpha is 0 where only the world would have been visible.** The manual does not spell out `alpha = 0`,
   but this is the definition of "transparent background" and is what every downstream workflow relies on
   (e.g. the Blender Artists thread where the user loses the starfield background the moment Transparent
   is checked, and regains it by compositing the Environment pass back in) —
   [Blender Artists 1622582](https://blenderartists.org/t/compositor-and-background-world-rendering/1622582). **[high]**
3. **RGB stays premultiplied.** The compositor reference states the invariant directly: *"For compositing and
   rendering, Premultiplied Alpha is the standard in Blender. Render layers will be premultiplied alpha, and
   images loaded into rendering or compositing will be converted to this."* — [Alpha Convert node](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/compositing/types/color/alpha_convert.rst).
   The Image Editor Alpha control also documents Premultiplied as *"The natural format for renders and used
   by file formats like OpenEXR"* — [image_settings.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/editors/image/image_settings.rst). **[high]**
   Practical consequence: object edges are correctly alpha-weighted with no white/black matte fringe bleeding
   into transparent pixels, so an Alpha Over straight onto a plate is correct with no fix-up.
4. **Legacy-implementation quirk worth knowing if you script it:** `film_transparent` is *defined in RNA as a
   boolean on the legacy `alphamode` bitfield, at bit `R_ALPHAPREMUL`*:
   `RNA_def_property_boolean_sdna(prop, nullptr, "alphamode", R_ALPHAPREMUL);` —
   [`rna_scene.cc`](https://raw.githubusercontent.com/blender/blender/main/source/blender/makesrna/intern/rna_scene.cc).
   So "Transparent" and "premultiply" share one legacy bit. Do not read this as "Transparent = premultiply
   disabled"; read it as "the flag is the historical premultiply/sky-alpha switch reused". **[high]** on the
   source fact, **[low]** on any inference about deep semantics from it.

Sibling controls in the same `Render → Film` panel (Cycles) — useful to set deliberately for a stylised look:

| Control | Python | Notes |
|---|---|---|
| `Exposure` | `CyclesRenderSettings.film_exposure` | *"works on the data"*, unlike the Color Management exposure which is on the view transform |
| `Pixel Filter → Type` | `CyclesRenderSettings.pixel_filter_type` | `Box` (no filter) / `Gaussian` / `Blackman-Harris` (default) |
| `Pixel Filter → Width` | `CyclesRenderSettings.filter_width` | lower = crisper |
| `Transparent Glass` | `CyclesRenderSettings.film_transparent_glass` | *"Render transmissive surfaces as transparent, for compositing glass over another background"* |
| `Roughness Threshold` | `CyclesRenderSettings.film_transparent_roughness` | keep glass above this roughness opaque |

Source: [film.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cycles/render_settings/film.rst).

### A.2 Compositing a background plate later — Alpha Over, and premultiplied vs straight

**Node:** `Compositor → Color → Alpha Over` (`bpy.types.CompositorNodeAlphaOver`).

**Input/property names differ between 4.x and 5.x — this is the single most common source of confusion:**

| | 4.5 LTS and earlier | 5.0+ |
|---|---|---|
| Menu path | Compositor → *Color* → Alpha Over (4.5 page lives at `compositing/types/color/mix/alpha_over.rst`) | Compositor → *Color* → Alpha Over (`compositing/types/color/alpha_over.rst`) |
| Sockets | `Factor`, `Image` (background), `Image` (foreground) | `Background`, `Foreground`, `Factor`, `Type` |
| Straight-/premultiplied-alpha control | **checkbox `Convert Premultiplied`** | **checkbox `Straight Alpha`** |
| `Type` enum | — | `Over` / `Disjoint Over` / `Conjoint Over` (new in 5.0) |

Sources: [4.5 alpha_over.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/compositing/types/color/mix/alpha_over.rst) ·
[5.x alpha_over.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/compositing/types/color/alpha_over.rst)

- `Convert Premultiplied` (4.x): *"Defines whether the foreground is in straight alpha form… Images in the
  compositor are in premultiplied alpha form by default, so this should be false in most cases. But if, and
  only if, the foreground was converted to straight alpha form for some reason, this should be set to true."*
- `Straight Alpha` (5.x): *"Specifies whether the foreground uses straight alpha (non-premultiplied) instead
  of premultiplied alpha. Most images in the compositor are premultiplied, so this should remain disabled in
  most cases."*
- 5.0 release notes confirm the rename and the added `Type` modes — *"The Alpha Over node now supports the
  Disjoint and Conjoint Over operations"* and *"The Alpha Over node input names were renamed to Background
  and Foreground"* — [5.0 compositor.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.0/compositor.md).
- 4.5 release notes list *"The `Premultiplied` option in the Alpha Over node was removed. The same
  functionality can be achieved using Convert Alpha and a Mix Color nodes"* —
  [4.5 compositor.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/4.5/compositor.md).
  **[med]** reconciliation: the 4.5 manual still documents the `Convert Premultiplied` *input*, so the
  release note is referring to the node's separate legacy `Premultiplied` *property*, not to that input.
  Net effect in 4.5: you have `Convert Premultiplied`; in 5.x you have `Straight Alpha`.

**Alpha Convert / "Convert Alpha" node**

- Node: `Compositor → Converter → Alpha Convert` in 4.5; in 5.x the add menus were unified and the node is
  documented as `Alpha Convert` with `bpy.types.CompositorNodePremulKey` (the 5.0 release notes call the same
  thing "Convert Alpha"). Path is `compositing/types/color/alpha_convert.rst` in **both** branches.
  Sources: [main alpha_convert.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/compositing/types/color/alpha_convert.rst) ·
  [5.0 compositor.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.0/compositor.md). **[med]** on the menu-path difference.
- Inputs: `Image`; enum `Type` = `To Premultiplied` | `To Straight`.
- The manual's own warning is the operating rule: *"If the alpha is converted to straight in the Compositor,
  it should be converted back to premultiplied before the Group Output node, otherwise some artifacts might
  occur."* (In 4.5 the same sentence says "Composite Output node" — the `Composite` node was removed in 5.0
  in favour of Group Output.)

**The correct "render transparent, add the plate later" graph [high]**

```
Render Layers (Combined) ──► Alpha Over .Foreground
Background plate (Image) ──► Alpha Over .Background
                               Alpha Over ──► Group Output (5.x) / Composite (4.x)
```

### A.3 The Environment pass — clarifying the actual behaviour

- **Exact location:** `View Layer Properties → Passes → Light → Other → Environment`;
  Python `bpy.types.ViewLayer.use_pass_environment`. Present for **both Cycles and EEVEE**
  ([passes.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst)).
- **Exact manual wording (identical in 4.5 and 5.x):** *"Emission from the directly visible World. When the
  Film is set to Transparent (meaning the world is excluded from the final render), this pass can be used to
  get the environment color and composite it back in."*
- **Clarification of the actual behaviour:**
  - The pass is a normal render pass; it is not conditional on the film setting. It is the directly-visible
    world emission (i.e. exactly what the camera would see of the world, no bounce light).
  - With `Transparent` **ON**, the world is excluded from `Combined`, so `Combined` alone will not rebuild the
    original look. You must `Alpha Over` the object `Combined` **over** the `Environment` pass to restore the
    background. This is the documented and field-confirmed workflow:
    [Blender Artists 1622582](https://blenderartists.org/t/compositor-and-background-world-rendering/1622582)
    ("Enable/use the 'Environment' pass, with transparency turned on… overlay it onto the 'Env' view layer in
    the compositor with e.g. an alpha over node"). **[high]**
  - With `Transparent` **OFF**, the world is already inside `Combined`, so the pass is *redundant for the
    purpose of putting the background back*; it remains useful for isolating/grading the world separately or
    for swapping worlds in comp. **[med]** — the manual does not state that the pass is unpopulated when the
    film is opaque; "redundant, not absent" is my reading, consistent with it being an ordinary pass.
  - Because it is premultiplied-normal render data, use `Alpha Over` (not `Mix`/`Add`) unless you deliberately
    want additive light.

### A.4 Colour-space / alpha gotchas — and the exact property names

**There is no "Straight Alpha" checkbox in `Render Properties → Output` in 4.5 or 5.x.** This is verified
from RNA, not inferred: `bpy.types.ImageFormatSettings` defines exactly these properties —
`media_type` (5.0+ only), `file_format`, `color_mode`, `color_depth`, `quality`, `compression`, `use_preview`,
`exr_codec`, `use_exr_interleave`, `use_jpeg2k_ycc`, `use_jpeg2k_cinema_preset`, `use_jpeg2k_cinema_48`,
`jpeg2k_codec`, `tiff_codec`. There is no alpha-mode property. `grep -c "media_type"` on the 4.5
`rna_scene.cc` returns 0, confirming `Media Type` is a 5.0 addition.
Sources: [`rna_scene.cc` (main)](https://raw.githubusercontent.com/blender/blender/main/source/blender/makesrna/intern/rna_scene.cc) ·
[`rna_scene.cc` (4.5)](https://raw.githubusercontent.com/blender/blender/blender-v4.5-release/source/blender/makesrna/intern/rna_scene.cc) **[high]**

The controls that actually exist:

**(a) `bpy.types.Image.alpha_mode`** — `Image Editor → Sidebar → Image tab → Alpha`.
Enum items and labels (`rna_image.cc`, `alpha_mode_items`):

| Enum | UI label | RNA description |
|---|---|---|
| `STRAIGHT` | **Straight** | *"Store RGB and alpha channels separately with alpha acting as a mask, also known as unassociated alpha. Commonly used by image editing applications and file formats like PNG."* |
| `PREMUL` | **Premultiplied** | *"Store RGB channels with alpha multiplied in, also known as associated alpha. The natural format for renders and used by file formats like OpenEXR."* |
| `CHANNEL_PACKED` | **Channel Packed** | images packed in RGB and alpha, should not affect each other |
| `IGNORE` | **None** | *"Ignore alpha channel from the file and make image fully opaque."* |

Sources: [`rna_image.cc`](https://raw.githubusercontent.com/blender/blender/main/source/blender/makesrna/intern/rna_image.cc) ·
[image_settings.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/editors/image/image_settings.rst).
**Note:** the property lives on `Image`, **not** on a public `ImBuf` RNA struct. There is no public
`bpy.types.ImBuf.alpha_mode`; internally it is `ImBufFlags::AlphaPremul` / `AlphaChannelPacked` / `AlphaIgnore`
bits on `ibuf->flags`. **[high]**

**(b) The default alpha interpretation on load is by file extension** —
`BKE_image_alpha_mode_from_extension_ex()` returns `IMA_ALPHA_PREMUL` for `.exr, .cin, .dpx, .hdr` and
`IMA_ALPHA_STRAIGHT` for everything else:
[`image.cc`](https://raw.githubusercontent.com/blender/blender/main/source/blender/blenkernel/intern/image.cc).
So: **an EXR is assumed premultiplied; a PNG is assumed straight.** `image_init_color_management()` then
refines it from the file's real alpha flags on load. This is the mechanical reason a Comp'd PNG plate needs
`Straight Alpha` / `Convert Premultiplied` ticked and an EXR does not. **[high]**

**(c) What Blender writes.** Blender's PNG writer is OIIO-based and sets
`oiio:UnassociatedAlpha`:

```cpp
/* Skip if the float buffer was managed already. */
if (is_16bit && (ibuf->float_buffer.colorspace || ibuf->colorspace_is_data())) {
  file_spec.attribute("oiio:UnassociatedAlpha", 0);
} else {
  file_spec.attribute("oiio:UnassociatedAlpha", 1);
}
```

`source/blender/imbuf/intern/format_png.cc`, identical logic in
[main](https://raw.githubusercontent.com/blender/blender/main/source/blender/imbuf/intern/format_png.cc) and
[4.5](https://raw.githubusercontent.com/blender/blender/blender-v4.5-release/source/blender/imbuf/intern/format_png.cc). **[high]**
Meaning: **8-bit PNG is written with unassociated (straight) alpha**; only 16-bit PNG written from a
colour-managed float buffer is written associated (premultiplied). An EXR carries premultiplied linear data.

**(d) `Save as Render`** is the documented switch for whether the view transform is baked:
*"For display image formats like PNG, apply view and display transform. For intermediate image formats like
OpenEXR, use the default render output color space."* —
[image_formats.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/files/media/image_formats.rst). **[high]**
`bpy.ops.image.save_as` exposes `save_as_render` (and `copy`, `relative_path`) but **no alpha-mode
argument** — output alpha behaviour is the format writer's, per (c). **[med-high]**

**(e) The scene-level `Output → Color Management` panel** has `Follow Scene` / `Override`
(`bpy.types.ImageFormatSettings.color_management`); `Override` throws away the scene colour management and
uses panel values instead — [output.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/output/properties/output.rst).
Do **not** use `Override` on an EXR you intend to re-composite. **[high]** on the property; **[med]** on the
recommendation, which follows from (f).

### A.5 What breaks if you only save the Combined PNG

Every item below is anchored to a manual or source fact, not a vibe.

| Loss | Why | Anchor |
|---|---|---|
| **8-bit clipping / no headroom** | PNG 8-bit = 256 levels per channel; also *"Internally, Blender only operates in either 8-bit or 32-bit"*, and 10/12/16-bit files are converted to 32-bit float on load. Highlights above 1.0 are destroyed. | [image_formats.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/files/media/image_formats.rst) |
| **Banding** | 8-bit gradients band; the only mitigation left is `Output → Post Processing → Dither` (`RenderSettings.dither_intensity`) *"to break up banding"* — which is a screen-space hack, not precision. | [post_processing.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/render/output/properties/post_processing.rst) |
| **View transform baked in** | `Save as Render` applies view+display transform for PNG. AgX/Standard is now irreversible in the file. | [image_formats.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/files/media/image_formats.rst) |
| **No re-grade / no re-balance** | Rebalancing lighting after the fact needs the light-component passes: `Diffuse Direct/Indirect/Color`, `Glossy Direct/Indirect/Color`, `Transmission Direct/Indirect/Color`, `Volume Direct/Indirect`, `Emission`. | [passes.rst — Light](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst) |
| **No relight** | Light Groups give *"a limited Combined render pass where the scene is only illuminated by certain lights. Multiple such passes can then be combined in compositing… it's possible to change the color and intensity of individual lights without having to re-render."* PNG flattens them. | [passes.rst — Light Groups](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst) |
| **No re-denoise** | With render denoising on, `Combined` **is** the denoised result. Without the `Denoising Data` passes there is no `Noisy Image` to re-denoise with different settings. | [SE 342076 (accepted answer)](https://blender.stackexchange.com/questions/342076/how-to-save-noisy-render-as-exr) |
| **No motion vectors** | `Vector` pass — *"Motion vectors for the Vector Blur [node]"*; and it is *"disabled when Motion Blur is enabled."* Without it you cannot redo motion blur at a different shutter. | [passes.rst — Data](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst) |
| **No depth / no re-DOF / no atmospheric re-grade** | `Depth` (labelled `Z` in 4.5) *"Distance to the nearest visible surface. Can be used with the Defocus [node]"*. | [4.5 passes.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/render/layers/passes.rst) |
| **Masking/keying impossible** | `Object Index`, `Material Index` (ID Mask), and the Cryptomatte `Object` / `Material` / `Asset` passes. Cryptomatte is the good one: *"works with transparency, as well as motion blur and depth of field when using Cycles."* | [passes.rst — Indexes / Cryptomatte](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst) |
| **Alpha/premultiply baked** | PNG is 8-bit straight alpha (A.4c); any coverage refinement, matte extension or edge colour correction is gone. Object-ID-based edge work is impossible. | [format_png.cc](https://raw.githubusercontent.com/blender/blender/main/source/blender/imbuf/intern/format_png.cc) |
| **Utility passes not anti-aliased, so irrecoverable** | *"The Z, Position, Object Index, and Material Index passes are not anti-aliased."* Once flattened you can never separate them. | [4.5](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/render/layers/passes.rst) / [main](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst) |

---

## B) DENOISING ARCHITECTURE

### B.1 Cycles denoise UI — exact control names

**Panel: `Render Properties → Sampling → Denoising`.** *(Note: it is a section of the **Sampling** page,
not a separate top-level panel — same in 3.6, 4.0, 4.2, 4.5 and 5.0. There was no "denoise settings moved"
event inside 4.x; the panel has been stable. **[high]**, verified by comparing
[4.5](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/render/cycles/render_settings/sampling.rst),
[4.2](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.2-release/manual/render/cycles/render_settings/sampling.rst),
[4.0](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.0-release/manual/render/cycles/render_settings/sampling.rst),
[3.6](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v3.6-release/manual/render/cycles/render_settings/sampling.rst),
[main](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cycles/render_settings/sampling.rst).)*

| UI label | Render property | Viewport property | Values / notes |
|---|---|---|---|
| `Denoise (Viewport)` | — | `CyclesRenderSettings.use_preview_denoising` | toggles denoising in Rendered shading |
| `Denoise (Render)` | `CyclesRenderSettings.use_denoising` | — | toggles denoising of the final render |
| `Denoiser` | `denoiser` | `preview_denoiser` | `Automatic` / `OpenImageDenoise` / `OptiX`. `Automatic` *"Uses GPU accelerated denoising if supported… Prefers OpenImageDenoise over OptiX."* `OptiX` is *"Only available on NVIDIA GPUs when configured in the [Preferences > Cycles] user preferences."* |
| `Passes` | `denoising_input_passes` | `preview_denoising_input_passes` | `None` / `Albedo` / `Albedo + Normal`. Manual: *"It is recommended to use at least Albedo as None can blur out details, especially at lower sample counts."* |
| `Prefilter` :guilabel:`OpenImageDenoise` | `denoising_prefilter` | `preview_denoising_prefilter` | `None` / `Fast` / `Accurate`. Visible only with OpenImageDenoise. |
| `Quality` :guilabel:`OpenImageDenoise` | `denoising_quality` | `preview_denoising_quality` | `High` / `Balanced` / `Fast`. **Added in 4.2** (absent in 4.0). |
| `Start Sample` | — | `preview_denoising_start_sample` | *"Sample at which to start denoising in the 3D Viewport."* Viewport only. |
| `Use GPU` | `denoising_use_gpu` | `preview_denoising_use_gpu` | *"Perform denoising on the GPU. This is significantly faster than on CPU, but requires additional GPU memory. When large scenes need more GPU memory, this option can be disabled."* |

Also in the Sampling page and directly relevant: `Adaptive Sampling → Noise Threshold`
(`CyclesRenderSettings.adaptive_threshold`), `Min Samples` (`adaptive_min_samples`), `Render (Max) Samples`
(`samples`), and `Advanced → Sample Subset` (`use_sample_subset`, `sample_offset`, `sample_subset_length`)
for splitting a frame's samples across machines, combined afterwards with
`bpy.ops.cycles.merge_images(...)`.

OIDN's `Accurate` prefilter maps to OIDN's *prefiltered auxiliary images* mode in the library API
(`cleanAux = true`, with separate in-place albedo and normal prefilter filters) — see the
[OIDN README](https://raw.githubusercontent.com/RenderKit/oidn/master/README.md).

Net: OIDN 2.3.3 ships with Blender 4.5 LTS; **2.5.0** with current 5.x.
*"OpenImageDenoise is now GPU accelerated on supported hardware. This makes full quality denoising available
at interactive rates in the 3D viewport. It is enabled automatically when using GPU rendering in the 3D
viewport. It can be disabled in the denoising settings panel"* —
[4.1 Cycles release notes](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/4.1/cycles.md).

### B.2 The `Denoising Data` pass — exact pass names

- **Exact location:** `View Layer Properties → Passes → Data → Denoising Data`.
  Python: `bpy.types.CyclesRenderLayerSettings.denoising_store_passes`
  (and `bpy.types.ViewLayerEEVEE.denoising_store_passes` for the newer EEVEE support).
- **4.5 LTS (exactly three things):** *"Includes Denoising Albedo, Denoising Normal, and the combined image
  before denoising."* — [4.5 passes.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/render/layers/passes.rst)
- **5.2 / current `main` (six):** an explicit bullet list:

  - *Noisy Image* — *"The combined render result before any denoising is applied."*
  - *Denoising Albedo* — *"The diffuse base color of surfaces without lighting or shading."*
  - *Denoising Specular Albedo* — *"The specular base color, representing reflective surface color without lighting."*
  - *Denoising Normal* — *"Surface normals used to preserve edges and fine detail during denoising."*
  - *Denoising Roughness* — *"Surface roughness values used to improve denoising of glossy reflections."*
  - *Denoising Depth* — *"Distance from the camera, used to help preserve depth-based detail."*

  [5.2 passes.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v5.2-release/manual/render/layers/passes.rst) ·
  [main passes.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst)
  **Dating:** the extra three arrived with the manual commit *"Cycles: Add specular albedo pass and improve
  denoising passes"* (2026-04-10), and are present only in `blender-v5.2-release` and `main` — **not** in
  5.0 or 5.1 (verified by branch grep). Commit list via
  `https://projects.blender.org/api/v1/repos/blender/blender-manual/commits?path=manual/render/layers/passes.rst&sha=main`.

- **Names in the Compositor `Render Layers` node:** the sockets are the pass names, i.e. `Noisy Image`,
  `Denoising Albedo`, `Denoising Specular Albedo`, `Denoising Normal`, `Denoising Roughness`,
  `Denoising Depth`. The node *"outputs its image and any enabled render passes"* —
  [render_layers.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/compositing/types/input/scene/render_layers.rst).
- **Names inside a multi-layer EXR:** Blender joins **view layer name + pass name with a period**, i.e.
  `ViewLayer.Combined`, `ViewLayer.Denoising Normal`, `ViewLayer.Noisy Image`, and so on. The authoritative
  evidence is a bug that exists *because of* that convention: *"OpenEXR layers from View Layers with names
  containing a period can't be read by Nuke"* (issue #71574). **[high]**
  → **Operational rule: never put a `.` in a View Layer name.** Use `CHAR`, `ENV`, `FX`, `MATTE`.
  Sources: [issue #71574](https://projects.blender.org/blender/blender/issues/71574) ·
  [archive mirror](https://archive.blender.org/developer/maniphest/0071/0071574/index.html)
- **`Noisy Image` is not a separate image** — it *is* the pre-denoise `Combined`. **Therefore, when render
  denoising is enabled, the `Combined` pass in the render result and in the EXR is the denoised image, and
  `Noisy Image` is the raw one.** Confirmed by the accepted StackExchange answer: *"If I have Combined
  selected when I save a rendered image (as PNG), I get the denoised image. If I have 'noisy image' selected,
  I get the noisy image. All as expected."* — [SE 342076](https://blender.stackexchange.com/questions/342076/how-to-save-noisy-render-as-exr).
  This was historically under-documented to the point of a bug report: *"'Noisy Image' pass not matching
  'Combined' pass is not well documented"* — [T77185](https://archive.blender.org/developer/maniphest/0077/0077185/).
  **[high]**
- **Known Blender bug to route around:** manually saving the Image Editor view to EXR writes the `Combined`
  pass regardless of which pass you are currently viewing (reported June 2024 as
  [issue #123913](https://projects.blender.org/blender/blender/issues/123913)). Multi-layer EXR written by the
  render pipeline / `File Output` node is **not** affected — all enabled passes are written. If you need the
  noisy image as a standalone file, use the `File Output` node, not `Image → Save As`. **[high]** (per the
  cited answer).
- Manual cost warning: *"These passes increase memory usage and render time. Enable them only when denoising
  in the Compositor is required."* — [main passes.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst). **[high]**

### B.3 The Compositor `Denoise` node

**Node:** `Compositor → Filter → Denoise` (`bpy.types.CompositorNodeDenoise`). *"It uses Open Image
Denoise, which transforms noisy images into clean images with machine learning."*

**4.5 vs 5.x — inputs vs properties:**

| | 4.5 | 5.x (`main`) |
|---|---|---|
| Inputs | `Image`, `Normal`, `Albedo`, `HDR` | `Image`, `Albedo`, `Normal`, `HDR`, `Prefilter`, `Quality` |
| Properties | `Prefilter`, `Quality` | (none — became sockets) |

5.0 release notes: *"Most nodes now expose their menu options as inputs"*, and the manual commit history for
`compositing/types/filter/denoise.rst` shows *"Compositor: Turn Denoise node options into inputs"* (2025-05-18)
then *"Compositor: Turn Menu options to inputs"* (2025-08-29).

- `Prefilter` enum (identical in both, from the manual): `None` — *"retains the most detail and is the
  fastest, but assumes the input passes are noise free… If the input passes are not noise free, then noise
  will remain"*; `Fast` — *"faster than Accurate but produces a blurrier result"*; `Accurate` — *"usually
  produces more detailed results than Fast with increased processing time."*
- `Quality` enum: `Follow Scene` / `High` / `Balanced` / `Fast`.
  `Follow Scene` *"Use the scene's quality setting"* → `bpy.types.RenderSettings.compositor_denoise_preview_quality`.
- `HDR` — *"Preserve colors outside the 0 to 1 range."* **Leave this on** for scene-linear beauty passes.
- **4.5 only:** *"The Denoise node now supports GPU devices."* —
  [4.5 compositor.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/4.5/compositor.md).
  **[high]** Note this is the *compositor* node using the GPU, distinct from the Cycles render denoiser's
  `Use GPU` (B.1) — they are different switches.

**Documented workflow (5.x manual, section "Workflow"):**
1. Enable `Denoising Data` in View Layer properties.
2. Render → generates `Noisy Image`, `Denoising Albedo`, `Denoising Normal` (+ auxiliaries).
3. In the Compositor: `Noisy Image` → node `Image`; `Denoising Albedo` → `Albedo`; `Denoising Normal` → `Normal`.
Manual: *"Providing these passes allows the denoiser to better preserve edges, textures, and fine details.
The node can still be used without these additional inputs, but the result may appear softer or lose detail."*
Sources: [main denoise.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/compositing/types/filter/denoise.rst) ·
[4.5 denoise.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/compositing/types/filter/denoise.rst)

### B.4 In-render vs in-compositor vs in Nuke; before vs after compositing; per-pass vs combined

**The manual frames them as alternatives and states no preference:**
*"If you enable the Denoising Data render pass, you can alternatively denoise in the compositing step using
the Denoise node."* — [sampling.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cycles/render_settings/sampling.rst).
The 4.5 wording for the pass says the same: the passes *"can be used with the Denoise node as a replacement for
automatic denoising."*

**Do not double-denoise.** The accepted StackExchange answer on exactly this question: *"It looks like the
Compositor uses the Open Image Denoise method, so it should be about the same as the Render panel Open Image
Denoise, if you use it in the Compositor make sure that you've disabled it in the Render panel otherwise
you'll have 2 denoisings."* —
[SE 332616](https://blender.stackexchange.com/questions/332616/whats-the-difference-between-render-properties-denoise-and-compositor-denoise). **[high]**

**Recommendation for a re-composite-later pipeline [high, and it follows from B.2 + D]:**
set `Denoise (Render)` **off**, enable `Denoising Data`, and denoise in the Compositor (or in Nuke/comp).
Reason: `Combined` is denoised when render-denoising is on, so you lose the ability to change denoiser,
prefilter, quality or sample count without re-rendering — which is exactly the cost you are trying to avoid.
With `Denoise (Render)` off plus `Denoising Data` on, the EXR holds both the raw `Noisy Image` and the
albedo/normal guides, so denoising becomes a comp-side, re-runnable step.

**Before or after grading?**
- **Denoise before grading, while the data is still scene-linear.** Mechanisms, each citable:
  - OIDN expects linear input: the library's `srgb` filter parameter defaults to `false`, documented as
    *"the main input image is encoded with the sRGB (or 2.2 gamma) curve (LDR only) **or is linear**; the
    output will be encoded with the same curve"* — i.e. the default is linear —
    [OIDN README, filter parameter table](https://raw.githubusercontent.com/RenderKit/oidn/master/README.md). **[high]** on the parameter, **[med]** on the extrapolated rule.
  - The guide passes (`Denoising Albedo`, `Denoising Normal`) are raw scene-linear surface data that only
    correspond to the ungraded beauty. Grade first and the albedo/normal no longer describe the image the
    denoiser is filtering. **[med]**
  - `HDR` exists precisely because beauty data is expected linear and out of 0–1. **[high]**
- **Denoise per lighting component, then sum, then grade.** See below.
- **Nuke/comp vs Blender compositor:** functionally equivalent for OIDN (Blender's node *is* OIDN). Choose
  Nuke/Fusion/Natron when you need: real multi-channel EXR handling, Cryptomatte nodes that match the rest of
  the pipeline, or a comp artist working away from Blender. I found **no** authoritative source claiming a
  quality difference between Blender's OIDN integration and an external OIDN integration — treat
  "denoise in Nuke is better" as unsubstantiated unless you are using a *different* denoiser (e.g. Neat Video,
  or a temporally-aware denoiser over a sequence). **[med]** Blender's own Denoise node is a *still-frame,
  single-image* filter with no temporal component, which is the real argument for an external temporal
  denoiser on animation. **[med]**

**Per-pass vs combined denoise — tradeoffs**

| | Denoise `Combined` only | Denoise per lighting pass |
|---|---|---|
| Effort | one node | N nodes + sum + masks |
| Re-grade safety | poor: boosting `Diffuse Indirect` after denoising the sum amplifies the denoiser's own artefacts and re-reveals residual noise in that component | good: each component is denoised at its own noise level before any gain is applied |
| Noise statistics | a single model sees the sum; the dominant noisy component drives the result | each component denoised with statistics matched to it |
| Guide passes | one set of Albedo/Normal (correct) | reuse the same `Denoising Albedo` / `Denoising Normal` for every component — they are surface properties, shared across components **[med]** |
| Alpha / holdout | denoising the premultiplied sum is the safest single operation | per-pass denoise on transparent-heavy passes can fringe; test on the FX/matte layers **[low]** |
| Light Groups | denoise the summed result, not each group; groups are *"a limited Combined render pass"* per group, and OIDN's guides correspond to the full render. If you must denoise per group, the same Albedo/Normal still apply. **[med]** | — |

There is a real production implementation of the per-pass pattern (Blender 5.0 add-on, "Output Setup Helper"):
*"Beauty passes are routed through a reusable **DenoiseWithMix** node group — Uses Cycles denoising data
(Normal + Albedo) — Global **Denoise level** allows blending between raw and denoised results… Utility passes
automatically bypass denoising"*, with outputs split into two multi-layer EXRs, one **Beauty** ("denoised and
comp-ready") and one **Utility** ("Depth, Normal, Vector, Cryptomatte, Indices, etc. — stored losslessly") —
[GitHub: lukas-remis/Blender-automatic-output-setup](https://github.com/lukas-remis/Blender-automatic-output-setup). **[high]** as a described pattern.

**Passes to never denoise (data, not radiance):** `Depth`/`Z`, `Position`, `Normal`, `Vector` (motion),
`UV`, `Object Index`, `Material Index`, `Cryptomatte *`, `Sample Count`, `Render Time`, `Alpha Threshold`-derived
utility data. Reinforcing citation: the manual notes *"The Z, Position, Object Index, and Material Index passes
are not anti-aliased"* — denoising would smear values across hard edges —
[passes.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst). **[high]**

**Prefer `Mist` over `Depth` for atmosphere:** *"This pass produces noisy results if the render itself uses
Depth of Field or motion blur. Use the Mist pass for a cleaner image."* —
[passes.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst). **[high]**

### B.5 4.x / 5.x denoising change log (what actually changed)

There is no "denoise settings moved" event in 4.x. What changed:

| Version | Change | Source |
|---|---|---|
| 4.1 | OIDN GPU acceleration; enabled automatically when using GPU rendering in the viewport; can be disabled in the denoising panel. Supported: NVIDIA GTX 16xx/TITAN V/all RTX, Intel Xe-HPG+, Apple Silicon on macOS 13+. | [4.1 cycles.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/4.1/cycles.md) |
| 4.2 | OIDN upgraded to 2.3; GPU denoise on AMD (Windows/Linux); **CPU renders can also use GPU-accelerated denoising** — the denoiser uses the GPU device configured in User Preferences, with the side effect that the OptiX denoiser requires an OptiX compute device configured in Preferences. `Quality` (High/Balanced/Fast) appears in the panel. | [4.2 cycles.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/4.2/cycles.md) |
| 4.2–4.3 | OIDN 2.3.0 | versions.cmake |
| 4.4 | OIDN 2.3.2; OptiX denoiser updated; `Sample Subset` (Offset + Length) replaces the older sample-offset arrangement. | [4.4 cycles.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/4.4/cycles.md) |
| 4.5 LTS | OIDN 2.3.3; **Compositor `Denoise` node now supports GPU devices**; OptiX minimum driver raised to 535. | [4.5 cycles.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/4.5/cycles.md) · versions.cmake |
| 5.0 | OIDN 2.5.0 on `main`; OptiX denoiser quality improved *"by flipping the image vertically to have a top-left origin before processing"*; `Render Time` pass added. | [5.0 cycles.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.0/cycles.md) |
| 5.1 | *"Improved denoising quality with textured transparency and roughness."* | [5.1 cycles.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.1/cycles.md) |
| 5.2 | *"Open Image Denoise is no longer GPU accelerated on RDNA2 generation GPUs due to ROCm incompatibilities"*; OptiX minimum driver 575. | [5.2 cycles.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.2/cycles.md) |
| 5.2 (manual) | `Denoising Data` gains `Denoising Specular Albedo`, `Denoising Roughness`, `Denoising Depth`. | [5.2 passes.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v5.2-release/manual/render/layers/passes.rst) |
| next (main) | `Denoising Data` becomes available on **EEVEE** too (manual commit *"EEVEE: Add denoising render passes"*, 2026-08-10; not in 5.0/5.1/5.2). | commit history for `passes.rst` |

Hard limitations to design around:
- **OptiX is not a free upgrade.** *"Only available on NVIDIA GPUs when configured in the Preferences >
  Cycles user preferences"* ([sampling.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cycles/render_settings/sampling.rst)),
  and since 4.2 the CPU-render-with-GPU-denoiser path also requires the device configured in Preferences
  ([4.2 cycles.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/4.2/cycles.md)).
  **[high]**
- `Use GPU` *"requires additional GPU memory. When large scenes need more GPU memory, this option can be
  disabled."* ([sampling.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cycles/render_settings/sampling.rst)) — so on a scene that barely fits in VRAM, disabling GPU denoise is the fix, at a large time cost. **[high]**
- No temporal denoising in Blender. **[high]** (absence of any such feature/manual text).

---

## C) LAYERING / MULTI-PASS STRATEGY

### C.1 Cycles Light Groups

- **Exact location:** `View Layer Properties → Passes → Light Groups`. Marked **`:guilabel:`Cycles only`** in
  the manual — **light groups do not exist in EEVEE** (4.5, 5.0, 5.1, 5.2 and `main` all carry the
  "Cycles only" label).
  [passes.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst) **[high]**
  Corroborating: EEVEE's 5.0 additions are *"View Layer Overrides (Material, World, Sample)"*, with no light
  group mention — [5.0 eevee.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.0/eevee.md).
- **Definition:** *"A Light Group provides a limited Combined render pass where the scene is only illuminated
  by certain lights. Multiple such passes can then be combined in compositing to construct a full render with
  all the lights. The most straightforward way is to simply Add them together using the Mix Color [node], but
  by making more complex combinations, it's possible to change the color and intensity of individual lights
  without having to re-render."*
- **Assigning lights:** `Object Properties → Shading → Light Group` (`bpy.types.Object.lightgroup`), with an
  `Add Light Group` button that creates the group if the typed name doesn't exist.
  **World:** `World → Settings → Light Group` (`bpy.types.World.lightgroup`).
- **Naming / list management:** the panel's `Name` field (`bpy.types.ViewLayer.active_lightgroup_index`) edits
  the active group. The two sync operators live behind the :bl-icon:`downarrow_hlt` button to the right of the
  Light Group list:
  - **`Add Used Lightgroups`** (`bpy.ops.scene.view_layer_add_used_lightgroups`) — *"Create Light Groups for
    any lights that reference a non-existing one."*
  - **`Remove Unused Lightgroups`** (`bpy.ops.scene.view_layer_remove_unused_lightgroups`) — *"Delete any Light
    Groups that are not referenced by any lights."*

  These are the "sync my group list to my lights" pair: name your lights first, then `Add Used Lightgroups`.
- **Operational rules [med, inference from the above]:** keep the group count small (each group is a full
  additional render pass → memory and file size); name them after *department/intent* (`KEY_SUN`, `FILL_SKY`,
  `PRACTICALS`, `FX_GLOW`), not after the light datablock; run `Add Used Lightgroups` before render and
  `Remove Unused Lightgroups` after refactors; and sum them with `Add`/`Mix Color` **in linear** before the
  view transform.
- Both are also affected by `Advanced → Layer Samples` and `Sample Overrides` on the view layer
  (`CyclesRenderSettings.use_layer_samples` = `Use` / `Bounded` / `Ignore`, `bpy.types.ViewLayer.samples`) —
  [sampling.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cycles/render_settings/sampling.rst).

### C.2 View Layers as logical layers, and the "Filter" panel question

- **View Layers are the right mechanism** (*"View Layers allow you to separate a render into multiple layers,
  which can then be composited together… Render characters separately from the environment for post-processing.
  Generate multiple lighting passes without modifying the original scene setup."*) —
  [render/layers/introduction.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/introduction.rst).
- **Adding:** `Add View Layer` with three variants — **New** (empty), **Copy Settings** (*"Duplicates the
  current View Layer, including collection visibility and overrides"*), **Blank** (*"Adds a new View Layer
  with all collections disabled"*). Each scene must keep at least one.
- **There is no `View Layer → Filter` panel with Include/Exclude in 2.8/4.5/5.x.** That was the Blender 2.7x
  design. The manual's View Layer page documents only the layer list, `Name`, add/remove, and collection-based
  visibility. Filtering is now expressed as **per-collection, per-view-layer state**, edited in the Outliner's
  collection context menu or in `Collection Properties → View Layer`:
  - `Disable from View Layer` / `Enable in View Layer` → `bpy.types.LayerCollection.exclude`
  - `Set Holdout` / `Clear Holdout` → `bpy.types.LayerCollection.holdout`
  - `Set Indirect Only` / `Clear Indirect Only` **Cycles Only** → `bpy.types.LayerCollection.indirect_only`
    (*"Objects inside this collection will only contribute to the final image indirectly through shadows and
    reflections."*)
  [Outliner editing.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v5.0-release/manual/editors/outliner/editing.rst).
  **[high]** for current state; **[med]** for the 2.7x-history explanation.
- **Recommended logical layout for a stylised engineering/historical piece [med, design recommendation]:**

  | View Layer | Collections enabled | Why a separate layer |
  |---|---|---|
  | `CHAR` | characters, rigs, char lights | own light groups, own denoise/sample budget, own Cryptomatte |
  | `ENV` | sets, terrain, props | heavy geometry; can be re-rendered alone; own depth/mist |
  | `FX` | sims, volumetrics, particles, glow cards | expensive, noisy, often re-rendered; often needs different sample count and denoise |
  | `MATTE` | holdout / shadow-catcher proxies, animated mattes | holdout-based plate integration and shadow catching |

### C.3 Holdout, Mask, and Is Shadow Catcher — exact panel names

This is the area where the manual's page structure most often misleads, because `Holdout` and
`Shadow Catcher` are **both under a `Mask` heading in the same `Visibility` panel**, but documented on two
different manual pages.

**Page 1 — `Properties → Object Properties → Visibility`** (general). Contents, in order:
`Selectable`, `Show In` (`Viewports`, `Renders`), then:

- **`Mask → Holdout`** (`bpy.types.Object.is_holdout`):
  *"Render objects as a holdout or matte, creating a hole in the image with zero Alpha, to fill out in
  compositing with real footage or another render."*

Source: [scene_layout/object/properties/visibility.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/scene_layout/object/properties/visibility.rst) —
identical text in
[4.5](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/scene_layout/object/properties/visibility.rst).

**Page 2 — `Object Properties → Visibility` (Cycles object settings)** — same panel, Cycles-contributed rows:

- **`Mask → Shadow Catcher`** (`bpy.types.Object.is_shadow_catcher`): *"Enables the object to only receive
  shadow rays… This simplifies compositing CGI elements into real-world footage."*
  **Critical behaviour note from the manual:** *"The Shadow Catcher outputs different results depending on if
  the Shadow Catcher pass is enabled in Render Layer settings. With the Shadow Catcher pass enabled, all
  indirect light interactions are captured. With it disabled, a simple approximation is used instead. The
  simple approximation is used in viewport rendering."*
  → **Enable `View Layer → Passes → Light → Other → Shadow Catcher` for final renders**, or you silently get
  the approximation. **[high]**
- Also in this panel: `Ray Visibility` (`Camera`, `Diffuse`, `Glossy`, `Transmission`, `Volume Scatter`,
  `Shadow`, `Raycast`), `Culling` (`Use Camera Cull`, `Use Distance Cull`), `Motion Blur` (`Steps`,
  `Deformation`), `Shading` (`Shadow Terminator → Geometry Offset` / `Shading Offset`), `Fast GI Approximation
  → AO Distance`, `Caustics` (`Cast Shadow Caustics`, `Receive Shadow Caustics`), `Light Group`, `Light
  Linking` (`Receiver Collection`), `Shadow Linking` (`Shadow Blocker Collection`).
  Source: [render/cycles/object_settings/object_data.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cycles/object_settings/object_data.rst).

**Summary of the four related controls:**

| Intent | Control | Python |
|---|---|---|
| Punch a hole with alpha 0 to be filled later | `Object Properties → Visibility → Mask → Holdout` | `Object.is_holdout` |
| Receive/catch shadows onto a plate | `Object Properties → Visibility → Mask → Shadow Catcher` **+** `View Layer → Passes → Light → Other → Shadow Catcher` | `Object.is_shadow_catcher`, `ViewLayer.use_pass_shadow_catcher` |
| Exclude a whole collection from a view layer | Outliner: `Disable from View Layer` | `LayerCollection.exclude` |
| Make a collection contribute only indirectly | Outliner: `Set Indirect Only` (Cycles Only) | `LayerCollection.indirect_only` |

### C.4 Multi-layer EXR vs `File Output` node — exact options

**Route 1 — Multi-layer EXR from the render output.**

- **4.5 LTS:** `Output Properties → Output → File Format` = **`OpenEXR MultiLayer`**.
  There is no `Media Type` control in 4.5 (`media_type` does not exist on `ImageFormatSettings`).
- **5.0+:** the panel gained a **`Media Type`** control with `Image` / **`Multi-Layer EXR`** / `Video`
  (`bpy.types.ImageFormatSettings.media_type`):
  *"Multi-Layer EXR: Saves all inputs together in a single multi-layer OpenEXR file."* The per-format options
  (`File Format`, `Color`, `Image Sequence → Overwrite/Placeholders`) then appear under `Media Type`.
- EXR-specific options: `Color Depth` = `Float (Half)` (16-bit float, *"reduces the actual 'bit depth' to
  10-bit, with a 5-bit power value and 1-bit sign"*) or `Float (Full)` (32-bit float); `Codec` = `None`, `ZIP`,
  `PIZ`, `DWAA (lossy)`, `DWAB (lossy)`, `ZIPS`, `RLE`, `Pxr24 (lossy)`, `B44 (lossy)`, `B44A (lossy)`
  (5.x adds `HTJ2K`); `Quality` for DWAA/DWAB; `Interleave` (`use_exr_interleave`) — *"Use legacy interleaved
  storage of views, layers and passes for compatibility with applications that do not support more efficient
  multi-part OpenEXR files"*; `Preview` (JPEG sidecar for animations).
  Sources: [main output.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/output/properties/output.rst) ·
  [4.5 output.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/render/output/properties/output.rst) ·
  [image_formats.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/files/media/image_formats.rst)
- Also on the Output panel: a **header checkbox toggling automatic saving**. 5.x manual: *"The automatic saving
  of renders can be toggled using the checkbox in the panel header… When disabled, Blender does not write render
  output from this panel and instead relies on other systems… if compositing is enabled, active File Output
  nodes are used to save the result. If no such nodes exist, an error is reported."* This is a genuinely useful
  switch for a comp-driven pipeline. — [main output.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/output/properties/output.rst). **[high]**
- **Recommended codec choice [med]:** `ZIP` (lossless, 16-row blocks) or `ZIPS` for a safe default;
  `PIZ` is *"Lossless wavelet compression, effective for noisy/grainy images"* — best size/quality for a
  multi-layer pass EXR; `DWAA`/`DWAB` are lossy and should never be the archival master. `Float (Half)` is
  usually enough; use `Float (Full)` if you will do heavy grading on linear data.

**Route 2 — Compositor `File Output` node** (`bpy.types.CompositorNodeOutputFile`).

- **4.5:** fields are **`Base Path`** and **`File Format`** (plus *"More options can be set in the Sidebar
  region"*), and outputs are `{base path}/{file name}{frame number}.{extension}`. Slots are exposed in RNA as
  `file_slots` (`bpy.types.NodeOutputFileSlotFile`, with a `path`) and `layer_slots`
  (`bpy.types.NodeOutputFileSlotLayer`, with a `name`) —
  [`rna_nodetree.cc` 4.5](https://raw.githubusercontent.com/blender/blender/blender-v4.5-release/source/blender/makesrna/intern/rna_nodetree.cc).
  **[high]** on the RNA structures; **[med]** on the exact sidebar panel titles in 4.5 (the 4.5 manual page is
  thin, it only says "more options in the Sidebar").
- **5.0+ — the node was redesigned.** 5.0 release notes: *"The File Output node was redesigned for a better
  user experience. It now supports dragging links to create a new input. The final paths of the images are
  displayed in the UI to remove guess work. The base path is now split into a Directory and a File Name…"* —
  [5.0 compositor.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.0/compositor.md).
  New structure, exactly:
  - Node body: `Directory`, `File Name`, `Media Type` (`Image` / `Multi-Layer EXR`).
  - Sidebar → **`Node → Properties → Node Format`**: format/encoding for all outputs; for `Image` each output
    can be given its own settings; for `Multi-Layer EXR` see the OpenEXR options.
  - Sidebar → **`Node → Properties → Images/Layers`**: *"Lists all input sockets of the node. The name of each
    input socket is used to construct the final file name."* Contains **`Override Node Format`**
    (`bpy.types.NodeCompositorFileOutputItem.override_node_format`) and, when enabled, an **`Item Format`**
    panel with that output's own format/encoding.
  - Sidebar → **`Node → Properties → Output Paths`**: *"Displays the final file path and extension for each
    input/layer, based on current settings."* Also `File Extensions`
    (`CompositorNodeOutputFile.use_file_extension`).
  - **Adding multiple slots:** *"By default, the node has no input sockets. Inputs can be added by dragging an
    output from another node onto the blank socket area, or by adding new inputs in the Images/Layers panel."*
    With `Media Type = Image`, *"input names are also used to construct subdirectories"*: *"If an input name
    contains a slash character (`/` or `\`), the path is interpreted as a directory hierarchy. Any missing
    directories are created automatically during output."* → you can name a socket `passes/diffuse` and get
    `passes/diffuse0001.exr`. **[high]**
  - **Filename convention:** `{Directory}/{File Name}{Socket Name}{frame number}.{extension}`, and *"Both the
    File Name and the Image names (when saving multiple images) can contain `####` to force the frame number to
    appear in a specific place in the filename."*
  - **5.0 behaviour change:** *"The File Output node now only appends the frame number to the image name when
    doing an animation render… adding `####` manually in the name should substitute the frame number even in
    single renders."* — [5.0 compositor.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.0/compositor.md). **[high]**
  Source for all of the above: [main file_output.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/compositing/types/output/file_output.rst).

**Which route?**
- **Multi-layer EXR** is the archival master: one file per frame, every enabled pass, all view layers,
  re-loadable into Blender retaining layers, and readable as `ViewLayer.PassName` elsewhere
  (*"An OpenEXR file can store multiple layers and passes. This means OpenEXR images can be loaded into a
  Compositor keeping render layers and passes intact."* —
  [image_formats.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/files/media/image_formats.rst)). **[high]**
- **`File Output` node** is for *split delivery*: separate Beauty and Utility files, per-pass files for an
  external comp app, JPEG previews, or different formats per pass (half-float beauty, lossless utility,
  PNG preview). 5.x's `Output Paths` panel removes the guesswork that used to make this error-prone. **[high]**
- **Do both:** multi-layer EXR as master, `File Output` for the downstream-consumable splits. Storage is cheap
  relative to a re-render.

### C.5 Concrete pass sets for "re-composite without re-rendering"

Enable in `View Layer Properties → Passes`. Names below are the manual's pass names; `Z` is the 4.5 UI label
for what 5.x calls `Depth` (`use_pass_z` in both).

**Minimum viable set — 8 passes. This is what you need to change your mind about the grade, the DOF, the
background and the masks, without re-rendering.**

| # | Pass | Group in UI | Why it's in the minimum |
|---|---|---|---|
| 1 | `Combined` | Data → Include | The final image; your fallback and your A/B reference |
| 2 | `Depth` (`Z` in 4.5) | Data → Include | Re-DOF (Defocus node), depth fog/atmosphere, depth compositing — **the single highest-value pass after Combined** |
| 3 | `Mist` | Data → Include | Cheap, clean atmospheric fall-off; explicitly the *"cleaner image"* alternative to Depth when DOF/motion blur is on |
| 4 | `Vector` | Data → Include | Only way to redo motion blur / add vector blur in comp (disabled when Motion Blur is on in-render) |
| 5 | `Normal` | Data → Include | Relight, normal-based effects, denoiser guide |
| 6 | `Denoising Data` | Data → Include | Gives `Noisy Image` + `Denoising Albedo` + `Denoising Normal` → re-denoise at will (and in 5.2+, Specular Albedo/Roughness/Depth) |
| 7 | `Cryptomatte → Object` (+ `Material`) | Cryptomatte | The only practical way to mask arbitrary objects *after* render, and it *"works with transparency, as well as motion blur and depth of field when using Cycles"* |
| 8 | `Emission` | Light → Other | Isolates emissive geometry (signage, lamps, screens, glows) — essential for a stylised look where glow is graded separately |

**Fuller set — for a production that will be re-graded, relit and re-composited in a comp app.**

Everything above, plus:

| Pass | Group | Why |
|---|---|---|
| `Position` | Data → Include | World-space relighting, projections, 3D-integrated effects |
| `UV` | Data → Include | Map UV node (Cycles only): re-texturing, decals, distortion in comp |
| `Object Index`, `Material Index` | Data → Indexes | Cheaper ID mattes; needed where Cryptomatte levels are exhausted |
| `Alpha Threshold` | Data (`ViewLayer.pass_alpha_threshold`) | Controls which surfaces write to Depth/Position/Normal/Vector/UV/Index — set it deliberately (0.0 = first hit always writes) |
| `Sample Count` | Data → Debug (`use_pass_sample_count`) | Diagnose adaptive sampling: where are you wasting samples |
| `Render Time` | Data → Debug (5.0+ only) | Per-pixel cost map; *"not supported on GPU rendering"*; ideal for finding the shots/regions to optimise |
| `Diffuse Direct`, `Diffuse Indirect`, `Diffuse Color` | Light → Cycles | The core relight/rebalance trio |
| `Glossy Direct`, `Glossy Indirect`, `Glossy Color` | Light → Cycles | Specular rebalance; essential for metal/glass on an engineering subject |
| `Transmission Direct`, `Transmission Indirect`, `Transmission Color` | Light → Cycles | Glass, fluid, gauges, lenses. *"The Transparent BSDF is not included… use a Glass with the IOR set to 1"* if you need it included |
| `Volume Direct`, `Volume Indirect` | Light → Cycles | Steam, smoke, dust, haze |
| `Environment` | Light → Other | Isolate/swap the world; **required** to put the background back when `Film → Transparent` is on (A.3) |
| `Ambient Occlusion` | Light → Other | Grayscale 0–1, *"suitable for multiplying with a color image"* — cheap contact-shadow/dirt for a stylised look |
| `Shadow Catcher` | Light → Other | Only if you use shadow catchers; **must be enabled** or you get the viewport approximation (C.3) |
| `Cryptomatte → Asset` | Cryptomatte | Groups objects by parent — useful for whole-assembly mattes. *"This option is not related to Blender's asset feature."* |
| `Cryptomatte Level` (`pass_cryptomatte_depth`) | Cryptomatte | *"The maximum number of objects to be distinguished per pixel. The Render Layers node will output half this many Cryptomatte images, named (for example) CryptoObject00, CryptoObject01 and so on — the reason being that one Cryptomatte image can reference two objects per pixel."* Raise it for busy mechanical assemblies; it multiplies file size |
| Light Groups | Light Groups | *"change the color and intensity of individual lights without having to re-render"* (C.1) |
| `Grease Pencil` (if used) | Data → Include | Separate layer for line-art/annotation; note the manual's caveat that some GP blend modes alter alpha chromaticity |
| Shader AOVs (`View Layer → Shader AOV`, `AOV.type` = `Color`/`Value`) | Shader AOV | Up to 16 Color + 16 Value AOVs; custom masks/curves/position data. *"The name can be anything as long as it doesn't conflict with other (enabled) passes."* |

Sources for every pass name and description in this section:
[main passes.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst) ·
[4.5 passes.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/render/layers/passes.rst).

**EEVEE caveats, if any shot is EEVEE** (worth knowing even in a Cycles show, for previz):
- *"Camera DOF and motion blur are not rendered in passes other than Combined."*
- *"Transparent materials that have their surface_render_method set to Blended are not rendered in passes
  other than Combined and Transparent. Use the Dithered method instead."*
- *"Shader to RGB only works correctly in the Combined pass."*
- Maximum 16 Color and 16 Value AOVs.
- There is no `Shadow` pass in Cycles (removed in 3.0 manual, 2022-12-05 commit); the EEVEE `Shadow` pass
  exists and is EEVEE-only.
- EEVEE's `Transparent` pass *"only supports grayscale opacity. Colored opacity will show differently than in
  the Combined pass."*
Source: [passes.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst).

---

## D) DELIVERY / RE-RENDER AVOIDANCE

### D.1 `Cache Result` — exact name, folder, filename, and persistence

- **Exact control:** `Output Properties → Output → Saving → Cache Result`.
  Python: `bpy.types.RenderSettings.use_render_cache`.
- **What it does (manual, verbatim):** *"Saves the rendered view layers and their passes to a multi-layer
  OpenEXR image. The Compositor can then use this file to improve performance, especially for heavy
  compositing. The image is stored in the Render Cache folder as specified in the File Paths Preferences. You
  can also load it back into the Image Editor's Render Result, **even after closing and reopening Blender**;
  see Open Cached Render."*
  Sources: [main output.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/output/properties/output.rst) ·
  [4.5 output.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/render/output/properties/output.rst) — the wording is identical in both, so **yes, it survives reopening Blender**. **[high]**
- **Exact preference name:** `Edit → Preferences → File Paths → Render → Render Cache`.
  Python: `bpy.types.PreferencesFilePaths.render_cache_directory`.
  [file_paths.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/editors/preferences/file_paths.rst).
  **[high]**
- **Exact on-disk filename.** From the source
  ([`render_result.cc`](https://raw.githubusercontent.com/blender/blender/main/source/blender/render/intern/render_result.cc)):

  ```c
  SNPRINTF(filename_full, "cached_RR_%s_%s_%s.exr", filename, sce->id.name + 2, path_hexdigest);
  BLI_path_join(r_path, FILE_CACHE_MAX, root, filename_full);
  ```

  where `filename` is the **blend filename with the `.blend` extension stripped**, `sce->id.name + 2` is the
  **scene name** (the `+ 2` skips Blender's `SC` ID prefix), and `path_hexdigest` is the **hex MD5 of the
  absolute blend-file path**. So:

  `{Render Cache}/{...}/cached_RR_{blendname}_{scenename}_{md5hex}.exr`

  e.g. `cached_RR_shot_010_0100_lighting_Main_4f2c...ab.exr`. **[high]** — read directly from source.
  Also from the same function: if the blend has never been saved, `filename` becomes the literal string
  `UNSAVED` and the relative root resolves against the OS temp dir (`BKE_tempdir_base()`); if `Render Cache`
  is left blank, the root also falls back to the OS temp dir — *"Default to *non-volatile* temp dir"* is the
  source comment, i.e. **set this preference explicitly or your cache may be in `/tmp` and vanish.**
  **[high]** — and note that this is the *opposite* of what the comment claims; verify empirically before
  relying on the default.
- **How it is implemented:** it is the `R_EXR_CACHE_FILE` flag in `RenderData.scemode` (pipeline:
  *"We still want to use 'Render Cache' setting from the original (main) scene"*,
  [`pipeline.cc`](https://raw.githubusercontent.com/blender/blender/main/source/blender/render/intern/pipeline.cc)),
  and the write/read pair prints `Caching exr file, %dx%d, %s` / `read exr cache file: %s` to the console —
  **watch the console to confirm the cache path you actually got.** **[high]**
- **Caveat:** the cache is keyed on the blend-file path + scene name, not on scene *content*. Change the scene
  and re-render, and the file is overwritten. It is a "reopen and keep comping" tool, not a versioned render
  archive. Use multi-layer EXR output for the archive. **[med]**

### D.2 `Open Cached Render`

- **Exact location:** `Image Editor → Image → Open Cached Render`. Shortcut **`Ctrl-R`**.
  Python: `bpy.ops.image.read_viewlayers`.
- **Manual, verbatim:** *"Find the render cache file for the current scene and load it into the Render Result.
  This way, you can restore the last render from a previous Blender session and continue working in the
  Compositor without having to render the scene again. Note that Blender doesn't create these cache files by
  default. You have to enable Cache Result in the scene's Output options and then render it at least once."*
  [editors/image/editing.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/editors/image/editing.rst). **[high]**
- So the full procedure is: tick `Cache Result` → render once → later, `Ctrl-R` restores it. **[high]**

### D.3 Why render-once / composite-many matters — with hard numbers

**The manual already argues the general case for you.** On the Output panel:
*"Try out different video encoding options in seconds, rather than minutes or hours as encoding is usually much
faster than rendering the 3D scene."* — [output.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/output/properties/output.rst). **[high]**
That is the *encoding* comparison, but the same ratio applies with a much larger multiplier to compositing:
comp ops on cached EXRs are CPU/GPU-bound on already-solved pixels, whereas a render re-solves light transport
from scratch.

**Concrete numbers (the honest answer — these are scarce, but here is a real one from Blender Studio):**
Blender Studio, February 2026, on the *Singularity* production:
*"The current estimate is that a preview of the film takes 700 hours to render. Final quality could take 7000.
Which is around 1h per frame."* And on how they scaled it: *"to estimate the final render time, we multiply
against the difference of current and final samples (100 samples in preview vs 1000 samples in final render
means multiplying total_time_hours by 10)."*
Source: [Blender Studio — "Estimating final render times using Blender VSE"](https://studio.blender.org/blog/estimating-final-render-times-using-blender-vse/). **[high]** (it is their own published figure and method).

Other real, checkable data points on the render-cost side:

- **Sample count is the dominant cost dial and is ~linear.** The `10×` figure above for a 10× sample increase
  is the production rule of thumb. In the Sprite Fright master class, the Art Director sets
  *"Render to 200 and cap Viewport at 100"*, both denoisers to OpenImageDenoise, `Start Sample` to 1, and
  leans on *"Blender's real-time denoising capabilities to get a clearer image while we're adjusting the
  lighting"* — i.e. production deliberately renders low and denoises, rather than rendering to convergence.
  [Blender Studio — Sprite Fright Master Class: Lighting & Rendering](https://studio.blender.org/blog/Sprite-Fright-Master-Class-Lighting-Rendering/). **[high]**
- **Cheating beats solving.** Same source, on volumetric light shafts: *"we won't resort to physically
  accurate volume rendering. For a movie this is too time-consuming to render."* They build the shafts from an
  emissive volume cube plus a noise/gradient ramp instead. This is the pattern for a stylised show: **bake the
  expensive effect into a cheap pass and control it in comp.** **[high]**
- **OIDN GPU denoise benchmark** (denoising time in seconds, Junkshop scene), from the 4.1 release notes:
  Apple M2 Ultra CPU 1.035 s vs Apple M2 Ultra GPU (76 cores) 0.293 s; Intel i9-13900k 1.224 s — i.e. **~3.5×
  from GPU denoise alone** on that hardware, at the same quality.
  [4.1 cycles.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/4.1/cycles.md). **[high]**
- **[med/low] I did not find** a credible published "compositing a frame takes X seconds vs rendering takes Y"
  figure from a studio. If you need one for a business case, measure it on your own shots: render one frame
  with `Render Time` pass enabled (5.0+), and record wall-clock for the same composite at 1× and at 4×
  resolution. Do not cite an invented ratio.

**The argument, assembled:** at ~1 hour per frame for final quality, a 90-second 24 fps shot is ~2,160 frames ≈
**2,160 GPU-hours**; a 6-minute piece is ~8,640 frames ≈ **8,640 GPU-hours**. Every class of mistake that
forces a re-render (wrong grade, wrong exposure, wrong DOF, a background that should have been a plate, a
matte that should have been Cryptomatte, a denoise that is too soft) costs that again. Every one of those is a
comp-time operation measured in seconds-to-minutes if the passes exist.

### D.4 Colour management when re-compositing

**The rule: keep the master EXR scene-linear and apply the View Transform only at final delivery.**

- *"For intermediate files in production, it is recommended to use OpenEXR files. These are always stored in
  scene linear color spaces, without any data loss. That makes them suitable to store renders that can later be
  composited, color graded and converted to different output formats."* (4.5 wording) —
  [4.5 color_management.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/render/color_management.rst).
  5.x wording: *"These are always stored in scene linear color spaces, with high precision to avoid data loss."*
  — [5.x color_spaces.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/color_management/color_spaces.rst). **[high]**
- *"Rendering and compositing is best done in scene linear color space, which corresponds more closely to
  nature, and makes computations more physically accurate."* — same pages. **[high]**
- **Do not bake the view transform into the EXR.** Mechanism: `Save as Render` — *"For display image formats
  like PNG, apply view and display transform. For intermediate image formats like OpenEXR, use the default
  render output color space."* — [image_formats.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/files/media/image_formats.rst). **[high]**
  A view-transform-baked EXR is a display-referred image wearing a scene-linear file extension: adding lights,
  multiplying passes, or grading it in linear space will all be wrong, and the highlights AgX rolled off are
  not recoverable.
- **Which view transform applies at the end.** `Render Properties → Color Management → View Transform`
  (`bpy.types.ColorManagedViewSettings.view_transform`).
  - **4.5 LTS values:** `Standard`, `Khronos PBR Neutral`, `AgX`, `Filmic`, `Filmic Log`, `False Color`, `Raw`.
    AgX is documented as *"A tone mapping transform that improves on Filmic… offers 16.5 stops of dynamic range
    and desaturates highly exposed colors to mimic film's natural response to light."* Filmic is
    *"deprecated and is superseded by AgX"*.
    [4.5 color_management.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/render/color_management.rst). **[high]**
  - **5.x values:** adds `ACES 1.3` and `ACES 2.0` (and an `AgX HDR` view), plus new displays
    `Rec.2100 PQ` / `Rec.2100 HLG` and a `Working Space` concept.
    [5.x displays_views.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/color_management/displays_views.rst) ·
    [5.0 color_management.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.0/color_management.md). **[high]**
  - AgX became the default replacing Filmic in Blender 4.0 — relevant if you are matching existing plates or
    legacy renders. **[med]** (widely reported; I did not fetch the 4.0 release note page for it specifically).
  - **For a stylised engineering/historical look, `Standard` is often the right choice** if your materials and
    lighting are authored to land in range, because it does no tone mapping and therefore no highlight
    desaturation; `AgX` if you need filmic highlight roll-off. Pick one at the start and record it — a view
    transform change is a re-grade of every frame. **[med]**
- **The manual page locations changed in 5.0** (the user's premise is correct):
  - 4.5: a single page at `render/color_management.rst` →
    [render/color_management.rst](https://projects.blender.org/blender/blender-manual/raw/branch/blender-v4.5-release/manual/render/color_management.rst)
    (rendered: `https://docs.blender.org/manual/en/4.5/render/color_management.html`).
  - 5.x: it became a section, `render/color_management/`, with `index.rst`, **`color_spaces.rst`**,
    **`displays_views.rst`**, `opencolorio.rst`, `system_configuration.rst` →
    `https://docs.blender.org/manual/en/5.0/render/color_management/`,
    `.../color_management/displays_views.html`, `.../color_management/color_spaces.html`. **[high]**
  - What moved where: `Display Device` + `View Transform` + `Look`/`Exposure`/`Gamma`/`Curves`/`White Balance`
    now live in **`displays_views.rst`**; the linear-workflow rationale, `Non-Color`, the OpenEXR
    recommendation and the built-in colour-space list now live in **`color_spaces.rst`**; the *new*
    `Working Space` panel (`bpy.types.BlendFileColorspace.working_space`, default **Linear Rec.709**, options
    Linear Rec.2020 and ACEScg) is in `color_spaces.rst`. **[high]**
  - ⚠️ **5.x: the working space is now a per-blend-file property.** *"The working space affects the colors of
    all data-blocks in a file, and has a significant effect on rendering and compositing results. Generally the
    working space should be chosen at the start of a project and used for all blend files."* Blender can convert
    between working spaces but *"this is only an approximation and manual fix-ups are typically needed."* —
    [5.x color_spaces.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/color_management/color_spaces.rst) ·
    [5.0 color_management.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.0/color_management.md). **If you build in 4.5 and later open in 5.x, the default will be Linear Rec.709 — the same as before — so 4.5 → 5.x is safe; only introduce Rec.2020/ACEScg deliberately.** **[high]**
- **Per-output-node override, exactly:**
  - **Scene-level:** `Output Properties → Output → Color Management` → `Follow Scene` | `Override`
    (`bpy.types.ImageFormatSettings.color_management`). `Override` uses the panel's own values and
    *"disregard[s] any color management settings set at the Scene level."*
    [output.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/output/properties/output.rst)
  - **Compositor `File Output` node:** sidebar `Node → Properties → Node Format` holds the default encoding;
    `Node → Properties → Images/Layers` → **`Override Node Format`**
    (`bpy.types.NodeCompositorFileOutputItem.override_node_format`) enables a per-output `Item Format` panel.
    [file_output.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/compositing/types/output/file_output.rst)
  - **Image level:** `bpy.ops.image.save_as(..., save_as_render=True)` and the Image sidebar's
    **`View as Render`** toggle (`bpy.types.Image.use_view_as_render`) — *"Display the image data-block (not
    only renders) with view, exposure, gamma, RGB curves applied. Useful for viewing rendered frames in linear
    OpenEXR files the same as when rendering them directly."*
    [5.x displays_views.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/color_management/displays_views.rst) ·
    [image_settings.rst](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/editors/image/image_settings.rst)
  - **Raw + manual conversion (5.0+ only):** a new **`Convert to Display`** compositor node, and a new
    `Working Space` choice on the `Convert Color Space` node. 5.0 release notes: *"For most workflows it is
    recommended to use the native color management options in the scene and file output nodes. But for some
    advanced use cases the conversion can be manually performed in the compositor, typically combined with a
    Raw view transform in the scene."*
    [5.0 color_management.md](https://projects.blender.org/blender/blender-developer-docs/raw/branch/main/docs/release_notes/5.0/color_management.md). **[high]**
- **Also relevant to a re-composite:** `Render Properties → Color Management → Look` (`view_settings.look`,
  *"Applied before color space conversion"*), `Exposure` (*"applied before color space conversion"*,
  `output = render × 2^exposure`), `Gamma` (*"after color space conversion"*), `Use Curves`
  (`use_curve_mapping`), `White Balance` (`use_white_balance`, `white_balance.temperature`/`.tint`), and
  `Sequencer` colour space (`ColorManagedSequencerColorspaceSettings.name`).
  **Note:** `Look`/`Exposure`/`Gamma`/`Curves`/`White Balance` are *view-side*, i.e. they are baked into a PNG
  but not into a scene-linear EXR. **They are therefore exactly the things you can still change after
  rendering — which is the point of keeping the EXR.** **[high]**

### D.5 File and folder naming conventions that are actually in the wild

Blender Studio's own published conventions (a defensible default for an in-house pipeline):

- *"No caps, no gaps: name files with lowercase letter and avoid whitespaces."* No special characters;
  underscores as spacing, dashes to separate items.
- General schema:
  `{show_prefix:optional}-{type}-{name}.{variant:optional}-{task}-v{version}_{version_info}.{extension}`
  where `type` ∈ `char|set|lib|prop`, `variant` (e.g. `red`, `blurry`) only on exports/renders, `version`
  (`v001`, `v002`) only on renders/exports else `version_info` (e.g. `720p`, `cache`).
- Shot identifier: `010_0030` = sequence `010` (3 digits, +10 on creation) + shot `0030` (4 digits, +10).
- Shot file: `140_0010-anim.blend`; path `svn/pro/shots/140_credits/140_0010/140_0010-anim.blend`.
- Project layout: `local/`, `shared/`, `svn/`, `render/` (symlink to farm output); `shared/` holds
  `editorial`, `audio`, `deliver`, `export`, `footage`; `svn/` holds `dev`, `edit`, `pre`, `pro`
  (`pro/assets/{cam,chars,props,sets}`, `pro/shots/{seq}/{shot}/`).
Sources: [Naming Conventions — Introduction](https://studio.blender.org/tools/naming-conventions/introduction) ·
[File Naming](https://studio.blender.org/tools/naming-conventions/file-types) ·
[Folder Structure Overview](https://studio.blender.org/tools/td-guide/folder_structure_overview). **[high]**

For the render itself, the concrete suggestion this research supports **[med]**:

```
renders/
  {shot}/                      e.g. 010_0030
    lighting/
      v001/
        exr/    010_0030-lighting-v001.0001.exr          # multi-layer master, all passes
        beauty/010_0030-lighting-v001.beauty.0001.exr    # if split via File Output
        utils/ 010_0030-lighting-v001.utils.0001.exr
        preview/010_0030-lighting-v001.0001.png          # view-transform baked, 8-bit, for review ONLY
```

Two hard rules from the sources: **no dots in View Layer names** (breaks `ViewLayer.Pass` parsing — issue
#71574) and **never reuse the same output folder across versions** (the render cache in particular is keyed
only on blend path + scene name and will be silently overwritten — D.1).

---

## Appendix: known-false premises, corrected

1. **"PNG output has a Straight Alpha setting in `bpy.types.ImBuf`/`ImageFormatSettings`."**
   No. `ImageFormatSettings` has no alpha property (verified from RNA), and `ImBuf` exposes no public
   `alpha_mode`. The real controls are `bpy.types.Image.alpha_mode` (Image Editor sidebar → `Image` → `Alpha`)
   and the compositor Alpha Over's `Convert Premultiplied` (4.x) / `Straight Alpha` (5.x). Blender's own PNG
   *writer* decides: 8-bit PNG is written with `oiio:UnassociatedAlpha = 1` (straight); 16-bit PNG from a
   managed float buffer with `= 0` (premultiplied). A.4.
2. **"The Cycles denoise settings moved in 4.x."**
   They did not. `Render Properties → Sampling → Denoising` is where they have been since 3.6 at least, and
   still are in 5.x. What changed in 4.x was *behaviour and added controls*: GPU denoise (4.1), `Quality` +
   OIDN 2.3 + AMD/CPU-GPU-denoise (4.2), OptiX update + `Sample Subset` (4.4), compositor Denoise GPU + the
   Alpha Over "Premultiplied" property removal (4.5). B.5.
3. **"View Layer `Filter` with Include/Exclude."**
   Not in 2.8+/4.5/5.x. Per-collection `exclude` / `holdout` / `indirect_only`, set from the Outliner, is the
   replacement. C.2.
4. **"The Environment pass only works when film is transparent."**
   It is an ordinary pass available in both Cycles and EEVEE. It is *needed* when film is transparent and
   *redundant* when it is not. A.3.
5. **"Denoising Data gives you an un-denoised Combined alongside the denoised one."**
   It gives you `Noisy Image` (pre-denoise) — which *is* the un-denoised Combined — plus guides. There is no
   separate "denoised" pass: **`Combined` itself is the denoised image when render denoising is on.** B.2.
