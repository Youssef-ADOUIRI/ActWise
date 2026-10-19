# Retrieval ablations

Each row is one change, measured on the **dev** split (20 scored questions) with `make eval-retrieval SYSTEM=<config>`.
Metrics are at article level; brackets give the 95 % bootstrap interval. With 20 questions, one miss moves Recall@5 by 0.05, so only gaps larger than the intervals count as real.

| Config | Chunking | Retrieval | Rerank | Recall@5 | MRR@10 | nDCG@10 | ms/query | Report |
|---|---|---|---|---|---|---|---|---|
| baseline | fixed 150-word windows | dense (BGE-M3) | no | 0.650 [0.45, 0.85] | 0.504 [0.32, 0.69] | 0.547 | 170 | [baseline-dev](../evals/reports/baseline-dev.md) |
| A | structure-aware | dense | no | | | | | |
| B | structure-aware | BM25 only | no | | | | | |
| C | structure-aware | dense + BM25 (RRF) | no | | | | | |
| D | structure-aware | dense + BM25 (RRF) | cross-encoder | | | | | |

ms/query is measured on a laptop CPU (i5-10300H, 4 cores) and includes embedding the query.

## What the baseline gets wrong (input for step 4)

| Pattern | Questions | Likely fix to test |
|---|---|---|
| A recital outranks the operative article | q006, q007, q010, q012, q019 | Headers in chunks; compare with and without recitals |
| A neighbouring article wins (Art. 13 over 14, 35 over 36, 47 over Annex V) | q002, q009, q011, q013, q014 | Structure-aware chunks: a window can no longer start in one article and end in the next |
| Annex lists rank low (Annex II at 15, Annex V absent) | q001, q002 | Title header on each annex point; BM25 for list terms |
| Cross-law questions find only one law | q019, q020 | Retrieve per law, or split the question in two |

Recall@20 is 0.825 against 0.650 at 5: the gold article is often retrieved but ranked too low, which is the case a reranker addresses.
