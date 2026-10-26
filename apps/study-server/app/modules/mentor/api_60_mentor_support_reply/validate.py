"""Validate signed-int64 path và JSON attachment refs API #60."""

from __future__ import annotations

import json
import re

from app.core.responses import ErrorDetail, error_response
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def _validation_error(trace_id: str, *, field: str, code: str, message: str) -> JSONResponse:
    """Dựng validation envelope chuẩn cho một trường API #60 không hợp lệ."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=(ErrorDetail(field=field, code=code, message=message),),
    )


def parse_support_request_id(value: str, *, trace_id: str) -> int | JSONResponse:
    """Parse signed-int64 request ID; malformed hoặc overflow trả lỗi catalog 422."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return _validation_error(
            trace_id,
            field="request_id",
            code="INVALID_INT64",
            message="Request ID must be a signed 64-bit integer.",
        )
    request_id = int(value)
    if not INT64_MIN <= request_id <= INT64_MAX:
        return _validation_error(
            trace_id,
            field="request_id",
            code="INVALID_INT64",
            message="Request ID must be a signed 64-bit integer.",
        )
    return request_id


def parse_attachment_refs(value: str, *, trace_id: str) -> list[int] | JSONResponse:
    """Parse JSON array UploadAsset IDs có thứ tự, unique và signed-int64."""

    try:
        decoded = json.loads(value)
    except (json.JSONDecodeError, TypeError):
        decoded = None
    if type(decoded) is not list or any(
        type(asset_id) is not int or not INT64_MIN <= asset_id <= INT64_MAX
        for asset_id in decoded
    ):
        return _validation_error(
            trace_id,
            field="attachment_refs",
            code="INVALID_ARRAY",
            message="Attachment references must be a JSON array of signed 64-bit integers.",
        )
    if len(decoded) != len(set(decoded)):
        return _validation_error(
            trace_id,
            field="attachment_refs",
            code="DUPLICATE_ID",
            message="Attachment references must be unique.",
        )
    return decoded


def validate_message(message: str, *, trace_id: str) -> JSONResponse | None:
    """Từ chối message rỗng sau strip nhưng giữ nguyên text hợp lệ."""

    if message.strip():
        return None
    return _validation_error(
        trace_id,
        field="message",
        code="VALUE_ERROR",
        message="Message must contain non-whitespace text.",
    )
