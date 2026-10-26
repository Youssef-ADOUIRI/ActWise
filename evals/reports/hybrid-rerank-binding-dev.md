# Retrieval report: hybrid-rerank-binding-dev

F: as D, with articles and annexes ranked before recitals. Split `dev`, 71 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.930 |
| **Recall@5** | **0.979** [0.94, 1.00] |
| Recall@10 | 1.000 |
| Recall@20 | 1.000 |
| MRR@10 | 0.966 [0.93, 0.99] |
| nDCG@10 | 0.973 |
| ms / query | 11894 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 43 | 1.000 | 0.965 |
| fr | 28 | 0.946 | 0.968 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.750 | 0.750 |
| definition | 1 | 1.000 | 1.000 |
| lookup | 39 | 0.974 | 0.964 |
| obligation | 29 | 1.000 | 0.983 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.925 | 0.906 |
| synthetic | 51 | 1.000 | 0.990 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q001 (en) | AIA-AnnexII | 2 | AIA-Art5, AIA-AnnexII, AIA-Rec38 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 2 | AIA-Art71, AIA-Art49, GDPR-Art30 |
| q093 (en) | AIA-Art15 | 2 | AIA-Rec74, AIA-Art15, AIA-Rec165 |
| q002 (fr) | AIA-AnnexV | 9 | AIA-Art47, AIA-Art24, AIA-Art42 |
