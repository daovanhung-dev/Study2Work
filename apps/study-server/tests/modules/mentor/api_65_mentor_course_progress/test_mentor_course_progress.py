from __future__ import annotations

from typing import Any

import app.modules.mentor.api_65_mentor_course_progress.view as progress_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả lập bộ đếm transaction cho các test HTTP."""

    def __init__(self) -> None:
        """Theo dõi commit/rollback để xác nhận route chỉ đọc."""

        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận nếu handler gọi commit ngoài dự kiến."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Ghi nhận rollback khi nhánh lỗi dọn transaction."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả fake session cho TestClient."""

    def dependency():
        """Yield fake session được test cung cấp."""

        yield session

    return dependency


def allow_mentor_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Thay decoder để tạo JWT Mentor với sub số ổn định."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": roles or ["MENTOR"]},
    )


def course_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection course legacy do Mentor kiểm thử sở hữu."""

    return {"id": 101, "mentor_id": 1001, **overrides}


def progress_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection aggregate hợp lệ của một Student."""

    return {
        "student_id": 2001,
        "full_name": "Nguyễn An",
        "avatar_url": "https://cdn.example.test/avatar/2001.png",
        "total_lessons": 3,
        "completed_lessons": 1,
        "progress_sum": 220,
        "invalid_progress_count": 0,
        **overrides,
    }


def get_progress_response(client: TestClient, course_id: str = "101"):
    """Gửi HTTP GET API #65 với Bearer token kiểm thử."""

    return client.get(
        f"/api/v1/mentor/courses/{course_id}/progress",
        headers={"Authorization": "Bearer valid-token"},
    )


def test_get_mentor_course_progress_returns_roster_aggregate(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả đúng roster progress và xác nhận các predicate SQL/read-only."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: dict[str, Any] = {}

    def find_course(_db, query, params):
        """Ghi nhận truy vấn kiểm tra owner và trả course fixture."""

        captured["course_sql"] = query
        assert params == {"course_id": 101}
        return course_row()

    def find_progress(_db, query, params):
        """Ghi nhận aggregate SQL và trả các progress fixture."""

        captured["progress_sql"] = query
        assert params == {"course_id": 101, "mentor_id": 1001}
        return [
            progress_row(),
            progress_row(
                student_id=2002,
                full_name="Trần Bình",
                avatar_url=None,
                completed_lessons=0,
                progress_sum=0,
            ),
        ]

    monkeypatch.setattr(progress_view, "query_one", find_course)
    monkeypatch.setattr(progress_view, "query_many", find_progress)

    response = get_progress_response(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["items"] == [
        {
            "student": {
                "id": 2001,
                "full_name": "Nguyễn An",
                "avatar_url": "https://cdn.example.test/avatar/2001.png",
            },
            "completed_lessons": 1,
            "total_lessons": 3,
            "progress_percent": 73,
        },
        {
            "student": {"id": 2002, "full_name": "Trần Bình"},
            "completed_lessons": 0,
            "total_lessons": 3,
            "progress_percent": 0,
        },
    ]
    assert payload["data"]["pagination"] == {
        "page": 1,
        "size": 2,
        "total": 2,
        "total_pages": 1,
    }
    assert "e.status = 'ACTIVE'" in captured["progress_sql"]
    assert "u.role = 'STUDENT'" in captured["progress_sql"]
    assert "l.status = 'PUBLISHED'" in captured["progress_sql"]
    assert "c.mentor_id = :mentor_id" in captured["progress_sql"]
    assert "DISTINCT ON (lp.user_id, lp.lesson_id)" in captured["progress_sql"]
    assert "lp.last_accessed_at DESC NULLS LAST" in captured["progress_sql"]
    assert "lp.user_id IS NOT NULL" in captured["progress_sql"]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_mentor_course_progress_returns_zero_for_empty_lesson_denominator(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả progress zero khi course không có published lesson."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(progress_view, "query_one", lambda *_args, **_kwargs: course_row())
    monkeypatch.setattr(
        progress_view,
        "query_many",
        lambda *_args, **_kwargs: [
            progress_row(total_lessons=0, completed_lessons=0, progress_sum=0)
        ],
    )

    response = get_progress_response(client)

    assert response.status_code == 200
    assert response.json()["data"]["items"][0]["progress_percent"] == 0
    assert response.json()["data"]["items"][0]["total_lessons"] == 0


def test_get_mentor_course_progress_returns_empty_page_for_empty_roster(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả empty page khi course không có Student đủ điều kiện."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(progress_view, "query_one", lambda *_args, **_kwargs: course_row())
    monkeypatch.setattr(progress_view, "query_many", lambda *_args, **_kwargs: [])

    response = get_progress_response(client)

    assert response.status_code == 200
    assert response.json()["data"] == {
        "items": [],
        "pagination": {"page": 1, "size": 0, "total": 0, "total_pages": 0},
    }
    assert response.json()["message"] == "No students found."


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_get_mentor_course_progress_rejects_bad_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Từ chối Bearer thiếu/sai format trước mọi truy vấn database."""

    monkeypatch.setattr(
        progress_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )
    headers = {} if authorization is None else {"Authorization": authorization}

    response = client.get("/api/v1/mentor/courses/101/progress", headers=headers)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert response.json()["data"] is None


def test_get_mentor_course_progress_rejects_non_mentor_role_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối caller không có Mentor role trước database."""

    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    monkeypatch.setattr(
        progress_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = get_progress_response(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


@pytest.mark.parametrize("course_id", ["abc", "9223372036854775808", "-9223372036854775809"])
def test_get_mentor_course_progress_maps_bad_int64_to_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    course_id: str,
) -> None:
    """Ánh xạ path không phải signed-int64 thành catalog 404."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        progress_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("invalid ID must not query")
        ),
    )

    response = get_progress_response(client, course_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_mentor_course_progress_returns_not_found_for_missing_course(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 404 khi không tìm thấy course và không chạy aggregate."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(progress_view, "query_one", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(
        progress_view,
        "query_many",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("aggregate must not run")),
    )

    response = get_progress_response(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_mentor_course_progress_forbids_another_owner_before_aggregate(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối course của owner khác trước khi đọc roster progress."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        progress_view,
        "query_one",
        lambda *_args, **_kwargs: course_row(mentor_id=2002),
    )
    monkeypatch.setattr(
        progress_view,
        "query_many",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("aggregate must not run")),
    )

    response = get_progress_response(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.rollback_count == 1


def test_get_mentor_course_progress_returns_safe_500_on_query_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map query failure thành safe 500 và rollback transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(progress_view, "query_one", lambda *_args, **_kwargs: course_row())
    monkeypatch.setattr(
        progress_view,
        "query_many",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(SQLAlchemyError("private database detail")),
    )

    response = get_progress_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private database detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    "row",
    [
        progress_row(total_lessons=-1),
        progress_row(completed_lessons=4),
        progress_row(progress_sum=301),
        progress_row(invalid_progress_count=1),
        progress_row(student_id=0),
    ],
)
def test_get_mentor_course_progress_rejects_invalid_aggregate_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    row: dict[str, Any],
) -> None:
    """Từ chối aggregate projection có số liệu hoặc ID bất hợp lệ."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(progress_view, "query_one", lambda *_args, **_kwargs: course_row())
    monkeypatch.setattr(progress_view, "query_many", lambda *_args, **_kwargs: [row])

    response = get_progress_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_get_mentor_course_progress_openapi_declares_int64_page_and_no_422(
    client: TestClient,
) -> None:
    """Kiểm tra OpenAPI int64, response page và đúng error status set."""

    schema = client.app.openapi()
    operation = schema["paths"]["/api/v1/mentor/courses/{course_id}/progress"]["get"]
    parameters = {parameter["name"]: parameter for parameter in operation["parameters"]}
    envelope = schema["components"]["schemas"]["GetMentorCourseProgressEnvelope"]

    assert parameters["course_id"]["schema"]["format"] == "int64"
    assert parameters["course_id"]["required"] is True
    assert parameters["Authorization"]["in"] == "header"
    assert envelope["properties"]["data"]["$ref"].endswith("/MentorStudentProgressPage")
    assert set(operation["responses"]) == {"200", "401", "403", "404", "500"}


def test_get_mentor_course_progress_propagates_trace_id(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Truyền trace ID vào envelope và response header."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(progress_view, "query_one", lambda *_args, **_kwargs: course_row())
    monkeypatch.setattr(progress_view, "query_many", lambda *_args, **_kwargs: [])
    trace_id = "50a45a59-7c6f-42aa-8f02-a42b3f1cf185"

    response = client.get(
        "/api/v1/mentor/courses/101/progress",
        headers={"Authorization": "Bearer valid-token", "X-Trace-Id": trace_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Trace-Id"] == trace_id
    assert response.json()["traceId"] == trace_id
