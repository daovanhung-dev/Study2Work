"""HTTP tests cho API #76 đổi status khóa học Admin."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import app.modules.admin.api_76_admin_course_status.view as status_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_74_admin_course_detail.query import FIND_ADMIN_COURSE_DETAIL
from app.modules.admin.api_76_admin_course_status.query import (
    INSERT_ADMIN_COURSE_STATUS_AUDIT,
    LOCK_ADMIN_COURSE_STATUS,
    UPDATE_ADMIN_COURSE_STATUS,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Đếm transaction calls và giả lập commit failure cho API #76."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        """Khởi tạo bộ đếm transaction và tùy chọn lỗi commit."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát sinh lỗi DB đã cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("sensitive commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback do lỗi hoặc không tìm thấy course."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả session giả cho TestClient."""

    def dependency():
        """Yield session test cho dependency get_db."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cài decoder giả trả JWT Admin hoặc role test được chỉ định."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def course_row(status: str = "PUBLISHED", **overrides: Any) -> dict[str, Any]:
    """Tạo Course/mentor projection candidate tương ứng API #74."""

    return {
        "id": 11,
        "title": "Linear Algebra II",
        "description": "Course description",
        "thumbnail_url": "https://example.test/course.png",
        "price": Decimal("199.00"),
        "status": status,
        "mentor_id": 501,
        "mentor_full_name": "Ada Lovelace",
        "mentor_avatar_url": None,
        **overrides,
    }


def patch_course_status(
    client: TestClient,
    course_id: str = "11",
    *,
    target_status: str = "PUBLISHED",
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP PATCH API #76 với raw path, target status và Authorization."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.patch(
        f"/api/v1/admin/courses/{course_id}/status",
        headers=headers,
        json={"status": target_status},
    )


def install_status_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    current_status: str | None = "DRAFT",
    update_row: dict[str, Any] | None = None,
    detail_row: dict[str, Any] | None = None,
    fail_lock: bool = False,
    fail_update: bool = False,
    fail_detail: bool = False,
    fail_audit: bool = False,
) -> tuple[list[tuple[str, dict[str, Any]]], list[dict[str, Any]]]:
    """Cài DB doubles, giữ query order/bindings và audit insert parameters."""

    queries: list[tuple[str, dict[str, Any]]] = []
    audit_rows: list[dict[str, Any]] = []

    def query_one(_db, query, params):
        """Trả từng row lock, update result, hoặc Course detail projection."""

        bound = dict(params)
        queries.append((query, bound))
        if query == LOCK_ADMIN_COURSE_STATUS:
            if fail_lock:
                raise SQLAlchemyError("sensitive lock detail")
            if current_status == "__MISSING__":
                return None
            if current_status == "__MALFORMED__":
                return {}
            return {"status": current_status}
        if query == UPDATE_ADMIN_COURSE_STATUS:
            if fail_update:
                raise SQLAlchemyError("sensitive update detail")
            return {"id": 11, "status": bound["status"]} if update_row is None else update_row
        if query == FIND_ADMIN_COURSE_DETAIL:
            if fail_detail:
                raise SQLAlchemyError("sensitive detail query")
            return course_row() if detail_row is None else detail_row
        raise AssertionError(f"Unexpected query: {query}")

    def execute_query(_db, query, params):
        """Ghi nhận audit insert hoặc giả lập lỗi khi append log."""

        assert query == INSERT_ADMIN_COURSE_STATUS_AUDIT
        if fail_audit:
            raise SQLAlchemyError("sensitive audit detail")
        audit_rows.append(dict(params))

    monkeypatch.setattr(status_view, "query_one", query_one)
    monkeypatch.setattr(status_view, "execute_query", execute_query)
    return queries, audit_rows


def test_patch_admin_course_status_updates_and_audits_in_same_transaction(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cập nhật status, ghi actor/old/new và trả CoursePage trước commit."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, audit_rows = install_status_queries(monkeypatch)

    response = patch_course_status(client, target_status="PUBLISHED")

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["data"]["items"][0]["status"] == "PUBLISHED"
    assert payload["data"]["pagination"] == {
        "page": 1,
        "size": 1,
        "total": 1,
        "total_pages": 1,
    }
    assert [query for query, _ in queries] == [
        LOCK_ADMIN_COURSE_STATUS,
        UPDATE_ADMIN_COURSE_STATUS,
        FIND_ADMIN_COURSE_DETAIL,
    ]
    assert queries[1][1] == {"course_id": 11, "status": "PUBLISHED"}
    assert audit_rows == [
        {
            "course_id": 11,
            "actor_user_id": 9001,
            "previous_status": "DRAFT",
            "new_status": "PUBLISHED",
        }
    ]
    assert payload["traceId"]
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_patch_admin_course_status_same_value_is_noop_without_duplicate_audit(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Lặp lại status hiện tại chỉ đọc projection và không ghi audit duplicate."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, audit_rows = install_status_queries(
        monkeypatch,
        current_status="PUBLISHED",
        detail_row=course_row("PUBLISHED"),
    )

    response = patch_course_status(client, target_status="PUBLISHED")

    assert response.status_code == 200
    assert [query for query, _ in queries] == [LOCK_ADMIN_COURSE_STATUS, FIND_ADMIN_COURSE_DETAIL]
    assert audit_rows == []
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    ("authorization", "roles", "expected_status", "business_code"),
    [
        (None, ["ADMIN"], 401, "DESIGN_AUTHENTICATION_REQUIRED"),
        ("Bearer student-token", ["STUDENT"], 403, "DESIGN_ACCESS_DENIED"),
    ],
)
def test_patch_admin_course_status_requires_admin_before_db(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str],
    expected_status: int,
    business_code: str,
) -> None:
    """Thiếu token hoặc role ADMIN bị từ chối trước query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch, roles=roles)
    queries, _audit_rows = install_status_queries(monkeypatch)

    response = patch_course_status(client, authorization=authorization)

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == business_code
    assert queries == []
    assert session.commit_count == 0


@pytest.mark.parametrize("course_id", ["abc", "9223372036854775808", "-9223372036854775809"])
def test_patch_admin_course_status_rejects_invalid_signed_int64_path(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    course_id: str,
) -> None:
    """Malformed/out-of-range course ID maps to catalog 422 before DB."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, _audit_rows = install_status_queries(monkeypatch)

    response = patch_course_status(client, course_id)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "course_id"
    assert queries == []


@pytest.mark.parametrize(
    ("body", "field"),
    [({"status": "ARCHIVED"}, "status"), ({"status": "DRAFT", "extra": True}, "body")],
)
def test_patch_admin_course_status_rejects_invalid_body_with_contract_envelope(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: dict[str, Any],
    field: str,
) -> None:
    """Unknown status and extra properties use the API validation envelope."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    response = client.patch(
        "/api/v1/admin/courses/11/status",
        headers={"Authorization": "Bearer valid-admin-token"},
        json=body,
    )

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None
    assert session.commit_count == 0
    if field == "status":
        assert response.json()["meta"]["fieldErrors"][0]["field"] == "status"


def test_patch_admin_course_status_not_found_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Course ID hợp lệ không có row trả 404 catalog."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, audit_rows = install_status_queries(monkeypatch, current_status="__MISSING__")

    response = patch_course_status(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert len(queries) == 1
    assert audit_rows == []
    assert session.rollback_count == 1


def test_patch_admin_course_status_rejects_malformed_locked_status_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Missing status column in lock result fails closed before mutation."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, audit_rows = install_status_queries(
        monkeypatch,
        current_status="__MALFORMED__",
    )

    response = patch_course_status(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert [query for query, _ in queries] == [LOCK_ADMIN_COURSE_STATUS]
    assert audit_rows == []
    assert session.rollback_count == 1


@pytest.mark.parametrize("failure", ["lock", "update", "audit", "detail", "commit"])
def test_patch_admin_course_status_rolls_back_on_transaction_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    """Lock/update/audit/projection/commit failure maps to safe 500 and rollback."""

    session = FakeSession(fail_commit=failure == "commit")
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, _audit_rows = install_status_queries(
        monkeypatch,
        fail_lock=failure == "lock",
        fail_update=failure == "update",
        fail_audit=failure == "audit",
        fail_detail=failure == "detail",
    )

    response = patch_course_status(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "sensitive" not in response.text
    assert session.rollback_count == 1
    if failure == "lock":
        assert [query for query, _ in queries] == [LOCK_ADMIN_COURSE_STATUS]
    if failure == "audit":
        assert [query for query, _ in queries] == [
            LOCK_ADMIN_COURSE_STATUS,
            UPDATE_ADMIN_COURSE_STATUS,
        ]


def test_patch_admin_course_status_rejects_bad_update_identity_and_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bad RETURNING identity or mismatched readback cannot commit status/audit."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_status_queries(
        monkeypatch,
        update_row={"id": 12, "status": "PUBLISHED"},
    )

    response = patch_course_status(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_patch_admin_course_status_openapi_matches_catalog_contract(client: TestClient) -> None:
    """OpenAPI exposes PATCH body, int64 path and catalog response statuses."""

    operation = client.app.openapi()["paths"][
        "/api/v1/admin/courses/{course_id}/status"
    ]["patch"]

    assert operation["parameters"] == [
        {
            "name": "course_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer", "format": "int64"},
        },
        {
            "name": "Authorization",
            "in": "header",
            "required": True,
            "schema": {"type": "string"},
        },
    ]
    assert operation["requestBody"]["required"] is True
    assert {"200", "401", "403", "404", "422", "500"}.issubset(operation["responses"])
