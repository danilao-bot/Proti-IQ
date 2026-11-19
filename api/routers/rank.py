"""
Router for Ranking endpoint (/api/v1/rank).
Serves precomputed rankings and candidate evaluations in < 300ms.
"""

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.db import get_db, Ranking, Protein, Crop, ModelRun
from api.schemas.rank import RankRequest, RankResponse, CandidateRankItem

router = APIRouter(prefix="/api/v1/rank", tags=["Rankings"])


@router.post("", response_model=RankResponse)
def get_rankings(req: RankRequest, db: Session = Depends(get_db)):
    """
    Generate ranked candidate list for a selected job and benchmark.
    Returns scores, explainable contribution breakdowns, confidence badges, and screening flags.
    """
    # Find latest completed model run
    latest_run = (
        db.query(ModelRun)
        .order_by(ModelRun.created_at.desc())
        .first()
    )
    run_id = latest_run.id if latest_run else None

    query = db.query(Ranking).filter(
        Ranking.job == req.job.value,
        Ranking.benchmark_id == req.benchmark_id,
    )
    if run_id:
        query = query.filter(Ranking.run_id == run_id)

    rankings = query.order_by(Ranking.score.desc()).all()

    # Deduplicate by crop_id (show the highest-scoring protein for each crop)
    seen_crops = set()
    candidate_items = []

    for r in rankings:
        if r.crop_id in seen_crops:
            continue
        seen_crops.add(r.crop_id)

        crop = db.query(Crop).filter(Crop.id == r.crop_id).first()
        protein = db.query(Protein).filter(Protein.id == r.protein_id).first()

        contributions = json.loads(r.contributions_json) if r.contributions_json else {}
        flags = json.loads(r.flags_json) if r.flags_json else []

        candidate_items.append(
            CandidateRankItem(
                crop_id=r.crop_id,
                common_name=crop.common_name if crop else r.crop_id,
                scientific_name=crop.scientific_name if crop else "",
                best_accession=protein.accession if protein else "",
                protein_name=protein.name if protein else "",
                family=protein.family if protein else "other",
                score=r.score,
                confidence=r.confidence,
                contributions=contributions,
                screening_flags=flags,
            )
        )

        if len(candidate_items) >= req.top_k:
            break

    return RankResponse(
        job=req.job.value,
        benchmark_id=req.benchmark_id,
        candidates=candidate_items,
    )
