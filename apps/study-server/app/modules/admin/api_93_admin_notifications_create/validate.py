"""Parse và kiểm tra body API #93 sau khi view xác thực Admin."""

from __future__ import annotations

from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_93_admin_notifications_create.models import (
    CreateAdminNotificationBody,
    NormalizedAdminNotificationRequest,
)
from pydantic import ValidationError
from starlette.responses import JSONResponse

MAX_INT64 = 2**63 - 1
MAX_TITLE_LENGTH = 200
_ALLOWED_CHANNELS = {"PUSH", "EMAIL"}


def _validation_response(
    *,
    trace_id: str,
    field: str,
    code: str,
    message: str,
) -> JSONResponse:
    """Dựng error envelope 422 an toàn cho một field của request."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Notification request is invalid.",
        trace_id=trace_id,
        errors=[ErrorDetail(field=field, code=code, message=message)],
    )


def _field_errors(exc: ValidationError) -> list[ErrorDetail]:
    """Chuyển lỗi Pydantic thành field errors mà không phản chiếu dữ liệu request."""

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
    return details or [ErrorDetail(field="body", code="INVALID_BODY", message="Body không hợp lệ.")]


def _invalid_body_response(
    exc: ValidationError,
    *,
    trace_id: str,
) -> JSONResponse:
    """Dựng 422 cho JSON sai cấu trúc, sai kiểu hoặc có field ngoài contract."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Notification request is invalid.",
        trace_id=trace_id,
        errors=_field_errors(exc),
    )


def validate_create_admin_notification_request(
    raw_body: bytes,
    *,
    trace_id: str,
) -> NormalizedAdminNotificationRequest | JSONResponse:
    """Parse explicit recipient request hoặc trả catalog 422 cho rule local."""

    try:
        body = CreateAdminNotificationBody.model_validate_json(raw_body)
    except ValidationError as exc:
        return _invalid_body_response(exc, trace_id=trace_id)

    # Từ chối segment vì catalog chưa định nghĩa enum hoặc predicate để mở rộng audience.
    if "segment" in body.model_fields_set:
        return _validation_response(
            trace_id=trace_id,
            field="segment",
            code="UNSUPPORTED_AUDIENCE_SEGMENT",
            message="Audience segment chưa được định nghĩa cho API này.",
        )

    # Chỉ nhận đúng một selector recipients tường minh, không đoán audience mặc định.
    if "recipients" not in body.model_fields_set or body.recipients is None:
        return _validation_response(
            trace_id=trace_id,
            field="recipients",
            code="RECIPIENTS_REQUIRED",
            message="Cần truyền danh sách recipients tường minh.",
        )
    if not body.recipients:
        return _validation_response(
            trace_id=trace_id,
            field="recipients",
            code="RECIPIENTS_EMPTY",
            message="Danh sách recipients không được để trống.",
        )
    if any(recipient_id < 1 or recipient_id > MAX_INT64 for recipient_id in body.recipients):
        return _validation_response(
            trace_id=trace_id,
            field="recipients",
            code="RECIPIENT_ID_RANGE",
            message="Mỗi recipient ID phải là số nguyên dương trong miền int64.",
        )
    if len(set(body.recipients)) != len(body.recipients):
        return _validation_response(
            trace_id=trace_id,
            field="recipients",
            code="DUPLICATE_RECIPIENT_ID",
            message="Danh sách recipients không được chứa ID trùng.",
        )

    # Giữ nguyên strings hợp lệ; chỉ dùng strip để phát hiện dữ liệu rỗng/whitespace.
    if not body.title.strip():
        return _validation_response(
            trace_id=trace_id,
            field="title",
            code="BLANK_TITLE",
            message="title không được để trống.",
        )
    if len(body.title) > MAX_TITLE_LENGTH:
        return _validation_response(
            trace_id=trace_id,
            field="title",
            code="TITLE_TOO_LONG",
            message="title vượt giới hạn 200 ký tự của local schema candidate.",
        )
    if not body.content.strip():
        return _validation_response(
            trace_id=trace_id,
            field="content",
            code="BLANK_CONTENT",
            message="content không được để trống.",
        )

    # Dùng channel tokens từ diagram và legacy delivery outbox, giữ nguyên thứ tự request.
    if not body.channels:
        return _validation_response(
            trace_id=trace_id,
            field="channels",
            code="CHANNELS_EMPTY",
            message="Cần chọn ít nhất một delivery channel.",
        )
    if any(channel not in _ALLOWED_CHANNELS for channel in body.channels):
        return _validation_response(
            trace_id=trace_id,
            field="channels",
            code="UNSUPPORTED_CHANNEL",
            message="channels chỉ hỗ trợ PUSH hoặc EMAIL theo local outbox candidate.",
        )
    if len(set(body.channels)) != len(body.channels):
        return _validation_response(
            trace_id=trace_id,
            field="channels",
            code="DUPLICATE_CHANNEL",
            message="Danh sách channels không được chứa channel trùng.",
        )

    return NormalizedAdminNotificationRequest(
        recipient_ids=body.recipients,
        title=body.title,
        content=body.content,
        channels=body.channels,
    )
