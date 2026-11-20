"""
Proti IQ — Supabase Sync Utility.
Syncs precomputed rankings, crops, and jobs from local SQLite to Supabase Cloud via PostgREST.
Reads credentials strictly from environment variables (.env).
"""

import os
import sys
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://dzbcefkvzufomdpfjmrw.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

def test_supabase_health():
    """Checks if Supabase instance is live and responsive."""
    if not SUPABASE_KEY:
        print("[ERROR] SUPABASE_SERVICE_KEY not set in .env. Please configure .env first.")
        return False

    url = f"{SUPABASE_URL}/rest/v1/"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[SUCCESS] Connected to Supabase Cloud at {SUPABASE_URL} (HTTP {resp.getcode()})")
            return True
    except Exception as e:
        print(f"[ERROR] Failed to connect to Supabase: {e}")
        return False

def check_tables():
    """Checks which tables have been created by Precious."""
    if not SUPABASE_KEY:
        return []

    url = f"{SUPABASE_URL}/rest/v1/"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            defs = list(data.get("definitions", {}).keys())
            if defs:
                print(f"[INFO] Tables detected in Supabase ({len(defs)}): {defs}")
            else:
                print("[NOTICE] No tables detected yet. Precious needs to run docs/SUPABASE_POSTGRESQL_SCHEMA.sql in Supabase SQL Editor.")
            return defs
    except Exception as e:
        print(f"[ERROR] Error checking tables: {e}")
        return []

if __name__ == "__main__":
    print("=== Proti IQ Supabase Diagnostics ===")
    if test_supabase_health():
        check_tables()
