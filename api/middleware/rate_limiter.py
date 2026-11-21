"""
Simple in-memory rate limiting middleware for Proti IQ.
Mitigates credential stuffing, automated scanning, and denial-of-service.
"""

import time
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests_per_minute: int = 60):
        super().__init__(app)
        self.max_requests = max_requests_per_minute
        self.clients = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()

        # Clean entries older than 60 seconds
        self.clients[client_ip] = [t for t in self.clients[client_ip] if now - t < 60]

        # Check limit
        if len(self.clients[client_ip]) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please wait a moment before trying again."},
                headers={"Retry-After": "60"}
            )

        self.clients[client_ip].append(now)
        return await call_next(request)
