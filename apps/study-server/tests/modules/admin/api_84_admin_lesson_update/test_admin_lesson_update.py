"""HTTP tests cho Admin Lesson update API #84."""

from __future__ import annotations

from typing import Any

import app.modules.admin.api_84_admin_lesson_update.view as lesson_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Đếm transaction calls và có thể giả lập lỗi commit cho API #84."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        """Khởi tạo bộ đếm commit/rollback của session giả."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit hoặc ném lỗi DB đã cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("sensitive commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback khi update hoặc transaction thất bại."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả fake session cho TestClient."""

    def dependency():
        """Cung cấp session giả trong một HTTP request."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cài decoder giả trả JWT Admin có subject ổn định."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def update_body(**overrides: Any) -> dict[str, Any]:
    """Tạo body full-replacement DERIVED với bốn Lesson metadata fields."""

    return {
        "title": "Giới thiệu khóa học",
        "content": "Nội dung bài học mới",
        "video_url": "https://cdn.example.test/lessons/501.mp4",
        "order": 2,
        **overrides,
    }


def lesson_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection Lesson theo aliases của API #09."""

    return {
        "id": 501,
        "course_id": 42,
        "title": "Giới thiệu khóa học",
        "content": "Nội dung bài học mới",
        "video_url": "https://cdn.example.test/lessons/501.mp4",
        "order": 2,
        "status": "DRAFT",
        **overrides,
    }


def put_lesson_response(
    client: TestClient,
    lesson_id: str,
    body: dict[str, Any] | None = None,
    *,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP PUT API #84 với raw path, body và Authorization tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.put(
        f"/api/v1/admin/lessons/{lesson_id}",
        headers=headers,
        json=body if body is not None else update_body(),
    )


def install_update_query(
    monkeypatch: pytest.MonkeyPatch,
    *,
    row: Any = ...,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query double cho UPDATE RETURNING và lưu SQL cùng bind values."""

    result_row = lesson_row() if row is ... else row
    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query, params):
        """Ghi nhận query và trả projection Lesson giả."""

        captured.append((query, dict(params)))
        if query != lesson_view.UPDATE_ADMIN_LESSON_METADATA:
            raise AssertionError("unexpected lesson query")
        return result_row

    monkeypatch.setattr(lesson_view, "query_one", query_one)
    return captured


def test_put_admin_lesson_updates_metadata_and_returns_direct_lesson(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Thay metadata, giữ quan hệ/trạng thái và commit sau projection hợp lệ."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_update_query(
        monkeypatch,
        row=lesson_row(content=None, video_url=None),
    )

    response = put_lesson_response(
        client,
        "000501",
        update_body(content=None, video_url=None),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["data"] == {
        "id": 501,
        "course_id": 42,
        "title": "Giới thiệu khóa học",
        "content": None,
        "video_url": None,
        "order": 2,
        "status": "DRAFT",
    }
    assert payload["meta"] == {}
    assert payload["traceId"] == response.headers["X-Trace-Id"]
    assert captured[0][1] == {
        "lesson_id": 501,
        "title": "Giới thiệu khóa học",
        "content": None,
        "video_url": None,
        "order": 2,
    }
    update_sql = captured[0][0]
    assert "name = :title" in update_sql
    assert "content = :content" in update_sql
    assert "video_url = :video_url" in update_sql
    assert "sort_order = :order" in update_sql
    assert "updated_at = CURRENT_TIMESTAMP" in update_sql
    assert "l.status IS DISTINCT FROM 'DELETED'" in update_sql
    assert "status =" not in update_sql
    assert "course_id =" not in update_sql
    assert "lesson_uploads" not in update_sql
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    ("authorization", "roles", "expected_status", "expected_code"),
    [
        (None, None, 401, "DESIGN_AUTHENTICATION_REQUIRED"),
        ("Bearer valid-token", ["STUDENT"], 403, "DESIGN_ACCESS_DENIED"),
    ],
)
def test_put_admin_lesson_checks_auth_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str] | None,
    expected_status: int,
    expected_code: str,
) -> None:
    """Thiếu credential hoặc role Admin trả lỗi mà không truy vấn DB."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    if roles is not None:
        allow_admin_token(monkeypatch, roles=roles)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu mutation chạy trước authorization."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(lesson_view, "query_one", fail_query)

    response = put_lesson_response(
        client,
        "not-an-int64",
        authorization=authorization,
    )

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code
    assert response.json()["data"] is None


@pytest.mark.parametrize(
    "lesson_id",
    ["not-an-id", "9223372036854775808", "-9223372036854775809", "1" * 21],
)
def test_put_admin_lesson_maps_invalid_int64_path_to_422_without_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    lesson_id: str,
) -> None:
    """Map path sai/out-of-range thành catalog 422 và không chạm database."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu path không hợp lệ vẫn chạy UPDATE."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(lesson_view, "query_one", fail_query)

    response = put_lesson_response(client, lesson_id)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "lesson_id"


@pytest.mark.parametrize(
    "body",
    [
        update_body(title="T" * 201),
        update_body(title=42),
        update_body(content=42),
        update_body(video_url=42),
        update_body(order=2**31),
        {"title": "Lesson", "content": None, "video_url": None},
        update_body(unexpected="field"),
    ],
)
def test_put_admin_lesson_rejects_invalid_body_without_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: dict[str, Any],
) -> None:
    """Từ chối body thiếu/thừa field, sai strict type hoặc ngoài giới hạn candidate."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu body sai vẫn chạy mutation."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(lesson_view, "query_one", fail_query)

    response = put_lesson_response(client, "501", body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None


def test_put_admin_lesson_returns_404_when_update_has_no_row(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map UPDATE RETURNING rỗng thành 404 và rollback transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_update_query(monkeypatch, row=None)

    response = put_lesson_response(client, "501")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None
    assert captured[0][1]["lesson_id"] == 501
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_put_admin_lesson_maps_query_error_to_safe_500_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """SQL exception trả lỗi an toàn và rollback transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def raise_query_error(*_args, **_kwargs):
        """Tạo lỗi SQL giả có chi tiết nhạy cảm để kiểm tra response."""

        raise SQLAlchemyError("sensitive SQL detail")

    monkeypatch.setattr(lesson_view, "query_one", raise_query_error)

    response = put_lesson_response(client, "501")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "sensitive SQL detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    "overrides",
    [
        {"course_id": None},
        {"title": None},
        {"order": None},
        {"status": None},
        {"id": 502},
    ],
)
def test_put_admin_lesson_rejects_incomplete_or_mismatched_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    overrides: dict[str, Any],
) -> None:
    """Projection sai Lesson contract rollback và trả 500 an toàn."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_update_query(monkeypatch, row=lesson_row(**overrides))

    response = put_lesson_response(client, "501")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_put_admin_lesson_maps_commit_error_to_safe_500_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Commit lỗi trả lỗi nội bộ an toàn và gọi rollback."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_update_query(monkeypatch)

    response = put_lesson_response(client, "501")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "sensitive commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_put_admin_lesson_openapi_declares_full_replacement_body(client: TestClient) -> None:
    """OpenAPI exposes the selected DERIVED body and direct Lesson response."""

    openapi = client.app.openapi()
    operation = openapi["paths"][
        "/api/v1/admin/lessons/{lesson_id}"
    ]["put"]

    assert "requestBody" in operation
    request_schema = operation["requestBody"]["content"]["application/json"]["schema"]
    schema_name = request_schema["$ref"].rsplit("/", maxsplit=1)[-1]
    schema = openapi["components"]["schemas"][schema_name]
    assert set(schema["required"]) == {"title", "content", "video_url", "order"}
    assert schema["additionalProperties"] is False
    assert operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "UpdateAdminLessonEnvelope"
    )
