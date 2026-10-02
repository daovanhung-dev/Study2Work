"""Kiểm tra xác thực và input cho API #4 đọc hồ sơ người dùng hiện tại."""

from __future__ import annotations

from app.core.responses import ApiError
from app.core.security.access_token import decode_access_token
from app.utils.validate import extract_bearer_token, validate_access_claims
from starlette.responses import JSONResponse


def validate_current_user_request(
    authorization: str | None,
    *,
    trace_id: str,
) -> tuple[int, list[str]] | JSONResponse:
    """Kiểm tra Bearer/JWT và quyền Student trước khi truy cập database."""

    try:
        token = extract_bearer_token(authorization)
    except ValueError:
        return _authentication_error(trace_id)

    claims = decode_access_token(token)
    if isinstance(claims, JSONResponse):
        if claims.status_code == 401:
            return _authentication_error(trace_id)
        return _internal_error(trace_id)

    try:
        user_id, roles = validate_access_claims(claims)
    except ValueError:
        return _authentication_error(trace_id)

    if "STUDENT" not in roles:
        return ApiError(
            status_code=403,
            business_code="DESIGN_ACCESS_DENIED",
            message="Access denied.",
            trace_id=trace_id,
        )
    return user_id, roles


def _authentication_error(trace_id: str) -> JSONResponse:
    return ApiError(
        status_code=401,
        business_code="DESIGN_AUTHENTICATION_REQUIRED",
        message="Authentication required.",
        trace_id=trace_id,
    )


def _internal_error(trace_id: str) -> JSONResponse:
    return ApiError(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Profile could not be retrieved.",
        trace_id=trace_id,
    )
