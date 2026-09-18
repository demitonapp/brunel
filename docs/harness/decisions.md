# Decisions

One entry per decision that is expensive to re-litigate. Dated, with the evidence that forced it
and the condition that would reopen it. If a decision has no reopening condition, say so.

Format is deliberately short. The evidence lives in `docs/research/` and `docs/strategy/`; this
file exists so nobody re-argues a settled question from memory.

---

## D1 — `local` is the shipping path. Generative is off the critical path.

**Decided 2026-09-18.** Confirms and hardens the conclusion already reached in
`docs/strategy/spec.md` §8.7.

**Why.** Measured on the only paid generation this repo has run (`renders/ad02/generated-wan/`):
iron rendered cobalt blue, the clay the narration promises deleted from frame, motion on the payoff
shot attenuated 52% against its own depth control, four incompatible grades across five shots, and
a payoff shot black end to end.

**Why the new slate makes it worse, not better.** `WanVaceBackend.requires = ("depth",)`. The Phase
0 subjects are the worst case for depth-only conditioning: a lattice mast is thin struts, rope
reeving is eight parallel thin lines, and a hydraulic cylinder is a smooth barrel whose depth pass
is a featureless gradient — which §8.7 already measured the model rendering as a void. And the new
slate removed generative's one legitimate job: an 1825 clay tunnel has atmosphere to add, a
hydraulic cylinder does not. Every shot in Phase 0 and Phase 1 carries a mechanical claim, and
§8.7's own rule excludes generative from exactly those.

**The economics finish the argument.** The strategy is to iterate a hook 30 times. At $0.08/s that
is ~$100 per full pass on three long-forms and ~$1,000 across ten iterations, none of it
reproducible. `local` is free and deterministic, which is the only reason 30 iterations is a plan.

**Not deleted.** `backend.py` stays. It is one class per backend, it costs nothing to keep, and it
is the portability hedge. This is a change to the plan, not to the code.

**Reopens when** a backend accepts more than one control pass — depth *and* segmentation *and*
edge, the Cosmos shape. Until then it is an atmosphere tool for a slate with no atmosphere.

---

## D2 — Render on the M1 through Phase 0. Defer the node.

**Decided 2026-09-18.**

**Why.** Measured, not extrapolated (H19): **26.86 s/frame** at 1080×1920 @ 8 spp on M1 CPU
Cycles. A 30-second Short is 900 frames — **6.7 hours, one overnight**. Eight Shorts across eight weeks is one overnight a
week, which is free and already fits the cadence.

**Why not sooner.** The 3080's OptiX throughput is `not_measured`, and sizing a node from an
extrapolation is how `render-bench.json` produced a number that turned out to be optimistic by
about 4×. Phase 0 produces the real curve; buy or build against that.

**Render on CPU, not Metal.** Measured in `render-bench.json`: Metal was *slower* than CPU on the
7-core M1 GPU. Do not assume the Mac's GPU is the fast path.

**Reopens at Phase 1**, which needs the node on two counts: **94 h** per 7-minute cut, and **~29 GB**
of frames against 12 GiB free (H20).

---

## D3 — The Australia-only clause is dropped.

**Decided 2026-09-18.** Reverses `docs/strategy/spec.md` §1 ("Australia only, for at least 12
months. Every subject Australian.").

**Why.** Measured penalty: Jared Owen's Sydney Opera House video returned **1.7M views against his
5.5M median** — 31%, same creator, same format, same quality, on a landmark far better known than
anything on the original slate. Seven of the twelve original episodes had effectively no global
search demand, and one of the two globally recognised subjects was already made by a 4.4M-subscriber
channel three years ago.

**What replaces it.** Construction-plant mechanism evergreens: globally searched, no geography
required, and squarely inside Demiton's domain. It is the only subject class that serves reach and
the sponsor at the same time. See `docs/strategy/slate.md`.

**What is kept.** The mechanism-first, sourced wedge and the public fact ledger. Those were never
the geographic part, and they are still the moat.

**Reopens at Phase 3**, where the Australian subjects return as the payoff of a proven format
rather than the opening bet.

---

## D4 — Reach first, sponsor second.

**Decided 2026-09-18.** Resolves the contradiction named in `reach-audit-2026-09-18.md` §1.

The channel optimises for reach; Demiton is a bumper, a link and a case-study page — the model that
already works for the largest construction channel on the platform. The B2B work (piling, batching,
site logistics, customer project visualisation) uses the same harness and the same specs but is
distributed on LinkedIn and in industry press, measured in named accounts rather than views.

**They are two products sharing a toolchain.** Mixing them dilutes both: the slate stops passing the
reach test, and the B2B work waits behind a YouTube cadence it does not need.

**Reopens if** the sponsor relationship becomes the primary revenue line, at which point the
optimisation target genuinely changes and this file should say so.
