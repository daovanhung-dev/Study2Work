"""Tạo và xác minh JWT access token theo thuật toán, issuer và audience trong cấu hình Study."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import jwt
from jwt.exceptions import InvalidTokenError
from starlette.responses import JSONResponse

from app.core.config import get_settings
from app.core.responses import error_response

ACCESS_TOKEN_TYPE = "access"

RESERVED_CLAIMS = {
    "sub",
    "type",
    "jti",
    "iat",
    "exp",
    "iss",
    "aud",
}


def create_access_token(
    *,
    user_id: str,
    roles: list[str] | None = None,
    claims: Mapping[str, Any] | None = None,
) -> str | JSONResponse:
    """Tạo payload access JWT từ user ID, danh sách role và claim bổ sung, sau đó ký bằng khóa theo
    thuật toán đang cấu hình. Payload luôn có sub, type, jti, iat, exp, iss và aud; claim tùy
    chỉnh không được ghi đè các claim dành riêng. Trả token đã mã hóa hoặc JSONResponse lỗi nếu
    thiếu khóa ký."""

    settings = get_settings()
    now = datetime.now(UTC)

    payload: dict[str, Any] = {
        "sub": user_id,
        "type": ACCESS_TOKEN_TYPE,
        "roles": roles or [],
        "jti": str(uuid4()),
        "iat": now,
        "exp": now
        + timedelta(
            minutes=settings.jwt_access_token_expire_minutes,
        ),
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
    }

    _add_custom_claims(
        payload=payload,
        claims=claims,
    )

    signing_key = _get_signing_key()
    if isinstance(signing_key, JSONResponse):
        return signing_key

    return jwt.encode(
        payload,
        signing_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(
    token: str,
) -> dict[str, Any] | JSONResponse:
    """Giải mã và kiểm tra access JWT bằng khóa, thuật toán, issuer và audience hiện hành. Hàm yêu
    cầu các claim bắt buộc, kiểm tra type là access và sub là chuỗi không rỗng; token sai hoặc
    hết hạn được ánh xạ thành lỗi xác thực 401."""

    settings = get_settings()
    verification_key = _get_verification_key()
    if isinstance(verification_key, JSONResponse):
        return verification_key

    try:
        payload = jwt.decode(
            token,
            verification_key,
            algorithms=[settings.jwt_algorithm],
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
            options={
                "require": [
                    "sub",
                    "type",
                    "jti",
                    "iat",
                    "exp",
                    "iss",
                    "aud",
                ],
            },
        )
    except (
        InvalidTokenError,
        TypeError,
        ValueError,
    ):
        return _invalid_access_token()

    if payload.get("type") != ACCESS_TOKEN_TYPE:
        return _invalid_access_token()

    user_id = payload.get("sub")

    if not isinstance(user_id, str) or not user_id:
        return _invalid_access_token()

    return payload


def _add_custom_claims(
    *,
    payload: dict[str, Any],
    claims: Mapping[str, Any] | None,
) -> None:
    """Chép các claim tùy chỉnh vào payload khi caller có cung cấp. Bỏ qua mọi khóa thuộc
    RESERVED_CLAIMS để dữ liệu bổ sung không thay đổi danh tính, loại token, thời hạn hoặc nguồn
    phát hành."""
    if not claims:
        return

    for key, value in claims.items():
        if key not in RESERVED_CLAIMS:
            payload[key] = value


def _get_signing_key() -> str | JSONResponse:
    """Chọn khóa ký theo thuật toán JWT: private key cho ES256 hoặc secret key cho HS256. Hàm mở
    SecretStr nếu cần và trả error_response mặc định an toàn khi khóa bắt buộc bị thiếu."""
    settings = get_settings()

    if settings.jwt_algorithm == "ES256":
        private_key = _secret_value(settings.jwt_private_key)

        if not private_key:
            return error_response()

        return private_key

    secret_key = _secret_value(settings.jwt_secret_key)

    if not secret_key:
        return error_response()

    return secret_key


def _get_verification_key() -> str | JSONResponse:
    """Chọn khóa xác minh theo thuật toán JWT: public key cho ES256 hoặc secret key cho HS256. Hàm
    mở giá trị secret theo cấu hình và trả error_response an toàn nếu không có khóa."""
    settings = get_settings()

    if settings.jwt_algorithm == "ES256":
        public_key = _secret_value(settings.jwt_public_key)

        if not public_key:
            return error_response()

        return public_key

    secret_key = _secret_value(settings.jwt_secret_key)

    if not secret_key:
        return error_response()

    return secret_key


def _secret_value(value: Any) -> str | None:
    """Chuẩn hóa giá trị bí mật thành chuỗi có thể dùng bởi thư viện JWT. Trả None nếu đầu vào là
    None, mở đối tượng có get_secret_value, còn giá trị khác được chuyển bằng str."""
    if value is None:
        return None

    if hasattr(value, "get_secret_value"):
        secret_value = value.get_secret_value()
        return None if secret_value is None else str(secret_value)

    return str(value)


def _invalid_access_token() -> JSONResponse:
    """Tạo response HTTP 401 thống nhất khi access token không hợp lệ hoặc hết hạn."""
    return error_response(
        status_code=401,
        business_code="DESIGN_AUTHENTICATION_REQUIRED",
        message="Token không hợp lệ hoặc đã hết hạn.",
    )
