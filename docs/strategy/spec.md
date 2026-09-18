# Brunel — Product Spec

> **The goal is viewers. The videos are the vehicle. The harness is only the cheapest way for one
> founder to ship the videos.**
>
> When a harness decision and a storytelling decision conflict, the storytelling decision wins.
> When a harness defect blocks a video, it is a product defect and it is ranked by the video it
> blocks — not by how interesting the bug is.

**Supersedes:** everything in `docs/archive/`. Evidence base stays in `docs/research/`.

**Partly superseded itself, 2026-09-18.** After the reach audit
([`reach-audit-2026-09-18.md`](reach-audit-2026-09-18.md)) three parts of this document were
overtaken. They are left in place, struck through, because the reasoning is still worth reading
and because silently rewriting a locked decision is how a repo forgets it ever made one.

| Section | Superseded by |
|---|---|
| §1, the Australia-only clause | [`../harness/decisions.md`](../harness/decisions.md) **D3** |
| §3, the 12-month slate | [`slate.md`](slate.md) |
| §4, "Shorts are the growth engine" | [`slate.md`](slate.md) §1 — a Short is a shot built early, not a trailer cut late |
| §5, the C1–C6 capability table | [`../harness/backlog.md`](../harness/backlog.md) Part V |
| Parts III–IV | [`../harness/backlog.md`](../harness/backlog.md) |

**Status:** channel strategy (Part I) locked 2026-09-18. Harness remediation (Part III, H1–H18)
**implemented and merged 2026-09-18** — see [PR #1](https://github.com/demitonapp/brunel/pull/1) and
`git log`. The findings and evidence in Parts II–III are kept as the historical record of what was
found and why each fix was made; they are not a live to-do list. What is still open:

- The capability roadmap in Part I §5 (C1–C6: Mode C diagrams, terrain input, dual aspect,
  thumbnails) — unstarted, months of product work.
- Fact-ledger *content* for `ad01`/`ad02` (H5 wired the gate; nobody has written the ledger).
- The underlying Wan duration mismatch itself (§8.1) — the harness now catches and refuses it
  correctly, but the mismatch is unresolved: `deliver --backend wan` still refuses `ad02` today.
- `eval/audience.md` (§6) — does not exist yet; needed before the first real upload.

---

# Part I — The channel

## 1. The niche

### Thesis

> **"How Australia was built — the machines and mega-projects that did the impossible, explained
> with nothing guessed and the receipts shown."**

> **REVERSED 2026-09-18 — see [decisions.md](../harness/decisions.md) D3.** The measured penalty is
> 31% of median on an Australian subject, by the same creator in the same format. The clause below
> is kept as the record of what was decided and why it did not survive contact with the numbers.

~~**Decision locked (2026-09-18):** Australia only, for at least 12 months. Every subject
Australian. International subjects wait until the format and the audience are proven.~~

### Why it is winnable for one founder

Globally, Animgraffs and Jared Owen own "how it works" and a solo founder cannot out-render them.
**In Australia nobody owns "how it was built."** There is documentary TV (slow, no mechanism
clarity) and small YouTubers (no animation quality, no sourcing discipline). The year-one benchmark
is not Animgraffs — it is a near-empty niche. Goal: **be the definitive Australian engineering
channel.** "Overtake Animgraffs" is a year-three question.

### The wedge

1. **Mechanism-first, sourced.** Every video shows *how it works* and cites the primary record on
   screen. The fact ledger is **public, not internal**. Trust is the moat.
2. **Story-driven, not explained.** Competitors answer "how does it work." We answer "how was the
   impossible done, and what did it cost." The mechanism is the hero; the story is the engine.
3. **The tunnelling spine.** Brunel's shield (1825) → the Snowy tunnels (1949–74) → Snowy 2.0's TBMs
   (now). One 200-year story about one machine, and the natural through-line of the year.

### Constraints, stated then designed around

- **"Australian" caps global reach and buys a loyal local audience with zero competition.** Frame
  every subject universally ("how a nation harnessed a mountain range"), never parochially.
- **Mega-projects are systems of systems.** The discipline that makes Animgraffs unbeatable is *one
  object, one mechanism, deeply*. Hold the same line: **one system per video.** If an episode
  cannot state its one mechanism in a sentence, it is two episodes.
- **The people problem is real.** `crew` produces scale witnesses, not people. Resolved in §5.

---

## 2. The story engine

Every video runs the same five beats. The harness exists to make those beats cheap to render.

```
1. IMPOSSIBLE PROBLEM   Why this had to happen, and why everyone said it couldn't.
2. THE BOLD BET         Someone proposes a way. The mechanism enters as the ANSWER.
3. THE BREAKDOWN        The obstacle that nearly killed it. Peak tension.
4. THE BREAKTHROUGH     The mechanism's moment of truth — doing the impossible.
5. THE LEGACY           What it changed, and why it matters to the viewer right now.
```

**The mechanism is the protagonist** — a character with a goal (dig under a river, hold back a
mountain, turn falling water into the grid) and obstacles. Every part is a plot point. This is the
single biggest unlock: it turns a "how it works" lecture into a story with an ending the viewer
wants.

Worked example, the Snowy flagship in one paragraph:

> *Australia in 1949 has a river that flows uselessly into the sea while the inland plains that feed
> the nation dry out — separated by the Great Dividing Range. The bet: carve 145 km of tunnels
> through the range, move the river backwards over the mountain, turn the fall into electricity. The
> breakdown: the rock, the floods, the 121 dead of ~100,000 men from 30+ countries. The
> breakthrough: a tunnel breaks through the far side — the same machine Brunel invented in 1825,
> grown to the size of a building. The legacy: every light in the east-coast grid, and the
> pumped-hydro battery being dug under the same mountains today.*

### 2.1 Cold open (first 15–30 s)

Never a title card. Open on one of three, in preference order:

| Open | Pattern | Snowy example |
|---|---|---|
| **The disaster** | Worst moment, mid-crisis, no context | *"In 2022 a 2,000-tonne boring machine stopped under the Snowy Mountains — and never moved again."* |
| **The scale** | A number they can't picture, then the picture | *"200 metres long, heavier than a warship, and buried under 700 metres of rock right now."* |
| **The stakes** | "Every time you…, part of that…" | *"Every time you turn on a light in Sydney, part of that power has been through a mountain — twice."* |

Then pose the problem, **withhold the answer**, cut to title. The mechanism is revealed only once
the problem has made it necessary.

### 2.2 One "aha" every ~90 seconds

Attention is a leaky bucket; plug a leak every ~90 s with a reveal. *Why a shield and not a pickaxe?*
Because the ground is wet and will collapse — the shield is a travelling wall. *Why does the arch
hold?* Because load runs down the curve into the ground. *Why are the Opera House sails the same
curve?* Because they're segments of one sphere.

**The withhold is the tool.** Problem fully stated before solution, or it's a lecture.

### 2.3 Scale anchoring — mandatory

Every hero shot carries a scale reference the viewer already knows. "11.43 m" is a number; "as wide
as a house, taller than a double-decker, one man in each of 36 cells" is a picture.

### 2.4 The "so what" closer

Every video ends on why it matters **now**, in the viewer's life, and plants the next video. Snowy →
the grid you use today and the battery being dug under the same mountains. Harbour Bridge → the city
you live in. This is the difference between "interesting" and "worth subscribing to."

### 2.5 Fact-as-trust: cite on screen, as a beat

"We don't guess" is a **storytelling device**, not a footnote. At peak claim, show the receipt — two
seconds of on-screen citation ("ICE Archives, 1828" / "National Archives of Australia, series
A1200"). It reads as confidence and it is the one thing separating us from the AI-slop history
channels flooding the platform. **The fact ledger becomes a linked page per video.**

> This clause is load-bearing and it is currently unenforced. See H8.

---

## 3. The 12-month slate

> **SUPERSEDED 2026-09-18 by [`slate.md`](slate.md).** Seven of the twelve episodes below had
> effectively no global search demand, and one of the two globally recognised subjects was
> already made by a 4.4M-subscriber channel three years ago. The mechanism episodes (5, 9, 11)
> were right and were ranked last; they are now first. The Australian subjects return in Phase 3.

One series: **"Built Australia."** One system per video. History and present alternating, so the
channel is never "old stuff" and never "news that expires."

| # | Type | Subject | Mechanism the harness shows | Hook title |
|---|---|---|---|---|
| **Phase 1 — own the Snowy (months 1–3)** |
| 1 | flagship | Snowy Mountains Scheme (1949–74) | Terrain map + tunnels + cross-section + one hydro cycle | *How Australia moved a river over a mountain* |
| 2 | mechanism | The Snowy tunnels | Shield/TBM cycle: bore, line, advance — Brunel's descendant | *How they dug 145 km through a mountain range* |
| 3 | now | Snowy 2.0 | Pumped-hydro cycle + the TBM under the mountain | *The machine stuck under the Snowy Mountains* |
| **Phase 2 — own the icons (months 4–7)** |
| 4 | icon | Sydney Harbour Bridge (1923–32) | The arch: load down the curve; the two halves meeting | *How a 53,000-tonne arch holds itself up* |
| 5 | mechanism | The tunnel boring machine | Full cutaway: cutterhead, thrust, segment erector | *How a tunnel boring machine works* |
| 6 | icon | Sydney Opera House (1959–73) | Orange-peel geometry: one sphere, many segments | *The geometry everyone said couldn't be built* |
| 7 | story | Overland Telegraph (1870–72) | Poles, wire, repeater stations — one circuit | *How Australia got wired to the world* |
| **Phase 3 — own the machines working today (months 8–12)** |
| 8 | now | Pilbara autonomous trains | AutoHaul: 2.8 km of train, no driver | *Australia's 2.8-km robots* |
| 9 | mechanism | Sydney Metro harbour tunnels | TBM under water + segmental lining | *How you dig a metro under a harbour* |
| 10 | story | Great Ocean Road (1919–32) | The cliff route, cut by hand | *The road built by 3,000 soldiers* |
| 11 | mechanism | The hydro power station | One station cross-section, water animated through | *How falling water becomes your electricity* |
| 12 | evergreen | Trans-Australian Railway (1912–17) | Laying track across nothing; the 478 km straight | *The straightest railway on Earth* |

**Why this order.** Starts on the highest-recognition, highest-search, highest-drama subject; anchors
a pure-mechanism evergreen (the TBM) early so search finds us; alternates history and present so the
channel never reads as nostalgia; every closer plants the next episode. **5, 9, 11** are the search
workhorses. **1, 4, 6, 10** are the emotional flagships. **3, 8** are the news-spike traffic.

**Brunel is Episode 0.** The existing Thames Tunnel work is the prequel and the proving ground: it
establishes "we show the receipts," and it is where the harness defects in Part III get fixed
cheaply, before the slate starts spending real production hours.

---

## 4. Packaging — what actually grows the channel

Content quality earns watch-time; **packaging earns the click, and the click is what grows a
channel.** Titles, thumbnails, hooks and closers are versioned, testable artifacts. Treat them like
code.

### Titles — three patterns

1. **"How [X did the impossible]"** — *How Australia moved a river over a mountain.*
2. **"[Number] [unit] + [impossible verb]"** — *A 53,000-tonne arch that holds itself up.*
3. **"The [object] everyone said couldn't be built."**

Rules: one concrete number or one concrete object, never both abstract; no colons; under ~60 chars;
subject visible in the first three words.

### Thumbnails

One subject, one glowing callout, high contrast, a scale reference, cutaway where possible.
**Rendered from the actual scene** — no stock art, no hand Photoshop. This is a real single-founder
advantage: the thumbnail and the hero frame come from the same deterministic scene, so the promise in
the thumbnail is *the same thing* the video delivers.

### Retention mechanics, baked into the script not the edit

- **Open loops** — pose a question, answer it 90 seconds later.
- **Chapter cliffhangers** — each beat ends by naming the next beat's stakes.
- **The one number** — each video has exactly one surprising fact the viewer will repeat ("the Snowy
  moved a river *backwards over a mountain*"). Design the whole video around it.

### The Shorts funnel

A Short is **a trailer for the long-form**, not a mini-video. One mechanism reveal, one "whoa," one
"see the full story." **Cut from the same render** — the founder writes one hook line. Shorts earn
*browse* discovery; the mechanism episodes earn *search*.

### Cadence

- **One long-form every 2–3 weeks** (10–18 min) — the growth engine.
- **1–2 Shorts per week from the same render** — the funnel, not a second production.

---

## 5. Production system — one founder, one harness

### The principle: cadence and story polish, not render polish

A 12-minute video with a great story and L1–L2 visuals beats a 20-minute video with L4 visuals and no
story. Spend the founder's scarce hours on **the hook, the hero frame, and the last line**. The
harness's job is to make the *bad* versions of a shot cheap, so those three things get iterated 30
times instead of 3.

### The character decision — resolved, stop re-litigating

The peg-doll "scale witness" is the worst of both worlds. **Year one: people-free diagrammatic style
+ a dedicated scale bar + archival photographs.** It is honest, cheaper, and Animgraffs proves a
people-free style can win. Revisit characters only when a story requires them (Episode 10).

### What the harness must gain, in slate order

> **RE-RANKED 2026-09-18 — see [`../harness/backlog.md`](../harness/backlog.md) Part V.** The table
> below is ranked against a Snowy flagship opening the channel. C4 is now first and C2/C3 have left
> the critical path entirely.

The content roadmap drives the engineering roadmap. Not the reverse.

| # | Capability | Needed by | Status |
|---|---|---|---|
| C1 | **Mode C — diagram/data**: terrain map, cross-section, animated dimension callout | Ep 1 | **does not exist** |
| C2 | **Geospatial terrain input** — DEM heightfield, real-world extents ("1 BU = 1 m" was made for this) | Ep 1 | **does not exist** |
| C3 | **Diagrammatic water flow** — animated arrows/sheets, not fluid sim | Ep 1, 3, 11 | **does not exist** |
| C4 | **Dual aspect from the spec** — 16:9 long-form and 9:16 Shorts from one spec | every video | **does not exist** |
| C5 | **Thumbnail render** from the same scene | every video | **does not exist** |
| C6 | **"As of" facts** in the fact gate, for moving Snowy 2.0 numbers | Ep 3 | **does not exist** |

C1 is the highest-leverage build in the whole plan: **the Snowy flagship is made of Mode C.** C4 is
second, because the Shorts funnel is the growth engine and doing it twice means learning every
camera and framing lesson twice.

**None of these can start until Part III's blocking defects are closed**, because every one of them
ships through the same broken delivery path.

---

## 6. Metrics — the ratchet aimed at the audience

The harness has an eval ledger for *render* quality. It needs a second for *audience* quality, under
the same discipline: every entry carries a check, or it doesn't belong.

| Metric | Measures | Lever |
|---|---|---|
| **CTR** (impressions → click) | Thumbnail + title | Version the pack, keep the winner |
| **Retention at 30 s, 2 min, mid-roll** | Cold open + the 90-second aha cadence | Version the hook, keep the winner |
| **Subs per 1,000 views** | Trust (the fact-as-trust device) | Cite on screen; ship the ledger page |
| **Search vs Browse split** | Evergreen vs discovery health | Mechanism eps feed search; Shorts feed browse |

**The versioning rule.** Hook, title, thumbnail and last line are versioned artifacts. Change one,
measure, keep the winner. `eval/audience.md` records each video's numbers and **the one change that
moved them**. Monotonic improvement in that file is the proof the ratchet works — aimed now at the
thing that grows a channel rather than at the renderer.

`eval/audience.md` must exist **before the first upload**, so video one is the baseline.

---

# Part II — The audit that set the harness priorities

Measured 2026-09-18 from `renders/ad02/generated-wan/shield-cycle-480p-captioned.mp4`, the most
recent paid generation, plus a full read of `harness/`. Reported here because it is the evidence
behind every ranking in Part III.

## 7. The finding that frames the rest

The harness has a check that catches a crushed-to-black clip. The check is correct. The delivered
video **fails it**, and the check never ran:

```
c05_c00.mp4                       FAIL: mean luminance 10.1 - the clip is crushed to black
shield-cycle-480p-captioned.mp4   FAIL: mean luminance 10.1 - the clip is crushed to black
```

`check_clip` is called in the sequential branch of `cmd_generate` and **not** in the
`submit`/`collect` branch — the branch taken whenever there is more than one bundle, i.e. every run
since the cold-start fix landed.

The founding defect class of this repo is "the failure was silent." The repo has now produced a new
instance: **the failure was not silent, it was unlistened-to.** Every item in Part III is ranked by
that principle. A defect is not fixed until a check fires on it.

## 8. What was actually delivered

### 8.1 The cut is 26.6% longer than the spec

| | Spec | Delivered |
|---|---|---|
| Shot length | 4.00 s × 5 | 5.0625 s × 5 |
| Total | **20.00 s** | **25.31 s** |
| Frames | 64 sent as control | 81 returned |

Wan VACE generates its own frame count and ignores the control video's length. 64 frames of depth go
out, 81 frames of video come back, **the last 17 of each unconditioned** — free model output with no
geometry behind it. Nothing compares declared duration to delivered duration.

### 8.2 The cost record is wrong by the same margin

`generate.json` records `"video_seconds": 20.0, "estimated_usd": 0.80`. fal bills per second of
**output**; output was 25.31 s, so true spend ≈ **$1.01**. `_bundle_seconds()` probes the *control*
video — the input, not the product — and the wrong number is written to the manifest as if measured.

### 8.3 The captions are on the wrong shots

Cues built on the 4.0 s/shot timeline, burned onto a 5.0625 s/shot video:

```
c01: spec  0.00- 4.00s   actual  0.00- 5.06s   drift +1.06s
c02: spec  4.00- 8.00s   actual  5.06-10.12s   drift +2.12s
c03: spec  8.00-12.00s   actual 10.12-15.19s   drift +3.19s
c04: spec 12.00-16.00s   actual 15.19-20.25s   drift +4.25s
c05: spec 16.00-20.00s   actual 20.25-25.31s   drift +5.31s
```

In the shipped file: "Turning them drives the cell forward" plays over **the digging shot**. The
brick-and-lining cues finish at 19.49 s — before c05, the shot they describe, begins at 20.25 s. The
final **5.06 seconds carry no captions at all**.

The narration is the product. It is currently describing the wrong pictures.

### 8.4 The payoff shot is black end to end

Mean luminance, threshold 12.0:

| shot | 0.0 s | 1.25 | 2.5 | 3.75 | 4.9 |
|---|---|---|---|---|---|
| c01 | 23.7 | 23.8 | 23.7 | 24.3 | 24.9 |
| c02 | 40.0 | 39.4 | 34.1 | 32.5 | 34.5 |
| c03 | 22.5 | 24.5 | 26.6 | 26.7 | 26.8 |
| c04 | 41.9 | 42.7 | 48.3 | 44.7 | 45.6 |
| **c05** | **10.8** | **11.4** | **11.1** | **9.9** | **10.1** |

Not a fade — uniformly below threshold for its whole duration. c05 is "The Advance," the shot the cut
builds to, and it is the last thing on screen. **The video ends on five seconds of near-black.**

Adjacent shots also swing 4× in mean luminance (c04 45.6 → c05 10.8). Nothing measures shot-to-shot
consistency, so a cut can pass every per-shot check and still flicker at every edit point.

### 8.5 The advance did not survive the generation

Motion energy, control depth pass vs delivered clip:

| shot | control | generated | |
|---|---|---|---|
| c01 | 42.5 | 34.4 | ok |
| c02 | 71.7 | 39.1 | **45% less** |
| c03 | 34.6 | 57.6 | model invents motion |
| c04 | 63.4 | 86.0 | model invents motion |
| c05 | 31.3 | 14.9 | **52% less** |

The depth control for c05 clearly shows the cell travelling; the delivered clip shows half of it. The
one mechanical fact the shot exists to communicate is what the model attenuated. Where generated
motion exceeds control, it is grade pumping and a mid-shot artefact — not the animation.

### 8.6 Every material decision in `ad02` is unreachable on this backend

`ad02.toml` carries careful, documented material work: four separated hues, iron roughness raised
0.42 → 0.62 to kill a specular bloom, crew moved to dark `cloth` because "a pale wooden figure in a
dark tunnel is the one thing the model lit into a glowing capsule," timber darkened because "the
model lit it into a glowing slab that appeared mid-shot."

`WanVaceBackend.requires = ("depth",)`. **The model never receives a colour.** Those fixes were aimed
at a channel that is not connected, they are recorded in `LESSONS.md` as though they worked, and the
artefacts they targeted are still in the delivered file — the glowing slab is visibly present in c04,
frames 3–4.

The material work is correct and necessary for `local`. The defect is that nothing says which backend
a decision reaches.

### 8.7 Depth alone is a silhouette — and this is a channel problem, not a bug

Every control pass passes the harness's own depth check:

```
c01 mean 128.7 clean   c02 120.2 clean   c03 113.2 clean   c04 127.3 clean   c05 155.6 clean
```

And the output is still unusable. In the c04 depth pass the cell is a **featureless white slab**
filling 40% of frame — correct, because a flat plate facing camera has constant depth. The model
receives no interior structure and renders that region as a dark void in c04, a blue box in c01.

`check_depth_pass` correctly answers "is this a valid depth map?" It does not answer "does this carry
enough information to render the subject," which is the question that decided this video.

**What the model actually delivered**, from contact sheets of all five clips:

- **c01** — iron as saturated cobalt **blue**, brick bright terracotta, the screw a modern hex-head
  machine bolt. The caption over it reads "The shield is a wall of thirty-six iron cells."
- **c03** — teal/orange grade, the miner a featureless orange mannequin holding a bright plank, and
  **no clay in frame at all** while the narration says he is cutting clay.
- **c04** — sodium orange. Screws read well, the best geometry in the cut. A bright cream rectangle
  appears in frames 3–4 and is gone by 5.
- **c05** — near-black, cell barely legible.

Five shots, four incompatible grades: blue, teal/orange, sodium orange, near-black. No continuity,
and nothing asks for any.

> **The strategic consequence.** §1 stakes the channel on *mechanism clarity* and *nothing guessed*.
> A depth-only generative path turns iron blue, deletes the clay the narration promises, and
> attenuates the advance. It is not merely low-quality — **it is actively hostile to the thesis**,
> because it guesses, and guessing is the one thing the channel sells itself as not doing.
>
> `README.md` already says the generative backend is "for atmosphere, not for mechanism." `ad02` was
> nonetheless shipped end-to-end through it. **Decision: `local` is the shipping path for year one.**
> Generative is for atmosphere plates behind deterministic mechanism, and never for a shot carrying a
> factual claim. Revisit when a backend accepts more than one control pass.

---

# Part III — The harness

> **Moved 2026-09-18 to [`../harness/backlog.md`](../harness/backlog.md).**
>
> H1–H18 and the order of work were extracted verbatim; H19–H20 and the re-ranked
> capability table were added there. This spec says what the channel is; the backlog says
> what stops it shipping, and the two were drifting inside one 698-line file.

---

## 14. First 30 days

1. **Lock the name and thesis line** (§1) — one sentence the audience remembers.
2. ~~Close the "Now" block (H1, H3, H2, H15).~~ **Done 2026-09-18**, along with the rest of H1–H18 —
   see the status note at the top of this document.
3. ~~Ship H4, then re-cut `ad02` through the fixed path.~~ **H4 shipped.** The re-cut is still
   blocked on the underlying Wan duration mismatch (§8.1), not on the pipeline.
4. ~~Write the Snowy flagship script~~ — **replaced 2026-09-18.** The Snowy flagship is Phase 3.
   Write **S1** instead: [`../videos/s01-hydraulic-cylinder/`](../videos/s01-hydraulic-cylinder/).
   Brief and script are written; the fact ledger is not, and it blocks `--publish`.
5. ~~Start C1 + C2.~~ **Re-ranked.** C4 (dual aspect) is first and C2 has left the critical path —
   [`../harness/backlog.md`](../harness/backlog.md) Part V.
6. **Stand up `eval/audience.md`** before the first upload. Not started.
7. **Source the S1 cylinder dimensions.** The arithmetic is done; the inputs are not cited, and
   "nothing guessed" is the whole product. See the brief's SOURCE NEEDED block.
8. **Ship S1 on the M1.** Measured 26.86 s/frame at 1080×1920 @ 8 spp — 6.7 h for a 30 s Short,
   one overnight. Do not build the render node until Phase 1 (D2).

---

## 15. Acceptance

The harness is fixed when:

- ✅ `python -m harness verify spec/ad02/ad02.toml --backend wan` reports the black c05 (confirmed
  against the real artefacts, 2026-09-18).
- ✅ `deliver --publish` refuses a spec with no fact ledger (confirmed against `ad02` and `ep01`).
- ✅ `LESSONS.md` states, per entry, what enforces it (all 39 entries, 2026-09-18).
- ⚠️ `deliver --backend wan` **correctly refuses** today's real `ad02` artefacts rather than
  producing a mistimed cut — proven correct on synthetic fixtures where the delivered length
  matches the spec. It does not yet produce a captioned cut from the *real* `ad02` clips, because
  those clips themselves are still 5.06 s against a 4.00 s spec (§8.1) — a real generation cost,
  not a code fix.
- The `tests/run.sh`-fails-on-real-artefacts bullet was a point-in-time proof step for this
  remediation, not a permanent assertion: `tests/run.sh` deliberately does not hard-code an
  expectation that `renders/ad02/generated-wan/` stays broken forever (see H6 - that pattern
  inverts the day someone fixes it). The proof was done manually and is recorded above.

The channel is working when `eval/audience.md` shows monotonic improvement in CTR and 30-second
retention across the first six uploads, and each entry names the one change that moved it. Not
started.

## 16. The one-line version

> ~~One channel — **"Built Australia"** … launched on the Snowy Scheme.~~
>
> **Revised 2026-09-18.** One channel — mechanism-first, sourced to the primary record, one system
> per video — launched on the machines that build things, because that is the only subject class
> that is both globally searched and squarely inside the sponsor's domain. Eight Shorts, then three
> long-forms, then the Australian flagships as the payoff of a proven format rather than the
> opening bet. The harness's only job is to make that cheap enough for one founder to run — and
> since 2026-09-18 it can, for the first time.
>
> The order is [`slate.md`](slate.md). The reasoning is
> [`reach-audit-2026-09-18.md`](reach-audit-2026-09-18.md). The decisions are
> [`../harness/decisions.md`](../harness/decisions.md).
