# Retrieval report: minilm-ft-test

H: as G, fine-tuned on questions written from train paragraphs. Split `test`, 84 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.696 |
| **Recall@5** | **0.917** [0.85, 0.96] |
| Recall@10 | 0.941 |
| Recall@20 | 0.964 |
| MRR@10 | 0.803 [0.73, 0.87] |
| nDCG@10 | 0.834 |
| ms / query | 21 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 52 | 0.865 | 0.791 |
| fr | 32 | 1.000 | 0.821 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 3 | 0.667 | 0.583 |
| definition | 1 | 1.000 | 1.000 |
| lookup | 45 | 0.911 | 0.792 |
| obligation | 35 | 0.943 | 0.830 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.850 | 0.738 |
| hard | 6 | 0.667 | 0.367 |
| synthetic | 58 | 0.966 | 0.870 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q024 (fr) | AIA-Art5 | 2 | AIA-Rec132, AIA-Art5, AIA-Art3 |
| q032 (en) | AIA-Art111 | 2 | AIA-Art3, AIA-Art111, AIA-Rec179 |
| q033 (en) | AIA-Art87 | 2 | AIA-Rec172, AIA-Art87, GDPR-Art54 |
| q038 (fr) | GDPR-Art85 | 2 | GDPR-Rec153, GDPR-Art85, GDPR-Art17 |
| q041 (fr) | AIA-Art101, GDPR-Art83 | 2 | AIA-Art99, GDPR-Art83, AIA-Art101 |
| q118 (fr) | GDPR-Art51 | 2 | GDPR-Rec119, GDPR-Art51, AIA-Rec153 |
| q125 (fr) | AIA-Art58 | 2 | AIA-Art57, AIA-Art58, AIA-Art112 |
| q126 (en) | GDPR-Art92 | 2 | AIA-Art97, GDPR-Art92, AIA-Art33 |
| q130 (fr) | GDPR-Art29 | 2 | GDPR-Art4, GDPR-Art29, GDPR-Art32 |
| q139 (en) | AIA-Art111 | 2 | AIA-Rec177, AIA-Art111, AIA-Rec179 |
| q147 (en) | GDPR-Art5 | 2 | GDPR-Rec156, GDPR-Art5, AIA-Art15 |
| q152 (fr) | GDPR-Art83 | 2 | AIA-Art99, GDPR-Art83, GDPR-Rec150 |
| h022 (en) | AIA-Art14 | 2 | AIA-Art60, AIA-Art14, AIA-Art3 |
| q115 (en) | GDPR-Art70 | 3 | GDPR-Rec140, GDPR-Art43, GDPR-Art70 |
| h024 (fr) | AIA-Art27 | 3 | AIA-Rec96, GDPR-Rec84, AIA-Art27 |
| q042 (en) | AIA-Art70, GDPR-Art51 | 4 | AIA-Rec153, AIA-Art74, AIA-Art57 |
| q145 (en) | AIA-Art12 | 4 | AIA-Rec95, AIA-Art5, AIA-Rec38 |
| q156 (fr) | AIA-Art58 | 4 | AIA-Art66, AIA-Art96, AIA-Art101 |
| h021 (fr) | AIA-Art5 | 5 | AIA-Art13, AIA-Rec57, AIA-Art9 |
| h023 (en) | GDPR-Art83 | 6 | AIA-Art34, AIA-Art99, AIA-Art101 |
| q137 (en) | AIA-Art79 | 7 | AIA-Art20, AIA-Art82, AIA-Art26 |
| q023 (en) | AIA-Art5 | 11 | AIA-Rec18, AIA-Art3, AIA-AnnexIII |
| h020 (en) | AIA-Art5 | 21 | AIA-Art3, AIA-Rec18, AIA-Art50 |
| q039 (en) | GDPR-Art89 | none | GDPR-Rec162, GDPR-Rec159, GDPR-Rec39 |
| q129 (en) | AIA-Art66 | none | GDPR-Art70, GDPR-Art65, AIA-Art112 |
