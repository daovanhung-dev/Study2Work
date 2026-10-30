"""Kiểm tra và chuẩn hóa dữ liệu đầu vào cho API #25 cập nhật tiến độ bài học."""

from __future__ import annotations

from app.core.responses import error_response
from app.modules.guest.api_25_lessons_progress.models import LessonProgressUpdateRequest
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse


def validate_lesson_progress_request(
    authorization: str | None,
    lesson_id_raw: str | int,
    user_data: LessonProgressUpdateRequest,
    *,
    trace_id: str,
) -> tuple[int, int, LessonProgressUpdateRequest] | JSONResponse:
    """Xác thực token học viên, định danh lesson_id và dữ liệu cập nhật tiến độ."""
    authentication = validate_current_user_request(
        authorization,
        role="STUDENT",
        trace_id=trace_id,
        internal_error_message="Lesson progress could not be updated.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    user_id, _roles = authentication

    try:
        lesson_id = int(lesson_id_raw)
        if lesson_id <= 0:
            return _lesson_not_found(trace_id)
    except (TypeError, ValueError):
        return _lesson_not_found(trace_id)

    return user_id, lesson_id, user_data


def _lesson_not_found(trace_id: str) -> JSONResponse:
    """Tạo phản hồi 404 chuẩn khi không tìm thấy bài học."""
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Lesson not found.",
        trace_id=trace_id,
    )
