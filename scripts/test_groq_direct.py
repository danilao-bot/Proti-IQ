"""Direct test of Groq API call outside of FastAPI."""
import os
from dotenv import load_dotenv
load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
print(f"Key present: {bool(groq_key)}, starts with: {groq_key[:10]}...")

import httpx

prompt = (
    "You are the Proti IQ African Alternative-Protein Advisory AI.\n"
    "Persona: Consumer / Caregiver\n"
    "Target Application: Plant-Based Egg Gel\n"
    "Selected Crop: pigeon_pea\n"
    "Provide 3 concise, practical, expert recommendations."
)

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "system", "content": "You are the Proti IQ African Alternative-Protein Advisory AI."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.2,
    "max_tokens": 300
}

try:
    with httpx.Client(timeout=10.0) as client:
        resp = client.post(url, headers=headers, json=payload)
        print(f"HTTP Status: {resp.status_code}")
        if resp.status_code == 200:
            text = resp.json()["choices"][0]["message"]["content"]
            print(f"LLM Response ({len(text)} chars):")
            print(text)
        else:
            print(f"Error body: {resp.text}")
except Exception as e:
    print(f"Exception: {type(e).__name__}: {e}")
