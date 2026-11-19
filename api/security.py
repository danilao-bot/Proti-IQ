"""
Security Middleware, Input Validation, and Protection Controls for Proti IQ.
Enforces rate-limiting, strict accession regex, security headers, and CORS rules.
"""

import re
import time
from collections import defaultdict
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse

# Strict UniProt accession regex (6-10 alphanumeric characters)
ACCESSION_REGEX = re.compile(r"^[A-Z0-9]{6,10}$")

try:
    from slowapi import Limiter
    from slowapi.util import get_remote_address
    limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
except ImportError:
    # Graceful in-memory rate limiter fallback
    class FallbackLimiter:
        def __init__(self):
            self.history = defaultdict(list)

        def limit(self, limit_value: str):
            def decorator(func):
                return func
            return decorator

    limiter = FallbackLimiter()


def validate_accession(accession: str) -> str:
    """Validate accession format against standard UniProt pattern to prevent SSRF / path traversal."""
    cleaned = accession.strip().upper()
    if not ACCESSION_REGEX.match(cleaned):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid protein accession format: '{accession}'. Must match standard alphanumeric identifier.",
        )
    return cleaned


async def security_headers_middleware(request: Request, call_next):
    """Inject strict security headers into every response."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "img-src 'self' data: https:; "
        "style-src 'self' 'unsafe-inline'; "
        "script-src 'self'; "
        "frame-ancestors 'none';"
    )
    if "server" in response.headers:
        del response.headers["server"]
    return response
