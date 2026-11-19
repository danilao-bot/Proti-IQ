"""
Proti IQ - Resource Pack Ingestion Engine
Hack the Fork Nigeria 2026

Ingests datasets provided by hackathon organizers (expected on Feb 20).
Supports CSV, TSV, Excel (.xlsx, .xls), and JSON tabular structures.
Performs fuzzy column mapping, data validation, and loads directly into data/proti_iq.db.
"""

import os
import sys
import argparse
import sqlite3
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DB_PATH = Path("data/proti_iq.db")

# Target schema columns and their common aliases
COLUMN_SYNONYMS = {
    "crop_id": ["crop", "crop_id", "species", "organism", "plant", "legume", "sample", "crop_name"],
    "form": ["form", "ingredient_form", "fraction", "type", "state", "isolate_flour"],
    "variety": ["variety", "cultivar", "landrace", "genotype", "accession", "sample_id"],
    "property": ["property", "parameter", "metric", "assay", "functional_property", "test", "measured_property"],
    "value": ["value", "measurement", "result", "mean", "percentage", "reading"],
    "unit": ["unit", "units", "dimension"],
    "conditions": ["conditions", "treatment", "method", "protocol", "temperature", "temp", "ph"],
    "citation": ["citation", "reference", "source", "author", "study", "doi", "paper"]
}

# Standardized property names mapping
PROPERTY_CANONICAL = {
    "lgc": "least_gelation_concentration",
    "least gelation concentration": "least_gelation_concentration",
    "gelation": "least_gelation_concentration",
    "solubility": "solubility",
    "protein solubility": "solubility",
    "wac": "water_absorption_capacity",
    "water absorption": "water_absorption_capacity",
    "oac": "oil_absorption_capacity",
    "oil absorption": "oil_absorption_capacity",
    "emulsion": "emulsion_stability",
    "emulsion stability": "emulsion_stability",
    "protein content": "protein_content",
    "protein": "protein_content"
}

# Crop name normalizer
CROP_ID_MAP = {
    "cowpea": "cowpea",
    "bambara": "bambara_groundnut",
    "bambara groundnut": "bambara_groundnut",
    "soy": "soy",
    "soybean": "soy",
    "pea": "pea",
    "field pea": "pea",
    "pigeon pea": "pigeon_pea",
    "african yam bean": "african_yam_bean",
    "groundnut": "groundnut",
    "peanut": "groundnut",
    "mung bean": "mung_bean"
}


def map_column(col_name: str) -> Optional[str]:
    """Map arbitrary column name to standardized canonical field."""
    norm = col_name.strip().lower().replace("_", " ").replace("-", " ")
    for target, synonyms in COLUMN_SYNONYMS.items():
        if norm in synonyms or any(s == norm for s in synonyms):
            return target
    for target, synonyms in COLUMN_SYNONYMS.items():
        if any(s in norm for s in synonyms):
            return target
    return None


def read_file(file_path: Path) -> pd.DataFrame:
    """Reads CSV, TSV, Excel, or JSON into DataFrame."""
    ext = file_path.suffix.lower()
    if ext in [".csv", ".tsv", ".txt"]:
        try:
            return pd.read_csv(file_path, sep=None, engine="python")
        except Exception:
            return pd.read_csv(file_path)
    elif ext in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)
    elif ext == ".json":
        return pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def ingest_resource_pack(file_or_dir: str, db_path: Path = DB_PATH) -> Tuple[int, int, List[str]]:
    """
    Ingest resource pack file(s) into database.
    Populates resource_pack_raw table and normalized measurements.
    """
    p = Path(file_or_dir)
    files = [p] if p.is_file() else list(p.glob("*.*"))
    valid_exts = {".csv", ".tsv", ".xlsx", ".xls", ".json"}
    target_files = [f for f in files if f.suffix.lower() in valid_exts]

    if not target_files:
        return 0, 0, [f"No valid data files found in {file_or_dir}"]

    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create dedicated resource pack storage table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resource_pack_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_raw TEXT,
            crop_id TEXT,
            form TEXT,
            variety TEXT,
            property TEXT NOT NULL,
            value REAL NOT NULL,
            unit TEXT,
            conditions TEXT,
            citation TEXT,
            source_file TEXT,
            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    total_imported = 0
    total_skipped = 0
    audit_log = []

    for f in target_files:
        audit_log.append(f"Processing file: {f.name}")
        try:
            df = read_file(f)
        except Exception as e:
            audit_log.append(f"  Error reading {f.name}: {e}")
            continue

        # Column mapping
        col_map = {}
        for c in df.columns:
            mapped = map_column(str(c))
            if mapped:
                col_map[c] = mapped

        audit_log.append(f"  Mapped columns: {col_map}")

        if "crop_id" not in col_map.values() or "value" not in col_map.values():
            audit_log.append(f"  Warning: {f.name} lacks required 'crop' or 'value' columns. Skipping.")
            total_skipped += len(df)
            continue

        df_renamed = df.rename(columns=col_map)
        
        file_imported = 0
        file_skipped = 0

        for _, row in df_renamed.iterrows():
            crop_raw = str(row.get("crop_id", "")).strip()
            if not crop_raw or crop_raw.lower() in ["nan", "none", ""]:
                file_skipped += 1
                continue

            try:
                val = float(row.get("value"))
            except (ValueError, TypeError):
                file_skipped += 1
                continue

            crop_id = CROP_ID_MAP.get(crop_raw.lower(), crop_raw.lower().replace(" ", "_"))
            form = str(row.get("form", "isolate")).strip()
            variety = str(row.get("variety", "unspecified")).strip()
            prop_raw = str(row.get("property", "functional_score")).strip().lower()
            prop = PROPERTY_CANONICAL.get(prop_raw, prop_raw)
            unit = str(row.get("unit", "")).strip()
            conditions = str(row.get("conditions", "")).strip()
            citation = str(row.get("citation", f"Organizers Resource Pack - {f.name}")).strip()

            cursor.execute("""
                INSERT INTO resource_pack_records (crop_raw, crop_id, form, variety, property, value, unit, conditions, citation, source_file)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (crop_raw, crop_id, form, variety, prop, val, unit, conditions, citation, f.name))
            file_imported += 1

        conn.commit()
        total_imported += file_imported
        total_skipped += file_skipped
        audit_log.append(f"  Imported: {file_imported} rows | Skipped: {file_skipped} rows")

    conn.close()
    return total_imported, total_skipped, audit_log


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Proti IQ Resource Pack Importer")
    parser.add_argument("path", help="Path to resource pack file or directory")
    args = parser.parse_args()

    imp, skp, logs = ingest_resource_pack(args.path)
    print("\n--- INGESTION REPORT ---")
    for log in logs:
        print(log)
    print(f"\nFinal: {imp} records imported, {skp} records skipped.")
