# S1 — script

**Target:** 30 s at 30 fps = 900 frames, 1080×1920.
**Voice:** flat, unhurried, no salesmanship. The number does the work.
**Rule:** every claim carries a ledger key. `SOURCE NEEDED` blocks `--publish`.

---

## Beat 1 — the hook (0.0–5.0 s, 150 frames)

**Picture.** The cylinder alone, three-quarter, extending. No context, no machine, no title.
Callout snaps on at 2.5 s: **40.4 t**.

> "This cylinder pushes with forty tonnes of force."

Then the stroke reverses and the callout changes to **22.4 t**.

> "Pulling, it manages twenty-two."

`ledger: s01.extend_kn` · `s01.retract_kn` — **SOURCE NEEDED**

---

## Beat 2 — the withhold (5.0–12.0 s, 210 frames)

**Picture.** Both strokes again, side by side, same pressure gauge visible on both. The gauge does
not move. Hold on that.

> "Same oil. Same pump. Same pressure, both directions."
>
> "So where does half the force go?"

Nothing is explained yet. The question is the product.

---

## Beat 3 — the reveal (12.0–23.0 s, 330 frames)

**Picture.** Section the cylinder — real geometry, not opacity (`ROADMAP.md` L2). Two annotated
faces, one each side of the piston. The extend face fills; the retract face fills, and the rod's
circle is subtracted from it in front of the viewer.

> "Force is pressure times area — and the two faces aren't the same size."
>
> "Pushing, the oil gets the whole piston."
>
> "Pulling, the rod is already sitting in the middle of it. That area is gone. What's left is a
> ring."

Callout: bore area **0.0113 m²** → annulus **0.0063 m²**.

`ledger: s01.bore` · `s01.rod` · `s01.bore_area` · `s01.annulus_area` — **SOURCE NEEDED**

---

## Beat 4 — the so-what, and the hook into S2 (23.0–30.0 s, 210 frames)

**Picture.** Pull back for the first and only time: the same cylinder, now on an excavator boom.
One curl in, one push out.

> "Which is why an excavator curls a bucket in hard — and pushes it back out weak."
>
> "There are three of these on the arm, and none of them pull their own weight."

Last frame holds on the three cylinders, unlabelled. That is S2.

---

## Word count and pace

78 words across 30 s ≈ 156 wpm. Deliberately under-written: the reveal in Beat 3 needs air, and
`ROADMAP.md` L0 asks for at least one held frame per 10 s.

## Caption policy

Burned in, central 1320 px (L1), two weights, one typeface. The two numbers — **40.4 t** and
**22.4 t** — are rendered as 3D-tracked callouts in the scene, not as caption text: a dimension that
lives in the edit is a dimension nothing can check.

## Open questions before the spec is written

1. **Source the bore and rod.** Everything above is provisional until then.
2. **Does the section in Beat 3 read at 1080×1920 on a phone?** Storyboard it first
   (`render --stills`) — that is the whole point of the stills pass.
3. **Is the gauge in Beat 2 legible, or is it a caption?** A needle that does not move is the
   clearest possible way to say "pressure is not the variable", but only if it reads at thumb size.
