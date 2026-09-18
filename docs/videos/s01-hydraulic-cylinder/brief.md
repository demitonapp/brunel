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
# Two parts, not one. A [[track]] targets a PART ID, so a rod inside the same
# part as its barrel cannot be animated separately from it. The stroke is a
# track on `cyl_rod`, which needs no generator support at all.
[[part]]
id  = "cyl_barrel"
gen = "cylinder_body"
[part.params]
bore     = 0.140     # m — ledger F002
stroke   = 1.30      # m
section  = 0.0       # 0..1 cutaway sweep — real geometry, not opacity (ROADMAP L2)
segments = 64        # H21 — 24 is visibly faceted on a chrome barrel at 1080×1920
smooth   = 30.0      # H21 — degrees, not a flag; keeps the end caps flat

[[part]]
id  = "cyl_rod"
gen = "cylinder_rod"
[part.params]
rod    = 0.100       # m — ledger F002
bore   = 0.140       # the piston is a bore-diameter disc on the end of the rod
stroke = 1.30

[[track]]              # the stroke. Beat 1 is this track and nothing else.
part    = "cyl_rod"
channel = "location"
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

**The rod is bore ÷ √2.** 140 / √2 = 99.0 → 100 mm. That puts half the piston's area under the rod
and leaves half as the ring. Rexroth prints the area ratio A1/A3 in its own catalogue column and the
standard series measures **1.96–2.08** across the range — so a realised cylinder lands within a point
of half, not on it: 153.94 → 75.40 is 48.98%. Four of Cat's five boom cylinders sit on the same
series. The video's whole reveal is that **half is a design decision, not an accident** — and the
narration must say "half", never "exactly half", because the callout on screen will not read 50.00%.

## Mechanism assertion — and why there is no `[shot.mechanism]` block

**There must not be one.** `MECHANISM_KEYS` is `{turns, pitch, advance, tolerance}`: the block exists
so `_check_mechanisms` can reconcile declared arithmetic against the **actual animation tracks** — a
jack that turns six times and advances nothing. The cylinder has no equivalent. Bore and rod fully
determine both areas; there is no independent track that could disagree with them. A block restating
them is exactly the tautology H7 names, and the validator would reject the keys anyway.

The check that earns its place compares the generator's output against **a number printed by someone
who does not know this repo exists.** Rexroth RE 17331 publishes, for 140 × 100, a piston area of
**153.94 cm²** and an annulus of **75.40 cm²**. Measured this session: derived 153.94 / 75.40 —
agreement to 0.002 cm². That assertion lives in `tests/run.sh`, specified in **H23**.

It fails if the generator ever computes the annulus from the bore *radius* instead of the bore
*area* — the most likely way to get this wrong, and one that still produces a plausible-looking
number.

## Gate status

`factgate` **blocks `--publish`**, and for exactly one reason: **no source is archived.**
`archive.org` rate-limited (HTTP 429) during the research session, so
`every_web_source_has_an_archive_url` fails. Five URLs need a Wayback snapshot and the snapshot URLs
pasted into the ledger. Nothing else is outstanding.

The `SOURCE NEEDED` markers are gone. The numbers came off documents.
