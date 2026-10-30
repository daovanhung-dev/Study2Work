from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

import app.modules.mentor.api_56_mentor_submissions_grade.view as grade_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.mentor.api_56_mentor_submissions_grade.query import (
    FIND_GRADED_SUBMISSION_UPLOAD,
    LOCK_MENTOR_SUBMISSION_FOR_GRADE,
    UPDATE_MENTOR_SUBMISSION_GRADE,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

_DEFAULT = object()


class FakeSession:
    """Theo dõi commit/rollback của transaction API #56."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        """Khởi tạo bộ đếm transaction và tùy chọn mô phỏng lỗi commit."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát sinh lỗi SQLAlchemy đã cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("private commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback của view khi request không thể hoàn tất."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override cung cấp FakeSession cho TestClient."""

    def dependency():
        """Yield session giả lập trong vòng đời một HTTP request."""

        yield session

    return dependency


def allow_mentor_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Thay decoder JWT bằng numeric subject và role Mentor mặc định."""

    def decode_token(_token: str) -> dict[str, Any]:
        """Trả claims giả lập theo role đã chọn trong test."""

        return {"sub": "1001", "roles": roles or ["MENTOR"]}

    monkeypatch.setattr(auth_utils, "decode_access_token", decode_token)


def candidate_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection hợp lệ của Submission và quan hệ Assignment/Course."""

    return {
        "id": 56001,
        "assignment_id": 1250,
        "user_id": 804,
        "content": "Bài làm cần được chấm.",
        "file_url": "https://storage.example/answer.pdf",
        "submitted_at": datetime(2026, 10, 25, 9, 30),
        "score": None,
        "feedback": "Feedback cũ được API #57 sở hữu.",
        "status": "SUBMITTED",
        "matched_assignment_id": 1250,
        "course_id": 101,
        "max_score": Decimal("10.00"),
        "matched_course_id": 101,
        "mentor_id": 1001,
        **overrides,
    }


def graded_row(**overrides: Any) -> dict[str, Any]:
    """Tạo UPDATE RETURNING projection với grade mới và feedback giữ nguyên."""

    row = candidate_row()
    row.update({"score": Decimal("8.00"), "status": "GRADED"})
    row.update(overrides)
    return row


def upload_row(**overrides: Any) -> dict[str, Any]:
    """Tạo metadata UploadAsset đầy đủ để kiểm tra response files."""

    return {
        "id": 34001,
        "name": "answer.pdf",
        "url": "https://storage.example/answer.pdf",
        "content_type": "application/pdf",
        "size_bytes": 12345,
        "status": "UPLOADED",
        **overrides,
    }


def grade_body(**overrides: Any) -> dict[str, Any]:
    """Tạo body API #56 theo fallback snake_case đã ghi trong worklog."""

    return {"score": 8, "rubric_items": "[]", **overrides}


def post_grade(
    client: TestClient,
    *,
    submission_id: str = "56001",
    body: dict[str, Any] | None = None,
    authorization: str | None = "Bearer valid-token",
    trace_id: str | None = None,
):
    """Gửi POST API #56 bằng Bearer token và body tùy chọn."""

    headers = {} if authorization is None else {"Authorization": authorization}
    if trace_id is not None:
        headers["X-Trace-Id"] = trace_id
    return client.post(
        f"/api/v1/mentor/submissions/{submission_id}/grade",
        json=grade_body() if body is None else body,
        headers=headers,
    )


def install_query_flow(
    monkeypatch: pytest.MonkeyPatch,
    *,
    current: Any = _DEFAULT,
    updated: Any = _DEFAULT,
    asset: Any = _DEFAULT,
    fail_at: str | None = None,
    captured: list[tuple[str, dict[str, Any]]] | None = None,
) -> None:
    """Cài query fake theo giai đoạn lock, update và asset lookup."""

    def query_one(_db, query: str, params: dict[str, Any]):
        """Ghi nhận SQL và trả projection tương ứng với từng giai đoạn."""

        if captured is not None:
            captured.append((query, params))
        if query == LOCK_MENTOR_SUBMISSION_FOR_GRADE:
            if fail_at == "lock":
                raise SQLAlchemyError("private lock detail")
            return candidate_row() if current is _DEFAULT else current
        if query == UPDATE_MENTOR_SUBMISSION_GRADE:
            if fail_at == "update":
                raise SQLAlchemyError("private update detail")
            return graded_row() if updated is _DEFAULT else updated
        if query == FIND_GRADED_SUBMISSION_UPLOAD:
            if fail_at == "asset":
                raise SQLAlchemyError("private asset detail")
            return upload_row() if asset is _DEFAULT else asset
        raise AssertionError("Unexpected API #56 SQL query.")

    monkeypatch.setattr(grade_view, "query_one", query_one)


def test_grade_mentor_submission_updates_grade_and_returns_submission(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cập nhật score/status, giữ feedback, resolve asset, rồi commit một lần."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: list[tuple[str, dict[str, Any]]] = []
    install_query_flow(monkeypatch, captured=captured)
    trace_id = "00000000-0000-4000-8000-000000000056"

    response = post_grade(client, trace_id=trace_id)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["traceId"] == trace_id
    assert response.headers["X-Trace-Id"] == trace_id
    assert payload["data"] == {
        "id": 56001,
        "assignment_id": 1250,
        "user_id": 804,
        "content": "Bài làm cần được chấm.",
        "files": [
            {
                "id": 34001,
                "name": "answer.pdf",
                "url": "https://storage.example/answer.pdf",
                "content_type": "application/pdf",
                "size_bytes": 12345,
                "status": "UPLOADED",
            }
        ],
        "status": "GRADED",
        "submitted_at": "2026-10-25T09:30:00",
        "score": "8.00",
        "feedback": "Feedback cũ được API #57 sở hữu.",
    }
    assert len(captured) == 3
    assert "FOR UPDATE OF s" in captured[0][0]
    assert "score = CAST(:score AS NUMERIC(6,2))" in captured[1][0]
    assert "status = 'GRADED'" in captured[1][0]
    assert captured[1][1]["score"] == Decimal("8")
    assert "rubric_items" not in captured[1][1]
    assert "u.url = :file_url" in captured[2][0]
    assert "u.owner_id = :user_id" in captured[2][0]
    assert "u.purpose = 'SUBMISSION'" in captured[2][0]
    assert "u.course_id = :course_id" in captured[2][0]
    assert "ORDER BY u.id ASC" in captured[2][0]
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_grade_mentor_submission_returns_empty_files_when_lookup_has_no_match(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả files rỗng khi không có file URL và omit field tùy chọn null."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: list[tuple[str, dict[str, Any]]] = []
    install_query_flow(
        monkeypatch,
        current=candidate_row(feedback=None),
        updated=graded_row(content=None, feedback=None),
        asset=None,
        captured=captured,
    )

    response = post_grade(client)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["files"] == []
    assert "content" not in data
    assert "feedback" not in data
    assert captured[-1][0] == FIND_GRADED_SUBMISSION_UPLOAD
    assert session.commit_count == 1


@pytest.mark.parametrize(
    ("authorization", "roles", "status_code", "business_code"),
    [
        (None, None, 401, "DESIGN_AUTHENTICATION_REQUIRED"),
        ("Bearer valid-token", ["STUDENT"], 403, "DESIGN_ACCESS_DENIED"),
    ],
)
def test_grade_mentor_submission_checks_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str] | None,
    status_code: int,
    business_code: str,
) -> None:
    """Từ chối auth thiếu hoặc sai role trước bất kỳ query DB nào."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    if authorization is not None:
        allow_mentor_token(monkeypatch, roles=roles)

    def fail_if_called(_db, _query, _params):
        """Báo lỗi nếu nhánh auth chạm tới database."""

        raise AssertionError("Database must not be queried before Mentor authentication.")

    monkeypatch.setattr(grade_view, "query_one", fail_if_called)
    response = post_grade(client, authorization=authorization)

    assert response.status_code == status_code
    assert response.json()["businessCode"] == business_code


@pytest.mark.parametrize("submission_id", ["abc", "9223372036854775808"])
def test_grade_mentor_submission_maps_bad_path_to_catalog_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    submission_id: str,
) -> None:
    """Ánh xạ path sai định dạng hoặc overflow về 404 mà không query DB."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_mentor_token(monkeypatch)

    def fail_if_called(_db, _query, _params):
        """Báo lỗi nếu path sai vẫn đến database."""

        raise AssertionError("Malformed submission IDs must not query the database.")

    monkeypatch.setattr(grade_view, "query_one", fail_if_called)
    response = post_grade(client, submission_id=submission_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


@pytest.mark.parametrize(
    "body",
    [
        {"rubric_items": "[]"},
        {"score": 8},
        {"score": "8", "rubric_items": "[]"},
        {"score": 8, "rubric_items": 1},
        {"score": 2**31, "rubric_items": "[]"},
        {"score": 8, "rubric items": "[]"},
    ],
)
def test_grade_mentor_submission_maps_bad_body_to_catalog_422(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: dict[str, Any],
) -> None:
    """Dùng DESIGN_VALIDATION_ERROR khi request thiếu/sai field theo fallback."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_mentor_token(monkeypatch)

    def fail_if_called(_db, _query, _params):
        """Báo lỗi nếu body không hợp lệ vẫn đến database."""

        raise AssertionError("Invalid grade bodies must not query the database.")

    monkeypatch.setattr(grade_view, "query_one", fail_if_called)
    response = post_grade(client, body=body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"


@pytest.mark.parametrize("score", [-1, 11])
def test_grade_mentor_submission_rejects_score_outside_assignment_max(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    score: int,
) -> None:
    """Không update và rollback khi score ngoài fallback [0, max_score]."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: list[tuple[str, dict[str, Any]]] = []
    install_query_flow(monkeypatch, captured=captured)

    response = post_grade(client, body=grade_body(score=score))

    assert response.status_code == 422
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert payload["meta"]["fieldErrors"][0]["field"] == "score"
    assert len(captured) == 1
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_grade_mentor_submission_allows_regrading_and_preserves_feedback(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cho phép regrade và giữ feedback riêng của API #57."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_query_flow(
        monkeypatch,
        current=candidate_row(status="GRADED", score=Decimal("7.00")),
    )

    response = post_grade(client)

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "GRADED"
    assert response.json()["data"]["feedback"] == "Feedback cũ được API #57 sở hữu."
    assert session.commit_count == 1


def test_grade_mentor_submission_handles_missing_and_unowned_rows(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map missing Submission thành 404 và course không sở hữu thành 403 trước update."""

    allow_mentor_token(monkeypatch)
    for current, expected_status, expected_code in [
        (None, 404, "DESIGN_RESOURCE_NOT_FOUND"),
        (candidate_row(mentor_id=2002), 403, "DESIGN_ACCESS_DENIED"),
    ]:
        session = FakeSession()
        client.app.dependency_overrides[get_db] = override_db(session)
        captured: list[tuple[str, dict[str, Any]]] = []
        install_query_flow(monkeypatch, current=current, captured=captured)

        response = post_grade(client)

        assert response.status_code == expected_status
        assert response.json()["businessCode"] == expected_code
        assert len(captured) == 1
        assert session.commit_count == 0
        assert session.rollback_count == 1


@pytest.mark.parametrize(
    "overrides",
    [
        {"assignment_id": None, "matched_assignment_id": None, "course_id": None},
        {"matched_assignment_id": None},
        {"course_id": None, "matched_course_id": None, "mentor_id": None},
        {"max_score": None},
    ],
)
def test_grade_mentor_submission_rejects_broken_parent_or_max_score(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    overrides: dict[str, Any],
) -> None:
    """Rollback khi relation bắt buộc hoặc max_score candidate không hợp lệ."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: list[tuple[str, dict[str, Any]]] = []
    install_query_flow(
        monkeypatch,
        current=candidate_row(**overrides),
        captured=captured,
    )

    response = post_grade(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert len(captured) == 1
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    ("fail_at", "expected_calls"),
    [("lock", 1), ("update", 2), ("asset", 3)],
)
def test_grade_mentor_submission_rolls_back_database_failures(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    fail_at: str,
    expected_calls: int,
) -> None:
    """Trả lỗi an toàn và rollback lỗi lock, update hoặc asset lookup."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: list[tuple[str, dict[str, Any]]] = []
    install_query_flow(monkeypatch, fail_at=fail_at, captured=captured)

    response = post_grade(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private" not in response.text
    assert len(captured) == expected_calls
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_grade_mentor_submission_rejects_update_with_no_returning_row(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối khi owner predicate tại thời điểm UPDATE không còn khớp."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query, params):
        """Trả hàng đã được authorize rồi mô phỏng UPDATE không còn đủ quyền."""

        captured.append((query, params))
        if query == LOCK_MENTOR_SUBMISSION_FOR_GRADE:
            return candidate_row()
        if query == UPDATE_MENTOR_SUBMISSION_GRADE:
            return None
        raise AssertionError("Asset lookup must not run after an empty UPDATE.")

    monkeypatch.setattr(grade_view, "query_one", query_one)
    response = post_grade(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert len(captured) == 2
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_grade_mentor_submission_rolls_back_invalid_mapping_and_commit_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback projection lỗi và lỗi commit thay vì trả success chưa lưu."""

    allow_mentor_token(monkeypatch)
    for updated, fail_commit in [
        (graded_row(score=Decimal("9.00")), False),
        (_DEFAULT, True),
    ]:
        session = FakeSession(fail_commit=fail_commit)
        client.app.dependency_overrides[get_db] = override_db(session)
        install_query_flow(monkeypatch, updated=updated)

        response = post_grade(client)

        assert response.status_code == 500
        assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
        assert session.commit_count == int(fail_commit)
        assert session.rollback_count == 1


def test_grade_mentor_submission_rolls_back_partial_asset_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không commit nếu UploadAsset query trả row thiếu field bắt buộc."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_query_flow(monkeypatch, asset=upload_row(name=None))
    response = post_grade(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_grade_mentor_submission_openapi_and_dynamic_error_mapping(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """OpenAPI giữ int64/int32; dynamic route dùng catalog validation code."""

    schema = client.app.openapi()
    path = "/api/v1/mentor/submissions/{submission_id}/grade"
    operation = schema["paths"][path]["post"]
    path_parameter = next(
        parameter for parameter in operation["parameters"] if parameter["name"] == "submission_id"
    )
    request_schema = schema["components"]["schemas"]["GradeSubmissionRequest"]
    request_ref = operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]

    assert path_parameter["schema"]["type"] == "integer"
    assert path_parameter["schema"]["format"] == "int64"
    assert request_ref.endswith("/GradeSubmissionRequest")
    assert request_schema["properties"]["score"]["type"] == "integer"
    assert request_schema["properties"]["score"]["format"] == "int32"
    assert request_schema["properties"]["rubric_items"]["type"] == "string"
    assert set(request_schema["required"]) == {"score", "rubric_items"}

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_mentor_token(monkeypatch)

    def fail_if_called(_db, _query, _params):
        """Báo lỗi nếu validation thất bại nhưng handler vẫn query database."""

        raise AssertionError("Invalid body must not query the database.")

    monkeypatch.setattr(grade_view, "query_one", fail_if_called)
    response = post_grade(client, body={"score": 2**40, "rubric_items": "[]"})

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
