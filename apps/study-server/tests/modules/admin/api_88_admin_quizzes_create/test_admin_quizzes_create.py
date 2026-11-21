from __future__ import annotations

import json
from decimal import Decimal
from typing import Any

import app.modules.admin.api_88_admin_quizzes_create.view as quizzes_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_88_admin_quizzes_create.query import (
    INSERT_ADMIN_QUIZ,
    INSERT_ADMIN_QUIZ_CHOICE,
    INSERT_ADMIN_QUIZ_QUESTION,
    SELECT_ADMIN_QUIZ_COURSE,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

_DEFAULT = object()


class FakeSession:
    """Session giả để xác minh transaction create Quiz."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Đếm commit hoặc phát sinh lỗi commit theo cấu hình test."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("private commit detail")

    def rollback(self) -> None:
        """Đếm rollback của transaction cần hủy."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả FakeSession cho TestClient."""

    def dependency():
        """Yield session giả trong một HTTP request."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cấp JWT giả có subject số và role tùy chọn cho request test."""

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
    """Tạo outer body với hai member giữ đúng JSON string types theo catalog."""

    selected_config = config if config is not None else {
        "course_id": 9001,
        "title": "Quiz minh họa",
        "duration_minutes": 30,
        "passing_score": "70.00",
    }
    selected_questions = questions if questions is not None else [
        {
            "text": "Câu hỏi minh họa?",
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


def post_quiz(
    client: TestClient,
    *,
    body: Any = _DEFAULT,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP POST API #88 với body/header có thể tùy chỉnh."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    if body is _DEFAULT:
        body = request_body()
    if isinstance(body, bytes):
        return client.post("/api/v1/admin/quizzes", headers=headers, content=body)
    return client.post("/api/v1/admin/quizzes", headers=headers, json=body)


def install_create_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    missing_course: bool = False,
    failing_query: str | None = None,
    bad_projection: str | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài DB double cho Q0/M1/M2/M3 và lưu mọi query binding."""

    captured: list[tuple[str, dict[str, Any]]] = []
    next_question_id = 6101
    next_choice_id = 7101

    def query_one(_db, query, params):
        """Trả về row phù hợp với SQL INSERT/SELECT của view."""

        nonlocal next_question_id, next_choice_id
        captured.append((query, dict(params)))
        if query == failing_query:
            raise SQLAlchemyError("private query detail")
        if query == SELECT_ADMIN_QUIZ_COURSE:
            return None if missing_course else {"id": params["course_id"]}
        if query == INSERT_ADMIN_QUIZ:
            row = {
                "id": 5101,
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

    monkeypatch.setattr(quizzes_view, "query_one", query_one)
    return captured


def test_create_admin_quiz_persists_nested_rows_and_returns_quiz(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Tạo Quiz, Question và Choice theo thứ tự rồi trả Quiz đầy đủ."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_create_queries(monkeypatch)

    response = post_quiz(client)

    assert response.status_code == 201
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_CREATED"
    assert payload["data"] == {
        "id": 5101,
        "course_id": 9001,
        "title": "Quiz minh họa",
        "duration_minutes": 30,
        "passing_score": "70.00",
        "questions": [
            {
                "id": 6101,
                "text": "Câu hỏi minh họa?",
                "type": "SINGLE_CHOICE",
                "choices": [
                    {"id": 7101, "text": "Phương án A", "is_correct": True},
                    {"id": 7102, "text": "Phương án B", "is_correct": False},
                ],
            }
        ],
    }
    assert [query for query, _ in captured] == [
        SELECT_ADMIN_QUIZ_COURSE,
        INSERT_ADMIN_QUIZ,
        INSERT_ADMIN_QUIZ_QUESTION,
        INSERT_ADMIN_QUIZ_CHOICE,
        INSERT_ADMIN_QUIZ_CHOICE,
    ]
    assert captured[2][1]["question_type"] == "SINGLE_CHOICE"
    assert captured[2][1]["sort_order"] == 0
    assert captured[3][1]["sort_order"] == 0
    assert captured[4][1]["sort_order"] == 1
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_create_admin_quiz_omits_optional_duration_and_defaults_choice_answer_flag(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Omit duration khi không truyền và dùng false khi choice thiếu is_correct."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_create_queries(monkeypatch)
    body = request_body(
        config={"course_id": 9001, "title": "Không thời lượng", "passing_score": "0"},
        questions=[{"text": "Q?", "type": "TRUE_FALSE", "choices": [{"text": "Có"}]}],
    )

    response = post_quiz(client, body=body)

    assert response.status_code == 201
    assert "duration_minutes" not in response.json()["data"]
    assert response.json()["data"]["questions"][0]["choices"][0]["is_correct"] is False
    assert captured[1][1]["duration_minutes"] is None
    assert captured[-1][1]["is_correct"] is False


def test_create_admin_quiz_authenticates_before_parsing_or_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Unauthenticated and wrong-role calls do not parse invalid body or reach DB."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    def fail_query(*_args, **_kwargs):
        """Fail nếu request không được xác thực vẫn gọi database."""

        raise AssertionError("database must not be queried")

    monkeypatch.setattr(quizzes_view, "query_one", fail_query)
    missing = post_quiz(client, authorization=None, body=b"{")
    assert missing.status_code == 401
    assert missing.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert missing.json()["data"] is None

    allow_admin_token(monkeypatch, roles=["STUDENT"])
    wrong_role = post_quiz(client, body=b"{")
    assert wrong_role.status_code == 403
    assert wrong_role.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert wrong_role.json()["data"] is None
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    ("body", "field"),
    [
        (b"{", "body"),
        ({"config": {}, "questions": "[]"}, "config"),
        ({"config": "{", "questions": "[]"}, "config"),
        ({"config": "{}", "questions": "["}, "questions"),
        (
            request_body(questions=[{"text": "Q", "type": "UNKNOWN", "choices": []}]),
            "embedded.questions.0.type",
        ),
    ],
)
def test_create_admin_quiz_rejects_invalid_body_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: Any,
    field: str,
) -> None:
    """Outer/embedded JSON và QuestionType sai trả 422 trước DB."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Fail nếu validation lỗi vẫn truy cập database."""

        raise AssertionError("database must not be queried")

    monkeypatch.setattr(quizzes_view, "query_one", fail_query)
    response = post_quiz(client, body=body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None
    assert response.json()["meta"]["fieldErrors"][0]["field"] == field
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    ("config", "field"),
    [
        ({"course_id": 2**63, "title": "Q", "passing_score": "1"}, "config.course_id"),
        ({"course_id": 9001, "title": "x" * 201, "passing_score": "1"}, "config.title"),
        ({"course_id": 9001, "title": "Q", "passing_score": "1000"}, "config.passing_score"),
        ({"course_id": 9001, "title": "Q", "passing_score": "1.234"}, "config.passing_score"),
    ],
)
def test_create_admin_quiz_rejects_values_outside_storage_ranges(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    config: dict[str, Any],
    field: str,
) -> None:
    """Physical int64/title/numeric limits map to validation errors before writes."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_create_queries(monkeypatch)

    response = post_quiz(client, body=request_body(config=config))

    assert response.status_code == 422
    assert response.json()["meta"]["fieldErrors"][0]["field"] == field
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_create_admin_quiz_returns_422_when_course_is_missing(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Thiếu course target trả catalog 422 và không tạo Quiz rows."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_create_queries(monkeypatch, missing_course=True)

    response = post_quiz(client)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "config.course_id"
    assert captured == [(SELECT_ADMIN_QUIZ_COURSE, {"course_id": 9001})]
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    ("failing_query", "bad_projection"),
    [
        (SELECT_ADMIN_QUIZ_COURSE, None),
        (INSERT_ADMIN_QUIZ, None),
        (None, "quiz"),
        (None, "question"),
        (None, "choice"),
        (INSERT_ADMIN_QUIZ_CHOICE, None),
    ],
)
def test_create_admin_quiz_rolls_back_query_or_projection_failures(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failing_query: str | None,
    bad_projection: str | None,
) -> None:
    """DB errors and invalid INSERT projections return safe 500 with full rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_create_queries(
        monkeypatch,
        failing_query=failing_query,
        bad_projection=bad_projection,
    )

    response = post_quiz(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "private" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_create_admin_quiz_rolls_back_when_commit_fails(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Lỗi commit trả safe 500 và gọi rollback."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_create_queries(monkeypatch)

    response = post_quiz(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_create_admin_quiz_openapi_documents_direct_outer_body_and_errors(
    client: TestClient,
) -> None:
    """OpenAPI mô tả outer JSON strings, HTTP 201 và catalog error set."""

    operation = client.app.openapi()["paths"]["/api/v1/admin/quizzes"]["post"]

    assert operation["requestBody"]["required"] is True
    schema = operation["requestBody"]["content"]["application/json"]["schema"]
    assert schema["required"] == ["config", "questions"]
    assert schema["properties"]["config"]["type"] == "string"
    assert schema["properties"]["questions"]["type"] == "string"
    assert set(operation["responses"]) >= {"201", "401", "403", "422", "500"}
    assert operation["responses"]["201"]["content"]["application/json"]["schema"]
