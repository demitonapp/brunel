# The slate — what we build, in order

> **Supersedes `docs/strategy/spec.md` §3 ("The 12-month slate").** That slate was twelve
> Australian-history episodes opening on a Snowy Mountains flagship. This one is ordered by
> measured demand and by which geometry the previous item leaves behind.
>
> The evidence is `docs/strategy/reach-audit-2026-09-18.md`. The decisions it forced are
> `docs/harness/decisions.md`.

---

## 1. The two rules this order obeys

**Demand is measured, not assumed.** Every item carries the best long-form on its query and the
best Shorts on the same topic, read off YouTube on 2026-09-18. The gap between those two numbers
*is* the opportunity: high Shorts demand plus weak long-form supply is an unoccupied query.

**Each item pays for the next.** The order is chosen so the geometry compounds. `library/` is
empty; by L3 it should hold cylinders, kinematic chains, lattice, rope, tracks, bore and lining —
which is the ratchet in `ROADMAP.md` §5 actually working for the first time, on real deliverables.

**A Short is a shot from a long-form, built early.** Not a trailer cut from a finished video —
the reverse. The Short ships first, the audience tells us which mechanism moment lands, and the
long-form opens on the one that won. That inverts `docs/strategy/spec.md` §4, deliberately.

---

## 2. Measured demand, 2026-09-18

| Query | Best long-form | Best Shorts | Read |
|---|---|---|---|
| tunnel boring machine | **75k** | 7.1M, 4.3M, 2.4M, 2.3M, 1.6M | demand proven, **query unoccupied** |
| excavator hydraulics | 1.8M, 764k | **14M**, 3.8M, 638k, 311k | strong, no premium supply |
| hydraulic cylinder *(principle)* | 349k | **14M**, 840k, 380k | principle Shorts >> principle long-form |
| tower crane | **7.5M** | 2.4M | demand proven, **incumbent holds it** (6 yrs old) |
| concrete pump | 661k (7 yrs old) | 268k, 87k | weak — not Phase 1 |
| piling / foundations | 155k | — | **no reach**; B2B asset only |

Two findings drive the order. **Principle beats machine at Short length** — "Hydraulic Cylinders
Push Harder Than They Pull" has 14M views while the best hydraulic-cylinder long-form has 349k.
And **an unoccupied query beats a busy one** — the TBM's best dedicated animation is 75k against
7.1M on a Short, which is a wider gap than the tower crane's, where a good incumbent already sits
on 7.5M.

---

## 3. Phase 0 — eight Shorts

20–40 s, 1080×1920, one mechanism each. Every one is a shot from a Phase 1 long-form, built early.

| # | Short | Reuses | New geometry | Long-form |
|---|---|---|---|---|
| **S1** | Why a hydraulic cylinder pushes harder than it pulls | — | rod, bore, seal | L1 |
| **S2** | Three joints, one pump — boom, stick, bucket | S1 cylinder ×3 | kinematic chain | L1 |
| **S3** | Why an excavator doesn't tip | S2 | counterweight; **first C1 callout** | L1 |
| **S4** | The shield advances four and a half inches | `ad02`, already rendered | **none** | — |
| **S5** | A TBM's thrust ram cycle | S1 cylinders, `ep01` bore + clay | cutterhead | L2 |
| **S6** | Building a ring behind the machine | S5 bore, `ep01` lining | segment erector | L2 |
| **S7** | A tower crane climbing itself | — | parametric lattice, climbing frame | L3 |
| **S8** | Why eight falls of rope lift eight times the load | S7 | reeving, hook block | L3 |

**S1 is first because it is the cheapest object the harness can make** — a rod and a barrel —
against the highest-proven hook on the board. It exists as much to force H1/H2/H3 closed on
something that costs an afternoon as it does to get views.

**S4 costs no new geometry at all.** It re-cuts `ad02` through the fixed delivery path, and its
only job is to prove `deliver` works end to end (H4). If S4 cannot be produced by one command, the
pipeline is not finished, whatever the other seven look like.

**Sponsor conversation opens after S8** — eight pieces, real view numbers, and S5/S6/S7 sitting
directly in a plant owner's world. A sponsored branded machine is also the first real test of
`licencegate` and of the per-asset licence register — H5 wired the gate, but no shipped cut has a
fact ledger yet. Write one before the call, not after.

---

## 4. Phase 1 — three long-forms, 6–8 minutes

| # | Video | Why here | Already built |
|---|---|---|---|
| **L1** | **How an Excavator Actually Works** | simplest mechanism, strongest Shorts signal, no premium incumbent | S1, S2, S3 |
| **L2** | **How a Tunnel Boring Machine Works** | widest supply gap on the board; `ep01` carries the bore | S5, S6 |
| **L3** | **How a Tower Crane Builds Itself** | 7.5M proves the demand; incumbent is 6 years old and covers erection only | S7, S8 |

6–8 minutes, not 10–18. Both benchmark channels launched at 1–4 minutes and grew scope with the
audience; opening at documentary length is the hardest possible first attempt at the point of least
knowledge about what the audience wants.

**Phase 1 needs the render node.** Measured 2026-09-18: **26.86 s/frame** and 2.3 MB/frame at
1080×1920 @ 8 spp on M1 CPU Cycles. A 7-minute cut is **94 hours and ~29 GB** — against 12 GiB
free. A 30 s Short is 6.7 hours, which is one overnight. See H19 and H20.

---

## 5. Phase 2 — verify before committing

Crawler crane, concrete batching plant, roadheader, slipform, dragline, asphalt train.

**None of these have been measured.** Concrete pump and piling both came back weak, so the category
does not carry on its own. Run the same two-query check in §2 before any of them earns a slot, and
record the numbers here.

---

## 6. Phase 3 — the ones that need C2 and C3

Hydro station → pumped hydro → the Snowy flagship, in that order.

By then C1 exists (built incrementally from S3), the tunnelling library is two long-forms deep, and
the flagship is cheap instead of being the hardest first attempt. This is where the original slate's
Australian subjects return — as the payoff of a proven format, not as the opening bet.

---

## 7. What is deliberately not on this list

**Piling, batching plants, site logistics.** 155k views at the top of the query. They are real
Demiton subjects and they have no reach, so they are the B2B asset — same harness, same specs,
LinkedIn and industry press rather than YouTube discovery. Do not mix them into the slate; they
fail the reach test and dilute the channel's one promise.

**Anything requiring a named, Australian-only subject, before Phase 3.** The measured penalty is in
`reach-audit-2026-09-18.md` §3: 31% of median, on a landmark better known than anything in the
original slate.
