from typing import Any

import pytest
from app.core import security
from app.core.config import Settings
from app.core.security import (
    TokenError,
    compare_token_hash,
    create_access_token,
    decode_access_token,
    generate_refresh_token,
    hash_refresh_token,
)


def test_access_token_validates_signature_issuer_audience_and_type(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = Settings(
        db_host="localhost",
        db_name="study",
        db_user="user",
        db_password="password",
        db_schema="public",
        jwt_algorithm="HS256",
        jwt_secret_key="test-secret-key-that-is-at-least-32-characters",
    )
    monkeypatch.setattr(security, "get_settings", lambda: settings)

    token = create_access_token(user_id="user-1", roles=["learner"])
    claims: dict[str, Any] = decode_access_token(token)

    assert claims["sub"] == "user-1"
    assert claims["aud"] == "study-api"
    assert claims["type"] == "access"
    assert claims["roles"] == ["learner"]

    with pytest.raises(TokenError):
        decode_access_token(f"{token}tampered")


def test_opaque_refresh_token_is_random_and_hashable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = Settings(
        db_host="localhost",
        db_name="study",
        db_user="user",
        db_password="password",
        db_schema="public",
        jwt_algorithm="HS256",
        jwt_secret_key="test-secret-key-that-is-at-least-32-characters",
        refresh_token_pepper="refresh-pepper-that-is-at-least-32-characters",
    )
    monkeypatch.setattr(security, "get_settings", lambda: settings)

    first = generate_refresh_token()
    second = generate_refresh_token()
    first_hash = hash_refresh_token(first)

    assert first != second
    assert "user-1" not in first
    assert first_hash == hash_refresh_token(first)
    assert compare_token_hash(first_hash, hash_refresh_token(first)) is True
    assert compare_token_hash(first_hash, hash_refresh_token(second)) is False
