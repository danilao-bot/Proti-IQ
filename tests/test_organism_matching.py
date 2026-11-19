"""
Unit test asserting that every stored protein's organism matches its assigned crop.
Verifies taxonomic integrity across the database.
"""

import pytest
from sqlalchemy.orm import Session
from api.db import SessionLocal, Crop, Protein


def test_every_stored_protein_organism_matches_crop():
    db: Session = SessionLocal()
    try:
        proteins = db.query(Protein).all()
        assert len(proteins) > 0, "No proteins found in database"

        mismatches = []
        for p in proteins:
            crop = db.query(Crop).filter(Crop.id == p.crop_id).first()
            assert crop is not None, f"Protein {p.accession} has invalid crop_id {p.crop_id}"

            # If tax_id is present on both, assert they match
            if crop.tax_id and p.tax_id:
                if crop.tax_id != p.tax_id:
                    mismatches.append({
                        "accession": p.accession,
                        "protein_name": p.name,
                        "crop_id": p.crop_id,
                        "crop_tax_id": crop.tax_id,
                        "protein_tax_id": p.tax_id,
                        "protein_organism": p.organism_name
                    })

        assert len(mismatches) == 0, f"Found {len(mismatches)} organism mismatches: {mismatches}"
    finally:
        db.close()
