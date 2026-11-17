from __future__ import annotations

from datetime import datetime
from typing import Any

import app.modules.guest.api_10_courses_reviews.view as reviews_view
import pytest
from app.core.database import get_db
from app.modules.guest.api_10_courses_reviews.models import CourseReviewsQuery
from app.modules.guest.api_10_courses_reviews.validate import (
    validate_course_reviews_request,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse


class FakeSession:
    def __init__(self) -> None:
        """Khởi tạo database session giả để kiểm tra rollback khi API phát sinh lỗi."""
        self.rollback_count = 0

    def rollback(self) -> None:
        """Tăng bộ đếm rollback để test xác nhận transaction được hoàn tác."""
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency database giả để API không kết nối database thật."""

    def dependency():
        """Yield FakeSession cho request kiểm thử."""
        yield session

    return dependency


def review_rows() -> list[dict[str, Any]]:
    """Tạo review mẫu dùng chung cho các test mapping và pagination."""
    return [
        {
            "id": 101,
            "course_id": 5,
            "user_id": 10,
            "content": "Review content",
            "status": "ACTIVE",
            "created_at": datetime(2026, 9, 15, 10, 0, 0),
            "author_id": 10,
            "author_full_name": "Nguyen Van A",
            "author_avatar_url": None,
        }
    ]


def reply_rows() -> list[dict[str, Any]]:
    """Tạo reply mẫu thuộc review 101 để kiểm tra mapping comments."""
    return [
        {
            "id": 201,
            "parent_id": 101,
            "user_id": 20,
            "content": "Reply content",
            "created_at": datetime(2026, 9, 15, 11, 0, 0),
            "author_id": 20,
            "author_full_name": "Nguyen Van B",
            "author_avatar_url": "avatar-b.png",
        }
    ]


def test_validate_course_reviews_request_uses_default_page() -> None:
    """Kiểm tra page không truyền sẽ dùng effective_page = 1 theo contract API #10."""
    result = validate_course_reviews_request(
        course_id="5",
        course_query=CourseReviewsQuery(),
        trace_id="trace-id",
    )

    assert result == (5, 1, None)


@pytest.mark.parametrize("course_id", ["invalid", "1.5"])
def test_validate_course_reviews_request_returns_404_for_invalid_course_id(
    course_id: str,
) -> None:
    """Kiểm tra course_id không parse được int64 trả 404 theo contract, không tự thêm 422."""
    result = validate_course_reviews_request(
        course_id=course_id,
        course_query=CourseReviewsQuery(),
        trace_id="trace-id",
    )

    assert isinstance(result, JSONResponse)
    assert result.status_code == 404
    assert b"DESIGN_RESOURCE_NOT_FOUND" in result.body


def test_course_reviews_returns_404_when_course_is_not_published(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra Q1 không tìm thấy published course thì API trả 404."""
    monkeypatch.setattr(
        reviews_view,
        "query_one",
        lambda db, query, params: None,
    )

    result = reviews_view.get_course_reviews(
        course_id="5",
        course_query=CourseReviewsQuery(),
        db=FakeSession(),
        trace_id="trace-id",
    )

    assert isinstance(result, JSONResponse)
    assert result.status_code == 404
    assert b"DESIGN_RESOURCE_NOT_FOUND" in result.body


def test_course_reviews_empty_result_returns_success(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra course tồn tại nhưng không có review thì trả 200 với items rỗng và total bằng 0."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    def fake_query_one(db, query, params):
        if query == reviews_view.GET_PUBLISHED_COURSE:
            return {"id": 5, "status": "PUBLISHED"}
        return {"total": 0}

    monkeypatch.setattr(reviews_view, "query_one", fake_query_one)
    monkeypatch.setattr(reviews_view, "query_many", lambda db, query, params: [])

    response = client.get("/api/v1/courses/5/reviews")

    assert response.status_code == 200

    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"] == {
        "items": [],
        "pagination": {
            "page": 1,
            "size": 20,
            "total": 0,
            "total_pages": 0,
        },
    }
    assert payload["meta"] == {}


def test_course_reviews_maps_review_and_replies(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra review và reply được gom đúng vào comments của review cha."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    def fake_query_one(db, query, params):
        if query == reviews_view.GET_PUBLISHED_COURSE:
            return {"id": 5, "status": "PUBLISHED"}
        return {"total": 1}

    def fake_query_many(db, query, params):
        if query == reviews_view.LIST_COURSE_REVIEWS:
            return review_rows()
        return reply_rows()

    monkeypatch.setattr(reviews_view, "query_one", fake_query_one)
    monkeypatch.setattr(reviews_view, "query_many", fake_query_many)

    response = client.get("/api/v1/courses/5/reviews")

    assert response.status_code == 200

    payload = response.json()
    item = payload["data"]["items"][0]

    assert item["discussion_id"] == 101
    assert item["title"] is None
    assert item["content"] == "Review content"
    assert item["user"] == {
        "id": 10,
        "full_name": "Nguyen Van A",
        "avatar_url": None,
    }
    assert item["comments"] == [
        {
            "discussion_id": 201,
            "user": {
                "id": 20,
                "full_name": "Nguyen Van B",
                "avatar_url": "avatar-b.png",
            },
            "content": "Reply content",
            "created_at": "2026-09-15T11:00:00",
        }
    ]


def test_course_reviews_uses_page_size_and_offset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra page=2 tạo LIMIT 20 và OFFSET 20 đúng contract pagination."""
    captured: dict[str, Any] = {}

    def fake_query_one(db, query, params):
        if query == reviews_view.GET_PUBLISHED_COURSE:
            return {"id": 5, "status": "PUBLISHED"}
        return {"total": 25}

    def fake_query_many(db, query, params):
        if query == reviews_view.LIST_COURSE_REVIEWS:
            captured.update(params)
        return []

    monkeypatch.setattr(reviews_view, "query_one", fake_query_one)
    monkeypatch.setattr(reviews_view, "query_many", fake_query_many)

    result = reviews_view.get_course_reviews(
        course_id="5",
        course_query=CourseReviewsQuery(page="2"),
        db=FakeSession(),
        trace_id="trace-id",
    )

    assert captured == {
        "course_id": 5,
        "limit": 20,
        "offset": 20,
    }
    assert result["data"]["pagination"] == {
        "page": 2,
        "size": 20,
        "total": 25,
        "total_pages": 2,
    }


def test_course_reviews_query_uses_review_ids_for_reply_query(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra Q3 tạo bind parameter riêng cho từng review ID thay vì bind trực tiếp một list."""
    captured: dict[str, Any] = {}

    def fake_query_one(db, query, params):
        if query == reviews_view.GET_PUBLISHED_COURSE:
            return {"id": 5, "status": "PUBLISHED"}
        return {"total": 2}

    def fake_query_many(db, query, params):
        if query == reviews_view.LIST_COURSE_REVIEWS:
            return [
                review_rows()[0],
                {
                    **review_rows()[0],
                    "id": 102,
                },
            ]

        captured["query"] = query
        captured["params"] = params
        return []

    monkeypatch.setattr(reviews_view, "query_one", fake_query_one)
    monkeypatch.setattr(reviews_view, "query_many", fake_query_many)

    result = reviews_view.get_course_reviews(
        course_id="5",
        course_query=CourseReviewsQuery(),
        db=FakeSession(),
        trace_id="trace-id",
    )

    assert result["success"] is True
    assert captured["params"] == {
        "review_id_0": 101,
        "review_id_1": 102,
    }
    assert "r.parent_id IN (:review_id_0, :review_id_1)" in captured["query"]


def test_course_reviews_does_not_add_rating_predicate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra rating được nhận nhưng chưa tạo SQL predicate vì DB chưa có source rating."""
    captured: dict[str, Any] = {}

    def fake_query_one(db, query, params):
        if query == reviews_view.GET_PUBLISHED_COURSE:
            return {"id": 5, "status": "PUBLISHED"}
        return {"total": 0}

    def fake_query_many(db, query, params):
        captured["query"] = query
        captured["params"] = params
        return []

    monkeypatch.setattr(reviews_view, "query_one", fake_query_one)
    monkeypatch.setattr(reviews_view, "query_many", fake_query_many)

    result = reviews_view.get_course_reviews(
        course_id="5",
        course_query=CourseReviewsQuery(rating="5"),
        db=FakeSession(),
        trace_id="trace-id",
    )

    assert result["success"] is True
    assert "rating" not in captured["query"].lower()
    assert "rating" not in captured["params"]


@pytest.mark.parametrize("failed_query", ["course", "reviews", "replies", "count"])
def test_course_reviews_database_error_returns_500_and_rolls_back(
    monkeypatch: pytest.MonkeyPatch,
    failed_query: str,
) -> None:
    """Kiểm tra lỗi Q1/Q2/Q3/Q4 đều được ánh xạ thành 500 và rollback session."""
    session = FakeSession()

    def fake_query_one(db, query, params):
        if failed_query == "course" and query == reviews_view.GET_PUBLISHED_COURSE:
            raise SQLAlchemyError("database unavailable")

        if query == reviews_view.GET_PUBLISHED_COURSE:
            return {"id": 5, "status": "PUBLISHED"}

        if failed_query == "count":
            raise SQLAlchemyError("database unavailable")

        return {"total": 1}

    def fake_query_many(db, query, params):
        if failed_query == "reviews" and query == reviews_view.LIST_COURSE_REVIEWS:
            raise SQLAlchemyError("database unavailable")

        if query == reviews_view.LIST_COURSE_REVIEWS:
            return review_rows()

        if failed_query == "replies":
            raise SQLAlchemyError("database unavailable")

        return reply_rows()

    monkeypatch.setattr(reviews_view, "query_one", fake_query_one)
    monkeypatch.setattr(reviews_view, "query_many", fake_query_many)

    result = reviews_view.get_course_reviews(
        course_id="5",
        course_query=CourseReviewsQuery(),
        db=session,
        trace_id="trace-id",
    )

    assert isinstance(result, JSONResponse)
    assert result.status_code == 500
    assert b"DESIGN_INTERNAL_ERROR" in result.body
    assert b"database unavailable" not in result.body
    assert session.rollback_count == 1


def test_course_reviews_mapping_error_returns_500(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra dữ liệu query thiếu field bắt buộc được ánh xạ thành lỗi nội bộ an toàn."""
    session = FakeSession()

    def fake_query_one(db, query, params):
        if query == reviews_view.GET_PUBLISHED_COURSE:
            return {"id": 5, "status": "PUBLISHED"}
        return {"total": 1}

    monkeypatch.setattr(reviews_view, "query_one", fake_query_one)
    monkeypatch.setattr(
        reviews_view,
        "query_many",
        lambda db, query, params: [{"id": 101}],
    )

    result = reviews_view.get_course_reviews(
        course_id="5",
        course_query=CourseReviewsQuery(),
        db=session,
        trace_id="trace-id",
    )

    assert isinstance(result, JSONResponse)
    assert result.status_code == 500
    assert b"DESIGN_INTERNAL_ERROR" in result.body
    assert session.rollback_count == 1


def test_course_reviews_http_returns_404_for_invalid_course_id(
    client: TestClient,
) -> None:
    """Kiểm tra endpoint HTTP giữ contract 404 khi course_id không parse được."""
    response = client.get("/api/v1/courses/not-an-int/reviews")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_course_reviews_http_database_error_is_safe(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra lỗi database qua HTTP trả 500 và không expose nội dung exception."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    monkeypatch.setattr(
        reviews_view,
        "query_one",
        lambda db, query, params: (_ for _ in ()).throw(
            SQLAlchemyError("database unavailable")
        ),
    )

    response = client.get("/api/v1/courses/5/reviews")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "database unavailable" not in response.text
    assert session.rollback_count == 1