# S1 — script

**Target:** 30 s at 30 fps = 900 frames, 1080×1920.
**Voice:** flat, unhurried, no salesmanship. The number does the work.
**Rule:** every claim carries a ledger key. `SOURCE NEEDED` blocks `--publish`.
**Ledger:** `spec/s01/facts/s01.facts.json` · **Evidence:**
`docs/research/hydraulic-cylinder-datasheets-2026-09-18.md` ·
**Critique that produced this draft:** `critique.md`

> **Draft 3, 2026-09-19 — the Tier 1 re-edit.** Draft 2 was rendered, verified and watched. It is
> 30 seconds in which the subject occupies **1.9–2.4% of the frame**, opens on a wide establishing
> shot (a named cliff trigger, where 50–60% of all drop-off happens), withholds for seven seconds,
> and carries **240 wpm** of narration that `voice` refused to record. The full analysis is in
> `critique.md`. This draft changes the edit, not the facts.
>
> **Draft 2's structure is kept below, under "Superseded".**

---

## The shape of the re-edit

**Draft 4 — Tiers 1–3.** Fourteen shots, none over 3 s. Draft 2 ran six shots at 5.0 s average,
which is documentary pacing in a swipe feed.

**State the conclusion first.** The comparator this slot was chosen against —
[@KnowArt, 432k likes](https://www.youtube.com/shorts/gjCfbgKbAbc) — opens with *"hydraulic
cylinders can push harder than they can pull"*. Title, first line and thumbnail are one sentence.

**Show a consequence, not only a mechanism.** c06 and c07 are new: the same cylinder at the same
pressure lifts a block pushing, and half a block pulling. The pull rig is mounted **inverted**,
because a cylinder pulls by retracting and the only way to lift with it is to hang the load beneath.

**Say how big it is.** c05 puts `crew` — 1.70 m, measured, assertion-checked — beside the cylinder.
Draft 2 ran thirty seconds without ever establishing scale.

**The numbers are in the scene.** `label` geometry, not caption text. Draft 2 had none.

---

## c01 — The conclusion (0.0–3.0 s)

> "A hydraulic cylinder pushes twice as hard as it pulls."


## c02 — Pushing (3.0–4.8 s)

> "Fifty-five tonnes pushing."


## c03 — Pulling (4.8–6.6 s)

> "Twenty-seven pulling."


## c04 — Same pressure (6.6–8.6 s)

> "Same oil. Same pressure."


## c05 — How big (8.6–10.6 s)

> *(silent — the figure does the talking)*


## c06 — Push lifts this (10.6–12.8 s)

> "Push, and it lifts this."


## c07 — Pull lifts half (12.8–15.0 s)

> "Pull, and only this."


## c08 — Inside (15.0–17.2 s)

> "Force is pressure times area."


## c09 — Two faces (17.2–19.2 s)

> "The faces are not the same size."


## c10 — The whole piston (19.2–21.0 s)

> "Pushing, the whole piston."


## c11 — The rod is in the way (21.0–23.0 s)

> "Pulling, the rod is in the way."


## c12 — A ring (23.0–25.1 s)

> "What is left is a ring."


## c13 — The same size (25.1–27.6 s)

> "It does not look like half. It is."


## c14 — Three of them (27.6–30.0 s)

> "Three on the arm. None pull their weight."



## Pace

| shot | s | words | speech s | ceiling s |
|---|---|---|---|---|
| c01 | 3.0 | 10 | 3.57 | 4.05 |
| c02 | 1.8 | 3 | 1.07 | 2.43 |
| c03 | 1.8 | 2 | 0.71 | 2.43 |
| c04 | 2.0 | 4 | 1.43 | 2.70 |
| c05 | 2.0 | 0 | 0.00 | 2.70 |
| c06 | 2.2 | 5 | 1.79 | 2.97 |
| c07 | 2.2 | 4 | 1.43 | 2.97 |
| c08 | 2.2 | 5 | 1.79 | 2.97 |
| c09 | 2.0 | 7 | 2.50 | 2.70 |
| c10 | 1.8 | 4 | 1.43 | 2.43 |
| c11 | 2.0 | 7 | 2.50 | 2.70 |
| c12 | 2.1 | 6 | 2.14 | 2.84 |
| c13 | 2.5 | 8 | 2.86 | 3.38 |
| c14 | 2.4 | 8 | 2.86 | 3.24 |

**73 words across 30.0 s = 146 wpm.** Draft 2 was 120 words at 240 wpm and `voice`
refused it. `validate` now refuses any shot whose narration cannot be spoken inside its own
duration, so this can no longer be discovered after a render.

## Caption policy

Burned in, central 1320 px (L1). The two forces are **in-scene `label` geometry**, not caption text —
`critique.md` §4.3 records that draft 2 shipped with no callouts at all, so the one number the brief
said the viewer would repeat never appeared on screen.

## Still open

1. **Subject coverage.** Draft 2 measured 1.9–2.4%. Target is 20–45%. Tracked per shot in
   `critique.md` §1; the geometric ceiling for a whole 12:1 cylinder is lower than for a crop, so
   h01–h03 crop and h04–h06 do not.
2. **No scale reference** anywhere in 30 s. `library/` has `crew`, measured. Tier 2.
3. **The film does not demonstrate a consequence** — no load is lifted and then not pulled. Tier 2.
4. **Silent.** No sound design. Tier 3.

---

## Superseded — draft 2's structure

Six shots: hook (5 s) · withhold (7 s) · section (4 s) · ring (3 s) · same size (4 s) · three (7 s).
120 words, 240 wpm, no callouts, 1.9–2.4% coverage, opens on a wide establishing shot. Rendered in
full at `ece0b64`; the critique is `critique.md`. Kept because the faults are the argument for this
draft, and a draft with no record of what it replaced invites the same edit back.
