# Retrieval report: minilm-test

G: structure-aware chunks with their headers, dense multilingual MiniLM-L12 (base), no rerank. Split `test`, 84 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.446 |
| **Recall@5** | **0.720** [0.62, 0.81] |
| Recall@10 | 0.768 |
| Recall@20 | 0.827 |
| MRR@10 | 0.579 [0.49, 0.67] |
| nDCG@10 | 0.620 |
| ms / query | 70 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 52 | 0.692 | 0.584 |
| fr | 32 | 0.766 | 0.571 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 3 | 0.500 | 0.667 |
| definition | 1 | 1.000 | 1.000 |
| lookup | 45 | 0.733 | 0.610 |
| obligation | 35 | 0.714 | 0.520 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.675 | 0.480 |
| hard | 6 | 0.000 | 0.052 |
| synthetic | 58 | 0.810 | 0.668 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q026 (fr) | AIA-Art12 | 2 | AIA-Art60, AIA-Art12, AIA-Art26 |
| q027 (en) | AIA-Art14 | 2 | AIA-Art26, AIA-Art14, AIA-Art60 |
| q035 (en) | GDPR-Art29 | 2 | GDPR-Art32, GDPR-Art29, GDPR-Art28 |
| q041 (fr) | AIA-Art101, GDPR-Art83 | 2 | AIA-Rec162, AIA-Art101, AIA-Rec109 |
| q042 (en) | AIA-Art70, GDPR-Art51 | 2 | AIA-Rec81, AIA-Art70, AIA-Rec153 |
| q103 (en) | GDPR-Art89 | 2 | GDPR-Rec158, GDPR-Art89, GDPR-Rec154 |
| q104 (fr) | AIA-Art79 | 2 | AIA-Art80, AIA-Art79, AIA-Art75 |
| q120 (en) | GDPR-Art83 | 2 | AIA-Art99, GDPR-Art83, GDPR-Rec142 |
| q121 (en) | AIA-Art5 | 2 | AIA-Rec34, AIA-Art5, AIA-Art3 |
| q123 (en) | AIA-Art25 | 2 | AIA-Art60, AIA-Art25, AIA-Art6 |
| q141 (fr) | AIA-Art71 | 2 | AIA-Art10, AIA-Art71, AIA-Rec131 |
| q142 (fr) | GDPR-Art85 | 2 | GDPR-Rec153, GDPR-Art85, GDPR-Rec10 |
| q150 (fr) | GDPR-Art51 | 2 | AIA-Art46, GDPR-Art51, AIA-Rec37 |
| q152 (fr) | GDPR-Art83 | 2 | GDPR-Rec150, GDPR-Art83, AIA-Art99 |
| q155 (fr) | AIA-Art25 | 2 | AIA-Rec86, AIA-Art25, AIA-Rec84 |
| q028 (en) | AIA-Art25 | 3 | AIA-Art24, AIA-Rec86, AIA-Art25 |
| q127 (en) | AIA-Art75 | 3 | AIA-Art79, AIA-Art80, AIA-Art75 |
| q130 (fr) | GDPR-Art29 | 3 | GDPR-Art32, GDPR-Art4, GDPR-Art29 |
| q137 (en) | AIA-Art79 | 3 | AIA-Art72, AIA-Art60, AIA-Art79 |
| q156 (fr) | AIA-Art58 | 3 | AIA-Art57, AIA-Rec49, AIA-Art58 |
| q023 (en) | AIA-Art5 | 4 | AIA-Rec18, AIA-Art3, AIA-AnnexIII |
| q138 (fr) | AIA-Art91 | 4 | AIA-Art54, AIA-Art92, AIA-Art6 |
| q034 (en) | AIA-AnnexVI | 5 | AIA-Art92, AIA-Art6, AIA-Art43 |
| q038 (fr) | GDPR-Art85 | 5 | GDPR-Rec63, GDPR-Rec153, GDPR-Rec156 |
| q125 (fr) | AIA-Art58 | 6 | AIA-Art57, AIA-Art70, AIA-Rec126 |
| h022 (en) | AIA-Art14 | 6 | AIA-Art60, AIA-Art3, AIA-Art25 |
| h025 (en) | AIA-Art101 | 7 | AIA-Art26, AIA-Art54, AIA-Rec53 |
| q025 (en) | AIA-Art11 | 8 | AIA-AnnexXI, AIA-AnnexIX, AIA-Art27 |
| q129 (en) | AIA-Art66 | 11 | GDPR-Art70, GDPR-Rec166, AIA-Art37 |
| q116 (fr) | GDPR-Art5 | 12 | GDPR-Rec39, GDPR-Rec61, GDPR-Rec50 |
| q118 (fr) | GDPR-Art51 | 13 | AIA-Rec153, GDPR-Rec119, GDPR-Art53 |
| q153 (en) | AIA-Art5 | 14 | AIA-Rec29, AIA-Rec134, AIA-Rec28 |
| q105 (fr) | AIA-Art91 | 17 | AIA-Rec101, AIA-Art53, AIA-Art22 |
| h020 (en) | AIA-Art5 | 21 | AIA-Art3, AIA-AnnexIII, AIA-Rec54 |
| q108 (en) | AIA-Art8 | 26 | AIA-Rec87, AIA-Rec46, AIA-Rec86 |
| q147 (en) | GDPR-Art5 | 29 | GDPR-Rec69, GDPR-Rec156, GDPR-Rec47 |
| q033 (en) | AIA-Art87 | 31 | AIA-Rec172, AIA-Art28, AIA-Art55 |
| h024 (fr) | AIA-Art27 | 34 | AIA-Rec58, AIA-Rec47, AIA-Art82 |
| h023 (en) | GDPR-Art83 | 43 | AIA-Rec146, AIA-Art34, AIA-Art63 |
| q024 (fr) | AIA-Art5 | none | AIA-Rec13, AIA-Rec81, AIA-Rec27 |
| q036 (en) | GDPR-Art48 | none | AIA-Rec141, AIA-Rec10, AIA-Art71 |
| q039 (en) | GDPR-Art89 | none | GDPR-Rec159, GDPR-Rec156, GDPR-Rec91 |
| q112 (en) | GDPR-Art48 | none | GDPR-Rec107, GDPR-Rec114, GDPR-Art3 |
| q115 (en) | GDPR-Art70 | none | GDPR-Rec140, GDPR-Art75, AIA-Rec10 |
| q126 (en) | GDPR-Art92 | none | AIA-Art36, AIA-Art30, AIA-Art46 |
| h021 (fr) | AIA-Art5 | none | AIA-Art9, AIA-Rec96, AIA-Art4 |
