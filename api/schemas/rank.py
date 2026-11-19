"""
Pydantic v2 schemas for ranking endpoints.
Strict validation with extra='forbid' to prevent unvalidated fields.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum


class JobEnum(str, Enum):
    egg = "egg"
    gel = "gel"
    milk = "milk"


class RankRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    job: JobEnum = Field(..., description="Target functional application (egg, gel, milk)")
    benchmark_id: str = Field(..., description="Benchmark crop ID (e.g. mung_bean, soy)")
    top_k: int = Field(5, ge=1, le=20, description="Maximum number of candidate crops to return")
    custom_weights: Optional[Dict[str, float]] = Field(
        None, description="Optional biochemist adjusted weights (must sum to ~1.0)"
    )


class CandidateRankItem(BaseModel):
    crop_id: str
    common_name: str
    scientific_name: str
    best_accession: str
    protein_name: str
    family: str
    score: float
    confidence: str  # 'High', 'Medium', 'Low'
    contributions: Dict[str, Any]
    screening_flags: List[str]


class RankResponse(BaseModel):
    job: str
    benchmark_id: str
    model_version: str = "v1.0"
    data_snapshot_id: str = "snapshot_nov2026"
    disclaimer: str = (
        "Scores represent similarity-based likelihoods, not laboratory measurements. "
        "Intended strictly for prioritizing wet-lab candidate screening."
    )
    candidates: List[CandidateRankItem]
