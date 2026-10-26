from __future__ import annotations

from datetime import datetime
from typing import Any

import app.modules.mentor.api_66_mentor_course_analytics.view as analytics_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả lập bộ đếm transaction cho các test HTTP."""

    def __init__(self) -> None:
        """Theo dõi commit và rollback để xác nhận API chỉ đọc."""

        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận nếu handler commit ngoài dự kiến."""

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
    """Thay decoder để tạo JWT Mentor với subject số ổn định."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": roles or ["MENTOR"]},
    )


def course_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection course legacy do Mentor kiểm thử sở hữu."""

    return {"id": 101, "mentor_id": 1001, **overrides}


def analytics_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection aggregate activity hợp lệ của API #66."""

    return {
        "tracked_lesson_accesses": 3,
        "students_with_activity": 2,
        "last_activity_at": datetime(2026, 10, 25, 9, 30),
        **overrides,
    }


def get_analytics_response(client: TestClient, course_id: str = "101"):
    """Gửi HTTP GET API #66 với Bearer token kiểm thử."""

    return client.get(
        f"/api/v1/mentor/courses/{course_id}/analytics",
        headers={"Authorization": "Bearer valid-token"},
    )


def test_get_mentor_course_analytics_returns_activity_summary(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả activity proxy và xác nhận source predicates cùng hành vi chỉ đọc."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: dict[str, Any] = {}

    def query_course(_db, query, params):
        """Ghi nhận owner query rồi trả course fixture."""

        captured.setdefault("queries", []).append(query)
        if len(captured["queries"]) == 1:
            assert params == {"course_id": 101}
            return course_row()
        assert params == {"course_id": 101, "mentor_id": 1001}
        return analytics_row()

    monkeypatch.setattr(analytics_view, "query_one", query_course)

    response = get_analytics_response(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"] == {
        "tracked_lesson_accesses": 3,
        "students_with_activity": 2,
        "last_activity_at": "2026-10-25T09:30:00",
    }
    aggregate_sql = captured["queries"][1]
    assert "c.mentor_id = :mentor_id" in aggregate_sql
    assert "l.status = 'PUBLISHED'" in aggregate_sql
    assert "u.role = 'STUDENT'" in aggregate_sql
    assert "lp.last_accessed_at IS NOT NULL" in aggregate_sql
    assert "GROUP BY lp.user_id, lp.lesson_id" in aggregate_sql
    assert "MAX(lp.last_accessed_at)" in aggregate_sql
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_mentor_course_analytics_returns_zero_for_empty_activity(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả count zero và timestamp null khi course chưa có dấu truy cập."""

    allow_mentor_token(monkeypatch)
    rows = iter([course_row(), analytics_row(
        tracked_lesson_accesses=0,
        students_with_activity=0,
        last_activity_at=None,
    )])
    monkeypatch.setattr(analytics_view, "query_one", lambda *_args, **_kwargs: next(rows))

    response = get_analytics_response(client)

    assert response.status_code == 200
    assert response.json()["data"] == {
        "tracked_lesson_accesses": 0,
        "students_with_activity": 0,
        "last_activity_at": None,
    }


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_get_mentor_course_analytics_rejects_bad_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Từ chối Bearer thiếu hoặc sai format trước mọi truy vấn database."""

    monkeypatch.setattr(
        analytics_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )
    headers = {} if authorization is None else {"Authorization": authorization}

    response = client.get("/api/v1/mentor/courses/101/analytics", headers=headers)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert response.json()["data"] is None


def test_get_mentor_course_analytics_rejects_non_mentor_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối principal không có Mentor role trước database."""

    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    monkeypatch.setattr(
        analytics_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = get_analytics_response(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


@pytest.mark.parametrize("course_id", ["abc", "9223372036854775808", "-9223372036854775809"])
def test_get_mentor_course_analytics_maps_bad_int64_to_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    course_id: str,
) -> None:
    """Ánh xạ path không biểu diễn được signed-int64 sang catalog 404."""

    allow_mentor_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Bảo đảm path lỗi không truy cập database."""

        raise AssertionError("invalid ID must not query")

    monkeypatch.setattr(
        analytics_view,
        "query_one",
        fail_query,
    )

    response = get_analytics_response(client, course_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_mentor_course_analytics_returns_not_found_for_missing_course(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 404 khi course không tồn tại và không chạy aggregate."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(analytics_view, "query_one", lambda *_args, **_kwargs: None)

    response = get_analytics_response(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_mentor_course_analytics_forbids_another_owner_before_aggregate(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối course do Mentor khác sở hữu trước khi đọc analytics."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        analytics_view,
        "query_one",
        lambda *_args, **_kwargs: course_row(mentor_id=2002),
    )

    response = get_analytics_response(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.rollback_count == 1


def test_get_mentor_course_analytics_returns_safe_500_on_query_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map lỗi aggregate thành safe 500 và rollback transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    calls = 0

    def fail_aggregate(_db, _query, _params):
        """Trả course ở lần đầu rồi phát SQLAlchemyError ở aggregate."""

        nonlocal calls
        calls += 1
        if calls == 1:
            return course_row()
        raise SQLAlchemyError("private database detail")

    monkeypatch.setattr(analytics_view, "query_one", fail_aggregate)

    response = get_analytics_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private database detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    "row",
    [
        analytics_row(tracked_lesson_accesses=-1),
        analytics_row(students_with_activity=4),
        analytics_row(tracked_lesson_accesses=2**63),
        analytics_row(last_activity_at="not-a-datetime"),
    ],
)
def test_get_mentor_course_analytics_rejects_invalid_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    row: dict[str, Any],
) -> None:
    """Từ chối aggregate projection âm, bất khả thi hoặc sai kiểu."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    rows = iter([course_row(), row])
    monkeypatch.setattr(analytics_view, "query_one", lambda *_args, **_kwargs: next(rows))

    response = get_analytics_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_get_mentor_course_analytics_openapi_declares_int64_and_exact_errors(
    client: TestClient,
) -> None:
    """Kiểm tra OpenAPI path/header, summary response và exact error status set."""

    schema = client.app.openapi()
    operation = schema["paths"]["/api/v1/mentor/courses/{course_id}/analytics"]["get"]
    parameters = {parameter["name"]: parameter for parameter in operation["parameters"]}
    envelope = schema["components"]["schemas"]["GetMentorCourseAnalyticsEnvelope"]

    assert parameters["course_id"]["schema"]["format"] == "int64"
    assert parameters["course_id"]["required"] is True
    assert parameters["Authorization"]["in"] == "header"
    assert envelope["properties"]["data"]["$ref"].endswith("/MentorCourseActivityAnalytics")
    assert set(operation["responses"]) == {"200", "401", "403", "404", "500"}


def test_get_mentor_course_analytics_propagates_trace_id(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Truyền trace ID vào envelope và response header."""

    allow_mentor_token(monkeypatch)
    rows = iter([course_row(), analytics_row()])
    monkeypatch.setattr(analytics_view, "query_one", lambda *_args, **_kwargs: next(rows))
    trace_id = "50a45a59-7c6f-42aa-8f02-a42b3f1cf185"

    response = client.get(
        "/api/v1/mentor/courses/101/analytics",
        headers={"Authorization": "Bearer valid-token", "X-Trace-Id": trace_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Trace-Id"] == trace_id
    assert response.json()["traceId"] == trace_id
