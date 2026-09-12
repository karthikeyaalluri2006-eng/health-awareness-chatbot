"""
HealthAware AI - Semantic Vector & Keyword Hybrid Retrieval
Fetches relevant knowledge chunks from vector store using hybrid similarity scoring.
"""

import json
import re
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from database.models import DocumentChunk
from rag.embeddings import get_embedding_provider, cosine_similarity


QUERY_STOPWORDS = {
    "about", "are", "can", "does", "for", "give", "how", "is", "me", "of",
    "please", "tell", "the", "this", "to", "what", "when", "which", "who",
    "why", "with", "you", "your",
}

GENERIC_HEALTH_TERMS = {
    "awareness", "condition", "disease", "health", "illness", "medical",
    "medicine", "sign", "signs", "symptom", "symptoms", "treatment", "wellness",
    "fever",
}


def retrieve_relevant_chunks(
    db: Session,
    query: str,
    top_k: int = 4,
    min_score: float = 0.05
) -> List[Dict[str, Any]]:
    """
    Hybrid retrieval: Dense vector cosine similarity + lexical keyword matching.
    """
    if not query or not query.strip():
        return []

    # 1. Embed query
    embedder = get_embedding_provider()
    query_vec = embedder.embed_text(query)

    # 2. Extract query keywords for lexical scoring
    query_tokens = {
        token for token in re.findall(r"\b[a-z0-9]{3,}\b", query.lower())
        if token not in QUERY_STOPWORDS
    }

    # 3. Fetch all indexed chunks
    chunks = db.query(DocumentChunk).all()
    if not chunks:
        return []

    document_text = {}
    for chunk in chunks:
        document_text.setdefault(chunk.document_id, "")
        document_text[chunk.document_id] += " " + chunk.content.lower()

    scored_chunks = []
    for chunk in chunks:
        meta = {}
        if chunk.metadata_json:
            try:
                meta = json.loads(chunk.metadata_json)
            except Exception:
                meta = {}

        # Cosine similarity
        try:
            chunk_vec = json.loads(chunk.embedding_json) if chunk.embedding_json else []
        except Exception:
            chunk_vec = []

        vector_score = cosine_similarity(query_vec, chunk_vec)

        # Keyword overlap score
        chunk_content_lower = chunk.content.lower()
        matched_words = sum(1 for token in query_tokens if token in chunk_content_lower)
        matched_occurrences = sum(
            len(re.findall(rf"\b{re.escape(token)}\b", chunk_content_lower))
            for token in query_tokens
        )
        keyword_score = min(
            matched_occurrences / max(len(query_tokens) * 2, 1),
            1.0
        )

        # Exact distinctive terms are deterministic and outweigh noisy local
        # vector hashing, especially when several conditions share a symptom.
        distinctive_tokens = [
            token for token in query_tokens
            if len(token) >= 4 and token not in GENERIC_HEALTH_TERMS
        ]
        document_content_lower = document_text[chunk.document_id]
        exact_term_score = max(
            (
                1.0
                if re.search(rf"\b{re.escape(token)}\b", document_content_lower)
                else 0.0
            )
            for token in distinctive_tokens
        ) if distinctive_tokens else 0
        title_lower = str(meta.get("title", "")).lower() if chunk.metadata_json else ""
        verified_dataset_score = 0.25 if "verified dataset" in title_lower else 0.0
        title_match_score = max(
            (
                1.0
                if re.search(rf"\b{re.escape(token)}\b", title_lower)
                else 0.0
            )
            for token in distinctive_tokens
        ) if distinctive_tokens else 0
        seasonal_symptom_score = (
            1.0
            if "seasonal illness" in title_lower
            and query_tokens.intersection({"fever", "cold", "flu", "cough"})
            else 0.0
        )
        combined_score = (
            (0.05 * vector_score)
            + (0.15 * keyword_score)
            + (0.35 * exact_term_score)
            + (0.8 * title_match_score)
            + (0.5 * seasonal_symptom_score)
            + verified_dataset_score
        )

        if combined_score >= min_score or matched_words > 0:
            scored_chunks.append({
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "content": chunk.content,
                "score": combined_score,
                "title": meta.get("title", "Health Reference"),
                "category": meta.get("category", "General Health"),
                "source": meta.get("source", "Verified Healthcare Documentation")
            })

    # Sort descending by score
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks[:top_k]
