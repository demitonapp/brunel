# Eval ledger

> **This file is the ratchet aimed at renders.** The one aimed at the audience is
> [`audience.md`](audience.md), and it must carry a baseline before the first upload.
> `docs/strategy/spec.md` §6.

The only evidence accepted in a retrospective.

One row per episode. A claim of "this episode is better" is not admissible; a row here is.

## Headline metric

`eval/headline.json` declares **one** metric for the current quarter. One. A moving metric is not
a metric.

Suggested sequence:

| Quarter | Headline metric |
|---|---|
| Q1 | `shots_passing_L1_checklist / shots_total` |
| Q2 | `canary_mean_ssim` (against the previous quarter's canary) |
| Q3 | `minutes_of_finished_animation_per_creator_hour` |
| Q4 | `shots_passing_L3_checklist / shots_total` |

## Row schema

```json
{
  "episode": "ep01",
  "level_claimed": "L0",
  "gates": { "factgate": "pass", "licencegate": "pass", "canary": "pass" },
  "soft_scores": { "rubric_L0": 0.82, "accuracy_historical": 0.9 },
  "cost": { "render_gpu_hours": 0, "llm_usd": 3.10, "creator_hours": 15.5 },
  "revisions": { "shots_rebuilt": 3, "escape_hatches_used": 2 },
  "benchmark_shot": { "ssim_vs_last_quarter": null, "lpips_vs_last_quarter": null },
  "retro": ["the one lesson that became an executable check in LESSONS.md"]
}
```

## Rules

1. **Never change the headline metric mid-quarter.** Otherwise it is a metric that follows the
   result.
2. **Record `escape_hatches_used` every episode.** If the count trends upward, the DSL is wrong,
   and that should be visible rather than silent.
3. **Record the level you actually achieved, not the one you aimed at.** The genre's currency is
   accuracy, and a channel that overstates its own tier has already spent it.
4. Every retrospective produces at least one entry in `LESSONS.md`, and every `LESSONS.md` entry
   carries an executable check or it does not belong there.
