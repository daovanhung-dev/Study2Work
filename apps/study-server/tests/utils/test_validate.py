import pytest
from app.utils.validate import (
    normalize_login_email,
    reject_blank_password,
    reject_blank_value,
    strip_email,
    validate_login_password,
    validate_refresh_token,
)


def test_strip_email_trims_only_string_values() -> None:
    assert strip_email(" student@example.com ") == "student@example.com"
    assert strip_email(123) == 123


@pytest.mark.parametrize("validator", [reject_blank_password, reject_blank_value])
def test_blank_value_validators_reject_whitespace(validator) -> None:
    with pytest.raises(ValueError):
        validator("   ")


def test_blank_value_validators_preserve_non_blank_values() -> None:
    assert reject_blank_password("password") == "password"
    assert reject_blank_value("refresh-token") == "refresh-token"


def test_login_email_validator_reuses_shared_email_normalization() -> None:
    assert normalize_login_email(" student@example.com ") == "student@example.com"


def test_login_password_validator_rejects_blank_password() -> None:
    with pytest.raises(ValueError):
        validate_login_password("   ")

    assert validate_login_password("password") == "password"


def test_refresh_token_validator_rejects_blank_token() -> None:
    with pytest.raises(ValueError):
        validate_refresh_token("   ")

    assert validate_refresh_token("refresh-token") == "refresh-token"
