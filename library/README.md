# library/ — the compounding asset kit

Nothing in here is episode-specific. Everything here pays back across every future video.

**This is the shadcn idea applied to geometry: components you own.** They live in this repo, you
compose them rather than re-deriving them, and improving one improves every video that uses it.

## Browse it

```bash
python -m harness library                    # the whole catalogue
python -m harness library screw              # one component: params, provenance, example
python -m harness library --search brick     # find by name or description
python -m harness library --category CHR     # GEN | CHR | DET | MAT | SHOTS
```

The catalogue lives in `harness/library.py`. It exists because `generators.py` already had the
components but **no way to find them** — so every new shot re-derived its geometry from primitives,
because nobody could tell without reading the source that `ring` already knew how to be a tunnel
bore, or that `crew` took a pose. The cost of that is invisible and recurring: the same wheel,
reinvented slightly differently, in every spec.

```
GEN/      parametric geometry      box cylinder sphere plane shield brick_wall ring arch
                                   timber screw boat dock train
DET/      reusable detail          (rivet fields, bolt patterns, plate seams — not yet built)
CHR/      figures                  crew
MAT/      material masters         (cast iron, wrought iron, rope, canvas — not yet built)
SHOTS/    shot templates           (not yet built)
```

## Rules

1. **Every component declares its provenance, and says whether its dimensions are cited.**
   `shield` and `brick_wall` are measured against sources. `screw` is explicitly **not** — its pitch
   is chosen so six turns advance the cell 0.20 m, which is the right order of magnitude and no more.
   `measured: false` is a legitimate answer and a much better one than silence, because the fact gate
   downstream depends on telling the difference.
2. **Parameterise, never fork.** `shield` takes `frames x levels`. Episode 1 uses 12 x 3; the same
   generator serves Greathead's 1869 Tower Subway shield with different numbers. If you are about to
   copy a generator for a new episode, add a parameter instead.
3. **A fix propagates.** Rebuilding `crew` from a cylinder-and-sphere stand-in into a figure with
   shoulders, arms and a cap improved every shot that uses a person — including ones not yet written.
4. **1 Blender unit = 1 metre.** No exceptions, no scale factors, no "it looked right".
5. **A component that has been seen to fail gets a test.** `crew` was rebuilt because it did not read
   as a person; `screw` was added because a bare cylinder did not read as a screw. Where a failure is
   checkable it belongs in `tests/run.sh`, not only in `LESSONS.md`.

## The upgrade path

Every folder above is where a future video gets cheaper. The two that pay back fastest and are still
empty:

- **DET/** — rivet fields and bolt patterns. The shield in `ad01` reads as a grid of bars partly
  because nothing gives the iron its scale; a rivet field is the cheapest fix for that in the medium.
- **SHOTS/** — parameterised shot templates. `ad01` and `ad02` both stage a cell against brick with a
  figure in it, and that composition was re-derived by hand twice.

## Not yet built

The kit is seeded but thin: thirteen geometry components, one figure, no materials master and no shot
templates. Each video added so far has seeded roughly two components. That seeding cost is the
deliberate premium on the early work, and it is the reason later videos are cheaper *and* better.
