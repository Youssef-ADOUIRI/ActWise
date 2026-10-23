# Retrieval report: hybrid-dev

C: structure-aware chunks with their headers, dense BGE-M3 + BM25 fused with RRF, no rerank. Split `dev`, 20 scored questions (2 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.375 |
| **Recall@5** | **0.900** [0.78, 1.00] |
| Recall@10 | 0.925 |
| Recall@20 | 1.000 |
| MRR@10 | 0.629 [0.49, 0.78] |
| nDCG@10 | 0.698 |
| ms / query | 174 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 13 | 0.962 | 0.596 |
| fr | 7 | 0.786 | 0.691 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.500 | 0.333 |
| definition | 1 | 1.000 | 0.333 |
| lookup | 12 | 0.917 | 0.632 |
| obligation | 5 | 1.000 | 0.800 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q001 (en) | AIA-AnnexII | 2 | AIA-Art5, AIA-AnnexII, AIA-Rec33 |
| q006 (en) | AIA-Art49 | 2 | AIA-Rec131, AIA-Art49, AIA-Art26 |
| q007 (en) | AIA-Art56 | 2 | AIA-Rec116, AIA-Art56, AIA-Rec179 |
| q012 (en) | GDPR-Art22 | 2 | GDPR-Rec71, GDPR-Art22, AIA-Rec42 |
| q013 (fr) | GDPR-Art36 | 2 | GDPR-Rec94, GDPR-Art36, GDPR-Rec127 |
| q014 (en) | GDPR-Art49 | 2 | GDPR-Art45, GDPR-Art49, GDPR-Art48 |
| q009 (en) | AIA-Art83 | 3 | AIA-Art48, AIA-Rec129, AIA-Art83 |
| q016 (en) | GDPR-Art78 | 3 | GDPR-Rec141, GDPR-Art12, GDPR-Art78 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 3 | AIA-Rec131, AIA-Art71, AIA-Art49 |
| q020 (fr) | GDPR-Art80, AIA-Art77 | 3 | AIA-Rec32, AIA-Rec59, AIA-Art77 |
| q010 (en) | GDPR-Art3 | 4 | GDPR-Rec16, GDPR-Art2, GDPR-Rec18 |
| q002 (fr) | AIA-AnnexV | 12 | AIA-Art47, AIA-Art16, AIA-AnnexVIII |
