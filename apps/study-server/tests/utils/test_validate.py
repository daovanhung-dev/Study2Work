import pytest
from app.utils.validate import reject_blank_password, reject_blank_value, strip_email


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
