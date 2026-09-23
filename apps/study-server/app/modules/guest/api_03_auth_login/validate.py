"""Pure validation rules for the auth login module."""

from app.utils.validate import reject_blank_password, reject_blank_value, strip_email


def normalize_login_email(value: object) -> object:
    """Normalize the login email before Pydantic email validation."""

    return strip_email(value)


def validate_login_password(value: object) -> object:
    """Reject a blank login password without querying external state."""

    return reject_blank_password(value)


def validate_refresh_token(value: object) -> object:
    """Reject a blank refresh token without querying external state."""

    return reject_blank_value(value)
