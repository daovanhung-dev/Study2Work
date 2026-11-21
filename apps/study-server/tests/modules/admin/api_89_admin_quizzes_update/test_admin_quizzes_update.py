from __future__ import annotations

import json
from decimal import Decimal
from typing import Any

import app.modules.admin.api_89_admin_quizzes_update.view as quizzes_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_88_admin_quizzes_create.query import (
    INSERT_ADMIN_QUIZ_CHOICE,
    INSERT_ADMIN_QUIZ_QUESTION,
)
from app.modules.admin.api_89_admin_quizzes_update.query import (
    CHECK_ADMIN_QUIZ_HISTORY,
    DELETE_ADMIN_QUIZ_CHOICES,
    DELETE_ADMIN_QUIZ_QUESTIONS,
    LOCK_ADMIN_QUIZ,
    LOCK_ADMIN_QUIZ_CHOICES,
    LOCK_ADMIN_QUIZ_COURSE,
    LOCK_ADMIN_QUIZ_QUESTIONS,
    UPDATE_ADMIN_QUIZ,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

_DEFAULT = object()


class FakeSession:
    """Session giả ghi nhận commit/rollback của transaction API #89."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        """Khởi tạo bộ đếm transaction và cấu hình lỗi commit tùy chọn."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Đếm commit và phát sinh lỗi giả nếu test yêu cầu."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("private commit detail")

    def rollback(self) -> None:
        """Đếm rollback của transaction cần hủy."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả session giả cho TestClient."""

    def dependency():
        """Yield session giả trong request hiện tại."""

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


def request_body(
    *,
    config: dict[str, Any] | None = None,
    questions: list[dict[str, Any]] | None = None,
) -> dict[str, str]:
    """Tạo outer body gồm config/questions JSON string theo proposal tái sử dụng #88."""

    selected_config = config if config is not None else {
        "course_id": 9001,
        "title": "Quiz đã cập nhật",
        "duration_minutes": 45,
        "passing_score": "75.00",
    }
    selected_questions = questions if questions is not None else [
        {
            "text": "Câu hỏi mới?",
            "type": "SINGLE_CHOICE",
            "choices": [
                {"text": "Phương án A", "is_correct": True},
                {"text": "Phương án B", "is_correct": False},
            ],
        }
    ]
    return {
        "config": json.dumps(selected_config, ensure_ascii=False),
        "questions": json.dumps(selected_questions, ensure_ascii=False),
    }


def put_quiz(
    client: TestClient,
    *,
    quiz_id: str = "5101",
    body: Any = _DEFAULT,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi PUT API #89 với raw body/path/header có thể tùy chỉnh."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    if body is _DEFAULT:
        body = request_body()
    if isinstance(body, bytes):
        return client.put(f"/api/v1/admin/quizzes/{quiz_id}", headers=headers, content=body)
    return client.put(f"/api/v1/admin/quizzes/{quiz_id}", headers=headers, json=body)


def install_update_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    missing_quiz: bool = False,
    missing_course: bool = False,
    history: str | None = None,
    failing_query: str | None = None,
    bad_projection: str | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài DB doubles cho lock/check/update/delete/insert và lưu tham số bound."""

    captured: list[tuple[str, dict[str, Any]]] = []
    next_question_id = 6101
    next_choice_id = 7101

    def query_one(_db, query, params):
        """Trả projection giả theo SQL constant đang được view thực thi."""

        nonlocal next_question_id, next_choice_id
        captured.append((query, dict(params)))
        if query == failing_query:
            raise SQLAlchemyError("private query detail")
        if query == LOCK_ADMIN_QUIZ:
            return None if missing_quiz else {"id": params["quiz_id"], "status": "DRAFT"}
        if query == CHECK_ADMIN_QUIZ_HISTORY:
            return {
                "has_attempts": history == "attempt",
                "has_answers": history == "answer",
            }
        if query == LOCK_ADMIN_QUIZ_COURSE:
            return None if missing_course else {"id": params["course_id"]}
        if query == UPDATE_ADMIN_QUIZ:
            row = {
                "id": params["quiz_id"],
                "course_id": params["course_id"],
                "title": params["title"],
                "duration_minutes": params["duration_minutes"],
                "passing_score": Decimal(params["passing_score"]),
            }
            if bad_projection == "quiz":
                row["course_id"] = None
            return row
        if query == INSERT_ADMIN_QUIZ_QUESTION:
            row = {
                "id": next_question_id,
                "quiz_id": params["quiz_id"],
                "text": params["text"],
                "type": params["question_type"],
                "sort_order": params["sort_order"],
            }
            next_question_id += 1
            if bad_projection == "question":
                row["type"] = "UNKNOWN"
            return row
        if query == INSERT_ADMIN_QUIZ_CHOICE:
            row = {
                "id": next_choice_id,
                "question_id": params["question_id"],
                "text": params["text"],
                "is_correct": params["is_correct"],
                "sort_order": params["sort_order"],
            }
            next_choice_id += 1
            if bad_projection == "choice":
                row["is_correct"] = "false"
            return row
        raise AssertionError("unexpected SQL query")

    def query_many(_db, query, params):
        """Trả child IDs cho lock/delete và cho phép giả lập lỗi query/mapping."""

        captured.append((query, dict(params)))
        if query == failing_query:
            raise SQLAlchemyError("private query detail")
        if query == LOCK_ADMIN_QUIZ_QUESTIONS:
            return [{"id": 5102}, {"id": 5103}]
        if query == LOCK_ADMIN_QUIZ_CHOICES:
            return [{"id": 7102}, {"id": 7103}]
        if query == DELETE_ADMIN_QUIZ_CHOICES:
            rows = [{"id": 7102}, {"id": 7103}]
            return rows[:1] if bad_projection == "choice_delete" else rows
        if query == DELETE_ADMIN_QUIZ_QUESTIONS:
            rows = [{"id": 5102}, {"id": 5103}]
            return rows[:1] if bad_projection == "question_delete" else rows
        raise AssertionError("unexpected SQL query")

    monkeypatch.setattr(quizzes_view, "query_one", query_one)
    monkeypatch.setattr(quizzes_view, "query_many", query_many)
    return captured


def test_update_admin_quiz_replaces_parent_and_children_in_order(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Thay metadata và child set theo đúng chuỗi lock, delete rồi insert."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_update_queries(monkeypatch)

    response = put_quiz(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["data"] == {
        "id": 5101,
        "course_id": 9001,
        "title": "Quiz đã cập nhật",
        "duration_minutes": 45,
        "passing_score": "75.00",
        "questions": [
            {
                "id": 6101,
                "text": "Câu hỏi mới?",
                "type": "SINGLE_CHOICE",
                "choices": [
                    {"id": 7101, "text": "Phương án A", "is_correct": True},
                    {"id": 7102, "text": "Phương án B", "is_correct": False},
                ],
            }
        ],
    }
    queries = [query for query, _ in captured]
    assert queries == [
        LOCK_ADMIN_QUIZ,
        LOCK_ADMIN_QUIZ_QUESTIONS,
        LOCK_ADMIN_QUIZ_CHOICES,
        CHECK_ADMIN_QUIZ_HISTORY,
        LOCK_ADMIN_QUIZ_COURSE,
        UPDATE_ADMIN_QUIZ,
        DELETE_ADMIN_QUIZ_CHOICES,
        DELETE_ADMIN_QUIZ_QUESTIONS,
        INSERT_ADMIN_QUIZ_QUESTION,
        INSERT_ADMIN_QUIZ_CHOICE,
        INSERT_ADMIN_QUIZ_CHOICE,
    ]
    assert captured[5][1] == {
        "quiz_id": 5101,
        "course_id": 9001,
        "title": "Quiz đã cập nhật",
        "passing_score": "75.00",
        "duration_minutes": 45,
    }
    choice_orders = [
        params["sort_order"]
        for query, params in captured
        if query == INSERT_ADMIN_QUIZ_CHOICE
    ]
    assert choice_orders == [0, 1]
    assert "SET status =" not in captured[5][0]
    assert "description =" not in captured[5][0]
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_update_admin_quiz_empty_questions_deletes_old_set_and_omits_null_duration(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cho phép question set rỗng và ánh xạ duration null thành omit theo #88."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_update_queries(monkeypatch)
    body = request_body(
        config={"course_id": 9001, "title": "Quiz không thời lượng", "passing_score": "0"},
        questions=[],
    )

    response = put_quiz(client, body=body)

    assert response.status_code == 200
    assert "duration_minutes" not in response.json()["data"]
    assert response.json()["data"]["questions"] == []
    assert captured[5][1]["duration_minutes"] is None
    assert captured[-1][0] == DELETE_ADMIN_QUIZ_QUESTIONS
    insert_queries = {INSERT_ADMIN_QUIZ_QUESTION, INSERT_ADMIN_QUIZ_CHOICE}
    assert not any(query in insert_queries for query, _ in captured)
    assert session.commit_count == 1


def test_update_admin_quiz_authenticates_before_path_body_or_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """401/403 được trả trước path/body parsing và mọi truy vấn."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    def fail_query(*_args, **_kwargs):
        """Fail nếu request không hợp lệ vẫn gọi DB."""

        raise AssertionError("database must not be queried")

    monkeypatch.setattr(quizzes_view, "query_one", fail_query)
    monkeypatch.setattr(quizzes_view, "query_many", fail_query)
    unauthenticated = put_quiz(client, quiz_id="bad", body=b"{", authorization=None)
    assert unauthenticated.status_code == 401
    assert unauthenticated.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert unauthenticated.json()["data"] is None

    allow_admin_token(monkeypatch, roles=["STUDENT"])
    wrong_role = put_quiz(client, quiz_id="bad", body=b"{")
    assert wrong_role.status_code == 403
    assert wrong_role.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert wrong_role.json()["data"] is None
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize("quiz_id", ["0", "-1", "9223372036854775808", "not-an-id"])
def test_update_admin_quiz_rejects_invalid_path_before_parsing_body_or_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    quiz_id: str,
) -> None:
    """ID path sai trả catalog 422 trước body parse hoặc truy vấn."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Fail nếu path sai vẫn truy cập database."""

        raise AssertionError("database must not be queried")

    monkeypatch.setattr(quizzes_view, "query_one", fail_query)
    monkeypatch.setattr(quizzes_view, "query_many", fail_query)
    response = put_quiz(client, quiz_id=quiz_id, body=b"{")

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "quiz_id"
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    "body",
    [b"{", {"config": {}, "questions": "[]"}, {"config": "{", "questions": "[]"}],
)
def test_update_admin_quiz_rejects_invalid_body_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: Any,
) -> None:
    """Body ngoài sai kiểu hoặc embedded JSON lỗi trả 422 trước query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Fail nếu request body sai vẫn gọi DB."""

        raise AssertionError("database must not be queried")

    monkeypatch.setattr(quizzes_view, "query_one", fail_query)
    monkeypatch.setattr(quizzes_view, "query_many", fail_query)
    response = put_quiz(client, body=body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_update_admin_quiz_returns_404_for_missing_or_deleted_quiz(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Quiz không tìm thấy theo active lock query trả catalog 404."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_update_queries(monkeypatch, missing_quiz=True)

    response = put_quiz(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert [query for query, _ in captured] == [LOCK_ADMIN_QUIZ]
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize("history", ["attempt", "answer"])
def test_update_admin_quiz_rejects_any_attempt_or_answer_history(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    history: str,
) -> None:
    """History hiện có chặn cả parent và child mutation trước mọi write."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_update_queries(monkeypatch, history=history)

    response = put_quiz(client)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "quiz_id"
    assert [query for query, _ in captured] == [
        LOCK_ADMIN_QUIZ,
        LOCK_ADMIN_QUIZ_QUESTIONS,
        LOCK_ADMIN_QUIZ_CHOICES,
        CHECK_ADMIN_QUIZ_HISTORY,
    ]
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_update_admin_quiz_returns_422_for_missing_target_course(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Course đích thiếu trả catalog 422 trước khi update hoặc delete."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_update_queries(monkeypatch, missing_course=True)

    response = put_quiz(client)

    assert response.status_code == 422
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "config.course_id"
    assert [query for query, _ in captured][-1] == LOCK_ADMIN_QUIZ_COURSE
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    ("failing_query", "bad_projection"),
    [
        (LOCK_ADMIN_QUIZ_QUESTIONS, None),
        (CHECK_ADMIN_QUIZ_HISTORY, None),
        (UPDATE_ADMIN_QUIZ, None),
        (DELETE_ADMIN_QUIZ_CHOICES, None),
        (INSERT_ADMIN_QUIZ_CHOICE, None),
        (None, "quiz"),
        (None, "question"),
        (None, "choice"),
        (None, "choice_delete"),
        (None, "question_delete"),
    ],
)
def test_update_admin_quiz_rolls_back_query_or_projection_failures(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failing_query: str | None,
    bad_projection: str | None,
) -> None:
    """Query, delete hoặc mapping failure trả safe 500 và rollback toàn bộ."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_update_queries(
        monkeypatch,
        failing_query=failing_query,
        bad_projection=bad_projection,
    )

    response = put_quiz(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "private" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_update_admin_quiz_rolls_back_when_commit_fails(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Commit failure trả safe 500 và rollback transaction đang mở."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_update_queries(monkeypatch)

    response = put_quiz(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_update_admin_quiz_openapi_documents_derived_body_path_and_catalog_errors(
    client: TestClient,
) -> None:
    """OpenAPI mô tả body proposal, int64 path, HTTP 200 và lỗi catalog."""

    operation = client.app.openapi()["paths"]["/api/v1/admin/quizzes/{quiz_id}"]["put"]
    parameters = {parameter["name"]: parameter for parameter in operation["parameters"]}
    assert parameters["quiz_id"]["schema"] == {"type": "integer", "format": "int64"}
    assert parameters["Authorization"]["in"] == "header"
    body_schema = operation["requestBody"]["content"]["application/json"]["schema"]
    assert body_schema["required"] == ["config", "questions"]
    assert body_schema["properties"]["config"]["type"] == "string"
    assert body_schema["properties"]["questions"]["type"] == "string"
    assert {"200", "401", "403", "404", "422", "500"} <= set(operation["responses"])
