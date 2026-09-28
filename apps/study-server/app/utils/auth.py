"""Cung cấp các helper điều phối việc phát hành token và ánh xạ dữ liệu xác thực thành payload
công khai."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from app.core.config import get_settings
from app.core.security.access_token import create_access_token
from app.core.security.refresh_token import generate_refresh_token, hash_refresh_token


@dataclass(frozen=True)
class IssuedTokens:
    """Gom access token, refresh token dạng gốc để trả cho client, hash dùng lưu trữ, thời điểm hết
    hạn và thời lượng hiệu lực của mỗi token."""

    access_token: str
    refresh_token: str
    refresh_token_hash: str
    refresh_expires_at: datetime
    expires_in: int
    refresh_expires_in: int


def issue_tokens(*, user_id: int | str, role: str) -> IssuedTokens:
    """Tạo access token cho user/role và refresh token opaque, tính hash cùng thời điểm hết hạn
    theo Settings. Trả IssuedTokens gồm token để gửi client, hash để lưu database và thời lượng
    hiệu lực tính bằng giây."""

    settings = get_settings()
    access_token = create_access_token(
        user_id=str(user_id),
        roles=[role],
    )
    refresh_token = generate_refresh_token()
    refresh_expires_in = settings.jwt_refresh_token_expire_days * 24 * 60 * 60

    return IssuedTokens(
        access_token=access_token,
        refresh_token=refresh_token,
        refresh_token_hash=hash_refresh_token(refresh_token),
        refresh_expires_at=datetime.now(UTC)
        + timedelta(days=settings.jwt_refresh_token_expire_days),
        expires_in=settings.jwt_access_token_expire_minutes * 60,
        refresh_expires_in=refresh_expires_in,
    )


def build_auth_payload(
    *,
    user: Mapping[str, Any],
    tokens: IssuedTokens,
) -> dict[str, Any]:
    """Chọn các trường profile công khai từ hàng user rồi ghép access token, refresh token và
    metadata bearer vào payload đăng nhập. Hàm không trả password hash hoặc các cột ngoài
    allowlist."""

    profile_fields = (
        "id",
        "full_name",
        "email",
        "role",
        "avatar_url",
        "phone",
        "status",
        "created_at",
        "updated_at",
    )
    payload = {field: user[field] for field in profile_fields}
    payload.update(
        {
            "access_token": tokens.access_token,
            "refresh_token": tokens.refresh_token,
            "token_type": "bearer",
            "expires_in": tokens.expires_in,
            "refresh_expires_in": tokens.refresh_expires_in,
        }
    )
    return payload
