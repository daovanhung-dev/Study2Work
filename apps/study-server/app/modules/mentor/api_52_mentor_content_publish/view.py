"""Điều phối auth, publication state transition và Content response API #52."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from app.modules.mentor.api_52_mentor_content_publish.models import PublishContentRequest
from app.modules.mentor.api_52_mentor_content_publish.query import (
    LOCK_MENTOR_CONTENT,
    UPDATE_PUBLICATION_STATUS,
)
from app.modules.mentor.api_52_mentor_content_publish.validate import parse_content_id
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho lookup, update hoặc ánh xạ Content."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Content publication could not be updated.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 cho Content ID không hợp lệ hoặc không hoạt động."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Content not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi Mentor không sở hữu course chứa Content."""

    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _validation_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 422 cho trạng thái không đủ điều kiện theo fallback DERIVED."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Content is not ready for the requested publication state.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đang mở mà không thay response lỗi ban đầu."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Content publication rollback failed; trace_id=%s", trace_id)


def _valid_current_projection(row: Mapping[str, Any], *, content_id: int) -> bool:
    """Kiểm tra đủ trường cần cho quyền Mentor và response Content."""

    if (
        row.get("id") != content_id
        or type(row.get("course_id")) is not int
        or "mentor_id" not in row
        or type(row.get("status")) is not str
        or type(row.get("content_type")) is not str
        or type(row.get("title")) is not str
        or not isinstance(row.get("payload"), Mapping)
        or (row.get("parent_id") is not None and type(row.get("parent_id")) is not int)
        or type(row.get("order")) is not int
    ):
        return False
    owner_id = row.get("mentor_id")
    return owner_id is None or type(owner_id) is int


def _map_content(
    row: Mapping[str, Any],
    *,
    content_id: int,
    course_id: int,
    status: str,
) -> ContentResponse | None:
    """Xác minh UPDATE/SELECT projection rồi dựng response Content dùng chung."""

    if (
        row.get("id") != content_id
        or row.get("course_id") != course_id
        or row.get("status") != status
        or type(row.get("content_type")) is not str
        or type(row.get("title")) is not str
        or not isinstance(row.get("payload"), Mapping)
        or (row.get("parent_id") is not None and type(row.get("parent_id")) is not int)
        or type(row.get("order")) is not int
    ):
        return None

    try:
        return ContentResponse(
            id=row.get("id"),
            course_id=row.get("course_id"),
            content_type=row.get("content_type"),
            title=row.get("title"),
            payload=dict(row.get("payload", {})),
            status=row.get("status"),
            parent_id=row.get("parent_id"),
            order=row.get("order"),
        )
    except (TypeError, ValidationError):
        return None


def publish_content(
    *,
    authorization: str | None,
    content_id_value: str,
    content_request: PublishContentRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor và áp dụng target publication state theo fallback DERIVED."""

    # Xác thực Bearer, numeric subject và MENTOR role trước khi truy cập database.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Content publication could not be updated.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Parse path trong view để ID sai format/range ánh xạ về 404 catalog.
    content_id = parse_content_id(content_id_value)
    if content_id is None:
        return _not_found(trace_id)

    # Lock Content và Course để serialize publication cùng kiểm tra direct ownership.
    try:
        current = query_one(db, LOCK_MENTOR_CONTENT, {"content_id": content_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content publication lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if current is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(current, Mapping) or not _valid_current_projection(
        current,
        content_id=content_id,
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content publication projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if current.get("mentor_id") != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    current_status = current["status"]
    target_status = "PUBLISHED" if content_request.published else "APPROVED"
    if current_status == target_status:
        # Target-state body makes an identical retry idempotent; commit releases the row lock.
        content_row: Mapping[str, Any] = current
    else:
        allowed_source = "APPROVED" if content_request.published else "PUBLISHED"
        if current_status != allowed_source:
            _rollback_safely(db, trace_id=trace_id)
            return _validation_error(trace_id)

        # Status APPROVED is the only available readiness signal; payload readiness is undefined.
        try:
            updated = query_one(
                db,
                UPDATE_PUBLICATION_STATUS,
                {
                    "content_id": content_id,
                    "expected_status": allowed_source,
                    "target_status": target_status,
                },
            )
        except SQLAlchemyError:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Content publication update failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        if not isinstance(updated, Mapping):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Content publication update returned no row; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        content_row = updated

    content = _map_content(
        content_row,
        content_id=content_id,
        course_id=current["course_id"],
        status=target_status,
    )
    if content is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content publication response mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    response_data = content.model_dump(mode="json", exclude_none=True)

    # Commit only after the Content response projection has passed validation.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content publication commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="Content publication state updated.",
        trace_id=trace_id,
        data=response_data,
    )
