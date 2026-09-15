"""Safe template for the local DB Admin constants file."""

from __future__ import annotations

from typing import Final

APP_ENV: Final[str] = "local"
HOST: Final[str] = "127.0.0.1"
PORT: Final[int] = 8010
CORS_ORIGINS: Final[list[str]] = ["http://localhost:5175"]

# Replace this placeholder locally. Never commit a real database credential.
URL_DATABASE: Final[str] = "postgresql://user:password@host/database?sslmode=require"

JWKS_URL: Final[str | None] = None
JWT_ISSUER: Final[str] = "study2work"
JWT_AUDIENCE: Final[str] = "db-admin-api"
JWT_ALGORITHMS: Final[list[str]] = ["ES256"]
DEV_AUTH: Final[bool] = True

STATEMENT_TIMEOUT_MS: Final[int] = 10_000
LOCK_TIMEOUT_MS: Final[int] = 5_000
MAX_ROWS: Final[int] = 1_000
MAX_SQL_BYTES: Final[int] = 262_144
AUDIT_CAPACITY: Final[int] = 500
