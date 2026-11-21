from __future__ import annotations

from typing import Any

import app.modules.mentor.api_52_mentor_content_publish.view as content_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả lập để theo dõi giao dịch mà không kết nối database."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        """Theo dõi commit/rollback và tùy chọn giả lập lỗi commit."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit và phát sinh SQLAlchemyError nếu test cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("private commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback mà API view yêu cầu."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override cung cấp FakeSession cho một HTTP request."""

    def dependency():
        """Yield session giả lập mà không kết nối PostgreSQL."""

        yield session

    return dependency


def allow_mentor_token(monkeypatch: pytest.MonkeyPatch, *, roles: list[str] | None = None) -> None:
    """Thay JWT decoder bằng principal số có role được test chỉ định."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": roles or ["MENTOR"]},
    )


def current_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection Content mặc định đang thuộc Mentor 1001."""

    return {
        "id": 50001,
        "course_id": 101,
        "mentor_id": 1001,
        "content_type": "lesson-node",
        "title": "Nội dung mẫu",
        "payload": {"body": "Nội dung kiểm thử"},
        "status": "APPROVED",
        "parent_id": 42001,
        "order": 3,
        **overrides,
    }


def patch_content(
    client: TestClient,
    *,
    content_id: str = "50001",
    body: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
):
    """Gửi PATCH API #52 với body và Bearer header mặc định hoặc được chỉ định."""

    request_headers = {"Authorization": "Bearer valid-token"} if headers is None else headers
    return client.patch(
        f"/api/v1/mentor/content/{content_id}/publish",
        json={"published": True} if body is None else body,
        headers=request_headers,
    )


def query_rows(
    initial: dict[str, Any],
    updated: dict[str, Any] | None = None,
    captured: dict[str, Any] | None = None,
):
    """Tạo query fake trả Content hiện tại rồi tùy chọn Content đã cập nhật."""

    call_index = 0

    def query_one(_db, query, params):
        """Ghi SQL/params và chọn row theo thứ tự gọi của view."""

        nonlocal call_index
        call_index += 1
        if captured is not None:
            captured[f"query_{call_index}"] = query
            captured[f"params_{call_index}"] = params
        return initial if call_index == 1 else updated

    return query_one


@pytest.mark.parametrize(
    ("initial_status", "published", "target_status"),
    [
        ("APPROVED", True, "PUBLISHED"),
        ("PUBLISHED", False, "APPROVED"),
    ],
)
def test_publish_content_updates_only_status_and_commits(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    initial_status: str,
    published: bool,
    target_status: str,
) -> None:
    """Kiểm tra publish/unpublish chỉ đổi status và commit response hợp lệ."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: dict[str, Any] = {}
    initial = current_row(status=initial_status)
    updated = current_row(status=target_status)
    monkeypatch.setattr(content_view, "query_one", query_rows(initial, updated, captured))

    response = patch_content(client, body={"published": published})

    assert response.status_code == 200
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert response.json()["data"] == {
        "id": 50001,
        "course_id": 101,
        "content_type": "lesson-node",
        "title": "Nội dung mẫu",
        "payload": {"body": "Nội dung kiểm thử"},
        "status": target_status,
        "parent_id": 42001,
        "order": 3,
    }
    assert "FOR UPDATE OF content, course" in captured["query_1"]
    assert "content.deleted_at IS NULL" in captured["query_1"]
    assert "SET status = :target_status" in captured["query_2"]
    assert "content_type =" not in captured["query_2"]
    assert captured["params_2"] == {
        "content_id": 50001,
        "expected_status": initial_status,
        "target_status": target_status,
    }
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    ("status", "published", "target_status"),
    [("APPROVED", False, "APPROVED"), ("PUBLISHED", True, "PUBLISHED")],
)
def test_publish_content_same_target_is_idempotent(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    status: str,
    published: bool,
    target_status: str,
) -> None:
    """Kiểm tra request lặp cùng target trả hiện trạng mà không chạy UPDATE."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    calls = 0

    def query_one(_db, _query, _params):
        """Trả Content hiện tại duy nhất để xác minh không có mutation thứ hai."""

        nonlocal calls
        calls += 1
        return current_row(status=status)

    monkeypatch.setattr(content_view, "query_one", query_one)

    response = patch_content(client, body={"published": published})

    assert response.status_code == 200
    assert response.json()["data"]["status"] == target_status
    assert calls == 1
    assert session.commit_count == 1


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_publish_content_rejects_bad_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Kiểm tra Bearer thiếu hoặc sai bị từ chối trước query Content."""

    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )
    headers = {} if authorization is None else {"Authorization": authorization}

    response = patch_content(client, headers=headers)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_publish_content_rejects_non_mentor_role_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra role không phải Mentor bị từ chối trước query Content."""

    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = patch_content(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


@pytest.mark.parametrize("content_id", ["abc", "9223372036854775808", "-9223372036854775809"])
def test_publish_content_maps_invalid_path_to_not_found(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    content_id: str,
) -> None:
    """Kiểm tra path ID sai format hoặc signed-int64 range ánh xạ về 404."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = patch_content(client, content_id=content_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"published": 1},
        {"published": "true"},
        {"published": True, "status": "PUBLISHED"},
    ],
)
def test_publish_content_rejects_invalid_request_body(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: dict[str, Any],
) -> None:
    """Kiểm tra body thiếu, sai kiểu hoặc có field thừa trả lỗi thiết kế 422."""

    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = patch_content(client, body=body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"


@pytest.mark.parametrize("status", ["PENDING_REVIEW", "REJECTED", "DRAFT", "UNKNOWN"])
def test_publish_content_rejects_state_that_is_not_ready(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    status: str,
) -> None:
    """Kiểm tra state ngoài APPROVED/PUBLISHED không được chuyển đổi."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    calls = 0

    def query_one(_db, _query, _params):
        """Trả Content có status được cấu hình cho kiểm tra readiness."""

        nonlocal calls
        calls += 1
        return current_row(status=status)

    monkeypatch.setattr(content_view, "query_one", query_one)

    response = patch_content(client)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert calls == 1
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_publish_content_returns_not_found_when_content_is_missing(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra Content không tồn tại ánh xạ về lỗi catalog 404."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(content_view, "query_one", lambda *_args, **_kwargs: None)

    response = patch_content(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert session.rollback_count == 1


def test_publish_content_denies_non_owner(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra direct owner không khớp bị từ chối mà không ghi dữ liệu."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: current_row(mentor_id=2002),
    )

    response = patch_content(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.rollback_count == 1


def test_publish_content_rolls_back_when_lookup_fails(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra lỗi truy vấn rollback và không làm lộ chi tiết DB."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Phát sinh lỗi SQL giả lập mà không lộ chi tiết ra response."""

        raise SQLAlchemyError("private SQL detail")

    monkeypatch.setattr(content_view, "query_one", fail_query)

    response = patch_content(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private SQL detail" not in response.text
    assert session.rollback_count == 1


def test_publish_content_rolls_back_when_commit_fails(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra lỗi commit rollback và trả lỗi nội bộ an toàn."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        content_view,
        "query_one",
        query_rows(current_row(), current_row(status="PUBLISHED")),
    )

    response = patch_content(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_publish_content_rejects_malformed_database_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra projection DB sai cấu trúc không được commit hoặc trả về."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: current_row(payload=[]),
    )

    response = patch_content(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_publish_content_openapi_declares_int64_path_and_derived_body(
    client: TestClient,
) -> None:
    """Kiểm tra OpenAPI khai báo path int64 và request body DERIVED tường minh."""

    schema = client.app.openapi()
    operation = schema["paths"]["/api/v1/mentor/content/{content_id}/publish"]["patch"]
    path_parameter = next(item for item in operation["parameters"] if item["name"] == "content_id")
    request_schema_ref = operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
    request_schema = schema["components"]["schemas"][request_schema_ref.rsplit("/", 1)[-1]]

    assert path_parameter["schema"]["format"] == "int64"
    assert request_schema["required"] == ["published"]
    assert request_schema["properties"]["published"]["type"] == "boolean"
    assert operation["responses"]["200"]["description"] == "Successful Response"


def test_publish_content_framework_body_error_uses_design_validation_code(
    client: TestClient,
) -> None:
    """Xác nhận middleware map body validation của route về mã thiết kế 422."""

    response = client.patch(
        "/api/v1/mentor/content/50001/publish",
        json={"published": "yes"},
        headers={"Authorization": "Bearer valid-token"},
    )

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"


def test_publish_content_propagates_trace_id(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Truyền request trace vào envelope và header khi target đã đạt."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(content_view, "query_one", lambda *_args, **_kwargs: current_row())
    trace_id = "f25e0fb8-ae67-40ae-8d6f-c50c660e5d17"

    response = client.patch(
        "/api/v1/mentor/content/50001/publish",
        json={"published": False},
        headers={"Authorization": "Bearer valid-token", "X-Trace-Id": trace_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Trace-Id"] == trace_id
    assert response.json()["traceId"] == trace_id
