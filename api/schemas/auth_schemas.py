"""
Pydantic Schemas for Onboarding, Session Verification, and Data Deletion.
"""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


ALLOWED_COUNTRIES = ["Nigeria", "Ghana", "Kenya", "South Africa"]


class OnboardingRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=13, le=120, description="Users must be at least 13 years old")
    country: str = Field(..., description="Target African market")
    region: Optional[str] = Field(None, max_length=100)
    mission: str = Field(..., description="Primary user objective")
    scale: str = Field(..., description="Operating scale or facility")
    consent_given: bool = Field(..., description="Required consent to terms and privacy policy")
    cookie_consent: bool = Field(..., description="Consent to essential session cookies")

    @field_validator("country")
    def validate_country(cls, v):
        for c in ALLOWED_COUNTRIES:
            if v.strip().lower() == c.lower():
                return c
        raise ValueError(f"Country must be one of: {', '.join(ALLOWED_COUNTRIES)}")

    @field_validator("consent_given")
    def validate_consent(cls, v):
        if not v:
            raise ValueError("You must accept the Terms of Service and Privacy Policy to proceed")
        return v

    @field_validator("cookie_consent")
    def validate_cookie(cls, v):
        if not v:
            raise ValueError("Essential session cookies are required to operate your workspace")
        return v


class OnboardingResponse(BaseModel):
    session_token: str
    user_id: str
    full_name: str
    age: int
    assigned_role: str
    role_title: str
    geriatric_mode: bool
    country: str
    accessible_routes: List[str]
    message: str


class SessionResponse(BaseModel):
    authenticated: bool
    user_id: Optional[str] = None
    full_name: Optional[str] = None
    age: Optional[int] = None
    country: Optional[str] = None
    region: Optional[str] = None
    assigned_role: Optional[str] = None
    role_title: Optional[str] = None
    geriatric_mode: Optional[bool] = None
    accessible_routes: Optional[List[str]] = None


class DeleteDataResponse(BaseModel):
    success: bool
    user_id: str
    message: str
    deleted_at: str
