"""Điều phối xác thực Admin, lưu tài khoản và trả profile an toàn cho API #105."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.core.security.password import hash_password
from app.modules.admin.api_105_admin_users_create.query import (
    CHECK_ADMIN_USER_EMAIL,
    INSERT_ADMIN_USER,
)
from app.modules.admin.api_105_admin_users_create.validate import (
    validate_create_admin_user_request,
)
from app.modules.student.api_04_users_me.models import UserProfile
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Tạo thông báo lỗi chung không tiết lộ cơ sở dữ liệu hoặc credential."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Không thể tạo tài khoản lúc này.",
        trace_id=trace_id,
    )


def _duplicate_email_response(trace_id: str) -> JSONResponse:
    """Trả xung đột khi email đã được dùng bởi một tài khoản khác."""

    return error_response(
        status_code=409,
        business_code="DESIGN_STATE_CONFLICT",
        message="Email đã tồn tại.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Hủy transaction lỗi mà không thay đổi lỗi trả về ban đầu."""

    try:
        # Hủy các thay đổi chưa commit trước khi dependency đóng Session.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin user create rollback failed; trace_id=%s", trace_id)


def _is_email_unique_violation(exc: IntegrityError) -> bool:
    """Nhận diện unique race của users.email theo constraint mặc định PostgreSQL."""

    original = getattr(exc, "orig", None)
    diagnostic = getattr(original, "diag", None)
    return getattr(diagnostic, "constraint_name", None) == "users_email_key"


def _map_created_user(row: Mapping[str, Any] | None) -> UserProfile | None:
    """Kiểm tra projection INSERT trước khi đưa ra response API."""

    if (
        row is None
        or type(row.get("id")) is not int
        or not 1 <= row["id"] <= MAX_INT64
        or row.get("role") not in {"STUDENT", "MENTOR", "ADMIN"}
        or row.get("status") != "ACTIVE"
    ):
        return None

    try:
        return UserProfile.model_validate(row)
    except (TypeError, ValidationError):
        return None


# API #105 admin_users_create
def create_admin_user(
    *,
    authorization: str | None,
    raw_body: bytes,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Yêu cầu role ADMIN rồi tạo user ACTIVE với role đã chọn."""

    # Xác thực Bearer/JWT và role Admin trước khi parse body hoặc mở transaction dữ liệu.
    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Không thể tạo tài khoản lúc này.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    # Chuẩn hóa field và từ chối role/credential không hợp lệ trước truy vấn.
    request = validate_create_admin_user_request(raw_body, trace_id=trace_id)
    if isinstance(request, JSONResponse):
        return request

    try:
        # Tránh băm mật khẩu và insert khi email đã tồn tại.
        existing_user = query_one(db, CHECK_ADMIN_USER_EMAIL, {"email": request.email})
        if existing_user is not None:
            db.rollback()
            return _duplicate_email_response(trace_id)

        # Lưu Argon2id hash cùng role/status đã được kiểm tra.
        created_row = query_one(
            db,
            INSERT_ADMIN_USER,
            {
                "full_name": request.full_name,
                "email": request.email,
                "password_hash": hash_password(request.password),
                "role": request.role,
            },
        )
        created_user = _map_created_user(created_row)
        if created_user is None:
            db.rollback()
            return _internal_error(trace_id)

        # Chỉ commit sau khi projection an toàn đã được xác thực.
        db.commit()
    except IntegrityError as exc:
        # Hoàn tác trước khi ánh xạ unique race thành conflict an toàn.
        _rollback_safely(db, trace_id=trace_id)
        if _is_email_unique_violation(exc):
            return _duplicate_email_response(trace_id)
        logger.error(
            "Admin user insert integrity error; error_type=%s; trace_id=%s",
            type(exc).__name__,
            trace_id,
        )
        return _internal_error(trace_id)
    except SQLAlchemyError as exc:
        # Hoàn tác DB failure và chỉ log loại lỗi + trace ID, không log bind params.
        _rollback_safely(db, trace_id=trace_id)
        logger.error(
            "Admin user insert database error; error_type=%s; trace_id=%s",
            type(exc).__name__,
            trace_id,
        )
        return _internal_error(trace_id)
    except Exception as exc:
        # Bảo vệ credential và response khi hash hoặc projection phát sinh lỗi bất ngờ.
        _rollback_safely(db, trace_id=trace_id)
        logger.error(
            "Admin user create unexpected error; error_type=%s; trace_id=%s",
            type(exc).__name__,
            trace_id,
        )
        return _internal_error(trace_id)

    # Trả profile allowlist, tuyệt đối không đưa password/hash ra ngoài.
    return success_response(
        business_code="DESIGN_RESOURCE_CREATED",
        message="Tạo tài khoản thành công.",
        trace_id=trace_id,
        data=created_user,
    )
