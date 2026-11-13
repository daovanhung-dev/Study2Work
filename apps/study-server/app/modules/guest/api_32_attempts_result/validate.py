"""Xác thực Student và kiểm tra path parameter cho API #32."""

from __future__ import annotations

from app.core.responses import error_response
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

MIN_INT64 = -(2**63)
MAX_INT64 = 2**63 - 1


def validate_attempt_result_request(
    authorization: str | None,
    attempt_id_raw: str,
    *,
    trace_id: str,
) -> tuple[int, int] | JSONResponse:
    """Xác thực Student và trả về user_id cùng attempt_id đã parse.

    Trả response lỗi từ auth helper nếu xác thực thất bại hoặc role bị từ chối.
    Path không parse được hoặc vượt miền int64 được ánh xạ thành 404 theo
    error set hiện có của API #32.
    """
    # Xác thực Bearer/JWT và quyền Student bằng helper dùng chung.
    authentication = validate_current_user_request(
        authorization,
        trace_id=trace_id,
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    user_id, _roles = authentication

    # Kiểm tra path parameter trước khi chuyển sang bước truy vấn dữ liệu.
    attempt_id = validate_attempt_id(attempt_id_raw, trace_id=trace_id)
    if isinstance(attempt_id, JSONResponse):
        return attempt_id

    return user_id, attempt_id


def validate_attempt_id(
    attempt_id_raw: str,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Parse attempt_id trong miền int64 hoặc trả lỗi 404 an toàn."""
    try:
        attempt_id = int(attempt_id_raw)
    except (TypeError, ValueError):
        return attempt_not_found(trace_id)

    if attempt_id < MIN_INT64 or attempt_id > MAX_INT64:
        return attempt_not_found(trace_id)

    return attempt_id


def attempt_not_found(trace_id: str) -> JSONResponse:
    """Tạo response 404 cho path attempt_id không hợp lệ theo error set hiện có."""
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Attempt result not found.",
        trace_id=trace_id,
    )
