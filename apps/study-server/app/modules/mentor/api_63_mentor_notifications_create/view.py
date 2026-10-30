"""Điều phối auth, scope, outbox transaction và Operation response API #63."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any
from uuid import uuid4

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_63_mentor_notifications_create.models import (
    CreateNotificationEnvelope,
    CreateNotificationRequest,
    NormalizedNotificationRequest,
    OperationResponse,
)
from app.modules.mentor.api_63_mentor_notifications_create.query import (
    FIND_COMMON_MENTOR_COURSE_FOR_RECIPIENTS,
    INSERT_NOTIFICATION,
    INSERT_NOTIFICATION_DELIVERY,
)
from app.modules.mentor.api_63_mentor_notifications_create.validate import (
    validate_notification_request,
)
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import DBAPIError, OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _is_database_unavailable(exc: SQLAlchemyError) -> bool:
    """Nhận diện lỗi kết nối DB để ánh xạ dependency failure thành HTTP 503."""

    return isinstance(exc, OperationalError) or (
        isinstance(exc, DBAPIError) and bool(exc.connection_invalidated)
    )


def _error_response(
    *,
    trace_id: str,
    status_code: int,
    business_code: str,
    message: str,
) -> JSONResponse:
    """Dựng error envelope chuẩn với code/status thuộc catalog API #63."""

    return error_response(
        status_code=status_code,
        business_code=business_code,
        message=message,
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi recipient set không nằm trong common owned course roster."""

    return _error_response(
        trace_id=trace_id,
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied for one or more recipients.",
    )


def _dependency_unavailable(trace_id: str) -> JSONResponse:
    """Dựng lỗi 503 khi database không thể xác minh hoặc nhận delivery outbox."""

    return _error_response(
        trace_id=trace_id,
        status_code=503,
        business_code="DESIGN_DEPENDENCY_UNAVAILABLE",
        message="Notification dispatch is temporarily unavailable.",
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi projection hoặc thao tác nội bộ không hợp lệ."""

    return _error_response(
        trace_id=trace_id,
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Notification dispatch could not be accepted.",
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction của batch mà không che lỗi persistence ban đầu."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Mentor notification rollback failed; trace_id=%s", trace_id)


def _validated_scope(
    row: dict[str, Any] | None,
    *,
    recipient_count: int,
) -> bool | None:
    """Trả True khi scope hợp lệ, False khi thiếu course chung, None khi projection sai."""

    if row is None:
        return False
    if not isinstance(row, Mapping):
        return None
    course_id = row.get("course_id")
    matched_count = row.get("matched_count")
    if (
        type(course_id) is not int
        or course_id < 1
        or type(matched_count) is not int
        or matched_count != recipient_count
    ):
        return None
    return True


def _map_notification_insert(row: dict[str, Any] | None) -> tuple[int, datetime] | None:
    """Kiểm tra ID và timestamp trả về khi tạo một notification row."""

    if not isinstance(row, Mapping):
        return None
    notification_id = row.get("id")
    created_at = row.get("created_at")
    if (
        type(notification_id) is not int
        or notification_id < 1
        or not isinstance(created_at, datetime)
    ):
        return None
    return notification_id, created_at


def _map_delivery_insert(row: dict[str, Any] | None) -> bool:
    """Xác nhận INSERT outbox đã trả về một delivery ID hợp lệ."""

    return (
        isinstance(row, Mapping)
        and type(row.get("id")) is int
        and row.get("id") > 0
    )


def _query_error_response(exc: SQLAlchemyError, trace_id: str) -> JSONResponse:
    """Ghi log lỗi DB theo trace và chọn 503 cho mất kết nối, 500 cho lỗi nội bộ khác."""

    logger.error("Mentor notification database operation failed; trace_id=%s", trace_id)
    if _is_database_unavailable(exc):
        return _dependency_unavailable(trace_id)
    return _internal_error(trace_id)


def _accept_notification_batch(
    *,
    request_data: CreateNotificationRequest,
    normalized: NormalizedNotificationRequest,
    mentor_id: int,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Kiểm tra common roster, ghi Notification/outbox atomically và dựng Operation response."""

    # Xác nhận toàn bộ recipient set cùng thuộc một ACTIVE roster của course Mentor sở hữu.
    try:
        scope_row = query_one(
            db,
            FIND_COMMON_MENTOR_COURSE_FOR_RECIPIENTS,
            {
                "mentor_id": mentor_id,
                "recipient_ids": normalized.recipient_ids,
                "recipient_count": len(normalized.recipient_ids),
            },
        )
    except SQLAlchemyError as exc:
        _rollback_safely(db, trace_id=trace_id)
        return _query_error_response(exc, trace_id)

    scope_valid = _validated_scope(scope_row, recipient_count=len(normalized.recipient_ids))
    if scope_valid is False:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)
    if scope_valid is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor notification scope projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    operation_id = uuid4()
    notification_ids: list[int] = []
    submitted_at: datetime | None = None

    # Tạo từng Notification cho một Student và gắn chung Operation UUID để giữ batch.
    for recipient_id in normalized.recipient_ids:
        try:
            notification_row = query_one(
                db,
                INSERT_NOTIFICATION,
                {
                    "user_id": recipient_id,
                    "sender_id": mentor_id,
                    "title": request_data.title,
                    "content": str(request_data.content),
                    "operation_id": operation_id,
                },
            )
        except SQLAlchemyError as exc:
            _rollback_safely(db, trace_id=trace_id)
            return _query_error_response(exc, trace_id)

        notification_projection = _map_notification_insert(notification_row)
        if notification_projection is None:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Mentor notification insert projection failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        notification_id, created_at = notification_projection
        notification_ids.append(notification_id)
        if submitted_at is None:
            submitted_at = created_at

        # Ghi mỗi channel thành outbox row QUEUED trước khi chấp nhận bất đồng bộ.
        for channel in normalized.channels:
            try:
                delivery_row = query_one(
                    db,
                    INSERT_NOTIFICATION_DELIVERY,
                    {"notification_id": notification_id, "channel": channel},
                )
            except SQLAlchemyError as exc:
                _rollback_safely(db, trace_id=trace_id)
                return _query_error_response(exc, trace_id)

            if not _map_delivery_insert(delivery_row):
                _rollback_safely(db, trace_id=trace_id)
                logger.error("Mentor notification outbox projection failed; trace_id=%s", trace_id)
                return _internal_error(trace_id)

    if submitted_at is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor notification batch has no persisted recipients; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Kiểm tra Operation/envelope trước commit để projection sai không tạo 202 giả.
    try:
        operation = OperationResponse(
            id=operation_id,
            kind="NOTIFICATION_DISPATCH",
            status="QUEUED",
            owner_id=mentor_id,
            submitted_at=submitted_at,
            updated_at=submitted_at,
        )
        envelope = CreateNotificationEnvelope.model_validate(
            success_response(
                business_code="DESIGN_OPERATION_ACCEPTED",
                message="Notification dispatch was queued.",
                trace_id=trace_id,
                data=operation.model_dump(mode="json", exclude_none=True),
                meta={"notification_ids": notification_ids},
            )
        )
    except ValidationError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor notification response mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Chỉ xác nhận yêu cầu sau khi notification rows và toàn bộ channel outbox cùng commit.
    try:
        db.commit()
    except SQLAlchemyError as exc:
        _rollback_safely(db, trace_id=trace_id)
        return _query_error_response(exc, trace_id)

    return envelope.model_dump(mode="json", exclude_none=True)


def create_mentor_notifications(
    *,
    authorization: str | None,
    request_data: CreateNotificationRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, chuẩn hóa body rồi ghi và chấp nhận batch notification API #63."""

    # Xác thực access token và role trước mọi thao tác database.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Notification dispatch could not be accepted.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Parse CSV fields trước khi mở các query kiểm tra quyền hoặc ghi dữ liệu.
    normalized = validate_notification_request(
        recipients=request_data.recipients,
        channels=request_data.channels,
        trace_id=trace_id,
    )
    if isinstance(normalized, JSONResponse):
        return normalized

    return _accept_notification_batch(
        request_data=request_data,
        normalized=normalized,
        mentor_id=mentor_id,
        db=db,
        trace_id=trace_id,
    )
