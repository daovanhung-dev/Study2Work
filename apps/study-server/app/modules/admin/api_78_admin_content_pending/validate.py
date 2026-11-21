"""Xác thực Admin và chuẩn hóa raw query cho hàng chờ duyệt API #78."""

from __future__ import annotations

import re

import app.utils.auth as auth_utils
from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_78_admin_content_pending.models import AdminPendingContentsQuery
from app.utils.validate import parse_integer
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
INT32_MAX = 2**31 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def validate_admin_request(
    authorization: str | None,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Dùng shared JWT guard với role ADMIN trước khi parse query hoặc truy vấn DB."""

    authentication = auth_utils.validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Pending content could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    admin_id, _roles = authentication
    return admin_id


def _parse_int64(value: str | None) -> int | None:
    """Trả signed-int64 hoặc None nếu raw query không hợp lệ."""

    if value is None:
        return None
    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    parsed = int(value)
    return parsed if INT64_MIN <= parsed <= INT64_MAX else None


def _validation_error(
    *,
    trace_id: str,
    field: str,
    code: str,
    message: str,
) -> JSONResponse:
    """Dựng lỗi 422 an toàn cho query parse theo fallback DERIVED của API #78."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=[ErrorDetail(field=field, code=code, message=message)],
    )


def validate_admin_pending_query(
    *,
    content_type: str | None,
    course_value: str | None,
    page_value: str | None,
    trace_id: str,
) -> AdminPendingContentsQuery | JSONResponse:
    """Parse exact Content/course filters và positive int32 page từ raw query."""

    course_id = _parse_int64(course_value)
    if course_value is not None and course_id is None:
        return _validation_error(
            trace_id=trace_id,
            field="course",
            code="INT_PARSING",
            message="Input should be a valid signed 64-bit integer",
        )

    page = 1 if page_value is None else parse_integer(page_value)
    if page is None:
        return _validation_error(
            trace_id=trace_id,
            field="page",
            code="INT_PARSING",
            message="Input should be a valid integer",
        )
    if page < 1:
        return _validation_error(
            trace_id=trace_id,
            field="page",
            code="GREATER_THAN_EQUAL",
            message="Input should be greater than or equal to 1",
        )
    if page > INT32_MAX:
        return _validation_error(
            trace_id=trace_id,
            field="page",
            code="LESS_THAN_EQUAL",
            message=f"Input should be less than or equal to {INT32_MAX}",
        )

    return AdminPendingContentsQuery(
        content_type=content_type,
        course_id=course_id,
        page=page,
    )
