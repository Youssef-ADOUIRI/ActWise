# Classifier report: classifier-dev

Prompt `classify.v1`, retrieval `hybrid-binding`, split `dev`: 20 scenarios (17 clear, 3 ambiguous).

| Metric | Value |
|---|---|
| **Accuracy, clear scenarios** | **1.0** |
| Accuracy, ambiguous scenarios | 1.0 |
| Prohibited labelled minimal risk | 0 |
| Prohibited or high risk labelled minimal risk | 0 |
| Runs that hit the step budget | 0 |
| Steps / lookups (reads and searches) per run | 3.55 / 3.05 |
| Accuracy by language (clear) | {'en': 1.0, 'fr': 1.0} |

## Confusion (clear scenarios: gold → predicted)

- **prohibited**: {'prohibited': 4}
- **high_risk**: {'high_risk': 5}
- **transparency_only**: {'transparency_only': 3}
- **minimal_risk**: {'minimal_risk': 3}
- **needs_more_info**: {'needs_more_info': 2}

## Misses

| Scenario | Gold | Predicted | Reasons |
|---|---|---|---|
