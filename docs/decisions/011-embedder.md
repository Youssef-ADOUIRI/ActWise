# 011: The cloud embedder: a fine-tuned multilingual MiniLM, int8 ONNX

- **Options:**
  - **The cloud embedder:**
    - BGE-M3, as on the local profile (568M parameters, 2.2 GB, needs torch);
    - `paraphrase-multilingual-MiniLM-L12-v2` (118M parameters, 384 dimensions), fine-tuned on our pairs and served from ONNX without torch, in fp32 or int8.
  - **Training pairs (`pairs.v1`):** one English and one French question for each of 800 train passages, with or without recitals.
  - **Batches:** mixed languages, or one language per batch.
  - **int8 quantization:** `quantize_dynamic` per tensor, or per channel with reduced range.
  - **What the cloud serves:** the int8 model alone (I), or system E's recipe with the int8 model instead of BGE-M3 (J).
- **Measured:**
  - **Pairs:** 1,431 drafted from train articles and annexes. Rules dropped 2 unreadable replies. A sample of 50 was reviewed, and 1 was dropped as too vague (`data/train/pairs_review.csv`). That leaves 1,428 pairs: 799 English, 629 French. `test_no_split_leakage` passes.
  - **Training:** 135 steps in 33 s on a Colab T4, final loss 0.26 (`models/minilm-ft/training.json`).
  - **Commits:** the model and the reports record commit `4e66661`. The step 9 commit messages were rewritten later without changing any file, so it is now `e5f56ae`, with the same tree `8f82719`.
  - **int8 parity:** on 20 corpus passages, the worst cosine to PyTorch is 0.973 per tensor and 0.989 per channel with reduced range. `test_onnx_parity` needs 0.98.
  - **Retrieval:** dev (76 questions) for every choice, then test (84), run once. Recall@5 [95 % interval] / MRR@10:

    | Row | System | Dev | Dev, hand-written (20) | Test | Test, hand-written (20) |
    |---|---|---|---|---|---|
    | G | `minilm`, base | 0.691 [0.58, 0.79] / 0.568 | 0.525 / 0.446 | 0.720 [0.62, 0.81] / 0.579 | 0.675 / 0.480 |
    | H | `minilm-ft`, PyTorch fp32 | 0.849 [0.76, 0.92] / 0.712 | 0.775 / 0.596 | 0.917 [0.85, 0.96] / 0.803 | 0.850 / 0.738 |
    | I | `minilm-ft-int8` | 0.862 [0.78, 0.93] / 0.702 | 0.775 / 0.565 | 0.905 [0.84, 0.96] / 0.817 | 0.850 / 0.730 |
    | J | `hybrid-binding-int8` | **0.961** [0.91, 1.00] / 0.810 | 1.000 / 0.746 | **0.988** [0.97, 1.00] / 0.902 | 0.950 / 0.912 |
    | E | `hybrid-binding`, BGE-M3 | 0.954 [0.91, 0.99] / **0.878** | 0.925 / 0.806 | 0.976 [0.95, 1.00] / **0.924** | 0.900 / 0.900 |

  - **Size:** the fp32 weights are 471 MB and `model.onnx` in int8 is 119 MB.
  - **Speed, one query embedded on a 4-core laptop CPU:**
    - PyTorch fp32: median 21.1 ms, p95 29.1 ms;
    - ONNX int8: median 12.6 ms, p95 33.4 ms;
    - the whole search on dev: 15 ms per query for J, 196 ms for E.
  - **Qdrant Cloud:** `actwise_ft_int8` holds the 3,799 passages. It returns the same top 5 as `NumpyStore` for 20 of 20 dev questions, with and without a `law` filter.
- **Chosen:**
  - **J (`hybrid-binding-int8`) for the cloud profile.** The local profile keeps E with BGE-M3.
  - **int8, per channel with reduced range** (`evals/export_onnx.py`).
  - **Published** as [`Youssef-ADOUIRI/actwise-minilm-l12-ft-int8`](https://huggingface.co/Youssef-ADOUIRI/actwise-minilm-l12-ft-int8), with [its card](../embedder_card.md). `MINILM_HUB` pins commit `8f2058b`, and I, J and `make index-cloud` load the model from there. Its `model.onnx` is the local export, byte for byte.
  - **One language per batch, no recitals.**
- **Why:**
  - **Fine-tuning lifts Recall@5 by 16 points on dev and 20 on test,** far over the guide's +5 bar. The hand-written questions gain as much as the synthetic ones: on test, 0.675 → 0.850 against 0.810 → 0.966. So the gain doesn't come only from questions that look like the training ones.
  - **J matches E's Recall@5 on both splits and needs no torch,** at a thirteenth of E's search time. It ranks less well: MRR 0.810 against 0.878 on dev. The answer step reads 5 paragraphs, so finding the gold article matters more than ranking it first.
  - **int8 is 4 times smaller and 1.7 times faster.** Its Recall@5 differs from fp32 by one question on each split: +1 on dev, −1 on test.
  - **One language per batch:** in a mixed batch, an English question often meets the French version of its own passage, and MNRL would count it as a negative. This was reasoned, not measured.
  - **No recitals:** the gold of the golden set is articles and annexes, and a recital ranked above its article was decision 002's main failure.
- **Revisit if:**
  - **The int8 target:** Recall@5 was to fall by 1 point or less. On test it fell by 1.2 points, one question out of 84. One question is the smallest step 84 questions can show, so the target is below what this test set can measure. Nothing was changed after reading test. A larger test set would settle it.
  - **J's lower MRR shows in the answers** when step 13 measures the cloud profile.
  - **The hard questions:** only 5 on dev and 6 on test. On dev, H, I and J find 2 of the 5, and E finds 3.
  - **Real users' questions** differ from the LLM-written training questions.
