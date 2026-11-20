"""
Biophysical Distance and Vector Divergence Utilities.
Calculates normalized metric divergence and cosine distance between 1,280-dim ESM-2 vectors.
"""

import math
from typing import List, Dict, Any, Optional

try:
    import numpy as np
    has_numpy = True
except ImportError:
    has_numpy = False


def calculate_cosine_distance(vec_a: Any, vec_b: Any) -> float:
    """
    Computes cosine distance between two 1,280-dimensional vectors:
    distance = 1.0 - (dot(a, b) / (norm(a) * norm(b)))
    Returns a value between 0.0 (identical fold) and 1.0 (maximally divergent).
    """
    if has_numpy and isinstance(vec_a, np.ndarray) and isinstance(vec_b, np.ndarray):
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        if norm_a == 0 or norm_b == 0:
            return 1.0
        similarity = float(np.dot(vec_a, vec_b) / (norm_a * norm_b))
        return max(0.0, min(1.0, 1.0 - similarity))

    # Python float list fallback
    dot = sum(x * y for x, y in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(x * x for x in vec_a))
    norm_b = math.sqrt(sum(y * y for y in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 1.0
    similarity = dot / (norm_a * norm_b)
    return max(0.0, min(1.0, 1.0 - similarity))


def calculate_normalized_divergence(val_cand: float, val_bench: float, normalizer: float) -> float:
    """
    Calculates normalized absolute relative divergence capped between 0.0 and 1.0.
    """
    if normalizer == 0:
        return 0.0
    diff = abs(val_cand - val_bench)
    return min(1.0, diff / normalizer)
