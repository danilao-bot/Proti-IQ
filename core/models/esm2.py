"""
Meta ESM-2 Embedding Model Interface.
Loads 1,280-dimensional precalculated embeddings from model_artifacts/embeddings/
or provides zero-shot similarity lookups.
"""

import os
from typing import Optional, Dict, Any

try:
    import numpy as np
    has_numpy = True
except ImportError:
    has_numpy = False

EMBEDDINGS_DIR = os.path.abspath("model_artifacts/embeddings")


def load_embedding(accession: str) -> Optional[Any]:
    """
    Loads precomputed 1,280-dim ESM-2 embedding vector from disk (.npy file).
    Returns numpy array if available, or None if not indexed.
    """
    if not has_numpy:
        return None

    path = os.path.join(EMBEDDINGS_DIR, f"{accession.strip().upper()}.npy")
    if os.path.exists(path):
        try:
            return np.load(path)
        except Exception:
            return None
    return None


def embedding_exists(accession: str) -> bool:
    """Checks if precomputed embedding vector exists on disk."""
    path = os.path.join(EMBEDDINGS_DIR, f"{accession.strip().upper()}.npy")
    return os.path.exists(path)
