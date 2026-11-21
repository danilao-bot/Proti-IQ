"""
Database Models and Engine for Proti IQ
SQLAlchemy 2.0 ORM schemas supporting SQLite (local dev) and PostgreSQL 16 (production).
Provides read-only session for API and writer session for pipeline.
"""

from datetime import datetime, timezone
import json
import os
from typing import Any, Dict, List, Optional
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/proti_iq.db")

# Ensure directory for sqlite exists
if DATABASE_URL.startswith("sqlite"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=5,
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ---------------------------------------------------------
# Database Models
# ---------------------------------------------------------

class Crop(Base):
    __tablename__ = "crops"

    id = Column(String(50), primary_key=True, index=True)
    common_name = Column(String(100), nullable=False)
    scientific_name = Column(String(100), nullable=False)
    tax_id = Column(Integer, nullable=True)
    role = Column(String(20), nullable=False)  # 'benchmark' or 'candidate'
    primary_job = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)

    proteins = relationship("Protein", back_populates="crop", cascade="all, delete-orphan")


class Protein(Base):
    __tablename__ = "proteins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    crop_id = Column(String(50), ForeignKey("crops.id"), nullable=False, index=True)
    accession = Column(String(30), unique=True, nullable=False, index=True)
    reviewed = Column(Boolean, default=False)  # True = Swiss-Prot, False = TrEMBL
    name = Column(String(255), nullable=False)
    family = Column(String(50), nullable=False)  # '7S', '11S', 'other'
    length = Column(Integer, nullable=False)
    sequence = Column(Text, nullable=False)
    keywords_json = Column(Text, default="[]")  # JSON list of keywords & screening flags
    alphafold_available = Column(Boolean, default=False)
    plddt_mean = Column(Float, nullable=True)
    tax_id = Column(Integer, nullable=True)
    organism_name = Column(String(100), nullable=True)
    source_release = Column(String(50), default="UniProtKB 2026_04 (snapshot_2026_04_20261118)")
    fetched_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    crop = relationship("Crop", back_populates="proteins")
    features = relationship("Feature", back_populates="protein", cascade="all, delete-orphan")
    embedding = relationship("Embedding", back_populates="protein", uselist=False, cascade="all, delete-orphan")


class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, autoincrement=True)
    protein_id = Column(Integer, ForeignKey("proteins.id"), nullable=False, index=True)
    feature_name = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)
    feature_set_version = Column(String(20), default="v1.0")

    protein = relationship("Protein", back_populates="features")

    __table_args__ = (
        Index("idx_feature_protein_name", "protein_id", "feature_name"),
    )


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    protein_id = Column(Integer, ForeignKey("proteins.id"), unique=True, nullable=False)
    model_name = Column(String(100), default="facebook/esm2_t6_8M_UR50D")
    dim = Column(Integer, default=480)
    vector_ref = Column(String(255), nullable=False)  # relative file path to .npy vector
    sha256 = Column(String(64), nullable=False)

    protein = relationship("Protein", back_populates="embedding")


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    crop_id = Column(String(50), nullable=True, index=True)
    protein_id = Column(Integer, ForeignKey("proteins.id"), nullable=True)
    job = Column(String(20), nullable=False, index=True)
    property = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(30), nullable=False)
    conditions = Column(String(255), nullable=True)
    extraction_method = Column(String(255), nullable=True)
    study_id = Column(String(50), nullable=False)
    citation = Column(Text, nullable=False)
    verified_by = Column(String(100), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String(20), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    config_version = Column(String(20), default="1.0")


class ModelRun(Base):
    __tablename__ = "model_runs"

    id = Column(String(50), primary_key=True)
    git_sha = Column(String(40), default="local_snapshot")
    data_snapshot_id = Column(String(50), nullable=False)
    config_hash = Column(String(64), nullable=False)
    metrics_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    rankings = relationship("Ranking", back_populates="run", cascade="all, delete-orphan")


class Ranking(Base):
    __tablename__ = "rankings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(50), ForeignKey("model_runs.id"), nullable=False, index=True)
    job = Column(String(20), nullable=False, index=True)
    benchmark_id = Column(String(50), nullable=False)
    crop_id = Column(String(50), nullable=False)
    protein_id = Column(Integer, ForeignKey("proteins.id"), nullable=False)
    score = Column(Float, nullable=False)
    confidence = Column(String(20), nullable=False)  # 'High', 'Medium', 'Low'
    contributions_json = Column(Text, nullable=False)
    flags_json = Column(Text, default="[]")

    run = relationship("ModelRun", back_populates="rankings")
    protein = relationship("Protein")

    __table_args__ = (
        Index("idx_rankings_lookup", "job", "benchmark_id", "run_id"),
    )


class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    url = Column(String(255), nullable=False)
    licence = Column(String(50), nullable=False)
    accessed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    actor = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False)
    target = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(String(36), primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    country = Column(String(50), nullable=False)
    region = Column(String(100), nullable=True)
    mission = Column(String(50), nullable=False)
    scale = Column(String(50), nullable=False)
    assigned_role = Column(String(50), nullable=False)
    geriatric_mode = Column(Boolean, default=False, nullable=False)
    consent_given = Column(Boolean, default=True, nullable=False)
    cookie_consent = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_login_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime, nullable=True)


def init_db():
    """Create all tables in the database if they do not exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for yielding a transactional database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
