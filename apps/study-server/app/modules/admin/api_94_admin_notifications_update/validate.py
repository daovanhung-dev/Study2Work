"""Parse và kiểm tra path/body API #94 sau shared ADMIN guard."""

from __future__ import annotations

import re

from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_94_admin_notifications_update.models import (
    AdminNotificationUpdateRequest,
)
from pydantic import ValidationError
from starlette.responses import JSONResponse

MAX_INT64 = 2**63 - 1


def _validation_error(
    *,
    trace_id: str,
    field: str,
    code: str,
    message: str,
) -> JSONResponse:
    """Dựng lỗi validation 422 theo envelope và business code Study."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Notification request is invalid.",
        trace_id=trace_id,
        errors=[ErrorDetail(field=field, code=code, message=message)],
    )


def validate_admin_notification_update_request(
    notification_id_value: object,
    raw_body: bytes,
    *,
    trace_id: str,
) -> tuple[int, AdminNotificationUpdateRequest] | JSONResponse:
    """Kiểm tra ID int64 và body chỉ gồm title/content."""

    valid_id_text = (
        isinstance(notification_id_value, str)
        and re.fullmatch(r"[0-9]+", notification_id_value) is not None
    )
    if not valid_id_text or len(notification_id_value) > 19:
        return _validation_error(
            trace_id=trace_id,
            field="notification_id",
            code="INVALID_INT64",
            message="notification_id phải là số nguyên dương trong miền int64.",
        )

    notification_id = int(notification_id_value)
    if not 1 <= notification_id <= MAX_INT64:
        return _validation_error(
            trace_id=trace_id,
            field="notification_id",
            code="INVALID_INT64",
            message="notification_id phải là số nguyên dương trong miền int64.",
        )

    try:
        request = AdminNotificationUpdateRequest.model_validate_json(raw_body)
    except ValidationError as exc:
        errors = [
            ErrorDetail(
                field=".".join(str(part) for part in item.get("loc", ())) or "body",
                code=str(item.get("type", "INVALID_FIELD")).upper().replace(".", "_"),
                message="Giá trị không hợp lệ.",
            )
            for item in exc.errors()
        ]
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Notification request is invalid.",
            trace_id=trace_id,
            errors=errors,
        )

    if not request.title.strip():
        return _validation_error(
            trace_id=trace_id,
            field="title",
            code="BLANK_TITLE",
            message="title không được để trống.",
        )
    if not request.content.strip():
        return _validation_error(
            trace_id=trace_id,
            field="content",
            code="BLANK_CONTENT",
            message="content không được để trống.",
        )

    return notification_id, request
