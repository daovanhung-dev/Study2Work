from __future__ import annotations

from typing import Any

import app.modules.mentor.api_51_mentor_content_update.view as content_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    def __init__(self, *, fail_commit: bool = False) -> None:
        """Theo dõi transaction và mô phỏng lỗi commit của API view."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát sinh lỗi SQLAlchemy đã cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("private commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback do API view yêu cầu."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override dùng FakeSession mà không kết nối PostgreSQL."""

    def dependency():
        """Yield session của test trong vòng đời request."""

        yield session

    return dependency


def allow_mentor_token(monkeypatch: pytest.MonkeyPatch, *, roles: list[str] | None = None) -> None:
    """Thay decoder JWT bằng subject số có role Mentor."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": roles or ["MENTOR"]},
    )


def request_body(**overrides: Any) -> dict[str, Any]:
    """Tạo body replacement hợp lệ cho API #51."""

    return {
        "content_type": "lesson-node-v2",
        "title": "Nội dung đã cập nhật",
        "payload": {"body": "Nội dung mới"},
        **overrides,
    }


def current_row(**overrides: Any) -> dict[str, Any]:
    """Tạo row Content đang thuộc Mentor 1001 trước khi update."""

    return {
        "id": 50001,
        "course_id": 101,
        "mentor_id": 1001,
        "content_type": "lesson-node",
        "title": "Nội dung cũ",
        "payload": {"body": "Bản trước"},
        "status": "PUBLISHED",
        "parent_id": 42001,
        "order": 3,
        **overrides,
    }


def updated_row(**overrides: Any) -> dict[str, Any]:
    """Tạo UPDATE/RETURNING row khớp body thay thế và Content response."""

    return {
        "id": 50001,
        "course_id": 101,
        "content_type": "lesson-node-v2",
        "title": "Nội dung đã cập nhật",
        "payload": {"body": "Nội dung mới"},
        "status": "PENDING_REVIEW",
        "parent_id": 42001,
        "order": 3,
        **overrides,
    }


def put_content(
    client: TestClient,
    *,
    content_id: str = "50001",
    body: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
):
    """Gửi PUT API #51 với Bearer token mặc định hoặc headers chỉ định."""

    request_headers = {"Authorization": "Bearer valid-token"} if headers is None else headers
    return client.put(
        f"/api/v1/mentor/content/{content_id}",
        json=request_body() if body is None else body,
        headers=request_headers,
    )


def successful_query_one(captured: dict[str, Any] | None = None):
    """Tạo query fake trả target, snapshot number và updated row theo thứ tự."""

    call_index = 0

    def query_one(_db, query, params):
        """Ghi lại truy vấn và trả projection thành công tương ứng."""

        nonlocal call_index
        call_index += 1
        if captured is not None:
            captured[f"query_{call_index}"] = query
            captured[f"params_{call_index}"] = params
        if call_index == 1:
            return current_row()
        if call_index == 2:
            return {"version_no": 1}
        return updated_row()

    return query_one


def test_update_content_archives_current_version_and_commits(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Archive trạng thái trước update, trả Content mới và commit một lần."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: dict[str, Any] = {}
    monkeypatch.setattr(content_view, "query_one", successful_query_one(captured))

    response = put_content(client)

    assert response.status_code == 200
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert response.json()["data"] == {
        "id": 50001,
        "course_id": 101,
        "content_type": "lesson-node-v2",
        "title": "Nội dung đã cập nhật",
        "payload": {"body": "Nội dung mới"},
        "status": "PENDING_REVIEW",
        "parent_id": 42001,
        "order": 3,
    }
    assert "FOR UPDATE OF content, course" in captured["query_1"]
    assert "content.deleted_at IS NULL" in captured["query_1"]
    assert captured["params_2"] == {
        "content_id": 50001,
        "course_id": 101,
        "content_type": "lesson-node",
        "title": "Nội dung cũ",
        "payload": '{"body":"Bản trước"}',
        "status": "PUBLISHED",
        "parent_id": 42001,
        "content_order": 3,
        "archived_by": 1001,
    }
    assert captured["params_3"]["content_type"] == "lesson-node-v2"
    assert captured["params_3"]["title"] == "Nội dung đã cập nhật"
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_update_content_rejects_missing_or_malformed_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Từ chối Bearer thiếu hoặc sai định dạng trước khi truy vấn Content."""

    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )
    headers = {} if authorization is None else {"Authorization": authorization}

    response = put_content(client, headers=headers)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_update_content_rejects_non_mentor_role_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối role Student trước mọi truy vấn Content."""

    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = put_content(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


@pytest.mark.parametrize("content_id", ["abc", "9223372036854775808", "-9223372036854775809"])
def test_update_content_maps_invalid_path_id_to_not_found(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    content_id: str,
) -> None:
    """Map path ID không phải signed int64 thành catalog 404 trước truy vấn."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = put_content(client, content_id=content_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


@pytest.mark.parametrize(
    "body",
    [
        {"content_type": "lesson-node-v2", "payload": {}},
        request_body(content_type=12),
        request_body(title=12),
        request_body(payload=[]),
        request_body(status="PUBLISHED"),
    ],
)
def test_update_content_rejects_invalid_body_with_design_validation_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: dict[str, Any],
) -> None:
    """Trả validation business code cho body thiếu, sai kiểu hoặc thừa field."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = put_content(client, body=body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"]


def test_update_content_maps_missing_or_non_owned_content(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map absent active Content to 404 and a different course owner to 403."""

    allow_mentor_token(monkeypatch)
    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    outcomes = [None, current_row(mentor_id=2002)]

    def query_one(_db, _query, _params):
        """Trả lần lượt target thiếu và target không thuộc Mentor."""

        return outcomes.pop(0)

    monkeypatch.setattr(content_view, "query_one", query_one)

    missing = put_content(client)
    denied = put_content(client)

    assert missing.status_code == 404
    assert missing.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert denied.status_code == 403
    assert denied.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


@pytest.mark.parametrize("failed_call", [1, 2, 3])
def test_update_content_rolls_back_query_failures(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failed_call: int,
) -> None:
    """Rollback và ẩn SQL detail khi target, snapshot hoặc update query lỗi."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    call_index = 0

    def query_one(_db, _query, _params):
        """Phát sinh lỗi SQLAlchemy ở bước được chọn."""

        nonlocal call_index
        call_index += 1
        if call_index == failed_call:
            raise SQLAlchemyError("private database detail")
        if call_index == 1:
            return current_row()
        if call_index == 2:
            return {"version_no": 1}
        return updated_row()

    monkeypatch.setattr(content_view, "query_one", query_one)

    response = put_content(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private database detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize("bad_projection_call", [2, 3])
def test_update_content_rolls_back_invalid_snapshot_or_update_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    bad_projection_call: int,
) -> None:
    """Không commit khi database không trả version number hoặc Content mới hợp lệ."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    call_index = 0

    def query_one(_db, _query, _params):
        """Trả projection lỗi tại bước snapshot hoặc update."""

        nonlocal call_index
        call_index += 1
        if call_index == 1:
            return current_row()
        if call_index == bad_projection_call:
            return {"version_no": "1"} if call_index == 2 else updated_row(title="Sai")
        if call_index == 2:
            return {"version_no": 1}
        return updated_row()

    monkeypatch.setattr(content_view, "query_one", query_one)

    response = put_content(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_update_content_maps_commit_failure_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map lỗi commit thành 500 an toàn và rollback transaction."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(content_view, "query_one", successful_query_one())

    response = put_content(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_update_content_propagates_trace_id(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Truyền trace ID vào success envelope và response header."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(content_view, "query_one", successful_query_one())
    trace_id = "f25e0fb8-ae67-40ae-8d6f-c50c660e5d17"

    response = put_content(
        client,
        headers={"Authorization": "Bearer valid-token", "X-Trace-Id": trace_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Trace-Id"] == trace_id
    assert response.json()["traceId"] == trace_id


def test_update_content_openapi_declares_int64_path_body_and_updated_response(
    client: TestClient,
) -> None:
    """Kiểm tra OpenAPI khai báo path int64, ba body fields và HTTP 200."""

    schema = client.app.openapi()
    operation = schema["paths"]["/api/v1/mentor/content/{content_id}"]["put"]
    path_parameter = next(item for item in operation["parameters"] if item["name"] == "content_id")
    body_ref = operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
    body_schema = schema["components"]["schemas"][body_ref.rsplit("/", 1)[-1]]

    assert path_parameter["schema"]["format"] == "int64"
    assert body_schema["required"] == ["content_type", "title", "payload"]
    assert operation["responses"]["200"]["description"] == "Successful Response"


def test_update_content_framework_body_error_uses_design_validation_code(
    client: TestClient,
) -> None:
    """Xác nhận middleware dùng business code validation cho route API #51."""

    response = client.put(
        "/api/v1/mentor/content/50001",
        json=request_body(payload=[]),
        headers={"Authorization": "Bearer valid-token"},
    )

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
