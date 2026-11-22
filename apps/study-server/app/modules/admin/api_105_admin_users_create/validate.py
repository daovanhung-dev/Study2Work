"""Xác thực và chuẩn hóa body tạo user Admin trước mọi truy vấn."""

from __future__ import annotations

from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_105_admin_users_create.models import CreateAdminUserRequest
from app.utils.validate import normalize_email
from pydantic import ValidationError
from starlette.responses import JSONResponse


def _field_errors(exc: ValidationError) -> list[ErrorDetail]:
    """Ánh xạ lỗi model sang field errors không phản chiếu input nhạy cảm."""

    return [
        ErrorDetail(
            field=".".join(str(part) for part in item.get("loc", ())) or "body",
            code=str(item.get("type", "INVALID_FIELD")).upper().replace(".", "_"),
            message="Giá trị không hợp lệ.",
        )
        for item in exc.errors()
    ] or [ErrorDetail(field="body", code="INVALID_BODY", message="Dữ liệu không hợp lệ.")]


def validate_create_admin_user_request(
    raw_body: bytes,
    *,
    trace_id: str,
) -> CreateAdminUserRequest | JSONResponse:
    """Parse body, chuẩn hóa email/tên và giữ nguyên password hợp lệ."""

    try:
        request = CreateAdminUserRequest.model_validate_json(raw_body)
    except ValidationError as exc:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=_field_errors(exc),
        )

    errors: list[ErrorDetail] = []
    normalized_email = normalize_email(request.email, max_length=255)
    if isinstance(normalized_email, ErrorDetail):
        email = request.email
        errors.append(
            ErrorDetail(
                field="email",
                code=normalized_email.code,
                message=normalized_email.message,
            )
        )
    else:
        email = normalized_email

    full_name = request.full_name.strip()
    if not full_name:
        errors.append(
            ErrorDetail(
                field="full_name",
                code="STRING_TOO_SHORT",
                message="Họ và tên không được để trống.",
            )
        )
    elif len(full_name) > 150:
        errors.append(
            ErrorDetail(
                field="full_name",
                code="STRING_TOO_LONG",
                message="Họ và tên không được vượt quá 150 ký tự.",
            )
        )

    if not request.password.strip():
        errors.append(
            ErrorDetail(
                field="password",
                code="VALUE_ERROR",
                message="Mật khẩu không được để trống.",
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

    return request.model_copy(update={"full_name": full_name, "email": email})
