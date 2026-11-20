import sys, os
sys.path.append(os.path.abspath("."))
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# 1. Test /health
r = client.get("/health")
print("Health:", r.status_code, r.json()["status"])

# 2. Test /api/v1/hub/applications
r = client.get("/api/v1/hub/applications")
data = r.json()
print("Hub Applications:", r.status_code, f"{data['total_categories']} categories")

# 3. Test /api/v1/hub/rankings for meat
r = client.get("/api/v1/hub/rankings?job=meat&country=Nigeria")
data = r.json()
top = data['top_pick']
print(f"Hub Rankings (meat): {r.status_code} | Top: {top['crop_name']} ({top['biophysical_similarity_score']}%)")

# 4. Test /api/v1/hub/advisory/formulate (Consumer)
payload = {"role": "consumer", "job": "milk", "crop_id": "cowpea"}
r = client.post("/api/v1/hub/advisory/formulate", json=payload)
data = r.json()
print(f"Advisory Consumer: {r.status_code} | {data['application']} | {len(data['kitchen_instructions'])} kitchen steps")

# 5. Test /api/v1/hub/advisory/formulate (Nutritionist)
payload = {"role": "nutritionist", "job": "sarcopenia", "crop_id": "cowpea", "older_person_mode": True}
r = client.post("/api/v1/hub/advisory/formulate", json=payload)
data = r.json()
print(f"Advisory Nutritionist: {r.status_code} | {data['delivered_protein_density']}")

# 6. Test /api/v1/hub/advisory/formulate (Food Processor)
payload = {"role": "food_processor", "job": "gel", "crop_id": "african_yam_bean"}
r = client.post("/api/v1/hub/advisory/formulate", json=payload)
data = r.json()
print(f"Advisory Food Processor: {r.status_code} | Breaking stress: {data['quality_assurance_spec']['target_breaking_stress']}")
