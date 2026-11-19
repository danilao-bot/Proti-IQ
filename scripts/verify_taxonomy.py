import urllib.request
import urllib.parse
import json
import yaml

with open("config/crops.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

crops = cfg.get("benchmarks", []) + cfg.get("candidates", [])

print("--- UNIPROT TAXONOMY VERIFICATION ---")
for c in crops:
    tid = c.get("tax_id")
    expected_sci = c.get("scientific_name")
    common = c.get("common_name")
    url = f"https://rest.uniprot.org/taxonomy/{tid}"
    req = urllib.request.Request(url, headers={"User-Agent": "ProtiIQ/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            actual_sci = data.get("scientificName")
            other_names = data.get("otherNames", [])
            match = (actual_sci.lower() == expected_sci.lower()) or any(expected_sci.lower() in o.lower() for o in other_names)
            print(f"[{'PASS' if match else 'FAIL'}] {common} (ID: {tid}):")
            print(f"   Expected: {expected_sci}")
            print(f"   Actual:   {actual_sci}")
            if other_names:
                print(f"   Synonyms: {', '.join(other_names[:3])}")
    except Exception as e:
        print(f"[ERROR] {common} (ID: {tid}): {e}")

print("\n--- SEARCHING VOANDZEIA SUBTERRANEA ---")
url = "https://rest.uniprot.org/taxonomy/search?query=Voandzeia+subterranea"
req = urllib.request.Request(url, headers={"User-Agent": "ProtiIQ/1.0"})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode())
    for r in data.get("results", []):
        print(f"TaxonId: {r.get('taxonId')} | ScientificName: {r.get('scientificName')} | Other: {r.get('otherNames')}")
