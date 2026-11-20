"""
Proti IQ Multi-Attribute Biophysical Scoring Engine.
Calculates calibrated match percentages across all 7 alternative-protein target applications.
"""

from typing import Dict, Any, Tuple
from core.biophysics.distance import calculate_cosine_distance, calculate_normalized_divergence


# Canonical parameter normalizers for seed storage globulins
NORMALIZERS = {
    "mw": 50000.0,       # 50 kDa range
    "pi": 5.0,           # pH scale divergence
    "charge": 30.0,      # net surface charge variance
    "gravy": 1.5,        # hydropathicity scale
    "cysteine": 0.05     # 5% cysteine range
}

# Dynamic weighting profiles by target job application
JOB_WEIGHT_PROFILES = {
    "meat": {
        "weights": {"esm": 0.40, "cysteine": 0.25, "mw": 0.15, "gravy": 0.10, "charge": 0.10},
        "description": "High weight on 11S legumin fold and cysteine disulfide dyads for fibrous shear texturization."
    },
    "egg": {
        "weights": {"esm": 0.45, "mw": 0.20, "gravy": 0.15, "pi": 0.10, "charge": 0.10},
        "description": "7S Vicilin trimer thermal gelation and rapid unfold onset."
    },
    "milk": {
        "weights": {"esm": 0.40, "charge": 0.30, "pi": 0.15, "gravy": 0.15},
        "description": "High net-negative surface charge and neutral solubility for colloidal suspension."
    },
    "gel": {
        "weights": {"esm": 0.40, "charge": 0.20, "mw": 0.20, "cysteine": 0.20},
        "description": "Divalent calcium bridging across unfolded acidic subunits for firm Awara curd."
    },
    "mayo": {
        "weights": {"esm": 0.40, "gravy": 0.25, "charge": 0.20, "mw": 0.15},
        "description": "Amphiphilic surface activity for stable oil-in-water emulsion."
    },
    "crayfish": {
        "weights": {"esm": 0.35, "mw": 0.35, "charge": 0.15, "cysteine": 0.15},
        "description": "Low-molecular weight peptide profile for savory umami taste receptor binding."
    },
    "sarcopenia": {
        "weights": {"esm": 0.40, "mw": 0.25, "charge": 0.20, "gravy": 0.15},
        "description": "High solubility and low paste viscosity for geriatric swallow fortification."
    }
}


def score_protein_pair(
    candidate_features: Dict[str, float],
    benchmark_features: Dict[str, float],
    job: str,
    cand_embedding: Any = None,
    bench_embedding: Any = None
) -> Tuple[float, Dict[str, float], str]:
    """
    Scores a candidate protein against a benchmark control for a specific job:
    Returns (final_score, contribution_breakdown, confidence_level).
    Score ranges from 0.0 to 100.0%.
    """
    profile = JOB_WEIGHT_PROFILES.get(job, JOB_WEIGHT_PROFILES["meat"])
    weights = profile["weights"]

    # 1. ESM-2 Cosine divergence
    if cand_embedding is not None and bench_embedding is not None:
        delta_esm = calculate_cosine_distance(cand_embedding, bench_embedding)
    else:
        delta_esm = 0.15  # calibrated baseline divergence

    # 2. Physicochemical feature divergences
    delta_mw = calculate_normalized_divergence(
        candidate_features.get("molecular_weight", 50000),
        benchmark_features.get("molecular_weight", 50000),
        NORMALIZERS["mw"]
    )
    delta_pi = calculate_normalized_divergence(
        candidate_features.get("isoelectric_point", 6.0),
        benchmark_features.get("isoelectric_point", 6.0),
        NORMALIZERS["pi"]
    )
    delta_charge = calculate_normalized_divergence(
        candidate_features.get("charge_at_ph7", 0.0),
        benchmark_features.get("charge_at_ph7", 0.0),
        NORMALIZERS["charge"]
    )
    delta_gravy = calculate_normalized_divergence(
        candidate_features.get("gravy", -0.4),
        benchmark_features.get("gravy", -0.4),
        NORMALIZERS["gravy"]
    )
    delta_cys = calculate_normalized_divergence(
        candidate_features.get("cysteine_fraction", 0.01),
        benchmark_features.get("cysteine_fraction", 0.01),
        NORMALIZERS["cysteine"]
    )

    divergence_map = {
        "esm": delta_esm,
        "mw": delta_mw,
        "pi": delta_pi,
        "charge": delta_charge,
        "gravy": delta_gravy,
        "cysteine": delta_cys
    }

    # 3. Weighted total penalty
    total_penalty = 0.0
    contributions = {}
    for feature_name, weight in weights.items():
        div = divergence_map.get(feature_name, 0.0)
        penalty = weight * div
        total_penalty += penalty
        contributions[feature_name] = round(float((1.0 - div) * weight * 100), 2)

    final_score = round(max(0.0, min(100.0, (1.0 - total_penalty) * 100)), 2)

    # 4. Confidence level determination
    if final_score >= 85.0:
        confidence = "High"
    elif final_score >= 75.0:
        confidence = "Medium"
    else:
        confidence = "Low"

    return final_score, contributions, confidence
