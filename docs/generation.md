# Answer quality

Each row answers the **dev** split: 20 in-scope questions and 2 out-of-scope ones. Run it with `make eval-answers SYSTEM=<system> PROMPT=<prompt>`. The judge is `openai/gpt-oss-120b` on Groq with `judge.v1`. It is a different model family from the Gemini answerer, and it is **not yet calibrated**: the human labels come in step 6b. The numbers are provisional. With two out-of-scope questions, the refusal rate can only be 0, 0.5 or 1.

| Row | Retrieval | Prompt | Out-of-scope refused | False refusals | Invented (shown) | Faithfulness | Citation precision strict / lenient | Report |
|---|---|---|---|---|---|---|---|---|
| baseline | naive windows, dense (Recall@5 0.650) | `plain` (step 5) | 0 / 2 | 0 / 20 | 0 (0) | 0.989 [0.97, 1.00] | n/a: no citations | [baseline-dev-plain](../evals/reports/baseline-dev-plain.md) |
| v1 | E, `hybrid-binding` (0.925) | `answer.v1` | 2 / 2 | **4 / 20** | 0 (0) | 1.000 [1.00, 1.00] | 0.870 / 1.000 | [answer.v1](../evals/reports/hybrid-binding-dev-answer.v1.md) |
| **v2** | E, `hybrid-binding` (0.925) | `answer.v2` | 2 / 2 | **0 / 20** | 0 (0) | 0.988 [0.96, 1.00] | 0.828 / 0.897 | [answer.v2](../evals/reports/hybrid-binding-dev-answer.v2.md) |

Every report comes from commit `9d5aefa`. Gemini 3.5 Flash-Lite writes every answer, at temperature 0 from the top 5 passages.

## What each change did

- **Plain baseline:** the answers stick to their context, with faithfulness at 0.99. But the baseline cites nothing and refuses nothing. On both out-of-scope questions it says the context has no information, then adds unrelated facts from it (q021 lists GPAI fines).
- **v1:** both out-of-scope questions are refused, and no citation is invented. But it refuses **4 in-scope questions** whose sources answer only part of the question:
  - q006 and q007: the gold article is in the top 5.
  - q019 and q020: cross-law questions whose GDPR article is not retrieved (`failure_cases.md`).
- **v2:** one rule changed. When the sources cover part of a question, answer that part and say what they don't cover; `NOT_COVERED` is kept for questions the sources say nothing about. False refusals fall from 4 to 0, and both out-of-scope questions are still refused. Lenient precision drops to 0.90 because the four partial answers bring harder citations.

## Choice (provisional)

**v2** is the working prompt. It answers every in-scope question and still refuses the out-of-scope ones, with no invented citation. Step 6b re-runs this table on the 150-question set, with 10 dev refusal questions and a judge calibrated against human labels. Only then is the choice final.

## Against the M3 targets (dev)

| Target | v2 now | Status |
|---|---|---|
| Invented citations shown = 0 | 0 | ✅ guaranteed by the pipeline, which reads citations back from the shown text and refuses otherwise |
| Faithfulness ≥ 0.85 | 0.988 | provisional: judge not calibrated yet |
| Citation precision ≥ 0.90 | 0.897 lenient, 0.828 strict | just below; re-measured on 150 questions |
| Out-of-scope refusals ≥ 95 % | 2 / 2 | not measurable on 2 questions; 10 in step 6b |
| Judge kappa ≥ 0.6 | — | step 6b, from 58 human labels |

## Why the judge is not trusted yet

It gives almost every answer a 5: 56 of the 58 verdicts across the three rows. Either the answers really are faithful (the plain baseline only rephrases its context), or the judge is lenient. The calibration sheet settles this. It mixes 45 real answers with 13 that were rewritten to include one unsupported claim, all scored blind by a person. If the judge misses the planted claims, `judge.v2` gets stricter rules before any number above is final.
