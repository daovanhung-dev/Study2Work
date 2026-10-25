from __future__ import annotations

from decimal import Decimal
from typing import Any

import app.modules.mentor.api_46_mentor_courses.view as mentor_courses_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.core.responses import error_response
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    def __init__(self) -> None:
        """Khởi tạo phiên DB giả và bộ đếm rollback cho các request Mentor."""
        self.rollback_count = 0

    def rollback(self) -> None:
        """Ghi nhận rollback để test xác nhận lỗi DB dọn transaction."""
        self.rollback_count += 1


def course_rows() -> list[dict[str, Any]]:
    """Tạo hai course thuộc Mentor với status được API #46 chấp nhận."""
    return [
        {
            "id": 101,
            "title": "Draft course",
            "description": None,
            "thumbnail_url": None,
            "price": Decimal("0.00"),
            "status": "DRAFT",
            "mentor_id": 1001,
            "mentor_full_name": "Nguyen Van Mentor",
            "mentor_avatar_url": None,
        },
        {
            "id": 102,
            "title": "Published course",
            "description": "Public course description",
            "thumbnail_url": "https://cdn.example.test/courses/102.png",
            "price": Decimal("49.90"),
            "status": "PUBLISHED",
            "mentor_id": 1001,
            "mentor_full_name": "Nguyen Van Mentor",
            "mentor_avatar_url": "https://cdn.example.test/mentors/1001.png",
        },
    ]


def override_db(session: FakeSession):
    """Tạo dependency thay thế DB để request dùng FakeSession, không mở kết nối thật."""
    def dependency():
        """Yield phiên DB giả được giữ trong closure của test."""
        yield session

    return dependency


def mentor_claims() -> dict[str, Any]:
    """Tạo access claims hợp lệ cho Mentor numeric ID 1001."""
    return {"sub": "1001", "roles": ["MENTOR"]}


def allow_mentor_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Thay JWT decoder bằng claims Mentor hợp lệ để test không cần khóa/token thật."""
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda _token: mentor_claims())


def forbid_queries(monkeypatch: pytest.MonkeyPatch) -> None:
    """Làm test thất bại nếu request chưa được phép vẫn gọi truy vấn course."""
    monkeypatch.setattr(
        mentor_courses_view,
        "count_owned_courses",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("DB query must not run")),
    )


def test_mentor_courses_returns_owner_scoped_page_and_preserves_trace(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Xác nhận API dùng numeric sub/status, map Course và trả pagination cùng trace ID."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: dict[str, Any] = {}
    monkeypatch.setattr(
        mentor_courses_view,
        "count_owned_courses",
        lambda db, **kwargs: {"total": 21, "missing_mentor_count": 0},
    )

    def find_courses(db, **kwargs):
        """Ghi tham số owner/page/status rồi trả một hàng course cho route test."""
        captured.update(kwargs)
        return course_rows()[1:]

    monkeypatch.setattr(mentor_courses_view, "find_owned_courses", find_courses)
    response = client.get(
        "/api/v1/mentor/courses?status=PUBLISHED&page=2&size=10",
        headers={
            "Authorization": "Bearer valid-token",
            "X-Trace-Id": "00000000-0000-0000-0000-000000000001",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert captured == {"mentor_id": 1001, "page": 2, "size": 10, "status": "PUBLISHED"}
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["items"][0]["price"] == "49.90"
    assert payload["data"]["items"][0]["mentor"] == {
        "id": 1001,
        "full_name": "Nguyen Van Mentor",
        "avatar_url": "https://cdn.example.test/mentors/1001.png",
    }
    assert "category" not in payload["data"]["items"][0]
    assert payload["data"]["pagination"] == {
        "page": 2,
        "size": 10,
        "total": 21,
        "total_pages": 3,
    }
    assert payload["traceId"] == response.headers["X-Trace-Id"]


def test_mentor_courses_defaults_to_all_owner_statuses(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Xác nhận thiếu status không thêm predicate và mặc định trả cả DRAFT/PUBLISHED."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: dict[str, Any] = {}
    monkeypatch.setattr(
        mentor_courses_view,
        "count_owned_courses",
        lambda db, **kwargs: {"total": 2, "missing_mentor_count": 0},
    )

    def find_courses(db, **kwargs):
        """Ghi default query values và trả cả hai trạng thái contract."""
        captured.update(kwargs)
        return course_rows()

    monkeypatch.setattr(mentor_courses_view, "find_owned_courses", find_courses)
    response = client.get(
        "/api/v1/mentor/courses",
        headers={"Authorization": "Bearer valid-token"},
    )

    assert response.status_code == 200
    assert captured == {"mentor_id": 1001, "page": 1, "size": 20, "status": None}
    assert [item["status"] for item in response.json()["data"]["items"]] == [
        "DRAFT",
        "PUBLISHED",
    ]
    assert response.json()["data"]["pagination"] == {
        "page": 1,
        "size": 20,
        "total": 2,
        "total_pages": 1,
    }


def test_mentor_courses_empty_and_out_of_range_page_returns_success(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Xác nhận page rỗng vẫn trả 200 và giữ total/page metadata."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        mentor_courses_view,
        "count_owned_courses",
        lambda db, **kwargs: {"total": 2, "missing_mentor_count": 0},
    )
    monkeypatch.setattr(mentor_courses_view, "find_owned_courses", lambda db, **kwargs: [])

    response = client.get(
        "/api/v1/mentor/courses?page=5&size=1",
        headers={"Authorization": "Bearer valid-token"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "No courses found."
    assert response.json()["data"] == {
        "items": [],
        "pagination": {"page": 5, "size": 1, "total": 2, "total_pages": 2},
    }


@pytest.mark.parametrize(
    "authorization",
    [None, "", "Basic token", "Bearer", "Bearer one two"],
)
def test_mentor_courses_rejects_missing_or_malformed_bearer_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Xác nhận Authorization thiếu hoặc sai cú pháp trả 401 trước khi truy vấn course."""
    forbid_queries(monkeypatch)
    headers = {} if authorization is None else {"Authorization": authorization}

    response = client.get("/api/v1/mentor/courses", headers=headers)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert response.json()["data"] is None


def test_mentor_courses_rejects_invalid_jwt_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Xác nhận token decoder trả lỗi 401 được ánh xạ thành authentication error."""
    forbid_queries(monkeypatch)
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: error_response(status_code=401, business_code="INVALID_TOKEN"),
    )

    response = client.get(
        "/api/v1/mentor/courses",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_mentor_courses_rejects_non_mapping_jwt_payload_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Xác nhận payload JWT không phải mapping bị từ chối trước khi truy vấn course."""
    forbid_queries(monkeypatch)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda _token: ["invalid-payload"])

    response = client.get(
        "/api/v1/mentor/courses",
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


@pytest.mark.parametrize(
    "claims",
    [
        {"roles": ["MENTOR"]},
        {"sub": "not-numeric", "roles": ["MENTOR"]},
        {"sub": "0", "roles": ["MENTOR"]},
        {"sub": "1001", "roles": []},
        {"sub": "1001", "roles": [1]},
    ],
)
def test_mentor_courses_rejects_invalid_claims_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    claims: dict[str, Any],
) -> None:
    """Xác nhận thiếu hoặc sai numeric subject/role claims trả 401 trước khi truy vấn."""
    forbid_queries(monkeypatch)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda _token: claims)

    response = client.get(
        "/api/v1/mentor/courses",
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_mentor_courses_rejects_student_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Xác nhận token Student hợp lệ nhận 403 và không gọi DB."""
    forbid_queries(monkeypatch)
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": ["STUDENT"]},
    )

    response = client.get(
        "/api/v1/mentor/courses",
        headers={"Authorization": "Bearer student-token"},
    )

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_mentor_courses_maps_decoder_configuration_error_to_design_internal(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Xác nhận lỗi cấu hình decoder trả 500 design code mà không chạy truy vấn."""
    forbid_queries(monkeypatch)
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: error_response(status_code=500, business_code="INTERNAL_SERVER_ERROR"),
    )

    response = client.get(
        "/api/v1/mentor/courses",
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["message"] == "Mentor courses could not be retrieved."
    assert response.json()["data"] is None


@pytest.mark.parametrize(
    "query_string",
    [
        "status=ARCHIVED",
        "status=draft",
        "page=0",
        "size=0",
        "size=101",
    ],
)
def test_mentor_courses_rejects_invalid_query_with_design_code(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    query_string: str,
) -> None:
    """Xác nhận status/page/size sai trả 422 DESIGN_VALIDATION_ERROR trước khi đọc DB."""
    allow_mentor_token(monkeypatch)
    forbid_queries(monkeypatch)

    response = client.get(
        f"/api/v1/mentor/courses?{query_string}",
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None


def test_mentor_courses_maps_non_integer_query_parse_error_to_design_code(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Xác nhận page không parse được được middleware ánh xạ thành lỗi validation API."""
    allow_mentor_token(monkeypatch)
    forbid_queries(monkeypatch)

    response = client.get(
        "/api/v1/mentor/courses?page=not-an-integer",
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None


def test_mentor_course_queries_bind_same_owner_and_status_predicates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Xác nhận page/count dùng numeric owner và status được bind cùng điều kiện."""
    captured: list[tuple[str, dict[str, Any]]] = []

    def fake_query_many(db, query: str, params: dict[str, Any]):
        """Lưu page SQL và tham số để kiểm tra owner/status scoping."""
        captured.append((query, params))
        return []

    def fake_query_one(db, query: str, params: dict[str, Any]):
        """Lưu count SQL và tham số rồi trả count rỗng."""
        captured.append((query, params))
        return {"total": 0, "missing_mentor_count": 0}

    monkeypatch.setattr(mentor_courses_view, "query_many", fake_query_many)
    monkeypatch.setattr(mentor_courses_view, "query_one", fake_query_one)

    mentor_courses_view.find_owned_courses(
        object(), mentor_id=1001, page=3, size=10, status="DRAFT"  # type: ignore[arg-type]
    )
    mentor_courses_view.count_owned_courses(
        object(), mentor_id=1001, status="DRAFT"  # type: ignore[arg-type]
    )

    assert len(captured) == 2
    for query, params in captured:
        assert "c.mentor_id = :mentor_id" in query
        assert "c.status = :status" in query
        assert params["mentor_id"] == 1001
        assert params["status"] == "DRAFT"
    assert captured[0][1]["limit"] == 10
    assert captured[0][1]["offset"] == 20
    assert "ORDER BY c.created_at DESC, c.id ASC" in captured[0][0]


def test_mentor_course_queries_omit_status_predicate_when_status_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Xác nhận thiếu status dùng SQL không lọc trạng thái nhưng vẫn lọc direct owner."""
    captured: list[tuple[str, dict[str, Any]]] = []

    def fake_query_many(db, query: str, params: dict[str, Any]):
        """Lưu list SQL không có status filter."""
        captured.append((query, params))
        return []

    def fake_query_one(db, query: str, params: dict[str, Any]):
        """Lưu count SQL không có status filter rồi trả tổng bằng không."""
        captured.append((query, params))
        return {"total": 0, "missing_mentor_count": 0}

    monkeypatch.setattr(mentor_courses_view, "query_many", fake_query_many)
    monkeypatch.setattr(mentor_courses_view, "query_one", fake_query_one)
    mentor_courses_view.find_owned_courses(
        object(), mentor_id=1001, page=1, size=20, status=None  # type: ignore[arg-type]
    )
    mentor_courses_view.count_owned_courses(
        object(), mentor_id=1001, status=None  # type: ignore[arg-type]
    )

    assert len(captured) == 2
    assert all("c.mentor_id = :mentor_id" in query for query, _params in captured)
    assert all("c.status = :status" not in query for query, _params in captured)
    assert all("status" not in params for _query, params in captured)


def test_mentor_courses_maps_database_failure_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Xác nhận lỗi SQL rollback Session, trả 500 an toàn và không lộ thông tin DB."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        mentor_courses_view,
        "count_owned_courses",
        lambda db, **kwargs: (_ for _ in ()).throw(SQLAlchemyError("database unavailable")),
    )

    response = client.get(
        "/api/v1/mentor/courses",
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "database unavailable" not in response.text
    assert session.rollback_count == 1


def test_mentor_courses_rejects_orphaned_mentor_projection_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Xác nhận owner row thiếu Mentor projection trả lỗi nội bộ trước truy vấn trang."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        mentor_courses_view,
        "count_owned_courses",
        lambda db, **kwargs: {"total": 1, "missing_mentor_count": 1},
    )
    monkeypatch.setattr(
        mentor_courses_view,
        "find_owned_courses",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("page query must not run")),
    )

    response = client.get(
        "/api/v1/mentor/courses",
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    "count_row",
    [
        {"total": "invalid", "missing_mentor_count": 0},
        {"total": 1, "missing_mentor_count": "invalid"},
    ],
)
def test_mentor_courses_maps_invalid_count_row_to_internal_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    count_row: dict[str, Any],
) -> None:
    """Xác nhận count row từ DB sai kiểu được ánh xạ lỗi nội bộ và rollback an toàn."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        mentor_courses_view,
        "count_owned_courses",
        lambda db, **kwargs: count_row,
    )
    monkeypatch.setattr(
        mentor_courses_view,
        "find_owned_courses",
        lambda db, **kwargs: course_rows(),
    )

    response = client.get(
        "/api/v1/mentor/courses",
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    "row",
    [
        {"id": 101, "status": "DRAFT"},
        {
            "id": 101,
            "title": "Unsupported status",
            "price": Decimal("5.00"),
            "status": "ARCHIVED",
            "mentor_id": 1001,
            "mentor_full_name": "Nguyen Van Mentor",
        },
    ],
)
def test_mentor_courses_maps_incomplete_or_unknown_status_to_internal_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    row: dict[str, Any],
) -> None:
    """Xác nhận thiếu Course fields bắt buộc hoặc status ngoài enum không lộ lỗi model."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        mentor_courses_view,
        "count_owned_courses",
        lambda db, **kwargs: {"total": 1, "missing_mentor_count": 0},
    )
    monkeypatch.setattr(mentor_courses_view, "find_owned_courses", lambda db, **kwargs: [row])

    response = client.get(
        "/api/v1/mentor/courses",
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "incomplete." not in response.text
    assert "outside the approved contract" not in response.text
