# 004: Reranking: cross-encoder offline only, not in serving

- **Options:** no reranker (row E); `BAAI/bge-reranker-v2-m3` on the top 20 fused passages (row F).
- **Measured (dev, 20 questions):**
  - Recall@5 is 0.925 for both.
  - The reranker lifts MRR@10 from 0.806 to 0.906, Recall@1 from 0.60 to 0.80 and nDCG@10 from 0.842 to 0.921.
  - Latency goes from 149 ms to 11,776 ms per query on a 4-core laptop CPU, and the reranker needs another 2 GB of memory.
- **Chosen:** serve E, with no reranker. Keep F as an offline configuration for evaluation runs.
- **Why:**
  - The reranker only reorders passages that are already in the top 20, so Recall@5 does not move. Its gains are the four neighbouring-article cases (q009, q010, q014, q016), where the gold article sits at rank 2. The answer generator still sees it, because it reads the top 5.
  - Twelve seconds per query on a CPU does not fit Cloud Run: requests time out at 60 s, and a classification makes several calls. A second 2 GB model does not fit its free tier either.
- **Revisit if:**
  - A GPU, or a smaller multilingual cross-encoder (an int8 ONNX export or a MiniLM-size model), brings reranking under about 300 ms.
  - Step 6 shows that the order inside the top 5 changes the quality of answers.
