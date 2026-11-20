"""
Proti IQ Database Service.
Handles clean data lookups across local SQLite and cloud Supabase PostgreSQL.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from api.db import SessionLocal, Ranking, Crop, Protein, ModelRun, Measurement
import json


def get_latest_rankings_for_job(job_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieves ranked candidates for a specific job from database."""
    db: Session = SessionLocal()
    try:
        latest_run = db.query(ModelRun).order_by(ModelRun.created_at.desc()).first()
        run_id = latest_run.id if latest_run else None

        query = db.query(Ranking).filter(Ranking.job == job_id)
        if run_id:
            query = query.filter(Ranking.run_id == run_id)
        rankings = query.order_by(Ranking.score.desc()).all()

        seen_crops = set()
        results = []
        for r in rankings:
            if r.crop_id in seen_crops:
                continue
            seen_crops.add(r.crop_id)

            crop = db.query(Crop).filter(Crop.id == r.crop_id).first()
            prot = db.query(Protein).filter(Protein.id == r.protein_id).first()
            contributions = json.loads(r.contributions_json) if r.contributions_json else {}

            results.append({
                "rank": len(seen_crops),
                "crop_id": r.crop_id,
                "crop_name": crop.common_name if crop else r.crop_id,
                "scientific_name": crop.scientific_name if crop else "",
                "biophysical_similarity_score": r.score,
                "confidence": r.confidence,
                "representative_protein": {
                    "accession": prot.accession if prot else "",
                    "name": prot.name if prot else "",
                    "family": prot.family if prot else ""
                },
                "contributions": contributions
            })
            if len(results) >= limit:
                break
        return results
    finally:
        db.close()


def get_all_crops() -> List[Dict[str, Any]]:
    """Retrieves all 14 crops with metadata and protein counts."""
    db: Session = SessionLocal()
    try:
        crops = db.query(Crop).all()
        results = []
        for c in crops:
            prots = db.query(Protein).filter(Protein.crop_id == c.id).all()
            results.append({
                "id": c.id,
                "common_name": c.common_name,
                "scientific_name": c.scientific_name,
                "role": c.role,
                "primary_job": c.primary_job,
                "description": c.description,
                "protein_count": len(prots)
            })
        return results
    finally:
        db.close()
