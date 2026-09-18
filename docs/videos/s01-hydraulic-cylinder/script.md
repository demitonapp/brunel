# S1 — script

**Target:** 30 s at 30 fps = 900 frames, 1080×1920.
**Voice:** flat, unhurried, no salesmanship. The number does the work.
**Rule:** every claim carries a ledger key. `SOURCE NEEDED` blocks `--publish`.
**Ledger:** `spec/s01/facts/s01.facts.json` · **Evidence:**
`docs/research/hydraulic-cylinder-datasheets-2026-09-18.md`

> **Revision, 2026-09-18.** The numbers changed when the datasheets landed. The old draft ran on an
> assumed 120 × 80 cylinder — a bore/rod pair that no manufacturer ships — and made the point as
> *"44% weaker"*. The sourced cylinder is **140 × 100**, and the honest answer is rounder and
> better: **half**. See the brief, "Why 140 × 100".

---

## Beat 1 — the hook (0.0–5.0 s, 150 frames)

**Picture.** The cylinder alone, three-quarter, extending. No context, no machine, no title.
Callout snaps on at 2.5 s: **54.9 t**.

> "This cylinder pushes with fifty-five tonnes of force."

Then the stroke reverses and the callout changes to **26.9 t**.

> "Pulling, it manages twenty-seven."

`ledger: s01.F006` — extend/retract force · `s01.F001` — working pressure

---

## Beat 2 — the withhold (5.0–12.0 s, 210 frames)

**Picture.** Both strokes again, side by side, same pressure gauge visible on both. The gauge does
not move. Hold on that.

> "Same oil. Same pump. Same pressure, both directions."
>
> "So where does half the force go?"

Nothing is explained yet. The question is the product. The line now says *half* rather than
gesturing at a fraction — it is the answer, stated early, and the viewer does not yet know why.

`ledger: s01.F001` — 350 bar both directions

---

## Beat 3 — the reveal (12.0–23.0 s, 330 frames)

**Picture.** **Explode, don't section.** The harness has no boolean, bisect or knife — and does not
need one here. Pull the two faces apart and show them whole: a full disc for the extend side, an
annulus for the retract side, the rod passing through the hole. `ROADMAP.md` L2 asks for a modelled
exploded state in real geometry, and two faces side by side read the area difference more directly
than a cut solid does.

Geometry, with no new generator: the full face is a thin `cylinder`; the annulus is a `ring` with
`thickness = bore_r − rod_r = 0.020 m` and a thin `height` — `ring`'s thickness is radial, so it is
an annular face already. Both carry `smooth = 30` and a raised `segments`, which is why those two
spec keys exist (see `docs/harness/backlog.md` H21).

> "Force is pressure times area — and the two faces aren't the same size."
>
> "Pushing, the oil gets the whole piston."
>
> "Pulling, the rod is already sitting in the middle of it. That area is gone. What's left is a
> ring."

Callout: bore area **153.94 cm²** → annulus **75.40 cm²**.

**Then the turn, and this is the video.** Hold on the two areas, side by side, and let them read as
the same size:

> "And that ring is exactly half. Not roughly — the rod is sized so it covers half the piston."
>
> "Bore, divided by root two."

Callout: **140 ÷ √2 = 99 → 100 mm**.

`ledger: s01.F004` — published areas · `s01.F005` — the √2 rod series · `s01.F002` — bore and rod

---

## Beat 4 — the so-what, and the hook into S2 (23.0–30.0 s, 210 frames)

**Picture.** Pull back for the first and only time: the same cylinder, now on an excavator boom.
One curl in, one push out.

> "Which is why an excavator curls a bucket in hard — and pushes it back out weak."
>
> "There are three of these on the arm, and none of them pull their own weight."

Last frame holds on the three cylinders, unlabelled. That is S2.

**The machine is never named.** Ledger `F003` — that this exact cylinder is a Cat 320 boom cylinder —
rests on a trade parts listing, not a Caterpillar document, and carries `status: unknown`. Its
on-screen treatment is therefore `omit`. "An excavator" is what the evidence supports, so "an
excavator" is what the narration says.

---

## Word count and pace

95 words across 30 s ≈ 190 wpm. Up from the previous draft's 78 because Beat 3 gained the √2 turn,
which is the reveal the whole video now rests on. If it reads rushed at read-through, Beat 2 gives up
the "So where does half the force go?" line — the reveal cannot be cut, the withhold can.

## Caption policy

Burned in, central 1320 px (L1), two weights, one typeface. **The numbers — 54.9 t, 26.9 t,
153.94 cm² and 75.40 cm² — ride in the captions**, and that is not a compromise on "nothing
guessed". Captions are generated from the spec's narration and `factgate` binds narration to the
ledger by hash, so a number in a caption is exactly as gated as one in a tracked callout.

3D-tracked callouts (C1) are an **L2 upgrade, deliberately not built for S1**. The reveal in Beat 3
is carried by *geometry and material* — the annulus is a differently-coloured face, not a label —
which reads harder than a number anyway. C1 arrives at **S3**, where a leader line anchored to a
moment arm is genuinely the point. See `docs/harness/backlog.md` Part V.

## Open questions before the spec is written

1. ~~Source the bore and rod.~~ **Done.** Rexroth RE 17331 and the Cat 320 spec sheet; see the
   evidence doc. The one remaining gate blocker is archiving, not sourcing.
2. **Does the section in Beat 3 read at 1080×1920 on a phone?** Storyboard it first
   (`render --stills`) — that is the whole point of the stills pass.
3. **Do the two areas read as "half" without the number?** The turn only lands if the annulus
   visibly looks like half the disc. If it does not, the callout is carrying the reveal alone and
   Beat 3 needs a different staging — an overlay of the ring onto the disc, twice.
4. **Is the gauge in Beat 2 legible, or is it a caption?** A needle that does not move is the
   clearest possible way to say "pressure is not the variable", but only if it reads at thumb size.
