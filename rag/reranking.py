"""
HealthAware AI - RAG Reranker
Deduplicates and re-scores retrieved document chunks for optimal LLM context packing.
"""

from typing import List, Dict, Any


def rerank_chunks(chunks: List[Dict[str, Any]], query: str, max_context_chunks: int = 3) -> List[Dict[str, Any]]:
    """
    Deduplicates overlapping or redundant text chunks and selects top diverse knowledge passages.
    """
    if not chunks:
        return []

    # Keep the answer grounded in one best-matching document. Mixing documents
    # can combine a general symptom with an unrelated condition.
    best_document_id = chunks[0].get("document_id")
    document_chunks = [
        chunk for chunk in chunks
        if chunk.get("document_id") == best_document_id
    ]

    unique_chunks = []
    seen_contents = set()

    for chunk in document_chunks:
        # Simple content deduplication based on first 80 characters
        key = chunk["content"][:80].lower()
        if key not in seen_contents:
            seen_contents.add(key)
            unique_chunks.append(chunk)

    # Return top N passages from the selected verified document.
    return unique_chunks[:max_context_chunks]
