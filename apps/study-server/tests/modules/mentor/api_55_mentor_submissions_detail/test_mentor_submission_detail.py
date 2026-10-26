from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

import app.modules.mentor.api_55_mentor_submissions_detail.view as submission_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Theo dõi transaction để bảo đảm API #55 chỉ đọc dữ liệu."""

    def __init__(self) -> None:
        """Khởi tạo bộ đếm commit và rollback của request."""
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận nếu endpoint gọi commit ngoài contract read-only."""
        self.commit_count += 1

    def rollback(self) -> None:
        """Ghi nhận cleanup transaction ở nhánh not-found, denied hoặc lỗi."""
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency database kiểm thử trả về fake session đã theo dõi."""

    def dependency():
        """Yield fake session cho một request TestClient."""
        yield session

    return dependency


def allow_mentor_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Thay JWT decoder bằng numeric subject có role Mentor mặc định."""

    def decode_token(_token: str) -> dict[str, Any]:
        """Trả claims giả lập theo role của test hiện tại."""
        return {"sub": "1001", "roles": roles or ["MENTOR"]}

    monkeypatch.setattr(auth_utils, "decode_access_token", decode_token)


def submission_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection hợp lệ gồm Submission, quan hệ course và UploadAsset."""

    return {
        "id": 55001,
        "assignment_id": 1250,
        "user_id": 804,
        "content": "Bài làm cần được chấm.",
        "status": "SUBMITTED",
        "submitted_at": datetime(2026, 10, 25, 9, 30),
        "score": Decimal("8.50"),
        "feedback": "Cần giải thích thêm bước cuối.",
        "matched_assignment_id": 1250,
        "course_id": 101,
        "matched_course_id": 101,
        "mentor_id": 1001,
        "file_id": 34001,
        "file_name": "answer.pdf",
        "file_url": "https://storage.example/answer.pdf",
        "file_content_type": "application/pdf",
        "file_size_bytes": 12345,
        "file_status": "UPLOADED",
        **overrides,
    }


def get_submission(
    client: TestClient,
    submission_id: str = "55001",
    *,
    authorization: str | None = "Bearer valid-token",
    trace_id: str | None = None,
):
    """Gửi GET API #55 với path, Bearer token và trace header tùy chọn."""

    headers = {} if authorization is None else {"Authorization": authorization}
    if trace_id is not None:
        headers["X-Trace-Id"] = trace_id
    return client.get(f"/api/v1/mentor/submissions/{submission_id}", headers=headers)


def test_get_mentor_submission_returns_submission_and_scoped_upload(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả Submission và file khớp URL, owner, purpose, course cùng trace ID."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: dict[str, Any] = {}

    def find_submission(_db, query, params):
        """Ghi nhận truy vấn và trả một Submission thuộc course của Mentor."""
        captured["sql"] = query
        captured["params"] = params
        return submission_row()

    monkeypatch.setattr(submission_view, "query_one", find_submission)
    trace_id = "00000000-0000-4000-8000-000000000055"

    response = get_submission(client, trace_id=trace_id)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["traceId"] == trace_id
    assert response.headers["X-Trace-Id"] == trace_id
    assert payload["data"] == {
        "id": 55001,
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
        "status": "SUBMITTED",
        "submitted_at": "2026-10-25T09:30:00",
        "score": "8.50",
        "feedback": "Cần giải thích thêm bước cuối.",
    }
    assert "LEFT JOIN assignments AS a" in captured["sql"]
    assert "LEFT JOIN courses AS c" in captured["sql"]
    assert "LEFT JOIN LATERAL" in captured["sql"]
    assert "u.url = s.file_url" in captured["sql"]
    assert "u.owner_id = s.user_id" in captured["sql"]
    assert "u.purpose = 'SUBMISSION'" in captured["sql"]
    assert "u.course_id = a.course_id" in captured["sql"]
    assert "ORDER BY u.id ASC" in captured["sql"]
    assert captured["params"] == {"submission_id": 55001}
    assert "rubric" not in payload["data"]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_mentor_submission_returns_empty_files_and_omits_optional_nulls(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Giữ files là mảng rỗng và dùng omit policy đang có cho field tùy chọn null."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_mentor_token(monkeypatch)

    def find_submission(_db, _query, _params):
        """Trả Submission không có metadata file hoặc giá trị optional."""
        return submission_row(
            content=None,
            score=None,
            feedback=None,
            file_id=None,
            file_name=None,
            file_url=None,
            file_content_type=None,
            file_size_bytes=None,
            file_status=None,
        )

    monkeypatch.setattr(submission_view, "query_one", find_submission)

    response = get_submission(client)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["files"] == []
    assert "content" not in data
    assert "score" not in data
    assert "feedback" not in data


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_get_mentor_submission_rejects_missing_or_malformed_auth_before_db(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Từ chối Authorization thiếu hoặc sai định dạng trước khi truy vấn."""

    def unexpected_query(_db, _query, _params):
        """Báo lỗi nếu request chưa xác thực chạm database."""
        raise AssertionError("database query must not run")

    monkeypatch.setattr(submission_view, "query_one", unexpected_query)

    response = get_submission(client, authorization=authorization)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_get_mentor_submission_rejects_non_mentor_role_before_db(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối JWT Student trên endpoint Mentor trước khi đọc Submission."""

    allow_mentor_token(monkeypatch, roles=["STUDENT"])

    def unexpected_query(_db, _query, _params):
        """Báo lỗi nếu role không hợp lệ vẫn chạm database."""
        raise AssertionError("database query must not run")

    monkeypatch.setattr(submission_view, "query_one", unexpected_query)

    response = get_submission(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


@pytest.mark.parametrize(
    "submission_id",
    ["abc", "9223372036854775808", "-9223372036854775809"],
)
def test_get_mentor_submission_maps_malformed_or_out_of_range_id_to_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    submission_id: str,
) -> None:
    """Map path sai định dạng hoặc ngoài signed-int64 vào lỗi 404 trong catalog."""

    allow_mentor_token(monkeypatch)

    def unexpected_query(_db, _query, _params):
        """Báo lỗi nếu path không hợp lệ vẫn truy vấn database."""
        raise AssertionError("invalid submission ID must not query")

    monkeypatch.setattr(submission_view, "query_one", unexpected_query)

    response = get_submission(client, submission_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_mentor_submission_returns_not_found_when_row_is_absent(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 404 khi ID hợp lệ không có Submission và dọn read transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)

    def find_missing(_db, _query, _params):
        """Mô phỏng lookup hợp lệ không tìm thấy row."""
        return None

    monkeypatch.setattr(submission_view, "query_one", find_missing)

    response = get_submission(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_mentor_submission_forbids_other_owner_before_mapping_response(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 403 cho course của Mentor khác và không serialize Submission."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)

    def find_other_owner(_db, _query, _params):
        """Trả row hợp lệ nhưng course thuộc Mentor khác."""
        return submission_row(mentor_id=2002)

    def unexpected_mapping(_row):
        """Báo lỗi nếu response mapper chạy trước khi kiểm tra ownership."""
        raise AssertionError("submission must not be mapped before access check")

    monkeypatch.setattr(submission_view, "query_one", find_other_owner)
    monkeypatch.setattr(submission_view, "_map_submission", unexpected_mapping)

    response = get_submission(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    "overrides",
    [
        {"assignment_id": None},
        {"matched_assignment_id": None},
        {"assignment_id": 1250, "matched_assignment_id": 1251},
        {"course_id": None},
        {"matched_course_id": None},
        {"course_id": 101, "matched_course_id": 102},
        {"mentor_id": None},
        {"user_id": None},
    ],
)
def test_get_mentor_submission_rejects_broken_parent_relations(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    overrides: dict[str, Any],
) -> None:
    """Map null/orphan assignment, course hoặc required identity thành safe 500."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)

    def find_broken_relation(_db, _query, _params):
        """Trả candidate row có quan hệ bắt buộc không hợp lệ."""
        return submission_row(**overrides)

    monkeypatch.setattr(submission_view, "query_one", find_broken_relation)

    response = get_submission(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "assignment_id" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_mentor_submission_returns_safe_internal_error_for_database_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Chuyển lỗi SQLAlchemy thành 500 an toàn và rollback transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)

    def fail_query(_db, _query, _params):
        """Ném lỗi DB giả lập để kiểm tra nhánh system error."""
        raise SQLAlchemyError("private database detail")

    monkeypatch.setattr(submission_view, "query_one", fail_query)

    response = get_submission(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private database detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_mentor_submission_rejects_partial_upload_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không trả UploadAsset nếu metadata row thiếu field bắt buộc."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)

    def find_partial_upload(_db, _query, _params):
        """Trả asset ID nhưng thiếu tên file để mô phỏng mapping lỗi."""
        return submission_row(file_name=None)

    monkeypatch.setattr(submission_view, "query_one", find_partial_upload)

    response = get_submission(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_mentor_submission_detail_openapi_declares_int64_path_and_submission_shape(
    client: TestClient,
) -> None:
    """Giữ path int64 và response schema theo reusable Submission, không tự thêm rubric."""

    schema = client.app.openapi()
    operation = schema["paths"]["/api/v1/mentor/submissions/{submission_id}"]["get"]
    path_parameter = next(
        parameter
        for parameter in operation["parameters"]
        if parameter["name"] == "submission_id"
    )
    assert path_parameter["required"] is True
    assert path_parameter["schema"]["type"] == "integer"
    assert path_parameter["schema"]["format"] == "int64"

    envelope_ref = operation["responses"]["200"]["content"]["application/json"][
        "schema"
    ]["$ref"]
    envelope_name = envelope_ref.rsplit("/", 1)[-1]
    data_ref = schema["components"]["schemas"][envelope_name]["properties"]["data"][
        "$ref"
    ]
    submission_name = data_ref.rsplit("/", 1)[-1]
    submission_schema = schema["components"]["schemas"][submission_name]
    assert set(submission_schema["properties"]) == {
        "id",
        "assignment_id",
        "user_id",
        "content",
        "files",
        "status",
        "submitted_at",
        "score",
        "feedback",
    }
