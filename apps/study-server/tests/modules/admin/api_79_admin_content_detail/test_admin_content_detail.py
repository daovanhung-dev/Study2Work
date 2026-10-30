from __future__ import annotations

from typing import Any

import app.modules.admin.api_78_admin_content_pending.view as pending_view
import app.modules.admin.api_79_admin_content_detail.view as detail_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

_DEFAULT_ROW = object()


class FakeSession:
    """Session giả để kiểm tra API #79 chỉ đọc và rollback lỗi."""

    def __init__(self) -> None:
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Đếm commit nếu handler đọc vô tình sửa database."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Đếm rollback trên lỗi query hoặc mapping."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả fake session cho TestClient."""

    def dependency():
        """Yield session giả dùng trong một HTTP request."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Thay decoder để cấp JWT Admin có subject số ổn định trong test."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def content_row(**overrides: Any) -> dict[str, Any]:
    """Tạo row detail hợp lệ theo legacy contents candidate."""

    return {
        "id": 901,
        "course_id": 501,
        "content_type": "QUIZ",
        "title": "Reviewable quiz",
        "payload": {"question_count": 4},
        "status": "PUBLISHED",
        "parent_id": None,
        "order": 2,
        **overrides,
    }


def install_detail_query(
    monkeypatch: pytest.MonkeyPatch,
    *,
    row: Any = _DEFAULT_ROW,
    error: Exception | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query double và lưu SQL/parameters của lookup detail."""

    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query, params):
        """Trả row giả hoặc raise lỗi sau khi capture câu SQL và binding."""

        captured.append((query, dict(params)))
        if query != detail_view.FIND_ADMIN_CONTENT:
            raise AssertionError("unexpected content query")
        if error is not None:
            raise error
        return content_row() if row is _DEFAULT_ROW else row

    monkeypatch.setattr(detail_view, "query_one", query_one)
    return captured


def get_detail(
    client: TestClient,
    *,
    content_id: str = "901",
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP GET API #79 với path/header tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get(f"/api/v1/admin/content/{content_id}", headers=headers)


def test_get_admin_content_returns_current_content_projection_read_only(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả object Content trực tiếp, status hiện tại và không ghi database."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_detail_query(monkeypatch, row=content_row(status="PUBLISHED"))

    response = get_detail(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"] == {
        "id": 901,
        "course_id": 501,
        "content_type": "QUIZ",
        "title": "Reviewable quiz",
        "payload": {"question_count": 4},
        "status": "PUBLISHED",
        "parent_id": None,
        "order": 2,
    }
    assert captured == [(detail_view.FIND_ADMIN_CONTENT, {"content_id": 901})]
    assert "WHERE id = :content_id" in captured[0][0]
    assert "deleted_at IS NULL" in captured[0][0]
    assert "AND status =" not in captured[0][0]
    assert payload["traceId"] == response.headers["X-Trace-Id"]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_content_authenticates_before_invalid_path_or_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Thiếu Bearer trả 401 trước path parse và DB access."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())

    def fail_query(*_args, **_kwargs):
        """Báo lỗi nếu unauthenticated request chạm database."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(detail_view, "query_one", fail_query)

    response = get_detail(client, content_id="not-an-int", authorization=None)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


@pytest.mark.parametrize("content_id", ["invalid", "9223372036854775808", "-9223372036854775809"])
def test_get_admin_content_maps_invalid_int64_path_to_catalog_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    content_id: str,
) -> None:
    """Malformed hoặc overflow signed-int64 path trả 404 trước DB."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Báo lỗi nếu invalid path tiếp tục tới database."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(detail_view, "query_one", fail_query)

    response = get_detail(client, content_id=content_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_admin_content_returns_404_for_missing_or_soft_deleted_row(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không có active row dùng catalog 404 và dọn read transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_detail_query(monkeypatch, row=None)

    response = get_detail(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert "deleted_at IS NULL" in captured[0][0]
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_content_returns_safe_500_and_rolls_back_query_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """SQLAlchemy error trả 500 an toàn và rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_detail_query(monkeypatch, error=SQLAlchemyError("private database detail"))

    response = get_detail(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private database detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    "row",
    [
        content_row(id=902),
        content_row(payload=["not", "an", "object"]),
        content_row(title=None),
        {"id": 901},
    ],
)
def test_get_admin_content_rejects_malformed_projection_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    row: dict[str, Any],
) -> None:
    """Sai ID hoặc row/payload không đạt Content contract trả safe 500."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_detail_query(monkeypatch, row=row)

    response = get_detail(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_static_pending_route_keeps_precedence_over_dynamic_detail_route(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Route cố định API #78 vẫn xử lý /pending sau khi thêm API #79 dynamic path."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def count_pending(_db, _query, _params):
        """Trả count rỗng cho route queue trong regression precedence."""

        return {"total": 0}

    def list_pending(_db, _query, _params):
        """Trả danh sách rỗng cho route queue trong regression precedence."""

        return []

    monkeypatch.setattr(pending_view, "query_one", count_pending)
    monkeypatch.setattr(pending_view, "query_many", list_pending)

    response = client.get(
        "/api/v1/admin/content/pending",
        headers={"Authorization": "Bearer valid-admin-token"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["items"] == []
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"


def test_admin_content_openapi_matches_catalog(
    client: TestClient,
) -> None:
    """OpenAPI mô tả signed-int64 path, Content envelope và đúng direct error set."""

    operation = client.app.openapi()["paths"]["/api/v1/admin/content/{content_id}"]["get"]
    parameters = {
        (item["name"], item["in"]): item
        for item in operation["parameters"]
    }

    assert parameters[("content_id", "path")]["required"] is True
    assert parameters[("content_id", "path")]["schema"]["format"] == "int64"
    assert parameters[("Authorization", "header")]["required"] is True
    assert operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "/GetAdminContentEnvelope"
    )
    assert {"401", "403", "404", "500"}.issubset(operation["responses"])
    assert "422" not in operation["responses"]
