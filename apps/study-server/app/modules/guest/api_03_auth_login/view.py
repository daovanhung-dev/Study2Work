from __future__ import annotations

import logging
from typing import Any

# import core's file
from app.core.database import execute_query, query_one
from app.core.responses import ApiError, success_response
from app.core.security import TokenError, verify_password
from app.core.security.refresh_token import hash_refresh_token

# import folder's files
from app.modules.guest.api_03_auth_login.models import LoginRequest, RefreshRequest
from app.modules.guest.api_03_auth_login.query import (
    INSERT_REFRESH_TOKEN,
    LOGIN_USER,
    REFRESH_SESSION,
    REVOKE_REFRESH_TOKEN,
)
from app.utils.auth import build_auth_payload, issue_tokens

# import framework
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def login(
    *,
    user_data: LoginRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any]:
    """Authenticate a user, persist a refresh session and return auth data."""

    email = str(user_data.email)
    try:
        user = query_one(db, LOGIN_USER, {"email": email})
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Login lookup failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id, "Không thể xử lý đăng nhập.") from exc

    if user is None or not verify_password(user_data.password, str(user["password_hash"])):
        raise ApiError(
            status_code=401,
            business_code="DESIGN_AUTHENTICATION_REQUIRED",
            message="Email hoặc mật khẩu không đúng.",
            trace_id=trace_id,
        )

    if user["status"] != "ACTIVE":
        raise ApiError(
            status_code=403,
            business_code="DESIGN_ACCESS_DENIED",
            message="Tài khoản không được phép đăng nhập.",
            trace_id=trace_id,
        )

    try:
        tokens = issue_tokens(user_id=user["id"], role=str(user["role"]))
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
    except (SQLAlchemyError, TokenError) as exc:
        db.rollback()
        logger.exception("Login token issuance failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id, "Không thể hoàn tất đăng nhập.") from exc

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Đăng nhập thành công.",
        trace_id=trace_id,
        data=build_auth_payload(user=user, tokens=tokens),
    )


def refresh(
    *,
    user_data: RefreshRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any]:
    """Rotate a valid refresh session and issue a new access token pair."""

    try:
        refresh_hash = hash_refresh_token(user_data.refresh_token)
        session = query_one(db, REFRESH_SESSION, {"token_hash": refresh_hash})
    except (SQLAlchemyError, TokenError) as exc:
        db.rollback()
        logger.exception("Refresh-token lookup failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id, "Không thể xử lý refresh token.") from exc

    if session is None:
        raise ApiError(
            status_code=401,
            business_code="DESIGN_AUTHENTICATION_REQUIRED",
            message="Refresh token không hợp lệ hoặc đã hết hạn.",
            trace_id=trace_id,
        )

    if session["status"] != "ACTIVE":
        raise ApiError(
            status_code=403,
            business_code="DESIGN_ACCESS_DENIED",
            message="Tài khoản không được phép tiếp tục phiên đăng nhập.",
            trace_id=trace_id,
        )

    try:
        tokens = issue_tokens(user_id=session["id"], role=str(session["role"]))
        revoked = execute_query(
            db,
            REVOKE_REFRESH_TOKEN,
            {"refresh_token_id": session["refresh_token_id"]},
        ).first()
        if revoked is None:
            db.rollback()
            raise ApiError(
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
    except ApiError:
        raise
    except (SQLAlchemyError, TokenError) as exc:
        db.rollback()
        logger.exception("Refresh-token rotation failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id, "Không thể làm mới phiên đăng nhập.") from exc

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Làm mới phiên đăng nhập thành công.",
        trace_id=trace_id,
        data=build_auth_payload(user=session, tokens=tokens),
    )


def _internal_error(trace_id: str, message: str) -> ApiError:
    return ApiError(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message=message,
        trace_id=trace_id,
    )
