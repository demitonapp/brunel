# S1 — Why a hydraulic cylinder pushes harder than it pulls

**Format:** Short, 1080×1920, ~30 s
**Slot:** Phase 0, first. `docs/strategy/slate.md` §3.
**Long-form it feeds:** L1, *How an Excavator Actually Works*

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

> **Forty tonnes pushing. Twenty-two pulling. Same oil, same pressure.**

## Reuses / adds

| | |
|---|---|
| Reuses | nothing — `library/` is empty and this is where it starts |
| Adds to `library/` | `GEN cylinder` — parametric bore, rod, stroke; a section state; two port stubs |
| Downstream | S2 (×3 as the excavator's boom/stick/bucket), S5 (TBM thrust rams), L1, L2 |

The cylinder generator is the single most reused component on the whole slate. Build it
parametrically or build it three more times.

## The arithmetic

A representative 20-tonne-class excavator boom cylinder at working pressure:

| | |
|---|---|
| Bore | 120 mm → area **0.011310 m²** |
| Rod | 80 mm → area **0.005027 m²** |
| Annulus (bore − rod) | **0.006283 m²** |
| Working pressure | 350 bar = 35 MPa |
| **Extend force** | 0.011310 × 35e6 = **395.8 kN** ≈ **40.4 tonnes-force** |
| **Retract force** | 0.006283 × 35e6 = **219.9 kN** ≈ **22.4 tonnes-force** |
| **Ratio** | **0.556** — retract is 44% weaker |

> **SOURCE NEEDED.** These are plausible class-typical dimensions, computed here, **not read off a
> cited datasheet.** The arithmetic is correct; the inputs are not yet sourced. `factgate` must
> block `--publish` until a manufacturer cylinder datasheet is attached to
> `spec/s01/facts/s01.facts.json` and the numbers are re-derived from it. If the sourced bore and
> rod differ, the script's "forty / twenty-two" changes and the hook is re-recorded.

This is exactly the failure mode `docs/strategy/spec.md` §2.5 sells the channel against. Do not
ship the number because the sum checks out.

## Mechanism assertion

The spec must declare and the harness must check that the modelled geometry agrees with the claim:

```toml
[shot.mechanism]
bore = 0.120
rod  = 0.080
pressure = 35.0e6
extend_kn = 395.8
retract_kn = 219.9
```

Per H7, a mechanism block that restates three hand-written numbers is a tautology. This one must be
derived from the modelled cylinder's actual dimensions, not from the block.
