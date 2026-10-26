# Retrieval report: bm25-dev

B: structure-aware chunks with their headers, BM25 only, no rerank. Split `dev`, 71 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.627 |
| **Recall@5** | **0.922** [0.86, 0.98] |
| Recall@10 | 0.951 |
| Recall@20 | 0.972 |
| MRR@10 | 0.770 [0.69, 0.84] |
| nDCG@10 | 0.814 |
| ms / query | 7 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 43 | 0.977 | 0.799 |
| fr | 28 | 0.839 | 0.725 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.500 | 0.222 |
| definition | 1 | 1.000 | 0.500 |
| lookup | 39 | 0.910 | 0.775 |
| obligation | 29 | 0.966 | 0.810 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.875 | 0.584 |
| synthetic | 51 | 0.941 | 0.843 |

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
| q058 (en) | GDPR-Art49 | 2 | GDPR-Art44, GDPR-Art49, GDPR-Art45 |
| q064 (en) | GDPR-Art86 | 2 | GDPR-Rec154, GDPR-Art86, GDPR-Rec164 |
| q069 (en) | GDPR-Art23 | 2 | GDPR-Rec19, GDPR-Art23, GDPR-Art9 |
| q071 (fr) | GDPR-Art66 | 2 | GDPR-Rec137, GDPR-Art66, GDPR-Art60 |
| q080 (en) | GDPR-Art80 | 2 | GDPR-Rec142, GDPR-Art80, GDPR-Rec141 |
| q086 (fr) | AIA-Art34 | 2 | AIA-Art31, AIA-Art34, AIA-Art35 |
| q087 (en) | GDPR-Art82 | 2 | GDPR-Rec146, GDPR-Art82, GDPR-Art62 |
| q089 (fr) | GDPR-Art23 | 2 | GDPR-Rec156, GDPR-Art23, AIA-Rec146 |
| q093 (en) | AIA-Art15 | 2 | AIA-Rec74, AIA-Art15, AIA-Rec165 |
| q007 (en) | AIA-Art56 | 3 | AIA-Rec116, AIA-Rec179, AIA-Art56 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 3 | AIA-Rec131, AIA-Rec53, AIA-Art49 |
| q059 (fr) | GDPR-Art80 | 3 | GDPR-Rec142, GDPR-Art77, GDPR-Art80 |
| q002 (fr) | AIA-AnnexV | 5 | AIA-Art47, AIA-AnnexVIII, AIA-Rec173 |
| q016 (en) | GDPR-Art78 | 5 | GDPR-Rec141, GDPR-Art11, GDPR-Art12 |
| q092 (fr) | GDPR-Art36 | 6 | GDPR-Rec94, GDPR-Rec82, GDPR-Art83 |
| q020 (fr) | GDPR-Art80, AIA-Art77 | 9 | GDPR-Rec142, AIA-Rec48, AIA-AnnexVII |
| q070 (fr) | AIA-Art49 | 13 | AIA-AnnexVIII, AIA-Rec131, AIA-Art60 |
| q073 (fr) | GDPR-Art22 | 31 | AIA-Art86, AIA-Art2, AIA-Art76 |
| q010 (en) | GDPR-Art3 | none | GDPR-Rec16, AIA-Rec118, AIA-Rec42 |
