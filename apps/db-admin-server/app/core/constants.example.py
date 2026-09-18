"""Safe template for the local DB Admin constants file."""

from __future__ import annotations

from typing import Final

APP_ENV: Final[str] = "local"
HOST: Final[str] = "127.0.0.1"
PORT: Final[int] = 3001
CORS_ORIGINS: Final[list[str]] = ["http://127.0.0.2:3000"]

# Keep the legacy value for compatibility with older tooling. New DB Admin
# requests use the explicitly named targets below.
URL_DATABASE: Final[str] = "postgresql://user:password@host/database?sslmode=require"

# Replace both placeholders locally. Never commit real database credentials.
DATABASE_TARGETS: Final[dict[str, str]] = {
    "work_server": "postgresql://user:password@work-host/database?sslmode=require",
    "study_server": "postgresql://user:password@study-host/database?sslmode=require",
}

JWKS_URL: Final[str | None] = None
JWT_ISSUER: Final[str] = "study2work"
JWT_AUDIENCE: Final[str] = "db-admin-api"
JWT_ALGORITHMS: Final[list[str]] = ["ES256"]
# Password auth is explicit. Keep DEV_AUTH for isolated tests only.
LOCAL_AUTH_ENABLED: Final[bool] = True
LOCAL_JWT_SECRET: Final[str] = "replace-with-a-random-secret-of-at-least-32-characters"
LOCAL_JWT_TTL_MINUTES: Final[int] = 15
DEV_AUTH: Final[bool] = False
CONTROL_SCHEMA: Final[str] = "db_admin"

STATEMENT_TIMEOUT_MS: Final[int] = 10_000
LOCK_TIMEOUT_MS: Final[int] = 5_000
MAX_ROWS: Final[int] = 1_000
MAX_SQL_BYTES: Final[int] = 262_144
AUDIT_CAPACITY: Final[int] = 500
