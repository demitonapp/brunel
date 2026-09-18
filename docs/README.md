# docs

Four kinds of document, and the rule for which is which.

```
docs/
  strategy/     what we are making and why. Changes when the evidence changes.
  videos/       one directory per video: the brief and the script. The editorial record.
  harness/      what is broken, what is next, and what has been decided. The engineering record.
  research/     the evidence base. Vendor claims, prices, licences, with sources and confidence.
  archive/      superseded. Kept for the audit trail. Never edited, never cited as current.
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
| [`backlog.md`](harness/backlog.md) | H1–H24 and C1–C6, ranked by which video they block. |
| [`decisions.md`](harness/decisions.md) | D1–D6. Dated, with the evidence and the reopening condition. |

## research/

Unchanged and untouched by the restructure. Every vendor claim, price and licence finding with its
source and a stated confidence. Cite it; do not summarise it into strategy documents and then let
the two drift.

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
