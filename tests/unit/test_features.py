"""
Unit tests for biophysical feature extraction.
"""

import pytest
from pipeline.features import extract_protein_features, clean_sequence


def test_clean_sequence():
    raw_seq = "ACDEFGHIKLMNPQRSTVWYXBZ"
    cleaned = clean_sequence(raw_seq)
    assert "X" not in cleaned
    assert "B" not in cleaned
    assert "Z" not in cleaned
    assert len(cleaned) == 20


def test_extract_protein_features_standard():
    # Test on a synthetic 10-amino-acid peptide with 1 cysteine
    seq = "ACDEFGHIKL"
    features = extract_protein_features(seq)

    assert "molecular_weight" in features
    assert "isoelectric_point" in features
    assert "cysteine_fraction" in features
    assert "gravy" in features
    assert "charge_at_ph7" in features

    assert features["cysteine_fraction"] == pytest.approx(0.1, rel=1e-2)
    assert features["length"] == 10.0
