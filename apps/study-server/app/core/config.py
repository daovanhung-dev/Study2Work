"""Typed application settings backed by static Study API constants."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
    field_validator,
    model_validator,
)

from app.core import constants

Environment = Literal["local", "test", "staging", "production"]
JwtAlgorithm = Literal["ES256", "HS256"]


class Settings(BaseModel):
    """Typed configuration shared by the API and its infrastructure helpers."""

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        validate_default=True,
    )

    app_env: Environment = Field(
        default=constants.APP_ENV,
        validation_alias=AliasChoices("APP_ENV", "app_env"),
    )
    enable_docs: bool = Field(
        default=constants.ENABLE_DOCS,
        validation_alias=AliasChoices("ENABLE_DOCS", "enable_docs"),
    )
    cors_origins: list[str] = Field(
        default_factory=lambda: list(constants.CORS_ORIGINS),
        validation_alias=AliasChoices("CORS_ORIGINS", "cors_origins"),
    )

    database_url: SecretStr = Field(
        default=SecretStr(constants.URL_DATABASE),
        validation_alias=AliasChoices("URL_DATABASE", "database_url"),
    )

    # Legacy field-wise DB settings are accepted for constructor compatibility
    # but are not used by app.core.database to create the engine.
    db_host: str | None = Field(
        default=None,
        validation_alias=AliasChoices("DB_HOST", "db_host"),
    )
    db_port: int | None = Field(
        default=None,
        ge=1,
        le=65535,
        validation_alias=AliasChoices("DB_PORT", "db_port"),
    )
    db_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("DB_NAME", "db_name"),
    )
    db_user: str | None = Field(
        default=None,
        validation_alias=AliasChoices("DB_USER", "db_user"),
    )
    db_password: SecretStr | None = Field(
        default=None,
        validation_alias=AliasChoices("DB_PASSWORD", "db_password"),
    )
    db_schema: str = Field(
        default=constants.DB_SCHEMA,
        min_length=1,
        validation_alias=AliasChoices("DB_SCHEMA", "db_schema"),
    )
    database_pool_size: int = Field(
        default=constants.DATABASE_POOL_SIZE,
        ge=1,
        validation_alias=AliasChoices("DATABASE_POOL_SIZE", "database_pool_size"),
    )
    database_max_overflow: int = Field(
        default=constants.DATABASE_MAX_OVERFLOW,
        ge=0,
        validation_alias=AliasChoices("DATABASE_MAX_OVERFLOW", "database_max_overflow"),
    )

    redis_url: str | None = Field(
        default=constants.REDIS_URL,
        validation_alias=AliasChoices("REDIS_URL", "redis_url"),
    )

    jwt_secret_key: SecretStr | None = Field(
        default=SecretStr(constants.JWT_SECRET_KEY) if constants.JWT_SECRET_KEY else None,
        min_length=32,
        validation_alias=AliasChoices("JWT_SECRET_KEY", "jwt_secret_key"),
    )
    jwt_private_key: SecretStr | None = Field(
        default=SecretStr(constants.JWT_PRIVATE_KEY) if constants.JWT_PRIVATE_KEY else None,
        validation_alias=AliasChoices("JWT_PRIVATE_KEY", "jwt_private_key"),
    )
    jwt_public_key: str | None = Field(
        default=constants.JWT_PUBLIC_KEY,
        validation_alias=AliasChoices("JWT_PUBLIC_KEY", "jwt_public_key"),
    )
    jwt_algorithm: JwtAlgorithm = Field(
        default=constants.JWT_ALGORITHM,
        validation_alias=AliasChoices("JWT_ALGORITHM", "jwt_algorithm"),
    )
    jwt_access_token_expire_minutes: int = Field(
        default=constants.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
        gt=0,
        validation_alias=AliasChoices(
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
            "jwt_access_token_expire_minutes",
        ),
    )
    jwt_refresh_token_expire_days: int = Field(
        default=constants.JWT_REFRESH_TOKEN_EXPIRE_DAYS,
        gt=0,
        validation_alias=AliasChoices(
            "JWT_REFRESH_TOKEN_EXPIRE_DAYS",
            "jwt_refresh_token_expire_days",
        ),
    )
    jwt_issuer: str = Field(
        default=constants.JWT_ISSUER,
        min_length=1,
        validation_alias=AliasChoices("JWT_ISSUER", "jwt_issuer"),
    )
    jwt_audience: str = Field(
        default=constants.JWT_AUDIENCE,
        min_length=1,
        validation_alias=AliasChoices("JWT_AUDIENCE", "jwt_audience"),
    )
    refresh_token_pepper: SecretStr | None = Field(
        default=SecretStr(constants.REFRESH_TOKEN_PEPPER),
        min_length=32,
        validation_alias=AliasChoices("REFRESH_TOKEN_PEPPER", "refresh_token_pepper"),
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> list[str]:
        """Accept either a comma-separated value or a list."""

        if value is None:
            return []
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        if isinstance(value, list):
            return [str(origin).strip() for origin in value if str(origin).strip()]
        raise TypeError("cors_origins must be a list or comma-separated string")

    @field_validator("db_schema")
    @classmethod
    def validate_db_schema(cls, value: str) -> str:
        """Reject schema values that cannot safely be used in search_path."""

        normalized = value.strip()
        if not normalized.replace("_", "").isalnum():
            raise ValueError("db_schema may contain only letters, numbers and underscores")
        return normalized

    @model_validator(mode="after")
    def validate_jwt_key_configuration(self) -> Settings:
        """Require the key material needed by the selected JWT algorithm."""

        if self.jwt_algorithm == "HS256" and self.jwt_secret_key is None:
            raise ValueError("JWT_SECRET_KEY is required when JWT_ALGORITHM is HS256")
        if self.jwt_algorithm == "ES256" and self.jwt_public_key is None:
            raise ValueError("JWT_PUBLIC_KEY is required when JWT_ALGORITHM is ES256")
        return self

    # Compatibility aliases for the original uppercase settings API.
    @property
    def DB_HOST(self) -> str | None:
        return self.db_host

    @property
    def DB_PORT(self) -> int | None:
        return self.db_port

    @property
    def DB_NAME(self) -> str | None:
        return self.db_name

    @property
    def DB_USER(self) -> str | None:
        return self.db_user

    @property
    def DB_PASSWORD(self) -> str | None:
        return self.db_password.get_secret_value() if self.db_password else None

    @property
    def DB_SCHEMA(self) -> str:
        return self.db_schema

    @property
    def URL_DATABASE(self) -> str:
        return self.database_url.get_secret_value()

    @property
    def JWT_SECRET_KEY(self) -> SecretStr | None:
        return self.jwt_secret_key

    @property
    def JWT_ALGORITHM(self) -> JwtAlgorithm:
        return self.jwt_algorithm

    @property
    def JWT_ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        return self.jwt_access_token_expire_minutes

    @property
    def JWT_REFRESH_TOKEN_EXPIRE_DAYS(self) -> int:
        return self.jwt_refresh_token_expire_days

    @property
    def JWT_ISSUER(self) -> str:
        return self.jwt_issuer


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Build and cache settings from :mod:`app.core.constants`."""

    return Settings()


class _LazySettings:
    """Compatibility proxy that defers settings validation until access."""

    def __getattr__(self, name: str) -> object:
        return getattr(get_settings(), name)

    def __repr__(self) -> str:
        return "settings (lazy)"


settings = _LazySettings()
