from __future__ import annotations

from typing import Any

import app.modules.guest.api_05_categories.view as categories_view
import pytest
from app.core.database import get_db
from app.core.exceptions import request_validation_exception_handler
from app.modules.guest.api_05_categories.models import CategoryQuery
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request


class FakeSession:
    def __init__(self) -> None:
        self.rollback_count = 0

    def rollback(self) -> None:
        self.rollback_count += 1


def override_db(session: FakeSession):
    def dependency():
        yield session

    return dependency


def category_rows() -> list[dict[str, Any]]:
    return [
        {
            "id": 1,
            "name": "Lập trình",
            "slug": "lap-trinh",
            "description": "Các khóa học lập trình.",
        },
        {
            "id": 2,
            "name": "Thiết kế",
            "slug": "thiet-ke",
            "description": None,
        },
    ]


def test_category_query_keeps_locale_optional_without_extra_rules() -> None:
    assert CategoryQuery().locale is None
    assert CategoryQuery(locale=" custom-locale ").locale == " custom-locale "


def test_category_query_rejects_non_string_locale() -> None:
    with pytest.raises(ValidationError):
        CategoryQuery(locale=123)  # type: ignore[arg-type]


def test_categories_http_success_uses_default_locale_and_safe_envelope(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    captured: dict[str, str] = {}

    def find_categories(db, *, locale: str):
        captured["locale"] = locale
        return category_rows()

    monkeypatch.setattr(categories_view, "find_active_categories", find_categories)

    response = client.get(
        "/api/v1/categories",
        headers={"X-Trace-Id": "00000000-0000-0000-0000-000000000001"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert captured == {"locale": "vi-VN"}
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["items"][0]["slug"] == "lap-trinh"
    assert payload["data"]["pagination"] == {
        "page": 1,
        "size": 2,
        "total": 2,
        "total_pages": 1,
    }
    assert payload["meta"] == {}
    assert payload["traceId"] == "00000000-0000-0000-0000-000000000001"
    assert response.headers["X-Trace-Id"] == "00000000-0000-0000-0000-000000000001"


def test_categories_http_uses_exact_requested_locale(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    captured: dict[str, str] = {}
    monkeypatch.setattr(
        categories_view,
        "find_active_categories",
        lambda db, *, locale: captured.update(locale=locale) or [],
    )

    response = client.get("/api/v1/categories?locale=en-US")

    assert response.status_code == 200
    assert captured == {"locale": "en-US"}
    assert response.json()["data"]["pagination"]["total"] == 0


def test_categories_empty_result_is_successful_empty_page(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(categories_view, "find_active_categories", lambda db, *, locale: [])

    response = client.get("/api/v1/categories")

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["message"] == "No active categories."
    assert payload["data"] == {
        "items": [],
        "pagination": {"page": 1, "size": 0, "total": 0, "total_pages": 1},
    }


def test_categories_database_error_is_safe_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        categories_view,
        "find_active_categories",
        lambda db, *, locale: (_ for _ in ()).throw(SQLAlchemyError("database unavailable")),
    )

    response = client.get("/api/v1/categories")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "database unavailable" not in response.text
    assert session.rollback_count == 1


def test_categories_mapping_error_is_safe(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        categories_view,
        "find_active_categories",
        lambda db, *, locale: [{"id": "not-an-id"}],
    )

    response = client.get("/api/v1/categories")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "not-an-id" not in response.text


@pytest.mark.asyncio
async def test_categories_validation_uses_design_error_code() -> None:
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "scheme": "http",
            "server": ("testserver", 80),
            "client": ("testclient", 50000),
            "root_path": "",
            "path": "/api/v1/categories",
            "raw_path": b"/api/v1/categories",
            "query_string": b"locale=123",
            "headers": [],
        }
    )
    error = RequestValidationError(
        [
            {
                "type": "string_type",
                "loc": ("query", "locale"),
                "msg": "Input should be a valid string",
                "input": 123,
            }
        ]
    )

    response = await request_validation_exception_handler(request, error)

    assert response.status_code == 422
    assert response.body is not None
    assert b"DESIGN_VALIDATION_ERROR" in response.body
