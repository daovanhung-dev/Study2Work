"""Điều phối nghiệp vụ cho API #21 lấy tiến độ tổng hợp."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_many
from app.core.responses import error_response, success_response
from app.modules.student.api_21_users_me_progress.models import (
    CourseProgressItem,
    OverallProgressSummary,
)
from app.modules.student.api_21_users_me_progress.query import (
    FIND_USER_COURSE_PROGRESS_ROWS,
)
from app.modules.student.api_21_users_me_progress.validate import (
    validate_progress_request,
)
from app.utils.validate import parse_integer
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_user_course_progress(
    db: Session,
    *,
    user_id: int,
    course_id: int | None = None,
) -> list[dict[str, Any]]:
    """Truy vấn số bài học và số bài đã hoàn thành theo từng khóa học của học viên."""
    return query_many(
        db,
        FIND_USER_COURSE_PROGRESS_ROWS,
        {"user_id": user_id, "course_id": course_id},
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Tạo phản hồi lỗi nội bộ chuẩn cho API #21."""
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Progress could not be retrieved.",
        trace_id=trace_id,
    )


# API #21 users_me_progress
def get_user_progress(
    *,
    authorization: str | None = None,
    course_id: str | None = None,
    aggregate: str | None = None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Lấy thông tin tiến độ tổng hợp thực tế từ enrollments và lesson_progress cho học viên hiện tại."""
    # Xác thực token Bearer và quyền Student của người dùng.
    validation = validate_progress_request(authorization, trace_id=trace_id)
    if isinstance(validation, JSONResponse):
        return validation
    user_id = validation

    # Chuẩn hóa tham số course_id tùy chọn nếu client truyền lên.
    parsed_course_id: int | None = None
    if course_id is not None and course_id.strip() != "":
        parsed_course_id = parse_integer(course_id.strip())
        if parsed_course_id is None or parsed_course_id <= 0:
            return error_response(
                status_code=422,
                business_code="DESIGN_VALIDATION_ERROR",
                message="Invalid course_id.",
                trace_id=trace_id,
            )

    # Truy vấn dữ liệu tiến độ từng khóa học từ cơ sở dữ liệu.
    try:
        rows = find_user_course_progress(
            db,
            user_id=user_id,
            course_id=parsed_course_id,
        )
    except Exception:
        db.rollback()
        logger.exception("User progress lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Tổng hợp số liệu khóa học, bài học và phần trăm hoàn thành.
    course_items: list[CourseProgressItem] = []
    active_courses = 0
    completed_courses = 0
    total_lessons_all = 0
    completed_lessons_all = 0

    for row in rows:
        status = str(row.get("enrollment_status") or "").strip().upper()
        if status == "ACTIVE":
            active_courses += 1
        elif status == "COMPLETED":
            completed_courses += 1

        total_lessons = int(row.get("total_lessons") or 0)
        completed_lessons = int(row.get("completed_lessons") or 0)
        percent = (
            round((completed_lessons / total_lessons) * 100.0, 2)
            if total_lessons > 0
            else 0.0
        )
        total_lessons_all += total_lessons
        completed_lessons_all += completed_lessons
        course_items.append(
            CourseProgressItem(
                course_id=int(row["course_id"]),
                course_name=str(row.get("course_name") or ""),
                enrollment_status=status,
                total_lessons=total_lessons,
                completed_lessons=completed_lessons,
                progress_percent=percent,
            )
        )

    overall_percent = (
        round((completed_lessons_all / total_lessons_all) * 100.0, 2)
        if total_lessons_all > 0
        else 0.0
    )

    summary = OverallProgressSummary(
        total_enrolled_courses=len(course_items),
        active_courses=active_courses,
        completed_courses=completed_courses,
        total_lessons=total_lessons_all,
        completed_lessons=completed_lessons_all,
        overall_progress_percent=overall_percent,
        courses=course_items,
    )

    # Trả về kết quả tổng hợp tiến độ thành công HTTP 200.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Progress retrieved.",
        trace_id=trace_id,
        data=summary.model_dump(mode="json"),
    )
