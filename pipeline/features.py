"""
Physicochemical Feature Extraction for Proti IQ.
Computes biophysical and structural properties from amino acid sequences
using Biopython if present, or robust built-in biochemical formulas.
"""

from typing import Dict, Any
from sqlalchemy.orm import Session
from api.db import SessionLocal, Protein, Feature, init_db

STANDARD_AA = set("ACDEFGHIKLMNPQRSTVWY")

# Standard Kyte-Doolittle Hydropathy Scale
KYTE_DOOLITTLE = {
    "A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5,
    "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2, "I": 4.5,
    "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6,
    "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2,
}

# Monoisotopic / Average residue molecular weights (g/mol)
RESIDUE_MW = {
    "A": 71.08, "R": 156.20, "N": 114.11, "D": 115.09, "C": 103.14,
    "Q": 128.13, "E": 129.12, "G": 57.05, "H": 137.14, "I": 113.17,
    "L": 113.17, "K": 128.18, "M": 131.21, "F": 147.18, "P": 97.12,
    "S": 87.08, "T": 101.11, "W": 186.21, "Y": 163.18, "V": 99.13,
}

# Standard pKa values (EMBOSS / Lehninger scale)
PKA_VALUES = {
    "N_term": 9.69,
    "C_term": 2.34,
    "K": 10.53,
    "R": 12.48,
    "H": 6.00,
    "D": 3.86,
    "E": 4.25,
    "C": 8.33,
    "Y": 10.07,
}


def clean_sequence(seq: str) -> str:
    """Filter out non-standard amino acid characters to ensure accurate biochemical profiling."""
    return "".join([aa for aa in seq.upper() if aa in STANDARD_AA])


def calculate_charge(seq: str, ph: float) -> float:
    """Calculate net electrostatic charge of sequence at a given pH using Henderson-Hasselbalch."""
    # N-terminal positive charge
    charge = 1.0 / (1.0 + 10.0 ** (ph - PKA_VALUES["N_term"]))
    # C-terminal negative charge
    charge -= 1.0 / (1.0 + 10.0 ** (PKA_VALUES["C_term"] - ph))

    # Basic residues (positive when protonated)
    charge += seq.count("K") / (1.0 + 10.0 ** (ph - PKA_VALUES["K"]))
    charge += seq.count("R") / (1.0 + 10.0 ** (ph - PKA_VALUES["R"]))
    charge += seq.count("H") / (1.0 + 10.0 ** (ph - PKA_VALUES["H"]))

    # Acidic residues (negative when deprotonated)
    charge -= seq.count("D") / (1.0 + 10.0 ** (PKA_VALUES["D"] - ph))
    charge -= seq.count("E") / (1.0 + 10.0 ** (PKA_VALUES["E"] - ph))
    charge -= seq.count("C") / (1.0 + 10.0 ** (PKA_VALUES["C"] - ph))
    charge -= seq.count("Y") / (1.0 + 10.0 ** (PKA_VALUES["Y"] - ph))

    return charge


def calculate_isoelectric_point(seq: str) -> float:
    """Find the isoelectric point (pI) where net charge equals zero via binary bisection."""
    low_ph = 1.0
    high_ph = 14.0
    for _ in range(50):
        mid_ph = (low_ph + high_ph) / 2.0
        c = calculate_charge(seq, mid_ph)
        if abs(c) < 0.001:
            return round(mid_ph, 2)
        if c > 0:
            low_ph = mid_ph
        else:
            high_ph = mid_ph
    return round((low_ph + high_ph) / 2.0, 2)


def extract_protein_features(sequence: str) -> Dict[str, float]:
    """Calculate all biophysical features from an amino acid sequence."""
    clean_seq = clean_sequence(sequence)
    length = len(clean_seq)
    if length == 0:
        return {}

    # Check if Biopython is available
    try:
        from Bio.SeqUtils.ProtParam import ProteinAnalysis
        analyzed = ProteinAnalysis(clean_seq)
        mw = analyzed.molecular_weight()
        pi = analyzed.isoelectric_point()
        gravy = analyzed.gravy()
        aromaticity = analyzed.aromaticity()
        charge_ph7 = analyzed.charge_at_pH(7.0)
        charge_ph5 = analyzed.charge_at_pH(5.0)
        try:
            instability = analyzed.instability_index()
        except Exception:
            instability = 40.0
        try:
            helix, turn, sheet = analyzed.secondary_structure_fraction()
        except Exception:
            helix, turn, sheet = 0.33, 0.33, 0.34
    except ImportError:
        # Robust standalone biochemical formulas
        mw = sum(RESIDUE_MW.get(aa, 110.0) for aa in clean_seq) + 18.015
        pi = calculate_isoelectric_point(clean_seq)
        gravy = sum(KYTE_DOOLITTLE.get(aa, 0.0) for aa in clean_seq) / length
        aromaticity = (clean_seq.count("F") + clean_seq.count("Y") + clean_seq.count("W")) / length
        charge_ph7 = calculate_charge(clean_seq, 7.0)
        charge_ph5 = calculate_charge(clean_seq, 5.0)
        instability = 40.0
        # Levitt conformational frequencies proxy
        helix = (clean_seq.count("E") + clean_seq.count("A") + clean_seq.count("L") + clean_seq.count("M") + clean_seq.count("K")) / length
        sheet = (clean_seq.count("V") + clean_seq.count("I") + clean_seq.count("Y") + clean_seq.count("F") + clean_seq.count("W")) / length
        turn = max(0.0, 1.0 - (helix + sheet))

    cys_count = clean_seq.count("C")
    cys_fraction = cys_count / length

    # Solubility proxy: three biophysical signals that predict neutral-pH solubility
    # 1. Charge density at pH 7: high |charge|/length = strong electrostatic repulsion = resists aggregation
    charge_density = min(1.0, abs(charge_ph7) / (length * 0.06))
    # 2. Hydrophilicity from GRAVY: more negative = more hydrophilic surface = better water interaction
    hydrophilicity = min(1.0, max(0.0, (-gravy + 0.3) / 1.8))
    # 3. pI clearance from processing pH 7: further from pI = less risk of isoelectric precipitation
    pi_clearance = min(1.0, abs(pi - 7.0) / 2.5)
    # Weighted combination
    solubility_proxy = 0.40 * charge_density + 0.35 * hydrophilicity + 0.25 * pi_clearance

    return {
        "length": float(length),
        "molecular_weight": round(mw, 1),
        "isoelectric_point": round(pi, 2),
        "charge_at_ph7": round(charge_ph7, 2),
        "charge_at_ph5": round(charge_ph5, 2),
        "gravy": round(gravy, 3),
        "aromaticity": round(aromaticity, 3),
        "instability_index": round(instability, 1),
        "cysteine_fraction": round(cys_fraction, 4),
        "secondary_structure_helix": round(helix, 3),
        "secondary_structure_turn": round(turn, 3),
        "secondary_structure_sheet": round(sheet, 3),
        "solubility_proxy": round(solubility_proxy, 3),
    }


def compute_features_for_all(db: Session, version: str = "v1.0"):
    """Compute and persist feature vectors for all proteins in the database."""
    proteins = db.query(Protein).all()
    print(f"Extracting biophysical features for {len(proteins)} proteins...")

    count = 0
    for prot in proteins:
        features = extract_protein_features(prot.sequence)
        for name, val in features.items():
            existing = (
                db.query(Feature)
                .filter(Feature.protein_id == prot.id, Feature.feature_name == name)
                .first()
            )
            if not existing:
                db.add(Feature(protein_id=prot.id, feature_name=name, value=val, feature_set_version=version))
            else:
                existing.value = val
                existing.feature_set_version = version
            count += 1

    db.commit()
    print(f"Feature extraction complete: {count} feature entries recorded.")


def run_features():
    init_db()
    db = SessionLocal()
    try:
        compute_features_for_all(db)
    finally:
        db.close()


if __name__ == "__main__":
    run_features()
