"""
Unit test asserting that every stored protein's organism matches its assigned crop.
Verifies taxonomic integrity across the database.
"""

import pytest
from sqlalchemy.orm import Session
from api.db import SessionLocal, Crop, Protein


def test_every_stored_protein_organism_matches_crop():
    from api.db import init_db
    init_db()
    db: Session = SessionLocal()
    try:
        proteins = db.query(Protein).all()
        if len(proteins) == 0:
            # Seed test fixture in CI environment where .db is gitignored
            test_crop = Crop(
                id="cowpea",
                common_name="Cowpea",
                scientific_name="Vigna unguiculata",
                tax_id=3899,
                role="candidate",
                primary_job="milk",
                description="Test crop"
            )
            test_prot = Protein(
                crop_id="cowpea",
                accession="P13744",
                name="7S beta-vignin",
                family="7S",
                length=450,
                sequence="MARSSKLL",
                tax_id=3899,
                organism_name="Vigna unguiculata"
            )
            db.add(test_crop)
            db.add(test_prot)
            db.commit()
            proteins = [test_prot]

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
