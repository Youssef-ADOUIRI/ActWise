# 010: Answer context: whole paragraphs, the units they name, and a rewritten retry

- **Options:**
  - **What the model reads:** the top 5 windows of 150 words (decision 004), or the first 5 distinct paragraphs of the ranking, whole, in the question's language, under 2,000 words.
  - **References:** none, or up to 3 units that a chosen paragraph names: a point of an annex, a one-unit annex, or another paragraph of the same article. "Article N" is never followed, because 1,166 of the 1,475 paragraphs cite another article.
  - **Query rewriting (`rewrite.v1`, 1–3 queries in the law's words):**
    - never;
    - for every question;
    - only to retry a refused question. The retry adds the first paragraph of each article it reads, since Art. 2(3) means little without Art. 2(1).
  - **How the retry merges its searches:**
    - the rewritten queries fused with the question's own search (RRF);
    - the same searches merged in turns, each one's best paragraph first;
    - the rewritten queries alone, fused with RRF.
  - **Answer prompt:** `answer.v2`, or `answer.v3`, which drops v2's sentence "You give legal information, not legal advice."
- **Measured:**
  - **The hard tuning set:** 18 questions, 13 on train articles and 5 on dev ones. They use everyday words, need two articles, or turn on an exception. Each answer was marked right or wrong against a reference answer in `data/eval/hard_verdicts.csv`. The user marked the baseline. After that, the user marked 7 answers and Claude, at the user's request, 33; Claude's notes start with "Claude:".
  - **Dev, regular questions:** 71 in scope and 12 out of scope, with the same judge as `docs/generation.md`.

    | Phase | Hard refused | Gold article in context (hard) | Hard right | Dev false refusals | Dev faithfulness | Dev precision strict / lenient |
    |---|---|---|---|---|---|---|
    | Baseline: windows, `answer.v2` | 7 / 18 | 72 % | 11 | 2 / 71 | 0.971 [0.93, 1.00] | 0.899 / 0.944 |
    | 1: whole paragraphs | 6 / 18 | 72 % | 11 | 1 / 71 | 0.975 [0.94, 1.00] | 0.902 / 0.967 |
    | 2: + named units | 6 / 18 | 72 % | 11 | 0 / 71 | not judged | 0.906 / – |
    | 3, every question rewritten | 3 / 18 | 94 % | – | 0 / 71 | not judged | **0.840** / – |
    | 3, retry: fused with the question | 2 / 18 | 94 % | – | 0 / 71 | 0.975 [0.94, 1.00] | 0.906 / 0.958 |
    | **3, retry: rewritten queries alone** | 1 / 18 | 100 % | 16 | 0 / 71 | 0.975 [0.94, 1.00] | 0.906 / 0.958 |
    | **+ `answer.v3`** | **1 / 18** | **100 %** | **16** | **0 / 71** | **0.982 [0.96, 1.00]** | **0.923 / 0.945** |

  - **No right answer became wrong** in any phase. The 16 right answers include A ("can a non-EU startup face fines?"), h002, h004, h016 and h017. h012 and h013 are still wrong (`docs/failure_cases.md`).
  - **Rewriting every question** drifts on questions that were already precise. On q009, the rewritten search lost Art. 83, and the answer cited Art. 8, 16, 20 and 80 instead. Dev precision fell to 0.840.
  - **The retry merges**, replayed on the 19 retried questions. Gold articles in the context, out of 8:
    - fused with the question: 6, because the penalty articles, found by two searches, outvoted A's Art. 2(1), found by one;
    - in turns: 6, losing Art. 113 for q050;
    - rewritten queries alone: 8, the only merge that also reaches h017's Art. 83.
  - **`answer.v3`:**
    - **The copied sentence:** answers that repeat v2's legal-advice sentence go from 15 of 94 to 0. The API shows its own disclaimer.
    - **Judged against v2 with the same context:** dev faithfulness 0.975 → 0.982, with fully supported answers at 0.944 for both. On the 13 train hard questions, faithfulness goes from 0.896 to 1.000.
    - **A first wording, v3a,** added "End with your last cited sentence". The model then cited sources on its "not covered" sentence: fully supported answers on dev fell from 0.944 to 0.901, and strict precision on the train hard questions from 1.0 to 0.714. The reports are `evals/reports/v3a-*`.
  - **Cost:**
    - On dev, input tokens rise from 77.6K to 114.8K (+48 %), from whole paragraphs and the named units.
    - A refused question costs two more model calls, the rewrite and a second answer, under the same request deadline. All 12 out-of-scope dev questions take that path and are still refused.
- **Chosen:**
  - **Whole paragraphs** (`ParagraphContext`): 5 paragraphs, 2,000 words.
  - **Up to 3 named units** (`MAX_REFERENCES`).
  - **Retry on refusal:** `rewrite.v1`, the rewritten queries alone fused with RRF, plus each article's first paragraph.
  - **Citation ids in the wrong case are corrected** before the citation check, so `[GDpr-Art3-2]` counts as `[GDPR-Art3-2]`.
  - **`answer.v3`:** it holds every M3 target, and no dev number falls below the baseline's interval.
  - `/ask` uses all of it (`api/app.py`). The classifier doesn't change.
- **Why:**
  - **Windows split the law.** Art. 5(1)(h) reached the model with its list (i)–(iii) before the "unless … strictly necessary" sentence. A whole paragraph keeps a rule and its exceptions together, and following "Annex II" brings in the offences that (h)(iii) refers to.
  - **The retry only runs when it can help.** A question that was answered never pays for it and never drifts. A refused question gets searched in the law's words, the step 8 failure that question A showed.
  - **The question's own search already failed,** so in the retry it only takes slots from what a rewritten query alone finds.
- **Revisit if:**
  - **Latency:** the p95 of a retried `/ask` gets close to the 50 s budget in step 14's load test.
  - **Cost:** the extra calls on out-of-scope questions matter. A cheap out-of-scope check before the retry would save them.
  - **h012:** the exception it needs, GDPR Art. 17(3)(b), never reaches the context, and no retrieved paragraph names it.
  - **The test split,** read once at the end of the project, disagrees with these tuning numbers.
