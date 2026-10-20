# Retrieval report: hybrid-binding-dev

E: as C, with articles and annexes ranked before recitals. Split `dev`, 20 scored questions (2 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.600 |
| **Recall@5** | **0.925** [0.80, 1.00] |
| Recall@10 | 1.000 |
| Recall@20 | 1.000 |
| MRR@10 | 0.806 [0.69, 0.93] |
| nDCG@10 | 0.842 |
| ms / query | 149 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 13 | 1.000 | 0.769 |
| fr | 7 | 0.786 | 0.873 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.750 | 0.750 |
| definition | 1 | 1.000 | 0.500 |
| lookup | 12 | 0.917 | 0.759 |
| obligation | 5 | 1.000 | 1.000 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q001 (en) | AIA-AnnexII | 2 | AIA-Art5, AIA-AnnexII, AIA-Art61 |
| q009 (en) | AIA-Art83 | 2 | AIA-Art48, AIA-Art83, AIA-Art24 |
| q010 (en) | GDPR-Art3 | 2 | GDPR-Art2, GDPR-Art3, GDPR-Art47 |
| q014 (en) | GDPR-Art49 | 2 | GDPR-Art45, GDPR-Art49, GDPR-Art48 |
| q016 (en) | GDPR-Art78 | 2 | GDPR-Art12, GDPR-Art78, GDPR-Art77 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 2 | AIA-Art71, AIA-Art49, AIA-AnnexV |
| q002 (fr) | AIA-AnnexV | 9 | AIA-Art47, AIA-Art16, AIA-AnnexVIII |
