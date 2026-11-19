"""
Import and verify newly generated ESM-2 embeddings.
Updates model_artifacts/manifest.json and the database embeddings table.
"""

import os
import sys
import json
import hashlib
import numpy as np

sys.path.insert(0, ".")
from api.db import SessionLocal, Protein, Embedding, init_db

MODEL_NAME = "facebook/esm2_t33_650M_UR50D"
ARTIFACTS_DIR = "model_artifacts/embeddings"
MANIFEST_PATH = "model_artifacts/manifest.json"


def compute_sha256(filepath: str) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()


def run_import():
    init_db()
    db = SessionLocal()
    proteins = db.query(Protein).all()
    print(f"Verifying embeddings for {len(proteins)} proteins in {ARTIFACTS_DIR}...")

    manifest = {}
    updated_count = 0

    for prot in proteins:
        filename = f"{prot.accession}.npy"
        filepath = os.path.join(ARTIFACTS_DIR, filename)

        if not os.path.exists(filepath):
            print(f"Warning: {filename} missing from {ARTIFACTS_DIR}")
            continue

        vec = np.load(filepath)
        dim = int(vec.shape[0])
        sha = compute_sha256(filepath)

        manifest[filename] = {
            "accession": prot.accession,
            "sha256": sha,
            "dim": dim,
            "model": MODEL_NAME,
        }

        emb = db.query(Embedding).filter(Embedding.protein_id == prot.id).first()
        if not emb:
            emb = Embedding(
                protein_id=prot.id,
                model_name=MODEL_NAME,
                dim=dim,
                vector_ref=filepath,
                sha256=sha,
            )
            db.add(emb)
        else:
            emb.model_name = MODEL_NAME
            emb.dim = dim
            emb.sha256 = sha
            emb.vector_ref = filepath

        updated_count += 1

    db.commit()

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Success! {updated_count} ESM-2 embeddings registered into manifest and database.")
    print("Now run:\n  python -m pipeline.scoring\n  python -m pipeline.export")
    db.close()


if __name__ == "__main__":
    run_import()
