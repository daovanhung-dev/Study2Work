"""Kiểm tra và chuẩn hóa dữ liệu đầu vào cho API #21."""

from __future__ import annotations

from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse


def validate_progress_request(
    authorization: str | None,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Xác thực token Bearer của học viên và trả về user_id hợp lệ."""
    authentication = validate_current_user_request(
        authorization,
        trace_id=trace_id,
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    user_id, _roles = authentication
    return user_id

