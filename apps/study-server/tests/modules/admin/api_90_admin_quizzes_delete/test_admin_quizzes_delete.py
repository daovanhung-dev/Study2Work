from __future__ import annotations

from datetime import datetime
from typing import Any

import app.modules.admin.api_90_admin_quizzes_delete.view as delete_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_90_admin_quizzes_delete.query import (
    CHECK_ADMIN_QUIZ_DELETE_HISTORY,
    DELETE_ADMIN_QUIZ,
    DELETE_ADMIN_QUIZ_CHOICES,
    DELETE_ADMIN_QUIZ_QUESTIONS,
    LOCK_ADMIN_QUIZ_CHOICES_FOR_DELETE,
    LOCK_ADMIN_QUIZ_FOR_DELETE,
    LOCK_ADMIN_QUIZ_QUESTIONS_FOR_DELETE,
    SOFT_DELETE_ADMIN_QUIZ,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

_UNSET = object()


class FakeSession:
    """Session giả ghi nhận commit và rollback cho API #90."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        """Khởi tạo transaction giả với tùy chọn lỗi commit."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát sinh lỗi database giả."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("private commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback của transaction hiện tại."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả session giả cho TestClient."""

    def dependency():
        """Cung cấp session giả cho một HTTP request."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cấp JWT giả có subject và role tùy chọn cho request test."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def delete_request(
    client: TestClient,
    quiz_id: str,
    *,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP DELETE với raw path và Authorization tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.request(
        "DELETE",
        f"/api/v1/admin/quizzes/{quiz_id}",
        headers=headers,
    )


def install_delete_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    lock_row: Any = _UNSET,
    history: tuple[bool, bool] = (False, False),
    fail_query: str | None = None,
    bad_delete: str | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Ghi lại SQL/bindings và mô phỏng các projection của nhánh xóa."""

    captured: list[tuple[str, dict[str, Any]]] = []
    quiz_row = (
        {"id": 5101, "status": "PUBLISHED", "updated_at": datetime(2026, 10, 26, 10)}
        if lock_row is _UNSET
        else lock_row
    )

    def query_one(_db: Any, query: str, params: dict[str, Any]) -> Any:
        """Trả về row phù hợp với SQL constant hoặc giả lập lỗi truy vấn."""

        captured.append((query, dict(params)))
        if query == fail_query:
            raise SQLAlchemyError("private query detail")
        if query == LOCK_ADMIN_QUIZ_FOR_DELETE:
            return quiz_row
        if query == CHECK_ADMIN_QUIZ_DELETE_HISTORY:
            return {"has_attempts": history[0], "has_answers": history[1]}
        if query == SOFT_DELETE_ADMIN_QUIZ:
            return {
                "id": params["quiz_id"],
                "deleted_at": datetime(2026, 10, 26, 10, 30),
            }
        if query == DELETE_ADMIN_QUIZ:
            return {
                "id": params["quiz_id"],
                "deleted_at": datetime(2026, 10, 26, 10, 45),
            }
        raise AssertionError("unexpected query")

    def query_many(_db: Any, query: str, params: dict[str, Any]) -> Any:
        """Trả child ID đã khóa/xóa hoặc một tập kết quả sai có chủ đích."""

        captured.append((query, dict(params)))
        if query == fail_query:
            raise SQLAlchemyError("private query detail")
        if query == LOCK_ADMIN_QUIZ_QUESTIONS_FOR_DELETE:
            return [{"id": 6101}, {"id": 6102}]
        if query == LOCK_ADMIN_QUIZ_CHOICES_FOR_DELETE:
            return [{"id": 7101}, {"id": 7102}]
        if query == DELETE_ADMIN_QUIZ_CHOICES:
            rows = [{"id": 7101}, {"id": 7102}]
            return rows[:1] if bad_delete == "choices" else rows
        if query == DELETE_ADMIN_QUIZ_QUESTIONS:
            rows = [{"id": 6101}, {"id": 6102}]
            return rows[:1] if bad_delete == "questions" else rows
        raise AssertionError("unexpected query")

    monkeypatch.setattr(delete_view, "query_one", query_one)
    monkeypatch.setattr(delete_view, "query_many", query_many)
    return captured


def test_delete_hard_deletes_children_before_quiz_and_returns_database_timestamp(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Xóa child trước Quiz khi không có history và trả timestamp từ database."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch)

    response = delete_request(client, "5101")

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_DELETED"
    assert payload["data"] == {
        "id": 5101,
        "status": "deleted",
        "deleted_at": "2026-10-26T10:45:00",
    }
    assert payload["meta"] == {}
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert [query for query, _ in captured] == [
        LOCK_ADMIN_QUIZ_FOR_DELETE,
        LOCK_ADMIN_QUIZ_QUESTIONS_FOR_DELETE,
        LOCK_ADMIN_QUIZ_CHOICES_FOR_DELETE,
        CHECK_ADMIN_QUIZ_DELETE_HISTORY,
        DELETE_ADMIN_QUIZ_CHOICES,
        DELETE_ADMIN_QUIZ_QUESTIONS,
        DELETE_ADMIN_QUIZ,
    ]
    assert all(params == {"quiz_id": 5101} for _, params in captured)
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize("history", [(True, False), (False, True)])
def test_delete_soft_marks_quiz_and_preserves_children_when_history_exists(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    history: tuple[bool, bool],
) -> None:
    """Giữ nguyên mọi child row nếu có attempt hoặc answer tham chiếu."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch, history=history)

    response = delete_request(client, "5101")

    assert response.status_code == 200
    assert response.json()["data"] == {
        "id": 5101,
        "status": "deleted",
        "deleted_at": "2026-10-26T10:30:00",
    }
    assert [query for query, _ in captured] == [
        LOCK_ADMIN_QUIZ_FOR_DELETE,
        LOCK_ADMIN_QUIZ_QUESTIONS_FOR_DELETE,
        LOCK_ADMIN_QUIZ_CHOICES_FOR_DELETE,
        CHECK_ADMIN_QUIZ_DELETE_HISTORY,
        SOFT_DELETE_ADMIN_QUIZ,
    ]
    assert "status = 'DELETED'" in SOFT_DELETE_ADMIN_QUIZ
    assert "updated_at = CURRENT_TIMESTAMP" in SOFT_DELETE_ADMIN_QUIZ
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_delete_existing_tombstone_is_idempotent_and_keeps_original_timestamp(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DELETE lặp trên tombstone trả lại updated_at mà không chạm child rows."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    original_time = datetime(2026, 10, 20, 8, 15)
    captured = install_delete_queries(
        monkeypatch,
        lock_row={"id": 5101, "status": "DELETED", "updated_at": original_time},
    )

    response = delete_request(client, "5101")

    assert response.status_code == 200
    assert response.json()["data"]["deleted_at"] == "2026-10-20T08:15:00"
    assert captured == [(LOCK_ADMIN_QUIZ_FOR_DELETE, {"quiz_id": 5101})]
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_delete_returns_not_found_for_missing_quiz(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map Quiz vắng mặt sang catalog 404 và rollback transaction đọc."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch, lock_row=None)

    response = delete_request(client, "5101")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None
    assert [query for query, _ in captured] == [LOCK_ADMIN_QUIZ_FOR_DELETE]
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize("quiz_id", ["0", "abc", "1.5", "+1", "-1", str(2**63)])
def test_delete_rejects_invalid_or_out_of_range_id_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    quiz_id: str,
) -> None:
    """Từ chối path ID ngoài miền positive signed-int64 trước mọi truy vấn."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch)

    response = delete_request(client, quiz_id)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None
    assert captured == []
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_delete_authentication_precedes_invalid_path_and_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Yêu cầu token trước khi parse path và trước khi gọi query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    captured = install_delete_queries(monkeypatch)

    response = delete_request(client, "not-an-id", authorization=None)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert response.json()["data"] is None
    assert captured == []


def test_delete_forbids_non_admin_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối principal không có role ADMIN trước khi mở truy vấn."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch, roles=["MENTOR"])
    captured = install_delete_queries(monkeypatch)

    response = delete_request(client, "5101")

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert response.json()["data"] is None
    assert captured == []


@pytest.mark.parametrize(
    "bad_delete",
    ["choices", "questions"],
)
def test_delete_rolls_back_when_returned_child_ids_do_not_match_locked_ids(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    bad_delete: str,
) -> None:
    """Rollback nếu DELETE RETURNING thiếu child ID đã khóa."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch, bad_delete=bad_delete)

    response = delete_request(client, "5101")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert captured[-1][0] == (
        DELETE_ADMIN_QUIZ_CHOICES if bad_delete == "choices" else DELETE_ADMIN_QUIZ_QUESTIONS
    )
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_delete_rolls_back_and_hides_database_error_details(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map lỗi truy vấn sang 500 mà không lộ chi tiết SQLAlchemy."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch, fail_query=CHECK_ADMIN_QUIZ_DELETE_HISTORY)

    response = delete_request(client, "5101")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private query detail" not in response.text
    assert captured[-1][0] == CHECK_ADMIN_QUIZ_DELETE_HISTORY
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_delete_rolls_back_when_commit_fails(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback và trả 500 nếu commit sau khi chuẩn bị kết quả gặp lỗi."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_delete_queries(monkeypatch)

    response = delete_request(client, "5101")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_delete_openapi_has_int64_path_auth_and_no_request_body_or_query(
    client: TestClient,
) -> None:
    """Giữ hợp đồng DELETE path-only cùng tập response catalog đã khai báo."""

    operation = client.app.openapi()["paths"]["/api/v1/admin/quizzes/{quiz_id}"]["delete"]

    assert {item["name"] for item in operation["parameters"]} == {"quiz_id", "Authorization"}
    quiz_id = next(item for item in operation["parameters"] if item["name"] == "quiz_id")
    assert quiz_id["required"] is True
    assert quiz_id["schema"]["format"] == "int64"
    assert quiz_id["schema"]["minimum"] == 1
    assert "requestBody" not in operation
    assert set(operation["responses"]) == {"200", "401", "403", "404", "422", "500"}
