"""
Proti IQ — Web Application Home Page
3-Click Decision-Support Interface for Nigerian Legume Protein Functional Screening.
Professional design with zero emojis.
"""

import streamlit as st
import httpx
import os
import sys

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ui.components.header import render_app_header
from ui.components.badges import render_confidence_badge, render_screening_flags
from api.db import SessionLocal, Ranking, Protein, Crop, ModelRun

st.set_page_config(
    page_title="Proti IQ | Legume Protein Screening",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_app_header("Alternative-Protein Screening", "Hack the Fork Nigeria 2026 - Challenge 1")

# Sidebar Status & Environment
st.sidebar.title("Proti IQ")
st.sidebar.markdown("**Decision-support for Nigerian food developers.**")
st.sidebar.markdown("---")
st.sidebar.caption("System Status: **Ready (Offline-Capable)**")
st.sidebar.caption("Snapshot ID: `snapshot_nov2026`")
st.sidebar.caption("Protein Model: `Meta ESM-2 650M (1280-D)`")

# Introduction Section
st.markdown(
    """
    ### Problem Statement
    Nigerian food startups and researchers seeking to formulate plant-based egg, milk, or tofu 
    from local crops (cowpea, Bambara groundnut, pigeon pea) face expensive trial-and-error. 
    **Proti IQ evaluates seed storage protein biophysics and deep language model representations 
    to rank which crops deserve lab-testing first.**
    
    > **New:** Explore the **African Alternative-Protein Discovery Hub** in the left sidebar (`0_Discovery_Hub`) 
    > to view the complete pan-African menu of alternatives (plant-based egg, milk, curd/cheese, suya meat, crayfish umami, and clinical sarcopenia swallows) with user onboarding and older-person filters.
    """
)

st.markdown("---")

# Step 1: Choose Application Job
st.subheader("Step 1: Choose Target Food Application")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Plant-Based Egg")
    st.caption("Thermal coagulation and heat-set network formation resembling scrambled or cooked egg.")
    egg_selected = st.button("Select Egg Job", use_container_width=True)

with col2:
    st.markdown("#### Tofu-Type Gel")
    st.caption("Coagulant/salt-induced firm curd network driven by 11S legumin hexamers and disulfide bonds.")
    gel_selected = st.button("Select Tofu Gel Job", use_container_width=True)

with col3:
    st.markdown("#### Plant Milk")
    st.caption("Neutral-pH colloidal solubility, low sedimentation, and emulsification stability.")
    milk_selected = st.button("Select Plant Milk Job", use_container_width=True)

if "selected_job" not in st.session_state:
    st.session_state["selected_job"] = "egg"

if egg_selected:
    st.session_state["selected_job"] = "egg"
elif gel_selected:
    st.session_state["selected_job"] = "gel"
elif milk_selected:
    st.session_state["selected_job"] = "milk"

active_job = st.session_state["selected_job"]
st.success(f"Active Job Selection: {active_job.upper()}")

# Step 2: Choose Reference Benchmark
st.markdown("---")
st.subheader("Step 2: Choose Reference Benchmark Crop")

bm_options = {
    "mung_bean": "Mung bean (Vigna radiata) - Industrial benchmark for plant egg (e.g. JUST Egg)",
    "soy": "Soybean (Glycine max) - Benchmark for tofu curd and plant milk",
    "pea": "Field pea (Pisum sativum) - Secondary benchmark; lower solubility anchor",
}

default_bm = "mung_bean" if active_job == "egg" else "soy"
selected_bm = st.selectbox(
    "Benchmark Reference Protein:",
    options=list(bm_options.keys()),
    format_func=lambda x: bm_options[x],
    index=0 if default_bm == "mung_bean" else 1,
)

# Step 3: Run Ranking
st.markdown("---")
st.subheader("Step 3: Generate Screening Ranking")

if st.button("Rank Indigenous Nigerian Legumes", type="primary", use_container_width=True):
    with st.spinner("Analyzing protein language embeddings and biophysical features..."):
        # Query local database
        db = SessionLocal()
        try:
            rankings = (
                db.query(Ranking)
                .filter(Ranking.job == active_job, Ranking.benchmark_id == selected_bm)
                .order_by(Ranking.score.desc())
                .all()
            )

            if not rankings:
                st.warning("No precomputed rankings found. Please run the pipeline CLI first.")
            else:
                st.session_state["latest_rankings"] = rankings
                st.session_state["current_job"] = active_job
                st.session_state["current_bm"] = selected_bm
                st.rerun()
        finally:
            db.close()

# Display Results if available
if "latest_rankings" in st.session_state:
    st.markdown("### Candidate Screening Leaderboard")
    rankings = st.session_state["latest_rankings"]
    db = SessionLocal()

    try:
        seen_crops = set()
        table_rows = []
        for r in rankings:
            if r.crop_id in seen_crops:
                continue
            seen_crops.add(r.crop_id)

            crop = db.query(Crop).filter(Crop.id == r.crop_id).first()
            prot = db.query(Protein).filter(Protein.id == r.protein_id).first()

            table_rows.append({
                "Rank": len(seen_crops),
                "Crop": crop.common_name if crop else r.crop_id,
                "Scientific Name": crop.scientific_name if crop else "",
                "Storage Family": prot.family if prot else "Other",
                "Suitability Likelihood Score": f"{r.score:.1f} / 100",
                "Confidence": r.confidence,
                "Best Accession": prot.accession if prot else "",
            })

        st.dataframe(table_rows, use_container_width=True)

        st.info("Open the Results and Breakdown page in the left navigation for component drivers, or Evidence to review the literature back-test.")
    finally:
        db.close()
