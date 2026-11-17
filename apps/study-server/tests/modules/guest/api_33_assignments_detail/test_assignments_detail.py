"""Kiểm thử API #33: route, xác thực, validation, truy vấn và response."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime
from decimal import Decimal
from typing import Any

import app.modules.guest.api_33_assignments_detail.view as assignment_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.core.responses import error_response
from app.modules.guest.api_33_assignments_detail.query import ASSIGNMENT_BY_ID
from app.modules.guest.api_33_assignments_detail.validate import validate_assignment_id
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

ENDPOINT = "/api/v1/assignments/{assignment_id}"
TRACE_ID = "00000000-0000-0000-0000-000000000033"
AUTHORIZATION = "Bearer test-access-token"


class FakeSession:
    """Session giả để test không cần database thật."""


def make_assignment_row(**overrides: Any) -> dict[str, Any]:
    """Tạo hàng dữ liệu mẫu theo các cột API #33 sử dụng."""
    row: dict[str, Any] = {
        "id": 3301,
        "course_id": 701,
        "title": "Bài tập cuối khóa",
        "description": "Nộp bài hoàn chỉnh.",
        "due_at": datetime(2026, 11, 1, 12, 30),
        "max_score": Decimal("10.00"),
        "internal_column": "không được trả ra response",
    }
    row.update(overrides)
    return row


@pytest.fixture
def fake_db(client: TestClient) -> Iterator[FakeSession]:
    """Thay DB dependency bằng Session giả và dọn override sau mỗi test."""
    session = FakeSession()

    def override_db() -> Iterator[FakeSession]:
        yield session

    client.app.dependency_overrides[get_db] = override_db
    try:
        yield session
    finally:
        client.app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def student_auth(monkeypatch: pytest.MonkeyPatch) -> None:
    """Giải mã token mẫu thành claims hợp lệ của Student."""
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda token: {"sub": "1001", "roles": ["STUDENT"]},
    )


def assignment_url(assignment_id: str | int) -> str:
    """Tạo URL API #33 từ assignment ID."""
    return ENDPOINT.format(assignment_id=assignment_id)


def test_assignment_detail_success_contract_and_trace_id(
    client: TestClient,
    fake_db: FakeSession,
    student_auth: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra response thành công, field contract, bind ID và trace ID."""
    captured: dict[str, Any] = {}

    def find_assignment(db: Any, *, assignment_id: int) -> dict[str, Any]:
        captured.update(db=db, assignment_id=assignment_id)
        return make_assignment_row()

    monkeypatch.setattr(assignment_view, "find_assignment", find_assignment)
    response = client.get(
        assignment_url(3301),
        headers={"Authorization": AUTHORIZATION, "X-Trace-Id": TRACE_ID},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert body["meta"] == {}
    assert body["traceId"] == TRACE_ID
    assert response.headers["X-Trace-Id"] == TRACE_ID
    data = body["data"]
    due_at = data["due_at"]
    assert due_at.startswith("2026-11-01T12:30:00")
    datetime.fromisoformat(due_at.replace("Z", "+00:00"))
    assert isinstance(data["max_score"], str)
    assert Decimal(data["max_score"]) == Decimal("10.00")
    assert data == {
        "id": 3301,
        "course_id": 701,
        "title": "Bài tập cuối khóa",
        "description": "Nộp bài hoàn chỉnh.",
        "due_at": due_at,
        "max_score": data["max_score"],
    }
    assert captured == {"db": fake_db, "assignment_id": 3301}


def test_assignment_detail_preserves_nullable_fields(
    client: TestClient,
    fake_db: FakeSession,
    student_auth: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra description và due_at có thể được trả về dưới dạng null."""
    monkeypatch.setattr(
        assignment_view,
        "find_assignment",
        lambda db, *, assignment_id: make_assignment_row(
            description=None,
            due_at=None,
        ),
    )

    response = client.get(assignment_url(3301), headers={"Authorization": AUTHORIZATION})

    assert response.status_code == 200
    assert response.json()["data"]["description"] is None
    assert response.json()["data"]["due_at"] is None


@pytest.mark.parametrize("authorization", [None, "", "Basic token", "Bearer"])
def test_assignment_detail_requires_valid_bearer_header(
    client: TestClient,
    fake_db: FakeSession,
    student_auth: None,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Kiểm tra thiếu hoặc sai cú pháp Authorization trả 401 trước khi query."""
    monkeypatch.setattr(
        assignment_view,
        "find_assignment",
        lambda *args, **kwargs: pytest.fail("Không được query khi chưa xác thực."),
    )
    headers = {} if authorization is None else {"Authorization": authorization}

    response = client.get(assignment_url(3301), headers=headers)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_assignment_detail_maps_invalid_jwt_to_authentication_error(
    client: TestClient,
    fake_db: FakeSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra helper auth chuẩn hóa JWT không hợp lệ thành lỗi 401 của API."""
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda token: error_response(
            status_code=401,
            business_code="TOKEN_INVALID",
            message="Chi tiết token nội bộ.",
            trace_id=TRACE_ID,
        ),
    )
    monkeypatch.setattr(
        assignment_view,
        "find_assignment",
        lambda *args, **kwargs: pytest.fail("Không được query khi JWT sai."),
    )

    response = client.get(assignment_url(3301), headers={"Authorization": AUTHORIZATION})

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


@pytest.mark.parametrize(
    ("claims", "expected_status", "expected_code"),
    [
        ({"sub": "1001", "roles": ["MENTOR"]}, 403, "DESIGN_ACCESS_DENIED"),
        ({"sub": "không-phải-số", "roles": ["STUDENT"]}, 401, "DESIGN_AUTHENTICATION_REQUIRED"),
        ({"roles": ["STUDENT"]}, 401, "DESIGN_AUTHENTICATION_REQUIRED"),
        ({"sub": "1001", "roles": []}, 401, "DESIGN_AUTHENTICATION_REQUIRED"),
    ],
)
def test_assignment_detail_checks_jwt_claims_and_student_role(
    client: TestClient,
    fake_db: FakeSession,
    monkeypatch: pytest.MonkeyPatch,
    claims: dict[str, Any],
    expected_status: int,
    expected_code: str,
) -> None:
    """Kiểm tra claims sai trả 401, role không phải Student trả 403."""
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: claims)
    monkeypatch.setattr(
        assignment_view,
        "find_assignment",
        lambda *args, **kwargs: pytest.fail("Không được query khi auth bị từ chối."),
    )

    response = client.get(assignment_url(3301), headers={"Authorization": AUTHORIZATION})

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code


@pytest.mark.parametrize(
    "assignment_id",
    ["khong-phai-so", "9223372036854775808", "-9223372036854775809"],
)
def test_assignment_detail_maps_invalid_id_to_not_found(
    client: TestClient,
    fake_db: FakeSession,
    student_auth: None,
    monkeypatch: pytest.MonkeyPatch,
    assignment_id: str,
) -> None:
    """Kiểm tra ID không parse được hoặc ngoài int64 trả 404 trước khi query."""
    monkeypatch.setattr(
        assignment_view,
        "find_assignment",
        lambda *args, **kwargs: pytest.fail("Không được query với ID không hợp lệ."),
    )

    response = client.get(
        assignment_url(assignment_id),
        headers={"Authorization": AUTHORIZATION},
    )

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_assignment_detail_returns_not_found_when_assignment_is_missing(
    client: TestClient,
    fake_db: FakeSession,
    student_auth: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra không có hàng assignment trả mã lỗi 404 theo catalog."""
    monkeypatch.setattr(assignment_view, "find_assignment", lambda db, *, assignment_id: None)

    response = client.get(assignment_url(404), headers={"Authorization": AUTHORIZATION})

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


@pytest.mark.parametrize("failure", ["database", "invalid_row"])
def test_assignment_detail_maps_internal_failures_to_safe_500(
    client: TestClient,
    fake_db: FakeSession,
    student_auth: None,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    """Kiểm tra lỗi DB hoặc row sai schema thành 500 và không lộ chi tiết nội bộ."""
    if failure == "database":
        monkeypatch.setattr(
            assignment_view,
            "find_assignment",
            lambda db, *, assignment_id: (_ for _ in ()).throw(
                SQLAlchemyError("database details must not leak")
            ),
        )
    else:
        monkeypatch.setattr(
            assignment_view,
            "find_assignment",
            lambda db, *, assignment_id: {"id": 3301},
        )

    response = client.get(assignment_url(3301), headers={"Authorization": AUTHORIZATION})

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "database details must not leak" not in response.text


def test_validate_assignment_id_accepts_int64_limits() -> None:
    """Kiểm tra validator chấp nhận hai giới hạn số nguyên int64."""
    assert validate_assignment_id(str(-(2**63)), trace_id=TRACE_ID) == -(2**63)
    assert validate_assignment_id(str(2**63 - 1), trace_id=TRACE_ID) == 2**63 - 1


def test_find_assignment_uses_shared_query_helper_and_bound_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra view dùng query_one chung và bind assignment ID, không ghép SQL."""
    db = FakeSession()
    row = make_assignment_row()
    captured: dict[str, Any] = {}

    def fake_query_one(actual_db: Any, sql: str, params: dict[str, int]) -> dict[str, Any]:
        captured.update(db=actual_db, sql=sql, params=params)
        return row

    monkeypatch.setattr(assignment_view, "query_one", fake_query_one)
    assert assignment_view.find_assignment(db, assignment_id=3301) is row  # type: ignore[arg-type]
    assert captured == {"db": db, "sql": ASSIGNMENT_BY_ID, "params": {"assignment_id": 3301}}

    normalized_sql = " ".join(ASSIGNMENT_BY_ID.lower().split())
    assert "from assignments as a" in normalized_sql
    assert "where a.id = :assignment_id" in normalized_sql
    assert "a.name as title" in normalized_sql
    assert all(
        column in normalized_sql
        for column in ("a.course_id", "a.description", "a.due_at", "a.max_score")
    )
    assert " join " not in normalized_sql
    assert "created_at" not in normalized_sql
    assert "updated_at" not in normalized_sql
    assert "submission" not in normalized_sql


def test_assignment_detail_openapi_declares_int64_path_parameter(
    client: TestClient,
) -> None:
    """Kiểm tra OpenAPI khai báo assignment_id là path parameter bắt buộc kiểu int64."""
    operation = client.app.openapi()["paths"][ENDPOINT]["get"]
    path_parameter = next(
        parameter
        for parameter in operation["parameters"]
        if parameter["name"] == "assignment_id"
    )

    assert path_parameter == {
        "name": "assignment_id",
        "in": "path",
        "required": True,
        "schema": {"type": "integer", "format": "int64"},
    }

