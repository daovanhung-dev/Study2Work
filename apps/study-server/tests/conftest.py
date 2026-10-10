from __future__ import annotations

from collections.abc import Iterator

import pytest
from app.core.config import Settings
from app.main import create_app
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def app() -> FastAPI:
    """Tạo Study API với cấu hình kiểm thử và dependency database không kết nối thật."""
    return create_app(
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


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    """Cung cấp TestClient mặc định, giữ nguyên việc re-raise exception chưa xử lý cho test."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def client_without_server_exception(app: FastAPI) -> Iterator[TestClient]:
    """Cung cấp TestClient để kiểm tra response 500 do ServerErrorMiddleware tạo mà không re-raise
    exception gốc sau khi response đã được gửi."""
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
