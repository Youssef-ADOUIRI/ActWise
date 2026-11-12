# Retrieval report: hybrid-binding-test

E: as C, with articles and annexes ranked before recitals. Split `test`, 84 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.869 |
| **Recall@5** | **0.976** [0.95, 1.00] |
| Recall@10 | 0.994 |
| Recall@20 | 0.994 |
| MRR@10 | 0.924 [0.88, 0.97] |
| nDCG@10 | 0.936 |
| ms / query | 203 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 52 | 0.971 | 0.896 |
| fr | 32 | 0.984 | 0.969 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 3 | 0.667 | 0.833 |
| definition | 1 | 1.000 | 1.000 |
| lookup | 45 | 0.978 | 0.887 |
| obligation | 35 | 1.000 | 0.977 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.900 | 0.900 |
| hard | 6 | 1.000 | 0.867 |
| synthetic | 58 | 1.000 | 0.938 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q042 (en) | AIA-Art70, GDPR-Art51 | 2 | AIA-Art77, GDPR-Art51, GDPR-Art59 |
| q105 (fr) | AIA-Art91 | 2 | AIA-Art62, AIA-Art91, AIA-Art78 |
| q125 (fr) | AIA-Art58 | 2 | AIA-Art57, AIA-Art58, AIA-Art59 |
| q137 (en) | AIA-Art79 | 2 | AIA-Art82, AIA-Art79, AIA-Art20 |
| q033 (en) | AIA-Art87 | 3 | AIA-Art50, AIA-Art59, AIA-Art87 |
| q126 (en) | GDPR-Art92 | 3 | AIA-Art97, GDPR-Art43, GDPR-Art92 |
| q129 (en) | AIA-Art66 | 3 | GDPR-Art70, AIA-Art96, AIA-Art66 |
| q145 (en) | AIA-Art12 | 4 | AIA-Art5, AIA-AnnexIII, AIA-Art26 |
| h022 (en) | AIA-Art14 | 5 | AIA-Art20, AIA-Art6, AIA-Art26 |
| q034 (en) | AIA-AnnexVI | 6 | AIA-Art43, AIA-Art16, AIA-Art14 |
