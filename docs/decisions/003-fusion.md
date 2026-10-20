# 003: Fusion: dense + BM25 with RRF, binding text first

- **Options:** dense only (row A); BM25 only (B); a weighted sum of normalised scores; reciprocal rank fusion (C); RRF with articles and annexes ranked before recitals (E).
- **Measured (dev, 20 questions):**
  - Recall@5: A 0.850, B 0.875, C 0.900, E 0.925.
  - MRR@10: A 0.704, B 0.584, C 0.629, E 0.806.
  - Latency: about 150–175 ms per query for every row with dense retrieval, 6 ms for BM25 alone.
  - With RRF, every gold article is in the top 20.
  - The weighted sum was not measured: it needs a weight tuned on these same 20 questions.
- **Chosen:** RRF with k = 60 and 30 hits from each retriever. Then articles and annexes go before recitals, each group keeping its fused order. Recitals stay in the list, after the binding text.
- **Why:**
  - RRF needs no score normalisation and no weight. BM25 brings exact legal terms, dense brings paraphrases, and their union finds every gold article.
  - Fusion alone ranked a recital above the article in 9 of 12 failures, because recitals restate an article in plain words. Recitals explain the law but do not bind, so the assistant should cite the article first.
  - The rule costs nothing at query time and needs no tuning.
- **Revisit if:** the 150-question set of step 6 orders the rows differently, or brings questions that only a recital answers. The fine-tuned embedder of step 9 may also make dense retrieval alone good enough.
