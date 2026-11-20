"""
Unit tests for core biophysical feature extraction and scoring.
"""

import pytest
from core.biophysics.features import extract_protein_features, clean_sequence
from core.biophysics.distance import calculate_cosine_distance, calculate_normalized_divergence
from core.biophysics.scoring import score_protein_pair


def test_core_clean_sequence():
    raw_seq = "ACDEFGHIKLMNPQRSTVWYXBZ"
    cleaned = clean_sequence(raw_seq)
    assert "X" not in cleaned
    assert "B" not in cleaned
    assert "Z" not in cleaned
    assert len(cleaned) == 20


def test_core_extract_protein_features():
    seq = "ACDEFGHIKL"
    features = extract_protein_features(seq)

    assert "molecular_weight" in features
    assert "isoelectric_point" in features
    assert "cysteine_fraction" in features
    assert "gravy" in features
    assert "charge_at_ph7" in features

    assert features["cysteine_fraction"] == pytest.approx(0.1, rel=1e-2)
    assert features["length"] == 10.0


def test_core_distance_identical():
    val = calculate_normalized_divergence(50000.0, 50000.0, 50000.0)
    assert val == 0.0

    vec = [1.0, 0.0, 0.0]
    cos_dist = calculate_cosine_distance(vec, vec)
    assert cos_dist == pytest.approx(0.0, abs=1e-5)


def test_core_score_protein_pair():
    feat = {
        "molecular_weight": 50000.0,
        "isoelectric_point": 5.5,
        "cysteine_fraction": 0.02,
        "gravy": -0.4,
        "charge_at_ph7": -10.0,
    }
    vec = [0.5] * 1280
    score, contributions, confidence = score_protein_pair(
        candidate_features=feat,
        benchmark_features=feat,
        job="meat",
        cand_embedding=vec,
        bench_embedding=vec
    )
    assert score == pytest.approx(100.0, abs=0.1)
    assert confidence == "High"
    assert "esm" in contributions
