"""Diagnostic: score each benchmark protein against itself to find the theoretical max."""
import numpy as np
import json
import os
import sys
import yaml

sys.path.insert(0, ".")
from api.db import SessionLocal, Protein, Crop, Feature, Embedding, init_db
from pipeline.scoring import score_protein_for_job, compute_cosine_similarity, compute_sequence_identity

init_db()
db = SessionLocal()

with open("config/jobs.yaml") as f:
    jobs = yaml.safe_load(f)["jobs"]

print("=" * 80)
print("PART 1: BENCHMARK SELF-SCORE (what does 100% match look like?)")
print("=" * 80)

for job_id, job_cfg in jobs.items():
    bm_id = job_cfg["primary_benchmark"]
    bm_crop = db.query(Crop).filter(Crop.id == bm_id).first()
    bm_prot = (
        db.query(Protein)
        .filter(Protein.crop_id == bm_crop.id)
        .order_by(Protein.reviewed.desc(), Protein.length.desc())
        .first()
    )

    bm_feats = {f.feature_name: f.value for f in db.query(Feature).filter(Feature.protein_id == bm_prot.id).all()}
    bm_vec_path = os.path.join("model_artifacts/embeddings", bm_prot.accession + ".npy")
    bm_vec = np.load(bm_vec_path)

    result = score_protein_for_job(bm_prot, bm_prot, job_cfg, bm_feats, bm_feats, bm_vec, bm_vec, 10, 1)
    print(f"\n{job_id.upper()} benchmark: {bm_crop.id} / {bm_prot.accession} ({bm_prot.name})")
    print(f"  SELF-SCORE: {result['score']}")
    contrib = result["contributions"]
    print(f"  emb_sim={contrib['embedding_similarity']}  phys={contrib['physicochemical_match']}  seq_id={contrib['sequence_identity']}  fam={contrib['family_match']}  cys={contrib['cysteine_fraction']}  sol={contrib['solubility_proxy']}")

print("\n" + "=" * 80)
print("PART 2: COMPONENT-LEVEL DRILL-DOWN FOR TOP CANDIDATES")
print("=" * 80)

# For the top candidate per job, show what cosine similarity and seq identity actually are (raw)
import sqlite3
conn = sqlite3.connect("data/proti_iq.db")
c = conn.cursor()

for job_id, job_cfg in jobs.items():
    bm_id = job_cfg["primary_benchmark"]
    bm_crop = db.query(Crop).filter(Crop.id == bm_id).first()
    bm_prot = (
        db.query(Protein)
        .filter(Protein.crop_id == bm_crop.id)
        .order_by(Protein.reviewed.desc(), Protein.length.desc())
        .first()
    )
    bm_vec = np.load(os.path.join("model_artifacts/embeddings", bm_prot.accession + ".npy"))

    # Get top candidate protein per crop
    c.execute("""
        SELECT crop_id, protein_id, score, contributions_json
        FROM rankings
        WHERE run_id = 'run_744893' AND job = ?
        GROUP BY crop_id
        HAVING score = MAX(score)
        ORDER BY score DESC
        LIMIT 2
    """, (job_id,))
    rows = c.fetchall()
    
    print(f"\n--- {job_id.upper()} (benchmark: {bm_prot.accession}) ---")
    for crop_id, prot_id, score, cj in rows:
        cand_prot = db.query(Protein).filter(Protein.id == prot_id).first()
        cand_vec = np.load(os.path.join("model_artifacts/embeddings", cand_prot.accession + ".npy"))
        
        raw_cos = float(np.dot(bm_vec, cand_vec) / (np.linalg.norm(bm_vec) * np.linalg.norm(cand_vec)))
        scaled_cos = max(0.0, min(1.0, (raw_cos + 1.0) / 2.0))
        
        seq_id = compute_sequence_identity(cand_prot.sequence, bm_prot.sequence)
        
        print(f"  {crop_id}: {cand_prot.accession} score={score}")
        print(f"    raw_cosine={raw_cos:.4f}  scaled_cosine={scaled_cos:.4f}  seq_identity={seq_id:.4f}")
        print(f"    cand_family={cand_prot.family}  cand_len={len(cand_prot.sequence)}  bm_len={len(bm_prot.sequence)}")

conn.close()

print("\n" + "=" * 80)
print("PART 3: WHERE IS THE SCORE CEILING?")
print("=" * 80)

# Show the weight allocations and theoretical max per component
for job_id, job_cfg in jobs.items():
    w = job_cfg["weights"]
    penalty = job_cfg.get("confidence_penalty", 1.0)
    total_w = sum(w.values())
    theoretical_max = total_w * 100.0 * penalty
    print(f"\n{job_id.upper()}: weights sum to {total_w:.2f}, penalty={penalty}, theoretical max = {theoretical_max:.1f}")
    for wname, wval in w.items():
        print(f"  {wname}: {wval} -> max contribution = {wval * 100 * penalty:.1f} points")

db.close()
