"""
AlphaFold Ingestion Pipeline for Proti IQ.
Queries AlphaFold DB API for predicted 3D structures and mean pLDDT confidence scores.
Caches structure files locally for offline 3D rendering.
"""

import json
import os
import time
import httpx
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from api.db import SessionLocal, Protein, init_db

ALPHAFOLD_API_URL = "https://alphafold.ebi.ac.uk/api/prediction/{accession}"
STRUCTURES_DIR = "data/raw/structures"


def fetch_alphafold_data(accession: str) -> Optional[Dict[str, Any]]:
    """Query AlphaFold DB API for protein accession structure and pLDDT data."""
    url = ALPHAFOLD_API_URL.format(accession=accession)
    headers = {"User-Agent": "Proti-IQ-Research/1.0 (academic; hackathon)"}

    try:
        with httpx.Client(timeout=20.0, follow_redirects=True) as client:
            resp = client.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0]
            elif resp.status_code == 404:
                return None
    except Exception as e:
        print(f"AlphaFold API error for {accession}: {e}")
    return None


def download_structure_file(pdb_url: str, target_path: str) -> bool:
    """Download and cache PDB structure file locally."""
    if os.path.exists(target_path):
        return True

    try:
        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            resp = client.get(pdb_url)
            if resp.status_code == 200:
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with open(target_path, "wb") as f:
                    f.write(resp.content)
                return True
    except Exception as e:
        print(f"Error downloading structure file from {pdb_url}: {e}")
    return False


def ingest_alphafold_for_proteins(db: Session, max_downloads: int = 100):
    """Scan all ingested proteins and fetch AlphaFold models and pLDDT scores."""
    proteins = db.query(Protein).all()
    print(f"Checking AlphaFold DB models for {len(proteins)} proteins...")

    updated_count = 0
    downloaded_structures = 0

    for prot in proteins:
        # Check if already processed
        if prot.alphafold_available and prot.plddt_mean is not None:
            continue

        af_info = fetch_alphafold_data(prot.accession)
        if af_info:
            mean_plddt = af_info.get("globalMetricValue") or af_info.get("plddt")
            pdb_url = af_info.get("pdbUrl")

            prot.alphafold_available = True
            prot.plddt_mean = float(mean_plddt) if mean_plddt is not None else 70.0

            if pdb_url and downloaded_structures < max_downloads:
                pdb_filename = os.path.join(STRUCTURES_DIR, f"{prot.accession}.pdb")
                if download_structure_file(pdb_url, pdb_filename):
                    downloaded_structures += 1

            updated_count += 1
        else:
            prot.alphafold_available = False
            prot.plddt_mean = None

        time.sleep(0.3)  # Rate limiting

    db.commit()
    print(f"AlphaFold ingestion complete: updated {updated_count} proteins, downloaded {downloaded_structures} structures.")


def run_af_ingest():
    init_db()
    db = SessionLocal()
    try:
        ingest_alphafold_for_proteins(db)
    finally:
        db.close()


if __name__ == "__main__":
    run_af_ingest()
