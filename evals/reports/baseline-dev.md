# Retrieval report: baseline-dev

Baseline: fixed 150-word windows (25 shared) ignoring structure, dense BGE-M3, cosine similarity, no rerank. Split `dev`, 71 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.289 |
| **Recall@5** | **0.775** [0.68, 0.87] |
| Recall@10 | 0.873 |
| Recall@20 | 0.908 |
| MRR@10 | 0.484 [0.40, 0.56] |
| nDCG@10 | 0.574 |
| ms / query | 145 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 43 | 0.779 | 0.497 |
| fr | 28 | 0.768 | 0.464 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.250 | 0.100 |
| definition | 1 | 0.000 | 0.000 |
| lookup | 39 | 0.756 | 0.528 |
| obligation | 29 | 0.862 | 0.468 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.650 | 0.504 |
| synthetic | 51 | 0.824 | 0.476 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q006 (en) | AIA-Art49 | 2 | AIA-Rec131, AIA-Art49, AIA-Rec130 |
| q054 (fr) | GDPR-Art30 | 2 | GDPR-Rec13, GDPR-Art30, GDPR-Rec97 |
| q060 (en) | GDPR-Art78 | 2 | GDPR-Art77, GDPR-Art78, GDPR-Rec141 |
| q065 (fr) | AIA-Art34 | 2 | AIA-Art29, AIA-Art34, AIA-Art27 |
| q070 (fr) | AIA-Art49 | 2 | AIA-Rec131, AIA-Art49, AIA-Art78 |
| q074 (en) | GDPR-Art30 | 2 | GDPR-Art29, GDPR-Art30, GDPR-Rec97 |
| q077 (en) | AIA-Art77 | 2 | AIA-Art76, AIA-Art77, AIA-Rec59 |
| q086 (fr) | AIA-Art34 | 2 | AIA-Art31, AIA-Art34, AIA-Art43 |
| q093 (en) | AIA-Art15 | 2 | AIA-Rec74, AIA-Art15, AIA-Rec142 |
| q096 (en) | GDPR-Art30 | 2 | GDPR-Rec81, GDPR-Art30, GDPR-Art29 |
| q098 (en) | GDPR-Art49 | 2 | GDPR-Art46, GDPR-Art49, GDPR-Rec107 |
| q011 (fr) | GDPR-Art14 | 3 | GDPR-Art13, GDPR-Art12, GDPR-Art14 |
| q013 (fr) | GDPR-Art36 | 3 | GDPR-Art35, GDPR-Rec94, GDPR-Art36 |
| q053 (en) | GDPR-Art14 | 3 | GDPR-Art13, GDPR-Rec61, GDPR-Art14 |
| q055 (fr) | AIA-Art83 | 3 | AIA-Art82, AIA-Art79, AIA-Art83 |
| q058 (en) | GDPR-Art49 | 3 | GDPR-Art47, GDPR-Art44, GDPR-Art49 |
| q059 (fr) | GDPR-Art80 | 3 | GDPR-Art57, GDPR-Art76, GDPR-Art80 |
| q071 (fr) | GDPR-Art66 | 3 | GDPR-Art65, GDPR-Rec136, GDPR-Art66 |
| q083 (en) | AIA-Art37 | 3 | AIA-Art36, AIA-Art31, AIA-Art37 |
| q087 (en) | GDPR-Art82 | 3 | GDPR-Rec146, GDPR-Art81, GDPR-Art82 |
| q088 (en) | AIA-Art38 | 3 | AIA-Art37, AIA-Art31, AIA-Art38 |
| q094 (en) | GDPR-Art22 | 3 | GDPR-Rec70, GDPR-Art21, GDPR-Art22 |
| q097 (en) | AIA-Art77 | 3 | AIA-Art76, AIA-Art78, AIA-Art77 |
| q099 (fr) | GDPR-Art78 | 3 | GDPR-Art77, GDPR-Rec143, GDPR-Art78 |
| q007 (en) | AIA-Art56 | 4 | AIA-Rec179, AIA-Rec116, AIA-Rec173 |
| q012 (en) | GDPR-Art22 | 4 | GDPR-Rec71, GDPR-Rec70, GDPR-Art21 |
| q067 (en) | GDPR-Art82 | 4 | GDPR-Rec145, GDPR-Rec146, GDPR-Art81 |
| q069 (en) | GDPR-Art23 | 4 | GDPR-Rec72, GDPR-Art22, GDPR-Rec19 |
| q073 (fr) | GDPR-Art22 | 4 | GDPR-Art21, AIA-Art2, AIA-Rec10 |
| q075 (fr) | AIA-Art83 | 4 | AIA-Art82, AIA-Art79, AIA-Rec155 |
| q078 (en) | GDPR-Art49 | 4 | GDPR-Rec107, GDPR-Art45, GDPR-Rec113 |
| q095 (en) | GDPR-Art14 | 4 | GDPR-Art13, GDPR-Rec59, GDPR-Rec61 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 5 | AIA-Rec131, AIA-Art71, AIA-AnnexVIII |
| q084 (fr) | AIA-Art36 | 5 | AIA-Art35, AIA-Art34, AIA-Art29 |
| q092 (fr) | GDPR-Art36 | 5 | GDPR-Art35, GDPR-Rec94, GDPR-Rec131 |
| q056 (en) | AIA-Art56 | 6 | AIA-Rec116, AIA-Art53, AIA-Art54 |
| q064 (en) | GDPR-Art86 | 6 | GDPR-Rec154, GDPR-Rec153, GDPR-Rec31 |
| q090 (en) | AIA-Art49 | 6 | AIA-Rec131, AIA-Art48, AIA-Rec53 |
| q010 (en) | GDPR-Art3 | 9 | GDPR-Rec23, GDPR-Rec24, AIA-Art74 |
| q014 (en) | GDPR-Art49 | 9 | GDPR-Art44, GDPR-Rec101, GDPR-Art46 |
| q081 (en) | GDPR-Art78 | 9 | GDPR-Rec135, GDPR-Art60, GDPR-Art66 |
| q061 (fr) | AIA-Art37 | 10 | AIA-Art34, AIA-Art30, AIA-Art29 |
| q066 (fr) | GDPR-Art67 | 12 | GDPR-Art66, GDPR-Art61, GDPR-Rec168 |
| q001 (en) | AIA-AnnexII | 15 | AIA-Art5, AIA-Rec42, AIA-Rec32 |
| q009 (en) | AIA-Art83 | 29 | AIA-Art23, AIA-Art48, AIA-Rec128 |
| q063 (fr) | GDPR-Art3 | 29 | GDPR-Rec115, GDPR-Rec23, GDPR-Rec79 |
| q002 (fr) | AIA-AnnexV | none | AIA-Art46, AIA-Art47, AIA-Art42 |
| q020 (fr) | GDPR-Art80, AIA-Art77 | none | AIA-Art76, AIA-Rec59, AIA-Rec70 |
| q068 (en) | AIA-Art38 | none | AIA-Art37, AIA-Art43, AIA-Art34 |
| q085 (fr) | GDPR-Art3 | none | GDPR-Rec22, GDPR-Rec20, GDPR-Rec17 |
