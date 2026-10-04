"""Kiểm tra input cho API #6 liệt kê khóa học công khai."""

from __future__ import annotations

from app.core.responses import ErrorDetail, error_response
from app.modules.guest._shared.course_catalog.constants import (
    MAX_SIZE,
    SORT_DIRECTIONS,
    SORT_FIELDS,
)
from app.modules.guest.api_06_courses.models import CourseQuery
from app.utils.validate import normalize_sort
from starlette.responses import JSONResponse


def validate_course_query(
    course_query: CourseQuery,
    *,
    trace_id: str,
) -> CourseQuery | JSONResponse:
    """Kiểm tra giới hạn trang, sort allowlist và category chưa được hỗ trợ."""

    errors: list[ErrorDetail] = []
    if course_query.page < 1:
        errors.append(
            ErrorDetail(
                field="page",
                code="GREATER_THAN_EQUAL",
                message="Input should be greater than or equal to 1",
            )
        )
    if course_query.size < 1:
        errors.append(
            ErrorDetail(
                field="size",
                code="GREATER_THAN_EQUAL",
                message="Input should be greater than or equal to 1",
            )
        )
    elif course_query.size > MAX_SIZE:
        errors.append(
            ErrorDetail(
                field="size",
                code="LESS_THAN_EQUAL",
                message=f"Input should be less than or equal to {MAX_SIZE}",
            )
        )

    normalized_sort = course_query.sort
    try:
        normalized_sort = normalize_sort(
            course_query.sort,
            allowed_fields=SORT_FIELDS,
            allowed_directions=SORT_DIRECTIONS,
        )
    except ValueError as exc:
        errors.append(
            ErrorDetail(field="sort", code="VALUE_ERROR", message=f"Value error, {exc}")
        )

    if errors:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=errors,
        )
    if course_query.category is not None:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Bộ lọc category chưa được hỗ trợ.",
            trace_id=trace_id,
        )

    return course_query.model_copy(update={"sort": normalized_sort})
