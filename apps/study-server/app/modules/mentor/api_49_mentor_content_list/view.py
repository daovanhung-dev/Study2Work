"""Điều phối xác thực Mentor, đọc các node Content và dựng response API #49."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from app.modules.mentor.api_49_mentor_content_list.query import (
    FIND_MENTOR_COURSE,
    LIST_COURSE_CONTENTS,
)
from app.modules.mentor.api_49_mentor_content_list.validate import parse_course_id
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi query hoặc ánh xạ cây Content thất bại."""

    # Chỉ trả mã lỗi chung; không đưa SQL hay chi tiết database ra client.
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Course content could not be retrieved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 cho course ID sai định dạng hoặc course không tồn tại."""

    # Giữ nguyên tập lỗi API #49 và không phát sinh HTTP 422 cho path ID.
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Course not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi Mentor không trực tiếp sở hữu course được yêu cầu."""

    # Không tiết lộ nội dung hoặc danh tính owner của course khác.
    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc dở mà không thay thế response lỗi gốc."""

    try:
        # Đóng transaction lỗi trước khi session được đóng bởi dependency request.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Course content rollback failed; trace_id=%s", trace_id)


def _map_contents(
    rows: list[dict[str, Any]],
    *,
    course_id: int,
) -> list[ContentResponse] | None:
    """Ánh xạ rows sang Content và từ chối projection sai course hoặc cây lỗi."""

    contents: list[ContentResponse] = []
    try:
        # Xác thực JSON object trước khi dựng response model từ từng hàng database.
        for row in rows:
            if not isinstance(row, Mapping):
                return None
            payload = row.get("payload")
            if not isinstance(payload, Mapping) or row.get("course_id") != course_id:
                return None
            content = ContentResponse(
                id=row.get("id"),
                course_id=row.get("course_id"),
                content_type=row.get("content_type"),
                title=row.get("title"),
                payload=dict(payload),
                status=row.get("status"),
                parent_id=row.get("parent_id"),
                order=row.get("order"),
            )
            contents.append(content)
    except (TypeError, ValidationError):
        # Sai kiểu hoặc thiếu field bắt buộc cho thấy row không thể phục vụ contract.
        return None

    # Kiểm tra unique IDs và bảo đảm mỗi parent đang hiện diện trong cùng cây trả về.
    by_id = {content.id: content for content in contents}
    if len(by_id) != len(contents):
        return None
    has_missing_parent = any(
        content.parent_id is not None and content.parent_id not in by_id
        for content in contents
    )
    if has_missing_parent:
        return None

    # Phát hiện cycle để response không trả một quan hệ cây không thể dựng được.
    for content in contents:
        visited: set[int] = set()
        current = content
        while current.parent_id is not None:
            if current.id in visited:
                return None
            visited.add(current.id)
            current = by_id[current.parent_id]

    return contents


# API #49 mentor_course_contents
def get_course_contents(
    *,
    authorization: str | None,
    course_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, kiểm tra direct owner và trả mọi node Content đang hoạt động."""

    # Xác thực Bearer, numeric subject và MENTOR role trước khi đọc database.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Course content could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Parse path trong view để ánh xạ sai format/range vào lỗi 404 của catalog.
    course_id = parse_course_id(course_id_value)
    if course_id is None:
        return _not_found(trace_id)

    # Đọc course trước để phân biệt resource thiếu với owner không khớp.
    try:
        course = query_one(db, FIND_MENTOR_COURSE, {"course_id": course_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Course content access lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if course is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(course, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Course content parent row has invalid shape; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if course.get("id") != course_id:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Course content parent mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if course.get("mentor_id") != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    # Đọc toàn bộ node của course, bao gồm draft, theo trạng thái quản lý của Mentor.
    try:
        rows = query_many(db, LIST_COURSE_CONTENTS, {"course_id": course_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Course content read failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Ánh xạ đầy đủ cây trước khi trả response để không phát nội dung một phần.
    contents = _map_contents(rows, course_id=course_id)
    if contents is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Course content mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Empty tree là kết quả hợp lệ để UI Mentor có thể bắt đầu tạo nội dung.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Course content retrieved." if contents else "No course content found.",
        trace_id=trace_id,
        data=[content.model_dump(mode="json", exclude_none=True) for content in contents],
    )
