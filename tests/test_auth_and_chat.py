"""
Unit and Integration Tests for Auth, RBAC Resolution, Chat, and Legal Endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app
from services.rbac_service import resolve_role

client = TestClient(app)


def test_rbac_resolution_consumer_older_adult():
    res = resolve_role(age=58, mission="family meals", scale="household")
    assert res["assigned_role"] == "consumer"
    assert res["geriatric_mode"] is True
    assert "hub" in res["accessible_routes"]


def test_rbac_resolution_clinical_nutritionist():
    res = resolve_role(age=34, mission="clinical diet", scale="clinical")
    assert res["assigned_role"] == "nutritionist"
    assert res["geriatric_mode"] is False
    assert "evidence" in res["accessible_routes"]


def test_rbac_resolution_industrial_processor():
    res = resolve_role(age=42, mission="commercial manufacturing", scale="factory")
    assert res["assigned_role"] == "processor"
    assert "structure" in res["accessible_routes"]


def test_rbac_resolution_researcher():
    res = resolve_role(age=29, mission="molecular research", scale="laboratory")
    assert res["assigned_role"] == "researcher"


def test_onboarding_and_session_cycle():
    # 1. Test onboarding
    payload = {
        "full_name": "Keemka Test",
        "age": 52,
        "country": "Nigeria",
        "region": "Oyo State",
        "mission": "family meals",
        "scale": "household",
        "consent_given": True,
        "cookie_consent": True
    }
    resp = client.post("/api/v1/auth/onboard", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "session_token" in data
    assert data["assigned_role"] == "consumer"
    assert data["geriatric_mode"] is True

    token = data["session_token"]

    # 2. Test session verification
    sess_resp = client.get("/api/v1/auth/session", headers={"Authorization": f"Bearer {token}"})
    assert sess_resp.status_code == 200
    sess_data = sess_resp.json()
    assert sess_data["authenticated"] is True
    assert sess_data["full_name"] == "Keemka Test"
    assert sess_data["assigned_role"] == "consumer"

    # 3. Test data deletion
    del_resp = client.post("/api/v1/auth/delete-data", headers={"Authorization": f"Bearer {token}"})
    assert del_resp.status_code == 200
    assert del_resp.json()["success"] is True

    # 4. Verify session is no longer valid after deletion
    post_del = client.get("/api/v1/auth/session", headers={"Authorization": f"Bearer {token}"})
    assert post_del.json()["authenticated"] is False


def test_onboarding_underage_blocked():
    payload = {
        "full_name": "Underage Kid",
        "age": 12,
        "country": "Nigeria",
        "mission": "family meals",
        "scale": "household",
        "consent_given": True,
        "cookie_consent": True
    }
    resp = client.post("/api/v1/auth/onboard", json=payload)
    assert resp.status_code == 422  # Pydantic validation ge=13 blocks it


def test_chat_suggestions_endpoint():
    resp = client.get("/api/v1/chat/suggestions?role=consumer")
    assert resp.status_code == 200
    assert len(resp.json()["suggestions"]) > 0


def test_legal_documents():
    for doc in ["privacy", "terms", "cookies"]:
        resp = client.get(f"/api/v1/legal/{doc}")
        assert resp.status_code == 200
        assert len(resp.json()["content"]) > 50


def test_export_recipe_endpoint():
    payload = {
        "user_name": "Keemka",
        "country": "Nigeria",
        "crop_name": "Cowpea",
        "job_name": "Milk",
        "role": "consumer"
    }
    resp = client.post("/api/v1/export/recipe", json=payload)
    assert resp.status_code == 200
    assert "PROTI IQ CULINARY RECIPE CARD" in resp.text
