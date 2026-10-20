# Retrieval report: hybrid-rerank-dev

D: structure-aware chunks with their headers, dense BGE-M3 + BM25 fused with RRF, top 20 reranked by bge-reranker-v2-m3. Split `dev`, 20 scored questions (2 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.550 |
| **Recall@5** | **0.900** [0.78, 1.00] |
| Recall@10 | 0.925 |
| Recall@20 | 1.000 |
| MRR@10 | 0.760 [0.61, 0.90] |
| nDCG@10 | 0.793 |
| ms / query | 12534 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 13 | 0.962 | 0.746 |
| fr | 7 | 0.786 | 0.786 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.500 | 0.600 |
| definition | 1 | 1.000 | 1.000 |
| lookup | 12 | 0.917 | 0.708 |
| obligation | 5 | 1.000 | 0.900 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q001 (en) | AIA-AnnexII | 2 | AIA-Art5, AIA-AnnexII, AIA-Rec34 |
| q007 (en) | AIA-Art56 | 2 | AIA-Rec179, AIA-Art56, AIA-Rec116 |
| q010 (en) | GDPR-Art3 | 2 | GDPR-Rec24, GDPR-Art3, GDPR-Art2 |
| q012 (en) | GDPR-Art22 | 2 | GDPR-Rec71, GDPR-Art22, AIA-Rec42 |
| q013 (fr) | GDPR-Art36 | 2 | GDPR-Rec94, GDPR-Art36, GDPR-Rec127 |
| q016 (en) | GDPR-Art78 | 2 | GDPR-Rec141, GDPR-Art78, GDPR-Art12 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 5 | AIA-Rec53, AIA-Rec131, AIA-Rec141 |
| q002 (fr) | AIA-AnnexV | 12 | AIA-Art47, AIA-Art24, AIA-Rec173 |
