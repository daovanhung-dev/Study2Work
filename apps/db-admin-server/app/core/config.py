"""Constants-backed configuration for the isolated DB Admin service."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal, cast

from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator

from app.core import constants

Environment = Literal["local", "test", "staging", "production"]


class Settings(BaseModel):
    """Runtime settings; database credentials never cross this service boundary."""

    model_config = ConfigDict(extra="ignore")

    app_env: Environment = "local"
    host: str = "127.0.0.1"
    port: int = Field(default=8010, ge=1, le=65_535)
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5175"])
    database_url: SecretStr
    jwks_url: str | None = None
    jwt_issuer: str = Field(min_length=1)
    jwt_audience: str = Field(min_length=1)
    jwt_algorithms: list[str] = Field(default_factory=lambda: ["ES256"])
    dev_auth: bool = False
    statement_timeout_ms: int = Field(default=10_000, ge=100, le=300_000)
    lock_timeout_ms: int = Field(default=5_000, ge=100, le=300_000)
    max_rows: int = Field(default=1_000, ge=1, le=100_000)
    max_sql_bytes: int = Field(default=262_144, ge=1_024, le=2_000_000)
    audit_capacity: int = Field(default=500, ge=50, le=10_000)

    @model_validator(mode="after")
    def validate_auth(self) -> Settings:
        if self.app_env not in {"local", "test"} and self.dev_auth:
            raise ValueError("DB_ADMIN_DEV_AUTH is only allowed in local/test")
        if not self.dev_auth and not self.jwks_url:
            raise ValueError("DB_ADMIN_JWKS_URL is required when development auth is disabled")
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load settings once from the local constants module."""

    return Settings(
        app_env=cast(Environment, constants.APP_ENV),
        host=constants.HOST,
        port=constants.PORT,
        cors_origins=list(constants.CORS_ORIGINS),
        database_url=SecretStr(constants.URL_DATABASE),
        jwks_url=constants.JWKS_URL,
        jwt_issuer=constants.JWT_ISSUER,
        jwt_audience=constants.JWT_AUDIENCE,
        jwt_algorithms=list(constants.JWT_ALGORITHMS),
        dev_auth=constants.DEV_AUTH,
        statement_timeout_ms=constants.STATEMENT_TIMEOUT_MS,
        lock_timeout_ms=constants.LOCK_TIMEOUT_MS,
        max_rows=constants.MAX_ROWS,
        max_sql_bytes=constants.MAX_SQL_BYTES,
        audit_capacity=constants.AUDIT_CAPACITY,
    )
