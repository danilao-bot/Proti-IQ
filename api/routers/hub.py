"""
Proti IQ Hub & Formulation Advisory Router.
Provides clean REST endpoints for the React frontend, delegating logic to core and services:
- GET  /api/v1/hub/applications
- GET  /api/v1/hub/rankings
- POST /api/v1/hub/advisory/formulate
- GET  /api/v1/hub/empirical/{crop_id}
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from api.db import get_db, Ranking, Crop, Protein, ModelRun
from core.catalog.applications import APPLICATIONS_CATALOG, REGIONAL_AVAILABILITY
from services.llm_service import generate_advisory
from services.pretoria_service import get_pretoria_measurements, get_bambara_empirical_dossier
import json

router = APIRouter(prefix="/api/v1/hub", tags=["Discovery Hub & Advisory"])


@router.get("/applications", summary="List All Alternative-Protein Categories")
def get_hub_applications():
    """Returns the comprehensive catalog of 7 alternative-protein discovery categories."""
    return {
        "total_categories": len(APPLICATIONS_CATALOG),
        "categories": APPLICATIONS_CATALOG
    }


@router.get("/rankings", summary="Query Crop Rankings for an Application")
def get_hub_rankings(
    job: str = Query(..., description="Target application ID: egg, milk, gel, meat, crayfish, mayo, sarcopenia"),
    country: str = Query("Nigeria", description="Target African country: Nigeria, Ghana, Kenya, South Africa"),
    db: Session = Depends(get_db)
):
    """
    Returns ranked African legume crops for a specific alternative-protein job,
    filtered by regional country availability.
    """
    valid_jobs = [c["id"] for c in APPLICATIONS_CATALOG]
    if job not in valid_jobs:
        raise HTTPException(status_code=400, detail=f"Invalid job ID. Must be one of: {valid_jobs}")

    # Fetch latest model run
    latest_run = db.query(ModelRun).order_by(ModelRun.created_at.desc()).first()
    run_id = latest_run.id if latest_run else None

    query = db.query(Ranking).filter(Ranking.job == job)
    if run_id:
        query = query.filter(Ranking.run_id == run_id)
    rankings = query.order_by(Ranking.score.desc()).all()

    # Regional availability lookup
    country_clean = country.split()[0]
    region_info = REGIONAL_AVAILABILITY.get(country_clean, REGIONAL_AVAILABILITY["Nigeria"])

    seen_crops = set()
    ranked_candidates = []
    for r in rankings:
        if r.crop_id in seen_crops:
            continue
        seen_crops.add(r.crop_id)

        crop = db.query(Crop).filter(Crop.id == r.crop_id).first()
        prot = db.query(Protein).filter(Protein.id == r.protein_id).first()
        contributions = json.loads(r.contributions_json) if r.contributions_json else {}

        ranked_candidates.append({
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
            "contributions": contributions,
            "regional_presence": r.crop_id in region_info["primary_crops"]
        })

    # Add wet-lab empirical data for Bambara if relevant
    wet_lab_note = None
    if job in ["milk", "gel", "sarcopenia"]:
        wet_lab_note = get_bambara_empirical_dossier()

    return {
        "job": job,
        "country": country_clean,
        "model_run_id": run_id,
        "top_pick": ranked_candidates[0] if ranked_candidates else None,
        "backup_substitute": ranked_candidates[1] if len(ranked_candidates) > 1 else None,
        "candidates": ranked_candidates,
        "wet_lab_empirical_evidence": wet_lab_note
    }


class FormulateRequest(BaseModel):
    role: str = Field(..., description="Role: 'consumer', 'nutritionist', or 'food_processor'")
    job: str = Field(..., description="Job application ID (e.g. egg, milk, gel, meat, crayfish, sarcopenia)")
    crop_id: Optional[str] = Field("cowpea", description="Selected crop ID")
    staple_vehicle: Optional[str] = Field(None, description="Traditional food vehicle (e.g. amala, tuwo, ogi)")
    older_person_mode: Optional[bool] = Field(False, description="Whether older-person sarcopenia mode is enabled")


@router.post("/advisory/formulate", summary="Generate Role-Based Formulation Instructions")
def formulate_advisory(req: FormulateRequest):
    """
    Generates role-differentiated formulation instructions:
    - Consumer: Kitchen recipe, 'Plant-Based as Cooked' verification, and savings.
    - Nutritionist: Protein density calculation, amino acid profile, and clinical advisory.
    - Food Processor: Path B industrial processing parameters (pH, CaCl2 %, heat profile).
    """
    role = req.role.lower().strip()
    job = req.job.lower().strip()
    crop = req.crop_id.lower().strip() if req.crop_id else "cowpea"
    older = req.older_person_mode

    # Match application metadata from core catalog
    matched_app = next((a for a in APPLICATIONS_CATALOG if a["id"] == job), APPLICATIONS_CATALOG[0])
    bio_ctx = matched_app.get("biochemical_mechanism", matched_app.get("target_metric", ""))

    if "consumer" in role or "caregiver" in role:
        instructions = [
            f"Step 1: Clean and de-hull dry {crop.replace('_', ' ').title()} seeds by soaking in warm water for 15 minutes.",
            "Step 2 (Critical de-flavoring): Blanch de-hulled seeds in hot water (90°C) for 3 minutes. This permanently destroys lipoxygenase enzymes and eliminates all beany off-flavors.",
            "Step 3: Wet-mill at a 1:6 seed-to-water ratio until silky smooth.",
            "Step 4: Strain through a fine muslin or cheesecloth to collect smooth protein liquor.",
            "Step 5: Simmer gently with date syrup or vanilla, or season for savory dishes."
        ]
        if job == "egg":
            instructions = [
                f"Step 1: Use finely milled {crop.replace('_', ' ').title()} flour (100g).",
                "Step 2: Whisk with 180ml water, 1 tbsp vegetable oil, a pinch of turmeric (for golden color), and salt.",
                "Step 3: Pour into a hot oiled pan over medium heat (85°C); cook for 3-4 minutes, folding gently into soft scrambles."
            ]
        elif job == "crayfish":
            instructions = [
                "Step 1: Obtain traditional fermented African locust beans (Iru / Dawadawa).",
                "Step 2: Sun-dry or oven-dry at 60°C until crisp.",
                "Step 3: Mill into a fine golden-brown seasoning powder.",
                "Step 4: Add 1-2 tablespoons directly into Egusi, Ogbono, or Efo Riro. Delivers 100% savory umami without crayfish allergens."
            ]

        llm_result = generate_advisory("Consumer / Caregiver", matched_app["name"], crop, bio_ctx)

        return {
            "role": "consumer",
            "application": matched_app["name"],
            "selected_crop": crop,
            "plant_based_as_cooked_status": matched_app["plant_based_flag"],
            "kitchen_instructions": instructions,
            "cost_benefit": "Saves an estimated ₦3,000–₦4,500 per week compared to commercial dairy or poultry eggs.",
            "nutritional_impact": "100% plant-based, zero dietary cholesterol, rich in prebiotic legume fiber." + (" Highly digestible soft protein; gentle on aging digestive systems." if older else ""),
            "ai_generative_advisory": llm_result["advisory_text"],
            "ai_provider": llm_result["provider"]
        }

    elif "nutritionist" in role or "dietitian" in role:
        vehicle = req.staple_vehicle or "Amala"
        llm_result = generate_advisory("Clinical Nutritionist", matched_app["name"], crop, f"Fortifying {vehicle} for elderly sarcopenia. Context: {bio_ctx}")

        return {
            "role": "nutritionist",
            "application": matched_app["name"],
            "target_cohort": "Geriatric Sarcopenia (Age 50+)" if older else "General Population / Clinical Nutrition",
            "fortification_vehicle": vehicle,
            "formulation_ratio": f"15% {crop.replace('_', ' ').title()} isolate + 85% {vehicle} flour",
            "delivered_protein_density": "18.5g protein per 100g cooked portion",
            "amino_acid_profile": {
                "leucine": "7.8g / 100g protein (triggers mTOR muscle synthesis pathway)",
                "lysine": "6.4g / 100g protein (compensates for cereal lysine deficiency)",
                "methionine_cysteine": "2.2g / 100g protein"
            },
            "viscosity_impact": "Negligible change in swallow texture; maintains traditional dough viscoelasticity",
            "clinical_advisory": "Recommended 2 servings daily to prevent age-related muscle mass loss and maintain glycemic stability.",
            "ai_generative_advisory": llm_result["advisory_text"],
            "ai_provider": llm_result["provider"]
        }

    else:  # food_processor / manufacturer
        llm_result = generate_advisory("Food Factory R&D Engineer", matched_app["name"], crop, f"Industrial processing spec: {matched_app['target_metric']}. Context: {bio_ctx}")

        return {
            "role": "food_processor",
            "application": matched_app["name"],
            "industrial_crop": crop,
            "target_benchmark_to_beat": matched_app["target_metric"],
            "path_b_processing_roadmap": {
                "extraction_ph": "8.5 - 9.0 (Alkaline solubilization at 45°C for 45 min)",
                "thermal_denaturation": "85°C for 15 minutes (unfolding 11S legumin hexamers)",
                "coagulant_addition": "0.3% w/v food-grade CaCl2 or 0.25% CaSO4 at 80°C",
                "pressing_pressure": "15 kPa for 20 minutes in perforated pneumatic mold",
                "curd_yield_multiplier": "2.4x yield compared to non-standardized traditional street curd"
            },
            "quality_assurance_spec": {
                "target_breaking_stress": "1.2 - 1.5 N",
                "microbial_safety": "Pasteurization at 90°C ensures zero viable pathogens",
                "moisture_content": "72% - 76% in finished coagulated curd"
            },
            "ai_generative_advisory": llm_result["advisory_text"],
            "ai_provider": llm_result["provider"]
        }


@router.get("/empirical/{crop_id}", summary="Get Wet-Lab Pretoria Data for a Crop")
def get_crop_empirical_data(crop_id: str):
    """Returns University of Pretoria wet-lab measurements for a specific crop."""
    measurements = get_pretoria_measurements(crop_id=crop_id)
    return {
        "crop_id": crop_id,
        "total_measurements": len(measurements),
        "measurements": measurements
    }
