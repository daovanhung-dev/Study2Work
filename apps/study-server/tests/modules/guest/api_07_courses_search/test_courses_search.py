from __future__ import annotations

from decimal import Decimal
from typing import Any

import app.modules.guest.api_07_courses_search.view as courses_view
import pytest
from app.core.database import get_db
from app.modules.guest.api_07_courses_search.models import CourseSearchQuery
from app.modules.guest.api_07_courses_search.validate import validate_course_search_query
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse


class FakeSession:
    def __init__(self) -> None:
        """Khởi tạo phiên database giả với các bộ đếm commit/rollback dùng để xác minh transaction
        trong test."""
        self.rollback_count = 0

    def rollback(self) -> None:
        """Tăng bộ đếm rollback để test xác nhận transaction được hoàn tác khi lỗi."""
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency thay thế database để route dùng FakeSession mà không mở kết nối thật."""
    def dependency():
        """Yield FakeSession được giữ trong closure cho request kiểm thử."""
        yield session

    return dependency


def course_rows() -> list[dict[str, Any]]:
    """Tạo course PUBLISHED mẫu có mentor và giá decimal để kiểm thử response."""
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


def test_course_search_validator_normalizes_keyword_and_uses_fixed_defaults() -> None:
    """Kiểm tra validator chuẩn hóa q và model giữ page mặc định cùng sort."""
    query = CourseSearchQuery(q="  Programming ", sort="price:asc")

    assert query.q == "  Programming "
    assert query.category is None
    assert query.page == 1
    assert query.sort == "price:asc"
    validated = validate_course_search_query(query, trace_id="trace-id")
    assert isinstance(validated, CourseSearchQuery)
    assert validated.q == "programming"


@pytest.mark.parametrize(
    "payload",
    [
        {"q": 101},
        {"page": 0},
        {"sort": "unknown:asc"},
        {"sort": "price:descending"},
        {"sort": "price"},
        {"category": "not-an-int"},
    ],
)
def test_course_search_validator_rejects_invalid_filters(payload: dict[str, object]) -> None:
    """Kiểm tra validator trả 422 cho page, category hoặc sort ngoài quy tắc hiện hành."""
    try:
        query = CourseSearchQuery(**payload)
    except ValidationError:
        return
    response = validate_course_search_query(query, trace_id="trace-id")
    assert isinstance(response, JSONResponse)
    assert response.status_code == 422


def test_find_published_courses_search_uses_parameterized_keyword_and_fixed_page_size(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra truy vấn search bind từ khóa, status, offset và DEFAULT_SIZE vào SQL."""
    captured: dict[str, Any] = {}

    def fake_query_many(db, query: str, params: dict[str, Any]):
        """Ghi SQL cùng tham số rồi trả danh sách rỗng cho kiểm thử truy vấn danh sách."""
        captured.update(query=query, params=params)
        return []

    monkeypatch.setattr(courses_view, "query_many", fake_query_many)

    result = courses_view.find_published_courses_search(
        object(),  # type: ignore[arg-type]
        q="programming",
        page=2,
        sort="price:asc",
    )

    assert result == []
    assert captured["params"] == {
        "status": "PUBLISHED",
        "q_pattern": "%programming%",
        "limit": 20,
        "offset": 20,
    }
    assert "LOWER(c.name) LIKE :q_pattern" in captured["query"]
    assert "ORDER BY c.price ASC, c.id ASC" in captured["query"]


def test_count_published_courses_search_uses_same_keyword_predicate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra truy vấn count dùng cùng q_pattern và status với truy vấn lấy kết quả."""
    captured: dict[str, Any] = {}

    def fake_query_one(db, query: str, params: dict[str, Any]):
        """Ghi SQL cùng tham số rồi trả dữ liệu count giả cho kiểm thử search."""
        captured.update(query=query, params=params)
        return {"total": 1, "missing_mentor_count": 0}

    monkeypatch.setattr(courses_view, "query_one", fake_query_one)

    result = courses_view.count_published_courses_search(object(), q="python")  # type: ignore[arg-type]

    assert result == {"total": 1, "missing_mentor_count": 0}
    assert captured["params"] == {"status": "PUBLISHED", "q_pattern": "%python%"}
    assert "LOWER(c.name) LIKE :q_pattern" in captured["query"]


def test_course_search_http_success_maps_result_and_trace(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra API search trả course đã ánh xạ, metadata đúng và trace ID nhất quán."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    captured: dict[str, Any] = {}

    monkeypatch.setattr(
        courses_view,
        "count_published_courses_search",
        lambda db, *, q: {"total": 21, "missing_mentor_count": 0},
    )

    def fake_find_courses(db, *, q: str | None, page: int, sort: str | None):
        """Ghi từ khóa, trang và sort rồi trả course mẫu cho kiểm thử search view."""
        captured.update(q=q, page=page, sort=sort)
        return course_rows()

    monkeypatch.setattr(courses_view, "find_published_courses_search", fake_find_courses)

    response = client.get(
        "/api/v1/courses/search",
        params={"q": "  PROGRAMMING ", "page": "2", "sort": "price:asc", "size": "5"},
        headers={"X-Trace-Id": "00000000-0000-0000-0000-000000000001"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert captured == {"q": "programming", "page": 2, "sort": "price:asc"}
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["message"] == "Courses search completed."
    assert payload["data"]["items"][0]["price"] == "49.90"
    assert payload["data"]["pagination"] == {
        "page": 2,
        "size": 20,
        "total": 21,
        "total_pages": 2,
    }
    assert payload["traceId"] == "00000000-0000-0000-0000-000000000001"
    assert response.headers["X-Trace-Id"] == payload["traceId"]


def test_course_search_empty_result_returns_success_with_fixed_page_size(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra search không có kết quả vẫn trả thành công với danh sách rỗng và size cố định."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        courses_view,
        "count_published_courses_search",
        lambda db, *, q: {"total": 0, "missing_mentor_count": 0},
    )
    monkeypatch.setattr(
        courses_view,
        "find_published_courses_search",
        lambda db, **kwargs: [],
    )

    response = client.get("/api/v1/courses/search?q=missing")

    assert response.status_code == 200
    assert response.json()["message"] == "No published courses matched the search."
    assert response.json()["data"] == {
        "items": [],
        "pagination": {"page": 1, "size": 20, "total": 0, "total_pages": 0},
    }


def test_course_search_out_of_range_page_keeps_total_metadata(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra trang search ngoài phạm vi trả danh sách rỗng nhưng giữ total và total_pages."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        courses_view,
        "count_published_courses_search",
        lambda db, *, q: {"total": 21, "missing_mentor_count": 0},
    )
    monkeypatch.setattr(
        courses_view,
        "find_published_courses_search",
        lambda db, **kwargs: [],
    )

    response = client.get("/api/v1/courses/search?page=3")

    assert response.status_code == 200
    assert response.json()["data"]["pagination"] == {
        "page": 3,
        "size": 20,
        "total": 21,
        "total_pages": 2,
    }


def test_course_search_rejects_category_before_db_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra category chưa hỗ trợ bị từ chối trước khi gọi database."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        courses_view,
        "count_published_courses_search",
        lambda db, **kwargs: (_ for _ in ()).throw(
            AssertionError("category must fail before query")
        ),
    )

    response = client.get("/api/v1/courses/search?category=1")

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    "query_string",
    ["category=not-an-int", "page=0", "sort=unknown:asc", "sort=price:descending"],
)
def test_course_search_http_validation_uses_design_error_code(
    client: TestClient,
    query_string: str,
) -> None:
    """Kiểm tra query search sai trả HTTP 422 cùng business code validation theo design."""
    response = client.get(f"/api/v1/courses/search?{query_string}")

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"


def test_course_search_maps_database_error_to_safe_internal_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra lỗi truy vấn search làm rollback Session và trả lỗi nội bộ an toàn."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        courses_view,
        "count_published_courses_search",
        lambda db, **kwargs: (_ for _ in ()).throw(SQLAlchemyError("database unavailable")),
    )

    response = client.get("/api/v1/courses/search")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "database unavailable" not in response.text
    assert session.rollback_count == 1


def test_course_search_rejects_published_orphan_mentor_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra kết quả search có course PUBLISHED thiếu mentor được chuyển thành lỗi toàn vẹn."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        courses_view,
        "count_published_courses_search",
        lambda db, **kwargs: {"total": 1, "missing_mentor_count": 1},
    )
    monkeypatch.setattr(
        courses_view,
        "find_published_courses_search",
        lambda db, **kwargs: (_ for _ in ()).throw(
            AssertionError("orphan must fail before page query")
        ),
    )

    response = client.get("/api/v1/courses/search")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "Published course" not in response.text
    assert session.rollback_count == 1


def test_course_search_maps_invalid_row_to_safe_internal_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra hàng search sai shape hoặc giá không parse được thành lỗi nội bộ an toàn."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        courses_view,
        "count_published_courses_search",
        lambda db, **kwargs: {"total": 1, "missing_mentor_count": 0},
    )
    monkeypatch.setattr(
        courses_view,
        "find_published_courses_search",
        lambda db, **kwargs: [{"id": 101}],
    )

    response = client.get("/api/v1/courses/search")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "Course price" not in response.text
    assert session.rollback_count == 1
