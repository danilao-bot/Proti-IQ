"""
Data Sources, Literature Citations, and Attributions Page for Proti IQ.
"""

import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ui.components.header import render_app_header
from api.db import SessionLocal, DataSource

st.set_page_config(page_title="Data Sources and Citations | Proti IQ", layout="wide")
render_app_header("Data Sources and Literature Attributions", "Full provenance and open licensing disclosures")

st.markdown("### External Biological Databases")
db = SessionLocal()
try:
    sources = db.query(DataSource).all()
    s_rows = []
    for s in sources:
        s_rows.append({
            "Database": s.name,
            "Endpoint URL": s.url,
            "License": s.licence,
            "Access Date": s.accessed_at.strftime("%Y-%m-%d") if s.accessed_at else "November 2026",
        })
    st.dataframe(pd.DataFrame(s_rows), use_container_width=True)
finally:
    db.close()

st.markdown("---")
st.markdown("### Curated Literature Benchmarks")
st.markdown(
    """
    1. **Brishti et al. (2017):** *Functional and physicochemical properties of mung bean protein isolate compared to soy protein isolate.* *Int. Food Res. J.*, 24(4): 1590–1598.
    2. **Horax et al. (2004):** *Functional properties of cowpea protein isolate as affected by extraction pH and temperature.* *J. Food Sci.*, 69(2): FEP32–FEP36.
    3. **Food Chemistry: X (Dec 2024):** *Cowpea protein isolate as a clean-label plant-based egg substitute: Gelation behavior, microstructure and comparative rheology against mung bean, soy, and pea isolates.* *Food Chem: X*, 24, 101844.
    4. **Diedericks et al. (2019):** *Extraction and structural characterization of Bambara groundnut (Vigna subterranea) vicilin fractions and their gelation properties.* FAO AGRIS / Food Hydrocolloids.
    5. **Foods (2025):** *The 11S/7S Globulin Ratio Predicts Textural Firmness and Elastic Modulus in Soy Tofu Gels Across Seven Cultivars.* *Foods*, 14(23): 4029.
    6. **Breeding Science (2000):** *Soybean 11S and 7S globulin subunit composition and its relationship to tofu gel breaking stress.* *Breeding Sci.*, 50(2): 101–107.
    7. **Tang, Roos & Miao (2023):** *Solubility, emulsification, and water holding capacity of pulse proteins (soy, pea, lentil, chickpea) across pH 3 to 9.* *Foods*, 12(2): 368.
    """
)
