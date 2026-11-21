from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.mentor.api_59_mentor_support_request_detail.view as support_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.mentor.api_59_mentor_support_request_detail.query import (
    FIND_MENTOR_SUPPORT_REQUEST,
    LIST_MENTOR_SUPPORT_REQUEST_MESSAGES,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Theo dõi commit/rollback cho các nhánh chỉ đọc của API #59."""

    def __init__(self) -> None:
        """Khởi tạo bộ đếm giao dịch."""
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận commit nếu endpoint đọc dữ liệu lại ghi transaction."""
        self.commit_count += 1

    def rollback(self) -> None:
        """Ghi nhận rollback khi endpoint gặp lỗi hoặc từ chối quyền."""
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency trả fake session cho một HTTP request."""

    def dependency():
        """Yield phiên giả lập cho FastAPI dependency injection."""
        yield session

    return dependency


def allow_mentor_token(monkeypatch: pytest.MonkeyPatch, *, roles: list[str] | None = None) -> None:
    """Thay decoder bằng JWT numeric subject có role đã chọn."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": roles or ["MENTOR"]},
    )


def request_row(**overrides: Any) -> dict[str, Any]:
    """Tạo parent projection hợp lệ cho một request và các FK cha."""

    return {
        "id": 59001,
        "course_id": 120,
        "parent_course_id": 120,
        "mentor_id": 1001,
        "student_id": 2042,
        "status": "OPEN",
        "created_at": datetime(2026, 10, 24, 8, 20, tzinfo=UTC),
        "resolved_at": None,
        "student_user_id": 2042,
        "student_full_name": "Nguyễn An",
        "student_avatar_url": None,
        **overrides,
    }


def message_row(**overrides: Any) -> dict[str, Any]:
    """Tạo Q2 projection hợp lệ cho message không có upload."""

    return {
        "request_id": 59001,
        "course_id": 120,
        "parent_course_id": 120,
        "mentor_id": 1001,
        "message_id": 90001,
        "author_id": 604,
        "author_user_id": 604,
        "author_role": "MENTOR",
        "author_full_name": "Trần Mentor",
        "author_avatar_url": None,
        "content": "Học viên cần hỗ trợ.",
        "message_created_at": datetime(2026, 10, 24, 8, 30, tzinfo=UTC),
        "linked_upload_id": None,
        "attachment_id": None,
        "attachment_name": None,
        "attachment_url": None,
        "attachment_content_type": None,
        "attachment_size_bytes": None,
        "attachment_status": None,
        **overrides,
    }


def get_request(
    client: TestClient,
    request_id: str = "59001",
    *,
    authorization: str | None = "Bearer valid-token",
):
    """Gửi GET API #59 với token Mentor mặc định."""

    headers = {} if authorization is None else {"Authorization": authorization}
    return client.get(f"/api/v1/mentor/support/{request_id}", headers=headers)


def test_get_mentor_support_request_returns_detail_thread_and_ordered_assets(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả một request, thread theo thời gian và attachment theo position query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    query_calls: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query, params):
        """Giả lập truy vấn request cùng owner/student projections."""
        query_calls.append((query, params))
        assert query == FIND_MENTOR_SUPPORT_REQUEST
        return request_row()

    def query_many(_db, query, params):
        """Giả lập thread đã sắp theo created_at/id/asset_position."""
        query_calls.append((query, params))
        assert query == LIST_MENTOR_SUPPORT_REQUEST_MESSAGES
        return [
            message_row(
                linked_upload_id=34001,
                attachment_id=34001,
                attachment_name="first.pdf",
                attachment_url="https://storage.example/first.pdf",
                attachment_content_type="application/pdf",
                attachment_size_bytes=4096,
                attachment_status="UPLOADED",
            ),
            message_row(
                linked_upload_id=34002,
                attachment_id=34002,
                attachment_name="second.pdf",
                attachment_url="https://storage.example/second.pdf",
                attachment_content_type="application/pdf",
                attachment_size_bytes=2048,
                attachment_status="UPLOADED",
            ),
            message_row(
                message_id=90002,
                author_id=2042,
                author_user_id=2042,
                author_role="STUDENT",
                author_full_name="Nguyễn An",
                content="Em gửi thêm thông tin.",
                message_created_at=datetime(2026, 10, 24, 8, 40, tzinfo=UTC),
            ),
        ]

    monkeypatch.setattr(support_view, "query_one", query_one)
    monkeypatch.setattr(support_view, "query_many", query_many)

    response = get_request(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert isinstance(payload["data"], dict)
    assert payload["data"]["id"] == 59001
    assert payload["data"]["student"] == {"id": 2042, "full_name": "Nguyễn An"}
    assert [message["id"] for message in payload["data"]["messages"]] == [90001, 90002]
    assert [
        asset["id"] for asset in payload["data"]["messages"][0]["attachments"]
    ] == [34001, 34002]
    assert payload["data"]["messages"][1]["attachments"] == []
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert query_calls == [
        (FIND_MENTOR_SUPPORT_REQUEST, {"request_id": 59001}),
        (
            LIST_MENTOR_SUPPORT_REQUEST_MESSAGES,
            {"request_id": 59001, "mentor_id": 1001},
        ),
    ]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_mentor_support_request_returns_empty_messages(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả messages rỗng khi LEFT JOIN không tìm thấy message nào."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(support_view, "query_one", lambda *_args: request_row())
    monkeypatch.setattr(
        support_view,
        "query_many",
        lambda *_args: [message_row(message_id=None, author_id=None, author_user_id=None,
                                    author_role=None, author_full_name=None,
                                    author_avatar_url=None, content=None,
                                    message_created_at=None)],
    )

    response = get_request(client)

    assert response.status_code == 200
    assert response.json()["data"]["messages"] == []
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize("request_id", ["abc", "9223372036854775808", "-9223372036854775809"])
def test_get_mentor_support_request_maps_invalid_int64_to_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    request_id: str,
) -> None:
    """Map path sai format hoặc vượt signed-int64 sang 404 catalog."""

    allow_mentor_token(monkeypatch)

    def fail_if_queried(*_args, **_kwargs):
        """Bảo đảm ID sai không truy cập database."""
        pytest.fail("database was queried for an invalid request ID")

    monkeypatch.setattr(support_view, "query_one", fail_if_queried)
    monkeypatch.setattr(support_view, "query_many", fail_if_queried)

    response = get_request(client, request_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_mentor_support_request_returns_404_when_missing(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả resource-not-found và không tải thread nếu request không tồn tại."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(support_view, "query_one", lambda *_args: None)

    def fail_if_queried(*_args, **_kwargs):
        """Bảo đảm không có truy vấn thread sau kết quả request rỗng."""
        pytest.fail("thread was queried for a missing request")

    monkeypatch.setattr(support_view, "query_many", fail_if_queried)

    response = get_request(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert session.rollback_count == 1


def test_get_mentor_support_request_returns_403_for_another_mentor(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả access-denied khi request tồn tại nhưng course có owner khác."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(support_view, "query_one", lambda *_args: request_row(mentor_id=2002))

    def fail_if_queried(*_args, **_kwargs):
        """Bảo đảm thread không được tải khi request ngoài scope."""
        pytest.fail("thread was queried for another Mentor's request")

    monkeypatch.setattr(support_view, "query_many", fail_if_queried)

    response = get_request(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.rollback_count == 1


def test_get_mentor_support_request_returns_safe_500_for_missing_parent(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối projection có request nhưng thiếu course parent bắt buộc."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        support_view,
        "query_one",
        lambda *_args: request_row(parent_course_id=None),
    )

    def fail_if_queried(*_args, **_kwargs):
        """Bảo đảm thread không được đọc sau lỗi parent projection."""
        pytest.fail("thread was queried for a request with a missing course")

    monkeypatch.setattr(support_view, "query_many", fail_if_queried)

    response = get_request(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    ("authorization", "roles", "expected_status"),
    [(None, None, 401), ("Bearer valid-token", ["STUDENT"], 403)],
)
def test_get_mentor_support_request_rejects_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str] | None,
    expected_status: int,
) -> None:
    """Từ chối thiếu token hoặc role sai trước khi truy cập database."""

    if roles is not None:
        allow_mentor_token(monkeypatch, roles=roles)

    def fail_if_queried(*_args, **_kwargs):
        """Bảo đảm auth thất bại trước khi chạy bất cứ query nào."""
        pytest.fail("database was queried before Mentor authentication")

    monkeypatch.setattr(support_view, "query_one", fail_if_queried)
    monkeypatch.setattr(support_view, "query_many", fail_if_queried)

    response = get_request(client, authorization=authorization)

    assert response.status_code == expected_status


def test_get_mentor_support_request_returns_safe_500_for_unresolved_upload(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không trả response một phần khi link upload thiếu metadata hợp lệ."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(support_view, "query_one", lambda *_args: request_row())
    monkeypatch.setattr(
        support_view,
        "query_many",
        lambda *_args: [message_row(linked_upload_id=34001)],
    )

    response = get_request(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "sql" not in response.text.lower()
    assert session.rollback_count == 1


def test_get_mentor_support_request_rolls_back_query_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả lỗi nội bộ an toàn và rollback khi query DB thất bại."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Mô phỏng lỗi truy vấn SQLAlchemy."""
        raise SQLAlchemyError("private database detail")

    monkeypatch.setattr(support_view, "query_one", fail_query)

    response = get_request(client)

    assert response.status_code == 500
    assert "private database detail" not in response.text
    assert session.rollback_count == 1


def test_get_mentor_support_request_documents_int64_singleton_response(client: TestClient) -> None:
    """OpenAPI mô tả path int64 và data là một object SupportRequest."""

    operation = client.app.openapi()["paths"]["/api/v1/mentor/support/{request_id}"]["get"]
    parameter = next(item for item in operation["parameters"] if item["name"] == "request_id")

    assert parameter["schema"]["type"] == "integer"
    assert parameter["schema"]["format"] == "int64"
    data_schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
    assert data_schema["$ref"].endswith("GetMentorSupportRequestEnvelope")
