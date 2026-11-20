"""
Lab-First Brief & Processing Optimization (Path B)
Translates In-Silico Screening into Food Science Laboratory Roadmaps.
Replaces speculative estimates with published empirical target benchmarks.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ui.components.header import render_app_header

st.set_page_config(page_title="Lab-First Brief & Processing | Proti IQ", layout="wide")
render_app_header("Lab-First Brief & Processing Roadmap", "Path B: Formulation protocols to bridge biophysical screening to commercial parity")

st.markdown("""
### The Proti IQ Formulation Paradigm
> **"We are not trying to clone foreign soy or mung bean. We are Africanizing alternative proteins."**
> 
> Powered by Meta's **ESM-2 650M Transformer embeddings**, Proti IQ screens the **native genetic architecture** of Nigerian crops. 
> In industrial food processing, **raw unformulated protein is never used directly**. Standard food-grade processing levers (pH-shifting, thermal exposure, and divalent salt cross-linking) are applied to achieve target functional texture and stability.
""")

jobs_options = [
    "Select a Functional Job...",
    "Heat-Set Plant-Based Egg Gel (7S Vicilin)",
    "Coagulated Curd Gel / Tofu (11S Legumin)",
    "Colloidal Plant-Based Milk"
]

selected_job_view = st.selectbox(
    "Choose Functional Food Application to View Lab Protocol:",
    jobs_options,
    index=0
)

if selected_job_view == "Select a Functional Job...":
    st.info("Select a functional application above to inspect the biochemical mechanism, target benchmark to beat, and standard wet-lab protocol.")

    st.markdown("---")
    st.subheader("Overview of Recommended Candidate Shortlists")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("#### 1. Heat-Set Egg Gel")
        st.markdown("- **Benchmark:** Mung bean 8S Vicilin (`A0A1S3VZW2`)")
        st.markdown("- **Target to Beat:** Rupture Force ~0.8 N, Springiness >85%")
        st.markdown("- **Recommended Shortlist:**")
        st.markdown("  1. Pigeon pea (**87.4%** similarity)")
        st.markdown("  2. Cowpea (**85.1%** similarity)")
        st.markdown("  3. Groundnut (**85.1%** similarity)")
        st.markdown("  4. African yam bean (**82.6%** similarity)")

    with col_b:
        st.markdown("#### 2. Coagulated Curd / Tofu")
        st.markdown("- **Benchmark:** Soy Glycinin G4 (`P02858`)")
        st.markdown("- **Target to Beat:** Breaking Stress 1.2–1.5 N")
        st.markdown("- **Recommended Shortlist:**")
        st.markdown("  1. African yam bean (**88.5%** similarity)")
        st.markdown("  2. Pigeon pea (**87.9%** similarity)")
        st.markdown("  3. Cowpea (**87.8%** similarity)")
        st.markdown("  4. Groundnut (**87.1%** similarity)")

    with col_c:
        st.markdown("#### 3. Colloidal Plant Milk")
        st.markdown("- **Benchmark:** Soy Beta-conglycinin (`P11827`)")
        st.markdown("- **Target to Beat:** Stability >90% at 7d, pH 7 Sol. >80%")
        st.markdown("- **Recommended Shortlist:**")
        st.markdown("  1. Pigeon pea (**80.6%** similarity)")
        st.markdown("  2. Cowpea (**79.1%** similarity; 82.6% wet-lab sol.)")
        st.markdown("  3. Bambara groundnut (**82.3%** wet-lab solubility)")
        st.markdown("  4. Groundnut (**76.6%** similarity)")

elif selected_job_view == "Heat-Set Plant-Based Egg Gel (7S Vicilin)":
    st.subheader("Heat-Set Plant-Based Egg Gel Protocol")
    st.caption("Benchmark: Mung Bean 8S Vicilin (A0A1S3VZW2) | Gold Standard: JUST Egg")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(r"""
        #### Biochemical Mechanism
        * **7S Vicilin Thermal Gelation:** The JUST Egg industrial formulation relies on mung bean 8S vicilin unfolding at $72^\circ\text{C}$ to form an elastic, scramblable gel matrix without rubberiness.
        * **Why Indigenous Vicilins Qualify:** African yam bean and Pigeon pea beta-conglycinin 7S trimers exhibit cupin barrel fold conservation, achieving >85% ESM-2 biophysical representation alignment with mung bean vicilin.
        
        #### Standardized Wet-Lab Protocol
        1. **pH-Shift Solubilization:** Extract protein isolate at pH 9.5–10.0 (partially unfolding native globulin), then neutralize back to pH 7.2.
        2. **Concentration Calibration:** Formulate at 10%–12% w/v protein isolate dispersion.
        3. **Emulsion Coupling:** Blend with 3% vegetable oil and 0.2% sunflower lecithin for fat mouthfeel.
        4. **Thermal Setting:** Cook in pan or water bath at $85^\circ\text{C}$ for 8–10 minutes.
        
        #### Published Literature Benchmark to Beat
        * **Rupture Force:** **~0.8 N** (*Brishti et al., Food Chemistry 2017*).
        * **Springiness:** **>85%** (*US Patent 10,820,612 B2*).
        * **Gelation Temperature Window:** $72^\circ\text{C} - 82^\circ\text{C}$.
        """)
    with col2:
        st.markdown("#### Recommended Candidate Shortlist (Native ESM-2 Similarity)")
        fig2 = go.Figure(go.Bar(
            x=["Pigeon pea", "Cowpea", "Groundnut", "African yam bean"],
            y=[87.4, 85.1, 85.1, 82.6],
            name="ESM-2 Biophysical Similarity Score (%)",
            marker_color="#1f77b4",
            text=[87.4, 85.1, 85.1, 82.6],
            textposition="auto"
        ))
        fig2.update_layout(
            yaxis=dict(title="Biophysical Similarity Score (%)", range=[0, 100]),
            height=340,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.info("Laboratory Action: Screen top candidates on benchtop texture analyzer against the 0.8 N rupture force benchmark.")

elif selected_job_view == "Coagulated Curd Gel / Tofu (11S Legumin)":
    st.subheader("Tofu-Type Curd Coagulation Protocol")
    st.caption("Benchmark: Soybean 11S Glycinin G4 (P02858) | Gold Standard: Commercial Firm Tofu")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(r"""
        #### Biochemical Mechanism
        * **11S Legumin Hexamer Cross-linking:** Soy tofu coagulates when divalent cations ($\text{Ca}^{2+}$) bridge negative carboxyl groups on adjacent glycinin subunits, while thermal heating ($85^\circ\text{C}$) exposes buried cysteine sulfhydryl groups for intermolecular $-S-S-$ cross-linking.
        * **Why Indigenous Legumins Qualify:** Groundnut arachin and African yam bean legumin possess dense clusters of acidic amino acids (Asp, Glu) and intact cysteine dyads matching soy glycinin G4.
        
        #### Standardized Wet-Lab Protocol
        1. **Alkaline Extraction:** Disperse de-fatted meal in water (1:10 w/v) at pH 8.5–9.0 ($45^\circ\text{C}$, 45 min) to maximize 11S globulin yield.
        2. **Thermal Unfolding:** Heat recovered curd liquor to $85^\circ\text{C}$ for 15 min to expose hydrophobic domains.
        3. **Ionic Coagulation:** Add food-grade **0.3% w/v $\text{CaCl}_2$** (or 0.25% Calcium Sulfate $\text{CaSO}_4$) at $80^\circ\text{C}$.
        4. **Pressing:** Transfer curd to perforated mold; press at 15 kPa for 20 minutes.
        
        #### Published Literature Benchmark to Beat
        * **Breaking Stress / Firmness:** **1.2 – 1.5 N** (*Foods 2025*, 14(3), 412; *Breeding Science 2000*).
        * **Elastic Storage Modulus ($G'$):** $> 1200\text{ Pa}$.
        """)
    with col2:
        st.markdown("#### Recommended Candidate Shortlist (Native ESM-2 Similarity)")
        fig1 = go.Figure(go.Bar(
            x=["African yam bean", "Pigeon pea", "Cowpea", "Groundnut"],
            y=[88.5, 87.9, 87.8, 87.1],
            name="ESM-2 Biophysical Similarity Score (%)",
            marker_color="#2ca02c",
            text=[88.5, 87.9, 87.8, 87.1],
            textposition="auto"
        ))
        fig1.update_layout(
            yaxis=dict(title="Biophysical Similarity Score (%)", range=[0, 100]),
            height=340,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.info("Laboratory Action: Test 0.3% CaCl2 vs 0.25% CaSO4 with African yam bean and Pigeon pea curds to measure breaking stress.")

elif selected_job_view == "Colloidal Plant-Based Milk":
    st.subheader("Colloidal Plant-Based Milk Protocol")
    st.caption("Benchmark: Soybean 7S Beta-conglycinin alpha' (P11827) | Control: Commercial Soy Milk")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(r"""
        #### Biochemical Mechanism
        * **Colloidal Stability & Electrostatic Repulsion:** Plant milks phase-separate if protein net charge near neutral pH is too low. Cowpea and Pigeon pea vicilins exhibit strong negative electrostatic potential ($-18$ to $-28$ net charge at pH 7.0), maintaining electrostatic repulsion against droplet aggregation.
        * **Pretoria Wet-Lab Empirical Evidence:** Lab-extracted Cowpea isolate reaches **82.6% solubility** at pH 7.0, outperforming lab-extracted soy isolate (**75.3%**). Bambara groundnut reaches **82.3% solubility**.
        
        #### Standardized Wet-Lab Protocol
        1. **Thermal Lipoxygenase Blanching:** Blanch de-hulled seeds at $90^\circ\text{C}$ for 3 minutes to deactivate lipoxygenase enzymes (completely prevents beany hexanal off-flavors).
        2. **Colloidal Wet-Milling:** Mill at 1:8 seed-to-water ratio; homogenize in two stages (50 MPa / 10 MPa).
        3. **pH Buffering:** Buffer at pH 6.8–7.2 with 0.1% food-grade dipotassium phosphate ($\text{K}_2\text{HPO}_4$).
        
        #### Published Literature Benchmark to Beat
        * **Colloidal Stability Index:** **>90%** after 7 days refrigerated storage at $4^\circ\text{C}$ (*Tang et al., 2023*).
        * **Neutral pH Solubility:** **>80%** at pH 7.0 (*Pretoria Dataset 2024*).
        """)
    with col2:
        st.markdown("#### Recommended Candidate Shortlist (Native ESM-2 Similarity)")
        fig3 = go.Figure(go.Bar(
            x=["Pigeon pea", "Cowpea", "Groundnut", "African yam bean"],
            y=[80.6, 79.1, 76.6, 70.2],
            name="ESM-2 Biophysical Similarity Score (%)",
            marker_color="#ff7f0e",
            text=[80.6, 79.1, 76.6, 70.2],
            textposition="auto"
        ))
        fig3.update_layout(
            yaxis=dict(title="Biophysical Similarity Score (%)", range=[0, 100]),
            height=340,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.info("Laboratory Action: Verify lipoxygenase inactivation via spectrophotometric assay (234 nm conjugated diene hydroperoxides).")

st.markdown("---")
st.markdown("""
### Biochemistry Lead Assignment (Vivian)
* **Status:** Research protocol guide prepared in `docs/VIVIAN_PATH_B_RESEARCH_GUIDE.md`.
* **Action:** Vivian will validate the 5 research questions (isoelectric pI points, cysteine availability, divalent salts, lipoxygenase blanching, and Bambara starch fractionation) and conduct laboratory verification trials.
""")
