from __future__ import annotations

from collections.abc import Iterator

import pytest
from app.core.config import Settings
from app.main import create_app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> Iterator[TestClient]:
    app = create_app(
        Settings(
            app_env="test",
            enable_docs=False,
            cors_origins=["http://testserver"],
            db_host="127.0.0.1",
            db_port=5432,
            db_name="study2work_test",
            db_user="study2work",
            db_password="study2work",
            db_schema="public",
            redis_url="redis://127.0.0.1:6379/0",
            jwt_algorithm="HS256",
            jwt_secret_key="test-secret-key-that-is-at-least-32-characters",
        )
    )
    with TestClient(app) as test_client:
        yield test_client
