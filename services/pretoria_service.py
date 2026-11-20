"""
University of Pretoria Empirical Wet-Lab Data Service.
Provides verified solubility, gelation, and composition measurements.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from api.db import SessionLocal, Measurement


def get_pretoria_measurements(crop_id: Optional[str] = None, job_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves verified empirical wet-lab measurements from University of Pretoria study."""
    db: Session = SessionLocal()
    try:
        query = db.query(Measurement)
        if crop_id:
            query = query.filter(Measurement.crop_id == crop_id)
        if job_id:
            query = query.filter(Measurement.job == job_id)
        rows = query.all()

        return [
            {
                "crop_id": m.crop_id,
                "job": m.job,
                "property": m.property,
                "value": m.value,
                "unit": m.unit,
                "conditions": m.conditions,
                "study_id": m.study_id,
                "citation": m.citation,
                "verified_by": m.verified_by,
                "notes": m.notes
            }
            for m in rows
        ]
    finally:
        db.close()


def get_bambara_empirical_dossier() -> Dict[str, Any]:
    """Returns the empirical wet-lab verification dossier for Bambara groundnut."""
    return {
        "crop": "Bambara groundnut (Vigna subterranea)",
        "empirical_solubility_ph7": 82.27,
        "least_gelation_concentration_pct": "8.0% - 10.0% w/v",
        "crude_protein_pct": "21.5%",
        "water_absorption_capacity": "2.3 g/g",
        "oil_absorption_capacity": "1.8 g/g",
        "citation": "University of Pretoria Plant-Protein Laboratory (2020), Sample M38",
        "scientific_integrity_status": "Tier 1 Wet-Lab Priority (Sequence models bypassed due to 0 UniProt globulin entries)"
    }
