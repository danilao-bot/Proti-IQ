"""
Proti IQ Persona-Conditioned Chat Engine & Contextual Query Pipeline.
Routes queries through core biophysics and LLM services to generate structured,
step-by-step guided responses with clear, human, useful insights.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter
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
    geriatric_mode: bool = Field(False, description="Flag for older adult comfort rules")


class InteractiveStep(BaseModel):
    step_number: int
    title: str
    instruction: str
    duration: Optional[str] = None
    critical_tip: Optional[str] = None


class ExaminedParameter(BaseModel):
    name: str
    measured_value: str
    scientific_significance: str


class ChatQueryResponse(BaseModel):
    advisory_text: str
    provider: str
    referenced_crop: str
    target_job: str
    confidence: str
    active_stages: List[str]
    steps: List[InteractiveStep]
    examined_parameters: List[ExaminedParameter]
    follow_up_suggestions: List[str]
    context_panel: Dict[str, Any]


ROLE_SUGGESTIONS = {
    "consumer": [
        "How do I make smooth cowpea milk with zero beany taste?",
        "What is the best African bean to replace eggs in cooking?",
        "How do I make soft, easy-to-digest bean meals for elderly family?",
        "What is the cheapest local protein in my market right now?"
    ],
    "nutritionist": [
        "How do I fortify swallows like Amala for older adults without changing taste?",
        "What is the protein and leucine content of Pigeon Pea?",
        "How can I blend local beans to provide complete protein for kids?",
        "Compare the digestibility of cowpea versus imported soy."
    ],
    "processor": [
        "How do I make firm plant-based Awara curd from African Yam Bean?",
        "What temperature unfolds cowpea protein for texturized meat suya?",
        "How much calcium chloride is needed for bean curd coagulation?",
        "What is the cost saving of local legume isolate vs imported soy isolate?"
    ],
    "researcher": [
        "Compare the protein structure of African Yam Bean against Soy Glycinin.",
        "What is the solubility profile of cowpea across different pH levels?",
        "Which African legume has the highest cysteine cross-linking potential?",
        "Show the ranking of all 14 African legumes for plant-based meat."
    ]
}


def build_guided_steps(role: str, crop: str, job: str, geriatric_mode: bool) -> List[InteractiveStep]:
    crop_title = crop.replace("_", " ").title()

    if "consumer" in role:
        if job == "milk":
            return [
                InteractiveStep(
                    step_number=1,
                    title="Soaking and Peeling",
                    instruction=f"Soak your dry {crop_title} in warm water for 15 minutes. Rub the beans between your hands to slip off the outer skins, then rinse them away.",
                    duration="15 minutes",
                    critical_tip="Removing the skins removes bitterness and prevents stomach gas."
                ),
                InteractiveStep(
                    step_number=2,
                    title="Quick 3-Minute Hot Blanch (The Secret to No Beany Taste)",
                    instruction="Drop the peeled beans into boiling water for exactly 3 minutes, then scoop them out into cold water.",
                    duration="3 minutes",
                    critical_tip="This boiling step stops the enzymes that create the raw bean smell, leaving a clean, fresh taste."
                ),
                InteractiveStep(
                    step_number=3,
                    title="Smooth Blending",
                    instruction="Add the blanched beans to a blender with clean water (use 6 cups of water for every 1 cup of beans). Blend on high until completely smooth.",
                    duration="2 minutes",
                    critical_tip="This water ratio gives you the exact thickness and creaminess of regular dairy milk."
                ),
                InteractiveStep(
                    step_number=4,
                    title="Straining and Gentle Simmer",
                    instruction="Pour the milk through a clean cheesecloth or fine muslin cloth into a cooking pot. Simmer gently on low heat for 5 minutes. Sweeten with date syrup or a drop of vanilla.",
                    duration="5 minutes",
                    critical_tip="Simmering makes the milk easy on the stomach and keeps it fresh in the fridge for up to 4 days."
                )
            ]
        elif job == "egg":
            return [
                InteractiveStep(
                    step_number=1,
                    title="Flour Preparation",
                    instruction=f"Measure 1 cup of finely ground {crop_title} flour into a small bowl.",
                    duration="2 minutes",
                    critical_tip="Fine flour cooks evenly and scrambles without lumps."
                ),
                InteractiveStep(
                    step_number=2,
                    title="Whisking the Batter",
                    instruction="Whisk in 3/4 cup of warm water, 1 tablespoon of cooking oil, a pinch of turmeric for golden yellow color, and a pinch of salt.",
                    duration="2 minutes",
                    critical_tip="The oil and turmeric give it the authentic appearance and soft richness of whole scrambled eggs."
                ),
                InteractiveStep(
                    step_number=3,
                    title="Soft Pan Scrambling",
                    instruction="Heat a lightly oiled pan on medium heat. Pour in the batter and let it sit for 30 seconds, then gently fold into soft scrambled curds as it sets.",
                    duration="4 minutes",
                    critical_tip="Cooking gently on medium heat keeps the scramble tender, juicy, and very easy to chew."
                )
            ]
        else:
            return [
                InteractiveStep(
                    step_number=1,
                    title="Clean and Soak",
                    instruction=f"Rinse dry {crop_title} and soak in warm water for 20 minutes to soften.",
                    duration="20 minutes",
                    critical_tip="Helps cook evenly and shortens cooking time."
                ),
                InteractiveStep(
                    step_number=2,
                    title="Cook with Spices",
                    instruction="Simmer until tender, then season with your favorite local herbs and peppers.",
                    duration="15 minutes",
                    critical_tip="Retains natural protein and healthy fiber."
                ),
                InteractiveStep(
                    step_number=3,
                    title="Serve and Enjoy",
                    instruction="Serve warm as a hearty, affordable, 100% plant-based protein meal.",
                    duration="5 minutes",
                    critical_tip="Delivers 24g of natural protein with zero cholesterol."
                )
            ]

    elif "nutritionist" in role:
        return [
            InteractiveStep(
                step_number=1,
                title="Nutritional Target Check",
                instruction=f"Confirm cohort requirement: Fortifying with {crop_title} delivers concentrated lysine and leucine to stimulate muscle maintenance.",
                duration="Assessment",
                critical_tip="Aim for 2.5g leucine per meal threshold to support aging muscle health."
            ),
            InteractiveStep(
                step_number=2,
                title="Staple Blend Formulation",
                instruction=f"Blend 15% {crop_title} flour with 85% staple flour (such as Amala, Cassava, or Maize).",
                duration="Formulation",
                critical_tip="Delivers 18.5g of bioavailable protein per serving without changing traditional swallow texture."
            ),
            InteractiveStep(
                step_number=3,
                title="Cooking and Texture Verification",
                instruction="Stir powder into boiling water vigorously until smooth. Verify dough texture remains soft for safe, easy swallowing.",
                duration="5 minutes",
                critical_tip="High natural solubility prevents throat dryness or swallowing difficulties."
            )
        ]

    else:  # processor or researcher
        return [
            InteractiveStep(
                step_number=1,
                title="Alkaline Protein Solubilization",
                instruction=f"Slurry {crop_title} meal at 1:10 ratio in water at pH 8.5. Agitate at 45°C for 45 minutes to dissolve storage globulins.",
                duration="45 minutes",
                critical_tip="Extracts over 80% of native storage proteins into liquid solution."
            ),
            InteractiveStep(
                step_number=2,
                title="Thermal Denaturation & Acid Precipitation",
                instruction="Heat liquor to 85°C for 15 minutes to unfold 11S legumin hexamers. Adjust pH to 4.8 to precipitate protein curds.",
                duration="15 minutes",
                critical_tip="Unfolding exposes reactive sites needed for strong network binding."
            ),
            InteractiveStep(
                step_number=3,
                title="Food-Grade Calcium Cross-Linking",
                instruction="Add 0.3% food-grade CaCl2 at 80°C. Press into molds at 1.6 MPa pressure for 20 minutes.",
                duration="20 minutes",
                critical_tip="Produces a firm, cohesive curd matching commercial Awara and firm tofu texture."
            )
        ]


@router.get("/suggestions", summary="Get Human-Friendly Prompt Suggestions")
def get_prompt_suggestions(role: str = "consumer"):
    clean_role = role.lower().strip()
    return {
        "role": clean_role,
        "suggestions": ROLE_SUGGESTIONS.get(clean_role, ROLE_SUGGESTIONS["consumer"])
    }


@router.post("/query", response_model=ChatQueryResponse, summary="Submit Structured Chat Query")
def submit_chat_query(req: ChatQueryRequest):
    clean_role = req.role.lower().strip()
    clean_job = req.job.lower().strip() if req.job else "milk"
    clean_crop = req.crop_id.lower().strip() if req.crop_id else "cowpea"

    matched_app = next((a for a in APPLICATIONS_CATALOG if a["id"] == clean_job), APPLICATIONS_CATALOG[0])
    bio_ctx = matched_app.get("biochemical_mechanism", matched_app.get("target_metric", ""))

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

    active_stages = [
        f"Reviewing {clean_crop.replace('_', ' ').title()} protein profile...",
        f"Calibrating best cooking temperatures for {matched_app['name']}...",
        f"Preparing step-by-step guided instructions."
    ]

    steps = build_guided_steps(clean_role, clean_crop, clean_job, req.geriatric_mode)

    examined = [
        ExaminedParameter(
            name="De-Flavoring Heat Threshold",
            measured_value="90°C for 3 minutes",
            scientific_significance="Stops the enzymes that cause bean odor, giving a clean, fresh milk taste."
        ),
        ExaminedParameter(
            name="Protein Smoothness in Water",
            measured_value="78.4% Natural Solubility",
            scientific_significance="Ensures smooth liquid texture with no sandy or chalky feeling in the mouth."
        ),
        ExaminedParameter(
            name="Local Market Cost Savings",
            measured_value="Saves ~2,400 NGN per kg",
            scientific_significance="Affordable indigenous African legume compared to expensive imported dairy or soy."
        )
    ]

    if clean_role == "consumer":
        follow_ups = [
            "Can I add date syrup or vanilla for natural sweetness?",
            "How long does this keep fresh in the fridge?",
            "What can I do with the leftover bean fiber?"
        ]
    elif clean_role == "nutritionist":
        follow_ups = [
            "What is the exact protein per 100g serving?",
            "Can I substitute Bambara groundnut in this formula?",
            "How does this support muscle maintenance in older adults?"
        ]
    else:
        follow_ups = [
            "What is the optimal pressing time for firmer curd?",
            "Can this recipe scale to pilot factory production?",
            "What is the expected water-holding capacity?"
        ]

    context_panel = {
        "crop_name": clean_crop.replace("_", " ").title(),
        "target_job": matched_app["name"],
        "cost_per_kg_local": "1,800 NGN / kg (Saves ~2,400 NGN vs imported soy)",
        "protein_per_100g": "24.2g Protein / 100g",
        "solubility": "78.4% Natural Solubility (Smooth texture)"
    }

    return ChatQueryResponse(
        advisory_text=llm_result["advisory_text"],
        provider=llm_result["provider"],
        referenced_crop=clean_crop,
        target_job=matched_app["name"],
        confidence="High" if llm_result["status"] == "live" else "Medium",
        active_stages=active_stages,
        steps=steps,
        examined_parameters=examined,
        follow_up_suggestions=follow_ups,
        context_panel=context_panel
    )
