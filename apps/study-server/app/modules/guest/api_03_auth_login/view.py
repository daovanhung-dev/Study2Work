from __future__ import annotations

import logging
from typing import Any

import app.utils.auth as auth_utils
from app.core.database import execute_query, query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.core.security import verify_password
from app.modules.guest.api_03_auth_login.models import LoginRequest, RefreshRequest
from app.modules.guest.api_03_auth_login.query import (
    INSERT_REFRESH_TOKEN,
    LOGIN_USER,
    REFRESH_SESSION,
    REVOKE_REFRESH_TOKEN,
)
from app.modules.guest.api_03_auth_login.validate import validate_login_request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, Response

logger = logging.getLogger(__name__)


# API #03 auth_login
def login(
    *,
    user_data: LoginRequest,
    db: Session,
    trace_id: str,
    response: Response | None = None,
    cookie_secure: bool | None = None,
    existing_refresh_token: str | None = None,
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

    tokens = auth_utils.issue_tokens(user_id=user["id"], role=str(user["role"]))
    if isinstance(tokens, JSONResponse):
        db.rollback()
        logger.error("Login token issuance failed; trace_id=%s", trace_id)
        return _internal_error(trace_id, "Không thể hoàn tất đăng nhập.")

    try:
        if existing_refresh_token:
            existing_hash = auth_utils.hash_refresh_token(existing_refresh_token)
            if isinstance(existing_hash, JSONResponse):
                db.rollback()
                return _internal_error(trace_id, "Không thể hoàn tất đăng nhập.")
            existing_session = query_one(db, REFRESH_SESSION, {"token_hash": existing_hash})
            if existing_session is not None:
                execute_query(
                    db,
                    REVOKE_REFRESH_TOKEN,
                    {"refresh_token_id": existing_session["refresh_token_id"]},
                )
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

    if response is not None:
        auth_utils.set_refresh_cookie(response, tokens, secure=cookie_secure)

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Đăng nhập thành công.",
        trace_id=trace_id,
        data=auth_utils.build_auth_payload(user=user, tokens=tokens),
    )


# API #03 auth_refresh
def refresh(
    *,
    user_data: RefreshRequest | None = None,
    refresh_token: str | None = None,
    db: Session,
    trace_id: str,
    response: Response | None = None,
    cookie_secure: bool | None = None,
) -> dict[str, Any] | JSONResponse:
    """Validate and rotate a refresh token inside one caller-owned transaction."""

    token_value = refresh_token
    if token_value is None and user_data is not None:
        token_value = user_data.refresh_token
    validated_token = auth_utils.validate_refresh_token(token_value)
    if isinstance(validated_token, ErrorDetail):
        return error_response(
            status_code=401,
            business_code="DESIGN_AUTHENTICATION_REQUIRED",
            message="Refresh token không hợp lệ hoặc đã hết hạn.",
            trace_id=trace_id,
        )

    refresh_hash = auth_utils.hash_refresh_token(str(validated_token))
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

    tokens = auth_utils.issue_tokens(user_id=session["id"], role=str(session["role"]))
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

    if response is not None:
        auth_utils.set_refresh_cookie(response, tokens, secure=cookie_secure)

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Làm mới phiên đăng nhập thành công.",
        trace_id=trace_id,
        data=auth_utils.build_auth_payload(user=session, tokens=tokens),
    )


def logout(
    *,
    refresh_token: str | None,
    db: Session,
    trace_id: str,
    response: Response | None = None,
    cookie_secure: bool | None = None,
) -> JSONResponse | None:
    """Revoke the cookie-backed refresh session; repeated logout is safe."""

    if not refresh_token or not refresh_token.strip():
        if response is not None:
            auth_utils.clear_refresh_cookie(response, secure=cookie_secure)
        return None

    refresh_hash = auth_utils.hash_refresh_token(refresh_token)
    if isinstance(refresh_hash, JSONResponse):
        db.rollback()
        return refresh_hash

    try:
        session = query_one(db, REFRESH_SESSION, {"token_hash": refresh_hash})
        if session is None:
            db.rollback()
            if response is not None:
                auth_utils.clear_refresh_cookie(response, secure=cookie_secure)
            return None

        execute_query(db, REVOKE_REFRESH_TOKEN, {"refresh_token_id": session["refresh_token_id"]})
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Logout refresh-token revocation failed; trace_id=%s", trace_id)
        return _internal_error(trace_id, "Không thể kết thúc phiên đăng nhập.")

    if response is not None:
        auth_utils.clear_refresh_cookie(response, secure=cookie_secure)
    return None


def _internal_error(trace_id: str, message: str) -> JSONResponse:
    """Return a safe API #3 internal-error response with the request trace ID."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message=message,
        trace_id=trace_id,
    )
