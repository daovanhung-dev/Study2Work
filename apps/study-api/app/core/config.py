from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="S2W_STUDY_",
        env_file=".env",
        extra="ignore",
    )

    app_name: str = "Study2Work Study API"
    app_version: str = "0.1.0"
    app_env: Literal["local", "test", "staging", "prod"] = "local"
    api_prefix: str = "/api/v1"
    enable_docs: bool = True
    log_level: str = "INFO"

    database_url: str = "postgresql+asyncpg://study2work:study2work@localhost:5433/study2work_study"
    redis_url: str = "redis://localhost:6380/0"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
