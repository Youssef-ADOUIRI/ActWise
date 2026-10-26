# Judge calibration

Judge `openai/gpt-oss-120b` with `judge.v1`, against 58 human labels (13 answers with a planted unsupported claim). Faithful = score 4 or 5.

| Measure | Value |
|---|---|
| **Cohen's kappa, faithful = 4–5 (target ≥ 0.6)** | **0.7393** |
| Agreement, faithful = 4–5 | 0.931 |
| Cohen's kappa, faithful = 5 only | 0.9517 |
| Quadratic-weighted kappa, 1–5 | 0.8995 |
| Planted claims marked below 5: human / judge | 12/13 / 12/13 |
| Unreadable judge replies | 0 |

## Disagreements at 4

| Item | Kind | Question | Human | Judge | Judge's reason |
|---|---|---|---|---|---|
| h11 | perturbed | q003 | 3 | 4 | The answer accurately reflects Article 15(4) except for the added 'within 30 days' which is not mentioned in the source. |
| h34 | perturbed | q001 | 3 | 4 | Main claim is supported but the added detail about a 48‑hour limit is not in the source |
| h41 | real | q001 | 2 | 4 | Main claim is supported, but the statement that sources do not cover point (h)(i) is inaccurate. |
| h50 | perturbed | q005 | 2 | 4 | Main claim that the Commission can investigate is supported, but the added detail of a 48‑hour deadline for the notifying authority is not found in the sources. |
