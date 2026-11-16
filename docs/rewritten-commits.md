# Rewritten commits

On 2026-11-12 every branch was rewritten to drop the co-author trailers from its commit messages. No file changed: each new commit has the same tree, author and date as the old one.

Reports, docs and the HF Hub card that name an old commit still mean the same code. This table gives each old hash its new one, newest first.

**Step 9's commit was rewritten twice.** The embedder's reports, `training.json` and the HF Hub card record `4e66661`. It became `e5f56ae` on 2026-11-11, and is now `30e667e`, with the same tree `8f82719`.

| Old | New | Commit |
|---|---|---|
| `a82e293` | `389321c` | Step 10: /simplify: leaner LangGraph state, to_hit in LlamaIndex, CountingLLM, one classifier registry |
| `207f9ae` | `ffdaeba` | Step 10: LlamaIndex retrieval and a LangGraph classifier, measured against our own |
| `7f12f3d` | `d2182e9` | Tracing plan: LangSmith instead of Langfuse (decision 012) |
| `ded5fe3` | `7c15ea8` | Step 9: note the rewritten commit hash (4e66661 is now e5f56ae, same tree) |
| `d63dba7` | `393799e` | Step 9: /simplify: shared provenance helpers, temporary fp32 export, saved tokenizer padding |
| `387ba50` | `675021d` | Step 9: publish the int8 embedder on the Hub and pin it |
| `ea6c19d` | `91a56b3` | Step 9: decision 011, ablations, embedder card, Hub publish script |
| `3841121` | `ae6a208` | Step 9: payload indexes for Qdrant Cloud filters; dev and test reports |
| `e5f56ae` | `30e667e` | Step 9: 1,428 training pairs, reviewed sample, pair tests, base MiniLM dev row |
| `5b6495c` | `a0480f2` | Step 9: MiniLM systems, ONNX embedder, training notebook, cloud index |
| `b144a1e` | `f6da33d` | Step 9: training pairs from train paragraphs (make pairs) |
| `6630acf` | `cc6409b` | Step 8b: /ask answers with answer.v3 (judged: dev faithfulness 0.982) |
| `15eebb0` | `7d74c57` | Step 8b: /simplify: a clearer RagPipeline docstring |
| `fc4da6c` | `c6fce50` | Step 8b: decision 010, generation.md rows, failure cases, CHANGELOG, TODO |
| `24ef891` | `ddb2547` | Step 8b: /ask reads whole paragraphs, follows references, retries refusals |
| `8f5b28a` | `a120bcb` | Step 8b: answer.v3 drops the legal-advice line the model copied |
| `ccd863c` | `4a7c67c` | Step 8b: hard verdicts complete (16 of 18 right after phase 3, none lost) |
| `85eef74` | `470fa02` | Step 8b phase 3: the retry searches the rewritten queries alone (A answered) |
| `5e21d7c` | `ccda184` | Step 8b phase 3: dev judged (faithfulness 0.975 on the regular questions) |
| `30de6c3` | `9675f7f` | Step 8b phase 3: always-on and on-refusal reports, changed hard answers to mark |
| `80a1ba8` | `5523139` | Step 8b phase 3: rewrite only on refusal; ids in the wrong case are corrected |
| `5a61caa` | `c80da51` | Step 8b phase 2: dev and train answers (judge to follow), changed hard answers to mark |
| `fd923be` | `dc86432` | Step 8b phase 3: rewritten queries and each article's first paragraph |
| `27502f2` | `b081e91` | Step 8b phase 2: follow the annexes and paragraphs a chosen paragraph names |
| `5cbbf05` | `727759e` | Step 8b phase 1: dev and train reports, changed hard answers to mark |
| `9f4b0c7` | `0cca15f` | Step 8b phase 1: whole paragraphs as the answer context |
| `9042eb7` | `cdbf982` | Step 8b: baseline verdicts (11 of 18 right; the 7 wrong are refusals) |
| `609b28d` | `461a1a1` | Step 8b: baseline on dev and train, verdict sheet for the hard answers |
| `e1e2a37` | `4638593` | Step 8b: 24 reviewed hard questions in the golden set |
| `0c1b0c1` | `d471628` | Step 8b: hard questions to review, gold-in-context metrics |
| `1e8f437` | `23a1d56` | Merge pull request #41 from Youssef-ADOUIRI/step-8-api |
| `51f1429` | `00ecb19` | Step 8: /simplify pass on the API |
| `ac4b420` | `0e200e5` | Step 8: the API, its guards and the Streamlit UI |
| `93c6617` | `a84ecde` | Merge pull request #40 from Youssef-ADOUIRI/step-7-classifier |
| `abbecc8` | `dd5c044` | Step 7: classifier report, decision 008, model card |
| `f3670f9` | `3cbc44f` | Step 7: /simplify pass on the classifier |
| `9d25061` | `8668c1f` | Step 7: all 40 scenario labels verified by a person (none changed) |
| `af88997` | `31c5c5c` | Merge pull request #39 from Youssef-ADOUIRI/step-6b-golden-150 |
| `c8f61bc` | `83658d6` | Step 7: warn three steps before the budget, so a refused submission can be fixed |
| `557e704` | `0567a78` | Step 7: Gemini thought signatures, an article reader, a budget warning |
| `3fafa73` | `186637d` | Step 7: risk classifier agent, scenarios and eval |
| `293c340` | `6a05f13` | Step 6b: plain baseline on the grown dev set |
| `569690d` | `09b110c` | Merge pull request #38 from Youssef-ADOUIRI/step-6b-golden-150 |
| `8b74af4` | `45b2a07` | Merge pull request #37 from Youssef-ADOUIRI/step-6a-cited-answers |
| `8dc2a89` | `9461d5e` | Step 6b: final answer table, decision 007, M3 done |
| `c07703c` | `d4966ad` | Step 6b: report the fully-supported rate next to faithfulness |
| `698a084` | `56128f6` | Step 6b: labels re-checked at the 3/4 boundary; judge kappa 0.739 |
| `afd9cb8` | `7616ca3` | Step 6b: ablation table on 71 dev questions, hand-written vs synthetic |
| `1fc7850` | `5e1e0a8` | Step 6b: ablations and the v1/v2 answer A/B on the grown dev set |
| `c2288b1` | `0d90d1b` | Step 6b: golden set grown to 179 questions; hand vs synthetic breakdowns |
| `86bbbac` | `266d883` | Step 6b: human labels for judge calibration (58 answers, scored blind) |
| `0f3f0bf` | `26a19ee` | Step 6a: answer reports, review files and docs |
| `9d5aefa` | `038a83e` | Step 6a: cited answers, guardrails, LLM judge and answer metrics |
| `c14f0c6` | `42852c5` | Merge pull request #36 from Youssef-ADOUIRI/step-5-provider-layer |
| `0ad6a0f` | `3f5e6a4` | Step 5: provider check, baseline answers and docs |
| `d511957` | `f8ff561` | Step 5: LLM provider layer (adapters, cache, retries, fallback) |
| `7e14f19` | `b8c3397` | Merge pull request #35 from Youssef-ADOUIRI/step-4-hybrid-rerank |
| `fa015c0` | `2c96c79` | Step 4: ablation reports, error analysis and decisions (Recall@5 0.925 on dev) |
| `8e5e84b` | `b85d850` | Step 4: hybrid retrieval (dense + BM25, RRF), reranker and Qdrant store |
| `ce032f3` | `d6ce137` | Merge pull request #34 from Youssef-ADOUIRI/step-3-cleanup |
| `f165c34` | `1fc68b4` | Clean up the step 3 code: one home per rule, no unused options |
| `497f004` | `c2564c2` | Docstrings on every function; ruff now requires them |
| `3309c59` | `3573169` | Merge pull request #33 from Youssef-ADOUIRI/step-3-baseline-eval |
| `43d436c` | `bfc7fbb` | Eval script: log our progress only, not every HTTP request |
| `488755d` | `5b375e8` | Step 3: baseline report, ablation table and docs |
| `d10a575` | `7fb0cf6` | Pin the BGE-M3 commit whose weights are actually loaded |
| `47fb935` | `bed4464` | Pin the BGE-M3 revision used by the retrieval eval |
| `9968464` | `26caef0` | Step 3: evaluation harness, golden set and naive baseline |
| `b36bff7` | `4bf731e` | Add project review and pipeline decks |
| `ef902ac` | `51bb631` | Merge pull request #31 from Youssef-ADOUIRI/step-2-parse-chunk |
| `1020f4f` | `962f3cb` | Step 2: parse and chunk the AI Act and GDPR with stable IDs |
| `80510d0` | `caf1cc6` | Changelog: note ruff-check hook id |
| `44b0dbd` | `bf98dd1` | Use ruff-check hook id (ruff is a legacy alias) |
| `e024915` | `cfea879` | Add uv.lock |
| `ed39b8f` | `47670e7` | Add changelog recapping steps 0 and 1 |
| `2bbf9fb` | `d461e50` | Update TODO for steps 0 and 1 |
| `2fc1cb9` | `898ab68` | Step 1: EUR-Lex sources and html_to_text |
| `b5f8634` | `d3fb911` | Step 0: project skeleton, tooling and CI |
| `e5ce255` | `d329a2f` | Merge remote-tracking branch 'origin/main' |
| `a04402d` | `ab362b9` | Delete LICENSE |
| `e37087c` | `d5667ee` | Initial commit |
