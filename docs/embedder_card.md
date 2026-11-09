---
license: apache-2.0
language:
  - en
  - fr
base_model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
pipeline_tag: sentence-similarity
tags:
  - onnx
  - int8
  - retrieval
  - legal
  - eu-ai-act
  - gdpr
---

# ActWise MiniLM-L12, fine-tuned, int8 ONNX

A multilingual sentence embedder for searching the **EU AI Act** (Regulation (EU) 2024/1689) and the **GDPR** in English and French. It was fine-tuned from [`paraphrase-multilingual-MiniLM-L12-v2`](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) on questions about the two laws, then exported to ONNX and quantized to int8. It runs with `onnxruntime` and `tokenizers` only, without PyTorch.

It is the cloud retriever of [ActWise](https://github.com/Youssef-ADOUIRI/ActWise), a citation-grounded assistant for the two laws. Decision [011](https://github.com/Youssef-ADOUIRI/ActWise/blob/main/docs/decisions/011-embedder.md) gives the full story.

- **Output:** 384 dimensions, mean-pooled over the tokens and L2-normalised, so a dot product is a cosine.
- **Input:** up to 256 tokens; longer texts are truncated. No query or passage prefix.
- **Files:** `model.onnx` (119 MB, int8 weights), `tokenizer.json` and `tokenizer_config.json`.

## Usage

```python
import numpy as np
import onnxruntime as ort
from huggingface_hub import snapshot_download
from tokenizers import Tokenizer

path = snapshot_download("Youssef-ADOUIRI/actwise-minilm-l12-ft-int8")
tokenizer = Tokenizer.from_file(f"{path}/tokenizer.json")
tokenizer.enable_truncation(max_length=256)
tokenizer.enable_padding(pad_id=1, pad_token="<pad>")  # XLM-R pads with id 1
session = ort.InferenceSession(f"{path}/model.onnx", providers=["CPUExecutionProvider"])


def embed(texts: list[str]) -> np.ndarray:
    encodings = tokenizer.encode_batch(texts)
    ids = np.array([e.ids for e in encodings], dtype=np.int64)
    mask = np.array([e.attention_mask for e in encodings], dtype=np.int64)
    hidden = session.run(None, {"input_ids": ids, "attention_mask": mask})[0]
    vectors = (hidden * mask[..., None]).sum(axis=1) / mask.sum(axis=1, keepdims=True)
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


scores = embed(["Can a non-EU company be fined?"]) @ embed(passages).T
```

ActWise embeds each passage with its header, for example "GDPR Article 83(5): General conditions for imposing administrative fines …", and searches article and annex paragraphs.

## Training data

- **Corpus:** the 2024 texts of the AI Act and the GDPR from EUR-Lex, in English and French, cut into paragraphs. The text may be reused under Commission Decision 2011/833/EU.
- **Split by article, before anything else:** 404 train, 87 dev and 87 test articles and annexes (seed 42). A paragraph and its French version always share a split. The training pairs come from **train articles only**; a test checks that no dev or test article is in them.
- **Pairs:**
  - 800 passages of at least 25 words from train articles and annexes (recitals left out). A passage is a paragraph, or a window of a long one.
  - For each passage, `gemini-3.5-flash-lite` wrote one question in English and one in French whose answer is in the passage. The prompt asks it not to copy long phrases and not to name an article number.
  - Each question is paired with the passage **in its own language**. Windows give English pairs only, because the French windows don't line up with the English ones.
  - Rules dropped 2 unreadable replies. A sample of 50 pairs was reviewed: 49 kept, 1 dropped as too vague.
  - **1,428 pairs:** 799 English, 629 French.

## Training

| Setting | Value |
|---|---|
| Loss | MultipleNegativesRankingLoss (in-batch negatives) |
| Batches | 32 pairs, one language per batch, no duplicate passage in a batch |
| Epochs, learning rate, warmup | 3, 2e-5, 10 % |
| Max length | 256 tokens |
| Precision, hardware | fp16 on a Tesla T4: 135 steps in 33 s |
| Seed | 42 |
| Libraries | sentence-transformers 6.1.0, transformers 5.18.0, torch 2.14.1 |

**One language per batch:** with mixed batches, an English question would often meet the French version of its own passage as a negative, which teaches the model to pull the two languages apart.

**Export:** `torch.onnx.export` (opset 18), then `onnxruntime` dynamic quantization to int8 (QInt8 weights, per channel, reduced range). On 20 corpus passages, the cosine between the int8 and PyTorch embeddings is 0.989 at worst and 0.992 on average.

## Evaluation

Measured with ActWise's own harness on its golden set. A question scores a hit when a passage of its gold article is among the top 5. Brackets give the 95 % bootstrap interval. Each choice was made on dev, and the **test split was run once**.

- **Hand-written:** questions written by the author.
- **Synthetic:** LLM-written and reviewed; each comes from a single passage, which makes them easier.
- **Hard:** everyday words, two-article answers or exceptions.

**Test (84 questions on 87 unseen articles), dense search alone:**

| Model | Recall@5 | MRR@10 | nDCG@10 | Hand-written R@5 (20) | Synthetic R@5 (58) | Hard R@5 (6) |
|---|---|---|---|---|---|---|
| Base MiniLM-L12 | 0.720 [0.62, 0.81] | 0.579 [0.49, 0.67] | 0.620 | 0.675 | 0.810 | 0.000 |
| Fine-tuned, PyTorch fp32 | 0.917 [0.85, 0.96] | 0.803 [0.73, 0.87] | 0.834 | 0.850 | 0.966 | 0.667 |
| **Fine-tuned, int8 (this model)** | **0.905** [0.84, 0.96] | **0.817** [0.74, 0.88] | **0.848** | **0.850** | **0.966** | **0.500** |

**Dev (76 questions):** Recall@5 goes from 0.691 (base) to 0.849 (fine-tuned) and 0.862 (int8). On hand-written questions it goes from 0.525 to 0.775 and 0.775.

**What int8 costs:**
- **Size:** 471 MB of fp32 weights become 119 MB.
- **Speed:** a single query takes a median 12.6 ms instead of 21.1 ms (PyTorch), on a 4-core laptop CPU (i5-10300H).
- **Quality:** int8 loses one test question in the top 5 (Recall@5 −1.2 points) and gains one on dev (+1.3). MRR and nDCG rise on test.

**In ActWise's hybrid search** (with BM25, and articles ranked before recitals), test Recall@5 is 0.988 and MRR 0.902. The same search with BGE-M3 (568M parameters) scores 0.976 and 0.924, and takes about 13 times as long per query on this CPU (15 against 196 ms).

## Limits

- **Two laws, two languages.** It was tuned on the AI Act and the GDPR in English and French. It is not a general legal embedder, and amendments after 2024 (such as the 2026 AI Omnibus) are not in its data.
- **The training questions are written by an LLM,** so they are cleaner than real users' questions. The synthetic evaluation questions come from a similar process and flatter the model. The hand-written and hard columns are the fairer guide, and they are small (20 and 6 questions per split).
- **Small test set.** One question moves Recall@5 by 1.2 points, and the intervals are about ±6 points.
- **On its own it ranks less well than BGE-M3.** ActWise pairs it with BM25.
- **256 tokens.** Longer paragraphs must be cut into windows.
- **Retrieval, not advice.** It finds passages and does not judge compliance.
