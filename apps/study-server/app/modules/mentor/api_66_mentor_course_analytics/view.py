"""Xác thực Mentor, kiểm tra course scope và tổng hợp activity proxy cho API #66."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_66_mentor_course_analytics.models import (
    MentorCourseActivityAnalytics,
)
from app.modules.mentor.api_66_mentor_course_analytics.query import (
    AGGREGATE_COURSE_ACTIVITY,
    FIND_MENTOR_COURSE,
)
from app.modules.mentor.api_66_mentor_course_analytics.validate import parse_course_id
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi truy vấn hoặc ánh xạ analytics thất bại."""

    # Không đưa SQL hoặc projection nội bộ vào message gửi client.
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Course analytics could not be retrieved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 cho course ID path không hợp lệ hoặc course không tồn tại."""

    # Giữ mã lỗi resource-not-found trực tiếp từ catalog.
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Course not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi Mentor hiện tại không sở hữu course được yêu cầu."""

    # Không phản chiếu thông tin về course ngoài quyền.
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
        logger.error("Mentor course analytics rollback failed; trace_id=%s", trace_id)


def _map_analytics_row(row: Mapping[str, Any]) -> MentorCourseActivityAnalytics | None:
    """Kiểm tra aggregate projection và dựng response activity theo schema công khai."""

    # Từ chối count âm, count sai kiểu hoặc số Student lớn hơn số cặp có activity.
    tracked_accesses = row.get("tracked_lesson_accesses")
    students_with_activity = row.get("students_with_activity")
    last_activity_at = row.get("last_activity_at")
    if (
        type(tracked_accesses) is not int
        or tracked_accesses < 0
        or type(students_with_activity) is not int
        or students_with_activity < 0
        or students_with_activity > tracked_accesses
        or (last_activity_at is not None and not isinstance(last_activity_at, datetime))
    ):
        return None

    # Dùng Pydantic để kiểm tra ranh giới int64 của response trước khi serialize.
    try:
        return MentorCourseActivityAnalytics(
            tracked_lesson_accesses=tracked_accesses,
            students_with_activity=students_with_activity,
            last_activity_at=last_activity_at,
        )
    except (TypeError, ValidationError):
        return None


# API #66 mentor_course_analytics
def get_mentor_course_analytics(
    *,
    authorization: str | None,
    course_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Trả tóm tắt dấu truy cập lesson của Student trong course Mentor sở hữu."""

    # Xác thực Bearer, JWT claims và Mentor role trước mọi thao tác database.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Course analytics could not be retrieved.",
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
        logger.error("Mentor course analytics access lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Chuyển course vắng mặt thành 404 theo direct error code.
    if course is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    # Từ chối mapping hỏng trước khi đọc dữ liệu activity.
    if (
        not isinstance(course, Mapping)
        or type(course.get("id")) is not int
        or course.get("id") != course_id
        or (course.get("mentor_id") is not None and type(course.get("mentor_id")) is not int)
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor course analytics course mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    # Giới hạn dashboard theo direct owner relation có trong legacy DDL.
    if course.get("mentor_id") != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    # Lặp lại owner predicate trong aggregate để giữ phạm vi truy vấn.
    try:
        row = query_one(
            db,
            AGGREGATE_COURSE_ACTIVITY,
            {"course_id": course_id, "mentor_id": mentor_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor course analytics aggregate lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Xác thực projection trước khi dựng response public.
    analytics = _map_analytics_row(row) if isinstance(row, Mapping) else None
    if analytics is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor course analytics mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả summary activity proxy; null last_activity_at được giữ nguyên khi chưa có dấu truy cập.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Course analytics retrieved.",
        trace_id=trace_id,
        data=analytics.model_dump(mode="json"),
    )
