"""Điều phối MENTOR auth, read-only delivery aggregation và Operation response API #64."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any
from uuid import UUID

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_64_mentor_notification_status.models import (
    GetMentorNotificationStatusEnvelope,
    NotificationStatusOperation,
)
from app.modules.mentor.api_64_mentor_notification_status.query import (
    FIND_NOTIFICATION_STATUS,
)
from app.modules.mentor.api_64_mentor_notification_status.validate import (
    parse_notification_id,
)
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi đọc hoặc ánh xạ notification status thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Notification status could not be retrieved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 cho path hoặc dispatch status resource không tồn tại."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Notification status was not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi notification thuộc một Mentor sender khác."""

    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback read session sau lỗi query mà không che lỗi gốc hoặc lộ nội bộ."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Notification status rollback failed; trace_id=%s", trace_id)


def _status_from_counts(
    *,
    delivery_count: int,
    queued_count: int,
    sent_count: int,
    failed_count: int,
) -> str | None:
    """Ánh xạ channel rows sang status Operation theo local DERIVED precedence."""

    counts = (delivery_count, queued_count, sent_count, failed_count)
    if any(type(count) is not int or count < 0 for count in counts):
        return None
    if delivery_count == 0 or queued_count + sent_count + failed_count != delivery_count:
        return None
    if queued_count > 0:
        return "QUEUED"
    if failed_count > 0:
        return "FAILED"
    if sent_count == delivery_count:
        return "SENT"
    return None


def _map_operation(
    row: dict[str, Any],
    *,
    notification_id: int,
) -> NotificationStatusOperation | None:
    """Validate local notification/outbox projection and build the Operation response."""

    if not isinstance(row, Mapping):
        return None
    if type(row.get("notification_id")) is not int:
        return None
    if row.get("notification_id") != notification_id:
        return None

    operation_id = row.get("operation_id")
    owner_id = row.get("sender_id")
    submitted_at = row.get("submitted_at")
    updated_at = row.get("updated_at")
    if (
        not isinstance(operation_id, UUID)
        or type(owner_id) is not int
        or owner_id < 1
        or not isinstance(submitted_at, datetime)
        or not isinstance(updated_at, datetime)
    ):
        return None

    status_value = _status_from_counts(
        delivery_count=row.get("delivery_count"),
        queued_count=row.get("queued_count"),
        sent_count=row.get("sent_count"),
        failed_count=row.get("failed_count"),
    )
    if status_value is None:
        return None

    try:
        return NotificationStatusOperation(
            id=operation_id,
            kind="NOTIFICATION_DISPATCH",
            status=status_value,
            owner_id=owner_id,
            submitted_at=submitted_at,
            updated_at=updated_at,
        )
    except ValidationError:
        return None


def get_mentor_notification_status(
    *,
    authorization: str | None,
    notification_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, kiểm tra sender scope và trả Operation status đã lưu."""

    # Xác thực Bearer, numeric subject và role trước path parsing/database access.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Notification status could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Parse raw path để giữ malformed/out-of-range response trong catalog 404 set.
    notification_id = parse_notification_id(notification_id_value)
    if notification_id is None:
        return _not_found(trace_id)

    # Đọc notification và delivery states một lần để không đếm retry/row ngoài resource này.
    try:
        row = query_one(
            db,
            FIND_NOTIFICATION_STATUS,
            {"notification_id": notification_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Notification status lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if row is None:
        return _not_found(trace_id)
    if not isinstance(row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Notification status query returned an invalid row; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Check local API #63 sender ownership before returning any operation metadata.
    owner_id = row.get("sender_id")
    if owner_id is None:
        return _not_found(trace_id)
    if type(owner_id) is not int or owner_id < 1:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Notification sender projection is invalid; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if owner_id != mentor_id:
        return _access_denied(trace_id)

    # Legacy notification rows without API #63 operation/outbox have no dispatch status resource.
    delivery_count = row.get("delivery_count")
    if row.get("operation_id") is None or (
        type(delivery_count) is int and delivery_count == 0
    ):
        return _not_found(trace_id)

    # Validate UUID, timestamps and state counts before constructing the direct Operation response.
    operation = _map_operation(row, notification_id=notification_id)
    if operation is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Notification status projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Dựng và kiểm tra envelope trước khi trả kết quả read-only.
    try:
        envelope = GetMentorNotificationStatusEnvelope.model_validate(
            success_response(
                business_code="DESIGN_RESOURCE_RETRIEVED",
                message="Notification status was retrieved.",
                trace_id=trace_id,
                data=operation.model_dump(mode="json", exclude_none=True),
            )
        )
    except ValidationError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Notification status response mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return envelope.model_dump(mode="json", exclude_none=True)
