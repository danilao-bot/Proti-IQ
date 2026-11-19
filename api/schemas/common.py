"""
Pydantic v2 schemas for Jobs, Crops, and Evidence endpoints.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict


class JobResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    description: str
    primary_benchmark: str
    key_family_target: str
    citations: List[str]


class CropResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    common_name: str
    scientific_name: str
    role: str
    primary_job: Optional[str]
    description: Optional[str]
    total_proteins: int = 0
    reviewed_count: int = 0
    decision: str = "Keep"


class EvidenceResponse(BaseModel):
    summary: str
    job: str
    spearman_rho: Optional[float]
    sample_size: Optional[int]
    held_out_cowpea: Optional[Dict[str, Any]]
    documented_failure_cases: List[Dict[str, Any]]
    answer_key_measurements: List[Dict[str, Any]]
