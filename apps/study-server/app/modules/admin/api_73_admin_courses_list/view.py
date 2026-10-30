"""Điều phối quyền Admin, truy vấn và dựng response danh sách khóa học API #73."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.modules.admin.api_73_admin_courses_list.models import (
    AdminCoursesQuery,
)
from app.modules.admin.api_73_admin_courses_list.query import (
    COUNT_ADMIN_COURSES,
    LIST_ADMIN_COURSES,
)
from app.modules.admin.api_73_admin_courses_list.validate import (
    validate_admin_courses_query,
    validate_admin_request,
)
from app.modules.guest._shared.course_catalog.helpers import map_course, normalize_course_count
from app.modules.guest._shared.course_catalog.models import CoursePage, Pagination
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
DEFAULT_PAGE_SIZE = 20
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho query hoặc ánh xạ danh sách khóa học."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Courses could not be retrieved.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc lỗi mà không che response lỗi ban đầu."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin courses rollback failed; trace_id=%s", trace_id)


def _query_parameters(query: AdminCoursesQuery) -> dict[str, Any]:
    """Gom các predicate chung để count và page dùng cùng một tập filter."""

    return {"status": query.status, "mentor": query.mentor}


def _normalize_count_row(
    count_row: Any,
    *,
    trace_id: str,
) -> tuple[int, int] | None:
    """Kiểm tra count projection và trả total cùng số course thiếu mentor."""

    if (
        not isinstance(count_row, Mapping)
        or "total" not in count_row
        or "missing_mentor_count" not in count_row
        or count_row.get("total") is None
        or count_row.get("missing_mentor_count") is None
    ):
        return None
    total = normalize_course_count(count_row.get("total"))
    missing_mentor_count = normalize_course_count(count_row.get("missing_mentor_count"))
    if (
        isinstance(total, ErrorDetail)
        or isinstance(missing_mentor_count, ErrorDetail)
        or total > MAX_INT64
        or missing_mentor_count > total
    ):
        logger.error("Admin courses count mapping failed; trace_id=%s", trace_id)
        return None
    return total, missing_mentor_count


# API #73 admin_courses_list
def get_admin_courses(
    *,
    authorization: str | None,
    status: str | None,
    mentor_value: str | None,
    category_value: str | None,
    page_value: str | None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Yêu cầu role ADMIN, áp dụng filter exact-match và trả một trang Course chỉ đọc."""

    # Xác thực Bearer/JWT và role Admin trước khi parse query hoặc truy cập DB.
    authentication = validate_admin_request(authorization, trace_id=trace_id)
    if isinstance(authentication, JSONResponse):
        return authentication

    # Parse ID/page từ raw query; category có giá trị hợp lệ vẫn bị từ chối do thiếu relation.
    validated_query = validate_admin_courses_query(
        status=status,
        mentor_value=mentor_value,
        category_value=category_value,
        page_value=page_value,
        trace_id=trace_id,
    )
    if isinstance(validated_query, JSONResponse):
        return validated_query

    # Count và page dùng cùng filter, page cố định 20 hàng theo thứ tự ID tăng dần.
    base_params = _query_parameters(validated_query)
    page_params = {
        **base_params,
        "limit": DEFAULT_PAGE_SIZE,
        "offset": (validated_query.page - 1) * DEFAULT_PAGE_SIZE,
    }
    try:
        # Đọc count/integrity trước, rồi lấy trang kết quả; view không commit transaction.
        count_row = query_one(db, COUNT_ADMIN_COURSES, base_params)
        rows = query_many(db, LIST_ADMIN_COURSES, page_params)
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin courses query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Từ chối count hỏng hoặc course mồ côi thay vì trả trang thiếu mentor âm thầm.
    normalized_count = _normalize_count_row(count_row, trace_id=trace_id)
    if normalized_count is None:
        _rollback_safely(db, trace_id=trace_id)
        return _internal_error(trace_id)
    total, missing_mentor_count = normalized_count
    if missing_mentor_count:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin courses have missing mentor rows; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not isinstance(rows, list):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin courses page projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Map qua Course response allowlist dùng chung để giữ decimal price chính xác.
    items = []
    for row in rows:
        if not isinstance(row, Mapping):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin courses row projection failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        try:
            item = map_course(dict(row))
        except (TypeError, ValueError, ValidationError):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin course mapping raised; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        if isinstance(item, ErrorDetail):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin course mapping failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        items.append(item)

    # Tạo Page metadata; trang ngoài phạm vi vẫn hợp lệ với items rỗng và HTTP 200.
    try:
        total_pages = (total + DEFAULT_PAGE_SIZE - 1) // DEFAULT_PAGE_SIZE if total else 0
        page = CoursePage(
            items=items,
            pagination=Pagination(
                page=validated_query.page,
                size=DEFAULT_PAGE_SIZE,
                total=total,
                total_pages=total_pages,
            ),
        )
    except (TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin courses page mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Courses retrieved." if items else "No courses found.",
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )
