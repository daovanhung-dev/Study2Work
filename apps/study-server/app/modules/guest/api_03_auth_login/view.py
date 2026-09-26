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

# API #03 auth_login
def login(
    *,
    user_data: LoginRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any]:
    """Authenticate a user, persist a refresh session and return auth data."""

    # DD 1.2/2: Nhận request, lấy email để lookup user.
    email = str(user_data.email)
    try:
        # DD 3.1: Lookup user theo email.
        user = query_one(db, LOGIN_USER, {"email": email})
    except SQLAlchemyError as exc:
        # DD 6.3: Query lỗi -> rollback, trả lỗi nội bộ.
        db.rollback()
        logger.exception("Login lookup failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id, "Không thể xử lý đăng nhập.") from exc

    # DD 4.1: Verify password với password_hash.
    if user is None or not verify_password(user_data.password, str(user["password_hash"])):
        # Sai user/password -> 401.
        raise ApiError(
            status_code=401,
            business_code="DESIGN_AUTHENTICATION_REQUIRED",
            message="Email hoặc mật khẩu không đúng.",
            trace_id=trace_id,
        )

    # DD 4.2: Kiểm tra status tài khoản.
    if user["status"] != "ACTIVE":
        # Tài khoản không active -> 403.
        raise ApiError(
            status_code=403,
            business_code="DESIGN_ACCESS_DENIED",
            message="Tài khoản không được phép đăng nhập.",
            trace_id=trace_id,
        )

    try:
        # DD 5.1: Issue access/refresh token.
        tokens = issue_tokens(user_id=user["id"], role=str(user["role"]))
        # Lưu refresh-token hash, không lưu raw token.
        execute_query(
            db,
            INSERT_REFRESH_TOKEN,
            {
                "user_id": user["id"],
                "token_hash": tokens.refresh_token_hash,
                "expires_at": tokens.refresh_expires_at,
            },
        )
        # Commit transaction.
        db.commit()
    except (SQLAlchemyError, TokenError) as exc:
        # DD 6.3: Token/session lỗi -> rollback, trả lỗi nội bộ.
        db.rollback()
        logger.exception("Login token issuance failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id, "Không thể hoàn tất đăng nhập.") from exc

    # DD 6.1: Map profile/token vào success envelope.
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
) -> dict[str, Any]:
    """Rotate a valid refresh session and issue a new access token pair."""

    try:
        # Nhận, hash và lookup refresh session.
        refresh_hash = hash_refresh_token(user_data.refresh_token)
        session = query_one(db, REFRESH_SESSION, {"token_hash": refresh_hash})
    except (SQLAlchemyError, TokenError) as exc:
        # Hash/query lỗi -> rollback, trả lỗi nội bộ.
        db.rollback()
        logger.exception("Refresh-token lookup failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id, "Không thể xử lý refresh token.") from exc

    if session is None:
        # Token không hợp lệ, hết hạn hoặc đã revoke -> 401.
        raise ApiError(
            status_code=401,
            business_code="DESIGN_AUTHENTICATION_REQUIRED",
            message="Refresh token không hợp lệ hoặc đã hết hạn.",
            trace_id=trace_id,
        )

    # Kiểm tra status user.
    if session["status"] != "ACTIVE":
        # Tài khoản không active -> 403.
        raise ApiError(
            status_code=403,
            business_code="DESIGN_ACCESS_DENIED",
            message="Tài khoản không được phép tiếp tục phiên đăng nhập.",
            trace_id=trace_id,
        )

    try:
        # Issue token mới.
        tokens = issue_tokens(user_id=session["id"], role=str(session["role"]))
        # Revoke token cũ.
        revoked = execute_query(
            db,
            REVOKE_REFRESH_TOKEN,
            {"refresh_token_id": session["refresh_token_id"]},
        ).first()
        if revoked is None:
            # Token đã được rotate -> rollback, trả 401.
            db.rollback()
            raise ApiError(
                status_code=401,
                business_code="DESIGN_AUTHENTICATION_REQUIRED",
                message="Refresh token không hợp lệ hoặc đã được sử dụng.",
                trace_id=trace_id,
            )

        # Lưu hash token mới.
        execute_query(
            db,
            INSERT_REFRESH_TOKEN,
            {
                "user_id": session["id"],
                "token_hash": tokens.refresh_token_hash,
                "expires_at": tokens.refresh_expires_at,
            },
        )
        # Commit rotation atomically.
        db.commit()
    except ApiError:
        # Giữ nguyên lỗi nghiệp vụ.
        raise
    except (SQLAlchemyError, TokenError) as exc:
        # Rotation lỗi -> rollback, trả lỗi nội bộ.
        db.rollback()
        logger.exception("Refresh-token rotation failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id, "Không thể làm mới phiên đăng nhập.") from exc

    # Map profile/token vào success envelope.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Làm mới phiên đăng nhập thành công.",
        trace_id=trace_id,
        data=build_auth_payload(user=session, tokens=tokens),
    )


def _internal_error(trace_id: str, message: str) -> ApiError:
    # Tạo lỗi nội bộ an toàn và giữ trace_id.
    return ApiError(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message=message,
        trace_id=trace_id,
    )
