# Brunel

A harness for producing engineering-history animation - starting with Marc Brunel's tunnelling
shield for the Thames Tunnel (1825-1843) - that gets **measurably better every episode**.

One person art-directs. An LLM writes specs. Deterministic Python writes Blender files.

> The deliverable of Episode 1 is not an episode. It is a **ratchet**.

See **[ROADMAP.md](ROADMAP.md)** for the full plan: maturity ladder, quarterly plan, budget, risks,
and the subject dossier.

---

## Status

Episode 1 renders end to end on this Mac as a **72-second low-fidelity animatic with a burned-in
caption track and a scratch voiceover**. The Mac is the control plane, not a render farm; final
frames belong on the RTX 3080.

## Quick start

```bash
cd brunel
uv venv --python 3.13
uv pip install -r requirements.txt      # bpy==5.2.2
python -m harness doctor                # verify the toolchain lock
```

**Always storyboard before you render.** Eight stills cost about a minute and catch the framing,
staging and lighting disasters that a full render would otherwise hide for an hour:

```bash
python -m harness validate spec/ep01/ep01.toml            # no Blender needed
python -m harness render   spec/ep01/ep01.toml --fast --stills
```

Then render and deliver:

```bash
python -m harness render  spec/ep01/ep01.toml --fast --res 384x682
python -m harness deliver spec/ep01/ep01.toml --fast
```

`deliver` assembles the cut, writes SRT + ASS captions from the spec's narration, synthesises a
scratch voiceover, burns the captions in, and muxes the audio.

| Command | Does |
|---|---|
| `doctor` | verify the toolchain lock against what is actually installed |
| `validate` | load and validate a spec, no Blender required |
| `build` | spec -> `.blend`, run the assertion layer, write `manifest.json` |
| `render` | frames to `renders/<ep>/<shot>/`; `--stills` for the storyboard pass |
| `assemble` | frames -> silent mp4 |
| `captions` | narration -> SRT + ASS, respecting the Reels safe zone |
| `voice` | scratch VO via macOS `say`, aligned to the shot timeline |
| `pipeline` | build + render + assemble |
| `deliver` | assemble + captions + voice -> finished file |

## Measured, not estimated

`render-bench.json` holds real numbers from this machine. On the M1 (Cycles, CPU):

| Scene | Resolution | spp | s/frame | Notes |
|---|---|---|---|---|
| `spec/ep01/ep01.toml` | 384x682 | 8 | **1.97** | 864 frames, 1442 objects - the number to trust |
| `spec/mvp/mvp.toml` | 384x682 | 8 | 3.00 | over 48 frames, so ~half of it was scene build |
| `spec/mvp/mvp.toml` | 384x682 | 8 | 3.91 | Metal - *slower* than CPU on the M1 |

Extrapolated to Episode 1's final settings (1080x1920, 32 spp): roughly **62 s/frame**, or about
**37 hours** for 2,160 frames on the Mac. The RTX 3080 row is still blank, and every schedule claim
in `ROADMAP.md` depends on it.

**Short benchmark runs lie.** Scene construction is a fixed cost independent of frame count, so a
48-frame benchmark overstates per-frame time by about half. Measure over hundreds of frames, or
subtract the build.

## Layout

```
harness/          the compiler - the only thing that writes bpy
  spec.py         spec loading + validation (closed vocabulary, refuses to guess)
  generators.py   geometry generators
  build.py        scene graph, assertion layer, manifest
  render.py       per-shot staging, visibility, tracked animation
  captions.py     narration -> SRT/ASS, burn-in
  audio.py        scratch voiceover via macOS say
  factgate.py     accuracy gate (--publish blocks)
  assemble.py     frames -> mp4
spec/             episode specs (TOML), shot lists, fact ledgers
library/          the compounding asset kit (GEN / MAT / SHOTS)
goldens/          canary renders for regression
qa/               rubrics, one per maturity level
legal/            per-asset licence register
eval/             the eval ledger - the only accepted retrospective evidence
renders/          gitignored output
```

## Principles

1. **The model is interchangeable; the harness is the moat.** The LLM writes a diffable spec.
   Only deterministic Python writes `bpy`.
2. **Automate generation, never adjudication.** The critic is advisory. The human gate is mandatory.
3. **Score renders, not code.** "The script ran" is not "the shot works".
4. **Storyboard before you render.** Eight stills are cheaper than an hour of wrong frames.
5. **1 Blender unit = 1 metre.** Always. Hero dimensions within +/-10% of a cited source.
6. **Facts before script; script before render.** `factgate` blocks the render.

## Requirements

- Python **3.13** exactly (bpy 5.2.2 requires it)
- `ffmpeg` (present: 8.0.1)
- Optional: a Windows box with an NVIDIA GPU for final frames
