import numpy as np
import sys
import os
import yaml
import json
from Bio.Align import PairwiseAligner, substitution_matrices

sys.path.insert(0, ".")
from api.db import SessionLocal, Protein, Crop, Feature, init_db

init_db()
db = SessionLocal()

aligner = PairwiseAligner()
aligner.mode = "global"
aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
aligner.open_gap_score = -10
aligner.extend_gap_score = -0.5

def calib_cos(vec1, vec2):
    dot = np.dot(vec1, vec2)
    n1, n2 = np.linalg.norm(vec1), np.linalg.norm(vec2)
    if n1 == 0 or n2 == 0:
        return 0.5
    raw = dot / (n1 * n2)
    scaled = (raw - (-0.15)) / (0.42 - (-0.15))
    return float(max(0.1, min(1.0, scaled)))

def seq_id(s1, s2):
    s1, s2 = s1[:700], s2[:700]
    sc = aligner.score(s1, s2)
    max_p = (aligner.score(s1, s1) + aligner.score(s2, s2)) / 2.0
    return float(max(0.0, min(1.0, sc / max_p if max_p > 0 else 0.0)))

# Curated benchmark proteins: the actual major food storage globulins
bm_map = {
    "egg": "A0A1S3VZW2",  # Mung bean beta-conglycinin (594 aa)
    "gel": "P02858",      # Soy glycinin G4 (563 aa)
    "milk": "P11827",     # Soy beta-conglycinin alpha' (621 aa)
}

with open("config/jobs.yaml") as f:
    jobs = yaml.safe_load(f)["jobs"]

for job_id, bm_acc in bm_map.items():
    job_cfg = jobs[job_id]
    target_fam = job_cfg.get("key_family_target", "7S")
    bm_prot = db.query(Protein).filter(Protein.accession == bm_acc).first()
    bm_feats = {f.feature_name: f.value for f in db.query(Feature).filter(Feature.protein_id == bm_prot.id).all()}
    bm_vec = np.load(f"model_artifacts/embeddings/{bm_prot.accession}.npy")

    print(f"\n=== {job_id.upper()} (Benchmark: {bm_prot.crop_id} / {bm_prot.accession} - {bm_prot.name[:35]}) ===")
    w = job_cfg["weights"]

    for cand_crop in db.query(Crop).filter(Crop.role == "candidate").all():
        if cand_crop.id == "bambara_groundnut":
            continue
        cand_prots = db.query(Protein).filter(Protein.crop_id == cand_crop.id, Protein.family.in_(["7S", "11S"])).all()
        if not cand_prots:
            continue

        best_sc = 0
        best_acc = None
        best_e = 0
        best_ph = 0
        best_s = 0

        for cp in cand_prots:
            cp_feats = {f.feature_name: f.value for f in db.query(Feature).filter(Feature.protein_id == cp.id).all()}
            cp_vec = np.load(f"model_artifacts/embeddings/{cp.accession}.npy")

            emb_sim = calib_cos(cp_vec, bm_vec)
            family_sc = 1.0 if cp.family == target_fam else (0.5 if cp.family in ["7S", "11S"] else 0.1)

            mw_diff = abs(cp_feats.get("molecular_weight", 50000) - bm_feats.get("molecular_weight", 50000)) / 50000.0
            pi_diff = abs(cp_feats.get("isoelectric_point", 5.5) - bm_feats.get("isoelectric_point", 5.5)) / 4.0
            gravy_diff = abs(cp_feats.get("gravy", -0.5) - bm_feats.get("gravy", -0.5)) / 2.0

            h_diff = abs(cp_feats.get("secondary_structure_helix", 0.2) - bm_feats.get("secondary_structure_helix", 0.2))
            s_diff = abs(cp_feats.get("secondary_structure_sheet", 0.3) - bm_feats.get("secondary_structure_sheet", 0.3))
            t_diff = abs(cp_feats.get("secondary_structure_turn", 0.3) - bm_feats.get("secondary_structure_turn", 0.3))
            sec_dist = (h_diff + s_diff + t_diff) / 1.5

            phys_dist = (mw_diff + pi_diff + gravy_diff + sec_dist) / 4.0
            phys_sim = float(max(0.0, 1.0 - phys_dist))

            sid = seq_id(cp.sequence, bm_prot.sequence)
            cys_frac = cp_feats.get("cysteine_fraction", 0.0)
            sol_proxy = cp_feats.get("solubility_proxy", 0.5)

            if job_id == "egg":
                tot = (
                    w["embedding_similarity"] * emb_sim
                    + w["family_match"] * family_sc
                    + w["physicochemical_distance"] * phys_sim
                    + w["sequence_identity"] * sid
                    + w["cysteine_fraction"] * min(1.0, cys_frac * 50.0)
                )
            elif job_id == "gel":
                tot = (
                    w["embedding_similarity"] * emb_sim
                    + w["family_match"] * family_sc
                    + w["cysteine_fraction"] * min(1.0, cys_frac * 60.0)
                    + w["physicochemical_distance"] * phys_sim
                    + w["sequence_identity"] * sid
                )
            elif job_id == "milk":
                tot = (
                    w["embedding_similarity"] * emb_sim
                    + w["family_match"] * family_sc
                    + w["solubility_proxy"] * sol_proxy
                    + w["physicochemical_distance"] * phys_sim
                    + w["sequence_identity"] * sid
                )

            sc = round(tot * 100.0, 1)
            if sc > best_sc:
                best_sc = sc
                best_acc = cp.accession
                best_e = emb_sim * 100
                best_ph = phys_sim * 100
                best_s = sid * 100

        print(f"  {cand_crop.id:20s}: {best_sc:5.1f} ({best_acc}) emb={best_e:.1f} phys={best_ph:.1f} seq={best_s:.1f}")

db.close()
