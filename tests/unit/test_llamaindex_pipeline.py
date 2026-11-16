import pytest

pytest.importorskip("llama_index.core")

from llama_index.core.embeddings import BaseEmbedding  # noqa: E402

from frameworks.llamaindex_pipeline import build  # noqa: E402
from tests.unit.toys import PASSAGES, CountingEmbedder  # noqa: E402


class ToyEmbedding(BaseEmbedding):
    """CountingEmbedder behind LlamaIndex's interface; records every passage text it embeds."""

    model_name: str = "toy"
    texts: list[str] = []

    def _get_text_embedding(self, text):
        """One passage vector."""
        self.texts.append(text)
        return CountingEmbedder().encode([text])[0].tolist()

    def _get_query_embedding(self, query):
        """One query vector, from the same bag of words."""
        return CountingEmbedder().encode([query])[0].tolist()

    async def _aget_query_embedding(self, query):
        """The async twin LlamaIndex requires."""
        return self._get_query_embedding(query)


def test_search_returns_chunk_ids_best_first(tmp_path):
    """Hits carry the language-free chunk id and the language, best first, `top_k` long."""
    retriever = build(PASSAGES, ToyEmbedding(), cache_dir=tmp_path)

    [best] = retriever.search("erasure", 1)
    both = retriever.search("ban", 2)

    assert (best.id, best.lang) == ("GDPR-Art17-1", "en")
    assert best.text == PASSAGES[0].text
    assert {(hit.id, hit.lang) for hit in both} == {("AIA-Art5-1", "en"), ("AIA-Art5-1", "fr")}
    assert both[0].score >= both[1].score


def test_only_the_passage_text_is_embedded(tmp_path):
    """LlamaIndex prepends metadata to the embedded text unless told not to."""
    embedder = ToyEmbedding()

    build(PASSAGES, embedder, cache_dir=tmp_path)

    assert sorted(embedder.texts) == sorted(p.text for p in PASSAGES)


def test_a_second_build_loads_the_saved_index(tmp_path):
    """The index is persisted once per embedder and corpus; loading embeds no passage."""
    build(PASSAGES, ToyEmbedding(), cache_dir=tmp_path)
    again = ToyEmbedding()

    retriever = build(PASSAGES, again, cache_dir=tmp_path)

    assert again.texts == []
    assert retriever.search("fine", 1)[0].id == "GDPR-Art83-5"
    assert build(PASSAGES[:2], ToyEmbedding(), cache_dir=tmp_path).config != retriever.config
