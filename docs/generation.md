# Answer quality

Each row answers the **dev** split: 71 in-scope questions (20 hand-written, 51 reviewed synthetic) and 12 out-of-scope ones. Run it with `make eval-answers SYSTEM=<system> PROMPT=<prompt>`.
- **Answers:** Gemini 3.5 Flash-Lite writes each one at temperature 0, from the top 5 passages of system E (`hybrid-binding`, Recall@5 0.979 on these questions).
- **Judge:** `openai/gpt-oss-120b` on Groq with `judge.v1`, calibrated against 58 human labels: **kappa 0.739** ([decision 007](decisions/007-judge-calibration.md)).

| Row | Prompt | Out-of-scope refused | False refusals | Invented (shown) | Faithfulness | Fully supported | Citation precision strict / lenient | Report |
|---|---|---|---|---|---|---|---|---|
| v1 | `answer.v1` | 12 / 12 | 5 / 71 (7.0 %) | 0 (0) | 0.992 [0.98, 1.00] | 0.985 | 0.925 / 1.000 | [answer.v1](../evals/reports/hybrid-binding-dev-answer.v1.md) |
| **v2** | `answer.v2` | 12 / 12 | **2 / 71 (2.8 %)** | 0 (0) | 0.971 [0.93, 1.00] | 0.942 | 0.899 / 0.944 | [answer.v2](../evals/reports/hybrid-binding-dev-answer.v2.md) |
| baseline | `plain`, naive retrieval (Recall@5 0.775) | 0 / 12 | 0 / 71 | 0 (0) | 0.991 [0.98, 1.00] | 0.964 | n/a: no citations | [baseline-dev-plain](../evals/reports/baseline-dev-plain.md) |

The v1 and v2 rows come from commit `c07703c`, the baseline from `8dc2a89`. The baseline is just as faithful to its context, but it cites nothing and refuses none of the 12 out-of-scope questions: those are the gains of the cited pipeline. Faithfulness is (score − 1) / 4 averaged over the answers given. Fully supported is the share of answers scored 5, with no unsupported claim at all; the judge and the human labels agree best on that one (kappa 0.952).

## Hand-written and synthetic apart

| Prompt | Source | n | False refusals | Faithfulness | Fully supported | Precision strict / lenient |
|---|---|---|---|---|---|---|
| v1 | hand-written | 22 | 4 / 20 | 1.000 | 1.000 | 0.870 / 1.000 |
| v1 | synthetic | 61 | 1 / 51 | 0.990 | 0.980 | 0.947 / 1.000 |
| v2 | hand-written | 22 | 0 / 20 | 0.988 | 0.950 | 0.828 / 0.897 |
| v2 | synthetic | 61 | 2 / 51 | 0.964 | 0.939 | 0.933 / 0.967 |

Each source has its out-of-scope questions (2 hand-written, 10 synthetic), and both prompts refuse all of them.

## The A/B: v2 wins

v2 changes one rule: when the sources answer part of a question, answer that part and say what they don't cover. `NOT_COVERED` is kept for questions the sources say nothing about.

- **False refusals fall from 5 to 2.**
  - v1's misses are the four partly covered hand-written questions (q006, q007, q019, q020) plus q073.
  - v2's two (q072, q081) are answers that came back with no citation. The pipeline refuses those rather than show an uncited answer.
- **The cost is faithfulness, 0.992 → 0.971.** The new rule sometimes claims a part is not covered when a source covers it:
  - q061: it says the sources don't say what to send the Commission, but Art. 37(2) does. Judge score 1; v1 gets 5.
  - q085: it adds a "not covered" sentence that Art. 3(2) and 3(3) contradict. Judge score 3.

Both prompts pass every target. **v2 is the serving prompt**, because a refusal gives the user nothing. Its known failure, a wrong "not covered" sentence in 2 of 69 answers, is the first thing a v3 would fix.

## Step 8b: what the model reads (decision 010)

The same 83 dev questions, with system E. "Windows" is the top 5 windows of the rows above; the other rows read whole paragraphs. Each report is `evals/reports/<row>-dev.md`. The hard tuning set (18 questions, right/wrong verdicts) is in decision 010.

| Row | Context | Prompt | Out-of-scope refused | False refusals | Invented (shown) | Faithfulness | Fully supported | Citation precision strict / lenient |
|---|---|---|---|---|---|---|---|---|
| baseline8b | windows | `answer.v2` | 12 / 12 | 2 / 71 (2.8 %) | 0 (0) | 0.971 [0.93, 1.00] | 0.942 | 0.899 / 0.944 |
| phase1 | whole paragraphs | `answer.v2` | 12 / 12 | 1 / 71 (1.4 %) | 0 (0) | 0.975 [0.94, 1.00] | 0.943 | 0.902 / 0.967 |
| phase2 | + up to 3 named units | `answer.v2` | 12 / 12 | 0 / 71 | 0 (0) | not judged | – | 0.906 / – |
| phase3 | + every question rewritten | `answer.v2` | 12 / 12 | 0 / 71 | 0 (0) | not judged | – | **0.840** / – |
| **phase3q** | phase2 + a refusal retried with rewritten queries | `answer.v2` | 12 / 12 | **0 / 71** | 0 (0) | **0.975 [0.94, 1.00]** | 0.944 | 0.906 / 0.958 |
| v3a | as phase3q | `answer.v3`, first wording | 12 / 12 | 0 / 71 | 0 (0) | 0.968 [0.94, 0.99] | 0.901 | 0.912 / 0.956 |
| v3 | as phase3q | `answer.v3` | 12 / 12 | 0 / 71 | 0 (0) | *judge pending* | – | 0.923 / – |

- **baseline8b** gives the same numbers as v2 above: the answers come from the cache.
- **Whole paragraphs** remove repeated windows from the context, and **phase3q** answers every in-scope question.
- **Rewriting every question** (phase3) drifts on precise ones, so the rewrite only retries a refusal.
- **Retry variants:** two other merges of the retry's searches give the same dev numbers as phase3q (`phase3r`, `phase3i`). Their differences show on the hard set (decision 010).
- **v3** drops v2's "You give legal information, not legal advice", which 15 of 94 answers repeated. The API shows its own disclaimer.

## Against the M3 targets (dev, v2)

| Target | v2 | Status |
|---|---|---|
| Invented citations shown = 0 | 0 | ✅ guaranteed by the pipeline, which reads citations back from the shown text and refuses otherwise |
| Faithfulness ≥ 0.85 | 0.971 [0.93, 1.00] | ✅ (fully supported: 0.942) |
| Citation precision ≥ 0.90 | 0.944 lenient, 0.899 strict | ✅ on the judge-based reading. Strict counts a citation outside the gold article as wrong, even when it supports the sentence |
| Out-of-scope refusals ≥ 95 % | 12 / 12 | ✅ |
| Judge vs human kappa ≥ 0.6 | 0.739 | ✅ |

Test-split numbers are reported once, at the end of the project.
