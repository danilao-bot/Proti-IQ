"""
AlphaFold 2 3D Coordinate and Confidence Inspector.
Reads local PDB files, extracts residue-level pLDDT values, and computes structural confidence tiers.
"""

import os
from typing import Dict, Any, List, Optional

STRUCTURES_DIR = os.path.abspath("data/raw/structures")


def get_structure_path(accession: str) -> Optional[str]:
    """Returns absolute file path to cached PDB structure file if present."""
    path = os.path.join(STRUCTURES_DIR, f"{accession.strip().upper()}.pdb")
    return path if os.path.exists(path) else None


def extract_plddt_metrics(accession: str) -> Dict[str, Any]:
    """
    Parses B-factor column in PDB coordinate file (where AlphaFold stores pLDDT 0-100 values).
    Returns mean pLDDT, per-tier counts (very high, high, low, very low), and quality badge.
    """
    path = get_structure_path(accession)
    if not path:
        return {
            "accession": accession,
            "available": False,
            "mean_plddt": None,
            "quality_tier": "Not Downloaded"
        }

    b_factors = []
    seen_residues = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("ATOM"):
                # Extract residue number and B-factor column (cols 61-66 in standard PDB)
                try:
                    res_seq = line[22:26].strip()
                    atom_name = line[12:16].strip()
                    if atom_name == "CA" and res_seq not in seen_residues:
                        seen_residues.add(res_seq)
                        bfactor = float(line[60:66].strip())
                        b_factors.append(bfactor)
                except (ValueError, IndexError):
                    continue

    if not b_factors:
        return {
            "accession": accession,
            "available": True,
            "mean_plddt": None,
            "quality_tier": "Invalid PDB Format"
        }

    mean_plddt = round(sum(b_factors) / len(b_factors), 2)
    very_high = sum(1 for b in b_factors if b >= 90)
    confident = sum(1 for b in b_factors if 70 <= b < 90)
    low = sum(1 for b in b_factors if 50 <= b < 70)
    very_low = sum(1 for b in b_factors if b < 50)

    if mean_plddt >= 80:
        tier = "High Confidence Backbone"
    elif mean_plddt >= 70:
        tier = "Medium-High Confidence"
    else:
        tier = "Flexible Loops / Partially Disordered"

    return {
        "accession": accession,
        "available": True,
        "mean_plddt": mean_plddt,
        "total_ca_residues": len(b_factors),
        "confidence_breakdown": {
            "very_high_gt90": very_high,
            "confident_70_90": confident,
            "low_50_70": low,
            "very_low_lt50": very_low
        },
        "quality_tier": tier
    }
