"""Xác thực Mentor, giới hạn roster và dựng progress chi tiết cho API #67."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_67_mentor_student_progress.models import (
    ProgressStudentSummary,
    StudentCourseProgress,
    StudentCourseProgressSummary,
    StudentLessonProgress,
)
from app.modules.mentor.api_67_mentor_student_progress.query import (
    FIND_ACTIVE_STUDENT,
    FIND_MENTOR_COURSE,
    LIST_STUDENT_LESSON_PROGRESS,
)
from app.modules.mentor.api_67_mentor_student_progress.validate import parse_int64_path_value
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi query hoặc ánh xạ progress thất bại."""

    # Không gửi câu SQL, projection hoặc chi tiết database về client.
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Student progress could not be retrieved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str, *, resource: str) -> JSONResponse:
    """Dựng lỗi 404 cho path, course hoặc Student không tìm thấy trong scope."""

    # Dùng cùng business code trực tiếp của catalog cho các nhánh resource.
    message = "Course not found." if resource == "course" else "Student not found."
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message=message,
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi Mentor không trực tiếp sở hữu course được yêu cầu."""

    # Giữ cùng phản hồi chung của các API Mentor liên quan để không lộ course ngoài quyền.
    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc dở mà không che lỗi gốc."""

    # Dọn transaction sau nhánh lỗi; rollback lỗi không đổi response gốc.
    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Mentor student progress rollback failed; trace_id=%s", trace_id)


def _map_student_row(
    row: Mapping[str, Any],
    *,
    student_id: int,
) -> ProgressStudentSummary | None:
    """Kiểm tra và ánh xạ identity projection tối thiểu của Student."""

    # Chỉ nhận đúng Student đã yêu cầu và các field public được proposal cho phép.
    if (
        type(row.get("id")) is not int
        or row.get("id") != student_id
        or not isinstance(row.get("full_name"), str)
        or (row.get("avatar_url") is not None and not isinstance(row.get("avatar_url"), str))
    ):
        return None
    try:
        return ProgressStudentSummary(
            id=row["id"],
            full_name=row["full_name"],
            avatar_url=row.get("avatar_url"),
        )
    except (TypeError, ValidationError):
        return None


def _map_lesson_rows(
    rows: list[dict[str, Any]],
) -> list[StudentLessonProgress] | None:
    """Kiểm tra và ánh xạ từng lesson progress theo thứ tự đã publish."""

    # Reject duplicate lessons and malformed state instead of hiding bad source rows.
    lessons: list[StudentLessonProgress] = []
    seen_lesson_ids: set[int] = set()
    allowed_statuses = {"NOT_STARTED", "IN_PROGRESS", "COMPLETED"}
    try:
        for row in rows:
            if not isinstance(row, Mapping):
                return None
            lesson_id = row.get("lesson_id")
            title = row.get("title")
            lesson_order = row.get("order")
            progress_status = row.get("progress_status")
            progress_percent = row.get("progress_percent")
            last_accessed_at = row.get("last_accessed_at")
            completed_at = row.get("completed_at")
            if (
                type(lesson_id) is not int
                or lesson_id < 1
                or lesson_id in seen_lesson_ids
                or not isinstance(title, str)
                or type(lesson_order) is not int
                or progress_status not in allowed_statuses
                or type(progress_percent) is not int
                or not 0 <= progress_percent <= 100
                or (last_accessed_at is not None and not isinstance(last_accessed_at, datetime))
                or (completed_at is not None and not isinstance(completed_at, datetime))
            ):
                return None
            seen_lesson_ids.add(lesson_id)
            lessons.append(
                StudentLessonProgress(
                    lesson_id=lesson_id,
                    title=title,
                    order=lesson_order,
                    progress_status=progress_status,
                    progress_percent=progress_percent,
                    last_accessed_at=last_accessed_at,
                    completed_at=completed_at,
                )
            )
    except (TypeError, ValidationError):
        return None

    return lessons


# API #67 mentor_student_progress
def get_mentor_student_progress(
    *,
    authorization: str | None,
    course_id_value: str,
    student_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Trả progress hiện tại của Student đang active trong course Mentor sở hữu."""

    # Xác thực Bearer/JWT và role Mentor trước khi gọi database.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Student progress could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Giữ quy tắc signed-int64 path và 404 của các API Mentor liền kề.
    course_id = parse_int64_path_value(course_id_value)
    student_id = parse_int64_path_value(student_id_value)
    if course_id is None:
        return _not_found(trace_id, resource="course")
    if student_id is None:
        return _not_found(trace_id, resource="student")

    # Kiểm tra course trước để không truy vấn learner trong scope của Mentor khác.
    try:
        course = query_one(db, FIND_MENTOR_COURSE, {"course_id": course_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor student progress course lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if course is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id, resource="course")
    if (
        not isinstance(course, Mapping)
        or type(course.get("id")) is not int
        or course.get("id") != course_id
        or (course.get("mentor_id") is not None and type(course.get("mentor_id")) is not int)
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor student progress course mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if course.get("mentor_id") != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    # Chỉ cho phép xem Student đang có enrollment ACTIVE và role STUDENT.
    try:
        student_row = query_one(
            db,
            FIND_ACTIVE_STUDENT,
            {"course_id": course_id, "mentor_id": mentor_id, "student_id": student_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor student progress roster lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if student_row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id, resource="student")
    if not isinstance(student_row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor student progress student mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    student = _map_student_row(student_row, student_id=student_id)
    if student is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor student progress student projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Lấy cùng PUBLISHED lesson set của API #65; SQL tự sắp xếp theo curriculum order.
    try:
        rows = query_many(
            db,
            LIST_STUDENT_LESSON_PROGRESS,
            {"course_id": course_id, "mentor_id": mentor_id, "student_id": student_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor student progress lessons lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Kiểm tra mọi lesson projection trước khi tính summary và dựng response.
    lessons = _map_lesson_rows(rows)
    if lessons is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor student progress lesson projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Dùng cùng completed count và floor-average với aggregate roster API #65.
    total_lessons = len(lessons)
    completed_lessons = sum(
        1 for lesson in lessons if lesson.progress_status == "COMPLETED"
    )
    progress_percent = (
        sum(lesson.progress_percent for lesson in lessons) // total_lessons
        if total_lessons
        else 0
    )
    try:
        progress = StudentCourseProgress(
            course_id=course_id,
            student=student,
            summary=StudentCourseProgressSummary(
                completed_lessons=completed_lessons,
                total_lessons=total_lessons,
                progress_percent=progress_percent,
            ),
            lessons=lessons,
        )
    except (TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor student progress response validation failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Giữ các giá trị null tường minh để phân biệt lesson chưa có dấu truy cập.
    data = progress.model_dump(mode="json")
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Student progress retrieved.",
        trace_id=trace_id,
        data=data,
    )
