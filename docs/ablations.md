# Retrieval ablations

Each row is one change, measured on the **dev** split with `make eval-retrieval SYSTEM=<name>`; `make ablations` runs them all. Since step 6b, dev has **71 scored questions**: the 20 hand-written ones of step 4 and 51 reviewed synthetic ones (decision 002).
Metrics are at article level, and brackets give the 95 % bootstrap interval. The hand-written columns reproduce step 4 exactly. Each synthetic question is written from a single passage, so it is easier, and the two sets are reported apart.

| Row | System | Retrieval | Rerank | Recall@5 (71) | MRR@10 (71) | nDCG@10 | Hand-written (20): R@5 / MRR | Synthetic (51): R@5 / MRR | ms/query |
|---|---|---|---|---|---|---|---|---|---|
| baseline | `baseline` | 150-word windows, dense (BGE-M3) | no | 0.775 [0.68, 0.87] | 0.484 [0.40, 0.56] | 0.574 | 0.650 / 0.504 | 0.824 / 0.476 | 145 |
| A | `dense` | structure-aware chunks, dense | no | 0.944 [0.89, 0.99] | 0.873 [0.81, 0.93] | 0.893 | 0.850 / 0.704 | 0.980 / 0.940 | 143 |
| B | `bm25` | chunks, BM25 only | no | 0.922 [0.86, 0.98] | 0.770 [0.69, 0.84] | 0.814 | 0.875 / 0.584 | 0.941 / 0.843 | 7 |
| C | `hybrid` | dense + BM25 (RRF) | no | 0.972 [0.94, 1.00] | 0.822 [0.75, 0.88] | 0.860 | 0.900 / 0.629 | 1.000 / 0.898 | 158 |
| D | `hybrid-rerank` | as C | cross-encoder | 0.972 [0.94, 1.00] | 0.904 [0.85, 0.95] | 0.921 | 0.900 / 0.760 | 1.000 / 0.961 | 12,638 |
| E | `hybrid-binding` | as C, articles and annexes before recitals | no | **0.979** [0.94, 1.00] | 0.904 [0.85, 0.95] | 0.925 | **0.925** / 0.806 | 1.000 / 0.943 | 161 |
| F | `hybrid-rerank-binding` | as D, articles and annexes before recitals | cross-encoder | **0.979** [0.94, 1.00] | **0.966** [0.93, 0.99] | **0.973** | **0.925** / **0.906** | 1.000 / **0.990** | 11,894 |

Every report comes from commit `c2288b1`. ms/query is measured on a laptop CPU (i5-10300H, 4 cores) and includes embedding the query. Vector search runs in process (`NumpyStore`). Qdrant gives the same rankings (150 of 150 sampled top-10 lists were identical), plus a local network round trip. D and F run in two passes, because the embedder and the reranker (about 2 GB each) don't fit together in this laptop's memory, so their ms/query adds both passes.

**What the 71 questions add:** the order of the rows is the same as on 20 questions, and the intervals are now about half as wide. On the synthetic questions, every structure-aware system finds the gold article in the top 5. The remaining misses are hand-written questions: cross-law ones, and annex lists cited by an article (below).

## What each change did (step 4, 20 hand-written questions)

- **Structure-aware chunks (baseline → A): +0.20 Recall@5**, the largest single gain. A chunk no longer starts in one article and ends in the next, and it carries its header ("AI Act Article 49(3): Registration").
- **BM25 alone (B)** matches dense at Recall@5 and is 25 times faster, but ranks worse (MRR 0.584). Exact terms such as "formal non-compliance" find the article; paraphrases don't rank it first.
- **RRF fusion (C)** has the best recall: every gold article is in the top 20 (Recall@20 = 1.000). But MRR falls below dense alone, because BM25 votes push up recitals that repeat the article's words.
- **The reranker (D)** fixes much of that order (MRR 0.629 → 0.760) at 70 times the latency.
- **Binding text first (E, F):** the biggest failure cause was a recital ranked above the operative article ([failure_cases.md](failure_cases.md)). Listing articles and annexes before recitals, each group in its fused order, costs nothing at query time. It lifts MRR to 0.806 without a reranker and 0.906 with one.

## Choice

**E (`hybrid-binding`) is the default**: Recall@5 0.925 and MRR 0.806 at about 150 ms per query on a CPU. F ranks better (MRR 0.906, Recall@1 0.80) but takes 12 s per query on this CPU, too slow for Cloud Run. See decisions [003](decisions/003-fusion.md) and [004](decisions/004-rerank.md).

On the 71 questions of step 6b the choice stands: E keeps the best Recall@5 of the fast rows (0.979), and F still ranks best (MRR 0.966) at 12 s per query.

## The baseline's failure patterns, after step 4

| Pattern | Baseline questions | With E |
|---|---|---|
| A recital outranks the operative article | q006, q007, q010, q012, q019 | Fixed: q006, q007 and q012 rank first; q010 and q019 rank 2, behind a neighbouring article |
| A neighbouring article wins | q002, q009, q011, q013, q014 | q011 and q013 rank first; q009 and q014 rank 2 (first with the reranker); q002 is in the next row |
| Annex lists rank low | q001, q002 | q001 ranks 2, behind the article that cites the annex; q002 ranks 9 |
| Cross-law questions find one law | q019, q020 | q019 finds both laws in the top 5; q020 still misses GDPR Art. 80 |
