from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import app.modules.guest.register_account.view as auth_view
import pytest
from app.core.database import get_db
from app.core.responses import ApiError
from app.modules.guest.register_account.models import RegisterRequest
from app.modules.guest.register_account.view import create_user
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class FakeSession:
    def __init__(self) -> None:
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        self.commit_count += 1

    def rollback(self) -> None:
        self.rollback_count += 1


def make_created_user() -> dict[str, Any]:
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
    def dependency():
        yield session

    return dependency


def test_register_request_validates_and_normalizes_whitespace() -> None:
    request = RegisterRequest(
        email=" student@example.com ",
        password="correct horse battery staple",
        full_name=" Nguyen Van A ",
    )

    assert str(request.email) == "student@example.com"
    assert request.full_name == "Nguyen Van A"


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
def test_register_request_rejects_invalid_payload(payload: dict[str, str]) -> None:
    with pytest.raises(ValidationError):
        RegisterRequest(**payload)


def test_create_user_hashes_password_commits_and_returns_safe_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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
    session = FakeSession()
    monkeypatch.setattr(auth_view, "find_user_by_email", lambda db, email: {"id": 1})

    with pytest.raises(ApiError) as error:
        create_user(
            user_data=RegisterRequest(
                email="student@example.com",
                password="password",
                full_name="Student",
            ),
            db=session,  # type: ignore[arg-type]
            trace_id="trace-id",
        )

    assert error.value.status_code == 409
    assert error.value.business_code == "DESIGN_STATE_CONFLICT"
    assert session.rollback_count == 1


def test_create_user_rolls_back_database_error(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()
    monkeypatch.setattr(auth_view, "find_user_by_email", lambda db, email: None)
    monkeypatch.setattr(
        auth_view,
        "insert_user",
        lambda db, **kwargs: (_ for _ in ()).throw(SQLAlchemyError("database unavailable")),
    )

    with pytest.raises(ApiError) as error:
        create_user(
            user_data=RegisterRequest(
                email="student@example.com",
                password="password",
                full_name="Student",
            ),
            db=session,  # type: ignore[arg-type]
            trace_id="trace-id",
        )

    assert error.value.status_code == 500
    assert error.value.business_code == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_create_user_maps_email_unique_race_to_conflict(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    monkeypatch.setattr(auth_view, "find_user_by_email", lambda db, email: None)
    original = SimpleNamespace(diag=SimpleNamespace(constraint_name="users_email_key"))
    unique_error = IntegrityError("insert failed", {}, original)
    monkeypatch.setattr(
        auth_view,
        "insert_user",
        lambda db, **kwargs: (_ for _ in ()).throw(unique_error),
    )

    with pytest.raises(ApiError) as error:
        create_user(
            user_data=RegisterRequest(
                email="student@example.com",
                password="password",
                full_name="Student",
            ),
            db=session,  # type: ignore[arg-type]
            trace_id="trace-id",
        )

    assert error.value.status_code == 409
    assert error.value.business_code == "DESIGN_STATE_CONFLICT"
    assert session.rollback_count == 1


def test_register_http_success_uses_canonical_path_and_safe_response(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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
    response = client.post(
        "/api/v1/register",
        json={
            "email": "student@example.com",
            "password": "password",
            "full_name": "Student",
        },
    )

    assert response.status_code == 404


def test_register_http_duplicate_returns_conflict(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_view, "find_user_by_email", lambda db, email: None)
    monkeypatch.setattr(
        auth_view,
        "hash_password",
        lambda password: (_ for _ in ()).throw(RuntimeError("unexpected failure")),
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
    assert "unexpected failure" not in response.text
