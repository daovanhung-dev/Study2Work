from __future__ import annotations

from typing import Any

import app.modules.mentor.api_49_mentor_content_list.view as content_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    def __init__(self) -> None:
        """Theo dõi commit và rollback của request chỉ đọc cây Content."""
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận commit ngoài dự kiến của endpoint chỉ đọc."""
        self.commit_count += 1

    def rollback(self) -> None:
        """Ghi nhận cleanup transaction sau lỗi hoặc nhánh không thành công."""
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override dùng fake session trong một request TestClient."""

    def dependency():
        """Yield fake session mà test đang theo dõi."""
        yield session

    return dependency


def allow_mentor_token(monkeypatch: pytest.MonkeyPatch, *, roles: list[str] | None = None) -> None:
    """Thay JWT decoder bằng numeric subject có role Mentor để kiểm tra route."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": roles or ["MENTOR"]},
    )


def course_row(**overrides: Any) -> dict[str, Any]:
    """Tạo hàng course legacy có Mentor trực tiếp sở hữu."""

    return {"id": 101, "mentor_id": 1001, **overrides}


def content_row(**overrides: Any) -> dict[str, Any]:
    """Tạo hàng Content theo projection legacy của API #49."""

    return {
        "id": 49001,
        "course_id": 101,
        "content_type": "lesson-node",
        "title": "Nội dung mẫu",
        "payload": {"body": "Nội dung kiểm thử"},
        "status": "draft-like",
        "parent_id": None,
        "order": 1,
        **overrides,
    }


def get_contents_response(client: TestClient, course_id: str = "101"):
    """Gửi GET API #49 với Bearer token dùng trong kiểm thử."""

    return client.get(
        f"/api/v1/mentor/courses/{course_id}/content",
        headers={"Authorization": "Bearer valid-token"},
    )


def test_get_course_contents_returns_flat_tree_and_keeps_parent_links(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả toàn bộ node theo thứ tự SQL và giữ link cha-con trong response."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: dict[str, Any] = {}

    def find_course(_db, query, params):
        """Ghi nhận truy vấn ownership và trả course của Mentor hiện tại."""

        captured["course_sql"] = query
        assert params == {"course_id": 101}
        return course_row()

    def find_contents(_db, query, params):
        """Ghi nhận truy vấn cây và trả roots cùng child theo sibling order."""

        captured["contents_sql"] = query
        assert params == {"course_id": 101}
        return [
            content_row(id=49001, title="Root A", order=1),
            content_row(id=49002, title="Child A1", parent_id=49001, order=1),
            content_row(id=49003, title="Root B", order=2, status="published-like"),
        ]

    monkeypatch.setattr(content_view, "query_one", find_course)
    monkeypatch.setattr(content_view, "query_many", find_contents)

    response = get_contents_response(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert [node["id"] for node in payload["data"]] == [49001, 49002, 49003]
    assert "parent_id" not in payload["data"][0]
    assert payload["data"][1]["parent_id"] == 49001
    assert payload["data"][2]["status"] == "published-like"
    assert payload["data"][0]["payload"] == {"body": "Nội dung kiểm thử"}
    assert "mentor_id" in captured["course_sql"]
    assert "deleted_at IS NULL" in captured["contents_sql"]
    assert "ORDER BY parent_id NULLS FIRST, content_order ASC, id ASC" in captured["contents_sql"]
    assert "status =" not in captured["contents_sql"].lower()
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_course_contents_returns_empty_array_for_empty_course(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả thành công với mảng rỗng khi course tồn tại nhưng chưa có nội dung."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(content_view, "query_one", lambda *_args, **_kwargs: course_row())
    monkeypatch.setattr(content_view, "query_many", lambda *_args, **_kwargs: [])

    response = get_contents_response(client)

    assert response.status_code == 200
    assert response.json()["data"] == []
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_get_course_contents_rejects_bad_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Từ chối Bearer thiếu hoặc sai định dạng trước mọi truy vấn."""

    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )
    headers = {} if authorization is None else {"Authorization": authorization}

    response = client.get("/api/v1/mentor/courses/101/content", headers=headers)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_get_course_contents_rejects_non_mentor_role_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối role Student trên endpoint Mentor trước khi đọc database."""

    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = get_contents_response(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


@pytest.mark.parametrize("course_id", ["abc", "9223372036854775808", "-9223372036854775809"])
def test_get_course_contents_maps_malformed_id_to_catalog_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    course_id: str,
) -> None:
    """Ánh xạ path sai format hoặc ngoài signed-int64 vào lỗi 404 đã khai báo."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("invalid ID must not query")
        ),
    )

    response = get_contents_response(client, course_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_course_contents_returns_not_found_for_missing_course(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 404 khi course không tồn tại và rollback read transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(content_view, "query_one", lambda *_args, **_kwargs: None)

    response = get_contents_response(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_course_contents_forbids_another_mentor_before_content_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Yêu cầu trực tiếp sở hữu course trước khi đọc Content rows."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: course_row(mentor_id=2002),
    )
    monkeypatch.setattr(
        content_view,
        "query_many",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("content query must not run")
        ),
    )

    response = get_contents_response(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    "rows",
    [
        [content_row(parent_id=49999)],
        [content_row(id=49001, parent_id=49002), content_row(id=49002, parent_id=49001)],
        [content_row(payload=["not", "an", "object"])],
        [content_row(course_id=999)],
        [content_row(), content_row()],
    ],
)
def test_get_course_contents_rejects_broken_tree_or_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    rows: list[dict[str, Any]],
) -> None:
    """Không trả cây một phần khi parent, cycle, JSON type hoặc row integrity sai."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(content_view, "query_one", lambda *_args, **_kwargs: course_row())
    monkeypatch.setattr(content_view, "query_many", lambda *_args, **_kwargs: rows)

    response = get_contents_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


@pytest.mark.parametrize("query_stage", ["course", "contents"])
def test_get_course_contents_returns_safe_error_for_query_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    query_stage: str,
) -> None:
    """Ẩn chi tiết SQL và rollback transaction khi một trong hai query thất bại."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)

    def find_course(*_args, **_kwargs):
        """Trả lỗi SQL tại bước course hoặc một course hợp lệ cho bước kế tiếp."""

        if query_stage == "course":
            raise SQLAlchemyError("private database detail")
        return course_row()

    def find_contents(*_args, **_kwargs):
        """Mô phỏng lỗi truy vấn nội dung khi test đang kiểm tra bước thứ hai."""

        raise SQLAlchemyError("private database detail")

    monkeypatch.setattr(content_view, "query_one", find_course)
    monkeypatch.setattr(content_view, "query_many", find_contents)

    response = get_contents_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private database detail" not in response.text
    assert session.rollback_count == 1


def test_get_course_contents_route_openapi_uses_int64_and_array_response(
    client: TestClient,
) -> None:
    """Kiểm tra OpenAPI công bố course ID int64 và danh sách Content response."""

    schema = client.app.openapi()
    operation = schema["paths"]["/api/v1/mentor/courses/{course_id}/content"]["get"]
    course_id_parameter = next(
        parameter for parameter in operation["parameters"] if parameter["name"] == "course_id"
    )

    assert course_id_parameter["schema"]["type"] == "integer"
    assert course_id_parameter["schema"]["format"] == "int64"
    envelope_schema = schema["components"]["schemas"]["GetCourseContentsEnvelope"]
    assert envelope_schema["properties"]["data"]["type"] == "array"
    assert envelope_schema["properties"]["data"]["items"]["$ref"].endswith("/ContentResponse")


def test_get_course_contents_propagates_trace_id(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Truyền trace ID request vào envelope và response header."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(content_view, "query_one", lambda *_args, **_kwargs: course_row())
    monkeypatch.setattr(content_view, "query_many", lambda *_args, **_kwargs: [])
    trace_id = "f25e0fb8-ae67-40ae-8d6f-c50c660e5d17"

    response = client.get(
        "/api/v1/mentor/courses/101/content",
        headers={"Authorization": "Bearer valid-token", "X-Trace-Id": trace_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Trace-Id"] == trace_id
    assert response.json()["traceId"] == trace_id
