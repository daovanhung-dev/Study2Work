"""Xử lý nghiệp vụ và điều phối dữ liệu cho API #8 chi tiết khóa học."""

from __future__ import annotations

import logging
from decimal import InvalidOperation
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.guest._shared.course_catalog.helpers import (
    course_internal_error,
    map_course,
)
from app.modules.guest._shared.course_catalog.models import CoursePage, Pagination
from app.modules.guest.api_08_courses_detail.query import FIND_PUBLISHED_COURSE_DETAIL
from app.modules.guest.api_08_courses_detail.validate import validate_course_id
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_published_course_detail(
    db: Session,
    *,
    course_id: int,
) -> dict[str, Any] | None:
    """Truy vấn một bản ghi khóa học ở trạng thái PUBLISHED kèm thông tin mentor."""
    return query_one(
        db,
        FIND_PUBLISHED_COURSE_DETAIL,
        {
            "course_id": course_id,
            "status": "PUBLISHED",
        },
    )


def _course_not_found_error(trace_id: str) -> JSONResponse:
    """Tạo response lỗi 404 chuẩn khi không tìm thấy khóa học hoặc khóa học chưa publish."""
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Published course not found.",
        trace_id=trace_id,
    )


# API #08 get_course_detail
def get_course_detail(
    *,
    course_id_raw: str | int,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Trả về thông tin chi tiết của một khóa học đã publish."""

    # Xác thực course_id; định dạng không hợp lệ sẽ trả về 404 theo DD #08.
    validated_course_id = validate_course_id(course_id_raw, trace_id=trace_id)
    if isinstance(validated_course_id, JSONResponse):
        return validated_course_id
    course_id = validated_course_id

    # Truy vấn chi tiết khóa học đã publish kèm mentor.
    try:
        row = find_published_course_detail(db, course_id=course_id)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Course detail lookup failed; trace_id=%s", trace_id)
        return course_internal_error(trace_id)

    # Trả về 404 nếu khóa học không tồn tại hoặc không ở trạng thái PUBLISHED.
    if row is None:
        return _course_not_found_error(trace_id)

    # Ánh xạ các trường của khóa học và tạo response CoursePage singleton.
    try:
        item = map_course(row)
        page = CoursePage(
            items=[item],
            pagination=Pagination(
                page=1,
                size=1,
                total=1,
                total_pages=1,
            ),
        )
    except (InvalidOperation, TypeError, ValueError, ValidationError):
        logger.exception("Course detail mapping failed; trace_id=%s", trace_id)
        return course_internal_error(trace_id)

    # Trả về response thành công chuẩn.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Course retrieved.",
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )