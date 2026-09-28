"""Tạo refresh token ngẫu nhiên, băm token bằng HMAC và so sánh hash theo cách an toàn trước
tấn công thời gian."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Any

from app.core.config import get_settings
from app.core.responses import ApiError


def generate_refresh_token() -> str:
    """Sinh refresh token opaque bằng secrets.token_urlsafe với 48 byte ngẫu nhiên. Trả về chuỗi
    URL-safe để cấp cho client; token gốc không được lưu tại database."""

    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    """Băm refresh token bằng HMAC-SHA256 với pepper cấu hình trước khi lưu database. Trả về digest
    dạng hex; thiếu pepper sẽ phát sinh ApiError an toàn."""

    pepper = _get_refresh_token_pepper()

    return hmac.new(
        pepper.encode("utf-8"),
        token.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def compare_refresh_token(
    token: str,
    stored_hash: str,
) -> bool:
    """Băm lại token nhận được rồi so sánh digest với hash đã lưu bằng hmac.compare_digest. Cách so
    sánh này giảm rò rỉ thông tin qua thời gian xử lý và trả về kết quả đúng/sai."""

    token_hash = hash_refresh_token(token)

    return hmac.compare_digest(
        token_hash,
        stored_hash,
    )


def _get_refresh_token_pepper() -> str:
    """Đọc pepper refresh token từ Settings và mở SecretStr nếu cần. Nếu pepper chưa được cấu hình,
    phát sinh ApiError mặc định để không băm token bằng khóa rỗng."""
    settings = get_settings()

    pepper = _secret_value(
        settings.refresh_token_pepper,
    )

    if not pepper:
        raise ApiError()

    return pepper


def _secret_value(value: Any) -> str | None:
    """Lấy giá trị chuỗi từ cấu hình có thể là SecretStr. Trả None khi đầu vào vắng mặt, mở
    get_secret_value khi có phương thức đó và chuyển kiểu khác thành str."""
    if value is None:
        return None

    if hasattr(value, "get_secret_value"):
        secret_value = value.get_secret_value()
        return None if secret_value is None else str(secret_value)

    return str(value)
