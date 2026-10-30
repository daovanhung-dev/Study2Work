"""HTTP tests cho API #75 cập nhật metadata khóa học Admin."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import app.modules.admin.api_75_admin_course_update.view as course_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

_DEFAULT_DETAIL = object()


class FakeSession:
    """Đếm transaction calls và giả lập commit failure cho API #75."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        """Khởi tạo transaction counters và trạng thái lỗi commit."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát sinh lỗi DB đã cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("sensitive commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback do lỗi hoặc không tìm thấy course."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả session giả cho TestClient."""

    def dependency():
        """Yield session test cho dependency get_db."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cài decoder giả trả JWT Admin hoặc role test được chỉ định."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def update_body(**overrides: Any) -> dict[str, Any]:
    """Tạo body full-replacement DERIVED với bốn field metadata."""

    return {
        "title": "Linear Algebra II",
        "description": "Updated course description",
        "thumbnail_url": "https://example.test/course.png",
        "price": "199.00",
        **overrides,
    }


def course_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection Course/mentor candidate tương ứng API #74."""

    return {
        "id": 11,
        "title": "Linear Algebra II",
        "description": "Updated course description",
        "thumbnail_url": "https://example.test/course.png",
        "price": Decimal("199.00"),
        "status": "SUSPENDED",
        "mentor_id": 501,
        "mentor_full_name": "Ada Lovelace",
        "mentor_avatar_url": None,
        **overrides,
    }


def put_course_response(
    client: TestClient,
    course_id: str,
    body: dict[str, Any] | None = None,
    *,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP PUT API #75 với raw path, body và Authorization tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.put(
        f"/api/v1/admin/courses/{course_id}",
        headers=headers,
        json=body if body is not None else update_body(),
    )


def install_update_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    update_row: dict[str, Any] | None = None,
    detail_row: dict[str, Any] | None | object = _DEFAULT_DETAIL,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query double cho UPDATE/RETURNING và SELECT detail; lưu bind parameters."""

    captured: list[tuple[str, dict[str, Any]]] = []
    returned_update = {"id": 11} if update_row is None else update_row
    returned_detail = course_row() if detail_row is _DEFAULT_DETAIL else detail_row

    def query_one(_db, query, params):
        """Trả từng projection theo thứ tự UPDATE rồi Course detail."""

        captured.append((query, dict(params)))
        if query.lstrip().startswith("UPDATE"):
            return returned_update
        return returned_detail

    monkeypatch.setattr(course_view, "query_one", query_one)
    return captured


def test_put_admin_course_updates_only_metadata_and_returns_course_page(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cập nhật metadata, giữ status/mentor và commit sau mapping thành công."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_update_queries(
        monkeypatch,
        detail_row=course_row(
            description=None,
            thumbnail_url=None,
            price=Decimal("199.90"),
        ),
    )

    response = put_course_response(
        client,
        "11",
        update_body(description=None, thumbnail_url=None, price="199.90"),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["data"]["pagination"] == {
        "page": 1,
        "size": 1,
        "total": 1,
        "total_pages": 1,
    }
    assert payload["data"]["items"] == [
        {
            "id": 11,
            "title": "Linear Algebra II",
            "description": None,
            "thumbnail_url": None,
            "price": "199.90",
            "status": "SUSPENDED",
            "mentor": {
                "id": 501,
                "full_name": "Ada Lovelace",
                "avatar_url": None,
            },
        }
    ]
    assert captured[0][1] == {
        "course_id": 11,
        "title": "Linear Algebra II",
        "description": None,
        "thumbnail_url": None,
        "price": Decimal("199.90"),
    }
    update_sql = captured[0][0]
    assert "name = :title" in update_sql
    assert "updated_at = CURRENT_TIMESTAMP" in update_sql
    assert "status =" not in update_sql
    assert "mentor_id =" not in update_sql
    assert captured[1][1] == {"course_id": 11}
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    ("authorization", "roles", "expected_status", "expected_code"),
    [
        (None, None, 401, "DESIGN_AUTHENTICATION_REQUIRED"),
        ("Bearer valid-token", ["STUDENT"], 403, "DESIGN_ACCESS_DENIED"),
    ],
)
def test_put_admin_course_checks_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str] | None,
    expected_status: int,
    expected_code: str,
) -> None:
    """Trả 401/403 và không mutation khi caller chưa qua shared ADMIN guard."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    if roles is not None:
        allow_admin_token(monkeypatch, roles=roles)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu query chạy trước khi xác thực role."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(course_view, "query_one", fail_query)

    response = put_course_response(client, "11", authorization=authorization)

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code
    assert response.json()["data"] is None


@pytest.mark.parametrize(
    "course_id",
    ["not-an-id", "9223372036854775808", "-9223372036854775809", "1" * 21],
)
def test_put_admin_course_maps_invalid_int64_to_catalog_422_without_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    course_id: str,
) -> None:
    """Map malformed/out-of-range path thành 422 mà không bắt đầu mutation."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu path sai vẫn gọi database."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(course_view, "query_one", fail_query)

    response = put_course_response(client, course_id)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "course_id"


@pytest.mark.parametrize(
    "body",
    [
        update_body(title="T" * 201),
        update_body(price="1.234"),
        update_body(price="1e2"),
        update_body(price="NaN"),
        update_body(price="10000000000.00"),
        update_body(price=199),
        {"title": "Course", "description": None, "thumbnail_url": None},
        update_body(extra_field="unsupported"),
    ],
)
def test_put_admin_course_rejects_invalid_body_without_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: dict[str, Any],
) -> None:
    """Từ chối body thiếu/thừa field, sai type hoặc ngoài giới hạn candidate."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu body không hợp lệ vẫn chạy UPDATE."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(course_view, "query_one", fail_query)

    response = put_course_response(client, "11", body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None


def test_put_admin_course_accepts_negative_decimal_candidate_without_rounding(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bind decimal âm theo đúng input vì DDL candidate không cấm giá âm."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)
    captured = install_update_queries(monkeypatch)

    response = put_course_response(client, "11", update_body(price="-12.30"))

    assert response.status_code == 200
    assert captured[0][1]["price"] == Decimal("-12.30")


def test_put_admin_course_returns_404_when_update_has_no_row(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map UPDATE RETURNING rỗng thành catalog 404 và rollback transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_update_queries(monkeypatch, update_row=None)
    monkeypatch.setattr(
        course_view,
        "query_one",
        lambda _db, query, params: captured.append((query, dict(params))) or None,
    )

    response = put_course_response(client, "11")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None
    assert len(captured) == 1
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_put_admin_course_maps_query_error_to_safe_500_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """SQL failure trả lỗi an toàn và rollback transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def raise_query_error(*_args, **_kwargs):
        """Tạo lỗi SQL giả có chi tiết nhạy cảm để kiểm tra response."""

        raise SQLAlchemyError("sensitive SQL detail")

    monkeypatch.setattr(course_view, "query_one", raise_query_error)

    response = put_course_response(client, "11")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "sensitive SQL detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_put_admin_course_rolls_back_when_response_query_fails(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback UPDATE nếu query đọc lại Course thất bại trong cùng transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured: list[str] = []

    def query_one(_db, query, _params):
        """Cho UPDATE thành công rồi tạo lỗi ở SELECT response projection."""

        if query.lstrip().startswith("UPDATE"):
            return {"id": 11}
        captured.append(query)
        raise SQLAlchemyError("sensitive projection query detail")

    monkeypatch.setattr(course_view, "query_one", query_one)

    response = put_course_response(client, "11")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "sensitive projection query detail" not in response.text
    assert len(captured) == 1
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_put_admin_course_rejects_wrong_update_identity_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối UPDATE RETURNING sai ID thay vì dựng response cho resource khác."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_update_queries(monkeypatch, update_row={"id": 12})

    response = put_course_response(client, "11")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    "detail_row",
    [
        None,
        course_row(id=12),
        course_row(mentor_id=None),
        course_row(mentor_full_name=None),
        course_row(price=None),
    ],
)
def test_put_admin_course_rolls_back_when_response_projection_is_invalid(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    detail_row: dict[str, Any] | None,
) -> None:
    """Rollback mutation khi Q2 thiếu row hoặc Course response không hợp lệ."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_update_queries(monkeypatch, detail_row=detail_row)

    response = put_course_response(client, "11")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_put_admin_course_maps_commit_failure_to_safe_500_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Commit failure trả 500 an toàn và rollback mutation."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_update_queries(monkeypatch)

    response = put_course_response(client, "11")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "sensitive commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_put_admin_course_openapi_declares_body_path_and_catalog_errors(
    client: TestClient,
) -> None:
    """OpenAPI công bố body candidate, path int64 và chính xác error set catalog."""

    operation = client.app.openapi()["paths"]["/api/v1/admin/courses/{course_id}"]["put"]
    parameters = {parameter["name"]: parameter for parameter in operation["parameters"]}

    assert parameters["course_id"]["in"] == "path"
    assert parameters["course_id"]["required"] is True
    assert parameters["course_id"]["schema"] == {"type": "integer", "format": "int64"}
    assert parameters["Authorization"]["in"] == "header"
    assert parameters["Authorization"]["required"] is True
    assert {"200", "401", "403", "404", "422", "500"}.issubset(operation["responses"])
    request_schema = operation["requestBody"]["content"]["application/json"]["schema"]
    assert request_schema["$ref"].endswith("AdminCourseUpdateRequest")
