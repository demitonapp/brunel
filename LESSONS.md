# LESSONS

Every entry carries an **executable check**, or it does not belong here. A lesson that cannot be
checked is a feeling, and feelings do not compound.

Format:

```
## YYYY-MM-DD — <one-line lesson>
- **Context:** what happened
- **Check:** the assertion, golden, or rubric item that now enforces it
- **Where:** the file that implements the check
```

---

## 2026-09-17 — A spec key the compiler silently ignores is a bug, not a convenience

- **Context:** An early spec set `depth` on a wall where the generator expected `brick_d`. The
  build succeeded and produced the wrong geometry. Nothing failed; the render was simply wrong.
- **Check:** The compiler raises `SpecError` on any key not in the schema's closed vocabulary.
- **Where:** `harness/spec.py` — `_unknown()`.

## 2026-09-17 — Score renders, not code

- **Context:** "The script ran" and "the shot works" are different claims, and only the second one
  is the product.
- **Check:** The canary reel is compared with SSIM >= 0.98 and LPIPS <= 0.05 per shot. Hash
  equality is not used, because Cycles is not bit-reproducible across driver or OptiX versions.
- **Where:** `goldens/canary/` (not yet populated).

## 2026-09-17 — Archived evidence only

- **Context:** Web sources rot. A citation that no longer resolves is not a citation.
- **Check:** `factgate` warns on every source without `archived: true`.
- **Where:** `harness/factgate.py`.

## 2026-09-17 — Blender's Action API is mid-transition; do not bet on one shape

- **Context:** Blender 4.4+ introduced slotted actions and the legacy `action.fcurves` accessor is
  being retired. Camera keyframe interpolation silently did nothing.
- **Check:** `_fcurves()` enumerates both the legacy and the slotted layout.
- **Where:** `harness/render.py` — `_fcurves()`.
