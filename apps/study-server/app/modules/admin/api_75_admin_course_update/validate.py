"""Xác thực role Admin, path int64 và metadata candidate của API #75."""

from __future__ import annotations

import re
from decimal import Decimal

from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_75_admin_course_update.models import AdminCourseUpdateRequest
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
MAX_COURSE_TITLE_LENGTH = 200
MAX_COURSE_PRICE_INTEGER_DIGITS = 10
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")
_DECIMAL_STRING_PATTERN = re.compile(r"-?[0-9]+(?:\.[0-9]+)?\Z")


def parse_admin_course_update_id(value: str) -> int | None:
    """Trả course ID signed-int64 hoặc None nếu path sai định dạng/vượt miền."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    course_id = int(value)
    if not INT64_MIN <= course_id <= INT64_MAX:
        return None
    return course_id


def parse_course_price(value: str) -> Decimal | None:
    """Parse decimal string không exponent, tối đa 2 số lẻ và 10 chữ số nguyên."""

    if _DECIMAL_STRING_PATTERN.fullmatch(value) is None:
        return None
    price = Decimal(value)
    if max(0, -price.as_tuple().exponent) > 2:
        return None
    if abs(price) >= Decimal(10**MAX_COURSE_PRICE_INTEGER_DIGITS):
        return None
    return price


def validate_admin_course_update_request(
    authorization: str | None,
    course_id_value: str,
    course_data: AdminCourseUpdateRequest,
    *,
    trace_id: str,
) -> tuple[int, Decimal] | JSONResponse:
    """Yêu cầu ADMIN rồi validate path, title và decimal price trước mutation."""

    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Course could not be updated.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    course_id = parse_admin_course_update_id(course_id_value)
    if course_id is None:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="course_id",
                    code="INT_PARSING",
                    message="Input should be a valid signed 64-bit integer",
                )
            ],
        )

    errors: list[ErrorDetail] = []
    if len(course_data.title) > MAX_COURSE_TITLE_LENGTH:
        errors.append(
            ErrorDetail(
                field="title",
                code="STRING_TOO_LONG",
                message="String should have at most 200 characters",
            )
        )

    price = parse_course_price(course_data.price)
    if price is None:
        errors.append(
            ErrorDetail(
                field="price",
                code="DECIMAL_CONSTRAINT",
                message="Price must fit the legacy NUMERIC(12,2) candidate without rounding",
            )
        )

    if errors:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=errors,
        )

    return course_id, price
