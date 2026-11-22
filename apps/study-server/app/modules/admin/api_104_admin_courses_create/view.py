"""Điều phối quyền Admin, validate Mentor, lưu khóa học và dựng API #104."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from decimal import Decimal
from typing import Any

from app.core.database import query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.modules.admin.api_104_admin_courses_create.query import (
    GET_CREATED_ADMIN_COURSE,
    INSERT_ADMIN_COURSE,
    SELECT_ACTIVE_ADMIN_COURSE_MENTOR,
)
from app.modules.admin.api_104_admin_courses_create.validate import (
    validate_create_admin_course_request,
)
from app.modules.shared.course_catalog.helpers import map_course
from app.modules.shared.course_catalog.models import Course
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho truy vấn, ghi, ánh xạ hoặc commit khóa học."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Course could not be created.",
        trace_id=trace_id,
    )


def _invalid_mentor_response(trace_id: str) -> JSONResponse:
    """Từ chối mentor không tồn tại, không còn hoạt động hoặc không thuộc role Mentor."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=[
            ErrorDetail(
                field="mentor_id",
                code="ACTIVE_MENTOR_REQUIRED",
                message="Chọn một giảng viên hướng dẫn đang hoạt động.",
            )
        ],
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction lỗi mà không thay đổi response ban đầu."""

    try:
        # Hủy mọi thay đổi chưa commit trước khi dependency đóng Session.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin course create rollback failed; trace_id=%s", trace_id)


def _valid_id(value: Any) -> bool:
    """Kiểm tra ID database dương trong miền BIGSERIAL/int64."""

    return type(value) is int and 1 <= value <= MAX_INT64


def create_admin_course(
    *,
    authorization: str | None,
    raw_body: bytes,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Admin rồi tạo khóa học DRAFT cho một Mentor ACTIVE."""

    # Xác thực role ADMIN trước khi parse body hoặc truy cập database.
    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Course could not be created.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    # Kiểm tra cấu trúc và precision trước khi khóa Mentor hay tạo dữ liệu.
    validated_request = validate_create_admin_course_request(raw_body, trace_id=trace_id)
    if isinstance(validated_request, JSONResponse):
        return validated_request
    request, price = validated_request

    try:
        # Khóa dòng Mentor đến khi hoàn tất để role/status không đổi giữa kiểm tra và insert.
        mentor_row = query_one(
            db,
            SELECT_ACTIVE_ADMIN_COURSE_MENTOR,
            {"mentor_id": request.mentor_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course mentor lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if (
        not isinstance(mentor_row, Mapping)
        or type(mentor_row.get("id")) is not int
        or mentor_row.get("id") != request.mentor_id
    ):
        _rollback_safely(db, trace_id=trace_id)
        return _invalid_mentor_response(trace_id)

    try:
        # Lưu các field đã xác thực với trạng thái DRAFT được quyết định cho API #104.
        created_row = query_one(
            db,
            INSERT_ADMIN_COURSE,
            {
                "mentor_id": request.mentor_id,
                "title": request.title,
                "description": request.description,
                "thumbnail_url": request.thumbnail_url,
                "price": price,
            },
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course insert failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not isinstance(created_row, Mapping) or not _valid_id(created_row.get("id")):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course insert returned an invalid ID; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    try:
        # Đọc projection cùng Mentor trước commit để response trùng dữ liệu vừa lưu.
        course_row = query_one(
            db,
            GET_CREATED_ADMIN_COURSE,
            {"course_id": created_row["id"]},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course projection query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not isinstance(course_row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course projection row is missing; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    try:
        course = map_course(dict(course_row))
    except (TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course response mapping raised; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not isinstance(course, Course):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course response mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if (
        course.id != created_row["id"]
        or course.title != request.title
        or course.description != request.description
        or course.thumbnail_url != request.thumbnail_url
        or course.status != "DRAFT"
        or course.mentor.id != request.mentor_id
        or Decimal(course.price) != price
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course response differs from its create request; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    response_data = course.model_dump(mode="json")
    try:
        # Commit chỉ sau khi xác thực response projection đầy đủ.
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course create commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả Course DRAFT được tạo với business code resource-created.
    return success_response(
        business_code="DESIGN_RESOURCE_CREATED",
        message="Course created.",
        trace_id=trace_id,
        data=response_data,
    )
