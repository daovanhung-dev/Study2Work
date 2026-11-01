from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.admin.api_98_admin_discussions_detail.view as detail_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Theo dõi transaction mà API #98 chỉ được rollback khi đọc hoặc ánh xạ lỗi."""

    def __init__(self) -> None:
        """Khởi tạo bộ đếm commit và rollback của request."""

        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Đếm commit nếu route GET vô tình ghi dữ liệu."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Đếm rollback khi query hoặc projection thất bại."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả session giả trong một request."""

    def dependency():
        """Yield session giả cho route API #98."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cấp claims JWT ổn định để kiểm tra ADMIN guard qua HTTP."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def install_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    discussion: dict[str, Any] | None = None,
    comments: list[dict[str, Any]] | None = None,
    failure: str | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query doubles và ghi lại thứ tự truy vấn cùng binding."""

    discussion_row = (
        {
            "id": 701,
            "course_id": 55,
            "content": "  Cần   xem xét\nphản ánh này. ",
            "status": "ACTIVE",
            "author_id": 8,
            "author_full_name": "Nguyễn An",
            "author_avatar_url": "https://example.test/avatar.png",
        }
        if discussion is None
        else discussion
    )
    comment_rows = (
        [
            {
                "id": 702,
                "discussion_id": 701,
                "content": "Phản hồi đầu tiên",
                "created_at": datetime(2026, 10, 26, 8, 30, tzinfo=UTC),
                "author_id": 9,
                "author_full_name": "Minh B",
                "author_avatar_url": None,
            },
            {
                "id": 703,
                "discussion_id": 701,
                "content": "Phản hồi thứ hai",
                "created_at": datetime(2026, 10, 26, 8, 31, tzinfo=UTC),
                "author_id": 10,
                "author_full_name": "Lan C",
                "author_avatar_url": "https://example.test/lan.png",
            },
        ]
        if comments is None
        else comments
    )
    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query, params):
        """Trả Discussion row hoặc phát lỗi đã cấu hình."""

        captured.append((query, dict(params)))
        assert query == detail_view.FIND_ADMIN_DISCUSSION_DETAIL
        if failure == "discussion":
            raise SQLAlchemyError("database detail failure")
        return discussion_row

    def query_many(_db, query, params):
        """Trả các comment trực tiếp hoặc phát lỗi đã cấu hình."""

        captured.append((query, dict(params)))
        assert query == detail_view.LIST_ADMIN_DISCUSSION_DETAIL_COMMENTS
        if failure == "comments":
            raise SQLAlchemyError("database comments failure")
        return comment_rows

    monkeypatch.setattr(detail_view, "query_one", query_one)
    monkeypatch.setattr(detail_view, "query_many", query_many)
    return captured


def detail_response(
    client: TestClient,
    *,
    discussion_id: str = "701",
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP GET API #98 với ID và Authorization tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get(f"/api/v1/admin/discussions/{discussion_id}", headers=headers)


def test_get_admin_discussion_detail_maps_thread_without_report_fields(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả Discussion Page và comment trực tiếp theo source, không dựng dữ liệu report."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_queries(monkeypatch)

    response = detail_response(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    item = payload["data"]["items"][0]
    assert item["title"] == "Cần xem xét phản ánh này."
    assert item["content"] == "  Cần   xem xét\nphản ánh này. "
    assert [comment["id"] for comment in item["comments"]] == [702, 703]
    assert "report" not in item
    assert "reason" not in item
    assert captured == [
        (detail_view.FIND_ADMIN_DISCUSSION_DETAIL, {"discussion_id": 701}),
        (detail_view.LIST_ADMIN_DISCUSSION_DETAIL_COMMENTS, {"discussion_id": 701}),
    ]
    assert "WHERE child.parent_id = :discussion_id" in captured[1][0]
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    ("discussion_id", "expected_status"),
    [("invalid", 404), ("0", 404), ("9223372036854775808", 404)],
)
def test_get_admin_discussion_detail_rejects_invalid_id_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    discussion_id: str,
    expected_status: int,
) -> None:
    """Trả 404 cho ID sai hoặc vượt signed-int64 trước khi gọi database."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_queries(monkeypatch)

    response = detail_response(client, discussion_id=discussion_id)

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert captured == []
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_discussion_detail_checks_admin_before_parsing_or_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối role khác trước khi parse ID hoặc truy vấn dữ liệu."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch, roles=["STUDENT"])
    captured = install_queries(monkeypatch)

    response = detail_response(client, discussion_id="invalid")

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert captured == []
    assert session.rollback_count == 0


def test_get_admin_discussion_detail_requires_bearer_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 401 khi thiếu Bearer token và không truy cập database."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    captured = install_queries(monkeypatch)

    response = detail_response(client, authorization=None)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert captured == []
    assert session.rollback_count == 0


def test_get_admin_discussion_detail_maps_missing_row_without_comment_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 404 cho Discussion không tồn tại và chỉ thực hiện lookup cha."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_queries(monkeypatch, discussion=None)

    def missing_discussion(_db, query, params):
        """Ghi lookup Discussion duy nhất rồi trả về không có hàng."""

        captured.append((query, dict(params)))
        return None

    monkeypatch.setattr(detail_view, "query_one", missing_discussion)

    response = detail_response(client, discussion_id="999999999")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert captured == [(detail_view.FIND_ADMIN_DISCUSSION_DETAIL, {"discussion_id": 999999999})]
    assert session.rollback_count == 0


@pytest.mark.parametrize("failure", ["discussion", "comments"])
def test_get_admin_discussion_detail_rolls_back_query_failures(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    """Trả lỗi 500 an toàn và rollback khi lookup cha hoặc comment thất bại."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_queries(monkeypatch, failure=failure)

    response = detail_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.headers["X-Trace-Id"] == response.json()["traceId"]
    assert session.commit_count == 0
    assert session.rollback_count == 1
