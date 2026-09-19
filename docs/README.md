# docs

Four kinds of document, and the rule for which is which.

```
docs/
  strategy/     what we are making and why. Changes when the evidence changes.
  videos/       one directory per video: the brief and the script. The editorial record.
  harness/      what is broken, what is next, and what has been decided. The engineering record.
  research/     the evidence base. Vendor claims, prices, licences, with sources and confidence.
    evidence/   the long-form receipts a summary compressed. Read the summary; keep these.
  archive/      superseded AND still cited. Kept only while something points into it.
```

## strategy/

| File | What it is |
|---|---|
| [`spec.md`](strategy/spec.md) | The product spec: the niche, the story engine, packaging, metrics. The audit that set the harness priorities. |
| [`slate.md`](strategy/slate.md) | **What we build, in order.** Supersedes `spec.md` §3. |
| [`reach-audit-2026-09-18.md`](strategy/reach-audit-2026-09-18.md) | Measured comparison against Animagraffs, Jared Owen, Practical Engineering and The B1M. The evidence behind the slate and D3/D4. |

## videos/

One directory per video — [the contract is in `videos/README.md`](videos/README.md). Facts, then
script, then spec, then render, in that order, every time.

## harness/

| File | What it is |
|---|---|
| [`backlog.md`](harness/backlog.md) | **What is open** — H19–H25 and C1–C6, ranked by which video they block. Closed items are in `git log` and `LESSONS.md`, not here. |
| [`decisions.md`](harness/decisions.md) | D1–D6. Dated, with the evidence and the reopening condition. |

## research/

Every vendor claim, price and licence finding with its source and a stated confidence. Cite it; do
not summarise it into strategy documents and then let the two drift.

**Licensing has one entry point.**
[`3d-asset-licensing-master-2026-09-17.md`](research/3d-asset-licensing-master-2026-09-17.md) — its
§1 is the table you act on. The four long-form source documents it was compressed from are in
[`research/evidence/`](research/evidence/README.md), which exists because a summary cannot carry
what could *not* be verified. Nothing in the repo currently links to any of it, while
`spec/ep01/legal/licences.json` still holds a placeholder that blocks `licencegate`; that gap is the open
action, not more research.

The newest entry is the first one bound to a shipping deliverable rather than to a tooling decision:
[`hydraulic-cylinder-datasheets-2026-09-18.md`](research/hydraulic-cylinder-datasheets-2026-09-18.md)
is where every number in `spec/s01/facts/s01.facts.json` comes from. It is the worked example of the
rule below — it became an assertion, and `factgate` evaluates it.

---

## The rule that matters

`docs/strategy/spec.md` §H17 measured **11,310 lines of markdown against 3,610 lines of code**, and
found four audited defects already written up as principles and shipped anyway. The metric is not
documents written. It is **documents that became an assertion.**

So: a new strategy document has to either replace one or delete an episode from the slate. A new
harness item has to name the check that will fire on it. If it does neither, it is prose, and this
repo already has too much.
