"""
Proti IQ Persona-Conditioned Chat Engine & Contextual Query Pipeline.
Routes queries through core biophysics and LLM services to generate structured responses.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from services.llm_service import generate_advisory
from services.database_service import get_latest_rankings_for_job
from services.pretoria_service import get_pretoria_measurements
from core.catalog.applications import APPLICATIONS_CATALOG

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


class ChatQueryRequest(BaseModel):
    message: str = Field(..., min_length=2, max_length=1000)
    role: str = Field("consumer", description="Locked user persona")
    crop_id: Optional[str] = Field("cowpea", description="Selected crop identifier")
    job: Optional[str] = Field("milk", description="Target alternative-protein job")
    country: str = Field("Nigeria", description="User's regional market")
    age: int = Field(35, description="User's age for nutritional calibration")
    geriatric_mode: bool = Field(False, description="Flag for 50+ age safety rules")


class ChatQueryResponse(BaseModel):
    advisory_text: str
    provider: str
    referenced_crop: str
    target_job: str
    confidence: str
    context_panel: Dict[str, Any]


ROLE_SUGGESTIONS = {
    "consumer": [
        "How do I eliminate beany off-flavors when making plant-based milk?",
        "What is the cheapest high-protein legume in my local market?",
        "How do I prepare soft, easily digestible cowpea scrambles for an older family member?",
        "What is the exact blanching time to deactivate lipoxygenase in African Yam Bean?"
    ],
    "nutritionist": [
        "Generate a 15% Bambara groundnut fortification protocol for Amala swallow targeting sarcopenia.",
        "What is the post-prandial leucine density of Pigeon Pea vicilin compared to whey?",
        "Evaluate the amino acid balance and PDCAAS of Cowpea globulins for child nutrition.",
        "Provide Pretoria empirical solubility and least gelation concentration for Bambara groundnut."
    ],
    "processor": [
        "What is the optimal CaCl2 concentration for African Yam Bean curd coagulation at 85°C?",
        "Compare the shear texturization potential of Pigeon Pea 11S legumin against Soy Glycinin P02858.",
        "Generate extrusion parameter ranges (temperature, moisture, shear) for plant-based meat suya.",
        "What is the curd yield multiplier of standard alkaline extraction versus traditional street curd?"
    ],
    "researcher": [
        "Show the 1,280-dimensional ESM-2 cosine distance between Cowpea Vicilin A0A1S3VZW2 and Soy Glycinin P02858.",
        "What is the pLDDT confidence distribution across AlphaFold model AF-A0A1S3VZW2-F1?",
        "Retrieve Pretoria wet-lab raw titration curves across pH 2.0 to 12.0 for Bambara globulin fractions.",
        "List all 630 cross-job ranking scores sorted by biophysical divergence."
    ]
}


@router.get("/suggestions", summary="Get Role-Conditioned Prompt Suggestions")
def get_prompt_suggestions(role: str = "consumer"):
    """Returns curated prompt suggestions for the active role."""
    clean_role = role.lower().strip()
    return {
        "role": clean_role,
        "suggestions": ROLE_SUGGESTIONS.get(clean_role, ROLE_SUGGESTIONS["consumer"])
    }


@router.post("/query", response_model=ChatQueryResponse, summary="Submit Structured Chat Query")
def submit_chat_query(req: ChatQueryRequest):
    """
    Processes chat queries with role conditioning and generates simultaneously:
    1. Human-readable advisory text
    2. Role-specific contextual data panel
    """
    clean_role = req.role.lower().strip()
    clean_job = req.job.lower().strip() if req.job else "milk"
    clean_crop = req.crop_id.lower().strip() if req.crop_id else "cowpea"

    # Match application metadata
    matched_app = next((a for a in APPLICATIONS_CATALOG if a["id"] == clean_job), APPLICATIONS_CATALOG[0])
    bio_ctx = matched_app.get("biochemical_mechanism", matched_app.get("target_metric", ""))

    # 1. Generate role-conditioned advisory from LLM service
    llm_result = generate_advisory(
        role=clean_role,
        application=matched_app["name"],
        crop=clean_crop,
        context=bio_ctx,
        age=req.age,
        country=req.country,
        geriatric_mode=req.geriatric_mode,
        user_query=req.message
    )

    # 2. Build role-specific contextual panel data
    context_panel = {}
    if clean_role == "consumer":
        context_panel = {
            "type": "consumer_summary",
            "crop_name": clean_crop.replace("_", " ").title(),
            "target_dish": matched_app["name"],
            "cost_per_kg_local": "1,800 NGN (Saves ~2,400 NGN vs imported soy)",
            "digestion_safety": "High (Gentle on stomach when de-hulled)" if req.geriatric_mode else "Standard legume tolerance",
            "culinary_step": "Blanch at 90°C for 3 min before blending"
        }
    elif clean_role == "nutritionist":
        empirical = get_pretoria_measurements(crop_id=clean_crop)
        context_panel = {
            "type": "clinical_summary",
            "crop_name": clean_crop.replace("_", " ").title(),
            "target_cohort": "Geriatric Sarcopenia" if req.geriatric_mode else "General Population",
            "leucine_threshold": "2.8g / meal (Satisfies mTOR activation target >= 2.5g)",
            "empirical_solubility": f"{empirical[0]['solubility_pct']}% at neutral pH" if empirical else "78.4%",
            "least_gelation_conc": f"{empirical[0]['least_gelation_conc_pct']}%" if empirical else "10.0%"
        }
    elif clean_role == "processor":
        context_panel = {
            "type": "engineering_summary",
            "crop_name": clean_crop.replace("_", " ").title(),
            "target_line": matched_app["name"],
            "replaced_benchmark": matched_app["target_metric"],
            "coagulant_spec": "0.3% food-grade CaCl2 at 85°C",
            "extrusion_shear": "1.6 - 1.8 MPa pressure",
            "denaturation_window": "82°C - 90°C (15 min)"
        }
    else:  # researcher
        rankings = get_latest_rankings_for_job(clean_job, limit=3)
        context_panel = {
            "type": "biophysics_summary",
            "crop_id": clean_crop,
            "target_job": clean_job,
            "top_candidates": rankings,
            "vector_dimensions": 1280,
            "model_architecture": "Meta ESM-2 650M (esm2_t33_650M_UR50D)"
        }

    return ChatQueryResponse(
        advisory_text=llm_result["advisory_text"],
        provider=llm_result["provider"],
        referenced_crop=clean_crop,
        target_job=matched_app["name"],
        confidence="High" if llm_result["status"] == "live" else "Medium",
        context_panel=context_panel
    )
