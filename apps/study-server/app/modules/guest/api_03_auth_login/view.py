from __future__ import annotations

import logging
from typing import Any

# Nhập các thành phần từ core.
from app.core.database import execute_query, query_one
from app.core.responses import ApiError, _ApiError, success_response
from app.core.security import verify_password
from app.core.security.refresh_token import hash_refresh_token

# Nhập các thành phần từ những thư mục của ứng dụng.
from app.modules.guest.api_03_auth_login.models import LoginRequest, RefreshRequest
from app.modules.guest.api_03_auth_login.query import (
    INSERT_REFRESH_TOKEN,
    LOGIN_USER,
    REFRESH_SESSION,
    REVOKE_REFRESH_TOKEN,
)
from app.utils.auth import build_auth_payload, issue_tokens

# Nhập các thành phần cần thiết từ SQLAlchemy.
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
    """Xác thực email và mật khẩu, từ chối tài khoản không hoạt động, phát hành access/refresh
    token rồi lưu hash refresh token trong Session. Hàm commit khi thành công, rollback và ánh
    xạ lỗi truy vấn/cấp token thành lỗi API an toàn; response chỉ trả payload xác thực công
    khai."""

    # DD 1.2/2: Nhận yêu cầu và lấy email để tra cứu người dùng.
    email = str(user_data.email)
    try:
        # DD 3.1: Tra cứu người dùng theo email.
        user = query_one(db, LOGIN_USER, {"email": email})
    except SQLAlchemyError as exc:
        # DD 6.3: Truy vấn lỗi → hoàn tác giao dịch và trả lỗi nội bộ.
        db.rollback()
        logger.exception("Login lookup failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id, "Không thể xử lý đăng nhập.") from exc

    # DD 4.1: Xác minh mật khẩu với password_hash.
    if user is None or not verify_password(user_data.password, str(user["password_hash"])):
        # Tài khoản hoặc mật khẩu sai → 401.
        raise ApiError(
            status_code=401,
            business_code="DESIGN_AUTHENTICATION_REQUIRED",
            message="Email hoặc mật khẩu không đúng.",
            trace_id=trace_id,
        )

    # DD 4.2: Kiểm tra trạng thái tài khoản.
    if user["status"] != "ACTIVE":
        # Tài khoản chưa hoạt động → 403.
        raise ApiError(
            status_code=403,
            business_code="DESIGN_ACCESS_DENIED",
            message="Tài khoản không được phép đăng nhập.",
            trace_id=trace_id,
        )

    try:
        # DD 5.1: Phát hành access token và refresh token.
        tokens = issue_tokens(user_id=user["id"], role=str(user["role"]))
        # Lưu bản băm refresh token, không lưu token gốc.
        execute_query(
            db,
            INSERT_REFRESH_TOKEN,
            {
                "user_id": user["id"],
                "token_hash": tokens.refresh_token_hash,
                "expires_at": tokens.refresh_expires_at,
            },
        )
        # Xác nhận giao dịch.
        db.commit()
    except (SQLAlchemyError, _ApiError) as exc:
        # DD 6.3: Lỗi phát hành token hoặc lưu phiên → hoàn tác giao dịch và trả lỗi nội bộ.
        db.rollback()
        logger.exception("Login token issuance failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id, "Không thể hoàn tất đăng nhập.") from exc

    # DD 6.1: Đưa hồ sơ và token vào cấu trúc phản hồi thành công.
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
    """Băm và tra cứu refresh token, xác nhận session/user còn hoạt động, thu hồi token cũ rồi lưu
    hash token mới trong cùng transaction. Hàm rollback nếu token đã bị dùng, lỗi database hoặc
    cấu hình; lỗi xác thực dưới 500 được giữ nguyên, còn thành công trả cặp token mới."""

    try:
        # Nhận token, băm token và tra cứu phiên refresh.
        refresh_hash = hash_refresh_token(user_data.refresh_token)
        session = query_one(db, REFRESH_SESSION, {"token_hash": refresh_hash})
    except (SQLAlchemyError, _ApiError) as exc:
        # Lỗi băm hoặc truy vấn → hoàn tác giao dịch và trả lỗi nội bộ.
        db.rollback()
        logger.exception("Refresh-token lookup failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id, "Không thể xử lý refresh token.") from exc

    if session is None:
        # Token không hợp lệ, hết hạn hoặc đã thu hồi → 401.
        raise ApiError(
            status_code=401,
            business_code="DESIGN_AUTHENTICATION_REQUIRED",
            message="Refresh token không hợp lệ hoặc đã hết hạn.",
            trace_id=trace_id,
        )

    # Kiểm tra trạng thái người dùng.
    if session["status"] != "ACTIVE":
        # Tài khoản chưa hoạt động → 403.
        raise ApiError(
            status_code=403,
            business_code="DESIGN_ACCESS_DENIED",
            message="Tài khoản không được phép tiếp tục phiên đăng nhập.",
            trace_id=trace_id,
        )

    try:
        # Phát hành token mới.
        tokens = issue_tokens(user_id=session["id"], role=str(session["role"]))
        # Thu hồi token cũ.
        revoked = execute_query(
            db,
            REVOKE_REFRESH_TOKEN,
            {"refresh_token_id": session["refresh_token_id"]},
        ).first()
        if revoked is None:
            # Token đã được xoay vòng → hoàn tác giao dịch và trả 401.
            db.rollback()
            raise ApiError(
                status_code=401,
                business_code="DESIGN_AUTHENTICATION_REQUIRED",
                message="Refresh token không hợp lệ hoặc đã được sử dụng.",
                trace_id=trace_id,
            )

        # Lưu bản băm của token mới.
        execute_query(
            db,
            INSERT_REFRESH_TOKEN,
            {
                "user_id": session["id"],
                "token_hash": tokens.refresh_token_hash,
                "expires_at": tokens.refresh_expires_at,
            },
        )
        # Xác nhận việc xoay vòng token trong cùng giao dịch.
        db.commit()
    except _ApiError as exc:
        # Giữ nguyên lỗi nghiệp vụ 401; chuyển lỗi cấu hình thành lỗi nội bộ của API.
        db.rollback()
        if exc.status_code < 500:
            raise
        logger.exception("Refresh-token rotation failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id, "Không thể làm mới phiên đăng nhập.") from exc
    except SQLAlchemyError as exc:
        # Lỗi CSDL → hoàn tác giao dịch và trả lỗi nội bộ.
        db.rollback()
        logger.exception("Refresh-token rotation failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id, "Không thể làm mới phiên đăng nhập.") from exc

    # Đưa hồ sơ và token vào cấu trúc phản hồi thành công.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Làm mới phiên đăng nhập thành công.",
        trace_id=trace_id,
        data=build_auth_payload(user=session, tokens=tokens),
    )


def _internal_error(trace_id: str, message: str) -> _ApiError:
    # Tạo lỗi nội bộ an toàn và giữ trace_id.
    """Tạo _ApiError HTTP 500 cho lỗi nội bộ của API #3, giữ business code thiết kế, thông điệp do
    caller cung cấp và trace ID request."""
    return ApiError(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message=message,
        trace_id=trace_id,
    )
