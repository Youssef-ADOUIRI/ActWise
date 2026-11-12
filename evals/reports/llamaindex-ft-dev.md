# Retrieval report: llamaindex-ft-dev

K: as H, embedded, stored and searched by LlamaIndex. Split `dev`, 76 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.599 |
| **Recall@5** | **0.849** [0.76, 0.92] |
| Recall@10 | 0.941 |
| Recall@20 | 0.967 |
| MRR@10 | 0.712 [0.63, 0.79] |
| nDCG@10 | 0.765 |
| ms / query | 103 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 46 | 0.804 | 0.689 |
| fr | 30 | 0.917 | 0.747 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 1.000 | 0.333 |
| definition | 1 | 0.000 | 0.167 |
| lookup | 39 | 0.885 | 0.723 |
| obligation | 34 | 0.824 | 0.737 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.775 | 0.596 |
| hard | 5 | 0.400 | 0.275 |
| synthetic | 51 | 0.922 | 0.800 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q002 (fr) | AIA-AnnexV | 2 | AIA-Art47, AIA-AnnexV, AIA-AnnexIV |
| q060 (en) | GDPR-Art78 | 2 | GDPR-Rec141, GDPR-Art78, GDPR-Art12 |
| q064 (en) | GDPR-Art86 | 2 | GDPR-Rec154, GDPR-Art86, AIA-Art77 |
| q071 (fr) | GDPR-Art66 | 2 | GDPR-Rec137, GDPR-Art66, GDPR-Rec85 |
| q073 (fr) | GDPR-Art22 | 2 | AIA-Art86, GDPR-Art22, AIA-Art5 |
| q074 (en) | GDPR-Art30 | 2 | GDPR-Rec82, GDPR-Art30, GDPR-Art28 |
| q091 (fr) | GDPR-Art66 | 2 | GDPR-Art64, GDPR-Art66, GDPR-Art65 |
| q006 (en) | AIA-Art49 | 3 | AIA-Art26, AIA-Art71, AIA-Art49 |
| q010 (en) | GDPR-Art3 | 3 | GDPR-Rec23, GDPR-Rec24, GDPR-Art3 |
| q012 (en) | GDPR-Art22 | 3 | GDPR-Rec143, GDPR-Rec32, GDPR-Art22 |
| q014 (en) | GDPR-Art49 | 3 | GDPR-Art45, GDPR-Art46, GDPR-Art49 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 3 | AIA-Art71, AIA-AnnexVIII, GDPR-Art30 |
| q020 (fr) | GDPR-Art80, AIA-Art77 | 3 | AIA-Rec57, AIA-Rec56, AIA-Art77 |
| q080 (en) | GDPR-Art80 | 3 | GDPR-Rec142, GDPR-Art77, GDPR-Art80 |
| q086 (fr) | AIA-Art34 | 3 | AIA-Art31, AIA-Art17, AIA-Art34 |
| q055 (fr) | AIA-Art83 | 4 | AIA-Art22, AIA-Art54, AIA-Rec29 |
| q069 (en) | GDPR-Art23 | 4 | GDPR-Art9, GDPR-Rec164, GDPR-Art90 |
| q070 (fr) | AIA-Art49 | 4 | AIA-Rec60, AIA-AnnexIII, AIA-AnnexVIII |
| h019 (fr) | GDPR-Art82 | 4 | GDPR-Art12, GDPR-Art15, GDPR-Rec85 |
| q009 (en) | AIA-Art83 | 6 | AIA-Art48, AIA-Rec75, AIA-Rec129 |
| q015 (en) | GDPR-Art66 | 7 | GDPR-Art62, GDPR-Art61, GDPR-Rec134 |
| q058 (en) | GDPR-Art49 | 7 | GDPR-Art44, GDPR-Rec101, GDPR-Art45 |
| q093 (en) | AIA-Art15 | 8 | AIA-AnnexIV, AIA-Art95, AIA-Rec133 |
| q098 (en) | GDPR-Art49 | 8 | GDPR-Art45, GDPR-Art46, GDPR-Rec107 |
| h017 (en) | AIA-Art83 | 8 | AIA-Rec129, AIA-Art48, AIA-Art24 |
| q016 (en) | GDPR-Art78 | 9 | GDPR-Art60, AIA-Art85, GDPR-Rec130 |
| q059 (fr) | GDPR-Art80 | 12 | GDPR-Art77, GDPR-Rec141, GDPR-Art12 |
| h015 (en) | GDPR-Art3 | 12 | GDPR-Rec23, GDPR-Rec53, AIA-AnnexX |
| q001 (en) | AIA-AnnexII | none | AIA-Art5, AIA-Art50, AIA-Rec33 |
| h016 (fr) | GDPR-Art22 | none | AIA-Art2, GDPR-Art32, GDPR-Rec43 |
