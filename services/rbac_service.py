"""
Proti IQ RBAC (Role-Based Access Control) Resolution Service.
Determines locked user personas deterministically based on onboarding inputs.
"""

from typing import Dict, Any, Tuple


ROLE_METADATA = {
    "consumer": {
        "title": "Consumer / Caregiver",
        "badge": "Community & Kitchen",
        "description": "Pragmatic kitchen protocols, enzyme de-flavoring, local market prices, and geriatric digestive safety.",
        "accessible_routes": ["hub", "crops"],
        "export_type": "Recipe Card",
        "min_body_font_size": "18px"
    },
    "nutritionist": {
        "title": "Clinical Nutritionist / Dietitian",
        "badge": "Clinical Nutrition",
        "description": "Leucine thresholds, PDCAAS/DIAAS amino acid balance, fortification sliders, and dietary advisory exports.",
        "accessible_routes": ["hub", "crops", "evidence"],
        "export_type": "Dietary Advisory Note",
        "min_body_font_size": "16px"
    },
    "processor": {
        "title": "Industrial Processor / R&D Engineer",
        "badge": "Industrial Manufacturing",
        "description": "Denaturation windows, isoelectric precipitation, CaCl2 cross-linking, and Technical Data Sheets.",
        "accessible_routes": ["hub", "crops", "evidence", "structure"],
        "export_type": "Technical Data Sheet (TDS)",
        "min_body_font_size": "16px"
    },
    "researcher": {
        "title": "Research Scientist / Academic",
        "badge": "Biophysics & Molecular Research",
        "description": "1,280-dim ESM-2 vectors, AlphaFold PDB coordinate structures, Pretoria wet-lab raw titrations, and complete matrices.",
        "accessible_routes": ["hub", "crops", "evidence", "structure", "data"],
        "export_type": "Raw Scientific Data Export",
        "min_body_font_size": "16px"
    }
}


def resolve_role(age: int, mission: str, scale: str) -> Dict[str, Any]:
    """
    Deterministically computes user role and flags from onboarding context.
    Strictly zero guessing; validates against standard operational personas.
    """
    mission_clean = mission.lower().strip()
    scale_clean = scale.lower().strip()

    geriatric_mode = (age >= 50)
    contradiction = False

    # Check for direct contradictions
    if "consumer" in mission_clean and ("factory" in scale_clean or "laboratory" in scale_clean):
        contradiction = True
    elif "researcher" in mission_clean and "household" in scale_clean:
        contradiction = True

    # Deterministic mapping
    if "research" in mission_clean or "scientist" in mission_clean or "laboratory" in scale_clean:
        role = "researcher"
    elif "processor" in mission_clean or "manufactur" in mission_clean or "factory" in scale_clean:
        role = "processor"
    elif "nutrition" in mission_clean or "diet" in mission_clean or "clinical" in scale_clean:
        role = "nutritionist"
    else:
        role = "consumer"

    meta = ROLE_METADATA.get(role, ROLE_METADATA["consumer"])

    return {
        "assigned_role": role,
        "role_title": meta["title"],
        "role_badge": meta["badge"],
        "geriatric_mode": geriatric_mode,
        "contradiction": contradiction,
        "accessible_routes": meta["accessible_routes"],
        "export_type": meta["export_type"],
        "description": meta["description"]
    }
