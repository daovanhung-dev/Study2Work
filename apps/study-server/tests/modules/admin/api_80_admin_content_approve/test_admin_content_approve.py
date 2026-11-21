from __future__ import annotations

from typing import Any

import app.modules.admin.api_78_admin_content_pending.view as pending_view
import app.modules.admin.api_79_admin_content_detail.view as detail_view
import app.modules.admin.api_80_admin_content_approve.view as approve_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

_DEFAULT_ROW = object()


class FakeSession:
    """Session giả ghi nhận commit/rollback và có thể giả lập lỗi commit."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Đếm commit hoặc phát sinh lỗi database được cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("private commit detail")

    def rollback(self) -> None:
        """Đếm rollback khi transaction phê duyệt phải bị hủy."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả session giả cho một request."""

    def dependency():
        """Yield session giả cho dependency FastAPI."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Thay decoder để cấp principal test có subject số và role tùy chọn."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def content_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection Content hợp lệ sau transition sang APPROVED."""

    return {
        "id": 901,
        "course_id": 501,
        "content_type": "QUIZ",
        "title": "Reviewable quiz",
        "payload": {"question_count": 4},
        "status": "APPROVED",
        "parent_id": None,
        "order": 2,
        **overrides,
    }


def install_approval_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    lock_row: Any = _DEFAULT_ROW,
    update_row: Any = _DEFAULT_ROW,
    fail_lock: bool = False,
    fail_update: bool = False,
    fail_audit: bool = False,
) -> tuple[list[tuple[str, dict[str, Any]]], list[dict[str, Any]]]:
    """Cài DB doubles và ghi nhận SQL/bindings cùng audit parameters."""

    queries: list[tuple[str, dict[str, Any]]] = []
    audit_rows: list[dict[str, Any]] = []

    def query_one(_db, query, params):
        """Trả lock/update row giả hoặc giả lập lỗi theo câu SQL."""

        bound = dict(params)
        queries.append((query, bound))
        if query == approve_view.LOCK_ADMIN_CONTENT_FOR_APPROVAL:
            if fail_lock:
                raise SQLAlchemyError("private lock detail")
            return {"id": 901, "status": "PENDING_REVIEW"} if lock_row is _DEFAULT_ROW else lock_row
        if query == approve_view.APPROVE_ADMIN_CONTENT:
            if fail_update:
                raise SQLAlchemyError("private update detail")
            return content_row() if update_row is _DEFAULT_ROW else update_row
        raise AssertionError("unexpected approval query")

    def execute_query(_db, query, params):
        """Ghi audit bindings hoặc giả lập lỗi append audit."""

        assert query == approve_view.INSERT_ADMIN_CONTENT_REVIEW_AUDIT
        if fail_audit:
            raise SQLAlchemyError("private audit detail")
        audit_rows.append(dict(params))

    monkeypatch.setattr(approve_view, "query_one", query_one)
    monkeypatch.setattr(approve_view, "execute_query", execute_query)
    return queries, audit_rows


def patch_approval(
    client: TestClient,
    *,
    content_id: str = "901",
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP PATCH API #80 với raw path và Authorization tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.patch(
        f"/api/v1/admin/content/{content_id}/approve",
        headers=headers,
    )


def test_patch_admin_content_approves_and_audits_atomically(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Chuyển pending sang APPROVED, append actor audit và commit một lần."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, audit_rows = install_approval_queries(monkeypatch)

    response = patch_approval(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["data"] == {
        "id": 901,
        "course_id": 501,
        "content_type": "QUIZ",
        "title": "Reviewable quiz",
        "payload": {"question_count": 4},
        "status": "APPROVED",
        "order": 2,
    }
    assert [query for query, _ in queries] == [
        approve_view.LOCK_ADMIN_CONTENT_FOR_APPROVAL,
        approve_view.APPROVE_ADMIN_CONTENT,
    ]
    assert queries[0][1] == {"content_id": 901}
    assert queries[1][1] == {"content_id": 901}
    assert "deleted_at IS NULL" in queries[0][0]
    assert "FOR UPDATE" in queries[0][0]
    assert "status = 'PENDING_REVIEW'" in queries[1][0]
    assert "content_versions" not in queries[1][0]
    assert audit_rows == [
        {
            "content_id": 901,
            "actor_user_id": 9001,
            "previous_status": "PENDING_REVIEW",
            "new_status": "APPROVED",
            "reason": None,
        }
    ]
    assert payload["traceId"] == response.headers["X-Trace-Id"]
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    ("authorization", "roles", "expected_status", "business_code"),
    [
        (None, ["ADMIN"], 401, "DESIGN_AUTHENTICATION_REQUIRED"),
        ("Bearer student-token", ["STUDENT"], 403, "DESIGN_ACCESS_DENIED"),
    ],
)
def test_patch_admin_content_requires_admin_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str],
    expected_status: int,
    business_code: str,
) -> None:
    """Thiếu token hoặc sai role bị từ chối trước query."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch, roles=roles)

    def fail_query(*_args, **_kwargs):
        """Báo lỗi nếu unauthenticated request truy cập database."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(approve_view, "query_one", fail_query)
    response = patch_approval(client, authorization=authorization)

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == business_code


@pytest.mark.parametrize(
    "content_id",
    ["invalid", "9223372036854775808", "-9223372036854775809"],
)
def test_patch_admin_content_maps_malformed_or_overflow_path_to_422(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    content_id: str,
) -> None:
    """Path sai format hoặc signed-int64 range trả 422 trước DB."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Báo lỗi nếu invalid path tiếp tục tới database."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(approve_view, "query_one", fail_query)
    response = patch_approval(client, content_id=content_id)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "content_id"


def test_patch_admin_content_returns_404_for_missing_or_soft_deleted_row(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không có active row dùng catalog 404 và rollback transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, audit_rows = install_approval_queries(monkeypatch, lock_row=None)

    response = patch_approval(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert len(queries) == 1
    assert audit_rows == []
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize("current_status", ["APPROVED", "PUBLISHED", "REJECTED", "DRAFT"])
def test_patch_admin_content_requires_pending_review_state(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    current_status: str,
) -> None:
    """Content ngoài PENDING_REVIEW trả catalog 422 mà không ghi audit."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, audit_rows = install_approval_queries(
        monkeypatch,
        lock_row={"id": 901, "status": current_status},
    )

    response = patch_approval(client)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert len(queries) == 1
    assert audit_rows == []
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    ("failure", "lock_row", "update_row", "fail_lock", "fail_update", "fail_audit"),
    [
        ("lock", _DEFAULT_ROW, _DEFAULT_ROW, True, False, False),
        ("update", _DEFAULT_ROW, _DEFAULT_ROW, False, True, False),
        ("audit", _DEFAULT_ROW, _DEFAULT_ROW, False, False, True),
        ("wrong identity", _DEFAULT_ROW, content_row(id=902), False, False, False),
        ("wrong status", _DEFAULT_ROW, content_row(status="PENDING_REVIEW"), False, False, False),
        ("bad payload", _DEFAULT_ROW, content_row(payload=["not-object"]), False, False, False),
        ("missing field", _DEFAULT_ROW, {"id": 901}, False, False, False),
        ("malformed lock", {}, _DEFAULT_ROW, False, False, False),
    ],
)
def test_patch_admin_content_rolls_back_safe_internal_failures(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
    lock_row: Any,
    update_row: Any,
    fail_lock: bool,
    fail_update: bool,
    fail_audit: bool,
) -> None:
    """Query, audit hoặc projection lỗi trả 500 an toàn và rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_approval_queries(
        monkeypatch,
        lock_row=lock_row,
        update_row=update_row,
        fail_lock=fail_lock,
        fail_update=fail_update,
        fail_audit=fail_audit,
    )

    response = patch_approval(client)

    assert response.status_code == 500, failure
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_patch_admin_content_rolls_back_commit_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Commit failure trả safe 500 rồi gọi rollback."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_approval_queries(monkeypatch)

    response = patch_approval(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_admin_content_approval_openapi_matches_catalog_without_request_body(
    client: TestClient,
) -> None:
    """OpenAPI khai báo path int64, Authorization và đúng response set #80."""

    operation = client.app.openapi()["paths"][
        "/api/v1/admin/content/{content_id}/approve"
    ]["patch"]
    parameters = {
        (item["name"], item["in"]): item
        for item in operation["parameters"]
    }

    assert parameters[("content_id", "path")]["required"] is True
    assert parameters[("content_id", "path")]["schema"]["format"] == "int64"
    assert parameters[("Authorization", "header")]["required"] is True
    assert "requestBody" not in operation
    assert operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "/ApproveAdminContentEnvelope"
    )
    assert {"401", "403", "404", "422", "500"}.issubset(operation["responses"])


def test_pending_and_content_detail_routes_remain_reachable(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Thêm action route không đổi static #78 hoặc dynamic GET #79."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    monkeypatch.setattr(pending_view, "query_one", lambda *_args: {"total": 0})
    monkeypatch.setattr(pending_view, "query_many", lambda *_args: [])
    monkeypatch.setattr(detail_view, "query_one", lambda *_args: {
        "id": 901,
        "course_id": 501,
        "content_type": "QUIZ",
        "title": "Reviewable quiz",
        "payload": {"question_count": 4},
        "status": "PENDING_REVIEW",
        "parent_id": None,
        "order": 2,
    })

    pending = client.get(
        "/api/v1/admin/content/pending",
        headers={"Authorization": "Bearer valid-admin-token"},
    )
    detail = client.get(
        "/api/v1/admin/content/901",
        headers={"Authorization": "Bearer valid-admin-token"},
    )

    assert pending.status_code == 200
    assert pending.json()["data"]["items"] == []
    assert detail.status_code == 200
    assert detail.json()["data"]["status"] == "PENDING_REVIEW"
