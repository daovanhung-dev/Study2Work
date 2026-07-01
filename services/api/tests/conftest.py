from __future__ import annotations

from collections.abc import Iterator

from app.core.config import Settings
from app.main import create_app
from fastapi.testclient import TestClient


def make_test_client() -> TestClient:
    app = create_app(
        Settings(
            app_env="test",
            database_url="postgresql+asyncpg://study2work:study2work@localhost:5432/test",
            redis_url="redis://localhost:6379/15",
            celery_broker_url="redis://localhost:6379/14",
            celery_result_backend="redis://localhost:6379/13",
        )
    )
    return TestClient(app)


def client() -> Iterator[TestClient]:
    with make_test_client() as test_client:
        yield test_client
