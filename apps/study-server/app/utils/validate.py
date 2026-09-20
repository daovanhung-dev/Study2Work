"""Reusable pure input-normalization and validation helpers."""


def strip_email(value: object) -> object:
    """Trim surrounding whitespace from string email inputs."""

    return value.strip() if isinstance(value, str) else value


def reject_blank_password(value: object) -> object:
    """Reject passwords that contain only whitespace."""

    if isinstance(value, str) and not value.strip():
        raise ValueError("Mật khẩu không được để trống.")
    return value


def reject_blank_value(value: object) -> object:
    """Reject string values that contain only whitespace."""

    if isinstance(value, str) and not value.strip():
        raise ValueError("Giá trị không được để trống.")
    return value
