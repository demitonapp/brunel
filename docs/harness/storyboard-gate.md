# The storyboard gate — what studios do, and what Brunel should copy

**Research date:** 20 September 2026. Sources are linked inline and were read on that date.

**Why this document exists.** s01 was rendered four times. Two of those renders — 3.5 hours and a
22-hour overnight attempt — went into cuts with faults that were visible in stills before a single
full-quality frame was made. The storyboard pass was run every time. **Nothing ever required a human
to look at it and say yes.**

---

## 1. What the studios actually do

### a. Iteration happens on the cheap artefact, and there is a lot of it

Pixar builds **6–8 full-length animatic passes before a film is approved for animation**
([Science Behind Pixar](https://sciencebehindpixar.org/pipeline/story-and-art)). Each pass refines
timing, pacing and beats. Boards go to editorial, who cut them into a reel with scratch voices and
temporary music.

The industry rule of thumb for commissioned work is **2–3 board revisions** and **2–10 style frames**
depending on scale ([Storyflow](https://storyflow.so/blog/moodboard-vs-lookbook-vs-style-frames)).

**Brunel ran zero board passes and four full renders.** Exactly inverted.

### b. "Locked" is a formal gate, not a feeling

> A storyboard lock is the point in pre-production where the shot-by-shot visual plan is approved
> and frozen — no further shot-design changes before money and crew commit.
> — [invideo](https://invideo.io/faq/what-is-a-storyboard-lock-and-do-you-need-one-for-ai/)

The reasoning is structural rather than ceremonial: animation is built frame by frame, so changing
frame 5 also changes the exit of frame 4 and the entry of frame 6. **The board is cheap to change.
The animation is not.**

### c. There are TWO approval axes, and they are tracked separately

The status vocabulary used across VFX and animation
([CAVE Academy](https://caveacademy.com/wiki/production/production-statuses/)) separates them:

```
VERSION PENDING REVIEW / VERSION REVIEW / VERSION DECLINED / VERSION APPROVED   <- creative
TECH CHECKS PENDING    / TECH CHECKS DECLINED / TECH CHECKS APPROVED           <- technical
CLIENT PENDING REVIEW  / CLIENT REVIEW / CLIENT DECLINED / CLIENT APPROVED
PUBLISHED - ELEMENT IN PIPE / ELEMENT APPROVED / PROPOSED FINAL / FINAL
```

Note `PUBLISHED – ELEMENT IN PIPE` — "internally approved but tech checks failed". The two axes can
disagree, and the vocabulary has a word for it.

**This is the single most useful finding for us.** Brunel has *only* the technical axis —
`check_storyboard`, `check_coverage`, `check_motion`, the pace check. It has no creative axis at all.
`verify` saying "all 900 artefact(s) pass" means **tech checks approved** and has never meant
anything else. Twice this week it was read as though it meant the cut was good.

### d. Look is approved BEFORE story, and separately

> A storyboard shows sequence... a styleframe shows finish by taking one moment and rendering it at
> full visual quality. Storyboards answer "what is the story", styleframes answer "what does it look
> like". — [Storyflow](https://storyflow.so/blog/moodboard-vs-lookbook-vs-style-frames)

> The style frame stage is where **90% of the visual debate happens** — and where it should happen.
> Catching visual concerns at the style frame stage costs an afternoon of design work, whereas
> catching them after animation has been underway costs significantly more.
> — [Storyflow](https://storyflow.so/blog/moodboard-vs-lookbook-vs-style-frames)

> If the client approves the styleframe, they have approved the look, and animation becomes a matter
> of **bringing that look to life rather than inventing it frame by frame**.

**This is precisely the mistake s01 made.** The backdrop, the light colours, the `annot` material,
the callout type size and the section treatment were all invented *during* staging passes. Every
look change forced a re-render of shots whose staging was already settled, and the 22-hour render
died carrying a backdrop that had never been approved as a look at all.

---

## 2. What Brunel should adopt

**Three gates, in this order. Each is cheap and each blocks the next.**

```
LOOK  ->  BOARD  ->  RENDER
```

### Gate 1 — LOOK. One frame, full quality, approved once per video.

One shot, rendered at final resolution and samples. It settles materials, lights, backdrop, type
size and the section treatment. **Nothing else is being judged** — not staging, not timing.

Approved once per video, and re-opened only deliberately. A look change after board approval
invalidates every board frame, and the gate should say so out loud.

### Gate 2 — BOARD. Every shot as a still, plus a low-res animatic with scratch VO.

`render --fast --stills` and `deliver` already produce exactly this — the animatic is the thing I
have been sending as "the preview". It becomes an artefact with a state rather than an attachment.

Per-shot approval, **fingerprint-bound**: `render.py` already computes `_fingerprint(ep, shot, ...)`
for its resume cache, which is precisely "what would change this shot's pixels". Record it at
sign-off; when it changes, that shot silently returns to `unreviewed`. Approval that cannot be
invalidated by a later edit is not approval, it is a memory — the same argument as
`script_hash_matches_ledger`.

### Gate 3 — RENDER. Full quality refuses unapproved shots.

`--fast` and `--stills` are **never** gated, or you cannot iterate toward approval.

### The two axes, kept apart

| | who | what it means | Brunel |
|---|---|---|---|
| **tech checks** | the harness | coverage, motion, storyboard, pace, mechanism | exists, automated |
| **review** | a human | does this shot do its job | **does not exist** |

Both must pass. A shot that is `checks: pass / review: unreviewed` is **not** ready, and `verify`
must stop implying it is.

### Status ladder

Trimmed from the studio vocabulary — there is one person here, not a client and a vendor:

```
unreviewed -> pending (tech checks pass, awaiting a human) -> approved
                                                           -> rework  (with a note)
                                                           -> waived  (loud, reason required)
```

---

## 3. What this would have caught

| Fault | Visible in | Cost paid |
|---|---|---|
| Hook at 1.9% of frame | every still | full render |
| Three frozen shots | stills, had motion run | 3.5 h render |
| Sectioned barrel in b01, spoiling beat 3 | one still | full render |
| b03b showing a disc where the annulus belongs | one still | full render |
| Pull block floating 0.305 m off the rod | one still | full render + review round |
| Section cut face unfilled | one still | full render + review round |
| Backdrop never approved as a look | a look frame | **22 h render** |

Every single one was visible before the expensive step.

---

## 4. Cost, honestly

A board pass is `render --fast --stills` — **14 frames, about 50 seconds**. The animatic is
`--fast` plus `deliver` — about 20 minutes. A full render is 6–10 hours on this machine.

**The gate costs roughly 0.2% of what it protects.**
