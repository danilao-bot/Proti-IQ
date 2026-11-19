"""
Router for Data Sources and Licences endpoint (/api/v1/sources).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.db import get_db, DataSource

router = APIRouter(prefix="/api/v1/sources", tags=["Sources"])


@router.get("")
def get_sources(db: Session = Depends(get_db)):
    """Return all biological databases and literature datasets with open licences."""
    sources = db.query(DataSource).all()
    return [
        {
            "name": s.name,
            "url": s.url,
            "licence": s.licence,
            "accessed_at": s.accessed_at.isoformat() if s.accessed_at else None,
        }
        for s in sources
    ]
