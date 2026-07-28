import re

from app.core.responses import ErrorDetail, error_payload
from app.module.auth.model import RegisterRequest


EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


def validate_user_create(user_data: RegisterRequest):
    display_name = user_data.display_name.strip()
    email = user_data.email.strip()
    phone = user_data.phone.strip()

    if not display_name or len(display_name) > 150:
        return error_payload(
            business_code="AUTH_001",
            message="Display name không hợp lệ",
            trace_id="trace-123",
            errors=[
                ErrorDetail(
                    field="display_name",
                    code="INVALID_DISPLAY_NAME",
                    message="Tên hiển thị phải có từ 1 đến 150 ký tự",
                )
            ],
        )

    if not email or len(email) > 320 or not re.fullmatch(EMAIL_REGEX, email):
        return error_payload(
            business_code="AUTH_002",
            message="Email không hợp lệ",
            trace_id="trace-123",
            errors=[
                ErrorDetail(
                    field="email",
                    code="INVALID_EMAIL",
                    message="Email không đúng định dạng",
                )
            ],
        )

    if not phone or not phone.isdigit() or not 10 <= len(phone) <= 11:
        return error_payload(
            business_code="AUTH_003",
            message="Số điện thoại không hợp lệ",
            trace_id="trace-123",
            errors=[
                ErrorDetail(
                    field="phone",
                    code="INVALID_PHONE",
                    message="Số điện thoại phải gồm 10 đến 11 chữ số",
                )
            ],
        )

    if not 8 <= len(user_data.password) <= 72:
        return error_payload(
            business_code="AUTH_004",
            message="Mật khẩu không hợp lệ",
            trace_id="trace-123",
            errors=[
                ErrorDetail(
                    field="password",
                    code="INVALID_PASSWORD",
                    message="Mật khẩu phải có từ 8 đến 72 ký tự",
                )
            ],
        )

    return None
