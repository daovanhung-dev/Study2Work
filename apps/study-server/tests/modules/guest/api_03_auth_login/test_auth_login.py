from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.guest.api_03_auth_login.view as auth_view
import pytest
from app.core.database import get_db
from app.core.responses import ApiError
from app.core.security.password import hash_password
from app.modules.guest.api_03_auth_login.models import LoginRequest, RefreshRequest
from app.utils.auth import IssuedTokens
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeResult:
    def __init__(self, row: Any) -> None:
        self.row = row

    def first(self) -> Any:
        return self.row


class FakeSession:
    def __init__(self) -> None:
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        self.commit_count += 1

    def rollback(self) -> None:
        self.rollback_count += 1


def make_user(*, status: str = "ACTIVE", include_password: bool = True) -> dict[str, Any]:
    created_at = datetime(2026, 9, 15, 12, 0, tzinfo=UTC)
    user = {
        "id": 1001,
        "full_name": "Nguyen Van A",
        "email": "student@example.com",
        "role": "STUDENT",
        "avatar_url": None,
        "phone": None,
        "status": status,
        "created_at": created_at,
        "updated_at": created_at,
    }
    if include_password:
        user["password_hash"] = hash_password("correct horse battery staple")
    return user


def make_tokens() -> IssuedTokens:
    return IssuedTokens(
        access_token="access-token",
        refresh_token="refresh-token",
        refresh_token_hash="refresh-token-hash",
        refresh_expires_at=datetime(2026, 10, 15, tzinfo=UTC),
        expires_in=3600,
        refresh_expires_in=2592000,
    )


def override_db(session: FakeSession):
    def dependency():
        yield session

    return dependency


def test_login_request_normalizes_email_and_rejects_blank_password() -> None:
    request = LoginRequest(
        email=" student@example.com ",
        password="correct horse battery staple",
    )

    assert str(request.email) == "student@example.com"

    with pytest.raises(ValueError):
        LoginRequest(email="student@example.com", password="   ")


def test_refresh_request_rejects_blank_token() -> None:
    with pytest.raises(ValueError):
        RefreshRequest(refresh_token="   ")


def test_login_returns_profile_and_tokens_and_commits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    user = make_user()
    executed: list[dict[str, Any]] = []

    monkeypatch.setattr(auth_view, "query_one", lambda db, query, params: user)
    monkeypatch.setattr(auth_view, "issue_tokens", lambda user_id, role: make_tokens())
    monkeypatch.setattr(
        auth_view,
        "execute_query",
        lambda db, query, params: executed.append(params) or FakeResult((1,)),
    )

    response = auth_view.login(
        user_data=LoginRequest(
            email="student@example.com",
            password="correct horse battery staple",
        ),
        db=session,  # type: ignore[arg-type]
        trace_id="trace-id",
    )

    assert session.commit_count == 1
    assert session.rollback_count == 0
    assert response["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert response["data"]["access_token"] == "access-token"
    assert response["data"]["refresh_token"] == "refresh-token"
    assert response["data"]["email"] == "student@example.com"
    assert "password_hash" not in response["data"]
    assert executed[0]["token_hash"] == "refresh-token-hash"


@pytest.mark.parametrize("status", ["LOCKED", "DISABLED"])
def test_login_rejects_inactive_account(
    monkeypatch: pytest.MonkeyPatch,
    status: str,
) -> None:
    session = FakeSession()
    monkeypatch.setattr(auth_view, "query_one", lambda db, query, params: make_user(status=status))

    with pytest.raises(ApiError) as error:
        auth_view.login(
            user_data=LoginRequest(
                email="student@example.com",
                password="correct horse battery staple",
            ),
            db=session,  # type: ignore[arg-type]
            trace_id="trace-id",
        )

    assert error.value.status_code == 403
    assert error.value.business_code == "DESIGN_ACCESS_DENIED"


def test_login_hides_unknown_or_wrong_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    monkeypatch.setattr(auth_view, "query_one", lambda db, query, params: None)

    with pytest.raises(ApiError) as error:
        auth_view.login(
            user_data=LoginRequest(
                email="student@example.com",
                password="wrong password",
            ),
            db=session,  # type: ignore[arg-type]
            trace_id="trace-id",
        )

    assert error.value.status_code == 401
    assert error.value.business_code == "DESIGN_AUTHENTICATION_REQUIRED"


def test_login_rolls_back_database_error(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()

    def fail_query(db, query, params):
        raise SQLAlchemyError("database unavailable")

    monkeypatch.setattr(auth_view, "query_one", fail_query)

    with pytest.raises(ApiError) as error:
        auth_view.login(
            user_data=LoginRequest(
                email="student@example.com",
                password="password",
            ),
            db=session,  # type: ignore[arg-type]
            trace_id="trace-id",
        )

    assert error.value.status_code == 500
    assert error.value.business_code == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_refresh_rotates_old_token_atomically(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()
    user = make_user(include_password=False)
    user["refresh_token_id"] = 9
    executed: list[tuple[str, dict[str, Any]]] = []

    monkeypatch.setattr(auth_view, "hash_refresh_token", lambda token: "old-token-hash")
    monkeypatch.setattr(auth_view, "query_one", lambda db, query, params: user)
    monkeypatch.setattr(auth_view, "issue_tokens", lambda user_id, role: make_tokens())

    def execute(db, query, params):
        executed.append((query, params))
        return FakeResult((9,))

    monkeypatch.setattr(auth_view, "execute_query", execute)

    response = auth_view.refresh(
        user_data=RefreshRequest(refresh_token="old-token"),
        db=session,  # type: ignore[arg-type]
        trace_id="trace-id",
    )

    assert session.commit_count == 1
    assert session.rollback_count == 0
    assert len(executed) == 2
    assert executed[0][1] == {"refresh_token_id": 9}
    assert executed[1][1]["token_hash"] == "refresh-token-hash"
    assert response["data"]["refresh_token"] == "refresh-token"


def test_refresh_rejects_invalid_token(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()
    monkeypatch.setattr(auth_view, "hash_refresh_token", lambda token: "missing-hash")
    monkeypatch.setattr(auth_view, "query_one", lambda db, query, params: None)

    with pytest.raises(ApiError) as error:
        auth_view.refresh(
            user_data=RefreshRequest(refresh_token="missing-token"),
            db=session,  # type: ignore[arg-type]
            trace_id="trace-id",
        )

    assert error.value.status_code == 401
    assert error.value.business_code == "DESIGN_AUTHENTICATION_REQUIRED"
    assert session.commit_count == 0


def test_auth_http_validation_uses_design_error_code(client: TestClient) -> None:
    login_response = client.post("/api/v1/auth/login", json={})
    refresh_response = client.post("/api/v1/auth/refresh", json={})

    assert login_response.status_code == 422
    assert refresh_response.status_code == 422
    assert login_response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert refresh_response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"


def test_auth_http_login_returns_tokens(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_view, "query_one", lambda db, query, params: make_user())
    monkeypatch.setattr(auth_view, "issue_tokens", lambda user_id, role: make_tokens())
    monkeypatch.setattr(
        auth_view,
        "execute_query",
        lambda db, query, params: FakeResult((1,)),
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "student@example.com",
            "password": "correct horse battery staple",
        },
    )

    assert response.status_code == 200
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert response.json()["data"]["access_token"] == "access-token"
