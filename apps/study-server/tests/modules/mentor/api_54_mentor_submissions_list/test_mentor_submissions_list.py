from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

import app.modules.mentor.api_54_mentor_submissions_list.view as submissions_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.mentor.api_54_mentor_submissions_list.query import (
    COUNT_MENTOR_SUBMISSIONS,
    FIND_MENTOR_COURSE,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Theo dõi rollback/commit để kiểm tra API #54 chỉ đọc dữ liệu."""

    def __init__(self) -> None:
        """Khởi tạo bộ đếm thao tác transaction của request."""
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận nếu route gọi commit ngoài contract read-only."""
        self.commit_count += 1

    def rollback(self) -> None:
        """Ghi nhận cleanup transaction ở nhánh lỗi hoặc quyền bị từ chối."""
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo FastAPI dependency trả fake session cho một request test."""

    def dependency():
        """Yield session được test đang theo dõi."""
        yield session

    return dependency


def allow_mentor_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Thay decoder bằng numeric JWT subject có role Mentor."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": roles or ["MENTOR"]},
    )


def submission_row(**overrides: Any) -> dict[str, Any]:
    """Tạo SQL projection hợp lệ cho một bài nộp và một file đã upload."""

    return {
        "id": 54001,
        "assignment_id": 1201,
        "user_id": 804,
        "content": "Bài làm mẫu",
        "status": "SUBMITTED",
        "submitted_at": datetime(2026, 10, 24, 9, 30),
        "score": Decimal("8.50"),
        "feedback": None,
        "file_id": 34001,
        "file_name": "answer.pdf",
        "file_url": "https://storage.example/answer.pdf",
        "file_content_type": "application/pdf",
        "file_size_bytes": 12345,
        "file_status": "UPLOADED",
        **overrides,
    }


def get_submissions(
    client: TestClient,
    *,
    query: str = "",
    authorization: str | None = "Bearer valid-token",
):
    """Gửi GET API #54 với query string và Bearer token tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get(f"/api/v1/mentor/submissions{query}", headers=headers)


def test_get_mentor_submissions_returns_page_and_linked_upload(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả trang Submission cùng asset khớp URL, owner, purpose và course."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: dict[str, Any] = {}

    def query_one(_db, query, params):
        """Trả course owner hoặc tổng số theo SQL constant được gọi."""

        captured.setdefault("query_one", []).append((query, params))
        if query == FIND_MENTOR_COURSE:
            return {"id": 101, "mentor_id": 1001}
        assert query == COUNT_MENTOR_SUBMISSIONS
        return {"total": 21}

    def query_many(_db, query, params):
        """Ghi nhận query trang và trả projection bài nộp có asset."""

        captured["list_sql"] = query
        captured["list_params"] = params
        return [submission_row()]

    monkeypatch.setattr(submissions_view, "query_one", query_one)
    monkeypatch.setattr(submissions_view, "query_many", query_many)

    response = get_submissions(
        client,
        query="?course_id=101&status=SUBMITTED&page=2",
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["pagination"] == {
        "page": 2,
        "size": 20,
        "total": 21,
        "total_pages": 2,
    }
    assert payload["data"]["items"][0]["score"] == "8.50"
    assert payload["data"]["items"][0]["files"] == [
        {
            "id": 34001,
            "name": "answer.pdf",
            "url": "https://storage.example/answer.pdf",
            "content_type": "application/pdf",
            "size_bytes": 12345,
            "status": "UPLOADED",
        }
    ]
    assert captured["list_params"] == {
        "mentor_id": 1001,
        "course_id": 101,
        "status": "SUBMITTED",
        "limit": 20,
        "offset": 20,
    }
    assert "c.mentor_id = :mentor_id" in captured["list_sql"]
    assert "u.owner_id = s.user_id" in captured["list_sql"]
    assert "u.purpose = 'SUBMISSION'" in captured["list_sql"]
    assert "u.course_id = a.course_id" in captured["list_sql"]
    assert "ORDER BY s.submitted_at DESC, s.id DESC" in captured["list_sql"]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_mentor_submissions_returns_empty_page_without_asset(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả collection rỗng hợp lệ khi không có submission phù hợp."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        submissions_view,
        "query_one",
        lambda _db, _query, _params: {"total": 0},
    )
    monkeypatch.setattr(submissions_view, "query_many", lambda *_args: [])

    response = get_submissions(client)

    assert response.status_code == 200
    assert response.json()["data"] == {
        "items": [],
        "pagination": {"page": 1, "size": 20, "total": 0, "total_pages": 0},
    }
    assert response.json()["message"] == "No submissions found."
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_mentor_submissions_returns_empty_files_when_no_upload_matches(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không dựng asset khi URL bài nộp không có metadata upload khớp."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        submissions_view,
        "query_one",
        lambda _db, _query, _params: {"total": 1},
    )
    monkeypatch.setattr(
        submissions_view,
        "query_many",
        lambda *_args: [
            submission_row(
                file_id=None,
                file_name=None,
                file_url=None,
                file_content_type=None,
                file_size_bytes=None,
                file_status=None,
            )
        ],
    )

    response = get_submissions(client)

    assert response.status_code == 200
    assert response.json()["data"]["items"][0]["files"] == []


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_get_mentor_submissions_rejects_missing_or_malformed_bearer(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Từ chối Bearer thiếu hoặc sai định dạng trước khi query database."""

    def fail_if_queried(*_args, **_kwargs):
        """Báo lỗi nếu request chưa xác thực vẫn truy cập dữ liệu."""

        pytest.fail("database was queried before Mentor authentication")

    monkeypatch.setattr(submissions_view, "query_one", fail_if_queried)
    monkeypatch.setattr(submissions_view, "query_many", fail_if_queried)

    response = get_submissions(client, authorization=authorization)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert response.json()["data"] is None


def test_get_mentor_submissions_rejects_non_mentor_role(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối user không có role Mentor trước khi truy vấn bài nộp."""

    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    monkeypatch.setattr(
        submissions_view,
        "query_one",
        lambda *_args, **_kwargs: pytest.fail("database was queried before role check"),
    )

    response = get_submissions(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_get_mentor_submissions_rejects_course_owned_by_another_mentor(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 403 nếu course filter thuộc Mentor khác mà không đọc danh sách."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: list[str] = []

    def query_one(_db, query, _params):
        """Trả course có owner khác để kiểm tra quyền trực tiếp."""

        captured.append(query)
        return {"id": 101, "mentor_id": 2002}

    monkeypatch.setattr(submissions_view, "query_one", query_one)
    monkeypatch.setattr(
        submissions_view,
        "query_many",
        lambda *_args: pytest.fail("submission list was read for another Mentor"),
    )

    response = get_submissions(client, query="?course_id=101")

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert captured == [FIND_MENTOR_COURSE]
    assert session.rollback_count == 1


def test_get_mentor_submissions_maps_database_errors_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Chuyển lỗi query database thành 500 an toàn và rollback read transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        submissions_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(SQLAlchemyError("private SQL detail")),
    )

    response = get_submissions(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private SQL detail" not in response.text
    assert session.rollback_count == 1


def test_get_mentor_submissions_rejects_malformed_asset_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không trả một Submission có asset projection thiếu metadata bắt buộc."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        submissions_view,
        "query_one",
        lambda _db, _query, _params: {"total": 1},
    )
    monkeypatch.setattr(
        submissions_view,
        "query_many",
        lambda *_args: [submission_row(file_name=None)],
    )

    response = get_submissions(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_get_mentor_submissions_validates_positive_page_and_course_id(
    client: TestClient,
) -> None:
    """Trả 422 với business code design khi page hoặc course_id nằm ngoài miền dương."""

    for query in ("?page=0", "?course_id=0"):
        response = get_submissions(client, query=query)
        assert response.status_code == 422
        assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
        assert response.json()["data"] is None


def test_get_mentor_submissions_openapi_describes_query_and_page_response(
    client: TestClient,
) -> None:
    """Mô tả query types và Page<Submission> trong OpenAPI."""

    operation = client.app.openapi()["paths"]["/api/v1/mentor/submissions"]["get"]
    params = {parameter["name"]: parameter for parameter in operation["parameters"]}

    assert set(params) >= {"course_id", "status", "page", "Authorization"}
    assert params["course_id"]["schema"]["format"] == "int64"
    assert params["page"]["schema"]["format"] == "int32"
    response_schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
    assert response_schema["$ref"].endswith("GetMentorSubmissionsEnvelope")
