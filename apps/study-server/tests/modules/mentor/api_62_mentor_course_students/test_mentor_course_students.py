from __future__ import annotations

from typing import Any

import app.modules.mentor.api_62_mentor_course_students.view as students_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    def __init__(self) -> None:
        """Theo dõi transaction read-only của endpoint roster."""
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận commit ngoài dự kiến của endpoint chỉ đọc."""
        self.commit_count += 1

    def rollback(self) -> None:
        """Ghi nhận rollback sau lỗi hoặc nhánh không thành công."""
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo database dependency override cho TestClient."""

    def dependency():
        """Yield fake session của test hiện tại."""
        yield session

    return dependency


def allow_mentor_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Thay JWT decoder bằng numeric subject và role kiểm thử."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": roles or ["MENTOR"]},
    )


def course_row(**overrides: Any) -> dict[str, Any]:
    """Tạo course legacy có Mentor sở hữu trực tiếp."""

    return {"id": 101, "mentor_id": 1001, **overrides}


def student_row(**overrides: Any) -> dict[str, Any]:
    """Tạo UserSummary projection từ users."""

    return {
        "id": 2001,
        "full_name": "Nguyễn An",
        "avatar_url": "https://cdn.example.test/avatar/2001.png",
        **overrides,
    }


def get_students_response(client: TestClient, course_id: str = "101"):
    """Gửi GET API #62 với Bearer token."""

    return client.get(
        f"/api/v1/mentor/courses/{course_id}/students",
        headers={"Authorization": "Bearer valid-token"},
    )


def test_get_mentor_course_students_returns_distinct_summaries(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả roster theo thứ tự ID, bỏ avatar NULL và không ghi transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: dict[str, Any] = {}

    def find_course(_db, query, params):
        captured["course_sql"] = query
        assert params == {"course_id": 101}
        return course_row()

    def find_students(_db, query, params):
        captured["students_sql"] = query
        assert params == {"course_id": 101, "mentor_id": 1001}
        return [
            student_row(id=2001),
            student_row(
                id=2002,
                full_name="Trần Bình",
                avatar_url=None,
            ),
        ]

    monkeypatch.setattr(students_view, "query_one", find_course)
    monkeypatch.setattr(students_view, "query_many", find_students)

    response = get_students_response(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert [student["id"] for student in payload["data"]] == [2001, 2002]
    assert payload["data"][0]["avatar_url"] == "https://cdn.example.test/avatar/2001.png"
    assert "avatar_url" not in payload["data"][1]
    assert "DISTINCT" in captured["students_sql"]
    assert "e.status = 'ACTIVE'" in captured["students_sql"]
    assert "u.role = 'STUDENT'" in captured["students_sql"]
    assert "c.mentor_id = :mentor_id" in captured["students_sql"]
    assert "ORDER BY u.id ASC" in captured["students_sql"]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_mentor_course_students_returns_empty_array(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả collection rỗng khi course hợp lệ chưa có Student đủ điều kiện."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(students_view, "query_one", lambda *_args, **_kwargs: course_row())
    monkeypatch.setattr(students_view, "query_many", lambda *_args, **_kwargs: [])

    response = get_students_response(client)

    assert response.status_code == 200
    assert response.json()["data"] == []
    assert response.json()["message"] == "No students found."
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_get_mentor_course_students_rejects_bad_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Từ chối Bearer thiếu/sai format trước khi truy vấn database."""

    monkeypatch.setattr(
        students_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )
    headers = {} if authorization is None else {"Authorization": authorization}

    response = client.get("/api/v1/mentor/courses/101/students", headers=headers)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert response.json()["data"] is None


def test_get_mentor_course_students_rejects_non_mentor_role(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối Student token trước mọi truy vấn roster."""

    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    monkeypatch.setattr(
        students_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = get_students_response(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


@pytest.mark.parametrize("course_id", ["abc", "9223372036854775808", "-9223372036854775809"])
def test_get_mentor_course_students_maps_invalid_int64_to_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    course_id: str,
) -> None:
    """Giữ catalog error set cho path không phải signed-int64."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        students_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("invalid ID must not query")
        ),
    )

    response = get_students_response(client, course_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_mentor_course_students_returns_not_found_for_missing_course(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 404 khi course không tồn tại và dọn read transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(students_view, "query_one", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(
        students_view,
        "query_many",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("roster query must not run")
        ),
    )

    response = get_students_response(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_mentor_course_students_forbids_another_owner_before_roster_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không đọc roster khi course thuộc Mentor khác."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        students_view,
        "query_one",
        lambda *_args, **_kwargs: course_row(mentor_id=2002),
    )
    monkeypatch.setattr(
        students_view,
        "query_many",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("roster query must not run")
        ),
    )

    response = get_students_response(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.rollback_count == 1


def test_get_mentor_course_students_returns_internal_error_on_course_query_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map database access failure to safe 500 and rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        students_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(SQLAlchemyError("private database detail")),
    )

    response = get_students_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private database detail" not in response.text
    assert session.rollback_count == 1


def test_get_mentor_course_students_returns_internal_error_on_roster_query_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map enrollment query failure to safe 500 and rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(students_view, "query_one", lambda *_args, **_kwargs: course_row())
    monkeypatch.setattr(
        students_view,
        "query_many",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(SQLAlchemyError("private database detail")),
    )

    response = get_students_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private database detail" not in response.text
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    "rows",
    [
        [{"id": 0, "full_name": "Invalid ID", "avatar_url": None}],
        [{"id": 2001, "full_name": None, "avatar_url": None}],
        [student_row(id=2001), student_row(id=2001)],
    ],
)
def test_get_mentor_course_students_rejects_invalid_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    rows: list[dict[str, Any]],
) -> None:
    """Không trả projection user thiếu hoặc duplicate."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(students_view, "query_one", lambda *_args, **_kwargs: course_row())
    monkeypatch.setattr(students_view, "query_many", lambda *_args, **_kwargs: rows)

    response = get_students_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_get_mentor_course_students_openapi_declares_int64_and_array_response(
    client: TestClient,
) -> None:
    """Kiểm tra OpenAPI path format và UserSummary array contract."""

    schema = client.app.openapi()
    operation = schema["paths"]["/api/v1/mentor/courses/{course_id}/students"]["get"]
    course_id_parameter = next(
        parameter for parameter in operation["parameters"] if parameter["name"] == "course_id"
    )
    envelope = schema["components"]["schemas"]["GetMentorCourseStudentsEnvelope"]

    assert course_id_parameter["schema"]["type"] == "integer"
    assert course_id_parameter["schema"]["format"] == "int64"
    assert envelope["properties"]["data"]["type"] == "array"
    assert envelope["properties"]["data"]["items"]["$ref"].endswith(
        "/StudentSummaryResponse"
    )


def test_get_mentor_course_students_propagates_trace_id(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Truyền trace ID vào envelope và response header."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(students_view, "query_one", lambda *_args, **_kwargs: course_row())
    monkeypatch.setattr(students_view, "query_many", lambda *_args, **_kwargs: [])
    trace_id = "50a45a59-7c6f-42aa-8f02-a42b3f1cf185"

    response = client.get(
        "/api/v1/mentor/courses/101/students",
        headers={
            "Authorization": "Bearer valid-token",
            "X-Trace-Id": trace_id,
        },
    )

    assert response.status_code == 200
    assert response.headers["X-Trace-Id"] == trace_id
    assert response.json()["traceId"] == trace_id
