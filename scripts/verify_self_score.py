"""Verify benchmark self-scores after fixes."""
import numpy as np
import json
import os
import sys
import yaml

sys.path.insert(0, ".")
from api.db import SessionLocal, Protein, Crop, Feature, init_db
from pipeline.scoring import score_protein_for_job

init_db()
db = SessionLocal()

with open("config/jobs.yaml") as f:
    jobs = yaml.safe_load(f)["jobs"]

for job_id, job_cfg in jobs.items():
    bm_id = job_cfg["primary_benchmark"]
    target_fam = job_cfg.get("key_family_target", "7S")
    bm_crop = db.query(Crop).filter(Crop.id == bm_id).first()

    bm_prot = (
        db.query(Protein)
        .filter(Protein.crop_id == bm_crop.id, Protein.family == target_fam)
        .order_by(Protein.reviewed.desc(), Protein.length.desc())
        .first()
    )
    if not bm_prot:
        bm_prot = (
            db.query(Protein)
            .filter(Protein.crop_id == bm_crop.id, Protein.family.in_(["7S", "11S"]))
            .order_by(Protein.reviewed.desc(), Protein.length.desc())
            .first()
        )

    bm_feats = {
        f.feature_name: f.value
        for f in db.query(Feature).filter(Feature.protein_id == bm_prot.id).all()
    }
    bm_vec = np.load(os.path.join("model_artifacts/embeddings", bm_prot.accession + ".npy"))

    result = score_protein_for_job(
        bm_prot, bm_prot, job_cfg, bm_feats, bm_feats, bm_vec, bm_vec, 10, 1
    )
    score = result["score"]
    name = bm_prot.name[:45]
    acc = bm_prot.accession
    fam = bm_prot.family
    print(f"{job_id.upper():5s}: {acc} ({name}) family={fam} -> SELF-SCORE={score}")

db.close()
