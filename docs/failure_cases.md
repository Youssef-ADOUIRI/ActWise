# Failure cases: error analysis of step 4

**Scope:** the 20 scored dev questions (all of them, since dev has 20). A question fails when its gold article is not ranked first, or when Recall@5 is below 1, as for a cross-law question that finds one of its two articles.

**Starting point:** row C (dense + BM25 with RRF). It had the best Recall@5 before this analysis, but ranked only 8 of the 20 gold articles first.

Ranks below are those of the first gold article; "R@5 0.5" means one of two gold articles is in the top 5.

| Question | Gold | Ranked above it in C | Cause | C | E | F |
|---|---|---|---|---|---|---|
| q001 (en) | AI Act Annex II | Art. 5, which refers to the list in Annex II | Cross-reference | 2 | 2 | 2 |
| q002 (fr) | AI Act Annex V | Art. 47 (the declaration "contains the information set out in Annex V"), Art. 16, Annex VIII | Cross-reference | 12 | 9 | 9 |
| q006 (en) | AI Act Art. 49 | Recital 131 | Recital | 2 | 1 | 1 |
| q007 (en) | AI Act Art. 56 | Recital 116 | Recital | 2 | 1 | 1 |
| q009 (en) | AI Act Art. 83 | Art. 48 (CE marking), Recital 129 | Neighbouring article, recital | 3 | 2 | 1 |
| q010 (en) | GDPR Art. 3 | Recitals 16 and 18, Art. 2 (material scope) | Recital, neighbouring article | 4 | 2 | 1 |
| q012 (en) | GDPR Art. 22 | Recital 71 | Recital | 2 | 1 | 1 |
| q013 (fr) | GDPR Art. 36 | Recital 94 | Recital | 2 | 1 | 1 |
| q014 (en) | GDPR Art. 49 | Art. 45 (adequacy decisions) | Neighbouring article | 2 | 2 | 1 |
| q016 (en) | GDPR Art. 78 | Recital 141, Art. 12 | Recital, neighbouring article | 3 | 2 | 1 |
| q019 (en) | GDPR Art. 30 + AI Act Art. 49 | Recital 131, Art. 71; GDPR Art. 30 outside the top 5 | Cross-law, recital | 3, R@5 0.5 | 2 | 2 |
| q020 (fr) | GDPR Art. 80 + AI Act Art. 77 | Recitals 32 and 59; GDPR Art. 80 outside the top 5 | Cross-law, recital | 3, R@5 0.5 | 1, R@5 0.5 | 1, R@5 0.5 |

The other 8 questions rank their gold article first in C, E and F.

## Causes

| Cause | Questions in C | Note |
|---|---|---|
| **A recital outranks the article** | 9 of 12 | Recitals restate an article in plain words, close to how people ask. They explain the law but do not bind. |
| A neighbouring article on the same subject | 4 | Scope (Art. 2 vs 3), adequacy vs derogations (Art. 45 vs 49), CE marking vs formal non-compliance (Art. 48 vs 83) |
| The article that cites the gold annex wins | 2 | The article names the annex; the annex holds the list the question asks about |
| A cross-law question finds one law | 2 | The AI Act half of the question dominates both rankings |
| Wrong language, short question, bad gold label | 0 | Gold labels of q001 and q002 re-checked against the text; both are right |

French questions have Recall@5 0.786 against 1.000 in English. That comes from q002 and q020, which fail for the cross-reference and cross-law reasons, not because of their language. So the optional query-language filter was not needed.

## The fix: binding text first

The biggest cause gets a rule instead of a tuned weight: articles and annexes come before recitals, and each group keeps its fused order (`HybridRetriever(binding_first=True)`). Recitals stay in the list, after the binding text, so the answer generator can still read them.

Effect: MRR@10 0.629 → 0.806 (C → E) and Recall@5 0.900 → 0.925, at the same latency. With the reranker, MRR@10 is 0.760 → 0.906 (D → F). Recitals were also hiding GDPR Art. 30 in q019, which now enters the top 5.

## What is left

| Question | Why | Idea, not done |
|---|---|---|
| q001, q002 | The article that refers to the annex ranks above the annex | Follow references: when a retrieved article names an annex ("set out in Annex V"), add that annex right after it |
| q009, q010, q014, q016 | A neighbouring article ranks first (E); the reranker fixes all four (F) | Keep for the generator, which reads the top 5; or a reranker cheap enough to serve (decision 004) |
| q020 | GDPR Art. 80 stays outside the top 5 | Retrieve once per law (`where={"law": ...}`) when a question names both laws, then interleave |

Each idea fixes one or two of 20 questions, so they wait for the 150-question set of step 6, where a gain can be told apart from noise.
