# Frameworks against hand-written code

Step 10 rebuilt two parts of ActWise with a framework and measured each against our own version.

- **Retrieval:** LlamaIndex.
- **The risk classifier:** LangGraph.

**Fair comparison:**
- **Same data:** the same chunks and the dev split.
- **Same model and embedder:** the fine-tuned MiniLM for retrieval, and Gemini Flash-Lite through our own cached LLM chain for the classifier.
- **Same guards:** `Classification` and `accept()`.

Every number comes from a report in `evals/reports/`, from `frameworks/loc.py`, or from the measurements below, all on one laptop CPU (i5-10300H, 4 cores). Decision [013](../docs/decisions/013-frameworks.md) records what we keep.

## Retrieval: LlamaIndex against system H

[`llamaindex_pipeline.py`](llamaindex_pipeline.py) embeds the same 3,799 passages with LlamaIndex's stock `HuggingFaceEmbedding` (`models/minilm-ft`, 256 tokens). It keeps them in a `VectorStoreIndex` and persists it under `.cache/llamaindex`. System H uses our `DenseRetriever`, `EmbeddingCache` and `NumpyStore`.

| | Hand-written (H) | LlamaIndex (K) |
|---|---|---|
| Recall@5 / MRR@10 (dev, 76) | 0.849 / 0.712 | 0.849 / 0.712: the same top 10 articles for 76 of 76 questions |
| Latency per query | **20 ms** | 105 ms (profiled: 16 ms embedding the query, about 80 ms in `SimpleVectorStore`) |
| First build | Vectors from the step 9 cache | 243 s: embeds the corpus |
| Later runs, whole eval | 23 s | 41 s: parses a 36 MB JSON index |
| Lines of code | 131 | **51** |
| Lines you did not have to write | | About 110 of H's: the sharded embedding cache (45), the vector store (26), the embedder wrapper (37) |
| Debuggability | Plain functions and arrays; every step can be printed | See below |
| Dependencies added | None | `llama-index-core`: 23 packages, 60 MB. The HF embeddings package adds 1 more, on the torch side we already had |
| Verdict | **Kept.** 5 times faster per query | Same answers in 40 % of the code, but slower, and 60 MB more in an image capped at 450 MB |

**What we saw when it went wrong:**
- **Metadata is embedded by default.** A node with `metadata={"id": "AIA-Art5-1"}` embeds `"id: AIA-Art5-1\n\n<text>"` unless `excluded_embed_metadata_keys` says otherwise. Nothing warns you: the vectors are just different. A test now checks the embedded text.
- **Where the time goes:** `SimpleVectorStore` rebuilds a numpy array from 3,799 Python lists on every query, then scores each passage with its own call (two norms each). `cProfile` found it, under several layers of LlamaIndex's instrumentation dispatcher. `NumpyStore` does one matrix product.
- **It needs our ids:** the hits carry LlamaIndex node ids, so a small adapter maps them back to our chunk ids and languages (`LlamaIndexRetriever.search`).

## Classifier: LangGraph rule walk against our agent

[`langgraph_classifier.py`](langgraph_classifier.py) is the guide's graph:
- `retrieve_for_rule` reads one rule's articles by id;
- `decide` asks the model "yes, no or unclear?" (`classify_rule.v1`);
- `submit` runs the agent's guards.

It walks Art. 5, then Art. 6 with Annexes I and III, then Art. 50, and stops at the first rule that applies. Our agent (`agent/classifier.py`, decision 008) picks its own reads and searches instead.

| | Hand-written agent | LangGraph rule walk |
|---|---|---|
| Accuracy, clear / ambiguous (dev, 17 + 3) | **17/17**, 3/3 | 16/17, 3/3 |
| Dangerous downgrades / failed runs | 0 / 0 | 0 / 0 |
| Model calls per run | 3.55 | **2.90**, of which 0.75 are retries (see below) |
| Input tokens per run | **8,714** | 11,312: every run reads Art. 5 whole, and many read Art. 6 with both annexes |
| Latency | Model calls dominate both. Cached: median 0.20 s per run (its searches embed with BGE-M3) | Cached: 0.02 s per run. LangGraph's own overhead: **4 ms** per run |
| Lines of code | **97** | 131 |
| Lines you did not have to write | | The 48-line loop. The typed state, the dependencies and three routing functions took more lines than the loop saved |
| Debuggability | One loop; the messages are a list we can print | See below |
| Dependencies added | None | `langgraph`: 16 packages, 12 MB, including `langchain-core` and `langsmith` |
| Verdict | **Kept** | A clear workflow with fewer calls, but it missed s29, and it costs more tokens and more lines |

**The live run doesn't give a latency figure.** It took a median 13.5 s per run, but the offline profile spaces calls to stay inside the free quota.

**What the numbers come from:**
- **s29, the one miss:** a tool that converts CVs into a structured form, without ranking or scoring anyone (gold: minimal risk). On the Art. 6 rule, the model read Annex III(4) and called it high risk, judging that the Art. 6(3) exception didn't apply. The agent could search for the exception and weigh it. The rule walk sees it only as one paragraph among the 39 of Art. 6 and Annexes I and III. That comes from the design, not from LangGraph.
- **15 of the 58 calls were retries.** Gemini often returned `"applies": ["no"]`, a list, for an enum field. The schema check refused it, and the model corrected itself on the next call. The agent's `tier` field is an enum too, and all 20 of its submissions sent a string. Without these retries the graph would need 2.15 calls per run.
- **Reasons in German in 9 of 20 runs,** although every description and rule text is in English or French. This also comes from the prompt and the model, not from LangGraph. Neither problem was tuned away: this table compares the first design of each.

**What we saw when it went wrong:**
- **Errors are plain Python.** An exception raised in a node reaches the caller unchanged. To see why a run took 5 calls, we wrapped the model, as we would without LangGraph. `stream(stream_mode="updates")` would show each node's state change.
- **Typing:** mypy accepted `invoke(..., context=Deps(...))` only after the compiled graph was annotated with all four of its type parameters.
- **LangGraph brings LangSmith:** a graph run is traced without extra code when `LANGSMITH_TRACING=true` (decision 012).

## Verdict

- **Both framework versions gave the same or close answers.** Neither was worth putting in the API.
- **LlamaIndex** saved about 60 % of the retrieval code. Its default store is 5 times slower per query than one numpy product, and the image has no 60 MB to spare. Its value would be its integrations, for example a Qdrant store or other loaders, which ActWise doesn't need.
- **LangGraph** made the rule walk easy to read as a graph, at 4 ms of overhead. The rule walk itself, not the framework, explains the result:
  - fewer model calls than the agent;
  - more tokens;
  - one miss, where the agent had to weigh an exception.

  The graph took more code than our loop. It would earn its place with what a loop doesn't give for free: checkpoints, a human-in-the-loop pause, or many branching steps.
