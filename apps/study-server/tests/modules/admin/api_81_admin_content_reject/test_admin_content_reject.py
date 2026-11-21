from __future__ import annotations

from typing import Any

import app.modules.admin.api_78_admin_content_pending.view as pending_view
import app.modules.admin.api_79_admin_content_detail.view as detail_view
import app.modules.admin.api_80_admin_content_approve.view as approve_view
import app.modules.admin.api_81_admin_content_reject.view as reject_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

_DEFAULT_ROW = object()
_DEFAULT_BODY = object()
_NO_BODY = object()


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
        """Đếm rollback khi quyết định review phải bị hủy."""

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
    """Tạo projection Content hợp lệ sau transition sang REJECTED."""

    return {
        "id": 901,
        "course_id": 501,
        "content_type": "QUIZ",
        "title": "Reviewable quiz",
        "payload": {"question_count": 4},
        "status": "REJECTED",
        "parent_id": None,
        "order": 2,
        **overrides,
    }


def install_rejection_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    lock_row: Any = _DEFAULT_ROW,
    update_row: Any = _DEFAULT_ROW,
    fail_lock: bool = False,
    fail_update: bool = False,
    fail_decision: bool = False,
) -> tuple[list[tuple[str, dict[str, Any]]], list[dict[str, Any]]]:
    """Cài DB doubles và ghi nhận SQL/bindings cùng decision parameters."""

    queries: list[tuple[str, dict[str, Any]]] = []
    decisions: list[dict[str, Any]] = []

    def query_one(_db, query, params):
        """Trả lock/update row giả hoặc giả lập lỗi theo câu SQL."""

        bound = dict(params)
        queries.append((query, bound))
        if query == reject_view.LOCK_ADMIN_CONTENT_FOR_REJECTION:
            if fail_lock:
                raise SQLAlchemyError("private lock detail")
            return {"id": 901, "status": "PENDING_REVIEW"} if lock_row is _DEFAULT_ROW else lock_row
        if query == reject_view.REJECT_ADMIN_CONTENT:
            if fail_update:
                raise SQLAlchemyError("private update detail")
            return content_row() if update_row is _DEFAULT_ROW else update_row
        raise AssertionError("unexpected rejection query")

    def execute_query(_db, query, params):
        """Ghi reason/actor bindings hoặc giả lập lỗi lưu decision."""

        assert query == reject_view.INSERT_ADMIN_CONTENT_REVIEW_DECISION
        if fail_decision:
            raise SQLAlchemyError("private decision detail")
        decisions.append(dict(params))

    monkeypatch.setattr(reject_view, "query_one", query_one)
    monkeypatch.setattr(reject_view, "execute_query", execute_query)
    return queries, decisions


def patch_rejection(
    client: TestClient,
    *,
    content_id: str = "901",
    authorization: str | None = "Bearer valid-admin-token",
    body: Any = _DEFAULT_BODY,
):
    """Gửi HTTP PATCH API #81 với raw path, Authorization và JSON body."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    request_options: dict[str, Any] = {"headers": headers}
    if body is _DEFAULT_BODY:
        request_options["json"] = {"reason": "The answer key is incomplete."}
    elif body is not _NO_BODY:
        request_options["json"] = body
    return client.patch(f"/api/v1/admin/content/{content_id}/reject", **request_options)


def test_patch_admin_content_rejects_and_records_reason_atomically(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Chuyển pending sang REJECTED và ghi actor/reason cùng transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, decisions = install_rejection_queries(monkeypatch)

    response = patch_rejection(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["data"] == {
        "id": 901,
        "course_id": 501,
        "content_type": "QUIZ",
        "title": "Reviewable quiz",
        "payload": {"question_count": 4},
        "status": "REJECTED",
        "order": 2,
    }
    assert [query for query, _ in queries] == [
        reject_view.LOCK_ADMIN_CONTENT_FOR_REJECTION,
        reject_view.REJECT_ADMIN_CONTENT,
    ]
    assert queries[0][1] == {"content_id": 901}
    assert queries[1][1] == {"content_id": 901}
    assert "deleted_at IS NULL" in queries[0][0]
    assert "FOR UPDATE" in queries[0][0]
    assert "status = 'PENDING_REVIEW'" in queries[1][0]
    assert "content_versions" not in queries[1][0]
    assert decisions == [
        {
            "content_id": 901,
            "actor_user_id": 9001,
            "previous_status": "PENDING_REVIEW",
            "new_status": "REJECTED",
            "reason": "The answer key is incomplete.",
        }
    ]
    assert payload["traceId"] == response.headers["X-Trace-Id"]
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_patch_admin_content_preserves_empty_reason_without_extra_policy(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reason string rỗng vẫn được lưu vì catalog không đặt blank-only rule."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    _queries, decisions = install_rejection_queries(monkeypatch)

    response = patch_rejection(client, body={"reason": ""})

    assert response.status_code == 200
    assert decisions[0]["reason"] == ""
    assert session.commit_count == 1


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
    """Thiếu token hoặc sai role bị từ chối trước truy vấn Content."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch, roles=roles)

    def fail_query(*_args, **_kwargs):
        """Báo lỗi nếu unauthenticated request truy cập database."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(reject_view, "query_one", fail_query)
    response = patch_rejection(client, authorization=authorization)

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
    """Path sai format hoặc signed-int64 range trả 422 trước database."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Báo lỗi nếu invalid path tiếp tục tới database."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(reject_view, "query_one", fail_query)
    response = patch_rejection(client, content_id=content_id)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "content_id"


@pytest.mark.parametrize(
    "body",
    [_NO_BODY, None, {}, {"reason": None}, {"reason": 42}, {"reason": "valid", "extra": True}],
)
def test_patch_admin_content_validates_required_strict_reason(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: Any,
) -> None:
    """Thiếu, sai kiểu hoặc thừa body field dùng catalog 422."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)
    monkeypatch.setattr(
        reject_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("invalid body should not query database")
        ),
    )

    response = patch_rejection(client, body=body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"


def test_patch_admin_content_returns_404_for_missing_or_soft_deleted_row(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không có active row dùng catalog 404 và rollback transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, decisions = install_rejection_queries(monkeypatch, lock_row=None)

    response = patch_rejection(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert len(queries) == 1
    assert decisions == []
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize("current_status", ["APPROVED", "PUBLISHED", "REJECTED", "DRAFT"])
def test_patch_admin_content_requires_pending_review_state(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    current_status: str,
) -> None:
    """Content ngoài PENDING_REVIEW trả catalog 422 mà không ghi decision."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, decisions = install_rejection_queries(
        monkeypatch,
        lock_row={"id": 901, "status": current_status},
    )

    response = patch_rejection(client)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert len(queries) == 1
    assert decisions == []
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    ("failure", "lock_row", "update_row", "fail_lock", "fail_update", "fail_decision"),
    [
        ("lock", _DEFAULT_ROW, _DEFAULT_ROW, True, False, False),
        ("update", _DEFAULT_ROW, _DEFAULT_ROW, False, True, False),
        ("decision", _DEFAULT_ROW, _DEFAULT_ROW, False, False, True),
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
    fail_decision: bool,
) -> None:
    """Query, decision hoặc projection lỗi trả safe 500 và rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_rejection_queries(
        monkeypatch,
        lock_row=lock_row,
        update_row=update_row,
        fail_lock=fail_lock,
        fail_update=fail_update,
        fail_decision=fail_decision,
    )

    response = patch_rejection(client)

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
    install_rejection_queries(monkeypatch)

    response = patch_rejection(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_admin_content_rejection_openapi_matches_catalog(
    client: TestClient,
) -> None:
    """OpenAPI khai báo path int64, Authorization, reason body và catalog errors."""

    operation = client.app.openapi()["paths"][
        "/api/v1/admin/content/{content_id}/reject"
    ]["patch"]
    parameters = {(item["name"], item["in"]): item for item in operation["parameters"]}
    body_schema = operation["requestBody"]["content"]["application/json"]["schema"]

    assert parameters[("content_id", "path")]["required"] is True
    assert parameters[("content_id", "path")]["schema"]["format"] == "int64"
    assert parameters[("Authorization", "header")]["required"] is True
    assert operation["requestBody"]["required"] is True
    assert body_schema["$ref"].endswith("/RejectAdminContentRequest")
    assert {"401", "403", "404", "422", "500"}.issubset(operation["responses"])


def test_pending_detail_and_approval_routes_remain_reachable(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Thêm reject action không đổi queue, detail hoặc API #80 approval route."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    monkeypatch.setattr(pending_view, "query_one", lambda *_args: {"total": 0})
    monkeypatch.setattr(pending_view, "query_many", lambda *_args: [])
    monkeypatch.setattr(
        detail_view,
        "query_one",
        lambda *_args: {
            "id": 901,
            "course_id": 501,
            "content_type": "QUIZ",
            "title": "Reviewable quiz",
            "payload": {"question_count": 4},
            "status": "PENDING_REVIEW",
            "parent_id": None,
            "order": 2,
        },
    )
    monkeypatch.setattr(
        approve_view,
        "query_one",
        lambda _db, query, _params: (
            {"id": 901, "status": "PENDING_REVIEW"}
            if query == approve_view.LOCK_ADMIN_CONTENT_FOR_APPROVAL
            else content_row(status="APPROVED")
        ),
    )
    monkeypatch.setattr(approve_view, "execute_query", lambda *_args: None)

    pending = client.get(
        "/api/v1/admin/content/pending",
        headers={"Authorization": "Bearer valid-admin-token"},
    )
    detail = client.get(
        "/api/v1/admin/content/901",
        headers={"Authorization": "Bearer valid-admin-token"},
    )
    approval = client.patch(
        "/api/v1/admin/content/901/approve",
        headers={"Authorization": "Bearer valid-admin-token"},
    )

    assert pending.status_code == 200
    assert pending.json()["data"]["items"] == []
    assert detail.status_code == 200
    assert detail.json()["data"]["status"] == "PENDING_REVIEW"
    assert approval.status_code == 200
    assert approval.json()["data"]["status"] == "APPROVED"

