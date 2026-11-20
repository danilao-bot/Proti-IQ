"""
Detailed Results and Explainability Page for Proti IQ.
"""

import json
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ui.components.header import render_app_header
from ui.components.badges import render_confidence_badge, render_screening_flags
from api.db import SessionLocal, Ranking, Crop, Protein, ModelRun

st.set_page_config(page_title="Results and Explainability | Proti IQ", layout="wide")
render_app_header("Screening Results and Explainability", "Component-level breakdown of biological drivers")

db = SessionLocal()
try:
    jobs = ["egg", "gel", "milk"]
    selected_job = st.selectbox("Select Functional Job:", jobs, format_func=lambda x: f"Job: {x.upper()}")

    latest_run = db.query(ModelRun).order_by(ModelRun.created_at.desc()).first()
    run_id = latest_run.id if latest_run else None

    query = db.query(Ranking).filter(Ranking.job == selected_job)
    if run_id:
        query = query.filter(Ranking.run_id == run_id)
    rankings = query.order_by(Ranking.score.desc()).all()

    if not rankings:
        st.warning(f"No ranking data available for job '{selected_job}'. Run the pipeline CLI first.")
    else:
        # Group by crop
        seen = set()
        unique_ranks = []
        for r in rankings:
            if r.crop_id not in seen:
                seen.add(r.crop_id)
                unique_ranks.append(r)

        # Plotly Bar Chart
        df_chart = []
        for r in unique_ranks:
            crop = db.query(Crop).filter(Crop.id == r.crop_id).first()
            df_chart.append({
                "Crop": crop.common_name if crop else r.crop_id,
                "Score": r.score,
                "Confidence": r.confidence,
            })

        df = pd.DataFrame(df_chart)
        fig = px.bar(
            df,
            x="Score",
            y="Crop",
            orientation="h",
            color="Score",
            color_continuous_scale="Viridis",
            title=f"Recommended Candidate Shortlist — Biophysical Similarity Scores for {selected_job.upper()}",
            text="Score",
            labels={"Score": "Biophysical Similarity Score (%)", "Crop": "Candidate Crop"}
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=350)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Biological Explainability Breakdown")

        for r in unique_ranks:
            crop = db.query(Crop).filter(Crop.id == r.crop_id).first()
            prot = db.query(Protein).filter(Protein.id == r.protein_id).first()
            contributions = json.loads(r.contributions_json) if r.contributions_json else {}
            flags = json.loads(r.flags_json) if r.flags_json else []

            with st.expander(f"**Candidate: {crop.common_name if crop else r.crop_id}** — Biophysical Similarity Score: {r.score:.1f}%", expanded=True):
                col_a, col_b = st.columns([2, 1])

                with col_a:
                    st.markdown(f"**Best Representative Protein:** `{prot.accession if prot else 'N/A'}` — *{prot.name if prot else 'Unknown'}*")
                    st.markdown(f"**Storage Family Classification:** `{prot.family if prot else 'Unknown'}`")

                    # Contribution metrics
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Embedding Similarity", f"{contributions.get('embedding_similarity', 0)}%")
                    c2.metric("Family Match", f"{contributions.get('family_match', 0)}%")
                    c3.metric("Physicochemical Match", f"{contributions.get('physicochemical_match', 0)}%")

                    c4, c5 = st.columns(2)
                    c4.metric("Sequence Alignment Identity", f"{contributions.get('sequence_identity', 0)}%")
                    if selected_job == "gel":
                        c5.metric("Cysteine Fraction (Cross-linking)", f"{contributions.get('cysteine_fraction', 0)}%")
                    else:
                        c5.metric("Solubility Index", f"{contributions.get('solubility_proxy', 0)}%")

                with col_b:
                    st.markdown("**Confidence Assessment:**")
                    render_confidence_badge(r.confidence)
                    for reason in contributions.get("confidence_reasons", []):
                        st.caption(f"• {reason}")

                    st.markdown("**Screening Flags:**")
                    render_screening_flags(flags)

        st.markdown("---")
        st.info("💡 **Ready to take these biophysical similarity scores to commercial production?** Open **6_Lab_Brief** in the sidebar to view the **Path B Food Science Formulation Roadmap** (pH-shifting, ionic cross-linking, and target benchmark metrics to beat).")
finally:
    db.close()
