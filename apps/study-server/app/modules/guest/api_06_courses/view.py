from __future__ import annotations

import logging
from decimal import InvalidOperation
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import success_response
from app.modules.guest._shared.course_catalog.helpers import (
    build_order_by,
    course_internal_error,
    map_course,
)
from app.modules.guest._shared.course_catalog.models import CoursePage, Pagination
from app.modules.guest.api_06_courses.models import CourseQuery
from app.modules.guest.api_06_courses.query import (
    COUNT_PUBLISHED_COURSES,
    LIST_PUBLISHED_COURSES,
)
from app.modules.guest.api_06_courses.validate import validate_course_query
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_published_courses(
    db: Session,
    *,
    page: int,
    size: int,
    sort: str | None,
) -> list[dict[str, Any]]:
    """Tính offset từ page và size, dựng ORDER BY bằng helper allowlist rồi truy vấn một trang khóa
    học PUBLISHED cùng mentor projection. Hàm bind status, limit và offset; không commit
    transaction."""

    offset = (page - 1) * size
    query = LIST_PUBLISHED_COURSES.format(order_by=build_order_by(sort))
    return query_many(
        db,
        query,
        {
            "status": "PUBLISHED",
            "limit": size,
            "offset": offset,
        },
    )


def count_published_courses(db: Session) -> dict[str, Any]:
    """Đếm tổng khóa học PUBLISHED và số hàng thiếu mentor bằng truy vấn count. Nếu truy vấn không
    trả hàng, cung cấp mặc định total=0 và missing_mentor_count=0."""

    return query_one(
        db,
        COUNT_PUBLISHED_COURSES,
        {"status": "PUBLISHED"},
    ) or {"total": 0, "missing_mentor_count": 0}


# API #06 courses
def get_courses(
    *,
    course_query: CourseQuery,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Từ chối bộ lọc category chưa có quan hệ dữ liệu được xác nhận, sau đó đếm và lấy trang khóa
    học PUBLISHED. Hàm kiểm tra tính toàn vẹn mentor, ánh xạ model và phân trang, rollback lỗi
    truy vấn và trả envelope thành công an toàn."""

    validated_query = validate_course_query(course_query, trace_id=trace_id)
    if isinstance(validated_query, JSONResponse):
        return validated_query
    course_query = validated_query

    try:
        count_row = count_published_courses(db)
        if int(count_row.get("missing_mentor_count") or 0) > 0:
            db.rollback()
            return course_internal_error(trace_id)
        rows = find_published_courses(
            db,
            page=course_query.page,
            size=course_query.size,
            sort=course_query.sort,
        )
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Course lookup failed; trace_id=%s", trace_id)
        return course_internal_error(trace_id)

    try:
        items = [map_course(row) for row in rows]
        total = int(count_row.get("total") or 0)
        total_pages = (total + course_query.size - 1) // course_query.size if total else 0
        page = CoursePage(
            items=items,
            pagination=Pagination(
                page=course_query.page,
                size=course_query.size,
                total=total,
                total_pages=total_pages,
            ),
        )
    except (InvalidOperation, TypeError, ValueError, ValidationError):
        logger.exception("Course mapping failed; trace_id=%s", trace_id)
        return course_internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Courses retrieved." if items else "No published courses.",
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )
