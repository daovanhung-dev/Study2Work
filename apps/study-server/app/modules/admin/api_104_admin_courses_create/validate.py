"""Xác thực request metadata tạo khóa học sau khi view đã kiểm tra quyền Admin."""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation

from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_104_admin_courses_create.models import CreateAdminCourseRequest
from pydantic import ValidationError
from starlette.responses import JSONResponse

MAX_INT64 = 2**63 - 1
MAX_COURSE_TITLE_LENGTH = 200
MAX_COURSE_PRICE_INTEGER_DIGITS = 10
_DECIMAL_STRING_PATTERN = re.compile(r"-?[0-9]+(?:\.[0-9]{1,2})?\Z")


def _field_errors(exc: ValidationError) -> list[ErrorDetail]:
    """Chuyển lỗi Pydantic thành danh sách field errors không phản chiếu input."""

    details: list[ErrorDetail] = []
    for item in exc.errors():
        parts = [str(part) for part in item.get("loc", ())]
        details.append(
            ErrorDetail(
                field=".".join(parts) or "body",
                code=str(item.get("type", "INVALID_FIELD")).upper().replace(".", "_"),
                message="Giá trị không hợp lệ.",
            )
        )
    return details or [
        ErrorDetail(field="body", code="INVALID_BODY", message="Dữ liệu đầu vào không hợp lệ.")
    ]


def _validation_response(trace_id: str, errors: list[ErrorDetail]) -> JSONResponse:
    """Tạo envelope 422 dùng chung cho request tạo khóa học sai."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=errors,
    )


def _parse_course_price(value: str) -> Decimal | None:
    """Parse decimal price theo precision NUMERIC(12,2) đã dùng bởi API #75."""

    if len(value) > 14 or _DECIMAL_STRING_PATTERN.fullmatch(value) is None:
        return None
    try:
        price = Decimal(value)
    except InvalidOperation:
        return None
    if not price.is_finite() or abs(price) >= Decimal(10**MAX_COURSE_PRICE_INTEGER_DIGITS):
        return None
    return price


def validate_create_admin_course_request(
    raw_body: bytes,
    *,
    trace_id: str,
) -> tuple[CreateAdminCourseRequest, Decimal] | JSONResponse:
    """Parse body, chuẩn hóa tên và kiểm tra field constraints trước mọi query."""

    try:
        request = CreateAdminCourseRequest.model_validate_json(raw_body)
    except ValidationError as exc:
        return _validation_response(trace_id, _field_errors(exc))

    title = request.title.strip()
    errors: list[ErrorDetail] = []
    if not title:
        errors.append(
            ErrorDetail(
                field="title",
                code="STRING_EMPTY",
                message="Tên khóa học là bắt buộc.",
            )
        )
    elif len(title) > MAX_COURSE_TITLE_LENGTH:
        errors.append(
            ErrorDetail(
                field="title",
                code="STRING_TOO_LONG",
                message="Tên khóa học vượt quá 200 ký tự.",
            )
        )

    if not 1 <= request.mentor_id <= MAX_INT64:
        errors.append(
            ErrorDetail(
                field="mentor_id",
                code="INT64_RANGE",
                message="mentor_id phải là số nguyên dương trong miền int64.",
            )
        )

    price = _parse_course_price(request.price)
    if price is None:
        errors.append(
            ErrorDetail(
                field="price",
                code="DECIMAL_CONSTRAINT",
                message="Học phí phải phù hợp NUMERIC(12,2).",
            )
        )

    if errors:
        return _validation_response(trace_id, errors)

    return request.model_copy(update={"title": title}), price
