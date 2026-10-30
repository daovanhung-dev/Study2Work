"""Xác thực Mentor, kiểm tra course scope và tổng hợp progress cho API #65."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_65_mentor_course_progress.models import (
    MentorStudentProgress,
    MentorStudentProgressPage,
    ProgressPagination,
    ProgressStudentSummary,
)
from app.modules.mentor.api_65_mentor_course_progress.query import (
    FIND_MENTOR_COURSE,
    LIST_ACTIVE_STUDENT_PROGRESS,
)
from app.modules.mentor.api_65_mentor_course_progress.validate import parse_course_id
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi truy vấn hoặc ánh xạ progress thất bại."""

    # Không đưa SQL hoặc projection nội bộ vào message gửi client.
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Course progress could not be retrieved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 cho path ID sai định dạng/range hoặc course không tồn tại."""

    # Giữ nguyên business code 404 trực tiếp từ catalog.
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Course not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi Mentor không trực tiếp sở hữu course được yêu cầu."""

    # Trả lỗi tổng quát để không phản chiếu thông tin course hoặc quyền.
    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc dở mà không che lỗi gốc."""

    # Dọn transaction đọc thất bại; rollback lỗi không thay response gốc.
    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Mentor course progress rollback failed; trace_id=%s", trace_id)


def _map_progress_rows(
    rows: list[dict[str, Any]],
) -> list[MentorStudentProgress] | None:
    """Validate aggregate projection rồi dựng đúng một item cho mỗi Student."""

    # Từ chối row sai kiểu, dữ liệu aggregate bất khả thi và ID Student lặp.
    items: list[MentorStudentProgress] = []
    seen_ids: set[int] = set()
    try:
        for row in rows:
            if not isinstance(row, Mapping):
                return None
            student_id = row.get("student_id")
            total_lessons = row.get("total_lessons")
            completed_lessons = row.get("completed_lessons")
            progress_sum = row.get("progress_sum")
            invalid_progress_count = row.get("invalid_progress_count")
            if (
                type(student_id) is not int
                or student_id < 1
                or student_id in seen_ids
                or type(total_lessons) is not int
                or total_lessons < 0
                or type(completed_lessons) is not int
                or completed_lessons < 0
                or completed_lessons > total_lessons
                or type(progress_sum) is not int
                or progress_sum < 0
                or progress_sum > total_lessons * 100
                or type(invalid_progress_count) is not int
                or invalid_progress_count != 0
            ):
                return None
            seen_ids.add(student_id)
            progress_percent = progress_sum // total_lessons if total_lessons else 0
            items.append(
                MentorStudentProgress(
                    student=ProgressStudentSummary(
                        id=student_id,
                        full_name=row.get("full_name"),
                        avatar_url=row.get("avatar_url"),
                    ),
                    completed_lessons=completed_lessons,
                    total_lessons=total_lessons,
                    progress_percent=progress_percent,
                )
            )
    except (TypeError, ValidationError):
        return None

    return items


# API #65 mentor_course_progress
def get_mentor_course_progress(
    *,
    authorization: str | None,
    course_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Trả một trang progress cho active Student trong course Mentor sở hữu."""

    # Xác thực Bearer, JWT claims và Mentor role trước mọi thao tác database.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Course progress could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Ánh xạ raw path sang signed int64; lỗi giữ status 404 trong catalog.
    course_id = parse_course_id(course_id_value)
    if course_id is None:
        return _not_found(trace_id)

    # Đọc owner trước để không chạy aggregate cho course ngoài scope.
    try:
        course = query_one(db, FIND_MENTOR_COURSE, {"course_id": course_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor course progress access lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if course is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if (
        not isinstance(course, Mapping)
        or type(course.get("id")) is not int
        or course.get("id") != course_id
        or (course.get("mentor_id") is not None and type(course.get("mentor_id")) is not int)
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor course progress course mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if course.get("mentor_id") != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    # Lấy aggregate read-only; SQL lặp lại owner predicate để giữ scope ở query.
    try:
        rows = query_many(
            db,
            LIST_ACTIVE_STUDENT_PROGRESS,
            {"course_id": course_id, "mentor_id": mentor_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor course progress aggregate lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Kiểm tra projection từ DB trước khi dựng response công khai.
    items = _map_progress_rows(rows)
    if items is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor course progress mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # API không có page/size nên toàn bộ roster được trả trong một DERIVED page.
    total = len(items)
    page = MentorStudentProgressPage(
        items=items,
        pagination=ProgressPagination(
            page=1,
            size=total,
            total=total,
            total_pages=1 if total else 0,
        ),
    )
    # Trả success envelope thống nhất và bỏ avatar_url khi nguồn là NULL.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Course progress retrieved." if items else "No students found.",
        trace_id=trace_id,
        data=page.model_dump(mode="json", exclude_none=True),
    )
