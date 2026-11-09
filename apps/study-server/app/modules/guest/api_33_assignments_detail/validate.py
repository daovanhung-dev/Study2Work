"""Kiểm tra path assignment_id của API #33."""

from __future__ import annotations

from app.core.responses import error_response
from starlette.responses import JSONResponse

MIN_INT64 = -(2**63)
MAX_INT64 = 2**63 - 1


def validate_assignment_id(
    assignment_id: str,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Parse assignment_id theo miền int64; ID sai định dạng trả lỗi an toàn."""

    try:
        parsed_assignment_id = int(assignment_id)
    except:
        return assignment_not_found(trace_id)

    if not MIN_INT64 <= parsed_assignment_id <= MAX_INT64:
        return assignment_not_found(trace_id)

    return parsed_assignment_id


def assignment_not_found(trace_id: str) -> JSONResponse:
    """Tạo response 404 thống nhất khi không tìm thấy assignment."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Assignment not found",
        trace_id=trace_id,
    )
