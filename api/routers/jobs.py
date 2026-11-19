"""
Router for Jobs endpoints (/api/v1/jobs).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import yaml
from api.db import get_db, Job

router = APIRouter(prefix="/api/v1/jobs", tags=["Jobs"])


@router.get("")
def list_jobs(db: Session = Depends(get_db)):
    """Return all active functional jobs with configurations and benchmarks."""
    with open("config/jobs.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)["jobs"]

    result = []
    for j_id, j_cfg in data.items():
        result.append({
            "id": j_id,
            "name": j_cfg["name"],
            "description": j_cfg["target_function"],
            "primary_benchmark": j_cfg["primary_benchmark"],
            "key_family_target": j_cfg.get("key_family_target", "7S"),
            "citations": j_cfg.get("citations", []),
        })
    return result
