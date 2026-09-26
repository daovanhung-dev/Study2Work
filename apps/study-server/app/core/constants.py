"""Static Study API configuration.

These values are the runtime defaults for :mod:`app.core.config`.  They are
kept as Python values rather than configuration-file text so configuration does
not depend on a ``.env`` file or process environment variables.
"""

from typing import Literal

APP_ENV: Literal["local", "test", "staging", "production"] = "local"
ENABLE_DOCS = True
CORS_ORIGINS = (
    "http://127.0.0.2:3002",
    "http://127.0.0.2:3001",
)

# Local database configuration is disabled; Neon is the runtime database.
# DB_HOST = "localhost"
# DB_PORT = 5433
# DB_NAME = "study2work_study"
# DB_USER = "study2work"
# DB_PASSWORD = "study2work"
DB_SCHEMA = "nguyen_anh_duc"#doi sang schema của mình
DATABASE_POOL_SIZE = 5
DATABASE_MAX_OVERFLOW = 10

# Primary PostgreSQL connection string for the Neon database.
URL_DATABASE = "postgresql://neondb_owner:npg_lujRC0XdsoI5@ep-red-frog-b3yp4d4v-pooler.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

REDIS_URL = "redis://localhost:6380/0"

OLLAMA_BASE_URL = "http://127.0.0.1:11434"
OLLAMA_MODEL = "qwen2.5-coder:1.5b"
OLLAMA_TIMEOUT = 180.0

# Canonical JWT setup uses ES256. These development values must be replaced by
# a secret-manager-backed key pair before production deployment.
JWT_ALGORITHM: Literal["ES256", "HS256"] = "ES256"
JWT_PUBLIC_KEY = (
    "-----BEGIN PUBLIC KEY-----\n"
    "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAERsfgq153AjoyCSGPE2NlIeaYE/d+\n"
    "+fW0KiuS6l9v8g3XvILBKmCwFEuz0ITuPRfL7D+32KaWXGDC/5Bqf3WwtA==\n"
    "-----END PUBLIC KEY-----"
)
JWT_PRIVATE_KEY = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQg84/4zY0lqbQ579hC\n"
    "NqjIl2E5U5lsXlJSdBxHQJSWOqihRANCAARGx+CrXncCOjIJIY8TY2Uh5pgT9375\n"
    "9bQqK5LqX2/yDde8gsEqYLAUS7PQhO49F8vsP7fYppZcYML/kGp/dbC0\n"
    "-----END PRIVATE KEY-----"
)
JWT_SECRET_KEY: str | None = None
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 15
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 30
JWT_ISSUER = "study2work"
JWT_AUDIENCE = "study-api"

# Required by the opaque refresh-token storage layer when it is enabled.
REFRESH_TOKEN_PEPPER = "replace-with-a-long-random-secret"
