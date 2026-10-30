"""Xác thực Admin và chuẩn hóa filter query cho API #82."""

from __future__ import annotations

import re

import app.utils.auth as auth_utils
from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_82_admin_lessons_list.models import AdminLessonsQuery
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def validate_admin_request(
    authorization: str | None,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Dùng shared JWT guard để yêu cầu role ADMIN trước khi validate query hoặc đọc DB."""

    authentication = auth_utils.validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Lessons could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    admin_id, _roles = authentication
    return admin_id


def _parse_int64(value: str | None) -> int | None:
    """Chuyển raw query sang signed-int64 hoặc trả None nếu sai định dạng/miền."""

    if value is None:
        return None
    if _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None

    # Bỏ dấu và số 0 đầu để chỉ kiểm tra độ dài phần có ý nghĩa trước int().
    negative = value.startswith("-")
    digits = value.lstrip("+-").lstrip("0") or "0"
    if len(digits) > 19:
        return None

    parsed = int(digits)
    if negative:
        parsed = -parsed
    return parsed if INT64_MIN <= parsed <= INT64_MAX else None


def _validation_error(
    *,
    trace_id: str,
    field: str,
    code: str,
    message: str,
) -> JSONResponse:
    """Dựng lỗi 422 chuẩn cho input query không hợp lệ hoặc chưa có mapping."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=[ErrorDetail(field=field, code=code, message=message)],
    )


def validate_admin_lessons_query(
    *,
    course_value: str | None,
    status: str | None,
    type_value: str | None,
    trace_id: str,
) -> AdminLessonsQuery | JSONResponse:
    """Parse course và từ chối type rõ ràng khi chưa có Lesson field tương ứng."""

    course_id = _parse_int64(course_value)
    if course_value is not None and course_id is None:
        return _validation_error(
            trace_id=trace_id,
            field="course",
            code="INT_PARSING",
            message="Input should be a valid signed 64-bit integer",
        )

    if type_value is not None:
        return _validation_error(
            trace_id=trace_id,
            field="type",
            code="UNSUPPORTED_FILTER",
            message="Lesson type filter is not supported by the available schema.",
        )

    return AdminLessonsQuery(course_id=course_id, status=status)
