"""
Unit and Integration Tests for RAG Chunking, Embeddings, Ingestion, and Retrieval
"""

import pytest
from rag.chunking import chunk_text
from rag.embeddings import FastLocalEmbeddingProvider, cosine_similarity
from rag.retrieval import retrieve_relevant_chunks
from database.connection import get_db_session, init_db


@pytest.fixture(autouse=True)
def setup_db():
    init_db()


def test_text_chunking():
    sample_text = " ".join([f"word{i}" for i in range(500)])
    chunks = chunk_text(sample_text, chunk_size=200, overlap=50)
    assert len(chunks) >= 3
    assert "chunk_index" in chunks[0]
    assert "content" in chunks[0]


def test_embedding_vector_generation():
    embedder = FastLocalEmbeddingProvider(dim=128)
    vec1 = embedder.embed_text("Blood pressure measures arterial hydrostatic force.")
    vec2 = embedder.embed_text("Hypertension and high blood pressure in arteries.")
    vec3 = embedder.embed_text("Baking chocolate cookies with vanilla sugar.")

    assert len(vec1) == 128
    sim_related = cosine_similarity(vec1, vec2)
    sim_unrelated = cosine_similarity(vec1, vec3)
    assert sim_related > sim_unrelated


def test_knowledge_retrieval():
    with get_db_session() as db:
        # Query indexed diabetes knowledge
        chunks = retrieve_relevant_chunks(db, query="What are symptoms of diabetes?", top_k=3)
        assert len(chunks) > 0
        assert "content" in chunks[0]
        assert "score" in chunks[0]


def test_retrieval_prioritizes_exact_health_topic():
    with get_db_session() as db:
        chunks = retrieve_relevant_chunks(db, query="What are symptoms about dengue?", top_k=1)

        assert len(chunks) == 1
        assert "dengue" in chunks[0]["content"].lower()
