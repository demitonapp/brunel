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

> **Restaged 2026-09-18 after a storyboard probe.** The original staging — "two annotated faces, one
> each side of the piston" — **cannot work**, and the probe proved it in two steps. A side-on section
> shows a piston face *edge-on*, as a line, so it can never read as an area. And when the two areas
> are shown properly, front-on and to scale, **a 140/100 annulus does not look like half a 140 disc.**
> It reads as about a third. The arithmetic is right and the eye disagrees. Frames:
> `scratchpad/probe/v4_beat3.png` (faces edge-on) and `areas_01.png` (the ring reading as a third).

**3a — the section, 12.0–16.0 s.** Three-quarter, the barrel cut away, rod and piston inside. This
beat is context, not the reveal: it establishes that the rod occupies the middle of the bore.

> "Force is pressure times area — and the two faces aren't the same size."
>
> "Pushing, the oil gets the whole piston."

**3b — front on, orthographic, 16.0–19.0 s.** Cut to the piston face square on. The rod's circle
lifts out of the middle and moves aside. What is left is a ring.

> "Pulling, the rod is in the way. What's left is a ring."

**3c — the turn, 19.0–23.0 s.** **Cut** to the ring re-formed as a solid circle, sitting beside the
rod's circle. **They are the same size.**

*A cut, not a morph.* `CHANNELS` is `{location, rotation, scale, spin}` — the harness has no shape
interpolation, so the ring cannot be animated into a disc. Two parts, each visible in one shot: the
annulus in 3b, the equal-area disc in 3c. The reveal is the **comparison**, not the transformation,
and a hard cut between two held frames states it more plainly than a tween would.

> "It doesn't look like half. It is."
>
> "Gather that ring into a circle, and it's the same size as the rod that took the space."

Callout: bore **153.94 cm²** → ring **75.40 cm²** · rod **78.54 cm²**.

**Why this is the honest version and not a trick.** The two pieces genuinely are near-equal: 75.40
against 78.54 cm², a 4% difference, because the rod is a stock 100 mm rather than the 98.99 mm that
bore/√2 asks for. That 4% *is* the gap between 49% and 50%, and it is the reason the narration says
"half" and never "exactly half". Re-formed as a solid disc the ring is 98.0 mm across against the
rod's 100.0 mm — the same size to the eye, and the small difference is real rather than hidden.

**The camera must be orthographic for 3b and 3c.** An area comparison under a perspective lens is
not a comparison; the nearer figure wins. **H24 is built**, so the spec can now say so:

```toml
[[camera]]
id = "cam_areas"
ortho_scale = 0.62      # the frame width in metres. Mutually exclusive with lens_mm.
loc = [0.0, -1.2, 0.0]
look_at = [0.0, 0.0, 0.0]
```

`ledger: s01.F004` — published areas · `s01.F005` — the √2 rod series · `s01.F002` — bore and rod

---

## Beat 4 — the so-what, and the hook into S2 (23.0–30.0 s, 210 frames)

**Picture.** Pull back for the first and only time — to **three cylinders alone**, no machine. Boom,
stick and bucket sizes, arranged in the attitude they sit in on an arm, each stroking once. Nothing
else in frame.

> "Which is why an excavator curls a bucket in hard — and pushes it back out weak."
>
> "There are three of these on the arm, and none of them pull their own weight."

Last frame holds on the three, unlabelled. That is S2.

**No excavator is modelled, deliberately.** The original staging put the cylinder on a boom, which
means a boom, a stick and a bucket — the whole kinematic chain, which is **S2's entire subject** and
geometry this video's brief never budgeted. Three bare cylinders carry the same line: the narration
supplies the machine, and the frame supplies the mechanism. It also makes the last frame a stronger
hook, because three unexplained cylinders is a question and an excavator is an answer.

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
