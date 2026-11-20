"""
Biophysical Feature Calculator.
Calculates molecular weight, isoelectric point, charge at pH 7.0, cysteines, and GRAVY using Biopython.
"""

import re
from typing import Dict, Any

try:
    from Bio.SeqUtils.ProtParam import ProteinAnalysis
    has_biopython = True
except ImportError:
    has_biopython = False


def clean_sequence(seq: str) -> str:
    """Sanitizes raw sequence text, stripping non-standard amino acid characters."""
    cleaned = re.sub(r"[^ACDEFGHIKLMNPQRSTVWY]", "", seq.upper().strip())
    return cleaned


def extract_protein_features(sequence: str) -> Dict[str, float]:
    """
    Computes standard physicochemical feature vectors for a validated amino acid sequence:
    - length: Integer sequence length
    - molecular_weight: Mass in Daltons
    - isoelectric_point: pI value (charge neutrality pH)
    - charge_at_ph7: Net surface electrical charge at physiological neutral pH
    - gravy: Grand Average of Hydropathicity (hydrophobic vs hydrophilic balance)
    - cysteine_fraction: Proportion of cysteine residues available for disulfide cross-linking
    """
    cleaned = clean_sequence(sequence)
    if not cleaned:
        return {
            "length": 0.0,
            "molecular_weight": 0.0,
            "isoelectric_point": 7.0,
            "charge_at_ph7": 0.0,
            "gravy": 0.0,
            "cysteine_fraction": 0.0
        }

    length = float(len(cleaned))
    cys_count = cleaned.count("C")
    cys_frac = cys_count / length

    if has_biopython:
        analysis = ProteinAnalysis(cleaned)
        mw = analysis.molecular_weight()
        pi = analysis.isoelectric_point()
        charge = analysis.charge_at_pH(7.0)
        gravy = analysis.gravy()
    else:
        # Graceful fallback approximations
        mw = length * 110.0
        pi = 6.0
        charge = 0.0
        gravy = -0.4

    return {
        "length": length,
        "molecular_weight": round(mw, 2),
        "isoelectric_point": round(pi, 2),
        "charge_at_ph7": round(charge, 2),
        "gravy": round(gravy, 3),
        "cysteine_fraction": round(cys_frac, 4)
    }
