from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.mentor.api_58_mentor_support_requests.view as support_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.mentor.api_58_mentor_support_requests.query import (
    FIND_MENTOR_COURSE,
    LIST_MENTOR_SUPPORT_MESSAGES,
    LIST_MENTOR_SUPPORT_REQUESTS,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Theo dõi rollback/commit để kiểm tra API #58 chỉ đọc dữ liệu."""

    def __init__(self) -> None:
        """Khởi tạo bộ đếm commit/rollback cho phiên giả lập."""
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận nếu API commit nhầm trong luồng chỉ đọc."""
        self.commit_count += 1

    def rollback(self) -> None:
        """Ghi nhận rollback khi query hoặc projection lỗi."""
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency trả fake session cho một request test."""

    def dependency():
        """Trả về phiên DB giả lập cho request hiện tại."""
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


def request_row(**overrides: Any) -> dict[str, Any]:
    """Tạo SQL projection hợp lệ cho một support request."""

    return {
        "id": 58001,
        "course_id": 120,
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
    """Tạo SQL projection hợp lệ cho một message không có attachment."""

    return {
        "request_id": 58001,
        "course_id": 120,
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


def get_requests(
    client: TestClient,
    *,
    query: str = "",
    authorization: str | None = "Bearer valid-token",
    headers: dict[str, str] | None = None,
):
    """Gửi GET tới endpoint support-request với token Mentor hợp lệ."""
    request_headers = dict(headers or {})
    if authorization is not None:
        request_headers["Authorization"] = authorization
    return client.get(f"/api/v1/mentor/support/requests{query}", headers=request_headers)


def test_get_mentor_support_requests_returns_collection_with_thread_and_asset(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra collection có thread và UploadAsset theo đúng response schema."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: dict[str, Any] = {"many": []}

    def query_one(_db, query, params):
        """Giả lập truy vấn kiểm tra course ownership."""
        captured["course_query"] = query
        captured["course_params"] = params
        return {"id": 120, "mentor_id": 1001}

    def query_many(_db, query, params):
        """Giả lập truy vấn request và thread bằng các hàng kiểm thử."""
        captured["many"].append((query, params))
        if query == LIST_MENTOR_SUPPORT_REQUESTS:
            return [request_row()]
        assert query == LIST_MENTOR_SUPPORT_MESSAGES
        return [
            message_row(
                linked_upload_id=34001,
                attachment_id=34001,
                attachment_name="guide.pdf",
                attachment_url="https://storage.example/guide.pdf",
                attachment_content_type="application/pdf",
                attachment_size_bytes=4096,
                attachment_status="UPLOADED",
            )
        ]

    monkeypatch.setattr(support_view, "query_one", query_one)
    monkeypatch.setattr(support_view, "query_many", query_many)

    response = get_requests(
        client,
        query="?course_id=120&status=OPEN",
        headers={"X-Trace-Id": "123e4567-e89b-42d3-a456-426614174000"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"][0]["id"] == 58001
    assert payload["data"][0]["student"] == {
        "id": 2042,
        "full_name": "Nguyễn An",
    }
    assert payload["data"][0]["messages"][0]["attachments"] == [
        {
            "id": 34001,
            "name": "guide.pdf",
            "url": "https://storage.example/guide.pdf",
            "content_type": "application/pdf",
            "size_bytes": 4096,
            "status": "UPLOADED",
        }
    ]
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert captured["course_query"] == FIND_MENTOR_COURSE
    assert captured["course_params"] == {"course_id": 120}
    assert captured["many"] == [
        (
            LIST_MENTOR_SUPPORT_REQUESTS,
            {"mentor_id": 1001, "course_id": 120, "status": "OPEN"},
        ),
        (
            LIST_MENTOR_SUPPORT_MESSAGES,
            {"mentor_id": 1001, "course_id": 120, "status": "OPEN"},
        ),
    ]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_mentor_support_requests_returns_empty_array_and_skips_thread_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra kết quả rỗng là mảng và không truy vấn thread."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    called: list[str] = []

    monkeypatch.setattr(support_view, "query_one", lambda *_args: None)

    def query_many(_db, query, _params):
        """Giả lập truy vấn request và thread bằng các hàng kiểm thử."""
        called.append(query)
        assert query == LIST_MENTOR_SUPPORT_REQUESTS
        return []

    monkeypatch.setattr(support_view, "query_many", query_many)

    response = get_requests(client, query="?course_id=999")

    assert response.status_code == 200
    assert response.json()["data"] == []
    assert response.json()["message"] == "No support requests found."
    assert called == [LIST_MENTOR_SUPPORT_REQUESTS]
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_get_mentor_support_requests_rejects_missing_or_malformed_bearer(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Kiểm tra token thiếu hoặc sai bị từ chối trước khi truy vấn DB."""
    def fail_if_queried(*_args, **_kwargs):
        """Báo lỗi nếu luồng auth thất bại vẫn truy cập DB."""
        pytest.fail("database was queried before Mentor authentication")

    monkeypatch.setattr(support_view, "query_one", fail_if_queried)
    monkeypatch.setattr(support_view, "query_many", fail_if_queried)

    response = get_requests(client, authorization=authorization)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert response.json()["data"] is None


def test_get_mentor_support_requests_rejects_non_mentor_role(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra role không phải Mentor nhận lỗi quyền truy cập."""
    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    monkeypatch.setattr(
        support_view,
        "query_one",
        lambda *_args, **_kwargs: pytest.fail("database queried before role check"),
    )

    response = get_requests(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_get_mentor_support_requests_rejects_course_owned_by_another_mentor(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra course của Mentor khác bị từ chối."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        support_view,
        "query_one",
        lambda *_args: {"id": 120, "mentor_id": 2002},
    )
    monkeypatch.setattr(
        support_view,
        "query_many",
        lambda *_args: pytest.fail("support requests read for another Mentor"),
    )

    response = get_requests(client, query="?course_id=120")

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.rollback_count == 1


def test_get_mentor_support_requests_returns_422_for_invalid_course_id(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra course_id sai kiểu hoặc ngoài int64 nhận 422."""
    monkeypatch.setattr(
        support_view,
        "query_many",
        lambda *_args: pytest.fail("database queried for invalid course_id"),
    )

    response = get_requests(client, query="?course_id=9223372036854775808")

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None


def test_get_mentor_support_requests_combines_filters_and_uses_stable_order(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra hai filter kết hợp và thứ tự SQL ổn định."""
    allow_mentor_token(monkeypatch)
    captured: list[tuple[str, dict[str, Any]]] = []

    monkeypatch.setattr(
        support_view,
        "query_one",
        lambda *_args: {"id": 120, "mentor_id": 1001},
    )

    def query_many(_db, query, params):
        """Giả lập truy vấn request và thread bằng các hàng kiểm thử."""
        captured.append((query, params))
        return [request_row()] if query == LIST_MENTOR_SUPPORT_REQUESTS else []

    monkeypatch.setattr(support_view, "query_many", query_many)

    response = get_requests(client, query="?course_id=120&status=OPEN")

    assert response.status_code == 200
    assert captured[0][1] == {"mentor_id": 1001, "course_id": 120, "status": "OPEN"}
    assert "course.mentor_id = :mentor_id" in LIST_MENTOR_SUPPORT_REQUESTS
    assert "request.course_id = :course_id" in LIST_MENTOR_SUPPORT_REQUESTS
    assert "request.status = :status" in LIST_MENTOR_SUPPORT_REQUESTS
    assert "ORDER BY request.created_at DESC, request.id DESC" in LIST_MENTOR_SUPPORT_REQUESTS
    assert "message.created_at ASC NULLS FIRST" in LIST_MENTOR_SUPPORT_MESSAGES


def test_get_mentor_support_requests_returns_safe_500_and_rolls_back_on_database_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra lỗi DB trả 500 an toàn và rollback."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Ném lỗi SQL giả lập để xác minh nhánh xử lý lỗi DB."""
        raise SQLAlchemyError("private database detail")

    monkeypatch.setattr(support_view, "query_many", fail_query)

    response = get_requests(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private database detail" not in response.text
    assert session.rollback_count == 1


def test_get_mentor_support_requests_rejects_broken_asset_link_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra link asset hỏng không tạo response thành công một phần."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(support_view, "query_one", lambda *_args: None)
    monkeypatch.setattr(
        support_view,
        "query_many",
        lambda _db, query, _params: (
            [request_row()]
            if query == LIST_MENTOR_SUPPORT_REQUESTS
            else [message_row(linked_upload_id=34001)]
        ),
    )

    response = get_requests(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.rollback_count == 1


def test_get_mentor_support_requests_openapi_declares_collection_and_int64_filter(
    client: TestClient,
) -> None:
    """Kiểm tra OpenAPI khai báo collection và course_id dạng int64."""
    operation = client.app.openapi()["paths"]["/api/v1/mentor/support/requests"]["get"]
    parameters = {parameter["name"]: parameter for parameter in operation["parameters"]}
    assert parameters["course_id"]["schema"]["format"] == "int64"
    assert parameters["status"]["schema"]["anyOf"][0]["type"] == "string"
    envelope_ref = operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
    envelope_name = envelope_ref.rsplit("/", 1)[-1]
    envelope = client.app.openapi()["components"]["schemas"][envelope_name]
    assert envelope["properties"]["data"]["type"] == "array"
