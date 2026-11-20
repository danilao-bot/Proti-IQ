"""
AlphaFold 3D Biomolecular Structure Visualization Page for Proti IQ.
Displays real 3D structural predictions, per-residue pLDDT confidence scores,
and biochemical food functional interpretations.
"""

import os
import streamlit as st
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ui.components.header import render_app_header
from api.db import SessionLocal, Protein, Crop

st.set_page_config(page_title="AlphaFold 3D View | Proti IQ", layout="wide")
render_app_header("AlphaFold 3D Structure Viewer", "Structural topology, residue surface exposure, and functional domain inspection")

st.info("Notice: Structures rendered below are in-silico computational predictions from AlphaFold DB (v6 models), evaluated by mean pLDDT confidence scores.")

BIOCHEMICAL_SIGNIFICANCE = {
    "A0A1S3VZW2": {
        "title": "Mung Bean 8S Vicilin (JUST Egg Industrial Control)",
        "food_role": "Plant-Based Egg Gelation",
        "mechanism": "The intact beta-barrel cupin fold unfolds at 72°C–80°C, releasing hydrophobic residues that associate into an elastic, non-rubbery scramblable gel matrix.",
        "key_residues": "Cupin core barrel (residues 180–420); low surface cysteine content ensures soft scramble without sulfur off-notes."
    },
    "P02858": {
        "title": "Soybean 11S Glycinin G4 (Commercial Tofu Control)",
        "food_role": "Coagulated Curd & Meat Fiber Formation",
        "mechanism": "Divalent calcium ions (0.3% CaCl2) cross-link surface-exposed Aspartate and Glutamate carboxylate oxygens, while 85°C heat unfolds the hexamer, triggering covalent -S-S- disulfide cross-linking.",
        "key_residues": "8 conserved cysteine residues forming intermolecular disulfide bonds; dense acidic surface patches binding Ca2+."
    },
    "P11827": {
        "title": "Soybean 7S Beta-conglycinin alpha' (Plant Milk Control)",
        "food_role": "Colloidal Milk Dispersion & Emulsification",
        "mechanism": "High surface net-negative charge (-18 to -28 mV at pH 7.0) generates strong electrostatic repulsion between fat droplets, preventing sedimentation and phase separation over 7 days.",
        "key_residues": "Hydrophilic acidic extension domain; amphiphilic core stabilizing oil-in-water interfaces."
    }
}

db = SessionLocal()
try:
    # Query proteins prioritizing AlphaFold available ones
    proteins = (
        db.query(Protein)
        .order_by(Protein.alphafold_available.desc(), Protein.plddt_mean.desc(), Protein.name.asc())
        .all()
    )

    options = {}
    for p in proteins:
        tag = f"[pLDDT: {p.plddt_mean:.1f} - Cached 3D]" if p.alphafold_available and p.plddt_mean else "[pLDDT: Unindexed]"
        options[p.accession] = f"{p.crop.common_name} — {p.name} ({p.accession}) {tag}"

    selected_acc = st.selectbox(
        "Select Protein Structure to Inspect:",
        options=list(options.keys()),
        format_func=lambda x: options[x],
        index=0
    )

    prot = db.query(Protein).filter(Protein.accession == selected_acc).first()
    pdb_path = os.path.join("data/raw/structures", f"{selected_acc}.pdb")

    col1, col2 = st.columns([2.5, 1.2])

    with col2:
        st.markdown("### Structural Metrics")
        st.metric("Sequence Length", f"{prot.length} AA")
        st.metric("Mean pLDDT", f"{prot.plddt_mean:.1f} / 100" if prot.plddt_mean else "In-Silico Prediction")
        st.markdown(f"**Storage Family:** `{prot.family}`")
        st.markdown(f"**Curation Status:** {'Swiss-Prot (Experimental)' if prot.reviewed else 'TrEMBL (Predicted)'}")

        st.markdown("---")
        st.markdown("#### pLDDT Confidence Color Scheme")
        st.markdown("- **Very High (>90) [Blue]:** High coordinate precision")
        st.markdown("- **Confident (70-90) [Cyan]:** Well-modeled core backbone")
        st.markdown("- **Low (50-70) [Yellow]:** Flexible loop or linker")
        st.markdown("- **Very Low (<50) [Orange]:** Disordered or terminal region")

        if selected_acc in BIOCHEMICAL_SIGNIFICANCE:
            st.markdown("---")
            info = BIOCHEMICAL_SIGNIFICANCE[selected_acc]
            st.markdown(f"#### Food Chemistry Rationale: {info['food_role']}")
            st.write(info["mechanism"])
            st.caption(f"Target Domains: {info['key_residues']}")

    with col1:
        if os.path.exists(pdb_path):
            with open(pdb_path, "r", encoding="utf-8") as f:
                pdb_text = f.read()

            try:
                import py3Dmol
                from stmol import showmol

                st.markdown(f"**Interactive 3D Ribbon Model:** `{prot.name}` (`{selected_acc}`)")
                view = py3Dmol.view(width=750, height=520)
                view.addModel(pdb_text, "pdb")
                # Color by b-factor (which represents pLDDT in AlphaFold DB)
                view.setStyle({"cartoon": {"colorscheme": {"prop": "b", "gradient": "roygb", "min": 50, "max": 90}}})
                view.zoomTo()
                showmol(view, height=520, width=750)
                st.caption("Rotate with Left Click | Zoom with Scroll Wheel | Pan with Right Click")
            except Exception as e:
                st.warning(f"3D rendering fallback: {e}")
                st.code(f"PDB file cached at: {pdb_path}\nFile size: {os.path.getsize(pdb_path):,} bytes")
        else:
            st.warning(f"No local 3D structure cached for accession `{selected_acc}`. Downloaded benchmark structures are: `A0A1S3VZW2`, `P02858`, and `P11827`.")
finally:
    db.close()
