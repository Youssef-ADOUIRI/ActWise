# Retrieval report: baseline-dev

Baseline: fixed 150-word windows (25 shared) ignoring structure, dense BGE-M3, cosine similarity, no rerank. Split `dev`, 20 scored questions (2 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.375 |
| **Recall@5** | **0.650** [0.45, 0.85] |
| Recall@10 | 0.750 |
| Recall@20 | 0.825 |
| MRR@10 | 0.504 [0.32, 0.69] |
| nDCG@10 | 0.547 |
| ms / query | 184 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 13 | 0.654 | 0.494 |
| fr | 7 | 0.643 | 0.524 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.250 | 0.100 |
| definition | 1 | 0.000 | 0.000 |
| lookup | 12 | 0.625 | 0.560 |
| obligation | 5 | 1.000 | 0.633 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q006 (en) | AIA-Art49 | 2 | AIA-Rec131, AIA-Art49, AIA-Rec130 |
| q011 (fr) | GDPR-Art14 | 3 | GDPR-Art13, GDPR-Art12, GDPR-Art14 |
| q013 (fr) | GDPR-Art36 | 3 | GDPR-Art35, GDPR-Rec94, GDPR-Art36 |
| q007 (en) | AIA-Art56 | 4 | AIA-Rec179, AIA-Rec116, AIA-Rec173 |
| q012 (en) | GDPR-Art22 | 4 | GDPR-Rec71, GDPR-Rec70, GDPR-Art21 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 5 | AIA-Rec131, AIA-Art71, AIA-AnnexVIII |
| q010 (en) | GDPR-Art3 | 9 | GDPR-Rec23, GDPR-Rec24, AIA-Art74 |
| q014 (en) | GDPR-Art49 | 9 | GDPR-Art44, GDPR-Rec101, GDPR-Art46 |
| q001 (en) | AIA-AnnexII | 15 | AIA-Art5, AIA-Rec42, AIA-Rec32 |
| q009 (en) | AIA-Art83 | 29 | AIA-Art23, AIA-Art48, AIA-Rec128 |
| q002 (fr) | AIA-AnnexV | none | AIA-Art46, AIA-Art47, AIA-Art42 |
| q020 (fr) | GDPR-Art80, AIA-Art77 | none | AIA-Art76, AIA-Rec59, AIA-Rec70 |
