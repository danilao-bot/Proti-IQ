"""
Router for Protein metadata and AlphaFold 3D structure delivery (/api/v1/proteins).
"""

import json
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, PlainTextResponse
from sqlalchemy.orm import Session
from api.db import get_db, Protein, Feature
from api.security import validate_accession

router = APIRouter(prefix="/api/v1", tags=["Proteins"])


@router.get("/proteins/{accession}")
def get_protein_detail(accession: str, db: Session = Depends(get_db)):
    """Retrieve full sequence and biophysical feature breakdown for a validated accession."""
    clean_acc = validate_accession(accession)
    prot = db.query(Protein).filter(Protein.accession == clean_acc).first()
    if not prot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Protein accession {clean_acc} not found in database.",
        )

    features = db.query(Feature).filter(Feature.protein_id == prot.id).all()
    feat_dict = {f.feature_name: f.value for f in features}
    flags = json.loads(prot.keywords_json).get("screening_flags", []) if prot.keywords_json else []

    return {
        "accession": prot.accession,
        "name": prot.name,
        "family": prot.family,
        "reviewed": prot.reviewed,
        "length": prot.length,
        "sequence": prot.sequence,
        "alphafold_available": prot.alphafold_available,
        "plddt_mean": prot.plddt_mean,
        "features": feat_dict,
        "screening_flags": flags,
    }


@router.get("/structure/{accession}")
def get_protein_structure(accession: str):
    """Serve cached AlphaFold 3D PDB structure file. Never proxies arbitrary URLs."""
    clean_acc = validate_accession(accession)
    pdb_path = os.path.join("data/raw/structures", f"{clean_acc}.pdb")

    if not os.path.exists(pdb_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Structure coordinate file for {clean_acc} is not indexed or downloaded.",
        )

    return FileResponse(
        path=pdb_path,
        media_type="chemical/x-pdb",
        filename=f"{clean_acc}.pdb",
    )
