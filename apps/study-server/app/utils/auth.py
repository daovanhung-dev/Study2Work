"""Cung cấp helper xác thực request, điều phối token và dựng payload auth công khai."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from starlette.responses import JSONResponse

from app.core.config import get_settings
from app.core.responses import ErrorDetail, error_response
from app.core.security.access_token import create_access_token
from app.core.security.access_token import decode_access_token as decode_signed_access_token
from app.core.security.refresh_token import generate_refresh_token, hash_refresh_token
from app.utils.validate import parse_integer, reject_blank_value


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


def validate_refresh_token(value: object) -> object | ErrorDetail:
    """Giữ refresh token hợp lệ hoặc trả ErrorDetail nếu token chỉ có khoảng trắng."""

    return reject_blank_value(value)


def extract_bearer_token(authorization: str | None) -> str | None:
    """Tách Bearer token; trả None nếu header thiếu hoặc sai định dạng."""

    if authorization is None:
        return None

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1]


def validate_access_claims(claims: Mapping[str, Any]) -> tuple[int, list[str]] | None:
    """Chuẩn hóa subject/roles của JWT hoặc trả None khi claims không hợp lệ."""

    subject = claims.get("sub")
    if not isinstance(subject, str) or not subject:
        return None
    user_id = parse_integer(subject)
    if user_id is None or user_id <= 0:
        return None

    raw_roles = claims.get("roles")
    if not isinstance(raw_roles, list) or not raw_roles:
        return None
    if not all(isinstance(role, str) and role.strip() for role in raw_roles):
        return None

    return user_id, [role.strip().upper() for role in raw_roles]


def decode_access_token(token: str) -> dict[str, Any] | JSONResponse:
    """Gọi decoder JWT cấp thấp và ánh xạ lỗi xác minh thành response 401 ở tầng ứng dụng."""

    try:
        return decode_signed_access_token(token)
    except TypeError:
        return _authentication_error()


def validate_current_user_request(
    authorization: str | None,
    *,
    role: str,
    trace_id: str,
    internal_error_message: str = "Profile could not be retrieved.",
) -> tuple[int, list[str]] | JSONResponse:
    """Kiểm tra Bearer/JWT và role caller yêu cầu trước khi truy cập tài nguyên."""

    token = extract_bearer_token(authorization)
    if token is None:
        return _authentication_error(trace_id)

    claims = decode_access_token(token)
    if isinstance(claims, JSONResponse):
        if claims.status_code == 401:
            return _authentication_error(trace_id)
        return _internal_error(trace_id, message=internal_error_message)
    if not isinstance(claims, Mapping):
        return _authentication_error(trace_id)

    validated_claims = validate_access_claims(claims)
    if validated_claims is None:
        return _authentication_error(trace_id)
    user_id, roles = validated_claims

    if role.strip().upper() not in roles:
        return error_response(
            status_code=403,
            business_code="DESIGN_ACCESS_DENIED",
            message="Access denied.",
            trace_id=trace_id,
        )
    return user_id, roles


def _authentication_error(trace_id: str | None = None) -> JSONResponse:
    """Tạo response 401 thống nhất cho request thiếu hoặc sai thông tin xác thực."""

    return error_response(
        status_code=401,
        business_code="DESIGN_AUTHENTICATION_REQUIRED",
        message="Authentication required.",
        trace_id=trace_id,
    )


def _internal_error(
    trace_id: str,
    *,
    message: str = "Profile could not be retrieved.",
) -> JSONResponse:
    """Tạo response 500 an toàn khi cấu hình giải mã token gặp lỗi nội bộ."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message=message,
        trace_id=trace_id,
    )


def issue_tokens(*, user_id: int | str, role: str) -> IssuedTokens | JSONResponse:
    """Tạo access token cho user/role và refresh token opaque, tính hash cùng thời điểm hết hạn
    theo Settings. Trả IssuedTokens gồm token để gửi client, hash để lưu database và thời lượng
    hiệu lực tính bằng giây."""

    settings = get_settings()
    access_token = create_access_token(
        user_id=str(user_id),
        roles=[role],
    )
    if isinstance(access_token, JSONResponse):
        return access_token

    refresh_token = generate_refresh_token()
    refresh_token_hash = hash_refresh_token(refresh_token)
    if isinstance(refresh_token_hash, JSONResponse):
        return refresh_token_hash
    refresh_expires_in = settings.jwt_refresh_token_expire_days * 24 * 60 * 60

    return IssuedTokens(
        access_token=access_token,
        refresh_token=refresh_token,
        refresh_token_hash=refresh_token_hash,
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
