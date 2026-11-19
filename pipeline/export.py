"""
Data Export and Integrity Snapshot Engine for Proti IQ.
Exports sanitized ranking tables and snapshot metadata.
Neutralizes spreadsheet formula injection in CSV exports.
"""

import csv
import json
import os
from typing import Any
from sqlalchemy.orm import Session
from api.db import SessionLocal, Ranking, Protein, Crop, init_db

PROCESSED_DIR = "data/processed"


def sanitize_csv_cell(value: Any) -> str:
    """Neutralize formula injection by prefixing '=', '+', '-', '@' with a single quote."""
    val_str = str(value) if value is not None else ""
    if val_str and val_str[0] in ("=", "+", "-", "@"):
        return f"'{val_str}"
    return val_str


def export_rankings_csv(db: Session, output_file: str = "data/processed/latest_rankings.csv"):
    """Export current candidate rankings from the latest model run to a formula-safe CSV."""
    from api.db import ModelRun
    latest_run = db.query(ModelRun).order_by(ModelRun.created_at.desc()).first()
    if latest_run:
        rankings = db.query(Ranking).filter(Ranking.run_id == latest_run.id).all()
        print(f"Exporting rankings from latest run: {latest_run.id} ({len(rankings)} entries)")
    else:
        rankings = db.query(Ranking).all()

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "job", "benchmark_id", "crop_id", "accession", "protein_name",
            "score", "confidence", "screening_flags"
        ]
        writer = csv.writer(f)
        writer.writerow(fieldnames)

        for r in rankings:
            prot = db.query(Protein).filter(Protein.id == r.protein_id).first()
            prot_name = prot.name if prot else "Unknown"
            accession = prot.accession if prot else "Unknown"

            row = [
                sanitize_csv_cell(r.job),
                sanitize_csv_cell(r.benchmark_id),
                sanitize_csv_cell(r.crop_id),
                sanitize_csv_cell(accession),
                sanitize_csv_cell(prot_name),
                sanitize_csv_cell(r.score),
                sanitize_csv_cell(r.confidence),
                sanitize_csv_cell(r.flags_json),
            ]
            writer.writerow(row)

    print(f"Exported sanitized rankings to {output_file}")


def run_export():
    init_db()
    db = SessionLocal()
    try:
        export_rankings_csv(db)
    finally:
        db.close()


if __name__ == "__main__":
    run_export()
