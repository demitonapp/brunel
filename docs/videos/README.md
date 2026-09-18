# Videos

One directory per video, named `<spec id>-<slug>`. The directory is the editorial record; the
`spec/` tree is the buildable one. They are deliberately separate — a spec is a compiler input and
a brief is an argument, and mixing them is how the argument stops being reviewable.

```
docs/videos/<id>-<slug>/
    brief.md      why this video exists, and the numbers that earned it the slot
    script.md     the narration, beat by beat, with timings
spec/<id>/
    <id>.toml     the buildable spec; its narration fields come FROM script.md
    facts/        the fact ledger, gated by factgate and published per video
```

## The order of work, and it is not negotiable

**Facts, then script, then spec, then render.** `README.md` principle 8. A script written against a
shot list is a lecture; a shot list written against a script is a video. Every time this has been
done the other way round in this repo the result was re-shot.

## What a brief must carry

1. **The one mechanism, in one sentence.** If it takes two, it is two videos
   (`docs/strategy/spec.md` §5, "the one system per video rule").
2. **The measured demand that earned the slot** — best long-form and best Shorts on the query, with
   the date read. No slot is awarded on a hunch; see `docs/strategy/slate.md` §2.
3. **What it reuses and what it adds to `library/`.** The slate's order depends on this being true.
4. **The one number** the viewer will repeat.

## What a script must carry

Timed beats, the narration verbatim, and — for every factual claim — the ledger key that backs it.
A claim with no ledger key does not ship: `factgate` blocks `--publish`, and the public ledger page
is the channel's whole differentiation (`docs/strategy/spec.md` §2.5).

Unsourced numbers are marked **`SOURCE NEEDED`** in the script until a primary source is attached.
That marker is not a formality — it is the difference between this channel and the ones it is
trying to beat.

## Status

| id | video | brief | script | spec | rendered |
|---|---|---|---|---|---|
| s01 | Why a hydraulic cylinder pushes harder than it pulls | yes | yes | no | no |
| s02–s08 | see `docs/strategy/slate.md` §3 | — | — | — | — |

Directories are created when a video starts, not when it is planned. The slate is the plan; empty
stub folders are just rot with a filename.
