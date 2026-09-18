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

**State the conclusion first.** The comparator this slot was chosen against —
[@KnowArt, 432k likes](https://www.youtube.com/shorts/gjCfbgKbAbc) — opens with
*"hydraulic cylinders can push harder than they can pull"*. Title, first line and thumbnail are one
sentence. Draft 2 opened with a number about an object the viewer could not yet identify.

**Seven shots, not six, and none longer than 7 s.** The seven-second withhold is gone; it is now
2.5 s and carries both numbers against one unmoving object, which makes the "same oil, same
pressure" point in a single frame instead of by waiting.

**77 words at 154 wpm**, down from 120 at 240.

---

## h01 — the conclusion (0.0–4.0 s, 120 frames)

**Picture.** The cylinder, stood up on the frame's diagonal, driving out. Callout **55 t** in scene,
upper left. No title, no logo, no establishing wide.

> "A hydraulic cylinder pushes twice as hard as it pulls."

`ledger: s01.F006` · `s01.F001`

## h02 — the other number (4.0–7.0 s, 90 frames)

**Picture.** The same shot reversing. The callout changes to **27 t**, lower right.

> "Fifty-five tonnes pushing. Twenty-seven pulling."

`ledger: s01.F006`

## h03 — same oil, same pressure (7.0–9.5 s, 75 frames)

**Picture.** Both callouts on screen at once against one barely-moving object. 2.5 s.

> "Same oil. Same pump. Same pressure."

This replaces draft 2's seven-second withhold. The question *"so where does half the force go?"* is
cut entirely: the viewer was told the answer in h01, and the video's job from here is to earn it.

`ledger: s01.F001` — 350 bar, both directions

## h04 — inside (9.5–14.0 s, 135 frames)

**Picture.** Cut to the sectioned barrel, tight. Bore, brass piston, rod through the gland.

> "Force is pressure times area. The faces are not the same size."

`ledger: s01.F002` · `s01.F004`

## h05 — the ring (14.0–18.0 s, 120 frames)

**Picture.** Front on, orthographic. The ring (140 outer, 100 inner) beside the rod's circle.

> "The rod is in the way. What is left is a ring."

## h06 — the same size (18.0–23.0 s, 150 frames)

**Picture.** Cut to the ring re-formed as a solid circle, 98.0 mm, beside the rod's 100.0 mm.
**They are the same size.**

> "It does not look like half. Gather it up: the same size."

`ledger: s01.F004` · `s01.F005`

**Orthographic, and it must stay so.** An area comparison under a perspective lens argues for
whichever figure is nearer the lens (H24).

**A cut, not a morph.** `CHANNELS` is `{location, rotation, scale, spin}` — no shape interpolation.
The reveal is the comparison, not the tween.

**Why the ring is not simply shown as "half".** Measured on a probe: a 140/100 annulus reads as about
**a third** of a 140 disc, not a half. The number is right and the eye disagrees, which is why the
ring is re-formed rather than asserted. `critique.md` §5.

## h07 — three of them (23.0–30.0 s, 210 frames)

**Picture.** Three cylinders, no machine, stroking in sequence.

> "That is why an excavator curls in hard and pushes out weak. Three on the arm. None pull their
> weight."

**No excavator is modelled.** A boom, stick and bucket is S2's entire subject and this brief never
budgeted it. **The machine is never named** either: ledger `F003` rests on a trade parts listing and
carries `status: unknown`, so its treatment is `omit`.

---

## Pace

| shot | s | words | wpm |
|---|---|---|---|
| h01 | 4.0 | 10 | 150 |
| h02 | 3.0 | 5 | 100 |
| h03 | 2.5 | 6 | 144 |
| h04 | 4.5 | 12 | 160 |
| h05 | 4.0 | 12 | 180 |
| h06 | 5.0 | 12 | 144 |
| h07 | 7.0 | 20 | 171 |
| **total** | **30.0** | **77** | **154** |

Draft 2 was 120 words at 240 wpm and `voice` refused it. h05 and h07 are the tightest lines left; if
`voice` complains, h05 loses "What is left is" and h07 loses "That is why".

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
