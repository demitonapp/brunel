# S1 — Why a hydraulic cylinder pushes harder than it pulls

**Format:** Short, 1080×1920, ~30 s
**Slot:** Phase 0, first. `docs/strategy/slate.md` §3.
**Long-form it feeds:** L1, *How an Excavator Actually Works*
**Evidence:** `docs/research/hydraulic-cylinder-datasheets-2026-09-18.md`
**Ledger:** `spec/s01/facts/s01.facts.json`

---

## The one mechanism

> A double-acting cylinder is not symmetrical: the rod occupies part of the piston face on the
> retract side, so the same oil at the same pressure has less area to push on coming back — and the
> cylinder is markedly weaker pulling than pushing.

One sentence. One mechanism. Nothing else is in this video.

## Why it earned the first slot

**Measured 2026-09-18** (`docs/strategy/slate.md` §2):

| | Best long-form | Best Shorts |
|---|---|---|
| "how a hydraulic cylinder works" | 349k | **14M**, 840k, 380k |

The 14M-view Short is literally this mechanism — *"Hydraulic Cylinders Push Harder Than They Pull"*.
Demand for the idea is proven at scale and the best long-form treatment of it is 349k, which is the
signature of an unoccupied query.

**And it is the cheapest object this harness can make.** A barrel, a rod, a piston, two ports. It
goes first as much to exercise the repaired delivery path on something that costs an afternoon as
to get views. H1–H18 are merged, but they have never been run end to end on a spec written after
the fix — S1 is the first one, and a fix proven only on fixtures is a fix with one witness.

## The one number

> **Whatever it pushes with, it pulls with half.**

Not a percentage. Not a figure that needs defending. **Half** — and on purpose.

## Reuses / adds

| | |
|---|---|
| Reuses | nothing — `library/` is empty and this is where it starts |
| Adds to `library/` | `GEN cylinder` — parametric bore, rod, stroke; a section state; two port stubs |
| Downstream | S2 (×3 as the excavator's boom/stick/bucket), S5 (TBM thrust rams), L1, L2 |

The cylinder generator is the single most reused component on the whole slate. Build it
parametrically or build it three more times.

**One generator, not five.** Single-acting is one port instead of two; tie-rod versus welded is an
end-cap treatment; both are parameters. Telescopic is genuinely different geometry and is genuinely
unslated — nothing through Phase 2 uses it. `library/README.md` rule 2: parameterise, never fork.

```toml
[[object]]
gen     = "cylinder"
bore    = 0.140      # m — ledger F002
rod     = 0.100      # m — ledger F002
stroke  = 1.30       # m
extend  = 0.0        # 0..1, animatable — the whole of beat 1
ends     = "welded"  # "welded" | "tie_rod"
ports    = 2         # 2 = double-acting, 1 = single
section  = 0.0       # 0..1 cutaway sweep — real geometry, not opacity (ROADMAP L2)
segments = 64        # H21 — 24 is visibly faceted on a chrome barrel at 1080×1920
smooth   = 30.0      # H21 — degrees, not a flag; keeps the end caps flat
```

`section` is the only parameter that earns real work. Everything else is a few calls to the `_cyl`
helper that `harness/generators.py` already has — now that **H21** has made `segments` spec-settable
and added per-part `smooth` shading, both of which this component needs and neither of which existed
when this brief was first written.

## The arithmetic

**140 mm bore × 100 mm rod at 350 bar.** Every input is now cited.

| | | Source |
|---|---|---|
| Bore | 140 mm → **153.94 cm²** | Rexroth RE 17331, published |
| Rod | 100 mm → **78.54 cm²** | Rexroth RE 17331, published |
| Annulus (bore − rod) | **75.40 cm²** | Rexroth RE 17331, published |
| Working pressure | 350 bar = 35 MPa | Cat 320 spec sheet, "Maximum Pressure – Equipment – Normal" |
| **Extend force** | 0.015394 × 35e6 = **538.8 kN** ≈ **54.9 tonnes-force** | derived |
| **Retract force** | 0.007540 × 35e6 = **263.9 kN** ≈ **26.9 tonnes-force** | derived |
| **Ratio** | **0.490** — retract is **half** | derived |

**Why 140 × 100 and not the 120 × 85 this brief used to assume.** 120 × 80 does not exist — the Cat
320 boom cylinder ships in five bore/rod pairs and none of them is 120/80. 140 × 100 is the one pair
that appears in *both* the Rexroth catalogue and the Cat parts list, which makes it the only
cross-confirmed dimension on the board.

**The rod is bore ÷ √2.** 140 / √2 = 99.0 → 100 mm. That puts exactly half the piston's area under
the rod, leaving exactly half as the ring. Rexroth sells it as the φ = 2 series and prints the ratio
in its own catalogue column; four of Cat's five boom cylinders are on the same series. The video's
whole reveal is that **half is a design decision, not an accident.**

## Mechanism assertion

The spec declares it and the harness checks it — but not by restating the inputs (H7 calls that a
tautology). The check that earns its place is against **the manufacturer's published areas**:

```toml
[shot.mechanism]
bore = 0.140
rod  = 0.100
pressure = 35.0e6
# Rexroth RE 17331 publishes A1 = 153.94 cm2 and A3 = 75.40 cm2 for this pair.
# GEN cylinder derives both from the modelled geometry; they must agree.
published_bore_area_cm2    = 153.94
published_annulus_area_cm2 = 75.40
tolerance_cm2 = 0.01
```

Measured this session: derived 153.94 / 75.40 against published 153.94 / 75.40 — agreement to
0.002 cm². A generator whose output can be compared against a printed table should be.

## Gate status

`factgate` **blocks `--publish`**, and for exactly one reason: **no source is archived.**
`archive.org` rate-limited (HTTP 429) during the research session, so
`every_web_source_has_an_archive_url` fails. Five URLs need a Wayback snapshot and the snapshot URLs
pasted into the ledger. Nothing else is outstanding.

The `SOURCE NEEDED` markers are gone. The numbers came off documents.
