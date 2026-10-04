"""Kiểm tra path resource_id của API #12 trước khi truy cập database."""

from __future__ import annotations

from app.core.responses import ApiError
from starlette.responses import JSONResponse

MAX_INT64 = 9_223_372_036_854_775_807


def validate_resource_id(resource_id: str, *, trace_id: str) -> int | JSONResponse:
    """Parse integer dương int64 hoặc trả lỗi 404 thống nhất mà không query database."""

    try:
        parsed_resource_id = int(resource_id)
    except ValueError:
        return resource_not_found(trace_id)

    if parsed_resource_id <= 0 or parsed_resource_id > MAX_INT64:
        return resource_not_found(trace_id)
    return parsed_resource_id


def resource_not_found(trace_id: str) -> JSONResponse:
    """Tạo response 404 an toàn dùng chung cho path và resource không được expose."""

    return ApiError(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Resource not found",
        trace_id=trace_id,
    )
