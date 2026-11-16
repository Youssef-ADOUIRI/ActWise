# Retrieval report: minilm-ft-int8-test

I: as H, exported to ONNX and quantized to int8 (no torch). Split `test`, 84 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.708 |
| **Recall@5** | **0.905** [0.84, 0.96] |
| Recall@10 | 0.952 |
| Recall@20 | 0.970 |
| MRR@10 | 0.817 [0.74, 0.88] |
| nDCG@10 | 0.848 |
| ms / query | 40 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 52 | 0.865 | 0.822 |
| fr | 32 | 0.969 | 0.808 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 3 | 0.667 | 0.583 |
| definition | 1 | 1.000 | 1.000 |
| lookup | 45 | 0.911 | 0.815 |
| obligation | 35 | 0.914 | 0.833 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.850 | 0.730 |
| hard | 6 | 0.500 | 0.389 |
| synthetic | 58 | 0.966 | 0.891 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q032 (en) | AIA-Art111 | 2 | AIA-Art3, AIA-Art111, AIA-Rec177 |
| q033 (en) | AIA-Art87 | 2 | AIA-Rec172, AIA-Art87, GDPR-Art54 |
| q038 (fr) | GDPR-Art85 | 2 | GDPR-Rec153, GDPR-Art85, GDPR-Art17 |
| q041 (fr) | AIA-Art101, GDPR-Art83 | 2 | AIA-Art99, GDPR-Art83, AIA-Art101 |
| q105 (fr) | AIA-Art91 | 2 | AIA-Art102, AIA-Art91, GDPR-Art61 |
| q115 (en) | GDPR-Art70 | 2 | GDPR-Rec140, GDPR-Art70, GDPR-Art43 |
| q116 (fr) | GDPR-Art5 | 2 | GDPR-Rec39, GDPR-Art5, GDPR-Art4 |
| q118 (fr) | GDPR-Art51 | 2 | GDPR-Rec119, GDPR-Art51, AIA-Rec153 |
| q125 (fr) | AIA-Art58 | 2 | AIA-Art57, AIA-Art58, GDPR-Art56 |
| q130 (fr) | GDPR-Art29 | 2 | GDPR-Art4, GDPR-Art29, GDPR-Art32 |
| q139 (en) | AIA-Art111 | 2 | AIA-Rec177, AIA-Art111, AIA-Rec179 |
| q147 (en) | GDPR-Art5 | 2 | GDPR-Rec156, GDPR-Art5, AIA-Art15 |
| q152 (fr) | GDPR-Art83 | 2 | AIA-Art99, GDPR-Art83, GDPR-Rec150 |
| h022 (en) | AIA-Art14 | 2 | AIA-Art60, AIA-Art14, AIA-Art3 |
| h024 (fr) | AIA-Art27 | 2 | AIA-Rec96, AIA-Art27, GDPR-Rec84 |
| q042 (en) | AIA-Art70, GDPR-Art51 | 4 | AIA-Rec153, AIA-Art74, AIA-Art57 |
| q024 (fr) | AIA-Art5 | 5 | AIA-Art3, AIA-Rec132, AIA-Rec134 |
| q137 (en) | AIA-Art79 | 6 | AIA-Art20, AIA-Art82, AIA-Art26 |
| h021 (fr) | AIA-Art5 | 6 | AIA-Rec57, AIA-Art13, AIA-Art9 |
| h023 (en) | GDPR-Art83 | 6 | AIA-Art34, AIA-Art99, AIA-Art101 |
| q023 (en) | AIA-Art5 | 7 | AIA-Rec18, AIA-Art3, AIA-AnnexIII |
| h020 (en) | AIA-Art5 | 20 | AIA-Art3, AIA-Rec18, AIA-Art65 |
| q039 (en) | GDPR-Art89 | 24 | GDPR-Rec162, GDPR-Rec159, GDPR-Rec156 |
| q129 (en) | AIA-Art66 | none | GDPR-Art70, GDPR-Art65, GDPR-Art97 |
