# Retrieval report: hybrid-binding-int8-dev

J: as E, with the int8 MiniLM of I instead of BGE-M3. Split `dev`, 76 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.697 |
| **Recall@5** | **0.961** [0.91, 1.00] |
| Recall@10 | 0.961 |
| Recall@20 | 0.987 |
| MRR@10 | 0.810 [0.73, 0.88] |
| nDCG@10 | 0.847 |
| ms / query | 15 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 46 | 0.957 | 0.819 |
| fr | 30 | 0.967 | 0.796 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 1.000 | 0.750 |
| definition | 1 | 1.000 | 0.500 |
| lookup | 39 | 1.000 | 0.853 |
| obligation | 34 | 0.912 | 0.773 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 1.000 | 0.746 |
| hard | 5 | 0.400 | 0.240 |
| synthetic | 51 | 1.000 | 0.890 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q001 (en) | AIA-AnnexII | 2 | AIA-Art5, AIA-AnnexII, AIA-Art50 |
| q009 (en) | AIA-Art83 | 2 | AIA-Art48, AIA-Art83, AIA-Art79 |
| q012 (en) | GDPR-Art22 | 2 | AIA-Art5, GDPR-Art22, AIA-Art36 |
| q013 (fr) | GDPR-Art36 | 2 | GDPR-Art56, GDPR-Art36, GDPR-Art58 |
| q016 (en) | GDPR-Art78 | 2 | GDPR-Art77, GDPR-Art78, GDPR-Art12 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 2 | AIA-Art71, AIA-Art49, AIA-AnnexVIII |
| q069 (en) | GDPR-Art23 | 2 | GDPR-Art9, GDPR-Art23, GDPR-Art90 |
| q086 (fr) | AIA-Art34 | 2 | AIA-Art31, AIA-Art34, AIA-Art17 |
| q092 (fr) | GDPR-Art36 | 2 | GDPR-Art56, GDPR-Art36, GDPR-Art60 |
| q093 (en) | AIA-Art15 | 2 | AIA-AnnexIV, AIA-Art15, AIA-AnnexXI |
| q002 (fr) | AIA-AnnexV | 3 | AIA-Art47, AIA-AnnexVIII, AIA-AnnexV |
| q015 (en) | GDPR-Art66 | 3 | AIA-Art79, GDPR-Art62, GDPR-Art66 |
| q058 (en) | GDPR-Art49 | 3 | GDPR-Art44, GDPR-Art45, GDPR-Art49 |
| q073 (fr) | GDPR-Art22 | 3 | AIA-Art86, AIA-Art2, GDPR-Art22 |
| q014 (en) | GDPR-Art49 | 4 | GDPR-Art45, GDPR-Art46, GDPR-Art48 |
| q059 (fr) | GDPR-Art80 | 4 | GDPR-Art77, GDPR-Art12, GDPR-Art78 |
| q070 (fr) | AIA-Art49 | 4 | AIA-AnnexVIII, AIA-AnnexIII, AIA-Art78 |
| q098 (en) | GDPR-Art49 | 4 | GDPR-Art45, GDPR-Art46, GDPR-Art44 |
| h019 (fr) | GDPR-Art82 | 5 | GDPR-Art4, GDPR-Art32, GDPR-Art12 |
| h015 (en) | GDPR-Art3 | 12 | GDPR-Art93, AIA-Art2, AIA-Art49 |
| h017 (en) | AIA-Art83 | 12 | AIA-Art48, AIA-Art3, AIA-Art24 |
| h016 (fr) | GDPR-Art22 | none | AIA-Art26, GDPR-Art12, AIA-Art2 |
