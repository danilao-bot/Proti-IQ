"""
Proti IQ FastAPI Main Application.
Provides high-performance, rate-limited, read-only inference and evidence endpoints.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
try:
    from slowapi import _rate_limit_exceeded_handler
    from slowapi.errors import RateLimitExceeded
    has_slowapi = True
except ImportError:
    has_slowapi = False
from api.db import init_db, SessionLocal
from api.security import limiter, security_headers_middleware
from api.routers import jobs, crops, rank, evidence, proteins, sources, hub

# Initialize tables
init_db()

app = FastAPI(
    title="Proti IQ API",
    description="In-Silico Screening and Ranking of Nigerian Legume Storage Proteins for Alternative Food Systems",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Attach rate limiter if available
if has_slowapi:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Inject security headers middleware
app.middleware("http")(security_headers_middleware)

# CORS configuration: Open to all origins for React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers under /api/v1
app.include_router(jobs.router)
app.include_router(crops.router)
app.include_router(rank.router)
app.include_router(evidence.router)
app.include_router(proteins.router)
app.include_router(sources.router)
app.include_router(hub.router)


@app.get("/health", tags=["Health"])
def health_check():
    """Liveness and readiness check for container orchestration and uptime monitoring."""
    from sqlalchemy import text
    db_ok = True
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
    except Exception:
        db_ok = False

    return {
        "status": "healthy" if db_ok else "degraded",
        "service": "proti-iq-api",
        "version": "1.0.0",
        "database_connected": db_ok,
        "data_snapshot_id": "snapshot_nov2026",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
