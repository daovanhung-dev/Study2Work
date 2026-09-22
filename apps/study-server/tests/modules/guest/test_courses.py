from __future__ import annotations

from decimal import Decimal
from typing import Any

import app.modules.guest.courses.query as courses_query
import app.modules.guest.courses.view as courses_view
import pytest
from app.core.database import get_db
from app.modules.guest.courses.models import CourseQuery
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    def __init__(self) -> None:
        self.rollback_count = 0

    def rollback(self) -> None:
        self.rollback_count += 1


def override_db(session: FakeSession):
    def dependency():
        yield session

    return dependency


def course_rows() -> list[dict[str, Any]]:
    return [
        {
            "id": 101,
            "title": "Introduction to Programming",
            "description": "Fundamentals of programming",
            "thumbnail_url": "https://cdn.example.test/courses/101.png",
            "price": Decimal("49.90"),
            "status": "PUBLISHED",
            "mentor_id": 7,
            "mentor_full_name": "Nguyen Van Mentor",
            "mentor_avatar_url": None,
        }
    ]


def test_course_query_uses_contract_defaults_and_normalizes_sort() -> None:
    query = CourseQuery(sort="price:asc")

    assert query.category is None
    assert query.page == 1
    assert query.size == 20
    assert query.sort == "price:asc"


@pytest.mark.parametrize(
    "payload",
    [
        {"page": 0},
        {"size": 0},
        {"size": 101},
        {"sort": "unknown:asc"},
        {"sort": "price:descending"},
        {"sort": "price"},
        {"category": "not-an-int"},
    ],
)
def test_course_query_rejects_invalid_filters(payload: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        CourseQuery(**payload)


def test_find_published_courses_uses_parameterized_page_and_allowlisted_sort(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_query_many(db, query: str, params: dict[str, Any]):
        captured.update(query=query, params=params)
        return []

    monkeypatch.setattr(courses_query, "query_many", fake_query_many)

    result = courses_query.find_published_courses(
        object(),  # type: ignore[arg-type]
        page=2,
        size=10,
        sort="price:asc",
    )

    assert result == []
    assert captured["params"] == {"status": "PUBLISHED", "limit": 10, "offset": 10}
    assert "ORDER BY c.price ASC, c.id ASC" in captured["query"]
    assert ":status" in captured["query"]
    assert ":limit" in captured["query"]
    assert ":offset" in captured["query"]


def test_courses_http_success_maps_price_mentor_and_pagination(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    captured: dict[str, Any] = {}

    monkeypatch.setattr(
        courses_view,
        "count_published_courses",
        lambda db: {"total": 21, "missing_mentor_count": 0},
    )

    def fake_find_courses(db, *, page: int, size: int, sort: str | None):
        captured.update(page=page, size=size, sort=sort)
        return course_rows()

    monkeypatch.setattr(courses_view, "find_published_courses", fake_find_courses)

    response = client.get(
        "/api/v1/courses?page=2&size=10&sort=price:asc",
        headers={"X-Trace-Id": "00000000-0000-0000-0000-000000000001"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert captured == {"page": 2, "size": 10, "sort": "price:asc"}
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["items"] == [
        {
            "id": 101,
            "title": "Introduction to Programming",
            "description": "Fundamentals of programming",
            "thumbnail_url": "https://cdn.example.test/courses/101.png",
            "price": "49.90",
            "status": "PUBLISHED",
            "mentor": {
                "id": 7,
                "full_name": "Nguyen Van Mentor",
                "avatar_url": None,
            },
        }
    ]
    assert payload["data"]["pagination"] == {
        "page": 2,
        "size": 10,
        "total": 21,
        "total_pages": 3,
    }
    assert "category" not in payload["data"]["items"][0]
    assert payload["traceId"] == "00000000-0000-0000-0000-000000000001"
    assert response.headers["X-Trace-Id"] == payload["traceId"]


def test_courses_empty_result_returns_success_with_zero_total_pages(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        courses_view,
        "count_published_courses",
        lambda db: {"total": 0, "missing_mentor_count": 0},
    )
    monkeypatch.setattr(courses_view, "find_published_courses", lambda db, **kwargs: [])

    response = client.get("/api/v1/courses")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "No published courses."
    assert payload["data"] == {
        "items": [],
        "pagination": {"page": 1, "size": 20, "total": 0, "total_pages": 0},
    }


def test_courses_out_of_range_page_returns_empty_page(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        courses_view,
        "count_published_courses",
        lambda db: {"total": 21, "missing_mentor_count": 0},
    )
    monkeypatch.setattr(courses_view, "find_published_courses", lambda db, **kwargs: [])

    response = client.get("/api/v1/courses?page=4&size=10")

    assert response.status_code == 200
    assert response.json()["data"] == {
        "items": [],
        "pagination": {"page": 4, "size": 10, "total": 21, "total_pages": 3},
    }


def test_courses_rejects_category_until_relation_exists(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        courses_view,
        "count_published_courses",
        lambda db: (_ for _ in ()).throw(AssertionError("category must fail before query")),
    )

    response = client.get("/api/v1/courses?category=1")

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"


def test_courses_maps_database_error_to_safe_internal_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        courses_view,
        "count_published_courses",
        lambda db: (_ for _ in ()).throw(SQLAlchemyError("database unavailable")),
    )

    response = client.get("/api/v1/courses")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "database unavailable" not in response.text
    assert session.rollback_count == 1


def test_courses_rejects_published_orphan_mentor_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        courses_view,
        "count_published_courses",
        lambda db: {"total": 1, "missing_mentor_count": 1},
    )
    monkeypatch.setattr(
        courses_view,
        "find_published_courses",
        lambda db, **kwargs: (_ for _ in ()).throw(
            AssertionError("orphan must fail before page query")
        ),
    )

    response = client.get("/api/v1/courses")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "Published course" not in response.text
    assert session.rollback_count == 1


def test_courses_maps_invalid_row_to_safe_internal_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        courses_view,
        "count_published_courses",
        lambda db: {"total": 1, "missing_mentor_count": 0},
    )
    monkeypatch.setattr(courses_view, "find_published_courses", lambda **kwargs: [{"id": 101}])

    response = client.get("/api/v1/courses")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "Course price" not in response.text


@pytest.mark.parametrize(
    "query_string",
    ["page=0", "size=0", "size=101", "sort=unknown:asc", "sort=price:descending"],
)
def test_courses_http_validation_uses_design_error_code(
    client: TestClient,
    query_string: str,
) -> None:
    response = client.get(f"/api/v1/courses?{query_string}")

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
