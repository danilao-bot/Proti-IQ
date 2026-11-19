"""
UniProt Ingestion Pipeline for Proti IQ.
Queries UniProt REST API, caches raw responses, parses 7S/11S storage proteins,
extracts allergen and anti-nutrient keywords, and populates the proteins table.
"""

import csv
import json
import os
import re
import time
import httpx
import yaml
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from api.db import SessionLocal, Crop, Protein, init_db

UNIPROT_SEARCH_URL = "https://rest.uniprot.org/uniprotkb/search"
CACHE_DIR = "data/raw"
PROCESSED_DIR = "data/processed"


def classify_storage_family(name: str, comments: str = "", keywords: List[str] = None) -> str:
    """Classify protein into 7S (vicilin-like), 11S (legumin-like), or other."""
    text = (name + " " + comments + " " + " ".join(keywords or [])).lower()
    if any(k in text for k in ["vicilin", "7s", "beta-conglycinin", "phaseolin", "canavalin", "8s"]):
        return "7S"
    elif any(k in text for k in ["legumin", "11s", "glycinin", "arachin", "provicilin"]):
        return "11S"
    return "other"


def extract_screening_flags(keywords: List[str], protein_name: str) -> List[str]:
    """Detect allergen and anti-nutritional factors from keywords and annotations."""
    flags = []
    text = (protein_name + " " + " ".join(keywords)).lower()
    if "allergen" in text:
        flags.append("Allergen (UniProt Annotated)")
    if any(k in text for k in ["trypsin inhibitor", "protease inhibitor", "bowman-birk"]):
        flags.append("Anti-Nutrient: Protease Inhibitor")
    if "lectin" in text or "agglutinin" in text:
        flags.append("Anti-Nutrient: Lectin / Agglutinin")
    return flags


def query_uniprot_for_crop(crop_info: Dict[str, Any], cache_file: str, force_refresh: bool = False) -> List[Dict[str, Any]]:
    """Fetch storage proteins for a given crop from UniProt with local file caching."""
    if not force_refresh and os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cached = json.load(f)
                if cached and len(cached) > 0:
                    return cached
        except Exception:
            pass

    tax_id = crop_info.get("tax_id")
    sci_name = crop_info.get("scientific_name", "")
    crop_id = crop_info.get("id", "")

    if tax_id:
        if crop_id == "bambara_groundnut":
            # Orphan legume with no reviewed storage proteins: fetch all organism proteins (<10)
            query = f"organism_id:{tax_id}"
        elif crop_id == "african_yam_bean":
            query = f"organism_id:{tax_id} AND (vicilin OR legumin OR globulin OR 7S OR 11S OR \"storage protein\")"
        elif crop_id == "groundnut":
            query = f"organism_id:{tax_id} AND (arachin OR conarachin OR vicilin OR legumin OR \"storage protein\")"
        elif crop_id == "soy":
            query = f"organism_id:{tax_id} AND (glycinin OR conglycinin OR vicilin OR legumin OR \"storage protein\")"
        elif crop_id == "pea":
            query = f"organism_id:{tax_id} AND (vicilin OR convicilin OR legumin OR \"storage protein\")"
        else:
            query = f"organism_id:{tax_id} AND (vicilin OR legumin OR globulin OR 7S OR 11S OR \"storage protein\")"
    else:
        query = f"taxonomy_name:\"{sci_name}\" AND (vicilin OR legumin OR globulin OR \"storage protein\")"

    params = {
        "query": query,
        "format": "json",
        "size": 50,
    }
    headers = {"User-Agent": "Proti-IQ-Research/1.0 (academic; hackathon)"}

    results = []
    try:
        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            resp = client.get(UNIPROT_SEARCH_URL, params=params, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                print(f"  -> Found {len(results)} proteins for {crop_info.get('common_name')}")
            else:
                print(f"Warning: UniProt returned status {resp.status_code} for {sci_name}: {resp.text[:200]}")
    except Exception as e:
        print(f"Error querying UniProt for {sci_name}: {e}")

    # Cache raw response
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return results


def parse_uniprot_entry(entry: Dict[str, Any], crop_id: str) -> Optional[Dict[str, Any]]:
    """Parse raw UniProt JSON item into standard Proti IQ protein dictionary."""
    accession = entry.get("primaryAccession")
    if not accession:
        return None

    # Organism verification
    org_info = entry.get("organism", {})
    entry_tax_id = org_info.get("taxonId")
    entry_sci_name = org_info.get("scientificName", "")

    # Protein name
    desc = entry.get("proteinDescription", {})
    rec_name = desc.get("recommendedName", {}).get("fullName", {}).get("value")
    sub_names = desc.get("submissionNames", [])
    if not rec_name and sub_names:
        rec_name = sub_names[0].get("fullName", {}).get("value")
    name = rec_name or entry.get("uniProtkbId", "Storage protein")

    # Sequence and length
    seq_info = entry.get("sequence", {})
    sequence = seq_info.get("value", "")
    length = seq_info.get("length", len(sequence))
    if not sequence:
        return None

    # Reviewed status (Swiss-Prot = reviewed, TrEMBL = unreviewed)
    reviewed = entry.get("entryType") == "UniProtKB reviewed (Swiss-Prot)"

    # Keywords & Screening flags
    kw_list = [k.get("name", "") for k in entry.get("keywords", []) if k.get("name")]
    screening_flags = extract_screening_flags(kw_list, name)

    # Comments for family classification
    comments = []
    for c in entry.get("comments", []):
        if c.get("commentType") == "SIMILARITY":
            for text_item in c.get("texts", []):
                comments.append(text_item.get("value", ""))
    comment_text = " ".join(comments)

    family = classify_storage_family(name, comment_text, kw_list)

    return {
        "crop_id": crop_id,
        "accession": accession,
        "reviewed": reviewed,
        "name": name,
        "family": family,
        "length": length,
        "sequence": sequence,
        "tax_id": entry_tax_id,
        "organism_name": entry_sci_name,
        "keywords_json": json.dumps({"keywords": kw_list, "screening_flags": screening_flags}),
        "source_release": "UniProtKB 2026_04 (snapshot_2026_04_20261118)",
    }


def ingest_all_crops(db: Session, config_path: str = "config/crops.yaml", force_refresh: bool = False) -> Dict[str, Any]:
    """Ingest storage proteins for all crops defined in config/crops.yaml."""
    with open(config_path, "r", encoding="utf-8") as f:
        crops_data = yaml.safe_load(f)

    all_crops = crops_data.get("benchmarks", []) + crops_data.get("candidates", [])
    coverage_stats = []

    for c in all_crops:
        crop_id = c["id"]
        sci_name = c["scientific_name"]
        cache_path = os.path.join(CACHE_DIR, f"uniprot_{crop_id}.json")

        print(f"Fetching UniProt storage proteins for {c['common_name']} ({sci_name})...")
        raw_entries = query_uniprot_for_crop(c, cache_path, force_refresh=force_refresh)

        count_7s = 0
        count_11s = 0
        count_reviewed = 0
        total_ingested = 0

        for raw_entry in raw_entries:
            parsed = parse_uniprot_entry(raw_entry, crop_id)
            if not parsed:
                continue

            # Organism assertion: verify protein matches the crop's tax_id
            if c.get("tax_id") and parsed.get("tax_id"):
                if parsed["tax_id"] != c["tax_id"]:
                    print(f"  Organism mismatch: {parsed['accession']} taxon {parsed['tax_id']} does not match crop {c['tax_id']} ({sci_name})")
                    continue

            if parsed["family"] == "7S":
                count_7s += 1
            elif parsed["family"] == "11S":
                count_11s += 1
            if parsed["reviewed"]:
                count_reviewed += 1

            # Check if protein already exists in DB
            prot = db.query(Protein).filter(Protein.accession == parsed["accession"]).first()
            if not prot:
                prot = Protein(**parsed)
                db.add(prot)
            else:
                prot.crop_id = parsed["crop_id"]
                prot.name = parsed["name"]
                prot.family = parsed["family"]
                prot.length = parsed["length"]
                prot.sequence = parsed["sequence"]
                prot.tax_id = parsed.get("tax_id")
                prot.organism_name = parsed.get("organism_name")
                prot.reviewed = parsed["reviewed"]
                prot.keywords_json = parsed["keywords_json"]
                prot.source_release = parsed.get("source_release")
            total_ingested += 1

        db.commit()

        # Decision rule: candidate stays if >= 1 7S or 11S; otherwise mark 'No Data'
        keep_decision = "Keep" if (count_7s + count_11s > 0) else "No Data / Unranked"

        coverage_stats.append({
            "crop_id": crop_id,
            "common_name": c["common_name"],
            "scientific_name": sci_name,
            "role": c["role"],
            "total_proteins": total_ingested,
            "count_7S": count_7s,
            "count_11S": count_11s,
            "count_reviewed": count_reviewed,
            "decision": keep_decision,
        })
        time.sleep(0.5)  # Polite API interval

    # Write coverage report CSV
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    report_file = os.path.join(PROCESSED_DIR, "coverage_report.csv")
    with open(report_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "crop_id", "common_name", "scientific_name", "role",
            "total_proteins", "count_7S", "count_11S", "count_reviewed", "decision"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(coverage_stats)

    print(f"Coverage report written to {report_file}")
    return {"coverage": coverage_stats}


def run_ingest(force_refresh: bool = True):
    init_db()
    db = SessionLocal()
    try:
        ingest_all_crops(db, force_refresh=force_refresh)
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    refresh = "--no-refresh" not in sys.argv
    run_ingest(force_refresh=refresh)
