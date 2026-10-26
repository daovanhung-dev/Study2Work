from __future__ import annotations

from typing import Any

import app.modules.mentor.api_50_mentor_content_create.view as content_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    def __init__(self, *, fail_commit: bool = False) -> None:
        """Theo dõi commit/rollback và mô phỏng lỗi commit của transaction."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát sinh lỗi SQLAlchemy đã cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("private commit detail")

    def rollback(self) -> None:
        """Ghi nhận yêu cầu rollback transaction từ API view."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override dùng một FakeSession trong request TestClient."""

    def dependency():
        """Yield session của test mà không kết nối PostgreSQL."""

        yield session

    return dependency


def allow_mentor_token(monkeypatch: pytest.MonkeyPatch, *, roles: list[str] | None = None) -> None:
    """Thay decoder JWT bằng subject số có role Mentor để kiểm tra route."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": roles or ["MENTOR"]},
    )


def request_body(**overrides: Any) -> dict[str, Any]:
    """Tạo body API #50 hợp lệ với các field có thể ghi đè trong từng test."""

    return {
        "course_id": 101,
        "content_type": "lesson-node",
        "title": "Nội dung mẫu",
        "payload": {"body": "Nội dung kiểm thử"},
        **overrides,
    }


def course_row(**overrides: Any) -> dict[str, Any]:
    """Tạo row course legacy do Mentor 1001 trực tiếp sở hữu."""

    return {"id": 101, "mentor_id": 1001, "status": "DRAFT", **overrides}


def content_row(**overrides: Any) -> dict[str, Any]:
    """Tạo row INSERT/RETURNING tương ứng với Content root API #50."""

    return {
        "id": 50001,
        "course_id": 101,
        "content_type": "lesson-node",
        "title": "Nội dung mẫu",
        "payload": {"body": "Nội dung kiểm thử"},
        "status": "PENDING_REVIEW",
        "parent_id": None,
        "order": 0,
        **overrides,
    }


def post_content(
    client: TestClient,
    body: dict[str, Any] | None = None,
    *,
    headers: dict[str, str] | None = None,
):
    """Gửi POST API #50 với Bearer token mặc định hoặc headers của test."""

    request_headers = (
        {"Authorization": "Bearer valid-token"} if headers is None else headers
    )
    return client.post(
        "/api/v1/mentor/content",
        json=request_body() if body is None else body,
        headers=request_headers,
    )


def test_create_content_returns_inserted_root_and_commits(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Tạo Content root, cấp order kế tiếp và trả dữ liệu sau khi commit."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: dict[str, Any] = {}
    call_index = 0

    def query_one(_db, query, params):
        """Trả course, next order và row vừa insert theo thứ tự API."""

        nonlocal call_index
        call_index += 1
        captured[f"query_{call_index}"] = query
        captured[f"params_{call_index}"] = params
        if call_index == 1:
            return course_row()
        if call_index == 2:
            return {"next_order": 7}
        return content_row(order=7)

    monkeypatch.setattr(content_view, "query_one", query_one)

    response = post_content(client)

    assert response.status_code == 201
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_CREATED"
    assert payload["data"] == {
        "id": 50001,
        "course_id": 101,
        "content_type": "lesson-node",
        "title": "Nội dung mẫu",
        "payload": {"body": "Nội dung kiểm thử"},
        "status": "PENDING_REVIEW",
        "order": 7,
    }
    assert "FOR UPDATE" in captured["query_1"]
    assert "status" not in captured["query_1"].lower()
    assert "GREATEST" in captured["query_2"]
    assert "parent_id IS NULL" in captured["query_2"]
    assert "deleted_at IS NULL" in captured["query_2"]
    assert captured["params_3"] == {
        "course_id": 101,
        "content_type": "lesson-node",
        "title": "Nội dung mẫu",
        "payload": '{"body":"Nội dung kiểm thử"}',
        "status": "PENDING_REVIEW",
        "content_order": 7,
    }
    assert "CAST(:payload AS JSONB)" in captured["query_3"]
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_create_content_starts_root_order_at_zero(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Dùng order 0 khi course chưa có root Content đang hoạt động."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: dict[str, Any] = {}
    call_index = 0

    def query_one(_db, _query, params):
        """Trả course, aggregate mặc định và row mới có order 0."""

        nonlocal call_index
        call_index += 1
        if call_index == 1:
            return course_row()
        if call_index == 2:
            return {"next_order": 0}
        captured.update(params)
        return content_row(order=0)

    monkeypatch.setattr(content_view, "query_one", query_one)

    response = post_content(client)

    assert response.status_code == 201
    assert response.json()["data"]["order"] == 0
    assert captured["content_order"] == 0
    assert session.commit_count == 1


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_create_content_rejects_missing_or_malformed_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Từ chối Bearer thiếu hoặc sai định dạng trước khi truy vấn course."""

    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )
    headers = {} if authorization is None else {"Authorization": authorization}

    response = post_content(client, headers=headers)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_create_content_rejects_non_mentor_role_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối role Student trước mọi truy vấn ghi Content."""

    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = post_content(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


@pytest.mark.parametrize(
    "body",
    [
        {"content_type": "lesson-node", "title": "Title", "payload": {}},
        request_body(course_id="101"),
        request_body(course_id=True),
        request_body(content_type=12),
        request_body(title=12),
        request_body(payload=[]),
        request_body(status="PUBLISHED"),
    ],
)
def test_create_content_rejects_invalid_body_with_design_validation_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: dict[str, Any],
) -> None:
    """Trả đúng validation business code cho thiếu, sai kiểu hoặc field ngoài contract."""

    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = post_content(client, body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"]


@pytest.mark.parametrize("course", [None, course_row(mentor_id=2002)])
def test_create_content_maps_absent_or_non_owned_course_to_access_denied(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    course: dict[str, Any] | None,
) -> None:
    """Dùng một lỗi 403 cho course vắng mặt và course không thuộc Mentor."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(content_view, "query_one", lambda *_args, **_kwargs: course)

    response = post_content(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize("course", [{"id": 101}, course_row(id=999)])
def test_create_content_rejects_invalid_course_projection_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    course: dict[str, Any],
) -> None:
    """Trả lỗi nội bộ khi query trả course row không khớp request."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(content_view, "query_one", lambda *_args, **_kwargs: course)

    response = post_content(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


@pytest.mark.parametrize("failed_call", [1, 2, 3])
def test_create_content_rolls_back_database_query_failures(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failed_call: int,
) -> None:
    """Rollback transaction và ẩn chi tiết lỗi tại course, order hoặc insert query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    call_index = 0

    def query_one(_db, _query, _params):
        """Phát sinh SQLAlchemyError ở bước được chọn để kiểm tra rollback."""

        nonlocal call_index
        call_index += 1
        if call_index == failed_call:
            raise SQLAlchemyError("private database detail")
        if call_index == 1:
            return course_row()
        if call_index == 2:
            return {"next_order": 0}
        return content_row()

    monkeypatch.setattr(content_view, "query_one", query_one)

    response = post_content(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private database detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_create_content_rolls_back_invalid_insert_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không commit khi INSERT/RETURNING projection khác với Content vừa yêu cầu."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    call_index = 0

    def query_one(_db, _query, _params):
        """Trả một insert row có status sai sau hai projection hợp lệ."""

        nonlocal call_index
        call_index += 1
        if call_index == 1:
            return course_row()
        if call_index == 2:
            return {"next_order": 0}
        return content_row(status="PUBLISHED")

    monkeypatch.setattr(content_view, "query_one", query_one)

    response = post_content(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_create_content_maps_commit_failure_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ánh xạ lỗi commit thành 500 an toàn và gọi rollback transaction."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    call_index = 0

    def query_one(_db, _query, _params):
        """Trả đủ course, order và inserted Content để lỗi chỉ xảy ra lúc commit."""

        nonlocal call_index
        call_index += 1
        if call_index == 1:
            return course_row()
        if call_index == 2:
            return {"next_order": 0}
        return content_row()

    monkeypatch.setattr(content_view, "query_one", query_one)

    response = post_content(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_create_content_propagates_trace_id(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Truyền trace ID request vào success envelope và response header."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    call_index = 0

    def query_one(_db, _query, _params):
        """Trả các projection thành công trong thứ tự query API #50."""

        nonlocal call_index
        call_index += 1
        if call_index == 1:
            return course_row()
        if call_index == 2:
            return {"next_order": 0}
        return content_row()

    monkeypatch.setattr(content_view, "query_one", query_one)
    trace_id = "f25e0fb8-ae67-40ae-8d6f-c50c660e5d17"

    response = client.post(
        "/api/v1/mentor/content",
        json=request_body(),
        headers={
            "Authorization": "Bearer valid-token",
            "X-Trace-Id": trace_id,
        },
    )

    assert response.status_code == 201
    assert response.headers["X-Trace-Id"] == trace_id
    assert response.json()["traceId"] == trace_id


def test_create_content_route_openapi_declares_int64_request_and_created_response(
    client: TestClient,
) -> None:
    """Kiểm tra OpenAPI công bố required body int64 và HTTP 201 response envelope."""

    schema = client.app.openapi()
    operation = schema["paths"]["/api/v1/mentor/content"]["post"]
    request_schema_ref = operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
    request_schema_name = request_schema_ref.rsplit("/", 1)[-1]
    request_schema = schema["components"]["schemas"][request_schema_name]
    assert request_schema["required"] == ["course_id", "content_type", "title", "payload"]
    assert request_schema["properties"]["course_id"]["format"] == "int64"
    assert operation["responses"]["201"]["description"] == "Successful Response"


def test_create_content_returns_design_validation_code_for_framework_body_error(
    client: TestClient,
) -> None:
    """Xác nhận middleware dispatch framework validation của route theo DESIGN contract."""

    response = client.post(
        "/api/v1/mentor/content",
        json=request_body(payload=[]),
        headers={"Authorization": "Bearer valid-token"},
    )

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
