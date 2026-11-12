# Classifier report: classifier-dev

Classifier `agent`, prompt `classify.v1`, retrieval `hybrid-binding`, split `dev`: 20 scenarios (17 clear, 3 ambiguous).

Scored again from the saved runs on 2026-11-12, at commit `afe4c97`; no model was called.

| Metric | Value |
|---|---|
| **Accuracy, clear scenarios** | **1.0** |
| Accuracy, ambiguous scenarios | 1.0 |
| **Recall, prohibited (all scenarios)** | **1.0** (4 of 4) |
| **Recall, high risk (all scenarios)** | **1.0** (6 of 6) |
| Prohibited labelled minimal risk | 0 |
| Prohibited or high risk labelled minimal risk | 0 |
| Runs that hit the step budget | 0 |
| Steps / lookups (reads and searches) per run | 3.55 / 3.05 |
| Seconds / input tokens per run | 1.163 / 8714 |
| Accuracy by language (clear) | {'en': 1.0, 'fr': 1.0} |

## Confusion matrix (all scenarios: gold rows, predicted columns)

In the first two rows, a count right of the diagonal is an under-classified system, except in `needs_more_info`, which asks for the missing facts. Failed runs are not in the matrix.

| Gold \ predicted | prohibited | high_risk | transparency_only | minimal_risk | needs_more_info |
|---|---|---|---|---|---|
| **prohibited** | 4 | 0 | 0 | 0 | 0 |
| **high_risk** | 0 | 6 | 0 | 0 | 0 |
| **transparency_only** | 0 | 0 | 3 | 0 | 0 |
| **minimal_risk** | 0 | 0 | 0 | 5 | 0 |
| **needs_more_info** | 0 | 0 | 0 | 0 | 2 |

## Misses

| Scenario | Gold | Predicted | Reasons |
|---|---|---|---|
