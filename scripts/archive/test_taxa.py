import urllib.request
import urllib.parse
import json

queries = {
    "Cowpea": ("3917", "organism_id:3917 AND (vicilin OR legumin OR \"storage protein\")"),
    "Bambara groundnut": ("115715", "organism_id:115715 AND (vicilin OR legumin OR \"storage protein\")"),
    "Bambara (name search)": ("", 'organism_name:"Vigna subterranea" AND (vicilin OR legumin OR "storage protein")'),
    "Pigeon pea": ("3821", "organism_id:3821 AND (vicilin OR legumin OR \"storage protein\")"),
    "African yam bean (92480)": ("92480", "organism_id:92480 AND (vicilin OR legumin OR \"storage protein\")"),
    "African yam bean (name)": ("", 'organism_name:"Sphenostylis stenocarpa" AND (vicilin OR legumin OR "storage protein")'),
    "Groundnut": ("3818", "organism_id:3818 AND (vicilin OR legumin OR \"storage protein\" OR arachin)"),
    "Mung bean": ("3916", "organism_id:3916 AND (vicilin OR legumin OR \"storage protein\")"),
    "Soybean": ("3847", "organism_id:3847 AND (vicilin OR legumin OR \"storage protein\" OR glycinin OR conglycinin)"),
    "Field pea": ("3888", "organism_id:3888 AND (vicilin OR legumin OR \"storage protein\")")
}

for name, (taxid, q) in queries.items():
    url = f"https://rest.uniprot.org/uniprotkb/search?query={urllib.parse.quote(q)}&size=50"
    req = urllib.request.Request(url, headers={"User-Agent": "ProtiIQ/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            total = len(data.get("results", []))
            reviewed = sum(1 for p in data.get("results", []) if p.get("entryType") == "UniProtKB reviewed (Swiss-Prot)")
            print(f"{name:<26} | Total: {total:<3} | Rev: {reviewed:<2} | Query: {q}")
    except Exception as e:
        print(f"{name:<26} | Error: {e}")
