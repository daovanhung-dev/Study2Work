"""Parse raw signed-int64 notification path input cho API #95."""

from __future__ import annotations

import re

from app.core.responses import ErrorDetail, error_response
from starlette.responses import JSONResponse

MAX_INT64 = 2**63 - 1
_POSITIVE_INTEGER_PATTERN = re.compile(r"[0-9]+\Z")


def parse_admin_notification_delete_id(value: object) -> int | None:
    """Parse ID dương trong miền signed-int64 từ raw path text."""

    if (
        not isinstance(value, str)
        or len(value) > 19
        or _POSITIVE_INTEGER_PATTERN.fullmatch(value) is None
    ):
        return None
    notification_id = int(value)
    return notification_id if 1 <= notification_id <= MAX_INT64 else None


def validate_admin_notification_delete_path(
    notification_id_value: object,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Trả 422 nếu raw notification ID không phải signed-int64 dương."""

    notification_id = parse_admin_notification_delete_id(notification_id_value)
    if notification_id is not None:
        return notification_id
    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=[
            ErrorDetail(
                field="notification_id",
                code="INVALID_INT64",
                message="notification_id phải là số nguyên dương trong miền int64.",
            )
        ],
    )
