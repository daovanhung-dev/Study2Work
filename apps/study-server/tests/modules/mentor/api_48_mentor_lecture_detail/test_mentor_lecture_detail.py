from __future__ import annotations

from typing import Any

import app.modules.mentor.api_48_mentor_lecture_detail.view as lecture_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    def __init__(self) -> None:
        """Theo dõi endpoint đọc không commit và rollback các lượt đọc lỗi."""
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận commit ngoài dự kiến của endpoint chỉ đọc."""
        self.commit_count += 1

    def rollback(self) -> None:
        """Ghi nhận cleanup transaction sau lượt đọc lỗi hoặc bị từ chối."""
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Cung cấp fake session theo request qua dependency database của Study."""
    def dependency():
        """Yield fake session đã được test giữ lại."""
        yield session

    return dependency


def allow_mentor_token(monkeypatch: pytest.MonkeyPatch, *, roles: list[str] | None = None) -> None:
    """Thay giải mã JWT bằng claim Mentor có subject dạng số."""
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": roles or ["MENTOR"]},
    )


def lecture_row(**overrides: Any) -> dict[str, Any]:
    """Tạo row lessons/courses legacy đã JOIN cho API #48."""
    return {
        "id": 48001,
        "course_id": 101,
        "name": "Bài học chi tiết",
        "content": None,
        "sort_order": 2,
        "status": "DRAFT",
        "parent_course_id": 101,
        "mentor_id": 1001,
        **overrides,
    }


def upload_row(upload_id: int, *, name: str) -> dict[str, Any]:
    """Tạo một row UploadAsset đã kiểm tra scope cho projection API #48."""
    return {
        "upload_id": upload_id,
        "id": upload_id,
        "name": name,
        "url": f"https://cdn.example.test/uploads/{upload_id}",
        "content_type": "application/pdf",
        "size_bytes": 1024 + upload_id,
        "status": "UPLOADED",
    }


def get_lecture_response(client: TestClient, lecture_id: str = "48001"):
    """Gửi API #48 cùng Bearer token Mentor hợp lệ dùng trong test."""
    return client.get(
        f"/api/v1/mentor/lectures/{lecture_id}",
        headers={"Authorization": "Bearer valid-token"},
    )


def test_get_lecture_returns_nullable_content_and_ordered_assets(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Đọc lecture và giữ thứ tự UploadAsset cùng giá trị content NULL."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: dict[str, Any] = {}

    def find_lecture(_db, query, params):
        captured["lecture_sql"] = query
        assert params == {"lecture_id": 48001}
        return lecture_row()

    def find_assets(_db, query, params):
        captured["assets_sql"] = query
        captured["assets_params"] = params
        return [
            upload_row(34002, name="second.pdf"),
            upload_row(34001, name="first.pdf"),
        ]

    monkeypatch.setattr(lecture_view, "query_one", find_lecture)
    monkeypatch.setattr(lecture_view, "query_many", find_assets)

    response = get_lecture_response(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["content"] is None
    assert payload["data"]["status"] == "DRAFT"
    assert [asset["id"] for asset in payload["data"]["assets"]] == [34002, 34001]
    assert [asset["name"] for asset in payload["data"]["assets"]] == [
        "second.pdf",
        "first.pdf",
    ]
    assert "l.status IS DISTINCT FROM 'DELETED'" in captured["lecture_sql"]
    assert "LEFT JOIN courses" in captured["lecture_sql"]
    assert "l.status = 'PUBLISHED'" not in captured["lecture_sql"]
    assert "ORDER BY lesson_uploads.asset_position ASC" in captured["assets_sql"]
    assert "owner_id = :mentor_id" in captured["assets_sql"]
    assert "purpose = 'LECTURE'" in captured["assets_sql"]
    assert captured["assets_params"] == {
        "lecture_id": 48001,
        "mentor_id": 1001,
        "course_id": 101,
    }
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_lecture_returns_empty_array_when_no_assets_are_linked(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả mảng assets rỗng khi lesson không có asset link nào."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(lecture_view, "query_one", lambda *_args, **_kwargs: lecture_row())
    monkeypatch.setattr(lecture_view, "query_many", lambda *_args, **_kwargs: [])

    response = get_lecture_response(client)

    assert response.status_code == 200
    assert response.json()["data"]["assets"] == []
    assert session.commit_count == 0


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_get_lecture_rejects_missing_or_malformed_auth_before_db(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Từ chối Bearer auth thiếu hoặc sai định dạng trước khi query lecture."""
    monkeypatch.setattr(
        lecture_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )
    headers = {} if authorization is None else {"Authorization": authorization}

    response = client.get("/api/v1/mentor/lectures/48001", headers=headers)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_get_lecture_rejects_non_mentor_role_before_db(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối JWT Student trên route Mentor trước khi đọc database."""
    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    monkeypatch.setattr(
        lecture_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = get_lecture_response(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


@pytest.mark.parametrize("lecture_id", ["abc", "9223372036854775808", "-9223372036854775809"])
def test_get_lecture_maps_malformed_or_out_of_range_id_to_catalog_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    lecture_id: str,
) -> None:
    """Map path sai định dạng vào kết quả 404 đã có trong catalog."""
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        lecture_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("invalid ID must not query")
        ),
    )

    response = get_lecture_response(client, lecture_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_lecture_returns_not_found_when_row_is_absent(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 404 và dọn read transaction khi không tìm thấy lesson."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(lecture_view, "query_one", lambda *_args, **_kwargs: None)

    response = get_lecture_response(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_lecture_forbids_another_mentor_and_skips_asset_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Yêu cầu direct ownership qua courses.mentor_id trước khi đọc linked uploads."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        lecture_view,
        "query_one",
        lambda *_args, **_kwargs: lecture_row(mentor_id=2002),
    )
    monkeypatch.setattr(
        lecture_view,
        "query_many",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("asset query must not run")),
    )

    response = get_lecture_response(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    "row_overrides",
    [{"course_id": None}, {"parent_course_id": None}],
)
def test_get_lecture_returns_internal_error_for_missing_parent_integrity(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    row_overrides: dict[str, Any],
) -> None:
    """Trả lỗi toàn vẹn dữ liệu khi quan hệ lesson-to-course bị hỏng."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        lecture_view,
        "query_one",
        lambda *_args, **_kwargs: lecture_row(**row_overrides),
    )

    response = get_lecture_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_get_lecture_returns_internal_error_for_broken_upload_link(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối lesson_uploads row khi không resolve được metadata uploads tham chiếu."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(lecture_view, "query_one", lambda *_args, **_kwargs: lecture_row())
    monkeypatch.setattr(
        lecture_view,
        "query_many",
        lambda *_args, **_kwargs: [{**upload_row(34001, name="broken.pdf"), "id": None}],
    )

    response = get_lecture_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_get_lecture_returns_safe_internal_error_for_query_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ẩn lỗi SQL và rollback session khi query lecture thất bại."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        lecture_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(SQLAlchemyError("database detail")),
    )

    response = get_lecture_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "database detail" not in response.text
    assert session.rollback_count == 1


def test_get_lecture_route_openapi_contract(client: TestClient) -> None:
    """Kiểm tra OpenAPI công bố GET path, lecture ID int64 và response model."""
    schema = client.app.openapi()
    operation = schema["paths"]["/api/v1/mentor/lectures/{lecture_id}"]["get"]
    lecture_id_parameter = next(
        parameter for parameter in operation["parameters"] if parameter["name"] == "lecture_id"
    )

    assert operation["responses"]["200"]
    assert lecture_id_parameter["schema"]["type"] == "integer"
    assert lecture_id_parameter["schema"]["format"] == "int64"
    response_schema = schema["components"]["schemas"]["LectureResponse"]["properties"]
    assert response_schema["assets"]["type"] == "array"
    assert "anyOf" in response_schema["content"] or response_schema["content"]["type"] == "string"
