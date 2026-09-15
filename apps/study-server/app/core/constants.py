"""Static Study API configuration.

These values are the runtime defaults for :mod:`app.core.config`.  They are
kept as Python values rather than dotenv-style text so configuration does not
depend on a ``.env`` file or process environment variables.
"""

from typing import Literal

APP_ENV: Literal["local", "test", "staging", "production"] = "local"
ENABLE_DOCS = True
CORS_ORIGINS = (
    "http://localhost:5173",
    "http://localhost:5174",
)

# Local database configuration is disabled; Neon is the runtime database.
# DB_HOST = "localhost"
# DB_PORT = 5433
# DB_NAME = "study2work_study"
# DB_USER = "study2work"
# DB_PASSWORD = "study2work"
DB_SCHEMA = "public"
DATABASE_POOL_SIZE = 5
DATABASE_MAX_OVERFLOW = 10

# Primary PostgreSQL connection string for the Neon database.
URL_DATABASE = "postgresql://neondb_owner:npg_lujRC0XdsoI5@ep-red-frog-b3yp4d4v-pooler.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

REDIS_URL = "redis://localhost:6380/0"

# Canonical JWT setup uses ES256. Store real PEM values in a secret manager in
# production; these are the existing local placeholder values.
JWT_ALGORITHM: Literal["ES256", "HS256"] = "ES256"
JWT_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\nreplace-with-public-key\n-----END PUBLIC KEY-----"
JWT_PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nreplace-with-private-key\n-----END PRIVATE KEY-----"
JWT_SECRET_KEY: str | None = None
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 15
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 30
JWT_ISSUER = "study2work"
JWT_AUDIENCE = "study-api"

# Required by the opaque refresh-token storage layer when it is enabled.
REFRESH_TOKEN_PEPPER = "replace-with-a-long-random-secret"
