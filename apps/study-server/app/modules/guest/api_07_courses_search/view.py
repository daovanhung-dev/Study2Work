from __future__ import annotations

import logging
from decimal import InvalidOperation
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import success_response
from app.modules.guest._shared.course_catalog.constants import DEFAULT_SIZE
from app.modules.guest._shared.course_catalog.helpers import (
    build_order_by,
    course_internal_error,
    map_course,
)
from app.modules.guest._shared.course_catalog.models import CoursePage, Pagination
from app.modules.guest.api_07_courses_search.models import CourseSearchQuery
from app.modules.guest.api_07_courses_search.query import (
    COUNT_SEARCHED_COURSES,
    LIST_SEARCHED_COURSES,
)
from app.modules.guest.api_07_courses_search.validate import validate_course_search_query
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_published_courses_search(
    db: Session,
    *,
    q: str | None,
    page: int,
    sort: str | None,
) -> list[dict[str, Any]]:
    """Tính offset theo page và kích thước cố định DEFAULT_SIZE, dựng ORDER BY qua allowlist rồi
    truy vấn các khóa học PUBLISHED khớp từ khóa tùy chọn. Giá trị tìm kiếm được bind thành
    q_pattern; không commit transaction."""

    offset = (page - 1) * DEFAULT_SIZE
    query = LIST_SEARCHED_COURSES.format(order_by=build_order_by(sort))
    return query_many(
        db,
        query,
        {
            "status": "PUBLISHED",
            "q_pattern": f"%{q}%" if q else None,
            "limit": DEFAULT_SIZE,
            "offset": offset,
        },
    )


def count_published_courses_search(
    db: Session,
    *,
    q: str | None,
) -> dict[str, Any]:
    """Đếm khóa học PUBLISHED khớp cùng điều kiện từ khóa và kiểm tra số hàng thiếu mentor. Trả mặc
    định tổng bằng 0 nếu truy vấn không có hàng."""

    return query_one(
        db,
        COUNT_SEARCHED_COURSES,
        {
            "status": "PUBLISHED",
            "q_pattern": f"%{q}%" if q else None,
        },
    ) or {"total": 0, "missing_mentor_count": 0}


# API #07 courses_search
def search_courses(
    *,
    course_query: CourseSearchQuery,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Từ chối category chưa được hỗ trợ, đếm kết quả và lấy trang khóa học PUBLISHED theo từ khóa
    đã chuẩn hóa. Hàm kiểm tra mentor, ánh xạ kết quả, tạo phân trang kích thước cố định,
    rollback lỗi database/mapping và trả envelope thành công."""

    validated_query = validate_course_search_query(course_query, trace_id=trace_id)
    if isinstance(validated_query, JSONResponse):
        return validated_query
    course_query = validated_query

    try:
        count_row = count_published_courses_search(db, q=course_query.q)
        if int(count_row.get("missing_mentor_count") or 0) > 0:
            db.rollback()
            return course_internal_error(trace_id)
        rows = find_published_courses_search(
            db,
            q=course_query.q,
            page=course_query.page,
            sort=course_query.sort,
        )
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Course search failed; trace_id=%s", trace_id)
        return course_internal_error(trace_id)

    try:
        items = [map_course(row) for row in rows]
        total = int(count_row.get("total") or 0)
        total_pages = (total + DEFAULT_SIZE - 1) // DEFAULT_SIZE if total else 0
        page = CoursePage(
            items=items,
            pagination=Pagination(
                page=course_query.page,
                size=DEFAULT_SIZE,
                total=total,
                total_pages=total_pages,
            ),
        )
    except (InvalidOperation, TypeError, ValueError, ValidationError):
        db.rollback()
        logger.exception("Course search mapping failed; trace_id=%s", trace_id)
        return course_internal_error(trace_id)

    message = "Courses search completed." if items else "No published courses matched the search."
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message=message,
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )
