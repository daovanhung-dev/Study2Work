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
        )
    )
    with TestClient(app) as test_client:
        yield test_client
