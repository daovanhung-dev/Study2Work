from __future__ import annotations

import json
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import app.modules.guest.api_01_auth_register.view as auth_view
import pytest
from app.core.database import get_db
from app.modules.guest.api_01_auth_register.models import RegisterRequest
from app.modules.guest.api_01_auth_register.validate import validate_register_request
from app.modules.guest.api_01_auth_register.view import create_user
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.responses import JSONResponse


class FakeSession:
    def __init__(self) -> None:
        """Khởi tạo phiên database giả với các bộ đếm commit/rollback dùng để xác minh quyền sở hữu
        transaction trong test."""
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Tăng bộ đếm commit của FakeSession để test xác nhận transaction được xác nhận đúng số
        lần."""
        self.commit_count += 1

    def rollback(self) -> None:
        """Tăng bộ đếm rollback của FakeSession để test xác nhận lỗi đã hoàn tác transaction."""
        self.rollback_count += 1


def make_created_user() -> dict[str, Any]:
    """Tạo hàng user giả mà câu insert đăng ký trả về, gồm các trường profile công khai và
    timestamp cố định."""
    created_at = datetime(2026, 9, 15, 12, 0, tzinfo=UTC)
    return {
        "id": 1001,
        "full_name": "Nguyen Van A",
        "email": "student@example.com",
        "role": "STUDENT",
        "avatar_url": None,
        "phone": None,
        "status": "ACTIVE",
        "created_at": created_at,
        "updated_at": created_at,
    }


def override_db(session: FakeSession):
    """Tạo dependency FastAPI thay thế database, để route dùng FakeSession trong kiểm thử mà không
    kết nối database thật."""
    def dependency():
        """Yield FakeSession đã được closure giữ lại để request kiểm thử dùng cùng một phiên giả."""
        yield session

    return dependency


def test_register_request_validates_and_normalizes_whitespace() -> None:
    """Model giữ dữ liệu thô; validator chuẩn hóa email và full_name trước nghiệp vụ."""
    request = RegisterRequest(
        email=" student@example.com ",
        password="correct horse battery staple",
        full_name=" Nguyen Van A ",
    )

    assert request.email == " student@example.com "
    assert request.full_name == " Nguyen Van A "
    validated = validate_register_request(request, trace_id="trace-id")
    assert isinstance(validated, RegisterRequest)
    assert validated.email == "student@example.com"
    assert validated.full_name == "Nguyen Van A"


@pytest.mark.parametrize(
    "payload",
    [
        {"email": "student@example.com", "password": "", "full_name": "Student"},
        {"email": "student@example.com", "password": "   ", "full_name": "Student"},
        {"email": "not-an-email", "password": "password", "full_name": "Student"},
        {"email": "student@example.com", "password": "password", "full_name": "   "},
        {
            "email": "student@example.com",
            "password": "password",
            "full_name": "a" * 151,
        },
    ],
)
def test_register_validator_rejects_invalid_payload(payload: dict[str, str]) -> None:
    """Kiểm tra validator trả response 422 với fieldErrors cho dữ liệu đăng ký không hợp lệ."""
    response = validate_register_request(RegisterRequest(**payload), trace_id="trace-id")
    assert isinstance(response, JSONResponse)
    assert response.status_code == 422
    body = json.loads(response.body)
    assert body["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert body["traceId"] == "trace-id"
    assert body["meta"]["fieldErrors"]


def test_create_user_hashes_password_commits_and_returns_safe_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra đăng ký băm password trước khi insert, commit đúng một lần và chỉ trả các trường
    profile công khai."""
    session = FakeSession()
    captured: dict[str, Any] = {}

    monkeypatch.setattr(auth_view, "find_user_by_email", lambda db, email: None)

    def fake_insert_user(
        db: FakeSession,
        *,
        full_name: str,
        email: str,
        password_hash: str,
    ) -> dict[str, Any]:
        """Ghi lại các trường insert nhận được rồi trả hàng user giả, giúp kiểm tra đầu vào và kết
        quả của luồng đăng ký."""
        captured.update(
            full_name=full_name,
            email=email,
            password_hash=password_hash,
        )
        return make_created_user()

    monkeypatch.setattr(auth_view, "insert_user", fake_insert_user)

    response = create_user(
        user_data=RegisterRequest(
            email="student@example.com",
            password="correct horse battery staple",
            full_name="Nguyen Van A",
        ),
        db=session,  # type: ignore[arg-type]
        trace_id="trace-id",
    )

    assert session.commit_count == 1
    assert session.rollback_count == 0
    assert captured["password_hash"].startswith("$argon2id$")
    assert captured["password_hash"] != "correct horse battery staple"
    assert response["businessCode"] == "DESIGN_RESOURCE_CREATED"
    assert response["data"]["email"] == "student@example.com"
    assert "password" not in response["data"]
    assert "password_hash" not in response["data"]


def test_create_user_rejects_duplicate_email(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra email đã tồn tại khiến create_user rollback và trả lỗi conflict HTTP 409."""
    session = FakeSession()
    monkeypatch.setattr(auth_view, "find_user_by_email", lambda db, email: {"id": 1})

    error = create_user(
            user_data=RegisterRequest(
                email="student@example.com",
                password="password",
                full_name="Student",
            ),
            db=session,  # type: ignore[arg-type]
            trace_id="trace-id",
        )

    assert isinstance(error, JSONResponse)
    assert error.status_code == 409
    assert json.loads(error.body)["businessCode"] == "DESIGN_STATE_CONFLICT"
    assert session.rollback_count == 1


def test_create_user_rolls_back_database_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra lỗi SQLAlchemy khi tạo tài khoản làm rollback transaction và được ánh xạ thành lỗi
    500 an toàn."""
    session = FakeSession()
    monkeypatch.setattr(auth_view, "find_user_by_email", lambda db, email: None)
    monkeypatch.setattr(
        auth_view,
        "insert_user",
        lambda db, **kwargs: (_ for _ in ()).throw(SQLAlchemyError("database unavailable")),
    )

    error = create_user(
            user_data=RegisterRequest(
                email="student@example.com",
                password="password",
                full_name="Student",
            ),
            db=session,  # type: ignore[arg-type]
            trace_id="trace-id",
        )

    assert isinstance(error, JSONResponse)
    assert error.status_code == 500
    assert json.loads(error.body)["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_create_user_maps_email_unique_race_to_conflict(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra unique constraint email phát sinh giữa lookup và insert được nhận diện thành
    conflict HTTP 409."""
    session = FakeSession()
    monkeypatch.setattr(auth_view, "find_user_by_email", lambda db, email: None)
    original = SimpleNamespace(diag=SimpleNamespace(constraint_name="users_email_key"))
    unique_error = IntegrityError("insert failed", {}, original)
    monkeypatch.setattr(
        auth_view,
        "insert_user",
        lambda db, **kwargs: (_ for _ in ()).throw(unique_error),
    )

    error = create_user(
            user_data=RegisterRequest(
                email="student@example.com",
                password="password",
                full_name="Student",
            ),
            db=session,  # type: ignore[arg-type]
            trace_id="trace-id",
        )

    assert isinstance(error, JSONResponse)
    assert error.status_code == 409
    assert json.loads(error.body)["businessCode"] == "DESIGN_STATE_CONFLICT"
    assert session.rollback_count == 1


def test_register_http_success_uses_canonical_path_and_safe_response(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra POST /api/v1/auth/register tạo tài khoản với HTTP 201, success envelope và dữ liệu
    không chứa password hash."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_view, "find_user_by_email", lambda db, email: None)
    monkeypatch.setattr(auth_view, "insert_user", lambda db, **kwargs: make_created_user())

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "student@example.com",
            "password": "correct horse battery staple",
            "full_name": "Nguyen Van A",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_CREATED"
    assert payload["data"]["id"] == 1001
    assert "password" not in response.text
    assert "password_hash" not in response.text
    assert session.commit_count == 1


def test_register_legacy_path_is_not_exposed(client: TestClient) -> None:
    """Kiểm tra đường dẫn đăng ký legacy không được mount và trả HTTP 404."""
    response = client.post(
        "/api/v1/register",
        json={
            "email": "student@example.com",
            "password": "password",
            "full_name": "Student",
        },
    )

    assert response.status_code == 404


def test_register_validation_returns_response_before_database_access(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Xác nhận input sai trả JSON lỗi trực tiếp, kèm fieldErrors/trace header và không query DB."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        auth_view,
        "find_user_by_email",
        lambda *args: (_ for _ in ()).throw(AssertionError("invalid input must fail first")),
    )
    trace_id = "00000000-0000-0000-0000-000000000001"

    response = client.post(
        "/api/v1/auth/register",
        json={"email": "invalid", "password": "password", "full_name": "Student"},
        headers={"X-Trace-Id": trace_id},
    )

    assert response.status_code == 422
    assert response.headers["X-Trace-Id"] == trace_id
    assert response.json()["traceId"] == trace_id
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "email"
    assert session.rollback_count == 0


def test_register_http_duplicate_returns_conflict(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra API đăng ký trả HTTP 409 cùng business code conflict khi email đã được dùng."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_view, "find_user_by_email", lambda db, email: {"id": 1})

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "student@example.com",
            "password": "password",
            "full_name": "Student",
        },
    )

    assert response.status_code == 409
    assert response.json()["businessCode"] == "DESIGN_STATE_CONFLICT"
    assert session.rollback_count == 1


def test_register_http_database_error_returns_safe_internal_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra lỗi database của API đăng ký trả lỗi nội bộ an toàn, không để lộ thông tin truy
    vấn."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_view, "find_user_by_email", lambda db, email: None)
    monkeypatch.setattr(
        auth_view,
        "insert_user",
        lambda db, **kwargs: (_ for _ in ()).throw(SQLAlchemyError("database unavailable")),
    )

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "student@example.com",
            "password": "password",
            "full_name": "Student",
        },
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "database unavailable" not in response.text
    assert session.rollback_count == 1


def test_register_http_unexpected_error_uses_design_internal_code(
    client_without_server_exception: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra exception ngoài dự kiến tại API đăng ký dùng business code lỗi nội bộ theo design
    contract."""
    session = FakeSession()
    client_without_server_exception.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_view, "find_user_by_email", lambda db, email: None)
    monkeypatch.setattr(
        auth_view,
        "hash_password",
        lambda password: (_ for _ in ()).throw(RuntimeError("unexpected failure")),
    )

    response = client_without_server_exception.post(
        "/api/v1/auth/register",
        json={
            "email": "student@example.com",
            "password": "password",
            "full_name": "Student",
        },
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "unexpected failure" not in response.text
