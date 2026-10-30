"""Xác thực Admin và chuẩn hóa raw query cho API #73."""

from __future__ import annotations

import re

import app.utils.auth as auth_utils
from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_73_admin_courses_list.models import AdminCoursesQuery
from app.utils.validate import parse_integer
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
MAX_PAGE = 2**31 - 1
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
        internal_error_message="Courses could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    admin_id, _roles = authentication
    return admin_id


def _parse_int64(value: str | None) -> int | None:
    """Trả về signed-int64 hoặc None nếu query không phải số nguyên hợp lệ."""

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
    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=[ErrorDetail(field=field, code=code, message=message)],
    )


def validate_admin_courses_query(
    *,
    status: str | None,
    mentor_value: str | None,
    category_value: str | None,
    page_value: str | None,
    trace_id: str,
) -> AdminCoursesQuery | JSONResponse:
    """Parse int64 filters/int32 page; reject category because no relation is source-backed."""

    mentor = _parse_int64(mentor_value)
    if mentor_value is not None and mentor is None:
        return _validation_error(
            trace_id=trace_id,
            field="mentor",
            code="INT_PARSING",
            message="Input should be a valid signed 64-bit integer",
        )

    category = _parse_int64(category_value)
    if category_value is not None and category is None:
        return _validation_error(
            trace_id=trace_id,
            field="category",
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
    if page > MAX_PAGE:
        return _validation_error(
            trace_id=trace_id,
            field="page",
            code="LESS_THAN_EQUAL",
            message=f"Input should be less than or equal to {MAX_PAGE}",
        )

    if category is not None:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Bộ lọc category chưa được hỗ trợ.",
            trace_id=trace_id,
        )

    return AdminCoursesQuery(status=status, mentor=mentor, page=page)
