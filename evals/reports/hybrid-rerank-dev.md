# Retrieval report: hybrid-rerank-dev

D: structure-aware chunks with their headers, dense BGE-M3 + BM25 fused with RRF, top 20 reranked by bge-reranker-v2-m3. Split `dev`, 71 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.817 |
| **Recall@5** | **0.972** [0.94, 1.00] |
| Recall@10 | 0.979 |
| Recall@20 | 1.000 |
| MRR@10 | 0.904 [0.85, 0.95] |
| nDCG@10 | 0.921 |
| ms / query | 12638 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 43 | 0.988 | 0.912 |
| fr | 28 | 0.946 | 0.893 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.500 | 0.600 |
| definition | 1 | 1.000 | 1.000 |
| lookup | 39 | 0.974 | 0.885 |
| obligation | 29 | 1.000 | 0.948 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.900 | 0.760 |
| synthetic | 51 | 1.000 | 0.961 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q001 (en) | AIA-AnnexII | 2 | AIA-Art5, AIA-AnnexII, AIA-Rec34 |
| q007 (en) | AIA-Art56 | 2 | AIA-Rec179, AIA-Art56, AIA-Rec116 |
| q010 (en) | GDPR-Art3 | 2 | GDPR-Rec24, GDPR-Art3, GDPR-Art2 |
| q012 (en) | GDPR-Art22 | 2 | GDPR-Rec71, GDPR-Art22, AIA-Rec42 |
| q013 (fr) | GDPR-Art36 | 2 | GDPR-Rec94, GDPR-Art36, GDPR-Rec127 |
| q016 (en) | GDPR-Art78 | 2 | GDPR-Rec141, GDPR-Art78, GDPR-Art12 |
| q059 (fr) | GDPR-Art80 | 2 | GDPR-Rec142, GDPR-Art80, GDPR-Art77 |
| q070 (fr) | AIA-Art49 | 2 | AIA-Rec131, AIA-Art49, AIA-Rec159 |
| q085 (fr) | GDPR-Art3 | 2 | GDPR-Rec22, GDPR-Art3, GDPR-Rec36 |
| q093 (en) | AIA-Art15 | 2 | AIA-Rec74, AIA-Art15, AIA-Rec165 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 5 | AIA-Rec53, AIA-Rec131, AIA-Rec141 |
| q002 (fr) | AIA-AnnexV | 12 | AIA-Art47, AIA-Art24, AIA-Rec173 |
