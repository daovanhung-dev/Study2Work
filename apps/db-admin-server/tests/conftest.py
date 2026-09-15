from __future__ import annotations

import pytest
from app.core.config import Settings
from app.main import create_app
from fastapi.testclient import TestClient


@pytest.fixture
def settings() -> Settings:
    return Settings(
        app_env="test",
        database_url="postgresql://user:password@localhost/database",
        jwt_issuer="test-issuer",
        jwt_audience="db-admin-api",
        dev_auth=True,
    )


@pytest.fixture
def client(settings: Settings) -> TestClient:
    return TestClient(create_app(settings))
