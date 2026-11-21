"""Validate signed-int64 path cho API #61."""

from __future__ import annotations

import re

from app.core.responses import ErrorDetail, error_response
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def parse_support_request_id(value: str, *, trace_id: str) -> int | JSONResponse:
    """Parse signed-int64 request ID, trả 422 nếu sai format hoặc overflow."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=(
                ErrorDetail(
                    field="request_id",
                    code="INVALID_INT64",
                    message="Request ID must be a signed 64-bit integer.",
                ),
            ),
        )

    request_id = int(value)
    if not INT64_MIN <= request_id <= INT64_MAX:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=(
                ErrorDetail(
                    field="request_id",
                    code="INVALID_INT64",
                    message="Request ID must be a signed 64-bit integer.",
                ),
            ),
        )
    return request_id
