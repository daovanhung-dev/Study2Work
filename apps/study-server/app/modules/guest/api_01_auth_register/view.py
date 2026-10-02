from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_one
from app.core.responses import ApiError, success_response
from app.core.security.password import hash_password
from app.modules.guest.api_01_auth_register.models import RegisterRequest
from app.modules.guest.api_01_auth_register.query import CHECK_DUPLICATE, INSERT_USER
from app.modules.guest.api_01_auth_register.validate import validate_register_request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_user_by_email(db: Session, email: str) -> dict[str, Any] | None:
    """Truy vấn theo email để tìm tài khoản đã tồn tại và trả về hàng người dùng nếu có. Hàm dùng
    câu SQL CHECK_DUPLICATE với tham số bind, không commit transaction."""

    return query_one(db, CHECK_DUPLICATE, {"email": email})


def insert_user(
    db: Session,
    *,
    full_name: str,
    email: str,
    password_hash: str,
) -> dict[str, Any] | None:
    """Thực thi câu INSERT_USER bằng full name, email và password hash đã chuẩn bị. Trả về các
    trường profile được truy vấn nếu insert thành công, hoặc None khi không có hàng trả về;
    transaction thuộc caller."""

    return query_one(
        db,
        INSERT_USER,
        {
            "full_name": full_name,
            "email": email,
            "password_hash": password_hash,
        },
    )


# API #01 auth_register
def create_user(
    *,
    user_data: RegisterRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Điều phối đăng ký: kiểm tra email trùng, băm mật khẩu, chèn tài khoản và commit trong
    Session do caller sở hữu. Hàm rollback khi lỗi, ánh xạ unique race/DB error thành ApiError
    an toàn, ghi log nội bộ và trả success envelope chỉ chứa profile công khai."""

    validated_user_data = validate_register_request(user_data, trace_id=trace_id)
    if isinstance(validated_user_data, JSONResponse):
        return validated_user_data

    user_data = validated_user_data
    email = user_data.email

    try:
        if find_user_by_email(db, email) is not None:
            db.rollback()
            return ApiError(
                status_code=409,
                business_code="DESIGN_STATE_CONFLICT",
                message="Email đã tồn tại.",
                trace_id=trace_id,
            )

        created_user = insert_user(
            db,
            full_name=user_data.full_name,
            email=email,
            password_hash=hash_password(user_data.password),
        )
        if created_user is None:
            db.rollback()
            return ApiError(
                status_code=500,
                business_code="DESIGN_INTERNAL_ERROR",
                message="Không thể tạo tài khoản.",
                trace_id=trace_id,
            )

        db.commit()
    except IntegrityError as exc:
        db.rollback()
        if _is_email_unique_violation(exc):
            return ApiError(
                status_code=409,
                business_code="DESIGN_STATE_CONFLICT",
                message="Email đã tồn tại.",
                trace_id=trace_id,
            )
        logger.exception("Account insert integrity error; trace_id=%s", trace_id)
        return ApiError(
            status_code=500,
            business_code="DESIGN_INTERNAL_ERROR",
            message="Không thể tạo tài khoản.",
            trace_id=trace_id,
        )
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Account insert database error; trace_id=%s", trace_id)
        return ApiError(
            status_code=500,
            business_code="DESIGN_INTERNAL_ERROR",
            message="Không thể tạo tài khoản.",
            trace_id=trace_id,
        )

    logger.info(
        "Verification dispatch deferred after account creation; trace_id=%s",
        trace_id,
        extra={"event": "verification_dispatch_pending", "user_id": created_user["id"]},
    )

    return success_response(
        business_code="DESIGN_RESOURCE_CREATED",
        message="Tạo tài khoản thành công.",
        trace_id=trace_id,
        data=created_user,
    )


def _is_email_unique_violation(exc: IntegrityError) -> bool:
    """Đọc constraint name từ IntegrityError.orig.diag và trả True khi lỗi đến từ users_email_key.
    Kết quả giúp create_user phân biệt race email trùng với lỗi integrity khác."""
    original = getattr(exc, "orig", None)
    diagnostic = getattr(original, "diag", None)
    return getattr(diagnostic, "constraint_name", None) == "users_email_key"
