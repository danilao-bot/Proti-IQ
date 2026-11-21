"""
Authentication, Onboarding, and Data Privacy Endpoints for Proti IQ.
Handles deterministic RBAC profile creation, session verification, and authentic data deletion.
"""

from datetime import datetime, timezone, timedelta
import os
import uuid
from typing import Optional
import jwt
from fastapi import APIRouter, HTTPException, Depends, Header, Request, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from api.db import get_db, UserProfile, engine as local_engine
from api.schemas.auth_schemas import (
    OnboardingRequest,
    OnboardingResponse,
    SessionResponse,
    DeleteDataResponse
)
from services.rbac_service import resolve_role, ROLE_METADATA

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

JWT_SECRET = os.getenv("JWT_SECRET", "proti-iq-2026-hack-the-fork-secure-session-key-64chars-min-production-secret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


def create_session_jwt(user_id: str, role: str, country: str, geriatric_mode: bool) -> str:
    """Generates a signed JWT session token valid for 24 hours."""
    payload = {
        "sub": user_id,
        "role": role,
        "country": country,
        "geriatric": geriatric_mode,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_session_jwt(token: str) -> dict:
    """Decodes and validates a session JWT."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired. Please onboard again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token.")


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> UserProfile:
    """Dependency that verifies JWT and returns the active user profile."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header.")
    
    token = authorization.split(" ")[1]
    payload = decode_session_jwt(token)
    user_id = payload.get("sub")

    user = db.query(UserProfile).filter(UserProfile.id == user_id, UserProfile.deleted_at.is_(None)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found or has been deleted.")
    return user


def sync_user_to_supabase(user_dict: dict):
    """Syncs created user profile to Supabase PostgreSQL."""
    supabase_db_url = os.getenv("SUPABASE_DB_URL")
    if not supabase_db_url:
        return
    try:
        from sqlalchemy import create_engine
        supa_engine = create_engine(supabase_db_url)
        with supa_engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO user_profiles (
                        id, full_name, age, country, region, mission, scale,
                        assigned_role, geriatric_mode, consent_given, cookie_consent, created_at, last_login_at
                    ) VALUES (
                        :id, :full_name, :age, :country, :region, :mission, :scale,
                        :assigned_role, :geriatric_mode, :consent_given, :cookie_consent, NOW(), NOW()
                    )
                    ON CONFLICT (id) DO UPDATE SET
                        last_login_at = NOW(),
                        assigned_role = EXCLUDED.assigned_role,
                        geriatric_mode = EXCLUDED.geriatric_mode;
                """),
                user_dict
            )
            conn.commit()
    except Exception as e:
        print("Warning: Supabase user sync error:", e)


def delete_user_from_supabase(user_id: str):
    """Executes true row deletion from Supabase PostgreSQL."""
    supabase_db_url = os.getenv("SUPABASE_DB_URL")
    if not supabase_db_url:
        return
    try:
        from sqlalchemy import create_engine
        supa_engine = create_engine(supabase_db_url)
        with supa_engine.connect() as conn:
            conn.execute(
                text("DELETE FROM user_profiles WHERE id = :id"),
                {"id": user_id}
            )
            conn.commit()
    except Exception as e:
        print("Warning: Supabase deletion error:", e)


@router.post("/onboard", response_model=OnboardingResponse, summary="Onboard User & Resolve Locked Role")
def onboard_user(req: OnboardingRequest, db: Session = Depends(get_db)):
    """
    Submits onboarding questions, deterministically resolves RBAC persona,
    persists profile to both SQLite and Supabase, and returns signed session JWT.
    """
    # 1. Deterministic RBAC role resolution
    resolution = resolve_role(req.age, req.mission, req.scale)
    role = resolution["assigned_role"]
    geriatric = resolution["geriatric_mode"]

    user_id = str(uuid.uuid4())
    now_utc = datetime.now(timezone.utc)

    # 2. Persist in local SQLite database
    profile = UserProfile(
        id=user_id,
        full_name=req.full_name.strip(),
        age=req.age,
        country=req.country.strip(),
        region=req.region.strip() if req.region else None,
        mission=req.mission.strip(),
        scale=req.scale.strip(),
        assigned_role=role,
        geriatric_mode=geriatric,
        consent_given=req.consent_given,
        cookie_consent=req.cookie_consent,
        created_at=now_utc,
        last_login_at=now_utc
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    # 3. Mirror to Supabase Cloud PostgreSQL
    sync_user_to_supabase({
        "id": user_id,
        "full_name": profile.full_name,
        "age": profile.age,
        "country": profile.country,
        "region": profile.region,
        "mission": profile.mission,
        "scale": profile.scale,
        "assigned_role": profile.assigned_role,
        "geriatric_mode": profile.geriatric_mode,
        "consent_given": profile.consent_given,
        "cookie_consent": profile.cookie_consent
    })

    # 4. Generate signed session token
    token = create_session_jwt(user_id, role, profile.country, geriatric)

    return OnboardingResponse(
        session_token=token,
        user_id=user_id,
        full_name=profile.full_name,
        age=profile.age,
        assigned_role=role,
        role_title=resolution["role_title"],
        geriatric_mode=geriatric,
        country=profile.country,
        accessible_routes=resolution["accessible_routes"],
        message=f"Workspace configured successfully for {resolution['role_title']}."
    )


@router.get("/session", response_model=SessionResponse, summary="Validate Active Session")
def get_session(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """
    Checks session JWT. If valid and user exists, returns profile and locked role.
    Allows returning users to bypass onboarding directly into their workspace.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return SessionResponse(authenticated=False)

    token = authorization.split(" ")[1]
    try:
        payload = decode_session_jwt(token)
    except HTTPException:
        return SessionResponse(authenticated=False)

    user_id = payload.get("sub")
    user = db.query(UserProfile).filter(UserProfile.id == user_id, UserProfile.deleted_at.is_(None)).first()
    if not user:
        return SessionResponse(authenticated=False)

    # Update last login timestamp
    user.last_login_at = datetime.now(timezone.utc)
    db.commit()

    meta = ROLE_METADATA.get(user.assigned_role, ROLE_METADATA["consumer"])

    return SessionResponse(
        authenticated=True,
        user_id=user.id,
        full_name=user.full_name,
        age=user.age,
        country=user.country,
        region=user.region,
        assigned_role=user.assigned_role,
        role_title=meta["title"],
        geriatric_mode=user.geriatric_mode,
        accessible_routes=meta["accessible_routes"]
    )


@router.post("/delete-data", response_model=DeleteDataResponse, summary="Permanent User Data Deletion")
def delete_user_data(current_user: UserProfile = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Permanently deletes all stored user data from local database and Supabase PostgreSQL.
    Enforces GDPR Article 17 and Nigerian Data Protection Act compliance.
    """
    user_id = current_user.id
    now_iso = datetime.now(timezone.utc).isoformat()

    # 1. Delete from local SQLite
    db.delete(current_user)
    db.commit()

    # 2. Delete from Supabase PostgreSQL
    delete_user_from_supabase(user_id)

    return DeleteDataResponse(
        success=True,
        user_id=user_id,
        message="All personal user profile data has been permanently deleted from Proti IQ servers.",
        deleted_at=now_iso
    )
