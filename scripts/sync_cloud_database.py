import sqlite3
import urllib.request
import json
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://dzbcefkvzufomdpfjmrw.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=ignore-duplicates,return=minimal"
}

def post_batch(endpoint, rows):
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    req = urllib.request.Request(url, data=json.dumps(rows).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode()
    except urllib.error.HTTPError as e:
        print(f"Error on {endpoint}: {e.code} - {e.read().decode()}")
        raise

def sync():
    sqlite_conn = sqlite3.connect("data/proti_iq.db")
    sqlite_conn.row_factory = sqlite3.Row
    cur = sqlite_conn.cursor()

    # 1. Sync Proteins
    print("=== 1. Syncing Proteins ===")
    cur.execute("SELECT * FROM proteins;")
    sqlite_proteins = cur.fetchall()
    
    crop_map = {
        "soy": "soybean",
        "pea": "field_pea"
    }

    # Deduplicate by accession
    seen_acc = set()
    deduped_proteins = []
    for p in sqlite_proteins:
        if p["accession"] in seen_acc:
            continue
        seen_acc.add(p["accession"])
        kw = json.loads(p["keywords_json"]) if p["keywords_json"] else []
        family = p["family"] if p["family"] in ["7S", "11S"] else "other"
        cid = crop_map.get(p["crop_id"], p["crop_id"])
        deduped_proteins.append({
            "crop_id": cid,
            "accession": p["accession"],
            "reviewed": bool(p["reviewed"]),
            "name": p["name"],
            "family": family,
            "length": p["length"],
            "sequence": p["sequence"],
            "keywords": kw,
            "alphafold_available": bool(p["alphafold_available"]),
            "plddt_mean": p["plddt_mean"],
            "tax_id": p["tax_id"],
            "organism_name": p["organism_name"],
            "source_release": p["source_release"] or "UniProtKB 2026_04"
        })
    protein_rows = deduped_proteins
    
    # Fetch existing accessions to prevent duplicate conflicts
    fetch_req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/proteins?select=accession",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    )
    with urllib.request.urlopen(fetch_req) as resp:
        existing_acc = set(p["accession"] for p in json.loads(resp.read().decode()))
    print(f"Already in Supabase: {len(existing_acc)} proteins")

    to_insert = [p for p in protein_rows if p["accession"] not in existing_acc]
    print(f"Remaining proteins to insert: {len(to_insert)}")

    # Insert in batches of 50
    batch_size = 50
    for i in range(0, len(to_insert), batch_size):
        batch = to_insert[i:i + batch_size]
        post_batch("proteins", batch)
        print(f"  Synced proteins {i+1} to {min(i+batch_size, len(to_insert))} / {len(to_insert)}")

    # Fetch newly inserted proteins to get their IDs by accession
    fetch_req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/proteins?select=id,accession",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    )
    with urllib.request.urlopen(fetch_req) as resp:
        sb_proteins = json.loads(resp.read().decode())
    acc_to_sb_id = {p["accession"]: p["id"] for p in sb_proteins}
    print(f"Supabase proteins loaded: {len(acc_to_sb_id)}")

    # Map SQLite protein_id -> accession -> Supabase protein_id
    cur.execute("SELECT id, accession FROM proteins;")
    sqlite_id_to_acc = {r["id"]: r["accession"] for r in cur.fetchall()}
    sqlite_id_to_sb_id = {sid: acc_to_sb_id.get(acc) for sid, acc in sqlite_id_to_acc.items() if acc in acc_to_sb_id}

    # 2. Sync Rankings for run_383377
    print("=== 2. Syncing Rankings (run_383377) ===")
    cur.execute("SELECT * FROM rankings WHERE run_id = 'run_383377';")
    sqlite_rankings = cur.fetchall()
    print(f"Found {len(sqlite_rankings)} rankings in SQLite for run_383377")

    ranking_rows = []
    for r in sqlite_rankings:
        sb_pid = sqlite_id_to_sb_id.get(r["protein_id"])
        if not sb_pid:
            continue
        contrib = json.loads(r["contributions_json"]) if r["contributions_json"] else {}
        flags = json.loads(r["flags_json"]) if r["flags_json"] else []
        conf = r["confidence"] if r["confidence"] in ["High", "Medium", "Low"] else "Medium"
        cid = crop_map.get(r["crop_id"], r["crop_id"])
        ranking_rows.append({
            "run_id": "run_383377",
            "job": r["job"],
            "benchmark_id": r["benchmark_id"],
            "crop_id": cid,
            "protein_id": sb_pid,
            "score": round(float(r["score"]), 3),
            "confidence": conf,
            "contributions": contrib,
            "flags": flags
        })

    for i in range(0, len(ranking_rows), batch_size):
        batch = ranking_rows[i:i + batch_size]
        post_batch("rankings", batch)
        print(f"  Synced rankings {i+1} to {min(i+batch_size, len(ranking_rows))} / {len(ranking_rows)}")

    # 3. Sync Measurements
    print("=== 3. Syncing Measurements ===")
    cur.execute("SELECT * FROM measurements;")
    sqlite_measurements = cur.fetchall()
    measurement_rows = []
    for m in sqlite_measurements:
        measurement_rows.append({
            "crop_id": m["crop_id"],
            "job": m["job"],
            "property": m["property"],
            "value": float(m["value"]),
            "unit": m["unit"],
            "conditions": m["conditions"],
            "study_id": m["study_id"],
            "citation": m["citation"],
            "verified_by": m["verified_by"],
            "notes": m["notes"]
        })
    if measurement_rows:
        post_batch("measurements", measurement_rows)
        print(f"Synced {len(measurement_rows)} empirical lab measurements.")

    sqlite_conn.close()
    print("=== SYNC COMPLETE! All data populated to Supabase Cloud ===")

if __name__ == "__main__":
    sync()
