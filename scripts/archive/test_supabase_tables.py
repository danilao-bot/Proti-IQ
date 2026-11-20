import urllib.request
import json
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("SUPABASE_SERVICE_KEY")
tables = ["crops", "jobs", "meals", "proteins", "rankings", "measurements", "lab_protocols", "advisory_inquiries"]

print("=== Testing Direct Table Queries on Supabase ===")
for tbl in tables:
    url = f"https://dzbcefkvzufomdpfjmrw.supabase.co/rest/v1/{tbl}?select=*"
    req = urllib.request.Request(url, headers={"apikey": key, "Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"Table [{tbl}]: SUCCESS ({len(data)} rows)")
            if data and tbl == "crops":
                sample = [d.get("common_name", "") for d in data[:5]]
                print(f"   -> Crops: {sample}")
            elif data and tbl == "jobs":
                sample = [d.get("name", "") for d in data[:3]]
                print(f"   -> Jobs: {sample}")
            elif data and tbl == "meals":
                sample = [d.get("name", "") for d in data[:5]]
                print(f"   -> Meals: {sample}")
    except Exception as e:
        print(f"Table [{tbl}]: {e}")
