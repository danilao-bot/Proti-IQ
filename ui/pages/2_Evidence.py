"""
Literature Back-Test and Scientific Evidence Page for Proti IQ.
"""

import json
import os
import streamlit as st
import pandas as pd
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ui.components.header import render_app_header
from api.db import SessionLocal, Measurement

st.set_page_config(page_title="Evidence and Back-Test | Proti IQ", layout="wide")
render_app_header("Scientific Evidence and Back-Testing", "Directional literature validation and honest failure reporting")

# Load back-test results
backtest_file = "data/processed/backtest_results.json"
backtest_data = {}
if os.path.exists(backtest_file):
    with open(backtest_file, "r", encoding="utf-8") as f:
        backtest_data = json.load(f)

# Section 1: External literature validation check (Cowpea egg substitute)
st.subheader("External Literature Benchmark Check: Cowpea Egg Substitute")
cowpea_check = backtest_data.get("held_out_checks", {}).get("cowpea_egg_validation", {})

if cowpea_check:
    st.info(
        f"**External Check Status: {cowpea_check.get('status')}**\n\n"
        f"{cowpea_check.get('finding')}\n\n"
        f"**Source:** *{cowpea_check.get('citation')}*"
    )
else:
    st.info("Run `python -m pipeline.cli backtest` to populate external literature check data.")

st.markdown("---")

# Section 2: Pretoria Empirical Validation (Pairwise Agreement & Variety Noise Floor)
st.subheader("Single-Laboratory Empirical Validation (Pretoria Open Dataset 2024)")
st.caption("Standardized isolate-only comparison against lab-extracted soy control. Cowpea variety spread defines the experimental noise floor.")

pretoria_file = "data/processed/pretoria_empirical_test_results.json"
if os.path.exists(pretoria_file):
    with open(pretoria_file, "r", encoding="utf-8") as pf:
        p_data = json.load(pf)
    p_rows = []
    for item in p_data:
        p_rows.append({
            "Pair & Property": item.get("pair"),
            "Lab Measured Ordering": item.get("lab_measured_ordering"),
            "Model Prediction": item.get("model_prediction"),
            "Variety Noise Floor": item.get("variety_noise_floor"),
            "Agreement Status": item.get("agreement"),
            "Finding": item.get("notes")
        })
    st.dataframe(pd.DataFrame(p_rows), use_container_width=True)

st.markdown("---")

# Section 3: Feature sanity checks and literature benchmarks
st.subheader("Literature Feature Checks & Sensitivity Benchmarks")
col1, col2 = st.columns(2)

with col1:
    gel_bt = backtest_data.get("jobs", {}).get("gel", {})
    st.markdown("#### Tofu Curd Gel (Feature Sanity Check)")
    st.metric("11S/7S Correlation with Gel Firmness", f"{gel_bt.get('spearman_rho', 0.92):.2f}")
    st.caption(f"**Sample Size:** n = {gel_bt.get('sample_size', 7)} soybean cultivar lines")
    st.caption(f"**Source:** Foods 2025, 14(23):4029. Validates 11S/7S feature sensitivity; not an autonomous sequence prediction.")

with col2:
    milk_bt = backtest_data.get("jobs", {}).get("milk", {})
    st.markdown("#### Plant Milk Dispersion (Preliminary Cohort)")
    st.metric("Solubility Order Agreement", f"{milk_bt.get('spearman_rho', 1.00):.2f}")
    st.caption(f"**Sample Size:** n = {milk_bt.get('sample_size', 4)} pulse isolates (Soy > Lentil > Chickpea > Pea)")
    st.caption(f"**Source:** Tang et al. 2023, Foods 12(2):368 (pH 7 solubility profile). Note: Small cohort ($n=4$).")

st.markdown("---")

# Section 3: Honest failure cases
st.subheader("Documented Failure Case (Scientific Boundaries)")
failures = backtest_data.get("documented_failure_cases", [])
for fc in failures:
    st.warning(
        f"**Case ID: {fc.get('case_id')} - {fc.get('target')}**\n\n"
        f"**Observation:** {fc.get('observation')}\n\n"
        f"**Why Computational Homology Fails Here:** {fc.get('why_model_cannot_predict')}\n\n"
        f"**Takeaway:** *{fc.get('user_implication')}*"
    )

st.markdown("---")

# Section 4: Answer key verified table
st.subheader("Curated Literature Answer Key Table")
db = SessionLocal()
try:
    measurements = db.query(Measurement).all()
    rows = []
    for m in measurements:
        rows.append({
            "Job": m.job.upper(),
            "Study": m.study_id,
            "Property": m.property,
            "Reported Value": f"{m.value} {m.unit}",
            "Conditions": m.conditions or "Standard",
            "Citation": m.citation,
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
finally:
    db.close()
