"""Reusable input normalization and validation helpers for Study API modules."""

from __future__ import annotations

import re
import sys
from collections.abc import Collection

from pydantic import EmailStr, TypeAdapter, ValidationError

from app.core.responses import ErrorDetail

_EMAIL_ADAPTER = TypeAdapter(EmailStr)
_INTEGER_PATTERN = re.compile(r"[+-]?[0-9](?:_?[0-9])*\Z")


def strip_email(value: object) -> object:
    """Loại khoảng trắng email ở hai đầu chuỗi và giữ nguyên các kiểu đầu vào khác."""
    return value.strip() if isinstance(value, str) else value


def reject_blank_password(value: object) -> object | ErrorDetail:
    """Từ chối mật khẩu chỉ có khoảng trắng, còn lại giữ nguyên giá trị đầu vào."""
    if isinstance(value, str) and not value.strip():
        return ErrorDetail(code="VALUE_ERROR", message="Mật khẩu không được để trống.")
    return value


def reject_blank_value(value: object) -> object | ErrorDetail:
    """Từ chối chuỗi chỉ có khoảng trắng, còn lại giữ nguyên giá trị đầu vào."""
    if isinstance(value, str) and not value.strip():
        return ErrorDetail(code="VALUE_ERROR", message="Giá trị không được để trống.")
    return value


def normalize_login_email(value: object) -> object:
    """Chuẩn hóa khoảng trắng email đăng nhập trước khi validator kiểm tra định dạng."""
    return strip_email(value)


def validate_login_password(value: object) -> object | ErrorDetail:
    """Áp dụng helper chung để từ chối mật khẩu đăng nhập rỗng."""
    return reject_blank_password(value)


def normalize_email(
    value: object,
    *,
    max_length: int | None = None,
) -> str | ErrorDetail:
    """Trim và kiểm tra email, trả chuỗi chuẩn hóa hoặc ErrorDetail nếu input sai."""

    if not isinstance(value, str):
        return ErrorDetail(code="VALUE_ERROR", message="Email must be a string.")

    normalized = value.strip()
    try:
        parsed = str(_EMAIL_ADAPTER.validate_python(normalized))
    except ValidationError as exc:
        email_errors = exc.errors(include_url=False)
        message = str(email_errors[0]["msg"]) if email_errors else "Invalid email address."
        return ErrorDetail(code="VALUE_ERROR", message=message)

    if max_length is not None and len(parsed) > max_length:
        return ErrorDetail(
            code="STRING_TOO_LONG",
            message=f"String should have at most {max_length} characters",
        )
    return parsed


def require_non_blank(value: object, *, field_name: str) -> str | ErrorDetail:
    """Trả chuỗi không rỗng hoặc ErrorDetail để validator API ánh xạ thành response."""

    if not isinstance(value, str) or not value.strip():
        return ErrorDetail(code="VALUE_ERROR", message=f"{field_name} must not be blank.")
    return value


def normalize_sort(
    value: str | None,
    *,
    allowed_fields: Collection[str],
    allowed_directions: Collection[str],
) -> str | None | ErrorDetail:
    """Chuẩn hóa sort theo allowlist hoặc trả ErrorDetail khi biểu thức không hợp lệ."""

    if value is None:
        return None

    parts = value.split(":")
    if len(parts) != 2:
        return ErrorDetail(code="VALUE_ERROR", message="sort must use field:direction format.")
    field, direction = parts
    if field not in allowed_fields:
        return ErrorDetail(code="VALUE_ERROR", message="sort field is not supported.")
    if direction not in allowed_directions:
        return ErrorDetail(code="VALUE_ERROR", message="sort direction is not supported.")
    return f"{field}:{direction}"


def parse_integer(value: object) -> int | None:
    """Chuyển chuỗi số nguyên hợp lệ thành int; trả None nếu không thể parse an toàn."""

    if type(value) is int:
        return value
    if not isinstance(value, str):
        return None

    normalized = value.strip()
    if not _INTEGER_PATTERN.fullmatch(normalized):
        return None

    digit_count = len(normalized.lstrip("+-").replace("_", ""))
    max_digits = sys.get_int_max_str_digits()
    if max_digits and digit_count > max_digits:
        return None
    return int(normalized)


def normalize_search_query(value: str | None) -> str | None:
    """Trim/chuyển chữ thường query và coi chuỗi trắng như không có filter tìm kiếm."""

    if isinstance(value, str):
        normalized = value.strip().lower()
        return normalized or None
    return value
