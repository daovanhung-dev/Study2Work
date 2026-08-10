"""Application settings and environment configuration.

The module deliberately keeps settings lazy.  Importing application modules
should not require a production ``.env`` file; configuration is validated when
the application starts or when a dependency actually needs it.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Annotated, Literal

from pydantic import AliasChoices, Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

Environment = Literal["local", "test", "staging", "production"]
JwtAlgorithm = Literal["ES256", "HS256"]


class Settings(BaseSettings):
    """Typed configuration shared by the API and its infrastructure helpers."""

    app_env: Environment = Field(
        default="local",
        validation_alias=AliasChoices("APP_ENV", "app_env"),
    )
    enable_docs: bool = Field(
        default=True,
        validation_alias=AliasChoices("ENABLE_DOCS", "enable_docs"),
    )
    cors_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=list,
        validation_alias=AliasChoices("CORS_ORIGINS", "cors_origins"),
    )

    db_host: str = Field(validation_alias=AliasChoices("DB_HOST", "db_host"))
    db_port: int = Field(
        default=5432,
        ge=1,
        le=65535,
        validation_alias=AliasChoices("DB_PORT", "db_port"),
    )
    db_name: str = Field(validation_alias=AliasChoices("DB_NAME", "db_name"))
    db_user: str = Field(validation_alias=AliasChoices("DB_USER", "db_user"))
    db_password: SecretStr = Field(validation_alias=AliasChoices("DB_PASSWORD", "db_password"))
    db_schema: str = Field(
        default="public",
        min_length=1,
        validation_alias=AliasChoices("DB_SCHEMA", "db_schema"),
    )
    database_pool_size: int = Field(
        default=5,
        ge=1,
        validation_alias=AliasChoices("DATABASE_POOL_SIZE", "database_pool_size"),
    )
    database_max_overflow: int = Field(
        default=10,
        ge=0,
        validation_alias=AliasChoices("DATABASE_MAX_OVERFLOW", "database_max_overflow"),
    )

    redis_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("REDIS_URL", "redis_url"),
    )

    jwt_secret_key: SecretStr | None = Field(
        default=None,
        min_length=32,
        validation_alias=AliasChoices("JWT_SECRET_KEY", "jwt_secret_key"),
    )
    jwt_private_key: SecretStr | None = Field(
        default=None,
        validation_alias=AliasChoices("JWT_PRIVATE_KEY", "jwt_private_key"),
    )
    jwt_public_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("JWT_PUBLIC_KEY", "jwt_public_key"),
    )
    jwt_algorithm: JwtAlgorithm = Field(
        default="ES256",
        validation_alias=AliasChoices("JWT_ALGORITHM", "jwt_algorithm"),
    )
    jwt_access_token_expire_minutes: int = Field(
        default=15,
        gt=0,
        validation_alias=AliasChoices(
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
            "jwt_access_token_expire_minutes",
        ),
    )
    jwt_refresh_token_expire_days: int = Field(
        default=30,
        gt=0,
        validation_alias=AliasChoices(
            "JWT_REFRESH_TOKEN_EXPIRE_DAYS",
            "jwt_refresh_token_expire_days",
        ),
    )
    jwt_issuer: str = Field(
        default="study2work",
        min_length=1,
        validation_alias=AliasChoices("JWT_ISSUER", "jwt_issuer"),
    )
    jwt_audience: str = Field(
        default="study-api",
        min_length=1,
        validation_alias=AliasChoices("JWT_AUDIENCE", "jwt_audience"),
    )
    refresh_token_pepper: SecretStr | None = Field(
        default=None,
        min_length=32,
        validation_alias=AliasChoices("REFRESH_TOKEN_PEPPER", "refresh_token_pepper"),
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> list[str]:
        """Accept either a comma-separated environment value or a list."""

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
    def DB_HOST(self) -> str:
        return self.db_host

    @property
    def DB_PORT(self) -> int:
        return self.db_port

    @property
    def DB_NAME(self) -> str:
        return self.db_name

    @property
    def DB_USER(self) -> str:
        return self.db_user

    @property
    def DB_PASSWORD(self) -> str:
        return self.db_password.get_secret_value()

    @property
    def DB_SCHEMA(self) -> str:
        return self.db_schema

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
    """Load and cache settings for the current process."""

    return Settings()


class _LazySettings:
    """Compatibility proxy that defers environment validation until access."""

    def __getattr__(self, name: str) -> object:
        return getattr(get_settings(), name)

    def __repr__(self) -> str:
        return "settings (lazy)"


settings = _LazySettings()
