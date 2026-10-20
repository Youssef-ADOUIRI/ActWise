# Retrieval ablations

Each row is one change, measured on the **dev** split (20 scored questions) with `make eval-retrieval SYSTEM=<name>`; `make ablations` runs them all.
Metrics are at article level; brackets give the 95 % bootstrap interval. With 20 questions, one miss moves Recall@5 by 0.05, so only gaps larger than the intervals count as real.

| Row | System | Chunking | Retrieval | Rerank | Recall@5 | MRR@10 | nDCG@10 | ms/query | Report |
|---|---|---|---|---|---|---|---|---|---|
| baseline | `baseline` | fixed 150-word windows | dense (BGE-M3) | no | 0.650 [0.45, 0.85] | 0.504 [0.32, 0.69] | 0.547 | 184 | [baseline-dev](../evals/reports/baseline-dev.md) |
| A | `dense` | structure-aware | dense | no | 0.850 [0.70, 0.97] | 0.704 [0.55, 0.85] | 0.737 | 160 | [dense-dev](../evals/reports/dense-dev.md) |
| B | `bm25` | structure-aware | BM25 only | no | 0.875 [0.72, 1.00] | 0.584 [0.44, 0.74] | 0.661 | 6 | [bm25-dev](../evals/reports/bm25-dev.md) |
| C | `hybrid` | structure-aware | dense + BM25 (RRF) | no | 0.900 [0.78, 1.00] | 0.629 [0.49, 0.78] | 0.698 | 174 | [hybrid-dev](../evals/reports/hybrid-dev.md) |
| D | `hybrid-rerank` | structure-aware | dense + BM25 (RRF) | cross-encoder | 0.900 [0.78, 1.00] | 0.760 [0.61, 0.90] | 0.793 | 12,534 | [hybrid-rerank-dev](../evals/reports/hybrid-rerank-dev.md) |
| E | `hybrid-binding` | structure-aware | as C, articles and annexes before recitals | no | **0.925** [0.80, 1.00] | 0.806 [0.69, 0.93] | 0.842 | 149 | [hybrid-binding-dev](../evals/reports/hybrid-binding-dev.md) |
| F | `hybrid-rerank-binding` | structure-aware | as D, articles and annexes before recitals | cross-encoder | **0.925** [0.80, 1.00] | **0.906** [0.79, 1.00] | **0.921** | 11,776 | [hybrid-rerank-binding-dev](../evals/reports/hybrid-rerank-binding-dev.md) |

ms/query is measured on a laptop CPU (i5-10300H, 4 cores) and includes embedding the query. Vector search runs in process (`NumpyStore`); Qdrant gives the same rankings (150 of 150 sampled top-10 lists were identical), plus a local network round trip. D and F run in two passes because the embedder and the reranker (about 2 GB each) don't fit together in this laptop's memory; their ms/query adds both passes.

## What each change did

- **Structure-aware chunks (baseline → A): +0.20 Recall@5**, the largest single gain. A chunk no longer starts in one article and ends in the next, and it carries its header ("AI Act Article 49(3): Registration").
- **BM25 alone (B)** matches dense at Recall@5 and is 25 times faster, but ranks worse (MRR 0.584). Exact terms such as "formal non-compliance" find the article; paraphrases don't rank it first.
- **RRF fusion (C)** has the best recall: every gold article is in the top 20 (Recall@20 = 1.000). But MRR falls below dense alone, because BM25 votes push up recitals that repeat the article's words.
- **The reranker (D)** fixes much of that order (MRR 0.629 → 0.760) at 70 times the latency.
- **Binding text first (E, F):** the biggest failure cause was a recital ranked above the operative article ([failure_cases.md](failure_cases.md)). Listing articles and annexes before recitals, each group in its fused order, costs nothing at query time. It lifts MRR to 0.806 without a reranker and 0.906 with one.

## Choice

**E (`hybrid-binding`) is the default**: Recall@5 0.925 and MRR 0.806 at about 150 ms per query on a CPU. F ranks better (MRR 0.906, Recall@1 0.80) but takes 12 s per query on this CPU, too slow for Cloud Run. See decisions [003](decisions/003-fusion.md) and [004](decisions/004-rerank.md).

The intervals of rows A to F overlap at 20 questions. Step 6 grows the golden set to 150 questions and re-runs this table.

## The baseline's failure patterns, after step 4

| Pattern | Baseline questions | With E |
|---|---|---|
| A recital outranks the operative article | q006, q007, q010, q012, q019 | Fixed: q006, q007 and q012 rank first; q010 and q019 rank 2, behind a neighbouring article |
| A neighbouring article wins | q002, q009, q011, q013, q014 | q011 and q013 rank first; q009 and q014 rank 2 (first with the reranker); q002 is in the next row |
| Annex lists rank low | q001, q002 | q001 ranks 2, behind the article that cites the annex; q002 ranks 9 |
| Cross-law questions find one law | q019, q020 | q019 finds both laws in the top 5; q020 still misses GDPR Art. 80 |
