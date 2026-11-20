"""
Proti IQ — African Alternative-Protein Discovery Hub
Interactive marketplace connecting indigenous African crops to commercial animal-protein replacements,
traditional culinary applications, and clinical nutrition.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ui.components.header import render_app_header
from api.db import SessionLocal, Crop, Protein, Ranking, Measurement

st.set_page_config(
    page_title="Discovery Hub | Proti IQ",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_app_header("African Alternative-Protein Discovery Hub", "Pan-African platform transforming indigenous legumes into commercial animal-protein alternatives")

# ---------------------------------------------------------
# 1. Onboarding & Filter Bar
# ---------------------------------------------------------
st.markdown("### 1. Tailor Your Discovery Experience")

col_user, col_country, col_toggle = st.columns([1.2, 1, 1.2])

with col_user:
    user_role = st.selectbox(
        "Who are you?",
        ["Food Processor / Commercial Manufacturer", "Nutritionist / Dietitian", "Consumer or Caregiver"],
        index=0
    )

with col_country:
    country = st.selectbox(
        "Region / Country Filter:",
        ["Nigeria (National Hub)", "Ghana", "Kenya", "South Africa"],
        index=0
    )

with col_toggle:
    st.write("") # spacing
    older_person_mode = st.toggle("Older-Person / Sarcopenia Filter (Age 50+)", value=False)
    if older_person_mode:
        st.caption("Active: Prioritizing high-digestibility, low-viscosity proteins to combat sarcopenia and muscle loss.")

st.markdown("---")

# ---------------------------------------------------------
# 2. The Anchor "Big Three" vs Expanded Spectrum
# ---------------------------------------------------------
st.markdown("""
### 2. The Three Core Anchor Proof-Cases
These three categories serve as Proti IQ's **validated proof-cases**, backed by our **Meta ESM-2 650M Transformer engine** (348 curated storage globulins) and the **University of Pretoria wet-lab dataset**:
""")

anchor_col1, anchor_col2, anchor_col3 = st.columns(3)

with anchor_col1:
    st.markdown("#### 1. Plant-Based Egg")
    st.caption("Direct replacement for poultry eggs in cooking, scrambling, and baking.")
    st.markdown("**Foreign Benchmark:** Mung bean 8S Vicilin (`A0A1S3VZW2` — JUST Egg)")
    st.markdown("**Top African Crop:** **Pigeon pea (87.4%)** & **Cowpea (85.1%)**")
    st.markdown("**Cultural Meal Link:** Moi moi, Akara, breakfast scrambled egg")
    st.success("Target Metric: 0.8 N Rupture Force, >85% Springiness")

with anchor_col2:
    st.markdown("#### 2. Plant-Based Milk")
    st.caption("Direct replacement for cow milk, canned evaporated milk, and milk powders.")
    st.markdown("**Foreign Benchmark:** Soy 7S Beta-conglycinin (`P11827`)")
    st.markdown("**Top African Crop:** **Cowpea (82.6% wet-lab sol.)** & **Bambara (82.3%)**")
    st.markdown("**Cultural Meal Link:** Kunu Aya (Tigernut milk), Kunu Gyada, tea/coffee milk")
    st.success("Target Metric: Colloidal Stability >90% at 7 days, pH 7 Solubility >80%")

with anchor_col3:
    st.markdown("#### 3. Plant-Based Tofu / Curd (Awara)")
    st.caption("Direct replacement for meat chunks and Fulani cow cheese (Wagashi / Wara).")
    st.markdown("**Foreign Benchmark:** Soy 11S Glycinin G4 (`P02858`)")
    st.markdown("**Top African Crop:** **African yam bean (88.5%)** & **Pigeon pea (87.9%)**")
    st.markdown("**Cultural Meal Link:** Awara (Northern tofu), fried wara cubes, stew meat")
    st.success("Target Metric: Breaking Stress 1.2–1.5 N via 0.3% CaCl2 cross-linking")

st.markdown("---")

# ---------------------------------------------------------
# 3. Complete Menu of Animal Protein Alternatives
# ---------------------------------------------------------
st.markdown("### 3. Explore the Complete Pan-African Alternative-Protein Spectrum")
st.markdown("Select any animal protein alternative to reveal candidate African crops, biophysical rationale, cultural meal links, and direct substitutes:")

spectrum_options = [
    "Plant-Based Scrambled & Baking Egg (Replacing Chicken Egg)",
    "Plant-Based Milk & Dairy Drinks (Replacing Cow & Evaporated Milk)",
    "Plant-Based Curd & Cheese (Replacing Awara, Wagashi & Dairy Cheese)",
    "Plant-Based Suya & Beef Strips (Replacing Red Meat & Beef)",
    "Plant-Based Crayfish & Fish Seasoning (Replacing Dried Crayfish & Fish)",
    "Plant-Based Poultry & Chicken (Replacing Hard Chicken & Turkey)",
    "Plant-Based Yogurt & Fermented Milk (Replacing Dairy Nunu & Yogurt)",
    "Plant-Based Mayonnaise & Dressings (Replacing Egg Mayonnaise)",
    "Clinical Sarcopenia Swallows & Porridges (Combating Elderly Muscle Loss)"
]

selected_alt = st.selectbox("Select Alternative Protein Application:", spectrum_options, index=0)

# Master Data Dictionary for all applications
app_data = {
    "Plant-Based Scrambled & Baking Egg (Replacing Chicken Egg)": {
        "benchmark": "Mung bean 8S Vicilin (JUST Egg control)",
        "protein_type": "7S Vicilin trimeric storage globulin",
        "top_pick": "Pigeon pea (Cajanus cajan)",
        "top_score": "87.4% (ESM-2 Biophysical Similarity)",
        "substitute": "Cowpea (Vigna unguiculata) — 85.1% similarity",
        "mechanism": "Thermal unfolding at 72°C–80°C creates an elastic, scramblable gel matrix without rubbery hardness.",
        "meals": ["Moi moi (steamed bean pudding)", "Akara (whipped bean fritters)", "Breakfast egg scramble"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "availability": "High across Nigeria, Ghana, Kenya; dry-season drought tolerant",
        "older_person_note": "Excellent high-bioavailability soft protein; easy to chew for dentition-compromised elderly."
    },
    "Plant-Based Milk & Dairy Drinks (Replacing Cow & Evaporated Milk)": {
        "benchmark": "Soybean 7S Beta-conglycinin alpha'",
        "protein_type": "High net-negative charge soluble globulin (-18 to -28 mV)",
        "top_pick": "Cowpea (Vigna unguiculata)",
        "top_score": "82.6% Empirical Solubility at pH 7.0 (Pretoria Dataset M39)",
        "substitute": "Bambara groundnut (Vigna subterranea) — 82.3% wet-lab solubility",
        "mechanism": "Electrostatic repulsion at neutral pH maintains colloidal dispersion; 90°C blanching for 3 min completely deactivates lipoxygenase enzymes to prevent beany hexanal off-flavors.",
        "meals": ["Kunu Aya (Tigernut milk)", "Kunu Gyada (Groundnut milk)", "Breakfast tea and pap whitener"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "availability": "Widespread across West & Southern Africa",
        "older_person_note": "Lactose-free; prevents gastrointestinal distress common in lactose-intolerant African older adults."
    },
    "Plant-Based Curd & Cheese (Replacing Awara, Wagashi & Dairy Cheese)": {
        "benchmark": "Soybean 11S Glycinin G4",
        "protein_type": "11S Legumin hexamer with acidic/basic subunits",
        "top_pick": "African yam bean (Sphenostylis stenocarpa)",
        "top_score": "88.5% (ESM-2 Biophysical Similarity)",
        "substitute": "Pigeon pea (87.9%) or Groundnut arachin (87.1%)",
        "mechanism": "Divalent calcium ions (0.3% CaCl2) form salt bridges between negatively charged glutamate/aspartate residues, while 85°C heat triggers covalent intermolecular -S-S- disulfide cross-linking.",
        "meals": ["Awara (fried plant curd)", "Wagashi / Wara (Fulani cheese alternative)", "Soup meat substitute"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "availability": "Traditional to Eastern and Central Nigeria; high protein content (29%)",
        "older_person_note": "Firm yet tender curd; provides bioavailable calcium for bone density."
    },
    "Plant-Based Suya & Beef Strips (Replacing Red Meat & Beef)": {
        "benchmark": "Soy Textured Vegetable Protein (SPI Extrudate)",
        "protein_type": "High 11S/7S ratio with structural cysteine dyads",
        "top_pick": "African yam bean + Groundnut meal blend",
        "top_score": "88.5% biophysical match; high tensile shear modulus",
        "substitute": "Bambara groundnut press-cake (defatted)",
        "mechanism": "High-temperature twin-screw shear texturization (140°C–160°C) aligns globulins into fibrous parallel meat-like muscle strands that absorb spicy suya yaji pepper.",
        "meals": ["Beef Suya skewers", "Dried Kilishi strips", "Peppered meat pies", "Stew beef chunks"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "availability": "Abundant across all agro-ecological zones",
        "older_person_note": "Zero saturated animal fat, zero dietary cholesterol; protects cardiovascular health."
    },
    "Plant-Based Crayfish & Fish Seasoning (Replacing Dried Crayfish & Fish)": {
        "benchmark": "Dried River Crayfish & Smoked Bonga Fish Umami Profile",
        "protein_type": "Enzymatic and microbial peptide hydrolysate (<1 kDa)",
        "top_pick": "Fermented African Locust Bean (Parkia biglobosa — Iru / Dawadawa)",
        "top_score": "High naturally occurring free glutamic acid and sulfurous savory peptides",
        "substitute": "Fermented African yam bean or soy dawadawa",
        "mechanism": "Solid-state fermentation with Bacillus subtilis breaks storage proteins into short-chain umami peptides and glutamates, mimicking the savory savory punch of dried crayfish without seafood allergens.",
        "meals": ["Egusi soup", "Ogbono soup", "Efo riro", "Gbegiri soup", "Jollof rice seasoning"],
        "plant_based_flag": "100% Plant-Based (Traditional umami secret of West Africa)",
        "availability": "Widespread in savannas across West Africa",
        "older_person_note": "Provides intense savory flavor with 60% less sodium than synthetic MSG/Maggi cubes, helping manage hypertension."
    },
    "Plant-Based Poultry & Chicken (Replacing Hard Chicken & Turkey)": {
        "benchmark": "Extruded Wheat/Soy High-Moisture Meat Analog (HMMA)",
        "protein_type": "Tensile fibrous 11S globulin fraction",
        "top_pick": "Pigeon pea isolate (87.9% 11S alignment)",
        "top_score": "87.4% similarity; pale cream color matching poultry meat",
        "substitute": "Cowpea white isolate",
        "mechanism": "Moisture extrusion at 55% hydration creates pale, tender delaminating fibers that tear like chicken breast.",
        "meals": ["Fried stew chicken", "Chicken pepper soup", "Asun-style spiced chunks"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "availability": "Widely available in dry grain markets",
        "older_person_note": "Easily digestible lean protein."
    },
    "Plant-Based Yogurt & Fermented Milk (Replacing Dairy Nunu & Yogurt)": {
        "benchmark": "Dairy Casein Acid-Coagulated Gel",
        "protein_type": "Acid-tolerant globulin with high water-holding capacity",
        "top_pick": "Bambara groundnut (Vigna subterranea)",
        "top_score": "82.3% solubility, Least Gelation Concentration 8.0% w/v",
        "substitute": "Cowpea isolate buffered at pH 6.8",
        "mechanism": "Lactic acid fermentation drops pH from 6.8 to 4.5, inducing controlled isoelectric aggregation into a smooth, spoonable curd without wheying-off (syneresis).",
        "meals": ["Fura da Nunu (millet dumplings in fermented milk)", "Spoonable plant yogurt"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "availability": "Semi-arid northern and eastern Nigeria, Ghana, Southern Africa",
        "older_person_note": "Contains live probiotic lactic cultures that improve gut microbiome and nutrient absorption in seniors."
    },
    "Plant-Based Mayonnaise & Dressings (Replacing Egg Mayonnaise)": {
        "benchmark": "Commercial Egg-Yolk Mayonnaise (70% oil emulsion)",
        "protein_type": "Amphiphilic surface-active globulin",
        "top_pick": "Groundnut conarachin (Arachis hypogaea)",
        "top_score": "85.1% ESM-2 similarity; superior oil-holding capacity",
        "substitute": "Pigeon pea 7S vicilin fraction",
        "mechanism": "Interfacial protein layer encapsulates micro-droplets of vegetable oil, preventing droplet coalescence for over 12 months ambient storage.",
        "meals": ["Nigerian salad dressing (Heinz/Bama style)", "Sandwich spread", "Shawarma sauce"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "availability": "Leading cash crop across Northern Nigeria, Senegal, Sudan",
        "older_person_note": "Cholesterol-free emulsion delivering heart-healthy monounsaturated fatty acids."
    },
    "Clinical Sarcopenia Swallows & Porridges (Combating Elderly Muscle Loss)": {
        "benchmark": "Medical Whey Protein Isolate (Oral Nutritional Supplement)",
        "protein_type": "Partially enzymatically hydrolyzed peptide (<5 kDa)",
        "top_pick": "Cowpea + Pigeon pea hydrolysate (Papain-digested)",
        "top_score": "Delivers 18g protein per 100g swallow without increasing paste viscosity",
        "substitute": "Bambara groundnut flour blend",
        "mechanism": "Mild enzymatic cleavage (DH 5–8%) reduces molecular weight, allowing high protein incorporation into traditional starch swallows (Amala, Tuwo, Fufu) and weaning porridges (Ogi/Akamu) without altering traditional texture.",
        "meals": ["Protein-fortified Amala", "Fortified Tuwo Shinkafa", "Fortified Ogi / Akamu porridge"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "availability": "Widespread local staple flours",
        "older_person_note": "CRITICAL: Direct solution for Africa's 189M older adults who suffer from sarcopenia due to eating 90% carbohydrate swallows."
    }
}

detail = app_data[selected_alt]

# Render Deep Dive Card
st.subheader(f"Application Profile: {selected_alt.split('(')[0].strip()}")

col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.markdown(f"**Target Animal Protein to Replace:** `{selected_alt.split('(')[-1].replace(')', '')}`")
    st.markdown(f"**Foreign Commercial Benchmark:** `{detail['benchmark']}`")
    st.markdown(f"**Required Protein Biophysics:** `{detail['protein_type']}`")
    st.markdown(f"**Biochemical Mechanism:** {detail['mechanism']}")

    st.markdown("---")
    st.markdown("#### Cultural African Dishes & Applications")
    for dish in detail["meals"]:
        st.markdown(f"- **{dish}**")
    st.caption(f"Dietary Status: {detail['plant_based_flag']}")

with col_right:
    st.markdown("#### Crop Selection & Substitution Engine")
    st.metric("Primary Recommended African Crop", detail["top_pick"], detail["top_score"])
    st.info(f"**Backup Regional Substitute:** {detail['substitute']}")
    st.markdown(f"**Agronomic Availability:** {detail['availability']}")

    if older_person_mode or user_role == "Nutritionist / Dietitian":
        st.warning(f"**Clinical Nutritionist Guidance:** {detail['older_person_note']}")

# Link to Lab Brief
st.markdown("---")
st.markdown("""
**Ready to test this formulation in the laboratory?**  
Navigate to **6_Lab_Brief** in the sidebar to review the precise **Path B Food Science Roadmap** (temperatures, pH-shifting regimes, and food-grade ionic salt cross-linking).
""")
