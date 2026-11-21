"""Xác thực Admin và chuẩn hóa raw query cho API #87."""

from __future__ import annotations

import re

from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_87_admin_quizzes_list.models import AdminQuizzesQuery
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
INT32_MIN = -(2**31)
INT32_MAX = 2**31 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def _parse_signed_integer(value: str | None, *, minimum: int, maximum: int) -> int | None:
    """Parse raw decimal integer text inside an inclusive signed range."""

    if value is None or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None

    negative = value.startswith("-")
    digits = value.lstrip("+-").lstrip("0") or "0"
    if len(digits) > len(str(max(abs(minimum), abs(maximum)))):
        return None

    parsed = int(digits)
    if negative:
        parsed = -parsed
    return parsed if minimum <= parsed <= maximum else None


def _validation_error(
    *,
    trace_id: str,
    field: str,
    message: str,
) -> JSONResponse:
    """Build the catalog validation envelope for an invalid query value."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=[
            ErrorDetail(
                field=field,
                code="INT_PARSING",
                message=message,
            )
        ],
    )


def validate_admin_quizzes_request(
    authorization: str | None,
    *,
    course_value: str | None,
    status_value: str | None,
    page_value: str | None,
    trace_id: str,
) -> AdminQuizzesQuery | JSONResponse:
    """Require ADMIN before parsing course/page and preserve exact status filtering."""

    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Quizzes could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    course_id = _parse_signed_integer(course_value, minimum=INT64_MIN, maximum=INT64_MAX)
    if course_value is not None and course_id is None:
        return _validation_error(
            trace_id=trace_id,
            field="course",
            message="Input should be a valid signed 64-bit integer",
        )

    page = 1 if page_value is None else _parse_signed_integer(
        page_value,
        minimum=INT32_MIN,
        maximum=INT32_MAX,
    )
    if page is None:
        return _validation_error(
            trace_id=trace_id,
            field="page",
            message="Input should be a valid signed 32-bit integer",
        )
    if page < 1:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="page",
                    code="GREATER_THAN_EQUAL",
                    message="Input should be greater than or equal to 1",
                )
            ],
        )

    return AdminQuizzesQuery(course_id=course_id, status=status_value, page=page)
