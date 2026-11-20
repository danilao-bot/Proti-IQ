"""Deep diagnostic of MILK job scoring — why it's low and what each lever does."""
import numpy as np
import json
import os
import sys
import yaml

sys.path.insert(0, ".")
from api.db import SessionLocal, Protein, Crop, Feature, Embedding, init_db
from pipeline.scoring import compute_cosine_similarity, compute_sequence_identity

init_db()
db = SessionLocal()

with open("config/jobs.yaml") as f:
    milk_cfg = yaml.safe_load(f)["jobs"]["milk"]

print("=" * 80)
print("MILK JOB — FULL ANATOMY")
print("=" * 80)

# 1. What benchmark is being used?
bm_crop = db.query(Crop).filter(Crop.id == milk_cfg["primary_benchmark"]).first()
bm_prot = (
    db.query(Protein)
    .filter(Protein.crop_id == bm_crop.id)
    .order_by(Protein.reviewed.desc(), Protein.length.desc())
    .first()
)
print(f"\nBenchmark crop: {bm_crop.id} ({bm_crop.scientific_name})")
print(f"Benchmark protein selected: {bm_prot.accession}")
print(f"  Name: {bm_prot.name}")
print(f"  Family: {bm_prot.family}")
print(f"  Length: {len(bm_prot.sequence)} aa")
print(f"  Reviewed: {bm_prot.reviewed}")

# What SHOULD be the benchmark? Show all soy storage proteins
soy_prots = db.query(Protein).filter(Protein.crop_id == "soy").all()
print(f"\nAll soy proteins ({len(soy_prots)} total):")
print(f"  Storage proteins (7S/11S):")
for p in sorted(soy_prots, key=lambda x: x.family or ""):
    if p.family in ("7S", "11S"):
        feats = {f.feature_name: f.value for f in db.query(Feature).filter(Feature.protein_id == p.id).all()}
        sol = feats.get("solubility_proxy", 0)
        pi = feats.get("isoelectric_point", 0)
        gravy = feats.get("gravy", 0)
        print(f"    {p.accession} | {p.family:3s} | {p.name[:50]:50s} | len={len(p.sequence):4d} | pI={pi:.2f} | GRAVY={gravy:.3f} | sol_proxy={sol:.3f} | reviewed={p.reviewed}")
    
print(f"\n  Non-storage proteins:")
for p in soy_prots:
    if p.family not in ("7S", "11S"):
        print(f"    {p.accession} | fam={p.family or 'None':6s} | {p.name[:60]:60s} | len={len(p.sequence):4d} | reviewed={p.reviewed}")

# 2. Weight breakdown
print("\n" + "=" * 80)
print("MILK WEIGHTS & THEORETICAL CEILING")
print("=" * 80)
w = milk_cfg["weights"]
penalty = milk_cfg.get("confidence_penalty", 1.0)
print(f"\nconfidence_penalty = {penalty}  (hard multiplier on final score)")
print(f"Theoretical maximum = {penalty * 100:.1f}\n")
for name, val in w.items():
    max_pts = val * 100 * penalty
    print(f"  {name:30s}: weight={val:.2f}  -> max {max_pts:5.1f} points")

# 3. For each candidate crop, show exactly where points are lost
print("\n" + "=" * 80)
print("MILK SCORE BREAKDOWN PER CROP (using CURRENT wrong benchmark)")
print("=" * 80)

bm_feats = {f.feature_name: f.value for f in db.query(Feature).filter(Feature.protein_id == bm_prot.id).all()}
bm_vec = np.load(os.path.join("model_artifacts/embeddings", bm_prot.accession + ".npy"))

candidates = db.query(Crop).filter(Crop.role == "candidate").all()
for cand_crop in sorted(candidates, key=lambda x: x.id):
    cand_prots = db.query(Protein).filter(Protein.crop_id == cand_crop.id, Protein.family.in_(["7S", "11S"])).all()
    if not cand_prots:
        print(f"\n  {cand_crop.id}: 0 storage proteins — skipped")
        continue
    
    # Find the best-scoring candidate protein
    best_score = 0
    best_prot = None
    best_breakdown = None
    
    for cp in cand_prots:
        cp_feats = {f.feature_name: f.value for f in db.query(Feature).filter(Feature.protein_id == cp.id).all()}
        cp_vec = np.load(os.path.join("model_artifacts/embeddings", cp.accession + ".npy"))
        
        emb_sim = compute_cosine_similarity(cp_vec, bm_vec)
        raw_cos = float(np.dot(cp_vec, bm_vec) / (np.linalg.norm(cp_vec) * np.linalg.norm(bm_vec)))
        
        sol_proxy = cp_feats.get("solubility_proxy", 0.5)
        
        mw_diff = abs(cp_feats.get("molecular_weight", 50000) - bm_feats.get("molecular_weight", 50000)) / 50000.0
        pi_diff = abs(cp_feats.get("isoelectric_point", 5.5) - bm_feats.get("isoelectric_point", 5.5)) / 4.0
        gravy_diff = abs(cp_feats.get("gravy", -0.5) - bm_feats.get("gravy", -0.5)) / 2.0
        phys_dist = (mw_diff + pi_diff + gravy_diff) / 3.0
        phys_sim = max(0.0, 1.0 - phys_dist)
        
        seq_id = compute_sequence_identity(cp.sequence, bm_prot.sequence)
        
        total = (
            w["embedding_similarity"] * emb_sim
            + w["solubility_proxy"] * sol_proxy
            + w["physicochemical_distance"] * phys_sim
            + w["sequence_identity"] * seq_id
        ) * penalty
        
        final = round(total * 100, 1)
        
        if final > best_score:
            best_score = final
            best_prot = cp
            best_breakdown = {
                "emb_sim": emb_sim,
                "raw_cos": raw_cos,
                "sol_proxy": sol_proxy,
                "phys_sim": phys_sim,
                "seq_id": seq_id,
                "mw_diff": mw_diff,
                "pi_diff": pi_diff,
                "gravy_diff": gravy_diff,
                "cp_feats": cp_feats,
            }
    
    if best_prot:
        b = best_breakdown
        print(f"\n  {cand_crop.id} -> best protein: {best_prot.accession} ({best_prot.family}) score={best_score}")
        print(f"    Component breakdown (raw 0-1 -> weighted -> after penalty):")
        
        emb_pts = w["embedding_similarity"] * b["emb_sim"] * penalty * 100
        sol_pts = w["solubility_proxy"] * b["sol_proxy"] * penalty * 100
        phys_pts = w["physicochemical_distance"] * b["phys_sim"] * penalty * 100
        seq_pts = w["sequence_identity"] * b["seq_id"] * penalty * 100
        
        print(f"    embedding_similarity: raw={b['emb_sim']:.3f} (cosine={b['raw_cos']:.4f})  -> {emb_pts:5.1f} / {w['embedding_similarity']*100*penalty:.1f} pts")
        print(f"    solubility_proxy:     raw={b['sol_proxy']:.3f}                            -> {sol_pts:5.1f} / {w['solubility_proxy']*100*penalty:.1f} pts")
        print(f"    physicochemical:      raw={b['phys_sim']:.3f} (mw={b['mw_diff']:.3f} pi={b['pi_diff']:.3f} grav={b['gravy_diff']:.3f}) -> {phys_pts:5.1f} / {w['physicochemical_distance']*100*penalty:.1f} pts")
        print(f"    sequence_identity:    raw={b['seq_id']:.3f}                               -> {seq_pts:5.1f} / {w['sequence_identity']*100*penalty:.1f} pts")
        print(f"    TOTAL: {emb_pts + sol_pts + phys_pts + seq_pts:.1f}")
        print(f"    Candidate pI={b['cp_feats'].get('isoelectric_point', '?')}  GRAVY={b['cp_feats'].get('gravy', '?')}  MW={b['cp_feats'].get('molecular_weight', '?')}")
        print(f"    Benchmark pI={bm_feats.get('isoelectric_point', '?')}  GRAVY={bm_feats.get('gravy', '?')}  MW={bm_feats.get('molecular_weight', '?')}")

# 4. What about the solubility proxy formula itself?
print("\n" + "=" * 80)
print("SOLUBILITY PROXY FORMULA ANALYSIS")
print("=" * 80)
print("\nFormula: sol = min(1, max(0, (|pI - 7| / 4) * 0.6 + (-GRAVY + 1) / 2 * 0.4))")
print("\nTest cases:")
test_cases = [
    ("Soy glycinin (typical)", 5.0, -0.35),
    ("Soy beta-conglycinin", 5.2, -0.42),
    ("Cowpea vicilin (typical)", 5.5, -0.40),
    ("Mung bean vicilin", 5.3, -0.38),
    ("Pea legumin", 4.8, -0.30),
    ("Perfect: pI far from 7, very hydrophilic", 3.0, -1.5),
    ("Worst: pI at 7, hydrophobic", 7.0, 1.0),
]
for label, pi, gravy in test_cases:
    pi_dist = abs(pi - 7.0)
    sol = min(1.0, max(0.0, (pi_dist / 4.0) * 0.6 + (-gravy + 1.0) / 2.0 * 0.4))
    print(f"  {label:45s}: pI={pi:.1f} GRAVY={gravy:+.2f}  -> sol_proxy={sol:.3f} ({sol*100:.0f}%)")

# 5. What would a correct soy benchmark give?
print("\n" + "=" * 80)
print("WHAT IF WE USE THE CORRECT SOY BENCHMARK? (best 7S or 11S)")
print("=" * 80)

# Find the best soy 7S and 11S
soy_storage = [p for p in soy_prots if p.family in ("7S", "11S")]
if soy_storage:
    # Pick the longest 7S and 11S
    soy_7s = [p for p in soy_storage if p.family == "7S"]
    soy_11s = [p for p in soy_storage if p.family == "11S"]
    
    for label, candidates_list in [("7S (beta-conglycinin)", soy_7s), ("11S (glycinin)", soy_11s)]:
        if not candidates_list:
            print(f"\n  No soy {label} found")
            continue
        # Pick longest reviewed, then longest
        best_bm = sorted(candidates_list, key=lambda p: (p.reviewed, len(p.sequence)), reverse=True)[0]
        best_bm_feats = {f.feature_name: f.value for f in db.query(Feature).filter(Feature.protein_id == best_bm.id).all()}
        best_bm_vec = np.load(os.path.join("model_artifacts/embeddings", best_bm.accession + ".npy"))
        
        print(f"\n  Using soy {label}: {best_bm.accession} ({best_bm.name[:50]}) len={len(best_bm.sequence)}")
        print(f"  Benchmark pI={best_bm_feats.get('isoelectric_point', '?')}  GRAVY={best_bm_feats.get('gravy', '?')}  MW={best_bm_feats.get('molecular_weight', '?')}")
        
        for cand_crop in sorted(candidates, key=lambda x: x.id):
            cand_prots = db.query(Protein).filter(Protein.crop_id == cand_crop.id, Protein.family.in_(["7S", "11S"])).all()
            if not cand_prots:
                continue
            
            best_s = 0
            for cp in cand_prots:
                cp_feats = {f.feature_name: f.value for f in db.query(Feature).filter(Feature.protein_id == cp.id).all()}
                cp_vec = np.load(os.path.join("model_artifacts/embeddings", cp.accession + ".npy"))
                
                emb_sim = compute_cosine_similarity(cp_vec, best_bm_vec)
                sol_proxy = cp_feats.get("solubility_proxy", 0.5)
                
                mw_diff = abs(cp_feats.get("molecular_weight", 50000) - best_bm_feats.get("molecular_weight", 50000)) / 50000.0
                pi_diff = abs(cp_feats.get("isoelectric_point", 5.5) - best_bm_feats.get("isoelectric_point", 5.5)) / 4.0
                gravy_diff = abs(cp_feats.get("gravy", -0.5) - best_bm_feats.get("gravy", -0.5)) / 2.0
                phys_dist = (mw_diff + pi_diff + gravy_diff) / 3.0
                phys_sim = max(0.0, 1.0 - phys_dist)
                
                seq_id = compute_sequence_identity(cp.sequence, best_bm.sequence)
                
                total = (
                    w["embedding_similarity"] * emb_sim
                    + w["solubility_proxy"] * sol_proxy
                    + w["physicochemical_distance"] * phys_sim
                    + w["sequence_identity"] * seq_id
                ) * penalty
                final = round(total * 100, 1)
                if final > best_s:
                    best_s = final
            
            print(f"    {cand_crop.id:20s}: {best_s:5.1f}  (was: see above)")

db.close()
