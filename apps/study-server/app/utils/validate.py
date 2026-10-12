"""Reusable input normalization and validation helpers for Study API modules."""

from __future__ import annotations

from collections.abc import Collection

from pydantic import EmailStr, TypeAdapter, ValidationError

_EMAIL_ADAPTER = TypeAdapter(EmailStr)


def strip_email(value: object) -> object:
    """Loại khoảng trắng email ở hai đầu chuỗi và giữ nguyên các kiểu đầu vào khác."""
    return value.strip() if isinstance(value, str) else value


def reject_blank_password(value: object) -> object:
    """Từ chối mật khẩu chỉ có khoảng trắng, còn lại giữ nguyên giá trị đầu vào."""
    if isinstance(value, str) and not value.strip():
        raise ValueError("Mật khẩu không được để trống.")
    return value


def reject_blank_value(value: object) -> object:
    """Từ chối chuỗi chỉ có khoảng trắng, còn lại giữ nguyên giá trị đầu vào."""
    if isinstance(value, str) and not value.strip():
        raise ValueError("Giá trị không được để trống.")
    return value


def normalize_login_email(value: object) -> object:
    """Chuẩn hóa khoảng trắng email đăng nhập trước khi validator kiểm tra định dạng."""
    return strip_email(value)


def validate_login_password(value: object) -> object:
    """Áp dụng helper chung để từ chối mật khẩu đăng nhập rỗng."""
    return reject_blank_password(value)


def normalize_email(value: object, *, max_length: int | None = None) -> str:
    """Trim và kiểm tra email, sau đó trả chuỗi email đã chuẩn hóa bởi Pydantic."""

    if not isinstance(value, str):
        raise ValueError("Email must be a string.")

    normalized = value.strip()
    try:
        parsed = str(_EMAIL_ADAPTER.validate_python(normalized))
    except ValidationError as exc:
        email_errors = exc.errors(include_url=False)
        message = str(email_errors[0]["msg"]) if email_errors else "Invalid email address."
        raise ValueError(message) from None

    if max_length is not None and len(parsed) > max_length:
        raise ValueError(f"String should have at most {max_length} characters")
    return parsed


def require_non_blank(value: object, *, field_name: str) -> str:
    """Trả chuỗi không rỗng hoặc phát sinh ValueError để validator của API ánh xạ thành lỗi."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must not be blank.")
    return value


def normalize_sort(
    value: str | None,
    *,
    allowed_fields: Collection[str],
    allowed_directions: Collection[str],
) -> str | None:
    """Chuẩn hóa biểu thức sort ``field:direction`` theo allowlist của API."""

    if value is None:
        return None

    parts = value.split(":")
    if len(parts) != 2:
        raise ValueError("sort must use field:direction format.")
    field, direction = parts
    if field not in allowed_fields:
        raise ValueError("sort field is not supported.")
    if direction not in allowed_directions:
        raise ValueError("sort direction is not supported.")
    return f"{field}:{direction}"


def normalize_search_query(value: str | None) -> str | None:
    """Trim/chuyển chữ thường query và coi chuỗi trắng như không có filter tìm kiếm."""

    if isinstance(value, str):
        normalized = value.strip().lower()
        return normalized or None
    return value
