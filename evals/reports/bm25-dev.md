# Retrieval report: bm25-dev

B: structure-aware chunks with their headers, BM25 only, no rerank. Split `dev`, 20 scored questions (2 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.325 |
| **Recall@5** | **0.875** [0.72, 1.00] |
| Recall@10 | 0.925 |
| Recall@20 | 0.950 |
| MRR@10 | 0.584 [0.44, 0.74] |
| nDCG@10 | 0.661 |
| ms / query | 6 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 13 | 0.923 | 0.567 |
| fr | 7 | 0.786 | 0.616 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.500 | 0.222 |
| definition | 1 | 1.000 | 0.500 |
| lookup | 12 | 0.875 | 0.603 |
| obligation | 5 | 1.000 | 0.700 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q001 (en) | AIA-AnnexII | 2 | AIA-Art5, AIA-AnnexII, AIA-Rec35 |
| q003 (en) | AIA-Art15 | 2 | AIA-Art3, AIA-Art15, AIA-Rec12 |
| q006 (en) | AIA-Art49 | 2 | AIA-Rec131, AIA-Art49, AIA-Art26 |
| q009 (en) | AIA-Art83 | 2 | AIA-Art48, AIA-Art83, AIA-Art80 |
| q012 (en) | GDPR-Art22 | 2 | GDPR-Rec71, GDPR-Art22, AIA-Rec42 |
| q013 (fr) | GDPR-Art36 | 2 | GDPR-Rec94, GDPR-Art36, GDPR-Rec127 |
| q017 (fr) | GDPR-Art79 | 2 | GDPR-Rec37, GDPR-Art79, GDPR-Rec80 |
| q007 (en) | AIA-Art56 | 3 | AIA-Rec116, AIA-Rec179, AIA-Art56 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 3 | AIA-Rec131, AIA-Rec53, AIA-Art49 |
| q002 (fr) | AIA-AnnexV | 5 | AIA-Art47, AIA-AnnexVIII, AIA-Rec173 |
| q016 (en) | GDPR-Art78 | 5 | GDPR-Rec141, GDPR-Art11, GDPR-Art12 |
| q020 (fr) | GDPR-Art80, AIA-Art77 | 9 | GDPR-Rec142, AIA-Rec48, AIA-AnnexVII |
| q010 (en) | GDPR-Art3 | none | GDPR-Rec16, AIA-Rec118, AIA-Rec42 |
