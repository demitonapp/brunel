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

**Draft 5 — review notes applied.** Four faults were called on draft 4 and all four were real:

1. **The pull block was not attached to the rod.** A measured 0.305 m gap; it floated. Fixed at the
   geometry: the rod tip sits at z = 0.10 and a 0.31 m block belongs centred at -0.055.
2. **Nothing indicated the block sizes.** The two loads lived in different shots with nothing to
   compare against. Both shots now share one camera and one rig position, and each load carries its
   own `label` — judging volume across a cut is the same mistake the ring already taught us.
3. **The section looked poor.** `bisect_plane` leaves the cut face OPEN, so the camera looked
   straight through the shell at the inside of the far wall. `_section_bm` now fills the cut, the
   wall went 15 mm to 22 mm so the cut face is a face rather than a sliver, and the crop widened
   from 105/150 mm to 52/88 mm so the object is legible.
4. **"It does not look like half. It is." asserted without evidence.** c13 now shows the published
   subtraction — 154 − 79 = 75 cm² — colour-coded to the two circles beneath it.

**And "the rod is in the way" was doing too much work.** The rod is *joined to the middle of that
face*, so there is nothing to push on there. That is the sentence.

---

## c01 — The conclusion (0.0–2.8 s)

> "A hydraulic cylinder pushes twice as hard as it pulls."

## c02 — Pushing (2.8–4.6 s)

> "Fifty-five tonnes pushing."

## c03 — Pulling (4.6–6.4 s)

> "Twenty-seven pulling."

## c04 — Same pressure (6.4–8.4 s)

> "Same oil. Same pressure."

## c05 — How big (8.4–10.2 s)

> *(silent — the figure carries it)*

## c06 — Push lifts this (10.2–12.3 s)

> "Push, and it lifts this."

## c07 — Pull lifts half (12.3–14.3 s)

> "Pull, and only this."

## c08 — Inside (14.3–16.3 s)

> "Force is pressure times area."

## c09 — Two faces (16.3–18.2 s)

> "The faces are not the same size."

## c10 — The whole piston (18.2–19.8 s)

> "Pushing: the whole face."

## c11 — The rod is in the way (19.8–22.0 s)

> "Oil pushes on the piston's face."

## c12 — A ring (22.0–24.8 s)

> "The rod takes the middle. Only a ring is left."

## c13 — The same size (24.8–27.8 s)

> "Ring and rod are the same size. Each is half."

## c14 — Three of them (27.8–30.0 s)

> "Three on the arm. None pull their weight."

## Pace

| shot | s | words | speech s | ceiling s |
|---|---|---|---|---|
| c01 | 2.8 | 10 | 3.57 | 3.78 |
| c02 | 1.8 | 3 | 1.07 | 2.43 |
| c03 | 1.8 | 2 | 0.71 | 2.43 |
| c04 | 2.0 | 4 | 1.43 | 2.70 |
| c05 | 1.8 | 0 | 0.00 | 2.43 |
| c06 | 2.1 | 5 | 1.79 | 2.84 |
| c07 | 2.0 | 4 | 1.43 | 2.70 |
| c08 | 2.0 | 5 | 1.79 | 2.70 |
| c09 | 1.9 | 7 | 2.50 | 2.56 |
| c10 | 1.6 | 4 | 1.43 | 2.16 |
| c11 | 2.2 | 6 | 2.14 | 2.97 |
| c12 | 2.8 | 10 | 3.57 | 3.78 |
| c13 | 3.0 | 10 | 3.57 | 4.05 |
| c14 | 2.2 | 8 | 2.86 | 2.97 |

**78 words across 30.0 s = 156 wpm.** `validate` refuses any shot whose narration cannot be
spoken in its own duration, and it fired twice while this draft was written.

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
