"""Điều phối quyền Admin, từ chối Content và lưu reason/audit cho API #81."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import execute_query, query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_81_admin_content_reject.models import RejectAdminContentRequest
from app.modules.admin.api_81_admin_content_reject.query import (
    INSERT_ADMIN_CONTENT_REVIEW_DECISION,
    LOCK_ADMIN_CONTENT_FOR_REJECTION,
    REJECT_ADMIN_CONTENT,
)
from app.modules.admin.api_81_admin_content_reject.validate import (
    validate_admin_content_rejection_request,
)
from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho truy vấn, ghi reason/audit hoặc commit."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Content rejection could not be completed.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi catalog 404 khi Content không tồn tại hoặc đã soft-delete."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Content not found.",
        trace_id=trace_id,
    )


def _invalid_state(trace_id: str) -> JSONResponse:
    """Dựng lỗi catalog 422 khi Content hiện không chờ duyệt."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Content is not pending review.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction lỗi mà không làm lộ exception nội bộ."""

    try:
        # Dọn transaction chưa hoàn tất trước khi request dependency đóng Session.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin Content rejection rollback failed; trace_id=%s", trace_id)


def _map_rejected_content(
    row: Mapping[str, Any],
    *,
    requested_content_id: int,
) -> ContentResponse | None:
    """Kiểm tra update projection rồi ánh xạ đúng tám field reusable Content."""

    required_fields = {
        "id",
        "course_id",
        "content_type",
        "title",
        "payload",
        "status",
        "parent_id",
        "order",
    }
    if not required_fields.issubset(row.keys()):
        return None
    if type(row.get("id")) is not int or row.get("id") != requested_content_id:
        return None
    if row.get("status") != "REJECTED":
        return None

    # Payload phải là object JSON theo legacy contents candidate.
    payload = row.get("payload")
    if not isinstance(payload, Mapping):
        return None

    try:
        # Reuse API #49 model để response chỉ chứa Content contract fields.
        return ContentResponse(
            id=row.get("id"),
            course_id=row.get("course_id"),
            content_type=row.get("content_type"),
            title=row.get("title"),
            payload=dict(payload),
            status=row.get("status"),
            parent_id=row.get("parent_id"),
            order=row.get("order"),
        )
    except (TypeError, ValidationError):
        return None


# API #81 admin_content_reject
def reject_admin_content(
    *,
    authorization: str | None,
    content_id_value: str,
    content_request: RejectAdminContentRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, từ chối Content pending và ghi reason cùng quyết định."""

    # Xác thực principal và raw path trước mọi thao tác database.
    validation = validate_admin_content_rejection_request(
        authorization,
        content_id_value,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    content_id, actor_user_id = validation

    # Khóa row active để kiểm tra state và mutation cùng một trạng thái.
    try:
        current = query_one(
            db,
            LOCK_ADMIN_CONTENT_FOR_REJECTION,
            {"content_id": content_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content rejection lock failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if current is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if (
        not isinstance(current, Mapping)
        or type(current.get("id")) is not int
        or current.get("id") != content_id
        or not isinstance(current.get("status"), str)
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content rejection lock projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    current_status = current.get("status")
    if current_status != "PENDING_REVIEW":
        _rollback_safely(db, trace_id=trace_id)
        return _invalid_state(trace_id)

    # Chỉ chuyển row vẫn active/pending và lấy Content projection bằng RETURNING.
    try:
        updated = query_one(
            db,
            REJECT_ADMIN_CONTENT,
            {"content_id": content_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content rejection update failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if updated is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(updated, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content rejection update row is malformed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Xác thực Content response trước khi lưu decision/reason.
    content = _map_rejected_content(updated, requested_content_id=content_id)
    if content is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content rejection projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Ghi cùng một decision row để lưu actor, status transition và reason đã gửi.
    try:
        execute_query(
            db,
            INSERT_ADMIN_CONTENT_REVIEW_DECISION,
            {
                "content_id": content_id,
                "actor_user_id": actor_user_id,
                "previous_status": current_status,
                "new_status": "REJECTED",
                "reason": content_request.reason,
            },
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content rejection decision insert failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Commit status và reason chỉ sau khi mutation cùng response đều hợp lệ.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content rejection commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="Content rejected.",
        trace_id=trace_id,
        data=content.model_dump(mode="json", exclude_none=True),
    )
