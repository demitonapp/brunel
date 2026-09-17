# Brunel

A harness for producing engineering-history animation — starting with Marc Brunel's tunnelling
shield for the Thames Tunnel (1825–1843) — that gets **measurably better every episode**.

One person art-directs. An LLM writes specs. Deterministic Python writes Blender files.

> The deliverable of Episode 1 is not an episode. It is a **ratchet**.

See **[ROADMAP.md](ROADMAP.md)** for the full plan: maturity ladder, quarterly plan, budget, risks,
and the subject dossier.

---

## Status

**MVP: low-fidelity preview render on the Mac.** No GPU render node required.

The Mac M1 is not a render farm — it is the control plane. But it can build scenes and render
low-fidelity previews headlessly via `bpy`, which is enough to prove the pipeline end to end and to
iterate on camera, staging and timing before any final frame is rendered on the RTX 3080.

## Quick start

```bash
cd brunel
uv venv --python 3.13
uv pip install -r requirements.txt      # bpy==5.2.2
python -m harness doctor                # verify the toolchain lock
python -m harness build  spec/ep01/ep01.toml     # spec -> scene, run assertions
python -m harness render spec/ep01/ep01.toml --fast   # low-fi preview -> renders/
python -m harness assemble renders/ep01          # frames -> mp4
```

## Measured, not estimated

`render-bench.json` holds real numbers from this machine. On the M1 (CPU, Cycles):

| Scene | Resolution | spp | s/frame |
|---|---|---|---|
| `spec/mvp/mvp.toml` | 384x682 | 8 | **3.00** |
| `spec/mvp/mvp.toml` | 480x854 | 8 | **4.48** |
| `spec/mvp/mvp.toml` | 384x682 | 8 | **3.91** (Metal - *slower* than CPU) |

Extrapolated to Episode 1 settings (1080x1920, 32 spp) that is roughly **95 s/frame**, or about
**57 hours** for 2,160 frames on the Mac. The RTX 3080 row is still blank, and every schedule
claim in `ROADMAP.md` depends on it.

One shot through all three steps:

```bash
python -m harness pipeline spec/ep01/ep01.toml --shots s04 --fast
```

## Layout

```
harness/          the compiler — the only thing that writes bpy
spec/             episode specs (TOML), shot lists, fact ledgers
library/          the compounding asset kit (GEN / MAT / SHOTS)
goldens/          canary renders for regression
qa/               rubrics, one per maturity level
legal/            per-asset licence register
eval/             the eval ledger — the only accepted retrospective evidence
renders/          gitignored output
docs/             architecture and process
```

## Principles

1. **The model is interchangeable; the harness is the moat.** The LLM writes a diffable spec.
   Only deterministic Python writes `bpy`.
2. **Automate generation, never adjudication.** The critic is advisory. The human gate is mandatory.
3. **Score renders, not code.** "The script ran" is not "the shot works".
4. **1 Blender unit = 1 metre.** Always. Hero dimensions within ±10% of a cited source.
5. **Facts before script; script before render.** `factgate` blocks the render.

## Requirements

- Python **3.13** exactly (bpy 5.2.2 requires it)
- `ffmpeg` (present: 8.0.1)
- Optional: a Windows box with an NVIDIA GPU for final frames
