"""
Router for Crops endpoints (/api/v1/crops).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.db import get_db, Crop, Protein

router = APIRouter(prefix="/api/v1/crops", tags=["Crops"])


@router.get("")
def list_crops(db: Session = Depends(get_db)):
    """Return all benchmark and candidate crops with sequence coverage stats."""
    crops = db.query(Crop).all()
    results = []

    for c in crops:
        prots = db.query(Protein).filter(Protein.crop_id == c.id).all()
        reviewed = sum(1 for p in prots if p.reviewed)
        decision = "Keep" if len(prots) > 0 else "No Data / Unranked"

        results.append({
            "id": c.id,
            "common_name": c.common_name,
            "scientific_name": c.scientific_name,
            "role": c.role,
            "primary_job": c.primary_job,
            "description": c.description,
            "total_proteins": len(prots),
            "reviewed_count": reviewed,
            "decision": decision,
        })
    return results
