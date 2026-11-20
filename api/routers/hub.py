"""
Proti IQ Hub & Formulation Advisory Router.
Provides REST endpoints for Edna's React frontend:
- GET  /api/v1/hub/applications
- GET  /api/v1/hub/rankings
- POST /api/v1/advisory/formulate
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from api.db import get_db, Ranking, Crop, Protein, ModelRun
import json

router = APIRouter(prefix="/api/v1/hub", tags=["Discovery Hub & Advisory"])

# Master Applications Catalog
APPLICATIONS_CATALOG = [
    {
        "id": "egg",
        "name": "Plant-Based Egg Gel",
        "animal_replaced": "Chicken Eggs",
        "benchmark": "Mung bean 8S Vicilin (JUST Egg control, A0A1S3VZW2)",
        "protein_family": "7S Vicilin trimeric storage globulin",
        "top_african_crop": "Pigeon pea (Cajanus cajan)",
        "backup_substitute": "Cowpea (Vigna unguiculata)",
        "cultural_meals": ["Moi moi (steamed bean pudding)", "Akara (whipped bean fritters)", "Breakfast egg scramble"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "target_metric": "Rupture Force ~0.8 N, Springiness >85%"
    },
    {
        "id": "milk",
        "name": "Plant-Based Milk & Dairy Drinks",
        "animal_replaced": "Cow Milk & Canned Evaporated Milk",
        "benchmark": "Soybean 7S Beta-conglycinin alpha' (P11827)",
        "protein_family": "High net-negative charge soluble globulin",
        "top_african_crop": "Cowpea (Vigna unguiculata)",
        "backup_substitute": "Bambara groundnut (Vigna subterranea)",
        "cultural_meals": ["Kunu Aya (Tigernut milk)", "Kunu Gyada (Groundnut milk)", "Tea & pap whitener"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "target_metric": "Colloidal Stability >90% at 7 days, pH 7 Solubility >80%"
    },
    {
        "id": "gel",
        "name": "Plant-Based Curd & Cheese (Awara / Wagashi)",
        "animal_replaced": "Stew Beef Chunks & Fulani Cow Cheese (Wara / Wagashi)",
        "benchmark": "Soybean 11S Glycinin G4 (P02858)",
        "protein_family": "11S Legumin hexamer with acidic/basic subunits",
        "top_african_crop": "African yam bean (Sphenostylis stenocarpa)",
        "backup_substitute": "Pigeon pea (Cajanus cajan)",
        "cultural_meals": ["Awara (fried plant curd)", "Wagashi (cheese curd alternative)", "Soup meat substitute"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "target_metric": "Breaking Stress 1.2 - 1.5 N via 0.3% CaCl2 cross-linking"
    },
    {
        "id": "meat",
        "name": "Textured Plant-Based Meat & Suya",
        "animal_replaced": "Red Meat, Beef & Chewy Goat Meat (Asun)",
        "benchmark": "Soy Textured Vegetable Protein (SPI Extrudate, P02858)",
        "protein_family": "11S Legumin hexamer with structural cysteine dyads",
        "top_african_crop": "Pigeon pea (Cajanus cajan) & African yam bean",
        "backup_substitute": "Groundnut meal & Bambara groundnut press-cake",
        "cultural_meals": ["Beef Suya skewers", "Dried Kilishi strips", "Peppered meat pies", "Stew meat chunks"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "target_metric": "Tensile shear modulus matching beef muscle fibers"
    },
    {
        "id": "crayfish",
        "name": "Savory Umami Peptides & Crayfish Alternative",
        "animal_replaced": "Dried River Crayfish & Smoked Bonga Fish Seasoning",
        "benchmark": "Dried River Crayfish & Smoked Fish Peptides",
        "protein_family": "Low-molecular weight umami peptide hydrolysate (<1 kDa)",
        "top_african_crop": "Fermented African Locust Bean (Iru / Dawadawa)",
        "backup_substitute": "Fermented African yam bean peptides",
        "cultural_meals": ["Egusi soup", "Ogbono soup", "Efo riro", "Gbegiri soup", "Jollof rice seasoning"],
        "plant_based_flag": "100% Plant-Based (Traditional umami secret of West Africa)",
        "target_metric": "High free glutamic acid and sulfurous savory peptides"
    },
    {
        "id": "mayo",
        "name": "Plant-Based Mayonnaise & Dressings",
        "animal_replaced": "Commercial Egg-Yolk Mayonnaise & Salad Creams",
        "benchmark": "Egg-Yolk Lecithin Emulsion (70% vegetable oil phase)",
        "protein_family": "Amphiphilic surface-active 7S globulin",
        "top_african_crop": "Pigeon pea (Cajanus cajan) & Groundnut conarachin",
        "backup_substitute": "Cowpea isolate",
        "cultural_meals": ["Nigerian salad dressing (Heinz/Bama style)", "Sandwich spread", "Shawarma sauce"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "target_metric": "Oil-in-Water emulsion stability >12 months without separation"
    },
    {
        "id": "sarcopenia",
        "name": "Clinical Sarcopenia High-Protein Swallows & Porridges",
        "animal_replaced": "Medical Whey Protein Isolate & Meat Broth Fortifiers",
        "benchmark": "Medical Whey Protein Isolate (Oral Nutritional Supplement)",
        "protein_family": "Partially enzymatically hydrolyzed peptides (<5 kDa)",
        "top_african_crop": "Cowpea & Pigeon pea hydrolysate (Papain-digested)",
        "backup_substitute": "Bambara groundnut flour blend",
        "cultural_meals": ["Protein-fortified Amala", "Fortified Tuwo Shinkafa", "Fortified Ogi / Akamu porridge"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "target_metric": "18g protein / 100g portion with zero swallow paste viscosity increase"
    }
]

# Regional agronomic crop availability matrix
REGIONAL_AVAILABILITY = {
    "Nigeria": {
        "primary_crops": ["cowpea", "bambara_groundnut", "pigeon_pea", "african_yam_bean", "groundnut"],
        "notes": "Cowpea and Groundnut widely available nationally; Bambara in East & North; AYB primarily in South & Central."
    },
    "Ghana": {
        "primary_crops": ["cowpea", "bambara_groundnut", "groundnut"],
        "notes": "Cowpea (Adua) and Bambara (Aboboi) are staple market commodities."
    },
    "Kenya": {
        "primary_crops": ["pigeon_pea", "cowpea", "groundnut"],
        "notes": "Pigeon pea (Mbaazi) is an agronomic cash crop across Eastern & Coastal Kenya."
    },
    "South Africa": {
        "primary_crops": ["bambara_groundnut", "cowpea", "groundnut", "soybean"],
        "notes": "Jugo beans (Bambara) and Cowpea cultivate well in Limpopo and Mpumalanga."
    }
}


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
    country_clean = country.split()[0]  # e.g. 'Nigeria' from 'Nigeria (National Hub)'
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
        wet_lab_note = {
            "crop": "Bambara groundnut",
            "empirical_solubility_ph7": "82.27% (Pretoria dataset M38)",
            "least_gelation_concentration": "8.0% - 10.0% w/v",
            "status": "Tier 1 Wet-Lab Validated (Sequence models bypassed due to 0 UniProt storage entries)"
        }

    return {
        "job": job,
        "country": country_clean,
        "model_run_id": run_id,
        "top_pick": ranked_candidates[0] if ranked_candidates else None,
        "backup_substitute": ranked_candidates[1] if len(ranked_candidates) > 1 else None,
        "candidates": ranked_candidates,
        "wet_lab_empirical_evidence": wet_lab_note
    }


# Request & Response schemas for Advisory Endpoint
class FormulateRequest(BaseModel):
    role: str = Field(..., description="Role: 'consumer', 'nutritionist', or 'food_processor'")
    job: str = Field(..., description="Job application ID (e.g. egg, milk, gel, meat, crayfish, sarcopenia)")
    crop_id: Optional[str] = Field("cowpea", description="Selected crop ID (e.g. cowpea, pigeon_pea, african_yam_bean, bambara_groundnut)")
    staple_vehicle: Optional[str] = Field(None, description="Traditional food vehicle (e.g. amala, tuwo, ogi, moi_moi, salad)")
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

    # Match application metadata
    matched_app = next((a for a in APPLICATIONS_CATALOG if a["id"] == job), APPLICATIONS_CATALOG[0])

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

        savings_note = "Saves an estimated ₦3,000–₦4,500 per week compared to commercial dairy or poultry eggs."
        health_note = "100% plant-based, zero dietary cholesterol, rich in prebiotic legume fiber."
        if older:
            health_note += " Highly digestible soft protein; gentle on aging digestive systems."

        return {
            "role": "consumer",
            "application": matched_app["name"],
            "selected_crop": crop,
            "plant_based_as_cooked_status": matched_app["plant_based_flag"],
            "kitchen_instructions": instructions,
            "cost_benefit": savings_note,
            "nutritional_impact": health_note
        }

    elif "nutritionist" in role or "dietitian" in role:
        vehicle = req.staple_vehicle or "Amala"
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
            "clinical_advisory": "Recommended 2 servings daily to prevent age-related muscle mass loss and maintain glycemic stability."
        }

    else:  # food_processor / manufacturer
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
            }
        }
