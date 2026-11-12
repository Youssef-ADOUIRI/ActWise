# Retrieval report: minilm-dev

G: structure-aware chunks with their headers, dense multilingual MiniLM-L12 (base), no rerank. Split `dev`, 76 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.474 |
| **Recall@5** | **0.691** [0.58, 0.79] |
| Recall@10 | 0.757 |
| Recall@20 | 0.829 |
| MRR@10 | 0.568 [0.47, 0.66] |
| nDCG@10 | 0.612 |
| ms / query | 17 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 46 | 0.663 | 0.567 |
| fr | 30 | 0.733 | 0.570 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.250 | 0.208 |
| definition | 1 | 0.000 | 0.000 |
| lookup | 39 | 0.692 | 0.569 |
| obligation | 34 | 0.735 | 0.606 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.525 | 0.446 |
| hard | 5 | 0.200 | 0.100 |
| synthetic | 51 | 0.804 | 0.662 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q064 (en) | GDPR-Art86 | 2 | GDPR-Rec154, GDPR-Art86, GDPR-Rec31 |
| q066 (fr) | GDPR-Art67 | 2 | AIA-Art100, GDPR-Art67, AIA-Art70 |
| q071 (fr) | GDPR-Art66 | 2 | GDPR-Rec137, GDPR-Art66, AIA-Art36 |
| q073 (fr) | GDPR-Art22 | 2 | AIA-Rec29, GDPR-Art22, AIA-Art36 |
| q079 (en) | GDPR-Art79 | 2 | GDPR-Rec145, GDPR-Art79, GDPR-Art37 |
| q089 (fr) | GDPR-Art23 | 2 | GDPR-Rec19, GDPR-Art23, GDPR-Rec150 |
| q091 (fr) | GDPR-Art66 | 2 | GDPR-Art64, GDPR-Art66, GDPR-Art65 |
| q099 (fr) | GDPR-Art78 | 2 | GDPR-Rec143, GDPR-Art78, GDPR-Rec141 |
| h018 (en) | AIA-Art49 | 2 | AIA-Rec53, AIA-Art49, AIA-Art22 |
| q060 (en) | GDPR-Art78 | 3 | GDPR-Rec141, GDPR-Art12, GDPR-Art78 |
| q065 (fr) | AIA-Art34 | 3 | AIA-Art31, AIA-Art37, AIA-Art34 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 4 | AIA-Rec53, AIA-Art71, AIA-AnnexVIII |
| q078 (en) | GDPR-Art49 | 4 | GDPR-Art45, GDPR-Rec115, GDPR-Rec101 |
| q002 (fr) | AIA-AnnexV | 5 | AIA-Art47, AIA-AnnexVIII, AIA-Rec3 |
| q006 (en) | AIA-Art49 | 5 | AIA-Art71, AIA-Rec131, AIA-Art26 |
| q070 (fr) | AIA-Art49 | 5 | AIA-AnnexVIII, AIA-Art14, AIA-Art78 |
| q072 (en) | GDPR-Art36 | 5 | AIA-Rec153, GDPR-Rec93, GDPR-Rec129 |
| q020 (fr) | GDPR-Art80, AIA-Art77 | 6 | AIA-Art92, AIA-Rec170, AIA-Rec91 |
| q051 (en) | AIA-Art15 | 7 | AIA-Art55, AIA-Art6, AIA-Art9 |
| q005 (fr) | AIA-Art37, AIA-Art36 | 9 | AIA-Art60, AIA-Art68, AIA-Art31 |
| q058 (en) | GDPR-Art49 | 9 | GDPR-Art45, GDPR-Rec115, GDPR-Rec101 |
| q055 (fr) | AIA-Art83 | 10 | AIA-Art76, AIA-Art85, AIA-Art22 |
| q098 (en) | GDPR-Art49 | 10 | GDPR-Art45, GDPR-Art46, GDPR-Art44 |
| q014 (en) | GDPR-Art49 | 11 | GDPR-Art45, GDPR-Art15, GDPR-Art46 |
| q016 (en) | GDPR-Art78 | 14 | GDPR-Art38, GDPR-Art77, GDPR-Art35 |
| q080 (en) | GDPR-Art80 | 14 | GDPR-Art37, GDPR-Rec108, GDPR-Art38 |
| q093 (en) | AIA-Art15 | 17 | AIA-Art54, AIA-Art4, AIA-AnnexIV |
| q012 (en) | GDPR-Art22 | 19 | GDPR-Rec32, AIA-Rec33, AIA-Rec130 |
| h015 (en) | GDPR-Art3 | 23 | GDPR-Rec17, GDPR-Rec108, AIA-Rec131 |
| q085 (fr) | GDPR-Art3 | 26 | GDPR-Art28, GDPR-Rec81, GDPR-Rec74 |
| q001 (en) | AIA-AnnexII | 29 | AIA-Art3, GDPR-Rec26, GDPR-Rec30 |
| q015 (en) | GDPR-Art66 | 32 | GDPR-Rec116, GDPR-Rec133, GDPR-Rec117 |
| q009 (en) | AIA-Art83 | none | AIA-Art48, AIA-Rec75, AIA-Art60 |
| q010 (en) | GDPR-Art3 | none | AIA-Rec131, AIA-Art71, AIA-Rec8 |
| q059 (fr) | GDPR-Art80 | none | GDPR-Art37, GDPR-Rec141, GDPR-Rec108 |
| q069 (en) | GDPR-Art23 | none | GDPR-Rec9, GDPR-Rec164, GDPR-Rec154 |
| q086 (fr) | AIA-Art34 | none | AIA-Art31, AIA-Art17, AIA-Rec88 |
| h016 (fr) | GDPR-Art22 | none | AIA-Art2, AIA-Rec130, AIA-Art22 |
| h017 (en) | AIA-Art83 | none | AIA-Art48, AIA-Rec129, AIA-Rec130 |
| h019 (fr) | GDPR-Art82 | none | GDPR-Rec85, GDPR-Art32, GDPR-Art15 |
