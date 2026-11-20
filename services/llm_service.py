"""
Proti IQ Multi-Provider LLM Advisory Service.
Interfaces with Groq Cloud (Qwen 3.8-27b), Google Gemini, OpenRouter, or falls back to Expert Biophysical Rules.
"""

import os
from typing import Optional, Dict, Any

try:
    import httpx
    has_httpx = True
except ImportError:
    has_httpx = False


def generate_advisory(role: str, application: str, crop: str, context: str) -> Dict[str, Any]:
    """
    Queries live cloud LLMs in priority order (Groq -> Gemini -> OpenRouter).
    If offline or no key is configured, seamlessly returns Proti IQ Expert Biophysical Rules.
    """
    groq_key = os.getenv("GROQ_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")

    prompt = (
        f"You are the Proti IQ African Alternative-Protein Advisory AI.\n"
        f"Persona: {role}\nTarget Application: {application}\nSelected Crop: {crop}\n"
        f"Biochemical Context: {context}\n"
        f"Provide 3 concise, practical, expert recommendations for this food preparation or clinical formulation."
    )

    if has_httpx:
        try:
            with httpx.Client(timeout=15.0) as client:
                # 1. Option: Groq Cloud (Free at console.groq.com)
                if groq_key:
                    url = "https://api.groq.com/openai/v1/chat/completions"
                    headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                    for model in ["qwen/qwen3.8-27b", "openai/gpt-oss-20b", "llama-3.3-70b-versatile"]:
                        payload = {
                            "model": model,
                            "messages": [
                                {"role": "system", "content": "You are the Proti IQ African Alternative-Protein Advisory AI."},
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": 0.2,
                            "max_tokens": 350
                        }
                        resp = client.post(url, headers=headers, json=payload)
                        if resp.status_code == 200:
                            content = resp.json()["choices"][0]["message"]["content"].strip()
                            return {
                                "advisory_text": content,
                                "provider": f"Groq Cloud ({model})",
                                "status": "live"
                            }
                        if resp.status_code != 404:
                            break

                # 2. Option: Google Gemini API (Free at aistudio.google.com)
                if gemini_key:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                    payload = {"contents": [{"parts": [{"text": prompt}]}]}
                    resp = client.post(url, json=payload)
                    if resp.status_code == 200:
                        content = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                        return {
                            "advisory_text": content,
                            "provider": "Google Gemini (1.5-Flash)",
                            "status": "live"
                        }

                # 3. Option: OpenRouter Free Tier
                if openrouter_key:
                    url = "https://openrouter.ai/api/v1/chat/completions"
                    headers = {"Authorization": f"Bearer {openrouter_key}", "Content-Type": "application/json"}
                    payload = {
                        "model": "meta-llama/llama-3.1-8b-instruct:free",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 300
                    }
                    resp = client.post(url, headers=headers, json=payload)
                    if resp.status_code == 200:
                        content = resp.json()["choices"][0]["message"]["content"].strip()
                        return {
                            "advisory_text": content,
                            "provider": "OpenRouter (Llama 3.1)",
                            "status": "live"
                        }
        except Exception:
            pass

    # Offline / Rule-Base Fallback
    return {
        "advisory_text": None,
        "provider": "Proti IQ Expert Bio-Rules",
        "status": "offline_rule_base"
    }
