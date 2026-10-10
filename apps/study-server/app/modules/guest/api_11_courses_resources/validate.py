"""Kiểm tra và chuẩn hóa dữ liệu yêu cầu cho API #11 xem tài nguyên khóa học."""

from __future__ import annotations

from app.core.responses import ErrorDetail, error_response
from starlette.responses import JSONResponse


def validate_course_resources_request(
    course_id: int,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Kiểm tra course_id là số nguyên dương hợp lệ trước khi truy vấn database."""

    if course_id <= 0:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="course_id",
                    code="GREATER_THAN",
                    message="Input should be greater than 0",
                )
            ],
        )

    return course_id

