"""Parse và kiểm tra API #88 sau khi view đã xác thực quyền Admin."""

from __future__ import annotations

import json
import re
from decimal import Decimal, InvalidOperation
from typing import Any

from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_88_admin_quizzes_create.models import (
    CreateAdminQuizBody,
    CreateAdminQuizInput,
)
from pydantic import ValidationError
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
INT32_MIN = -(2**31)
INT32_MAX = 2**31 - 1
_DECIMAL_SCORE_PATTERN = re.compile(r"[+-]?[0-9]+(?:\.[0-9]{1,2})?\Z")


def _validation_response(
    *,
    trace_id: str,
    errors: list[ErrorDetail],
) -> JSONResponse:
    """Dựng envelope 422 cho lỗi outer hoặc embedded request."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=errors,
    )


def _field_errors(exc: ValidationError, *, prefix: str = "") -> list[ErrorDetail]:
    """Chuyển lỗi Pydantic thành field errors an toàn, không phản chiếu input value."""

    details: list[ErrorDetail] = []
    for item in exc.errors():
        parts = [str(part) for part in item.get("loc", ())]
        field = ".".join(part for part in (prefix, *parts) if part) or "body"
        code = str(item.get("type", "INVALID_FIELD")).upper().replace(".", "_")
        details.append(
            ErrorDetail(
                field=field,
                code=code,
                message="Giá trị không hợp lệ.",
            )
        )
    return details or [
        ErrorDetail(field=prefix or "body", code="INVALID_FIELD", message="Giá trị không hợp lệ.")
    ]


def _score_fits_legacy_numeric(value: str) -> bool:
    """Kiểm tra decimal-string có thể lưu nguyên vẹn vào NUMERIC(5,2)."""

    if _DECIMAL_SCORE_PATTERN.fullmatch(value) is None:
        return False
    try:
        parsed = Decimal(value)
    except InvalidOperation:
        return False
    return parsed.is_finite() and abs(parsed) <= Decimal("999.99")


def validate_create_admin_quiz_request(
    raw_body: bytes,
    *,
    trace_id: str,
) -> CreateAdminQuizInput | JSONResponse:
    """Decode outer strings and validate their DERIVED nested Quiz request shape."""

    try:
        outer = CreateAdminQuizBody.model_validate_json(raw_body)
    except ValidationError as exc:
        return _validation_response(trace_id=trace_id, errors=_field_errors(exc))

    try:
        config_data: Any = json.loads(outer.config)
    except json.JSONDecodeError:
        return _validation_response(
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="config",
                    code="INVALID_JSON",
                    message="config phải chứa JSON hợp lệ.",
                )
            ],
        )

    try:
        questions_data: Any = json.loads(outer.questions)
    except json.JSONDecodeError:
        return _validation_response(
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="questions",
                    code="INVALID_JSON",
                    message="questions phải chứa JSON hợp lệ.",
                )
            ],
        )

    try:
        request = CreateAdminQuizInput.model_validate(
            {"config": config_data, "questions": questions_data}
        )
    except ValidationError as exc:
        return _validation_response(
            trace_id=trace_id,
            errors=_field_errors(exc, prefix="embedded"),
        )

    config = request.config
    if not INT64_MIN <= config.course_id <= INT64_MAX:
        return _validation_response(
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="config.course_id",
                    code="INT64_RANGE",
                    message="course_id nằm ngoài miền int64.",
                )
            ],
        )
    duration = config.duration_minutes
    if duration is not None and not INT32_MIN <= duration <= INT32_MAX:
        return _validation_response(
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="config.duration_minutes",
                    code="INT32_RANGE",
                    message="duration_minutes nằm ngoài miền int32.",
                )
            ],
        )
    if len(config.title) > 200:
        return _validation_response(
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="config.title",
                    code="MAX_LENGTH",
                    message="title vượt quá 200 ký tự theo schema lưu trữ.",
                )
            ],
        )
    if not _score_fits_legacy_numeric(config.passing_score):
        return _validation_response(
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="config.passing_score",
                    code="NUMERIC_PRECISION",
                    message="passing_score không biểu diễn được chính xác bằng NUMERIC(5,2).",
                )
            ],
        )

    return request
