from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="S2W_", env_file=".env", extra="ignore")

    app_name: str = "Study2Work API"
    app_version: str = "0.1.0"
    app_env: Literal["local", "dev", "test", "staging", "prod"] = "local"
    api_prefix: str = "/api/v1"
    enable_docs: bool = True

    database_url: str = "postgresql+asyncpg://study2work:study2work@localhost:5432/study2work"
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    log_level: str = "INFO"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
