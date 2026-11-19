"""
Import and validate configuration and answer-key data into the database.
Enforces strict schema checks, citation presence, and data provenance.
"""

import csv
import os
import yaml
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from api.db import SessionLocal, init_db, Crop, Job, Measurement, DataSource


def import_crops(db: Session, config_path: str = "config/crops.yaml") -> int:
    """Load benchmark and candidate crops into the crops table."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    count = 0
    all_crops = data.get("benchmarks", []) + data.get("candidates", [])
    for entry in all_crops:
        crop_obj = db.query(Crop).filter(Crop.id == entry["id"]).first()
        if not crop_obj:
            crop_obj = Crop(
                id=entry["id"],
                common_name=entry["common_name"],
                scientific_name=entry["scientific_name"],
                tax_id=entry.get("tax_id"),
                role=entry["role"],
                primary_job=entry.get("primary_job"),
                description=entry.get("description"),
            )
            db.add(crop_obj)
        else:
            crop_obj.common_name = entry["common_name"]
            crop_obj.scientific_name = entry["scientific_name"]
            crop_obj.tax_id = entry.get("tax_id")
            crop_obj.role = entry["role"]
            crop_obj.primary_job = entry.get("primary_job")
            crop_obj.description = entry.get("description")
        count += 1

    db.commit()
    return count


def import_jobs(db: Session, config_path: str = "config/jobs.yaml") -> int:
    """Load application jobs into the jobs table."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Jobs configuration file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    count = 0
    jobs_dict = data.get("jobs", {})
    for job_id, entry in jobs_dict.items():
        job_obj = db.query(Job).filter(Job.id == job_id).first()
        if not job_obj:
            job_obj = Job(
                id=job_id,
                name=entry["name"],
                description=entry["target_function"],
                config_version="1.0",
            )
            db.add(job_obj)
        else:
            job_obj.name = entry["name"]
            job_obj.description = entry["target_function"]
        count += 1

    db.commit()
    return count


def import_answer_key(db: Session, csv_path: str = "data/answer_key/answer_key.csv") -> int:
    """Load curated measurements from answer_key.csv with strict citation validation."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Answer key CSV not found: {csv_path}")

    count = 0
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Enforce that citation and study_id are present
            if not row["citation"] or not row["study_id"]:
                raise ValueError(f"Measurement row missing citation or study_id: {row}")

            val = float(row["value"])
            measurement = Measurement(
                crop_id=row.get("crop_id") or None,
                job=row["job"],
                property=row["measured_property"],
                value=val,
                unit=row["unit"],
                conditions=row.get("conditions"),
                extraction_method=row.get("extraction_method"),
                study_id=row["study_id"],
                citation=row["citation"],
                verified_by=row.get("verified_by") or None,
                notes=row.get("notes"),
            )
            db.add(measurement)
            count += 1

    db.commit()
    return count


def init_data_sources(db: Session):
    """Seed baseline data sources with open licenses."""
    sources = [
        {
            "name": "UniProt Knowledgebase (UniProtKB)",
            "url": "https://rest.uniprot.org",
            "licence": "CC BY 4.0",
        },
        {
            "name": "AlphaFold Protein Structure Database",
            "url": "https://alphafold.ebi.ac.uk",
            "licence": "CC BY 4.0",
        },
    ]
    for s in sources:
        existing = db.query(DataSource).filter(DataSource.name == s["name"]).first()
        if not existing:
            db.add(DataSource(name=s["name"], url=s["url"], licence=s["licence"]))
    db.commit()


def run_import():
    """Execute complete initial configuration and answer key import."""
    init_db()
    db = SessionLocal()
    try:
        crops_count = import_crops(db)
        jobs_count = import_jobs(db)
        key_count = import_answer_key(db)
        init_data_sources(db)
        print(f"Successfully imported {crops_count} crops, {jobs_count} jobs, and {key_count} answer key measurements.")
    finally:
        db.close()


if __name__ == "__main__":
    run_import()
