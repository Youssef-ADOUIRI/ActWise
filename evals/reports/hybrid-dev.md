# Retrieval report: hybrid-dev

C: structure-aware chunks with their headers, dense BGE-M3 + BM25 fused with RRF, no rerank. Split `dev`, 71 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.697 |
| **Recall@5** | **0.972** [0.94, 1.00] |
| Recall@10 | 0.979 |
| Recall@20 | 1.000 |
| MRR@10 | 0.822 [0.75, 0.88] |
| nDCG@10 | 0.860 |
| ms / query | 158 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 43 | 0.988 | 0.831 |
| fr | 28 | 0.946 | 0.808 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.500 | 0.333 |
| definition | 1 | 1.000 | 0.333 |
| lookup | 39 | 0.974 | 0.808 |
| obligation | 29 | 1.000 | 0.891 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.900 | 0.629 |
| synthetic | 51 | 1.000 | 0.898 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q001 (en) | AIA-AnnexII | 2 | AIA-Art5, AIA-AnnexII, AIA-Rec33 |
| q006 (en) | AIA-Art49 | 2 | AIA-Rec131, AIA-Art49, AIA-Art26 |
| q007 (en) | AIA-Art56 | 2 | AIA-Rec116, AIA-Art56, AIA-Rec179 |
| q012 (en) | GDPR-Art22 | 2 | GDPR-Rec71, GDPR-Art22, AIA-Rec42 |
| q013 (fr) | GDPR-Art36 | 2 | GDPR-Rec94, GDPR-Art36, GDPR-Rec127 |
| q014 (en) | GDPR-Art49 | 2 | GDPR-Art45, GDPR-Art49, GDPR-Art48 |
| q056 (en) | AIA-Art56 | 2 | AIA-Art55, AIA-Art56, AIA-Art53 |
| q058 (en) | GDPR-Art49 | 2 | GDPR-Art44, GDPR-Art49, GDPR-Art45 |
| q063 (fr) | GDPR-Art3 | 2 | GDPR-Rec25, GDPR-Art3, GDPR-Rec23 |
| q087 (en) | GDPR-Art82 | 2 | GDPR-Rec146, GDPR-Art82, GDPR-Art79 |
| q092 (fr) | GDPR-Art36 | 2 | GDPR-Rec94, GDPR-Art36, GDPR-Rec131 |
| q093 (en) | AIA-Art15 | 2 | AIA-Rec74, AIA-Art15, AIA-Rec165 |
| q009 (en) | AIA-Art83 | 3 | AIA-Art48, AIA-Rec129, AIA-Art83 |
| q016 (en) | GDPR-Art78 | 3 | GDPR-Rec141, GDPR-Art12, GDPR-Art78 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 3 | AIA-Rec131, AIA-Art71, AIA-Art49 |
| q020 (fr) | GDPR-Art80, AIA-Art77 | 3 | AIA-Rec32, AIA-Rec59, AIA-Art77 |
| q059 (fr) | GDPR-Art80 | 3 | GDPR-Art77, GDPR-Rec142, GDPR-Art80 |
| q010 (en) | GDPR-Art3 | 4 | GDPR-Rec16, GDPR-Art2, GDPR-Rec18 |
| q073 (fr) | GDPR-Art22 | 4 | AIA-Art86, AIA-Art2, AIA-Art5 |
| q070 (fr) | AIA-Art49 | 5 | AIA-Rec131, AIA-Rec60, AIA-AnnexIII |
| q002 (fr) | AIA-AnnexV | 12 | AIA-Art47, AIA-Art16, AIA-AnnexVIII |
