# Audience ledger

> `LESSONS.md` is the ratchet aimed at renders. **This is the ratchet aimed at the audience**, and it
> runs on the same rule: every entry names the *one change* that moved the number, or it does not
> belong here.
>
> This file must exist **before the first upload** so video one is a baseline rather than a memory.
> It is empty of results on purpose. An empty baseline is honest; a remembered one is not.

Defined by `docs/strategy/spec.md` §6. The slate it measures is `docs/strategy/slate.md`.

---

## 1. The four numbers, and the lever behind each

| Metric | What it actually measures | The lever |
|---|---|---|
| **CTR** (impressions → click) | the thumbnail and the title, nothing else | version the pack, keep the winner |
| **Retention at 0:30 / 2:00 / mid** | the cold open, then the ~90-second reveal cadence | version the hook, keep the winner |
| **Subscribers per 1,000 views** | trust — whether showing the receipts is working | cite on screen; ship the ledger page |
| **Search vs Browse/Suggested** | evergreen health vs discovery health | mechanism videos feed search; Shorts feed browse |

## 2. The versioning rule

The **hook**, the **title**, the **thumbnail** and the **last line** are versioned artifacts. Change
**one**, measure, keep the winner. Changing two teaches you nothing, which is the same reason a
render experiment moves one variable.

**Read the numbers at a fixed age**, not whenever you happen to look. Use **48 hours** and **28 days**
for every video, so rows are comparable. A number read at "about a week" is not a measurement.

## 3. The entries

One row per video, filled at 48 h and again at 28 d. Leave a cell blank rather than estimating it.

| Video | Published | CTR | Ret 0:30 | Ret 2:00 | Subs/1k | Search % | The one change | Result |
|---|---|---|---|---|---|---|---|---|
| _(none yet — S1 is unshipped)_ | | | | | | | | |

## 4. What counts as proof

`docs/strategy/spec.md` §15: *"the channel is working when `eval/audience.md` shows monotonic
improvement in CTR and 30-second retention across the first six uploads, and each entry names the one
change that moved it."*

Two honest cautions on that bar, recorded now rather than discovered at video four:

- **Six Shorts is a small sample.** Short-form view counts are long-tailed; one video going wide
  says more about the recommender than about the hook. Treat a single outlier as noise, and look at
  the median of the last three.
- **Monotonic is the wrong shape to expect.** The useful claim is that a change was made, measured,
  and kept or reverted — not that every number went up. Record reversions too. A change that made
  CTR worse is worth more here than one that did nothing, and it will be deleted from memory unless
  it is written down.

## 5. Benchmarks, for scale

Measured 2026-09-18, `docs/strategy/reach-audit-2026-09-18.md`. Context for what a number means, not
a target for year one.

| Channel | Subs | Videos | Median views |
|---|---|---|---|
| Practical Engineering | 4.83M | 250 | — |
| Jared Owen | 4.43M | 121 | 5.5M |
| The B1M | 4.07M | 923 | — |
| Animagraffs | 1.93M | 48 | 4.3M |

Both animation benchmarks took **7–11 years and 48–121 videos**, and both are currently below their
own median per video. The realistic 24-month marker is **100–300k subscribers**, if the format works.
