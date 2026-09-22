from __future__ import annotations

from typing import Any

import pytest
from app.core.database import get_db
from app.modules.guest.verify_email_send.models import VerifyEmailSendRequest
from app.service.email.provider import (
    VerificationDispatchResult,
    VerificationEmailProviderError,
    get_verification_email_provider,
)
from fastapi.testclient import TestClient
from pydantic import ValidationError


class FakeProvider:
    def __init__(self, result: VerificationDispatchResult | None = None) -> None:
        self.result = result or VerificationDispatchResult(status="accepted")
        self.calls: list[dict[str, Any]] = []

    def dispatch(
        self,
        *,
        user_id: int,
        email: str,
        trace_id: str,
    ) -> VerificationDispatchResult:
        self.calls.append(
            {
                "user_id": user_id,
                "email": email,
                "trace_id": trace_id,
            }
        )
        return self.result


class FailingProvider:
    def dispatch(
        self,
        *,
        user_id: int,
        email: str,
        trace_id: str,
    ) -> VerificationDispatchResult:
        del user_id, email, trace_id
        raise VerificationEmailProviderError("provider response must not leak")


def override_provider(provider: object):
    def dependency() -> object:
        return provider

    return dependency


def test_verify_email_request_accepts_contract_fields() -> None:
    request = VerifyEmailSendRequest(user_id=1001, email="student@example.com")

    assert request.user_id == 1001
    assert str(request.email) == "student@example.com"


@pytest.mark.parametrize(
    "payload",
    [
        {"email": "student@example.com"},
        {"user_id": 1001},
        {"user_id": "1001", "email": "student@example.com"},
        {"user_id": 1001, "email": "not-an-email"},
    ],
)
def test_verify_email_request_rejects_invalid_payload(payload: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        VerifyEmailSendRequest(**payload)


@pytest.mark.parametrize(
    "headers",
    [{}, {"Authorization": "Bearer malformed-token"}],
)
def test_verify_email_http_accepts_public_dispatch(
    client: TestClient,
    headers: dict[str, str],
) -> None:
    provider = FakeProvider()
    client.app.dependency_overrides[get_verification_email_provider] = override_provider(provider)

    response = client.post(
        "/api/v1/auth/verify-email/send",
        json={"user_id": 1001, "email": "student@example.com"},
        headers=headers,
    )

    assert response.status_code == 202
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_OPERATION_ACCEPTED"
    assert payload["data"] == {"status": "accepted"}
    assert payload["meta"] == {}
    assert payload["traceId"]
    assert provider.calls[0]["user_id"] == 1001
    assert provider.calls[0]["email"] == "student@example.com"
    assert provider.calls[0]["trace_id"] == payload["traceId"]


def test_verify_email_http_does_not_require_database(
    client: TestClient,
) -> None:
    def fail_db_dependency():
        raise AssertionError("API #2 must not resolve the database dependency")

    client.app.dependency_overrides[get_db] = fail_db_dependency

    response = client.post(
        "/api/v1/auth/verify-email/send",
        json={"user_id": 1001, "email": "student@example.com"},
    )

    assert response.status_code == 202


def test_verify_email_http_maps_provider_failure_without_leaking_details(
    client: TestClient,
) -> None:
    client.app.dependency_overrides[get_verification_email_provider] = override_provider(
        FailingProvider()
    )

    response = client.post(
        "/api/v1/auth/verify-email/send",
        json={"user_id": 1001, "email": "student@example.com"},
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "provider response must not leak" not in response.text


def test_verify_email_http_uses_design_validation_code(client: TestClient) -> None:
    response = client.post("/api/v1/auth/verify-email/send", json={})

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
