from __future__ import annotations

import logging
from typing import Any

from app.core.database import execute_query, query_one
from app.core.responses import error_response, success_response
from app.core.security import verify_password
from app.core.security.refresh_token import hash_refresh_token
from app.modules.guest.api_03_auth_login.models import LoginRequest, RefreshRequest
from app.modules.guest.api_03_auth_login.query import (
    INSERT_REFRESH_TOKEN,
    LOGIN_USER,
    REFRESH_SESSION,
    REVOKE_REFRESH_TOKEN,
)
from app.modules.guest.api_03_auth_login.validate import (
    validate_login_request,
    validate_refresh_request,
)
from app.utils.auth import build_auth_payload, issue_tokens
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


# API #03 auth_login
def login(
    *,
    user_data: LoginRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Validate credentials, authenticate the user, issue tokens and persist the refresh-token
    hash. Database failures roll back and return a safe API error response."""

    validated_user_data = validate_login_request(user_data, trace_id=trace_id)
    if isinstance(validated_user_data, JSONResponse):
        return validated_user_data
    user_data = validated_user_data

    try:
        user = query_one(db, LOGIN_USER, {"email": user_data.email})
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Login lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id, "Không thể xử lý đăng nhập.")

    if user is None or not verify_password(user_data.password, str(user["password_hash"])):
        return error_response(
            status_code=401,
            business_code="DESIGN_AUTHENTICATION_REQUIRED",
            message="Email hoặc mật khẩu không đúng.",
            trace_id=trace_id,
        )

    if user["status"] != "ACTIVE":
        return error_response(
            status_code=403,
            business_code="DESIGN_ACCESS_DENIED",
            message="Tài khoản không được phép đăng nhập.",
            trace_id=trace_id,
        )

    tokens = issue_tokens(user_id=user["id"], role=str(user["role"]))
    if isinstance(tokens, JSONResponse):
        db.rollback()
        logger.error("Login token issuance failed; trace_id=%s", trace_id)
        return _internal_error(trace_id, "Không thể hoàn tất đăng nhập.")

    try:
        execute_query(
            db,
            INSERT_REFRESH_TOKEN,
            {
                "user_id": user["id"],
                "token_hash": tokens.refresh_token_hash,
                "expires_at": tokens.refresh_expires_at,
            },
        )
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Login token persistence failed; trace_id=%s", trace_id)
        return _internal_error(trace_id, "Không thể hoàn tất đăng nhập.")

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Đăng nhập thành công.",
        trace_id=trace_id,
        data=build_auth_payload(user=user, tokens=tokens),
    )


# API #03 auth_refresh
def refresh(
    *,
    user_data: RefreshRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Validate and rotate a refresh token inside one caller-owned transaction."""

    validated_user_data = validate_refresh_request(user_data, trace_id=trace_id)
    if isinstance(validated_user_data, JSONResponse):
        return validated_user_data
    user_data = validated_user_data

    refresh_hash = hash_refresh_token(user_data.refresh_token)
    if isinstance(refresh_hash, JSONResponse):
        db.rollback()
        logger.error("Refresh-token hashing failed; trace_id=%s", trace_id)
        return _internal_error(trace_id, "Không thể xử lý refresh token.")

    try:
        session = query_one(db, REFRESH_SESSION, {"token_hash": refresh_hash})
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Refresh-token lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id, "Không thể xử lý refresh token.")

    if session is None:
        return error_response(
            status_code=401,
            business_code="DESIGN_AUTHENTICATION_REQUIRED",
            message="Refresh token không hợp lệ hoặc đã hết hạn.",
            trace_id=trace_id,
        )

    if session["status"] != "ACTIVE":
        return error_response(
            status_code=403,
            business_code="DESIGN_ACCESS_DENIED",
            message="Tài khoản không được phép tiếp tục phiên đăng nhập.",
            trace_id=trace_id,
        )

    tokens = issue_tokens(user_id=session["id"], role=str(session["role"]))
    if isinstance(tokens, JSONResponse):
        db.rollback()
        logger.error("Refresh-token issuance failed; trace_id=%s", trace_id)
        return _internal_error(trace_id, "Không thể làm mới phiên đăng nhập.")

    try:
        revoked = execute_query(
            db,
            REVOKE_REFRESH_TOKEN,
            {"refresh_token_id": session["refresh_token_id"]},
        ).first()
        if revoked is None:
            db.rollback()
            return error_response(
                status_code=401,
                business_code="DESIGN_AUTHENTICATION_REQUIRED",
                message="Refresh token không hợp lệ hoặc đã được sử dụng.",
                trace_id=trace_id,
            )

        execute_query(
            db,
            INSERT_REFRESH_TOKEN,
            {
                "user_id": session["id"],
                "token_hash": tokens.refresh_token_hash,
                "expires_at": tokens.refresh_expires_at,
            },
        )
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Refresh-token rotation failed; trace_id=%s", trace_id)
        return _internal_error(trace_id, "Không thể làm mới phiên đăng nhập.")

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Làm mới phiên đăng nhập thành công.",
        trace_id=trace_id,
        data=build_auth_payload(user=session, tokens=tokens),
    )


def _internal_error(trace_id: str, message: str) -> JSONResponse:
    """Return a safe API #3 internal-error response with the request trace ID."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message=message,
        trace_id=trace_id,
    )
