from __future__ import annotations

from datetime import datetime
from typing import Any

import app.modules.mentor.api_53_mentor_content_delete.view as content_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả lập để theo dõi commit/rollback mà không nối database."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        """Theo dõi transaction và tùy chọn làm commit thất bại."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit và phát sinh lỗi nếu test cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("private commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback do view yêu cầu."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override dùng FakeSession cho một HTTP request."""

    def dependency():
        """Yield session giả lập mà không mở PostgreSQL connection."""

        yield session

    return dependency


def allow_mentor_token(monkeypatch: pytest.MonkeyPatch, *, roles: list[str] | None = None) -> None:
    """Thay JWT decoder bằng principal số với role được test yêu cầu."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": roles or ["MENTOR"]},
    )


def current_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection Content mặc định thuộc Mentor 1001."""

    return {
        "id": 50001,
        "course_id": 101,
        "mentor_id": 1001,
        "status": "APPROVED",
        **overrides,
    }


def delete_content(
    client: TestClient,
    *,
    content_id: str = "50001",
    headers: dict[str, str] | None = None,
):
    """Gửi DELETE API #53 với Authorization mặc định hoặc tùy chỉnh."""

    request_headers = {"Authorization": "Bearer valid-token"} if headers is None else headers
    return client.delete(f"/api/v1/mentor/content/{content_id}", headers=request_headers)


def query_rows(
    initial: dict[str, Any],
    dependency: dict[str, Any] | None,
    deleted: dict[str, Any] | None,
    captured: dict[str, Any] | None = None,
):
    """Trả lần lượt Content hiện tại, dependency và kết quả UPDATE RETURNING."""

    results = [initial, dependency, deleted]
    call_index = 0

    def query_one(_db, query, params):
        """Ghi SQL/params rồi trả kết quả tương ứng từng bước."""

        nonlocal call_index
        call_index += 1
        if captured is not None:
            captured[f"query_{call_index}"] = query
            captured[f"params_{call_index}"] = params
        return results[call_index - 1]

    return query_one


def test_delete_content_soft_deletes_and_returns_catalog_result(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Soft-delete row được phép, trả DeleteResult và commit sau khi validate."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    deleted_at = datetime(2026, 10, 25, 10, 30, 15)
    captured: dict[str, Any] = {}
    monkeypatch.setattr(
        content_view,
        "query_one",
        query_rows(
            current_row(),
            {"has_active_child": False},
            {"id": 50001, "deleted_at": deleted_at},
            captured,
        ),
    )

    response = delete_content(client)

    assert response.status_code == 200
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_DELETED"
    assert response.json()["data"] == {
        "id": 50001,
        "status": "deleted",
        "deleted_at": "2026-10-25T10:30:15",
    }
    assert "FOR UPDATE OF content, course" in captured["query_1"]
    assert "content.deleted_at IS NULL" in captured["query_1"]
    assert "child.parent_id = :content_id" in captured["query_2"]
    assert "child.deleted_at IS NULL" in captured["query_2"]
    assert "SET deleted_at = CURRENT_TIMESTAMP" in captured["query_3"]
    assert captured["params_2"] == {"content_id": 50001, "course_id": 101}
    assert captured["params_3"] == {"content_id": 50001, "course_id": 101}
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_delete_content_rejects_bad_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Thiếu hoặc sai Bearer token bị từ chối trước query Content."""

    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )
    headers = {} if authorization is None else {"Authorization": authorization}

    response = delete_content(client, headers=headers)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_delete_content_rejects_non_mentor_role_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Role không phải Mentor bị từ chối trước query Content."""

    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = delete_content(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


@pytest.mark.parametrize("content_id", ["abc", "9223372036854775808", "-9223372036854775809"])
def test_delete_content_maps_invalid_id_to_not_found(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    content_id: str,
) -> None:
    """ID không phải signed int64 ánh xạ về 404 theo Content API convention."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        content_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = delete_content(client, content_id=content_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_delete_content_returns_not_found_for_missing_or_deleted_row(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Target không còn trong active lookup trả lỗi catalog 404."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(content_view, "query_one", lambda *_args, **_kwargs: None)

    response = delete_content(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_delete_content_denies_non_owner(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Direct owner không khớp bị từ chối trước dependency query/mutation."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    calls = 0

    def query_one(_db, _query, _params):
        """Trả row thuộc Mentor khác và đếm query."""

        nonlocal calls
        calls += 1
        return current_row(mentor_id=2002)

    monkeypatch.setattr(content_view, "query_one", query_one)

    response = delete_content(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert calls == 1
    assert session.rollback_count == 1


def test_delete_content_rejects_published_without_dependency_or_write(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """PUBLISHED bị chặn theo proposal DERIVED và không chạy dependency/mutation."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    calls = 0

    def query_one(_db, _query, _params):
        """Trả row PUBLISHED nếu chỉ query lock được gọi."""

        nonlocal calls
        calls += 1
        return current_row(status="PUBLISHED")

    monkeypatch.setattr(content_view, "query_one", query_one)

    response = delete_content(client)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert calls == 1
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_delete_content_rejects_active_child_without_mutation(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Parent có child active trả 422 và không thực hiện soft-delete."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    calls = 0

    def query_one(_db, _query, _params):
        """Trả target rồi báo child active ở dependency check."""

        nonlocal calls
        calls += 1
        if calls == 1:
            return current_row()
        return {"has_active_child": True}

    monkeypatch.setattr(content_view, "query_one", query_one)

    response = delete_content(client)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert calls == 2
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize("status", ["PENDING_REVIEW", "APPROVED", "REJECTED"])
def test_delete_content_accepts_non_published_statuses(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    status: str,
) -> None:
    """Các trạng thái ngoài PUBLISHED được soft-delete theo fallback DERIVED."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    deleted_at = datetime(2026, 10, 25, 10, 30, 15)
    monkeypatch.setattr(
        content_view,
        "query_one",
        query_rows(
            current_row(status=status),
            {"has_active_child": False},
            {"id": 50001, "deleted_at": deleted_at},
        ),
    )

    response = delete_content(client)

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "deleted"
    assert session.commit_count == 1


def test_delete_content_returns_internal_error_on_database_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Lỗi DB được rollback, ẩn chi tiết và map sang mã 500 trong catalog."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Mô phỏng lỗi PostgreSQL mà không tiết lộ nội dung."""

        raise SQLAlchemyError("private SQL detail")

    monkeypatch.setattr(content_view, "query_one", fail_query)

    response = delete_content(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private SQL detail" not in response.text
    assert session.rollback_count == 1


def test_delete_content_rolls_back_when_commit_fails(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Commit lỗi trả 500 an toàn và rollback transaction."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        content_view,
        "query_one",
        query_rows(
            current_row(),
            {"has_active_child": False},
            {"id": 50001, "deleted_at": datetime(2026, 10, 25, 10, 30, 15)},
        ),
    )

    response = delete_content(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_delete_content_openapi_declares_path_without_request_body(client: TestClient) -> None:
    """OpenAPI giữ path int64 và không công bố body/query ngoài catalog."""

    schema = client.app.openapi()
    operation = schema["paths"]["/api/v1/mentor/content/{content_id}"]["delete"]
    path_parameter = next(item for item in operation["parameters"] if item["name"] == "content_id")

    assert "requestBody" not in operation
    assert path_parameter["schema"]["format"] == "int64"
    assert all(item["in"] in {"path", "header"} for item in operation["parameters"])
    response_schema_ref = operation["responses"]["200"]["content"]["application/json"]["schema"][
        "$ref"
    ]
    envelope_schema = schema["components"]["schemas"][response_schema_ref.rsplit("/", 1)[-1]]
    result_schema_ref = envelope_schema["properties"]["data"]["$ref"]
    result_schema = schema["components"]["schemas"][result_schema_ref.rsplit("/", 1)[-1]]

    assert result_schema["properties"]["id"]["format"] == "int64"
    assert result_schema["properties"]["status"]["const"] == "deleted"
    assert result_schema["properties"]["deleted_at"]["format"] == "date-time"
