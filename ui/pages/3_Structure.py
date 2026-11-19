"""
AlphaFold 3D Biomolecular Structure Visualization Page for Proti IQ.
"""

import os
import streamlit as st
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ui.components.header import render_app_header
from api.db import SessionLocal, Protein, Crop

st.set_page_config(page_title="AlphaFold 3D View | Proti IQ", layout="wide")
render_app_header("AlphaFold 3D Structure Viewer", "Structural confidence analysis and residue topology")

st.info("Notice: Structures rendered below are in-silico computational predictions from AlphaFold DB, not experimentally determined crystallographic coordinates.")

db = SessionLocal()
try:
    proteins = (
        db.query(Protein)
        .order_by(Protein.alphafold_available.desc(), Protein.name.asc())
        .all()
    )

    options = {
        p.accession: f"{p.crop.common_name} - {p.name} ({p.accession}) [pLDDT: {p.plddt_mean or 'N/A'}]"
        for p in proteins
    }

    if not options:
        st.warning("No protein records found. Run the ingestion pipeline first.")
    else:
        selected_acc = st.selectbox(
            "Select Protein to Inspect:",
            options=list(options.keys()),
            format_func=lambda x: options[x],
        )

        prot = db.query(Protein).filter(Protein.accession == selected_acc).first()
        pdb_path = os.path.join("data/raw/structures", f"{selected_acc}.pdb")

        col1, col2 = st.columns([3, 1])

        with col2:
            st.markdown("### Structural Metrics")
            st.metric("Sequence Length", f"{prot.length} AA")
            st.metric("Mean pLDDT", f"{prot.plddt_mean:.1f}" if prot.plddt_mean else "Unindexed")
            st.markdown(f"**Storage Family:** `{prot.family}`")
            st.markdown(f"**Reviewed Status:** {'Swiss-Prot' if prot.reviewed else 'TrEMBL'}")

            st.markdown("---")
            st.markdown("#### pLDDT Color Scheme")
            st.markdown("- **Very High (>90) [Blue]:** High coordinate accuracy")
            st.markdown("- **Confident (70-90) [Cyan]:** Well-modeled backbone")
            st.markdown("- **Low (50-70) [Yellow]:** Flexible domain or loop")
            st.markdown("- **Very Low (<50) [Orange]:** Likely intrinsically disordered")

        with col1:
            if os.path.exists(pdb_path):
                with open(pdb_path, "r", encoding="utf-8") as f:
                    pdb_text = f.read()

                try:
                    import py3Dmol
                    from stmol import showmol

                    view = py3Dmol.view(width=750, height=500)
                    view.addModel(pdb_text, "pdb")
                    view.setStyle({"cartoon": {"colorscheme": {"prop": "b", "gradient": "roygb", "min": 50, "max": 90}}})
                    view.zoomTo()
                    showmol(view, height=500, width=750)
                except ImportError:
                    st.warning("`stmol` or `py3Dmol` not installed in this environment. Showing PDB metadata.")
                    st.code(f"PDB file cached at: {pdb_path}\nFile size: {os.path.getsize(pdb_path)} bytes")
            else:
                st.warning(f"No local structure file found for accession `{selected_acc}`. Downloaded during Phase 1 ingestion.")
finally:
    db.close()
