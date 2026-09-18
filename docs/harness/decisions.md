# Decisions

One entry per decision that is expensive to re-litigate. Dated, with the evidence that forced it
and the condition that would reopen it. If a decision has no reopening condition, say so.

Format is deliberately short. The evidence lives in `docs/research/` and `docs/strategy/`; this
file exists so nobody re-argues a settled question from memory.

---

## D1 — `local` is the shipping path. Generative is off the critical path.

**Decided 2026-09-18.** Confirms and hardens the conclusion already reached in
`docs/strategy/spec.md` §8.7.

**Why.** Measured on the only paid generation this repo has run (`renders/ad02/generated-wan/`):
iron rendered cobalt blue, the clay the narration promises deleted from frame, motion on the payoff
shot attenuated 52% against its own depth control, four incompatible grades across five shots, and
a payoff shot black end to end.

**Why the new slate makes it worse, not better.** `WanVaceBackend.requires = ("depth",)`. The Phase
0 subjects are the worst case for depth-only conditioning: a lattice mast is thin struts, rope
reeving is eight parallel thin lines, and a hydraulic cylinder is a smooth barrel whose depth pass
is a featureless gradient — which §8.7 already measured the model rendering as a void. And the new
slate removed generative's one legitimate job: an 1825 clay tunnel has atmosphere to add, a
hydraulic cylinder does not. Every shot in Phase 0 and Phase 1 carries a mechanical claim, and
§8.7's own rule excludes generative from exactly those.

**The economics finish the argument.** The strategy is to iterate a hook 30 times. At $0.08/s that
is ~$100 per full pass on three long-forms and ~$1,000 across ten iterations, none of it
reproducible. `local` is free and deterministic, which is the only reason 30 iterations is a plan.

**Not deleted.** `backend.py` stays. It is one class per backend, it costs nothing to keep, and it
is the portability hedge. This is a change to the plan, not to the code.

**Reopens when** a backend accepts more than one control pass — depth *and* segmentation *and*
edge, the Cosmos shape. Until then it is an atmosphere tool for a slate with no atmosphere.

---

## D2 — Render on the M1 through Phase 0. Defer the node.

**Decided 2026-09-18.**

**Why.** Measured, not extrapolated (H19): **26.86 s/frame** at 1080×1920 @ 8 spp on M1 CPU
Cycles. A 30-second Short is 900 frames — **6.7 hours, one overnight**. Eight Shorts across eight weeks is one overnight a
week, which is free and already fits the cadence.

**Why not sooner.** The 3080's OptiX throughput is `not_measured`, and sizing a node from an
extrapolation is how `render-bench.json` produced a number that turned out to be optimistic by
about 4×. Phase 0 produces the real curve; buy or build against that.

**Render on CPU, not Metal.** Measured in `render-bench.json`: Metal was *slower* than CPU on the
7-core M1 GPU. Do not assume the Mac's GPU is the fast path.

**Reopens at Phase 1**, which needs the node on two counts: **94 h** per 7-minute cut, and **~29 GB**
of frames against 12 GiB free (H20).

---

## D3 — The Australia-only clause is dropped.

**Decided 2026-09-18.** Reverses `docs/strategy/spec.md` §1 ("Australia only, for at least 12
months. Every subject Australian.").

**Why.** Measured penalty: Jared Owen's Sydney Opera House video returned **1.7M views against his
5.5M median** — 31%, same creator, same format, same quality, on a landmark far better known than
anything on the original slate. Seven of the twelve original episodes had effectively no global
search demand, and one of the two globally recognised subjects was already made by a 4.4M-subscriber
channel three years ago.

**What replaces it.** Construction-plant mechanism evergreens: globally searched, no geography
required, and squarely inside Demiton's domain. It is the only subject class that serves reach and
the sponsor at the same time. See `docs/strategy/slate.md`.

**What is kept.** The mechanism-first, sourced wedge and the public fact ledger. Those were never
the geographic part, and they are still the moat.

**Reopens at Phase 3**, where the Australian subjects return as the payoff of a proven format
rather than the opening bet.

---

## D4 — Reach first, sponsor second.

**Decided 2026-09-18.** Resolves the contradiction named in `reach-audit-2026-09-18.md` §1.

The channel optimises for reach; Demiton is a bumper, a link and a case-study page — the model that
already works for the largest construction channel on the platform. The B2B work (piling, batching,
site logistics, customer project visualisation) uses the same harness and the same specs but is
distributed on LinkedIn and in industry press, measured in named accounts rather than views.

**They are two products sharing a toolchain.** Mixing them dilutes both: the slate stops passing the
reach test, and the B2B work waits behind a YouTube cadence it does not need.

**Reopens if** the sponsor relationship becomes the primary revenue line, at which point the
optimisation target genuinely changes and this file should say so.

---

## D5 — Python stays. The gap was the guardrails, not the language.

**Decided 2026-09-18**, after auditing the question properly rather than by preference.

**Why it is barely a choice.** `bpy` is Python-only — Blender's public extension API *is* Python.
**1,970 of 6,084 lines (32%) import `bpy` or `bmesh`** and cannot move without leaving Blender:
`build.py`, `generators.py`, `passes.py`, `render.py`. The other 68% — argparse, TOML/JSON
validation, HTTP, ffmpeg wrapping — could be anything, but splitting a one-person project into two
toolchains to rewrite a CLI is what this repo's own principles exist to prevent. **Python is
entailed by Blender; see D6.**

Python is also not on the critical path. 26.86 s/frame is Cycles, which is C++. Scene build is
60–90 s against a 6.7-hour render — 0.4%.

**What the audit actually found.** Of H1–H23, roughly **three** would have been caught by a stricter
compiler: H9's write-only `offset`, H13's two `BuildError` classes, and the shadowed `_depth_range`.
The other twenty are missing call sites, missing comparisons, wrong semantics, a schema gap or
unsourced facts. **No language prevents those**, which is the strongest argument against a rewrite
rather than for one.

Meanwhile ruff was configured in `pyproject.toml` and wired into nothing, with 28 findings waiting;
its select list omitted `W`, so W605 — the invalid escape that raised a SyntaxWarning on every test
run until H14 fixed it by hand — sat outside the project's own ruleset. There was no type checker at
all. And the duplicate-definition bug had been answered by **hand-writing an AST walk in
`tests/run.sh`**: a partial reimplementation of a type checker nobody was running.

**Fixed 2026-09-18.** ruff and mypy pinned in `requirements-dev.txt`, both hard requirements of
`tests/run.sh`, all 28 ruff and 8 mypy findings resolved rather than suppressed, and the hand-rolled
check cut down to the one job no type checker does (see H13 — a class in two modules is legal).

**Reopens if** Blender is replaced (D6). Not before, and not on taste.

---

## D6 — Blender, not Unreal. The engine question is the real one, and the answer is still Blender.

**Decided 2026-09-18.** Follows directly from D5: if Python is entailed by Blender, the question
worth asking is Blender vs Unreal.

**On this machine it is not a choice.** Against Epic's own macOS requirements, on an M1 / 16 GB /
12 GiB free:

| UE5 feature | Requires | Here |
|---|---|---|
| **Nanite** | Apple Silicon **M2+** (Beta) | ✗ M1 |
| **Lumen, hardware RT + MegaLights** | **M2+** (Experimental) | ✗ M1 |
| Recommended memory | **32 GB** (16 is the minimum) | 16 GB |

**The two features that are the argument for Unreal are the two this hardware cannot run.** Add disk:
UE5 plus Xcode plus a derived-data cache is tens of gigabytes against 12 GiB free, where the entire
current renderer is a **690 MB** pip install.

**The pain it would relieve is relieved for free.** The only real operational problem is 94 h per
7-minute long-form, and that is an unbenchmarked RTX 3080 (see D2), not an engine. Buying an engine
to avoid running a benchmark is the wrong order.

**The objection that survives better hardware.** The thesis is "a diffable spec, deterministic Python
writes the scene graph, reproducible from `hash(spec) + toolchain pin`." The `.blend` is binary too,
but it is *derived* — rebuilt from TOML every run, never hand-edited. Unreal's unit of work is the
binary `.uasset` and the level, versioned with Perforce. And `bpy` on PyPI is genuinely exceptional:
Blender ships as an importable library, which is why `doctor`, `validate` and every pure-function
check run without an application. Unreal has no equivalent.

Deepest of all: real-time rendering is temporally accumulated. TSR and Lumen carry history between
frames, and "same spec, same frames" is exactly what an accumulator does not give. MRQ's Path Tracer
is deterministic — and switching it on hands back the speed that was the reason to move. **You would
migrate for speed, then disable the thing that made it fast to keep reproducibility.**

**Where Unreal genuinely wins**, and it clusters on one product: Datasmith/BIM ingest (IFC, Revit,
STEP, point clouds), interactive client-driven deliverables, and site-scale environments. All three
describe the **Demiton B2B arm**, not the channel. D4 split those into two products sharing a
toolchain; this is the first place that split has an engineering consequence — **they may not share
one forever.**

**The cheap hedge, deliberately not built.** The analogue of the control-pass portability argument is
USD export: the spec is already the truth layer, so emitting USD alongside the `.blend` would make
the *renderer* swappable the way `backend.py` made the model swappable. Nothing needs it. Recorded so
the option is known rather than rediscovered under pressure.

**Reopens if** the B2B arm needs BIM ingest or interactivity — as a *second* pipeline, not a
replacement — or if the 3080 benchmark disappoints badly enough to change the arithmetic.
