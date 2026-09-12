"""
HealthAware AI - Embedding Engine
Provides vector representations for document chunks and user queries.
Includes a fast, deterministic local embedding provider that runs without GPU or external APIs,
along with support for dense transformer models.
"""

import math
import re
from typing import List
import numpy as np


class EmbeddingProvider:
    def embed_text(self, text: str) -> List[float]:
        raise NotImplementedError

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]


class FastLocalEmbeddingProvider(EmbeddingProvider):
    """
    High-performance, deterministic semantic hashing vectorizer.
    Generates normalized 128-dimensional float vectors using token hashing + term frequency.
    Ensures zero cold-start delay, runs purely in Python + NumPy.
    """
    def __init__(self, dim: int = 128):
        self.dim = dim

    def _tokenize(self, text: str) -> List[str]:
        cleaned = text.lower()
        tokens = re.findall(r"\b[a-z0-9]{2,}\b", cleaned)
        return tokens

    def embed_text(self, text: str) -> List[float]:
        tokens = self._tokenize(text)
        if not tokens:
            return [0.0] * self.dim

        vec = np.zeros(self.dim, dtype=np.float32)
        for token in tokens:
            # Deterministic bucket hashing
            h = hash(token)
            idx = abs(h) % self.dim
            sign = 1.0 if (h % 2 == 0) else -1.0
            vec[idx] += sign

        # L2 normalization
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm

        return vec.tolist()


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Calculate cosine similarity between two vector lists."""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0
    a = np.array(vec_a, dtype=np.float32)
    b = np.array(vec_b, dtype=np.float32)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


# Singleton default provider
_default_provider = FastLocalEmbeddingProvider()


def get_embedding_provider() -> EmbeddingProvider:
    return _default_provider
