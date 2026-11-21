"""
Legal Policy Endpoints for Proti IQ.
Serves authoritative markdown content for Privacy Policy, Terms of Service, and Cookie Policy.
"""

import os
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v1/legal", tags=["legal"])

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "docs")


def read_doc_file(filename: str) -> str:
    path = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Legal document {filename} not found.")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@router.get("/privacy", summary="Get Privacy Policy")
def get_privacy_policy():
    return {"title": "Privacy Policy", "content": read_doc_file("PRIVACY_POLICY.md")}


@router.get("/terms", summary="Get Terms of Service")
def get_terms_of_service():
    return {"title": "Terms of Service", "content": read_doc_file("TERMS_OF_SERVICE.md")}


@router.get("/cookies", summary="Get Cookie Policy")
def get_cookie_policy():
    return {"title": "Cookie Policy", "content": read_doc_file("COOKIE_POLICY.md")}
