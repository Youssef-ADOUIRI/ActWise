# Retrieval report: hybrid-binding-dev-76q

E: as C, with articles and annexes ranked before recitals. Split `dev`, 76 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.789 |
| **Recall@5** | **0.954** [0.91, 0.99] |
| Recall@10 | 0.974 |
| Recall@20 | 0.987 |
| MRR@10 | 0.878 [0.82, 0.93] |
| nDCG@10 | 0.899 |
| ms / query | 196 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 46 | 0.978 | 0.880 |
| fr | 30 | 0.917 | 0.873 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.750 | 0.750 |
| definition | 1 | 1.000 | 0.500 |
| lookup | 39 | 0.974 | 0.877 |
| obligation | 34 | 0.941 | 0.897 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.925 | 0.806 |
| hard | 5 | 0.600 | 0.500 |
| synthetic | 51 | 1.000 | 0.943 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q001 (en) | AIA-AnnexII | 2 | AIA-Art5, AIA-AnnexII, AIA-Art61 |
| q009 (en) | AIA-Art83 | 2 | AIA-Art48, AIA-Art83, AIA-Art24 |
| q010 (en) | GDPR-Art3 | 2 | GDPR-Art2, GDPR-Art3, GDPR-Art47 |
| q014 (en) | GDPR-Art49 | 2 | GDPR-Art45, GDPR-Art49, GDPR-Art48 |
| q016 (en) | GDPR-Art78 | 2 | GDPR-Art12, GDPR-Art78, GDPR-Art77 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 2 | AIA-Art71, AIA-Art49, AIA-AnnexV |
| q056 (en) | AIA-Art56 | 2 | AIA-Art55, AIA-Art56, AIA-Art53 |
| q058 (en) | GDPR-Art49 | 2 | GDPR-Art44, GDPR-Art49, GDPR-Art45 |
| q059 (fr) | GDPR-Art80 | 2 | GDPR-Art77, GDPR-Art80, GDPR-Art34 |
| h018 (en) | AIA-Art49 | 2 | AIA-Art24, AIA-Art49, AIA-Art6 |
| q070 (fr) | AIA-Art49 | 3 | AIA-AnnexIII, AIA-AnnexVIII, AIA-Art49 |
| q073 (fr) | GDPR-Art22 | 4 | AIA-Art86, AIA-Art2, AIA-Art5 |
| q002 (fr) | AIA-AnnexV | 9 | AIA-Art47, AIA-Art16, AIA-AnnexVIII |
| h016 (fr) | GDPR-Art22 | 11 | AIA-Art74, GDPR-Art61, AIA-Art5 |
| h017 (en) | AIA-Art83 | none | AIA-Art48, AIA-Art23, AIA-Art24 |
