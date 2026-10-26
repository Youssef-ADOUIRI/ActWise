# Retrieval report: dense-dev

A: structure-aware chunks with their headers, dense BGE-M3, no rerank. Split `dev`, 71 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.789 |
| **Recall@5** | **0.944** [0.89, 0.99] |
| Recall@10 | 0.972 |
| Recall@20 | 0.972 |
| MRR@10 | 0.873 [0.81, 0.93] |
| nDCG@10 | 0.893 |
| ms / query | 143 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 43 | 0.965 | 0.862 |
| fr | 28 | 0.911 | 0.890 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.500 | 0.667 |
| definition | 1 | 0.000 | 0.167 |
| lookup | 39 | 0.974 | 0.874 |
| obligation | 29 | 0.966 | 0.911 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.850 | 0.704 |
| synthetic | 51 | 0.980 | 0.940 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q001 (en) | AIA-AnnexII | 2 | AIA-Art5, AIA-AnnexII, AIA-Rec33 |
| q012 (en) | GDPR-Art22 | 2 | GDPR-Rec71, GDPR-Art22, AIA-Rec42 |
| q014 (en) | GDPR-Art49 | 2 | GDPR-Art45, GDPR-Art49, GDPR-Art46 |
| q018 (en) | GDPR-Art82 | 2 | GDPR-Rec146, GDPR-Art82, GDPR-Art28 |
| q056 (en) | AIA-Art56 | 2 | AIA-Art55, AIA-Art56, AIA-Art53 |
| q063 (fr) | GDPR-Art3 | 2 | GDPR-Rec25, GDPR-Art3, GDPR-Rec80 |
| q093 (en) | AIA-Art15 | 2 | AIA-Rec74, AIA-Art15, AIA-Art40 |
| q016 (en) | GDPR-Art78 | 3 | GDPR-Rec141, GDPR-Art12, GDPR-Art78 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 3 | AIA-Art71, AIA-Rec131, AIA-Art49 |
| q006 (en) | AIA-Art49 | 4 | AIA-Rec131, AIA-Art26, AIA-Art71 |
| q070 (fr) | AIA-Art49 | 4 | AIA-Rec60, AIA-Rec131, AIA-AnnexIII |
| q009 (en) | AIA-Art83 | 6 | AIA-Rec129, AIA-Art48, AIA-Art6 |
| q059 (fr) | GDPR-Art80 | 6 | GDPR-Art77, GDPR-Rec142, GDPR-Rec94 |
| q002 (fr) | AIA-AnnexV | none | AIA-Art47, AIA-Art16, AIA-Art42 |
