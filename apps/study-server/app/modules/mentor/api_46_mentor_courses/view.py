"""Điều phối truy vấn danh sách course do Mentor trực tiếp sở hữu cho API #46."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import ErrorDetail, success_response
from app.modules.guest._shared.course_catalog.helpers import (
    course_internal_error,
    map_course,
    normalize_course_count,
)
from app.modules.guest._shared.course_catalog.models import CoursePage, Pagination
from app.modules.mentor.api_46_mentor_courses.models import MentorCourseQuery
from app.modules.mentor.api_46_mentor_courses.query import (
    COUNT_MENTOR_COURSES,
    COUNT_MENTOR_COURSES_BY_STATUS,
    LIST_MENTOR_COURSES,
    LIST_MENTOR_COURSES_BY_STATUS,
)
from app.modules.mentor.api_46_mentor_courses.validate import (
    COURSE_STATUS_VALUES,
    validate_mentor_courses_query,
    validate_mentor_request,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_owned_courses(
    db: Session,
    *,
    mentor_id: int,
    page: int,
    size: int,
    status: str | None,
) -> list[dict[str, Any]]:
    """Đọc một trang course theo owner xác thực, thêm status filter tùy chọn và giữ sort ổn định."""
    # Tính offset và chọn câu SQL tĩnh theo status để không ghép dữ liệu query vào SQL.
    offset = (page - 1) * size
    query = LIST_MENTOR_COURSES_BY_STATUS if status is not None else LIST_MENTOR_COURSES
    # Bind numeric owner, phân trang và status tùy chọn cho truy vấn danh sách.
    params: dict[str, Any] = {
        "mentor_id": mentor_id,
        "limit": size,
        "offset": offset,
    }
    if status is not None:
        params["status"] = status
    return query_many(db, query, params)


def count_owned_courses(
    db: Session,
    *,
    mentor_id: int,
    status: str | None,
) -> dict[str, Any]:
    """Đếm course theo cùng owner/status predicates với page query.

    Hàm cũng phát hiện hàng không có Mentor join tương ứng.
    """
    # Dùng cùng predicate owner/status với page query để tổng số khớp tập kết quả.
    query = COUNT_MENTOR_COURSES_BY_STATUS if status is not None else COUNT_MENTOR_COURSES
    params: dict[str, Any] = {"mentor_id": mentor_id}
    if status is not None:
        params["status"] = status
    return query_one(db, query, params) or {"total": 0, "missing_mentor_count": 0}


# API #46 mentor_courses
def get_mentor_courses(
    *,
    authorization: str | None,
    mentor_query: MentorCourseQuery,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, kiểm tra query và dựng response phân trang read-only."""
    # Xác thực bearer, claims và role trước khi kiểm tra query hoặc truy cập DB.
    mentor_id = validate_mentor_request(authorization, trace_id=trace_id)
    if isinstance(mentor_id, JSONResponse):
        return mentor_id

    # Chặn status/page/size ngoài contract trước khi chạy truy vấn.
    validated_query = validate_mentor_courses_query(mentor_query, trace_id=trace_id)
    if isinstance(validated_query, JSONResponse):
        return validated_query

    # Đọc count rồi kiểm tra integrity trước khi lấy trang courses.
    try:
        count_row = count_owned_courses(
            db,
            mentor_id=mentor_id,
            status=validated_query.status,
        )
        missing_mentor_count = normalize_course_count(count_row.get("missing_mentor_count"))
        if isinstance(missing_mentor_count, ErrorDetail):
            # Dọn transaction nếu count row không tuân theo kiểu dữ liệu của truy vấn.
            db.rollback()
            logger.error("Mentor count mapping failed; trace_id=%s", trace_id)
            return course_internal_error(trace_id)
        if missing_mentor_count > 0:
            # Rollback transaction nếu khóa học không có mentor projection bắt buộc.
            db.rollback()
            return course_internal_error(trace_id)
        rows = find_owned_courses(
            db,
            mentor_id=mentor_id,
            page=validated_query.page,
            size=validated_query.size,
            status=validated_query.status,
        )
    except SQLAlchemyError:
        # Dọn transaction lỗi trước khi trả response nội bộ an toàn.
        db.rollback()
        logger.exception("Mentor course lookup failed; trace_id=%s", trace_id)
        return course_internal_error(trace_id)

    # Map rows sang contract dùng chung và tính metadata phân trang.
    try:
        items = []
        for row in rows:
            item = map_course(row)
            if isinstance(item, ErrorDetail):
                logger.error("Mentor course row mapping failed; trace_id=%s", trace_id)
                return course_internal_error(trace_id)
            items.append(item)
        if any(item.status not in COURSE_STATUS_VALUES for item in items):
            logger.error("Mentor course status mapping failed; trace_id=%s", trace_id)
            return course_internal_error(trace_id)
        total = normalize_course_count(count_row.get("total"))
        if isinstance(total, ErrorDetail):
            db.rollback()
            logger.error("Mentor total mapping failed; trace_id=%s", trace_id)
            return course_internal_error(trace_id)
        total_pages = (total + validated_query.size - 1) // validated_query.size if total else 0
        page = CoursePage(
            items=items,
            pagination=Pagination(
                page=validated_query.page,
                size=validated_query.size,
                total=total,
                total_pages=total_pages,
            ),
        )
    except (TypeError, ValidationError):
        logger.exception("Mentor course mapping failed; trace_id=%s", trace_id)
        return course_internal_error(trace_id)

    # Trả envelope thành công; danh sách rỗng vẫn là kết quả hợp lệ.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Mentor courses retrieved." if items else "No courses found.",
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )
