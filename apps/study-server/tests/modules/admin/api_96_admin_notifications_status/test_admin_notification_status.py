from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.admin.api_96_admin_notifications_status.view as status_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

_USE_DEFAULT_ROW = object()


class FakeSession:
    """Session giả để xác minh API #96 chỉ đọc và rollback lỗi."""

    def __init__(self) -> None:
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Đếm commit nếu GET vô tình ghi dữ liệu."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Đếm rollback nếu query hoặc projection thất bại."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả session giả cho một request."""

    def dependency():
        """Yield fake session từ dependency database."""

        yield session

    return dependency


def allow_admin_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Thay decoder để cấp JWT Admin có subject số trong test."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": ["ADMIN"]},
    )


def notification_row(**overrides: Any) -> dict[str, Any]:
    """Tạo Notification projection theo local API #92 fallback."""

    return {
        "id": 501,
        "title": "Thông báo lịch học",
        "content": "Lịch học được cập nhật.",
        "channels": ["EMAIL", "PUSH"],
        "status": "QUEUED",
        "created_at": datetime(2026, 10, 26, 8, 30, tzinfo=UTC),
        **overrides,
    }


def install_query_result(
    monkeypatch: pytest.MonkeyPatch,
    *,
    row: Any = _USE_DEFAULT_ROW,
    failure: SQLAlchemyError | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query double và ghi nhận SQL cùng bindings."""

    result_row = notification_row() if row is _USE_DEFAULT_ROW else row
    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query, params):
        """Trả row giả hoặc phát database error cấu hình trong test."""

        captured.append((query, dict(params)))
        if query != status_view.FIND_ADMIN_NOTIFICATION_STATUS:
            raise AssertionError("unexpected status query")
        if failure is not None:
            raise failure
        return result_row

    monkeypatch.setattr(status_view, "query_one", query_one)
    return captured


def get_status_response(
    client: TestClient,
    notification_id: str = "501",
    *,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi GET API #96 với raw path và header tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get(
        f"/api/v1/admin/notifications/{notification_id}/status",
        headers=headers,
    )


def test_get_admin_notification_status_returns_notification_and_is_read_only(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả Notification hiện hữu với channels/status, không thêm delivery counts."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_result(monkeypatch)

    response = get_status_response(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"] == {
        "id": 501,
        "title": "Thông báo lịch học",
        "content": "Lịch học được cập nhật.",
        "channels": ["EMAIL", "PUSH"],
        "status": "QUEUED",
        "created_at": "2026-10-26T08:30:00Z",
    }
    assert "queued" not in payload["data"]
    assert "sent" not in payload["data"]
    assert "failed" not in payload["data"]
    assert len(captured) == 1
    assert captured[0][1] == {"notification_id": 501}
    assert "FROM notifications AS n" in captured[0][0]
    assert "FROM notification_deliveries AS d" in captured[0][0]
    assert "WHEN ds.queued_count > 0 THEN 'QUEUED'" in captured[0][0]
    assert "WHEN ds.failed_count > 0 THEN 'FAILED'" in captured[0][0]
    assert "WHEN ds.sent_count = ds.delivery_count THEN 'SENT'" in captured[0][0]
    assert "ARRAY_AGG(d.channel ORDER BY d.channel)" in captured[0][0]
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize("status_value", ["QUEUED", "FAILED", "SENT"])
def test_get_admin_notification_status_maps_supported_delivery_states(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    status_value: str,
) -> None:
    """Cho phép đúng ba status token đã dùng bởi aggregate API #92."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)
    install_query_result(monkeypatch, row=notification_row(status=status_value))

    response = get_status_response(client)

    assert response.status_code == 200
    assert response.json()["data"]["status"] == status_value


@pytest.mark.parametrize("notification_id", ["0", "-1", "9223372036854775808", "1.5", "abc"])
def test_get_admin_notification_status_maps_invalid_id_to_catalog_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    notification_id: str,
) -> None:
    """Trả 404 cho path không phải signed-int64 dương và không query DB."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    response = get_status_response(client, notification_id)

    assert response.status_code == 404
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert payload["data"] is None
    assert payload["meta"] == {}


def test_get_admin_notification_status_authenticates_before_invalid_path_or_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả auth error trước ID parsing hoặc khi không có quyền Admin."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": ["MENTOR"]},
    )
    captured = install_query_result(monkeypatch)

    response = get_status_response(client, "not-an-id")

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert captured == []
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_notification_status_requires_authentication_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 401 khi thiếu Bearer token mà không chạy query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    captured = install_query_result(monkeypatch)

    response = get_status_response(client, authorization=None)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert captured == []
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_notification_status_returns_404_when_notification_or_delivery_is_absent(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Dùng 404 cho lookup rỗng, gồm notification chưa có delivery status."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)
    install_query_result(monkeypatch, row=None)

    response = get_status_response(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_admin_notification_status_returns_safe_500_and_rolls_back_query_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ẩn chi tiết SQL, rollback query failure và không commit GET."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_query_result(monkeypatch, failure=SQLAlchemyError("private database detail"))

    response = get_status_response(client)

    assert response.status_code == 500
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert payload["data"] is None
    assert payload["meta"] == {}
    assert "private database detail" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    "projection",
    [{"status": "UNKNOWN"}, {"channels": ["EMAIL", "EMAIL"]}],
)
def test_get_admin_notification_status_returns_500_for_invalid_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    projection: dict[str, Any],
) -> None:
    """Không trả response nếu aggregate không khớp Notification schema."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_query_result(monkeypatch, row=notification_row(**projection))

    response = get_status_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_admin_notification_status_openapi_matches_catalog_contract(client: TestClient) -> None:
    """Khai báo đúng path/header, success schema và error set catalog."""

    operation = client.app.openapi()["paths"][
        "/api/v1/admin/notifications/{notification_id}/status"
    ]["get"]

    assert operation["parameters"] == [
        {
            "name": "notification_id",
            "in": "path",
            "required": True,
            "schema": {
                "type": "integer",
                "format": "int64",
                "minimum": 1,
                "maximum": 9223372036854775807,
            },
        },
        {
            "name": "Authorization",
            "in": "header",
            "required": True,
            "schema": {"type": "string"},
        },
    ]
    assert set(operation["responses"]) == {"200", "401", "403", "404", "500"}
    assert {
        code: operation["responses"][code]["description"] for code in ("401", "403", "404", "500")
    } == {
        "401": "DESIGN_AUTHENTICATION_REQUIRED",
        "403": "DESIGN_ACCESS_DENIED",
        "404": "DESIGN_RESOURCE_NOT_FOUND",
        "500": "DESIGN_INTERNAL_ERROR",
    }
    envelope_ref = operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
    assert envelope_ref.endswith("GetAdminNotificationStatusEnvelope")
    envelope_name = envelope_ref.rsplit("/", maxsplit=1)[-1]
    data_schema = client.app.openapi()["components"]["schemas"][envelope_name]["properties"]["data"]
    assert data_schema["$ref"].endswith("AdminNotificationResponse")
    assert "requestBody" not in operation
