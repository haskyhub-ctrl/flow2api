"""Local-only review controls for this fork; no Google traffic is needed to preview."""

import os
from urllib.parse import urlsplit
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


def review_mode():
    return os.environ.get("FLOW2API_REVIEW_MODE", "1") != "0"


class LocalSecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        host = request.url.hostname
        if host not in {"localhost", "127.0.0.1", "::1", "testserver"}:
            return JSONResponse({"detail": "This build only accepts local hosts."}, 403)
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            origin = request.headers.get("origin")
            if origin:
                source = urlsplit(origin)
                if (source.scheme, source.netloc) != (request.url.scheme, request.url.netloc):
                    return JSONResponse({"detail": "Cross-origin writes are blocked."}, 403)
            if review_mode() and request.url.path not in {
                "/api/login", "/api/admin/login", "/api/logout", "/api/admin/logout"
            }:
                return JSONResponse({"detail": "Ban xem thu: chua cho phep them tai khoan, goi Google hoac tao video."}, 403)
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        return response
