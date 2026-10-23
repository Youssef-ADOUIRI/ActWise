from actwise.retrieval.embedders import BGE_M3, SentenceTransformerEmbedder
from actwise.retrieval.rerank import BGE_RERANKER, CrossEncoderReranker


def test_models_load_only_when_used():
    """Building the embedder and reranker reads no weights; their config names the pinned commit."""
    embedder = SentenceTransformerEmbedder(*BGE_M3)
    reranker = CrossEncoderReranker(*BGE_RERANKER)

    assert embedder._model is None and reranker._model is None
    assert embedder.config["revision"] == BGE_M3[1]
    assert (reranker.config["model"], reranker.config["revision"]) == BGE_RERANKER
