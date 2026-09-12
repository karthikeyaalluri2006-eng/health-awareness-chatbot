"""
HealthAware AI - Document Chunking
Splits healthcare texts into overlapping semantic chunks with rich metadata.
"""

from typing import List, Dict, Any


def chunk_text(
    text: str,
    chunk_size: int = 350,
    overlap: int = 50,
    metadata: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """
    Split text into chunks of approximately `chunk_size` words with `overlap` words.
    Returns a list of dictionaries with content, chunk_index, and metadata.
    """
    if not text or not text.strip():
        return []

    words = text.split()
    chunks = []
    metadata = metadata or {}

    start = 0
    chunk_index = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunk_text_str = " ".join(chunk_words).strip()

        if chunk_text_str:
            chunks.append({
                "chunk_index": chunk_index,
                "content": chunk_text_str,
                "metadata": {
                    **metadata,
                    "word_count": len(chunk_words),
                    "chunk_index": chunk_index
                }
            })
            chunk_index += 1

        if end >= len(words):
            break

        start += (chunk_size - overlap)

    return chunks
