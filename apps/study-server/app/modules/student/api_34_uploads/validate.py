"""Kiểm tra role, purpose và kiểu int64 của multipart API #34."""

from app.core.responses import ErrorDetail, error_response
from app.modules.student.api_34_uploads.models import UploadPurpose
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1


def validate_upload_policy(
    *,
    roles: list[str],
    purpose: UploadPurpose,
    course_id: int | None,
    trace_id: str,
) -> JSONResponse | None:
    """Ràng buộc SUBMISSION cho Student và LECTURE cho Mentor trước khi truy cập DB."""

    required_role = "STUDENT" if purpose is UploadPurpose.SUBMISSION else "MENTOR"
    if required_role not in roles:
        return error_response(
            status_code=403,
            business_code="DESIGN_ACCESS_DENIED",
            message="Access denied.",
            trace_id=trace_id,
        )

    errors: list[ErrorDetail] = []
    if course_id is not None and not INT64_MIN <= course_id <= INT64_MAX:
        errors.append(
            ErrorDetail(
                field="course_id",
                code="INT64_RANGE",
                message="Input should be a 64-bit integer",
            )
        )
    if purpose is UploadPurpose.LECTURE and course_id is None:
        errors.append(
            ErrorDetail(
                field="course_id",
                code="FIELD_REQUIRED",
                message="Field required",
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
    return None
