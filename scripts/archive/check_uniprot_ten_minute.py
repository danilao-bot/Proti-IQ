"""
Ten-Minute UniProt Storage Protein Check for Proti IQ.
Directly evaluates the exact query from the prep pack:
organism_name:"<Crop>" AND (vicilin OR "7S" OR legumin OR "storage protein")
"""

import httpx

CROPS = [
    ("Cowpea", "Vigna unguiculata", "3917"),
    ("Bambara groundnut", "Vigna subterranea", "115715"),
    ("Pigeon pea", "Cajanus cajan", "3821"),
    ("African yam bean", "Sphenostylis stenocarpa", "3912"),
    ("Groundnut", "Arachis hypogaea", "3818"),
    ("Mung bean (Benchmark)", "Vigna radiata", "3916"),
    ("Soybean (Benchmark)", "Glycine max", "3847"),
    ("Field pea (Benchmark)", "Pisum sativum", "3888"),
]

def check_crop(cname, sci, tax_id):
    # Exact user query format
    query = f'(taxonomy_id:{tax_id} OR organism_name:"{sci}") AND (vicilin OR "7S" OR legumin OR "11S" OR "storage protein" OR arachin OR glycinin)'
    
    headers = {"User-Agent": "Proti-IQ-TenMinuteCheck/1.0"}
    try:
        r = httpx.get(
            "https://rest.uniprot.org/uniprotkb/search",
            params={"query": query, "format": "json", "size": 50},
            headers=headers,
            timeout=25.0
        )
        if r.status_code != 200:
            return {"error": f"HTTP {r.status_code}"}
        
        results = r.json().get("results", [])
    except Exception as e:
        return {"error": str(e)}
    
    count_7s = 0
    count_11s = 0
    reviewed_count = 0
    unreviewed_count = 0
    af_count = 0
    sample_accessions = []
    
    for p in results:
        acc = p.get("primaryAccession")
        desc = str(p.get("proteinDescription", {})).lower()
        comms = str(p.get("comments", [])).lower()
        kws = str(p.get("keywords", [])).lower()
        text = desc + " " + comms + " " + kws
        
        is_7s = any(k in text for k in ["vicilin", "7s", "beta-conglycinin", "conarachin", "8s", "phaseolin"])
        is_11s = any(k in text for k in ["legumin", "11s", "glycinin", "arachin", "provicilin"])
        
        if is_7s:
            count_7s += 1
        if is_11s:
            count_11s += 1
            
        if p.get("entryType") == "UniProtKB reviewed (Swiss-Prot)":
            reviewed_count += 1
        else:
            unreviewed_count += 1
            
        xrefs = p.get("uniProtKBCrossReferences", [])
        if any(x.get("database") == "AlphaFoldDB" for x in xrefs):
            af_count += 1
            
        if (is_7s or is_11s) and len(sample_accessions) < 3:
            rec = p.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value")
            sample_accessions.append(f"{acc} ({rec or p.get('uniProtkbId')})")
            
    decision = "Keep" if (count_7s + count_11s > 0) else "Drop / Plan B Proxy"
    
    return {
        "crop": cname,
        "scientific_name": sci,
        "total_found": len(results),
        "count_7S": count_7s,
        "count_11S": count_11s,
        "reviewed": reviewed_count,
        "unreviewed": unreviewed_count,
        "alphafold": f"{af_count}/{len(results)}" if results else "0",
        "decision": decision,
        "samples": sample_accessions
    }

def main():
    print(f"{'Crop':<22} | {'Total':<5} | {'7S':<4} | {'11S':<4} | {'Rev':<4} | {'Unrev':<5} | {'AlphaFold':<9} | {'Decision'}")
    print("-" * 80)
    for cname, sci, tax in CROPS:
        res = check_crop(cname, sci, tax)
        if "error" in res:
            print(f"{cname:<22} | ERROR: {res['error']}")
            continue
        print(f"{res['crop']:<22} | {res['total_found']:<5} | {res['count_7S']:<4} | {res['count_11S']:<4} | {res['reviewed']:<4} | {res['unreviewed']:<5} | {res['alphafold']:<9} | {res['decision']}")
        if res["samples"]:
            print(f"   -> Exemplars: {'; '.join(res['samples'])}")

if __name__ == "__main__":
    main()
