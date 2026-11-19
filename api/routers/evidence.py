"""
Router for Evidence and Back-Test endpoints (/api/v1/evidence).
"""

import json
import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.db import get_db, Measurement

router = APIRouter(prefix="/api/v1/evidence", tags=["Evidence"])


@router.get("/{job}")
def get_job_evidence(job: str, db: Session = Depends(get_db)):
    """Retrieve back-test metrics, literature answer-key rows, and explicit failure cases."""
    backtest_file = "data/processed/backtest_results.json"
    backtest_data = {}
    if os.path.exists(backtest_file):
        with open(backtest_file, "r", encoding="utf-8") as f:
            backtest_data = json.load(f)

    # Fetch verified literature measurements for this job
    measurements = (
        db.query(Measurement)
        .filter(Measurement.job == job)
        .all()
    )

    meas_list = []
    for m in measurements:
        meas_list.append({
            "study_id": m.study_id,
            "property": m.property,
            "value": m.value,
            "unit": m.unit,
            "conditions": m.conditions,
            "citation": m.citation,
            "notes": m.notes,
        })

    job_bt = backtest_data.get("jobs", {}).get(job, {})
    held_out = backtest_data.get("held_out_checks", {}).get("cowpea_egg_validation") if job == "egg" else None

    return {
        "job": job,
        "summary": "Within-study Spearman correlation and held-out benchmark validation",
        "spearman_rho": job_bt.get("spearman_rho"),
        "sample_size": job_bt.get("sample_size"),
        "interpretation": job_bt.get("interpretation"),
        "held_out_validation": held_out,
        "documented_failure_cases": backtest_data.get("documented_failure_cases", []),
        "literature_answer_key": meas_list,
    }
