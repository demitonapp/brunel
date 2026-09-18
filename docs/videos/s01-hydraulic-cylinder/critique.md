# S1 — critique of the first cut, and what Tier 1 changes

**Written 2026-09-19, against `renders/s01/s01_captioned.mp4`** — 30 s, 1080×1920, 900 frames,
verified, gate-clean, silent. The harness did its job. The film does not.

> **The one sentence:** this is a technically correct, gate-verified, well-sourced 30 seconds that
> would be scrolled past in under two, because it is composed for the wrong aspect ratio and opens by
> withholding from an audience that leaves in three seconds.

---

## 1. The measurement that governs everything else

Subject coverage — the fraction of the frame that is not flat background:

| frame | | coverage |
|---|---|---|
| b01 f001 | 0.0 s, the opening frame | **1.9%** |
| b01 f045 | 1.5 s | 2.2% |
| b01 f090 | 3.0 s | 2.2% |
| b04 f105 | the closing hook | 2.4% |
| b03c f060 | the reveal | **7.0%** — the best frame in the film |

**98% of the frame is empty.** The cylinder was modelled accurately, lit deliberately and rendered at
32 spp — and then staged as a landscape product shot letterboxed into a portrait frame. Every other
fault below is downstream of this one, and fixing it is most of the available gain.

## 2. The comparator

[@KnowArt, *"Hydraulic Cylinders Push Harder Than They Pull"*](https://www.youtube.com/shorts/gjCfbgKbAbc)
— **432k likes, 1,888 comments**, read live 2026-09-19. The creator holds 363k on TikTok and 237k on
Instagram and reports roughly **two hours of work per second** of finished video.

Its first spoken line, verbatim from the burned-in captions:

> "hydraulic cylinders can push harder than they can pull..."

**It opens by stating the conclusion.** Title, first line and thumbnail are one sentence. The viewer
knows in one second what they are promised and stays for the *why*.

Ours opens with *"This cylinder pushes with fifty-five tonnes of force"* — a number about an object
the viewer cannot yet identify, at 1.9% of frame.

## 3. Against the genre's constraints

| | Genre | S1, first cut |
|---|---|---|
| Drop-off in the first 3 s | **50–60% of all viewers** | spent on a wide establishing shot |
| Named cliff triggers | intro cards, logo animations, **wide establishing shots** | we open on one |
| Target intro retention | > 70% past 3 s | opening frame is 98% background |
| Total length | 15–35 s | 30 s — the one thing that was right |
| Cutting rate | fast | **6 shots, 5.0 s average, one 7 s shot** |

Two cuts per ten seconds is documentary pacing in a swipe feed.

## 4. Faults, ranked by damage

1. **The frame is empty.** Fatal. Nothing else matters until it is fixed.
2. **The hook withholds instead of promising.** Beat 2 is seven seconds of a near-static cylinder
   asking "so where does half the force go?" A withhold is a documentary device; in a feed it is a
   scroll. A quarter of the film has no visual change.
3. **The one number was never built.** The brief mandates the forces as *"3D-tracked callouts in the
   scene, not caption text: a dimension that lives in the edit is a dimension nothing can check."*
   `spec/s01/s01.toml` contained **no callouts at all**. The brief's "one number the viewer will
   repeat" never appeared on screen in any form. A straight spec omission.
4. **Narration 60% over-written.** 120 words at **240 wpm** where ~75 fits; `voice` refused to record
   it. The shot carrying the reveal ran at **405 wpm**.
5. **No scale reference anywhere.** Nothing says a cylinder is the size of a leg or a lamppost.
   `library/` already holds `crew`, measured, and the cut uses none of it.
6. **It explains rather than demonstrates.** We show geometry and assert a consequence, and never
   show the cylinder lifting a load and then failing to lift the same load pulling.
7. **Captions small, low-contrast, broken mid-phrase** — *"pushes with fifty-five / tonnes of force"*.
8. **One colour.** Grey-blue throughout except four gold circles. No temperature contrast, no depth.
9. **The section shot is unreadable** — a tight crop of chrome with no context.
10. **The closing hook reads as debris** — three small sticks at 2.4% coverage.

## 5. What is good, and must survive the rework

- **b03b → b03c is real visual argument.** The ring looks smaller than the rod's circle; re-formed,
  it is identical. It is the best seven seconds here and it is *better than the comparator's*
  treatment, because it shows the halving rather than asserting it. Also the only shot above 7%.
- **The facts are sourced and hash-bound to the script.** No one else in this niche can say that.
- **The geometry is parametric.** S2, S5 and L1 inherit it.

## 6. Tier 1 — what is being changed now

Recomposition and edit only. No new mechanism, one new generator, one re-render.

| | Change | Why |
|---|---|---|
| 1 | **Fill the frame** — target 25–40% coverage on every shot | §1 |
| 2 | **Open on the payoff** — first frame is the reveal, first line is the conclusion | §2, §4.2 |
| 3 | **Build the callouts** — `55 t` / `27 t` as in-scene geometry, 15–20% of frame height | §4.3 |
| 4 | **Cut narration to ~75 words**, re-balanced across shots | §4.4 |
| 5 | **Kill the withhold** — 7 s becomes 2–3 s | §4.2 |

Deferred to Tier 2: `crew` for scale, the load demonstration, 12–14 shots, colour and lighting
rework, caption system, sound.

**This changes the narration, which is hash-bound to `spec/s01/facts/s01.facts.json`.** No *fact*
changes — the bore, rod, pressure and forces are untouched — but the words carrying them do, so the
ledger re-stamps and the six facts want a fresh read before `--publish`.
