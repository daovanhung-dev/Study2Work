from __future__ import annotations

from datetime import datetime
from typing import Any

import app.modules.mentor.api_67_mentor_student_progress.view as progress_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả lập transaction cho các test HTTP API #67."""

    def __init__(self) -> None:
        """Khởi tạo bộ đếm commit và rollback."""

        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận commit ngoài dự kiến nếu handler gọi."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Ghi nhận rollback khi handler dọn transaction lỗi."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả fake session cho TestClient."""

    def dependency():
        """Yield session giả lập cho request."""

        yield session

    return dependency


def allow_mentor_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Thay decoder để tạo JWT Mentor có subject ổn định trong test."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": roles or ["MENTOR"]},
    )


def course_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection course legacy do Mentor kiểm thử sở hữu."""

    return {"id": 101, "mentor_id": 1001, **overrides}


def student_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection identity tối thiểu của Student đang active."""

    return {
        "id": 2001,
        "full_name": "Nguyễn An",
        "avatar_url": "https://cdn.example.test/avatar/2001.png",
        **overrides,
    }


def lesson_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection progress hợp lệ của một published lesson."""

    return {
        "lesson_id": 9001,
        "title": "Introduction",
        "order": 1,
        "progress_status": "COMPLETED",
        "progress_percent": 100,
        "last_accessed_at": datetime(2026, 10, 24, 9, 0),
        "completed_at": datetime(2026, 10, 24, 9, 20),
        **overrides,
    }


def install_query_rows(
    monkeypatch: pytest.MonkeyPatch,
    *,
    course: dict[str, Any] | None = None,
    student: dict[str, Any] | None = None,
    lessons: list[dict[str, Any]] | None = None,
) -> dict[str, list[tuple[str, dict[str, Any]]]]:
    """Cài query doubles và lưu câu SQL/tham số để assertion."""

    captured: dict[str, list[tuple[str, dict[str, Any]]]] = {"one": [], "many": []}

    def query_one(_db, query, params):
        """Trả row theo query constant API #67 và ghi nhận tham số."""

        captured["one"].append((query, params))
        if query == progress_view.FIND_MENTOR_COURSE:
            return course_row() if course is None else course
        if query == progress_view.FIND_ACTIVE_STUDENT:
            return student_row() if student is None else student
        raise AssertionError("unexpected query_one call")

    def query_many(_db, query, params):
        """Trả detail rows và ghi nhận câu SQL API #67."""

        captured["many"].append((query, params))
        if query != progress_view.LIST_STUDENT_LESSON_PROGRESS:
            raise AssertionError("unexpected query_many call")
        return [lesson_row()] if lessons is None else lessons

    monkeypatch.setattr(progress_view, "query_one", query_one)
    monkeypatch.setattr(progress_view, "query_many", query_many)
    return captured


def get_progress_response(
    client: TestClient,
    *,
    course_id: str = "101",
    student_id: str = "2001",
    authorization: str = "Bearer valid-token",
):
    """Gửi HTTP GET API #67 với path và Bearer header kiểm thử."""

    return client.get(
        f"/api/v1/mentor/courses/{course_id}/students/{student_id}/progress",
        headers={"Authorization": authorization},
    )


def test_get_mentor_student_progress_returns_ordered_detail_and_summary(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả detail theo curriculum và summary floor-average giống API #65."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured = install_query_rows(
        monkeypatch,
        lessons=[
            lesson_row(),
            lesson_row(
                lesson_id=9002,
                title="Core concepts",
                order=2,
                progress_status="IN_PROGRESS",
                progress_percent=50,
                completed_at=None,
            ),
            lesson_row(
                lesson_id=9003,
                title="Practice",
                order=3,
                progress_status="NOT_STARTED",
                progress_percent=0,
                last_accessed_at=None,
                completed_at=None,
            ),
        ],
    )

    response = get_progress_response(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["course_id"] == 101
    assert payload["data"]["student"] == {
        "id": 2001,
        "full_name": "Nguyễn An",
        "avatar_url": "https://cdn.example.test/avatar/2001.png",
    }
    assert payload["data"]["summary"] == {
        "completed_lessons": 1,
        "total_lessons": 3,
        "progress_percent": 50,
    }
    assert [item["lesson_id"] for item in payload["data"]["lessons"]] == [9001, 9002, 9003]
    assert payload["data"]["lessons"][2]["progress_status"] == "NOT_STARTED"
    assert payload["data"]["lessons"][2]["last_accessed_at"] is None
    assert "e.status = 'ACTIVE'" in captured["one"][1][0]
    assert "u.role = 'STUDENT'" in captured["one"][1][0]
    assert "c.mentor_id = :mentor_id" in captured["many"][0][0]
    assert "l.status = 'PUBLISHED'" in captured["many"][0][0]
    assert "ORDER BY pl.lesson_order ASC, pl.id ASC" in captured["many"][0][0]
    assert "DISTINCT ON (lp.user_id, lp.lesson_id)" in captured["many"][0][0]
    assert "lp.last_accessed_at DESC NULLS LAST" in captured["many"][0][0]
    assert captured["one"][1][1] == {
        "course_id": 101,
        "mentor_id": 1001,
        "student_id": 2001,
    }
    assert captured["many"][0][1] == {
        "course_id": 101,
        "mentor_id": 1001,
        "student_id": 2001,
    }
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_mentor_student_progress_keeps_nulls_and_defaults_absent_progress(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Biểu diễn lesson không có progress row bằng NOT_STARTED/0 và giữ timestamp null."""

    allow_mentor_token(monkeypatch)
    install_query_rows(
        monkeypatch,
        student=student_row(avatar_url=None),
        lessons=[
            lesson_row(
                progress_status="NOT_STARTED",
                progress_percent=0,
                last_accessed_at=None,
                completed_at=None,
            )
        ],
    )

    response = get_progress_response(client)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["student"]["avatar_url"] is None
    assert data["lessons"][0]["progress_status"] == "NOT_STARTED"
    assert data["lessons"][0]["progress_percent"] == 0
    assert data["lessons"][0]["last_accessed_at"] is None
    assert data["lessons"][0]["completed_at"] is None
    assert data["summary"] == {
        "completed_lessons": 0,
        "total_lessons": 1,
        "progress_percent": 0,
    }


def test_get_mentor_student_progress_returns_zero_summary_for_empty_curriculum(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả summary zero khi course không có published lesson."""

    allow_mentor_token(monkeypatch)
    install_query_rows(monkeypatch, lessons=[])

    response = get_progress_response(client)

    assert response.status_code == 200
    assert response.json()["data"]["summary"] == {
        "completed_lessons": 0,
        "total_lessons": 0,
        "progress_percent": 0,
    }
    assert response.json()["data"]["lessons"] == []


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_get_mentor_student_progress_rejects_bad_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Từ chối Bearer thiếu hoặc sai format trước mọi truy vấn database."""

    monkeypatch.setattr(
        progress_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )
    monkeypatch.setattr(
        progress_view,
        "query_many",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )
    header = "" if authorization is None else authorization

    response = get_progress_response(client, authorization=header)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert response.json()["data"] is None


def test_get_mentor_student_progress_rejects_non_mentor_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối principal không có role Mentor trước truy vấn database."""

    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    monkeypatch.setattr(
        progress_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = get_progress_response(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


@pytest.mark.parametrize(
    ("course_id", "student_id"),
    [
        ("invalid", "2001"),
        ("101", "9223372036854775808"),
        ("-9223372036854775809", "2001"),
    ],
)
def test_get_mentor_student_progress_maps_invalid_int64_to_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    course_id: str,
    student_id: str,
) -> None:
    """Ánh xạ path không phải signed-int64 thành catalog 404."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        progress_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("invalid IDs must not query")
        ),
    )

    response = get_progress_response(client, course_id=course_id, student_id=student_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_mentor_student_progress_returns_not_found_for_missing_course(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 404 khi course không tồn tại và không truy vấn learner."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: list[str] = []

    def find_course(_db, query, _params):
        """Ghi nhận owner lookup rồi trả course vắng mặt."""

        captured.append(query)
        return None

    monkeypatch.setattr(progress_view, "query_one", find_course)
    monkeypatch.setattr(
        progress_view,
        "query_many",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("lessons must not query")),
    )

    response = get_progress_response(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert len(captured) == 1
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_mentor_student_progress_forbids_another_course_owner(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối course của Mentor khác trước khi truy vấn learner hoặc lesson."""

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
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("lessons must not query")),
    )

    response = get_progress_response(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.rollback_count == 1


def test_get_mentor_student_progress_returns_not_found_for_ineligible_student(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không trả dữ liệu khi Student không nằm trong roster ACTIVE của course."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: list[str] = []

    def missing_student(_db, query, params):
        """Trả course owner nhưng không tìm thấy Student đủ điều kiện."""

        captured.append(query)
        if query == progress_view.FIND_MENTOR_COURSE:
            return course_row()
        if query == progress_view.FIND_ACTIVE_STUDENT:
            return None
        raise AssertionError("unexpected query_one call")

    monkeypatch.setattr(progress_view, "query_one", missing_student)
    monkeypatch.setattr(
        progress_view,
        "query_many",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("lessons must not query")),
    )

    response = get_progress_response(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert captured == [progress_view.FIND_MENTOR_COURSE, progress_view.FIND_ACTIVE_STUDENT]
    assert session.rollback_count == 1


@pytest.mark.parametrize("failure_stage", ["course", "student", "lessons"])
def test_get_mentor_student_progress_returns_safe_500_on_query_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failure_stage: str,
) -> None:
    """Map lỗi SQLAlchemy ở từng bước thành safe 500 và rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)

    def query_one(_db, query, _params):
        """Phát sinh lỗi tại owner hoặc roster lookup được chọn."""

        if failure_stage == "course" and query == progress_view.FIND_MENTOR_COURSE:
            raise SQLAlchemyError("private database detail")
        if failure_stage == "student" and query == progress_view.FIND_ACTIVE_STUDENT:
            raise SQLAlchemyError("private database detail")
        if query == progress_view.FIND_MENTOR_COURSE:
            return course_row()
        return student_row()

    def query_many(*_args, **_kwargs):
        """Phát sinh lỗi ở bước đọc lesson hoặc trả fixture hợp lệ."""

        if failure_stage == "lessons":
            raise SQLAlchemyError("private database detail")
        return [lesson_row()]

    monkeypatch.setattr(progress_view, "query_one", query_one)
    monkeypatch.setattr(progress_view, "query_many", query_many)

    response = get_progress_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "private database detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    "lesson_overrides",
    [
        {"lesson_id": 0},
        {"progress_status": "PAUSED"},
        {"progress_percent": 101},
        {"order": "first"},
        {"last_accessed_at": "not-a-timestamp"},
    ],
)
def test_get_mentor_student_progress_rejects_invalid_lesson_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    lesson_overrides: dict[str, Any],
) -> None:
    """Từ chối lesson projection sai kiểu, status hoặc range bằng safe 500."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_query_rows(monkeypatch, lessons=[lesson_row(**lesson_overrides)])

    response = get_progress_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_get_mentor_student_progress_rejects_duplicate_lesson_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối cùng lesson xuất hiện nhiều lần trong projection đã resolve."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_query_rows(monkeypatch, lessons=[lesson_row(), lesson_row()])

    response = get_progress_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_get_mentor_student_progress_rejects_mismatched_student_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối identity projection không khớp Student ID trong path."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_query_rows(monkeypatch, student=student_row(id=2002))

    response = get_progress_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_get_mentor_student_progress_openapi_declares_path_types_and_error_set(
    client: TestClient,
) -> None:
    """Kiểm tra OpenAPI path int64, singular response và direct error status."""

    schema = client.app.openapi()
    operation = schema["paths"][
        "/api/v1/mentor/courses/{course_id}/students/{student_id}/progress"
    ]["get"]
    parameters = {parameter["name"]: parameter for parameter in operation["parameters"]}
    envelope = schema["components"]["schemas"]["GetMentorStudentProgressEnvelope"]

    assert parameters["course_id"]["schema"]["format"] == "int64"
    assert parameters["course_id"]["required"] is True
    assert parameters["student_id"]["schema"]["format"] == "int64"
    assert parameters["student_id"]["required"] is True
    assert parameters["Authorization"]["in"] == "header"
    assert envelope["properties"]["data"]["$ref"].endswith("/StudentCourseProgress")
    assert set(operation["responses"]) == {"200", "401", "403", "404", "500"}


def test_get_mentor_student_progress_propagates_trace_id(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Truyền trace ID từ request sang response body và header."""

    allow_mentor_token(monkeypatch)
    install_query_rows(monkeypatch)
    trace_id = "50a45a59-7c6f-42aa-8f02-a42b3f1cf185"

    response = client.get(
        "/api/v1/mentor/courses/101/students/2001/progress",
        headers={"Authorization": "Bearer valid-token", "X-Trace-Id": trace_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Trace-Id"] == trace_id
    assert response.json()["traceId"] == trace_id
