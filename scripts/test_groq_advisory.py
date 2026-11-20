"""Test that the Groq LLM key is live and generating real advisory text."""
import sys, os
sys.path.append(os.path.abspath("."))
from dotenv import load_dotenv
load_dotenv()

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# Test consumer advisory and check if LLM is active
payload = {"role": "consumer", "job": "egg", "crop_id": "pigeon_pea"}
r = client.post("/api/v1/hub/advisory/formulate", json=payload)
data = r.json()

print("=== Groq LLM Integration Test ===")
print(f"Status: {r.status_code}")
print(f"AI Provider: {data.get('ai_provider', 'MISSING')}")
if data.get("ai_generative_advisory"):
    advice = data["ai_generative_advisory"]
    print(f"LLM Response ({len(advice)} chars): {advice[:200]}...")
else:
    print("[WARNING] No LLM response returned. Falling back to rule-base.")
    print("Check that GROQ_API_KEY is set in .env and the FastAPI server reloads env vars.")

# Test all 3 personas
for role in ["consumer", "nutritionist", "food_processor"]:
    r2 = client.post("/api/v1/hub/advisory/formulate", json={"role": role, "job": "milk", "crop_id": "cowpea"})
    d2 = r2.json()
    provider = d2.get("ai_provider", "UNKNOWN")
    has_llm = bool(d2.get("ai_generative_advisory"))
    print(f"  [{role}] -> {provider} | LLM active: {has_llm}")
