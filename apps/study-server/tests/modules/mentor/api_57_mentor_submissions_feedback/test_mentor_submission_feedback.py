from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

import app.modules.mentor.api_57_mentor_submissions_feedback.view as feedback_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.mentor.api_57_mentor_submissions_feedback.query import (
    FIND_FEEDBACK_SUBMISSION_UPLOAD,
    LOCK_MENTOR_SUBMISSION_FOR_FEEDBACK,
    UPDATE_MENTOR_SUBMISSION_FEEDBACK,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

_DEFAULT = object()


class FakeSession:
    """Theo dõi commit/rollback transaction API #57."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        """Khởi tạo bộ đếm transaction và cấu hình lỗi commit tùy chọn."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát sinh lỗi SQLAlchemy đã cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("private commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback do view yêu cầu."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override cung cấp FakeSession cho TestClient."""

    def dependency():
        """Yield session giả trong vòng đời request."""

        yield session

    return dependency


def allow_mentor_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Thay decoder JWT bằng numeric subject và role Mentor mặc định."""

    def decode_token(_token: str) -> dict[str, Any]:
        """Trả claim giả lập theo role đã chọn trong test."""

        return {"sub": "1001", "roles": roles or ["MENTOR"]}

    monkeypatch.setattr(auth_utils, "decode_access_token", decode_token)


def current_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection hợp lệ của Submission và quan hệ Assignment/Course."""

    return {
        "id": 57001,
        "assignment_id": 1250,
        "user_id": 804,
        "content": "Bài làm cần được nhận xét.",
        "file_url": "https://storage.example/answer.pdf",
        "submitted_at": datetime(2026, 10, 25, 10, 30),
        "score": Decimal("8.00"),
        "feedback": "Feedback trước.",
        "status": "GRADED",
        "matched_assignment_id": 1250,
        "course_id": 101,
        "matched_course_id": 101,
        "mentor_id": 1001,
        **overrides,
    }


def updated_row(**overrides: Any) -> dict[str, Any]:
    """Tạo UPDATE RETURNING projection có feedback mới."""

    row = current_row()
    row["feedback"] = "Bài làm có lập luận rõ ràng."
    row.update(overrides)
    return row


def upload_row(**overrides: Any) -> dict[str, Any]:
    """Tạo metadata UploadAsset đầy đủ cho response files."""

    return {
        "id": 34001,
        "name": "answer.pdf",
        "url": "https://storage.example/answer.pdf",
        "content_type": "application/pdf",
        "size_bytes": 12345,
        "status": "UPLOADED",
        **overrides,
    }


def feedback_body(**overrides: Any) -> dict[str, Any]:
    """Tạo body API #57 theo các wire key fallback đã chọn."""

    return {
        "feedback_text": "Bài làm có lập luận rõ ràng.",
        "attachments": "opaque-attachment-descriptor",
        **overrides,
    }


def post_feedback(
    client: TestClient,
    *,
    submission_id: str = "57001",
    body: dict[str, Any] | None = None,
    authorization: str | None = "Bearer valid-token",
    trace_id: str | None = None,
):
    """Gửi POST API #57 bằng Bearer token và body tùy chọn."""

    headers = {} if authorization is None else {"Authorization": authorization}
    if trace_id is not None:
        headers["X-Trace-Id"] = trace_id
    return client.post(
        f"/api/v1/mentor/submissions/{submission_id}/feedback",
        json=feedback_body() if body is None else body,
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
    """Cài query fake theo các giai đoạn lock, update và asset lookup."""

    def query_one(_db, query: str, params: dict[str, Any]):
        """Ghi nhận SQL và trả projection cho giai đoạn tương ứng."""

        if captured is not None:
            captured.append((query, params))
        if query == LOCK_MENTOR_SUBMISSION_FOR_FEEDBACK:
            if fail_at == "lock":
                raise SQLAlchemyError("private lock detail")
            return current_row() if current is _DEFAULT else current
        if query == UPDATE_MENTOR_SUBMISSION_FEEDBACK:
            if fail_at == "update":
                raise SQLAlchemyError("private update detail")
            return updated_row() if updated is _DEFAULT else updated
        if query == FIND_FEEDBACK_SUBMISSION_UPLOAD:
            if fail_at == "asset":
                raise SQLAlchemyError("private asset detail")
            return upload_row() if asset is _DEFAULT else asset
        raise AssertionError("Unexpected API #57 SQL query.")

    monkeypatch.setattr(feedback_view, "query_one", query_one)


def test_feedback_saves_text_and_returns_submission_without_echoing_attachments(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Lưu feedback, dựng Submission/file và không phản chiếu attachments."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: list[tuple[str, dict[str, Any]]] = []
    install_query_flow(monkeypatch, captured=captured)
    trace_id = "00000000-0000-4000-8000-000000000057"

    response = post_feedback(client, trace_id=trace_id)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["traceId"] == trace_id
    assert response.headers["X-Trace-Id"] == trace_id
    assert payload["data"] == {
        "id": 57001,
        "assignment_id": 1250,
        "user_id": 804,
        "content": "Bài làm cần được nhận xét.",
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
        "submitted_at": "2026-10-25T10:30:00",
        "score": "8.00",
        "feedback": "Bài làm có lập luận rõ ràng.",
    }
    assert "attachments" not in payload["data"]
    assert len(captured) == 3
    assert "FOR UPDATE OF s" in captured[0][0]
    assert captured[1][0] == UPDATE_MENTOR_SUBMISSION_FEEDBACK
    assert "SET feedback = :feedback_text" in captured[1][0]
    assert "score =" not in captured[1][0]
    assert "status =" not in captured[1][0]
    assert captured[1][1] == {
        "submission_id": 57001,
        "assignment_id": 1250,
        "mentor_id": 1001,
        "feedback_text": "Bài làm có lập luận rõ ràng.",
    }
    assert "attachments" not in captured[1][1]
    assert "u.url = :file_url" in captured[2][0]
    assert "u.owner_id = :user_id" in captured[2][0]
    assert "u.purpose = 'SUBMISSION'" in captured[2][0]
    assert "u.course_id = :course_id" in captured[2][0]
    assert "ORDER BY u.id ASC" in captured[2][0]
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_feedback_allows_empty_text_and_returns_empty_files_when_no_student_file(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Chấp nhận chuỗi feedback rỗng và trả files rỗng khi không có URL file."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_query_flow(
        monkeypatch,
        current=current_row(file_url=None, content=None),
        updated=updated_row(file_url=None, content=None, feedback=""),
        asset=None,
    )

    response = post_feedback(client, body=feedback_body(feedback_text=""))

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["files"] == []
    assert "content" not in data
    assert data["feedback"] == ""
    assert session.commit_count == 1


def test_feedback_does_not_require_graded_and_preserves_current_score_and_status(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cho phép gọi trước GRADED và giữ nguyên score/status hiện có."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_query_flow(
        monkeypatch,
        current=current_row(status="SUBMITTED", score=None),
        updated=updated_row(status="SUBMITTED", score=None),
        asset=None,
    )

    response = post_feedback(client)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["status"] == "SUBMITTED"
    assert "score" not in data
    assert data["feedback"] == "Bài làm có lập luận rõ ràng."
    assert session.commit_count == 1


@pytest.mark.parametrize(
    ("authorization", "roles", "status_code", "business_code"),
    [
        (None, None, 401, "DESIGN_AUTHENTICATION_REQUIRED"),
        ("Bearer valid-token", ["STUDENT"], 403, "DESIGN_ACCESS_DENIED"),
    ],
)
def test_feedback_checks_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str] | None,
    status_code: int,
    business_code: str,
) -> None:
    """Từ chối auth/role không hợp lệ trước mọi query dữ liệu."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    if authorization is not None:
        allow_mentor_token(monkeypatch, roles=roles)

    def unexpected_query(*_args, **_kwargs):
        """Phát hiện truy vấn dữ liệu trước khi xác thực Mentor thành công."""

        raise AssertionError("Database must not be queried before Mentor auth passes.")

    monkeypatch.setattr(feedback_view, "query_one", unexpected_query)

    response = post_feedback(client, authorization=authorization)

    assert response.status_code == status_code
    assert response.json()["businessCode"] == business_code
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize("submission_id", ["abc", "9223372036854775808", "-9223372036854775809"])
def test_feedback_maps_invalid_path_to_catalog_422(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    submission_id: str,
) -> None:
    """Ánh xạ path sai định dạng hoặc tràn int64 sang 422 catalog."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)

    def unexpected_query(*_args, **_kwargs):
        """Phát hiện path int64 không hợp lệ vẫn chạm database."""

        raise AssertionError("Invalid int64 path must not reach the database.")

    monkeypatch.setattr(feedback_view, "query_one", unexpected_query)

    response = post_feedback(client, submission_id=submission_id)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "submission_id"


@pytest.mark.parametrize(
    "body",
    [
        {"attachments": "opaque"},
        {"feedback_text": "good"},
        {"feedback_text": 42, "attachments": "opaque"},
        {"feedback_text": "good", "attachments": ["file-id"]},
        {"feedback_text": "good", "attachments": "opaque", "extra": True},
    ],
)
def test_feedback_maps_invalid_body_to_catalog_422(
    client: TestClient,
    body: dict[str, Any],
) -> None:
    """Ánh xạ body thiếu, sai kiểu hoặc có field thừa sang 422 catalog."""

    response = post_feedback(client, body=body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None


def test_feedback_handles_missing_and_unowned_submission(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 404 cho row thiếu và 403 cho course của Mentor khác."""

    allow_mentor_token(monkeypatch)
    missing_session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(missing_session)
    install_query_flow(monkeypatch, current=None)

    missing = post_feedback(client)

    assert missing.status_code == 404
    assert missing.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert missing_session.rollback_count == 1

    unowned_session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(unowned_session)
    install_query_flow(monkeypatch, current=current_row(mentor_id=2002))

    unowned = post_feedback(client)

    assert unowned.status_code == 403
    assert unowned.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert unowned_session.rollback_count == 1
    assert unowned_session.commit_count == 0


@pytest.mark.parametrize(
    "overrides",
    [
        {"assignment_id": None, "matched_assignment_id": None, "course_id": None},
        {"matched_assignment_id": 9999},
        {"matched_course_id": 9999},
        {"mentor_id": None},
    ],
)
def test_feedback_rejects_broken_parent_or_owner_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    overrides: dict[str, Any],
) -> None:
    """Trả lỗi 500 an toàn khi relation hoặc owner projection bị hỏng."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_query_flow(monkeypatch, current=current_row(**overrides))

    response = post_feedback(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize("fail_at", ["lock", "update", "asset"])
def test_feedback_rolls_back_database_failures(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    fail_at: str,
) -> None:
    """Rollback và che chi tiết nội bộ khi query lock/update/asset lỗi."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_query_flow(monkeypatch, fail_at=fail_at)

    response = post_feedback(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_feedback_rolls_back_when_owner_predicate_returns_no_row(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback nếu UPDATE không còn khớp owner predicate."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_query_flow(monkeypatch, updated=None)

    response = post_feedback(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    ("updated", "asset"),
    [
        (updated_row(status="SUBMITTED"), _DEFAULT),
        (updated_row(score=Decimal("9.00")), _DEFAULT),
        (updated_row(feedback="different"), _DEFAULT),
        (updated_row(), {"id": 34001}),
    ],
)
def test_feedback_rolls_back_invalid_returning_or_asset_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    updated: Any,
    asset: Any,
) -> None:
    """Rollback khi RETURNING hoặc UploadAsset không khớp projection."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_query_flow(monkeypatch, updated=updated, asset=asset)

    response = post_feedback(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_feedback_rolls_back_commit_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback an toàn và trả 500 nếu commit thất bại."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_query_flow(monkeypatch)

    response = post_feedback(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_feedback_openapi_and_dynamic_error_mapping(client: TestClient) -> None:
    """Kiểm tra path/body OpenAPI và đăng ký dynamic design-error mapping."""

    from app.core.middleware import DESIGN_CONTRACT_PATHS

    path = "/api/v1/mentor/submissions/{submission_id}/feedback"
    assert path in DESIGN_CONTRACT_PATHS
    openapi = client.app.openapi()
    operation = openapi["paths"][path]["post"]
    parameters = {parameter["name"]: parameter for parameter in operation["parameters"]}
    assert parameters["submission_id"]["schema"]["format"] == "int64"
    body_schema = openapi["components"]["schemas"]["FeedbackSubmissionRequest"]
    assert body_schema["required"] == ["feedback_text", "attachments"]
    assert body_schema["properties"]["feedback_text"]["type"] == "string"
    assert body_schema["properties"]["attachments"]["type"] == "string"
