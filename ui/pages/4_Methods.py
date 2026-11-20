"""
Scientific Methodology, Limitations, and Governance Page for Proti IQ.
"""

import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ui.components.header import render_app_header

st.set_page_config(page_title="Methodology and Limitations | Proti IQ", layout="wide")
render_app_header("Methodology, Limitations and Governance", "Transparent computational framework and ethical boundaries")

tab1, tab2, tab3 = st.tabs(["Scientific Methodology", "Limitations and Boundaries", "Governance and Privacy"])

with tab1:
    st.markdown(
        r"""
        ### Multi-Criteria Functional Scoring Framework
        Proti IQ evaluates seed storage proteins using a multi-representation computational pipeline:
        
        1. **Deep Protein Language Model Embeddings (ESM-2 8M):**  
           Captures evolutionary conservation and structural topology beyond primary sequence alone.
        2. **Biophysical Feature Profiling (Biopython):**  
           Isoelectric point ($pI$), net molecular charge at pH 7.0, grand average of hydropathicity (GRAVY), and cysteine fraction ($N_{\\text{Cys}} / L$).
        3. **Restricted Storage Family Classification:**  
           Strict alignment between homologous protein classes (e.g. 7S vicilin for egg, 11S legumin for curd/tofu).
        4. **Pairwise Sequence Alignment Identity:**  
           Global alignment with BLOSUM62 scoring matrix against proven industrial benchmarks.
        
        $$\\text{Score} = 100 \\times \\sum_i w_i \\cdot S_i$$
        """
    )

with tab2:
    st.markdown(
        """
        ### Explicit Scope Boundaries & Non-Negotiable Limits
        - **Likelihoods vs Measurements:** Scores are in-silico screening metrics, not empirical laboratory measurements or taste guarantees.
        - **Food Matrix Effects:** Industrial processing (pH-shifting, shear, heat, salt concentration) drastically modifies protein conformations.
        - **AlphaFold In-Silico Models:** Structural models are machine-learning predictions from AlphaFold DB; disordered regions carry low pLDDT.
        - **Screening Flags:** Allergen and protease-inhibitor flags are initial indicators from UniProt annotations, not clinical or toxicological clearances.
        - **Indigenous Crop Data Scarcity:** Several orphan African legumes possess limited reviewed Swiss-Prot sequences, reflected in visible Low Confidence badges.
        """
    )

with tab3:
    st.markdown(
        """
        ### Data Privacy & Compliance Statement
        - **Zero Personal Data Collection:** Proti IQ does not collect names, email addresses, payment information, or IP logs.
        - **No Tracking Cookies:** The application uses strictly functional session cookies required for UI interaction.
        - **Open Access Compliance:** All biological database queries utilize open APIs under Creative Commons Attribution (CC BY 4.0).
        """
    )
