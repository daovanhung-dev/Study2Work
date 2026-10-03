"""Kiểm tra và chuẩn hóa input cho API #10 lấy review khóa học."""

from __future__ import annotations

from app.core.responses import ApiError
from app.modules.guest.api_10_courses_reviews.models import CourseReviewsQuery
from fastapi.responses import JSONResponse


def validate_course_reviews_request(
    *,
    course_id: str,
    course_query: CourseReviewsQuery,
    trace_id: str,
) -> tuple[int, int, str | None] | JSONResponse:
    """Parse course_id và chuẩn hóa input đã được contract API #10 xác nhận."""

    try:
        parsed_course_id = int(course_id)
    except (TypeError, ValueError):
        return ApiError(
            status_code=404,
            business_code="DESIGN_RESOURCE_NOT_FOUND",
            message="Course not found.",
            trace_id=trace_id,
        )

    if course_query.page is None:
        effective_page = 1
    else:
        try:
            effective_page = int(course_query.page)
        except (TypeError, ValueError):
            # Contract API #10 chưa xác định behavior cho malformed page.
            # Không tự thêm HTTP/business error branch tại đây.
            raise ValueError("Malformed page") from None

    if effective_page < 1:
        raise ValueError("Page must be greater than or equal to 1")

    return parsed_course_id, effective_page, course_query.rating