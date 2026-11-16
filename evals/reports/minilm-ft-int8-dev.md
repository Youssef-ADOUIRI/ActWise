# Retrieval report: minilm-ft-int8-dev

I: as H, exported to ONNX and quantized to int8 (no torch). Split `dev`, 76 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.586 |
| **Recall@5** | **0.862** [0.78, 0.93] |
| Recall@10 | 0.901 |
| Recall@20 | 0.967 |
| MRR@10 | 0.702 [0.61, 0.79] |
| nDCG@10 | 0.749 |
| ms / query | 8 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 46 | 0.826 | 0.688 |
| fr | 30 | 0.917 | 0.722 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 1.000 | 0.333 |
| definition | 1 | 0.000 | 0.000 |
| lookup | 39 | 0.885 | 0.703 |
| obligation | 34 | 0.853 | 0.742 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.775 | 0.565 |
| hard | 5 | 0.400 | 0.267 |
| synthetic | 51 | 0.941 | 0.798 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q006 (en) | AIA-Art49 | 2 | AIA-Art26, AIA-Art49, AIA-Art71 |
| q008 (fr) | AIA-Art68 | 2 | AIA-Rec147, AIA-Art68, AIA-Art69 |
| q012 (en) | GDPR-Art22 | 2 | GDPR-Rec143, GDPR-Art22, GDPR-Rec32 |
| q060 (en) | GDPR-Art78 | 2 | GDPR-Rec141, GDPR-Art78, GDPR-Art12 |
| q064 (en) | GDPR-Art86 | 2 | GDPR-Rec154, GDPR-Art86, AIA-Art77 |
| q071 (fr) | GDPR-Art66 | 2 | GDPR-Rec137, GDPR-Art66, GDPR-Rec85 |
| q073 (fr) | GDPR-Art22 | 2 | AIA-Art86, GDPR-Art22, AIA-Art5 |
| q074 (en) | GDPR-Art30 | 2 | GDPR-Rec82, GDPR-Art30, GDPR-Rec97 |
| q002 (fr) | AIA-AnnexV | 3 | AIA-Art47, AIA-AnnexIV, AIA-AnnexV |
| q010 (en) | GDPR-Art3 | 3 | GDPR-Rec23, GDPR-Rec24, GDPR-Art3 |
| q014 (en) | GDPR-Art49 | 3 | GDPR-Art45, GDPR-Art46, GDPR-Art49 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 3 | AIA-Art71, AIA-AnnexVIII, AIA-Art49 |
| q020 (fr) | GDPR-Art80, AIA-Art77 | 3 | GDPR-Rec142, AIA-Rec57, GDPR-Art80 |
| q080 (en) | GDPR-Art80 | 3 | GDPR-Rec142, GDPR-Art77, GDPR-Art80 |
| q086 (fr) | AIA-Art34 | 3 | AIA-Art31, AIA-Art17, AIA-Art34 |
| q091 (fr) | GDPR-Art66 | 3 | GDPR-Art64, GDPR-Art65, GDPR-Art66 |
| h019 (fr) | GDPR-Art82 | 3 | GDPR-Art12, GDPR-Art15, GDPR-Art82 |
| q055 (fr) | AIA-Art83 | 4 | AIA-Art22, AIA-Art54, AIA-Rec29 |
| q069 (en) | GDPR-Art23 | 4 | GDPR-Art9, GDPR-Rec164, GDPR-Art90 |
| q070 (fr) | AIA-Art49 | 4 | AIA-Rec60, AIA-AnnexIII, AIA-AnnexVIII |
| q093 (en) | AIA-Art15 | 5 | AIA-AnnexIV, AIA-Rec148, AIA-Art95 |
| q098 (en) | GDPR-Art49 | 7 | GDPR-Art46, GDPR-Art45, GDPR-Rec107 |
| q016 (en) | GDPR-Art78 | 8 | GDPR-Art60, GDPR-Art77, GDPR-Rec130 |
| q058 (en) | GDPR-Art49 | 9 | GDPR-Rec101, GDPR-Art44, GDPR-Art45 |
| q015 (en) | GDPR-Art66 | 11 | GDPR-Art62, AIA-Rec154, GDPR-Art52 |
| h017 (en) | AIA-Art83 | 12 | AIA-Rec129, AIA-Art48, AIA-Art24 |
| q009 (en) | AIA-Art83 | 13 | AIA-Rec75, AIA-Art48, AIA-Art79 |
| h015 (en) | GDPR-Art3 | 13 | GDPR-Rec23, GDPR-Rec53, AIA-Rec60 |
| q059 (fr) | GDPR-Art80 | 16 | GDPR-Rec141, GDPR-Art77, GDPR-Art12 |
| q001 (en) | AIA-AnnexII | none | AIA-Art5, AIA-Rec33, AIA-Rec34 |
| h016 (fr) | GDPR-Art22 | none | AIA-Art2, GDPR-Art32, GDPR-Rec43 |
