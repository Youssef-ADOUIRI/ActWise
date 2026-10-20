# Retrieval report: dense-dev

A: structure-aware chunks with their headers, dense BGE-M3, no rerank. Split `dev`, 20 scored questions (2 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.500 |
| **Recall@5** | **0.850** [0.70, 0.97] |
| Recall@10 | 0.900 |
| Recall@20 | 0.900 |
| MRR@10 | 0.704 [0.55, 0.85] |
| nDCG@10 | 0.737 |
| ms / query | 160 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 13 | 0.885 | 0.622 |
| fr | 7 | 0.786 | 0.857 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.500 | 0.667 |
| definition | 1 | 0.000 | 0.167 |
| lookup | 12 | 0.917 | 0.736 |
| obligation | 5 | 1.000 | 0.750 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q001 (en) | AIA-AnnexII | 2 | AIA-Art5, AIA-AnnexII, AIA-Rec33 |
| q012 (en) | GDPR-Art22 | 2 | GDPR-Rec71, GDPR-Art22, AIA-Rec42 |
| q014 (en) | GDPR-Art49 | 2 | GDPR-Art45, GDPR-Art49, GDPR-Art46 |
| q018 (en) | GDPR-Art82 | 2 | GDPR-Rec146, GDPR-Art82, GDPR-Art28 |
| q016 (en) | GDPR-Art78 | 3 | GDPR-Rec141, GDPR-Art12, GDPR-Art78 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 3 | AIA-Art71, AIA-Rec131, AIA-Art49 |
| q006 (en) | AIA-Art49 | 4 | AIA-Rec131, AIA-Art26, AIA-Art71 |
| q009 (en) | AIA-Art83 | 6 | AIA-Rec129, AIA-Art48, AIA-Art6 |
| q002 (fr) | AIA-AnnexV | none | AIA-Art47, AIA-Art16, AIA-Art42 |
