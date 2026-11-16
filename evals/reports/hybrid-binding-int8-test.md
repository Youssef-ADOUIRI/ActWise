# Retrieval report: hybrid-binding-int8-test

J: as E, with the int8 MiniLM of I instead of BGE-M3. Split `test`, 84 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.821 |
| **Recall@5** | **0.988** [0.97, 1.00] |
| Recall@10 | 0.994 |
| Recall@20 | 0.994 |
| MRR@10 | 0.902 [0.85, 0.95] |
| nDCG@10 | 0.922 |
| ms / query | 52 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 52 | 0.981 | 0.893 |
| fr | 32 | 1.000 | 0.917 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 3 | 0.667 | 0.833 |
| definition | 1 | 1.000 | 1.000 |
| lookup | 45 | 1.000 | 0.918 |
| obligation | 35 | 1.000 | 0.883 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.950 | 0.912 |
| hard | 6 | 1.000 | 0.569 |
| synthetic | 58 | 1.000 | 0.932 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q039 (en) | GDPR-Art89 | 2 | GDPR-Art6, GDPR-Art89, GDPR-Art5 |
| q042 (en) | AIA-Art70, GDPR-Art51 | 2 | AIA-Art74, AIA-Art70, AIA-Art28 |
| q126 (en) | GDPR-Art92 | 2 | AIA-Art97, GDPR-Art92, AIA-Art33 |
| q130 (fr) | GDPR-Art29 | 2 | GDPR-Art4, GDPR-Art29, GDPR-Art32 |
| q132 (fr) | AIA-Art14 | 2 | AIA-Art1, AIA-Art14, AIA-Art26 |
| q137 (en) | AIA-Art79 | 2 | AIA-Art20, AIA-Art79, AIA-Art82 |
| q152 (fr) | GDPR-Art83 | 2 | AIA-Art99, GDPR-Art83, AIA-Art100 |
| h024 (fr) | AIA-Art27 | 2 | AIA-AnnexVIII, AIA-Art27, AIA-Art9 |
| q145 (en) | AIA-Art12 | 3 | AIA-AnnexIII, AIA-Art5, AIA-Art12 |
| h021 (fr) | AIA-Art5 | 3 | AIA-Art9, AIA-Art4, AIA-Art5 |
| h022 (en) | AIA-Art14 | 3 | AIA-Art20, AIA-Art60, AIA-Art14 |
| q023 (en) | AIA-Art5 | 4 | AIA-Art3, GDPR-Art88, AIA-AnnexIII |
| q129 (en) | AIA-Art66 | 4 | GDPR-Art70, AIA-Art96, GDPR-Art65 |
| h020 (en) | AIA-Art5 | 4 | AIA-Art65, AIA-Art3, AIA-Art14 |
