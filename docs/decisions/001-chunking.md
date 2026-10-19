# 001: Structure-aware chunking with language-free IDs

- **Options:** fixed 150-word windows; one chunk per article; one chunk per paragraph, recital or annex point.
- **Measured:** the parser finds every official unit (AI Act 180 / 113 / 13, GDPR 173 / 99) in EN and FR. That gives 3,799 chunks, a median of 71 words and a maximum of 150. EN and FR produce identical ID sets.
- **Chosen:** one chunk per paragraph, split into 150-word windows with 25 words of overlap when longer. IDs look like `AIA-Art6-2` and never contain the language. Storage uses `Chunk.key` (`id@lang`).
- **Why:** paragraph-level citations are what a lawyer checks, and shared IDs let FR questions be scored against EN gold labels. Retrieval quality will be compared with fixed windows in Step 4.
- **Revisit if:** the Step 4 ablation shows fixed windows retrieving as well, or answers need more context than a single paragraph.

Edge cases found on the real pages (the guide's parser missed all of them):

| Case | Handling |
|---|---|
| FR preamble ends with `ONT ADOPTÉ`, not `ONT ARRÊTÉ` | Both forms match |
| FR definitions are `1)`, EN definitions are `(1)` | One regex accepts both |
| Footnote marks split over lines `(`, `12`, `)`, `,` | Removed; trailing punctuation kept |
| Signatures, footnote list and page footer after the body | Ignored after `Done at` / `Fait à` / `ELI: http` |
| GDPR uses `Section 1`, the AI Act `SECTION 1` | Both skipped as headings |
| Annex VIII (Sections A–C) and XI (Sections 1–2) restart their numbering | Points become `b.1`, `2.1`; label "Annex VIII, Section B, point 1" |
