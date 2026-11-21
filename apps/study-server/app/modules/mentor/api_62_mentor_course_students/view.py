"""Điều phối xác thực Mentor, scope course và đọc roster cho API #62."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_62_mentor_course_students.models import StudentSummaryResponse
from app.modules.mentor.api_62_mentor_course_students.query import (
    FIND_MENTOR_COURSE,
    LIST_ACTIVE_COURSE_STUDENTS,
)
from app.modules.mentor.api_62_mentor_course_students.validate import parse_course_id
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi query hoặc ánh xạ roster thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Course students could not be retrieved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 cho path ID sai định dạng/range hoặc course không tồn tại."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Course not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi Mentor không trực tiếp sở hữu course được yêu cầu."""

    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc dở mà không che lỗi gốc."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Mentor course students rollback failed; trace_id=%s", trace_id)


def _map_students(rows: list[dict[str, Any]]) -> list[StudentSummaryResponse] | None:
    """Ánh xạ distinct UserSummary rows và từ chối projection sai hoặc trùng ID."""

    students: list[StudentSummaryResponse] = []
    seen_ids: set[int] = set()
    try:
        for row in rows:
            if not isinstance(row, Mapping):
                return None
            student_id = row.get("id")
            if type(student_id) is not int or student_id in seen_ids:
                return None
            seen_ids.add(student_id)
            students.append(
                StudentSummaryResponse(
                    id=student_id,
                    full_name=row.get("full_name"),
                    avatar_url=row.get("avatar_url"),
                )
            )
    except (TypeError, ValidationError):
        return None

    return students


def get_mentor_course_students(
    *,
    authorization: str | None,
    course_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, kiểm tra direct owner và trả active Student summaries."""

    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Course students could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    course_id = parse_course_id(course_id_value)
    if course_id is None:
        return _not_found(trace_id)

    try:
        course = query_one(db, FIND_MENTOR_COURSE, {"course_id": course_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor course students access lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if course is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if (
        not isinstance(course, Mapping)
        or type(course.get("id")) is not int
        or course.get("id") != course_id
        or (
            course.get("mentor_id") is not None
            and type(course.get("mentor_id")) is not int
        )
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor course students course mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if course.get("mentor_id") != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    try:
        rows = query_many(
            db,
            LIST_ACTIVE_COURSE_STUDENTS,
            {"course_id": course_id, "mentor_id": mentor_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor course students roster lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    students = _map_students(rows)
    if students is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor course students mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Students retrieved." if students else "No students found.",
        trace_id=trace_id,
        data=[student.model_dump(mode="json", exclude_none=True) for student in students],
    )
