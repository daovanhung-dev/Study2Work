from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.mentor.api_60_mentor_support_reply.view as reply_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.mentor.api_59_mentor_support_request_detail.query import (
    LIST_MENTOR_SUPPORT_REQUEST_MESSAGES,
)
from app.modules.mentor.api_60_mentor_support_reply.query import (
    FIND_REPLY_UPLOADS,
    INSERT_MENTOR_SUPPORT_MESSAGE,
    INSERT_MENTOR_SUPPORT_MESSAGE_UPLOADS,
    LOCK_MENTOR_SUPPORT_REQUEST_FOR_REPLY,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Theo dõi commit/rollback của mutation API #60."""

    def __init__(self, *, commit_error: bool = False) -> None:
        """Khởi tạo bộ đếm giao dịch và lỗi commit tùy chọn."""
        self.commit_count = 0
        self.rollback_count = 0
        self.commit_error = commit_error

    def commit(self) -> None:
        """Ghi nhận commit sau khi response projection hợp lệ."""
        self.commit_count += 1
        if self.commit_error:
            raise SQLAlchemyError("private commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback khi request không thể hoàn tất."""
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency trả fake session cho một HTTP request."""

    def dependency():
        """Yield session giả lập."""
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
    """Tạo parent projection hợp lệ cho SupportRequest và các FK cha."""

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
    """Tạo row thread hợp lệ, mặc định là reply Mentor không đính kèm."""

    return {
        "request_id": 59001,
        "course_id": 120,
        "parent_course_id": 120,
        "mentor_id": 1001,
        "message_id": 90002,
        "author_id": 1001,
        "author_user_id": 1001,
        "author_role": "MENTOR",
        "author_full_name": "Trần Mentor",
        "author_avatar_url": None,
        "content": "Mình đã gửi hướng dẫn.",
        "message_created_at": datetime(2026, 10, 25, 9, 0, tzinfo=UTC),
        "linked_upload_id": None,
        "attachment_id": None,
        "attachment_name": None,
        "attachment_url": None,
        "attachment_content_type": None,
        "attachment_size_bytes": None,
        "attachment_status": None,
        **overrides,
    }


def post_reply(
    client: TestClient,
    *,
    request_id: str = "59001",
    body: dict[str, Any] | None = None,
    authorization: str | None = "Bearer valid-token",
):
    """Gửi POST API #60 với body và token mặc định."""

    headers = {} if authorization is None else {"Authorization": authorization}
    return client.post(
        f"/api/v1/mentor/support/{request_id}/reply",
        json=body or {"message": "Mình đã gửi hướng dẫn.", "attachment_refs": "[]"},
        headers=headers,
    )


def test_reply_returns_updated_request_and_commits_after_thread_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả thread đã có reply và chỉ commit sau projection thành công."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    query_one_calls: list[tuple[str, dict[str, Any]]] = []
    query_many_calls: list[tuple[str, dict[str, Any]]] = []
    created_at = datetime(2026, 10, 25, 9, 0, tzinfo=UTC)

    def query_one(_db, query, params):
        query_one_calls.append((query, params))
        if query == LOCK_MENTOR_SUPPORT_REQUEST_FOR_REPLY:
            return request_row()
        assert query == INSERT_MENTOR_SUPPORT_MESSAGE
        return {
            "id": 90002,
            "request_id": 59001,
            "author_id": 1001,
            "content": "Mình đã gửi hướng dẫn.",
            "created_at": created_at,
        }

    def query_many(_db, query, params):
        query_many_calls.append((query, params))
        assert query == LIST_MENTOR_SUPPORT_REQUEST_MESSAGES
        return [message_row(message_created_at=created_at)]

    monkeypatch.setattr(reply_view, "query_one", query_one)
    monkeypatch.setattr(reply_view, "query_many", query_many)

    response = post_reply(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["data"]["status"] == "OPEN"
    assert [item["id"] for item in payload["data"]["messages"]] == [90002]
    assert payload["data"]["messages"][0]["content"] == "Mình đã gửi hướng dẫn."
    assert payload["data"]["messages"][0]["attachments"] == []
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert query_one_calls == [
        (LOCK_MENTOR_SUPPORT_REQUEST_FOR_REPLY, {"request_id": 59001}),
        (
            INSERT_MENTOR_SUPPORT_MESSAGE,
            {
                "request_id": 59001,
                "mentor_id": 1001,
                "message": "Mình đã gửi hướng dẫn.",
            },
        ),
    ]
    assert query_many_calls == [
        (
            LIST_MENTOR_SUPPORT_REQUEST_MESSAGES,
            {"request_id": 59001, "mentor_id": 1001},
        )
    ]
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_reply_resolves_and_links_ordered_assets(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Resolve asset ID theo scope, ghi vị trí và trả attachment theo request order."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    created_at = datetime(2026, 10, 25, 9, 0, tzinfo=UTC)

    def query_one(_db, query, _params):
        if query == LOCK_MENTOR_SUPPORT_REQUEST_FOR_REPLY:
            return request_row()
        assert query == INSERT_MENTOR_SUPPORT_MESSAGE
        return {
            "id": 90002,
            "request_id": 59001,
            "author_id": 1001,
            "content": "Mình đã gửi hướng dẫn.",
            "created_at": created_at,
        }

    def query_many(_db, query, params):
        if query == FIND_REPLY_UPLOADS:
            assert params == {"asset_ids": [41002, 41001], "mentor_id": 1001, "course_id": 120}
            return [
                {
                    "id": 41001,
                    "name": "first.pdf",
                    "url": "https://storage.example/first.pdf",
                    "content_type": "application/pdf",
                    "size_bytes": 2048,
                    "status": "UPLOADED",
                },
                {
                    "id": 41002,
                    "name": "second.pdf",
                    "url": "https://storage.example/second.pdf",
                    "content_type": "application/pdf",
                    "size_bytes": 4096,
                    "status": "UPLOADED",
                },
            ]
        if query == INSERT_MENTOR_SUPPORT_MESSAGE_UPLOADS:
            assert params == {"message_id": 90002, "asset_ids": [41002, 41001]}
            return [
                {"upload_id": 41001, "asset_position": 1},
                {"upload_id": 41002, "asset_position": 0},
            ]
        assert query == LIST_MENTOR_SUPPORT_REQUEST_MESSAGES
        return [
            message_row(
                message_created_at=created_at,
                linked_upload_id=41002,
                attachment_id=41002,
                attachment_name="second.pdf",
                attachment_url="https://storage.example/second.pdf",
                attachment_content_type="application/pdf",
                attachment_size_bytes=4096,
                attachment_status="UPLOADED",
            ),
            message_row(
                message_created_at=created_at,
                linked_upload_id=41001,
                attachment_id=41001,
                attachment_name="first.pdf",
                attachment_url="https://storage.example/first.pdf",
                attachment_content_type="application/pdf",
                attachment_size_bytes=2048,
                attachment_status="UPLOADED",
            ),
        ]

    monkeypatch.setattr(reply_view, "query_one", query_one)
    monkeypatch.setattr(reply_view, "query_many", query_many)

    response = post_reply(
        client,
        body={"message": "Mình đã gửi hướng dẫn.", "attachment_refs": "[41002,41001]"},
    )

    assert response.status_code == 200
    assert [
        asset["id"] for asset in response.json()["data"]["messages"][0]["attachments"]
    ] == [41002, 41001]
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize("request_id", ["abc", "9223372036854775808", "-9223372036854775809"])
def test_reply_rejects_invalid_int64_path_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    request_id: str,
) -> None:
    """Map path sai format hoặc overflow thành 422 trước mọi query."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        reply_view,
        "query_one",
        lambda *_args, **_kwargs: pytest.fail("database queried for invalid request_id"),
    )

    response = post_reply(client, request_id=request_id)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "request_id"


@pytest.mark.parametrize(
    ("body", "field"),
    [
        ({"message": "  ", "attachment_refs": "[]"}, "message"),
        ({"message": "reply", "attachment_refs": "not-json"}, "attachment_refs"),
        ({"message": "reply", "attachment_refs": "[1,1]"}, "attachment_refs"),
        ({"message": "reply", "attachment_refs": "[true]"}, "attachment_refs"),
        ({"message": "reply", "attachment_refs": "[1.5]"}, "attachment_refs"),
    ],
)
def test_reply_rejects_invalid_message_or_attachment_refs_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: dict[str, Any],
    field: str,
) -> None:
    """Từ chối message/ref sai quy tắc đã chọn trước khi lock request."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        reply_view,
        "query_one",
        lambda *_args, **_kwargs: pytest.fail("database queried for invalid request body"),
    )

    response = post_reply(client, body=body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == field


def test_reply_framework_validation_uses_design_business_code(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Body sai kiểu vẫn trả đúng validation business code của catalog."""

    allow_mentor_token(monkeypatch)
    response = post_reply(
        client,
        body={"message": 123, "attachment_refs": "[]"},
    )
    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"


@pytest.mark.parametrize(
    ("row", "status", "code"),
    [
        (None, 404, "DESIGN_RESOURCE_NOT_FOUND"),
        (request_row(mentor_id=2002), 403, "DESIGN_ACCESS_DENIED"),
        (request_row(parent_course_id=None), 500, "DESIGN_INTERNAL_ERROR"),
    ],
)
def test_reply_classifies_missing_owner_and_broken_parent(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    row: dict[str, Any] | None,
    status: int,
    code: str,
) -> None:
    """Phân biệt request thiếu, khác owner và parent projection hỏng."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(reply_view, "query_one", lambda *_args: row)

    response = post_reply(client)

    assert response.status_code == status
    assert response.json()["businessCode"] == code
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_reply_returns_404_for_out_of_scope_upload_without_inserting(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không insert reply nếu một asset ref không resolve theo owner/course."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(reply_view, "query_one", lambda *_args: request_row())

    def query_many(_db, query, _params):
        assert query == FIND_REPLY_UPLOADS
        return []

    monkeypatch.setattr(reply_view, "query_many", query_many)

    response = post_reply(
        client,
        body={"message": "reply", "attachment_refs": "[41001]"},
    )

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_reply_rolls_back_partial_asset_links(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback toàn bộ message nếu số link trả về không đủ."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    created_at = datetime(2026, 10, 25, 9, 0, tzinfo=UTC)

    def query_one(_db, query, _params):
        if query == LOCK_MENTOR_SUPPORT_REQUEST_FOR_REPLY:
            return request_row()
        return {
            "id": 90002,
            "request_id": 59001,
            "author_id": 1001,
            "content": "reply",
            "created_at": created_at,
        }

    def query_many(_db, query, _params):
        if query == FIND_REPLY_UPLOADS:
            return [
                {
                    "id": 41001,
                    "name": "a.pdf",
                    "url": "https://storage.example/a.pdf",
                    "content_type": "application/pdf",
                    "size_bytes": 1,
                    "status": "UPLOADED",
                },
                {
                    "id": 41002,
                    "name": "b.pdf",
                    "url": "https://storage.example/b.pdf",
                    "content_type": "application/pdf",
                    "size_bytes": 2,
                    "status": "UPLOADED",
                },
            ]
        assert query == INSERT_MENTOR_SUPPORT_MESSAGE_UPLOADS
        return [{"upload_id": 41001, "asset_position": 0}]

    monkeypatch.setattr(reply_view, "query_one", query_one)
    monkeypatch.setattr(reply_view, "query_many", query_many)

    response = post_reply(
        client,
        body={"message": "reply", "attachment_refs": "[41001,41002]"},
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_reply_rolls_back_when_thread_projection_does_not_include_inserted_message(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không commit nếu full-thread read-back thiếu message vừa insert."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    created_at = datetime(2026, 10, 25, 9, 0, tzinfo=UTC)
    monkeypatch.setattr(
        reply_view,
        "query_one",
        lambda _db, query, _params: request_row()
        if query == LOCK_MENTOR_SUPPORT_REQUEST_FOR_REPLY
        else {
            "id": 90002,
            "request_id": 59001,
            "author_id": 1001,
            "content": "Mình đã gửi hướng dẫn.",
            "created_at": created_at,
        },
    )
    monkeypatch.setattr(
        reply_view,
        "query_many",
        lambda *_args: [message_row(message_id=90003)] ,
    )

    response = post_reply(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_reply_rolls_back_database_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DB exception during request lock returns safe 500 and rolls back."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)

    def fail_lookup(*_args, **_kwargs):
        raise SQLAlchemyError("private SQL detail")

    monkeypatch.setattr(reply_view, "query_one", fail_lookup)

    response = post_reply(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private SQL detail" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_reply_rolls_back_when_commit_fails_and_keeps_error_safe(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Commit lỗi trả 500 an toàn và gọi rollback."""

    session = FakeSession(commit_error=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    created_at = datetime(2026, 10, 25, 9, 0, tzinfo=UTC)
    monkeypatch.setattr(
        reply_view,
        "query_one",
        lambda _db, query, _params: request_row()
        if query == LOCK_MENTOR_SUPPORT_REQUEST_FOR_REPLY
        else {
            "id": 90002,
            "request_id": 59001,
            "author_id": 1001,
            "content": "Mình đã gửi hướng dẫn.",
            "created_at": created_at,
        },
    )
    monkeypatch.setattr(
        reply_view,
        "query_many",
        lambda _db, query, _params: [message_row(message_created_at=created_at)]
        if query == LIST_MENTOR_SUPPORT_REQUEST_MESSAGES
        else pytest.fail("unexpected query for empty attachments"),
    )

    response = post_reply(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_reply_rejects_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Token thiếu hoặc role khác không được phép chạm database."""

    monkeypatch.setattr(
        reply_view,
        "query_one",
        lambda *_args, **_kwargs: pytest.fail("database queried before Mentor auth"),
    )
    response = post_reply(client, authorization=None)
    assert response.status_code == 401

    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    response = post_reply(client)
    assert response.status_code == 403


def test_reply_route_exposes_int64_path_and_request_schema(client: TestClient) -> None:
    """OpenAPI công bố request body và signed-int64 path cho API #60."""

    operation = client.app.openapi()["paths"]["/api/v1/mentor/support/{request_id}/reply"]["post"]
    path_parameter = next(item for item in operation["parameters"] if item["name"] == "request_id")
    body_schema = operation["requestBody"]["content"]["application/json"]["schema"]

    assert path_parameter["schema"]["type"] == "integer"
    assert path_parameter["schema"]["format"] == "int64"
    assert body_schema["$ref"].endswith("ReplyToMentorSupportRequest")
    schema_name = body_schema["$ref"].split("/")[-1]
    request_model = client.app.openapi()["components"]["schemas"][schema_name]
    assert request_model["required"] == ["message", "attachment_refs"]
