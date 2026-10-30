"""Điều phối quyền Admin, notification fan-out, outbox và response API #93."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any
from uuid import uuid4

from app.core.database import query_many, query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.modules.admin.api_92_admin_notifications_list.models import AdminNotificationResponse
from app.modules.admin.api_93_admin_notifications_create.models import (
    CreateAdminNotificationEnvelope,
    NormalizedAdminNotificationRequest,
)
from app.modules.admin.api_93_admin_notifications_create.query import (
    FIND_ADMIN_NOTIFICATION_RECIPIENTS,
    INSERT_ADMIN_NOTIFICATION,
    INSERT_ADMIN_NOTIFICATION_DELIVERY,
)
from app.modules.admin.api_93_admin_notifications_create.validate import (
    validate_create_admin_notification_request,
)
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import DBAPIError, OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _is_database_unavailable(exc: SQLAlchemyError) -> bool:
    """Nhận diện mất kết nối DB để ánh xạ dependency failure thành HTTP 503."""

    return isinstance(exc, OperationalError) or (
        isinstance(exc, DBAPIError) and bool(exc.connection_invalidated)
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi insert, projection hoặc commit thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Notification could not be accepted.",
        trace_id=trace_id,
    )


def _dependency_unavailable(trace_id: str) -> JSONResponse:
    """Dựng lỗi 503 khi DB chưa thể nhận durable notification outbox."""

    return error_response(
        status_code=503,
        business_code="DESIGN_DEPENDENCY_UNAVAILABLE",
        message="Notification dispatch is temporarily unavailable.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback batch sau lỗi mà không làm thay đổi HTTP response gốc."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin notification rollback failed; trace_id=%s", trace_id)


def _query_error_response(exc: SQLAlchemyError, trace_id: str) -> JSONResponse:
    """Ghi log theo trace và phân loại lỗi DB 503/500 theo khả năng kết nối."""

    logger.error("Admin notification database operation failed; trace_id=%s", trace_id)
    if _is_database_unavailable(exc):
        return _dependency_unavailable(trace_id)
    return _internal_error(trace_id)


def _recipient_projection_matches(
    rows: Any,
    *,
    recipient_ids: list[int],
    trace_id: str,
) -> bool | None:
    """Trả True nếu query trả đúng toàn bộ user IDs, False nếu thiếu recipient."""

    if not isinstance(rows, list) or len(rows) > len(recipient_ids):
        return None
    found_ids: list[int] = []
    for row in rows:
        if not isinstance(row, Mapping):
            return None
        recipient_id = row.get("id")
        if type(recipient_id) is not int or not 1 <= recipient_id <= MAX_INT64:
            logger.error("Admin notification recipient mapping failed; trace_id=%s", trace_id)
            return None
        found_ids.append(recipient_id)
    if len(set(found_ids)) != len(found_ids):
        logger.error("Admin notification recipient rows duplicated; trace_id=%s", trace_id)
        return None
    return set(found_ids) == set(recipient_ids)


def _map_notification_insert(row: Any, *, trace_id: str) -> tuple[int, datetime] | None:
    """Kiểm tra ID/time từ notification INSERT RETURNING trước khi dựng response."""

    if not isinstance(row, Mapping):
        return None
    notification_id = row.get("id")
    created_at = row.get("created_at")
    if (
        type(notification_id) is not int
        or not 1 <= notification_id <= MAX_INT64
        or not isinstance(created_at, datetime)
    ):
        logger.error("Admin notification insert projection failed; trace_id=%s", trace_id)
        return None
    return notification_id, created_at


def _map_delivery_insert(row: Any, *, trace_id: str) -> bool:
    """Xác nhận một delivery row đã được tạo với BIGSERIAL ID hợp lệ."""

    if (
        not isinstance(row, Mapping)
        or type(row.get("id")) is not int
        or not 1 <= row["id"] <= MAX_INT64
    ):
        logger.error("Admin notification delivery projection failed; trace_id=%s", trace_id)
        return False
    return True


def _recipient_validation_error(trace_id: str) -> JSONResponse:
    """Trả 422 chung nếu một hoặc nhiều ID request không tồn tại trong users."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Notification request is invalid.",
        trace_id=trace_id,
        errors=[
            ErrorDetail(
                field="recipients",
                code="RECIPIENT_NOT_FOUND",
                message="Một hoặc nhiều recipient không hợp lệ.",
            )
        ],
    )


def _create_notification_batch(
    *,
    request_data: NormalizedAdminNotificationRequest,
    admin_id: int,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Ghi một notification/recipient và một delivery/channel trong cùng transaction."""

    # Kiểm tra đúng các user được request chỉ rõ, không suy diễn role hoặc audience scope.
    try:
        recipient_rows = query_many(
            db,
            FIND_ADMIN_NOTIFICATION_RECIPIENTS,
            {"recipient_ids": request_data.recipient_ids},
        )
    except SQLAlchemyError as exc:
        _rollback_safely(db, trace_id=trace_id)
        return _query_error_response(exc, trace_id)

    recipients_match = _recipient_projection_matches(
        recipient_rows,
        recipient_ids=request_data.recipient_ids,
        trace_id=trace_id,
    )
    if recipients_match is False:
        _rollback_safely(db, trace_id=trace_id)
        return _recipient_validation_error(trace_id)
    if recipients_match is None:
        _rollback_safely(db, trace_id=trace_id)
        return _internal_error(trace_id)

    operation_id = uuid4()
    notification_ids: list[int] = []
    first_notification: AdminNotificationResponse | None = None

    # Tạo một legacy Notification cho từng recipient và gắn cùng operation UUID.
    for recipient_id in request_data.recipient_ids:
        try:
            notification_row = query_one(
                db,
                INSERT_ADMIN_NOTIFICATION,
                {
                    "user_id": recipient_id,
                    "sender_id": admin_id,
                    "title": request_data.title,
                    "content": request_data.content,
                    "operation_id": operation_id,
                },
            )
        except SQLAlchemyError as exc:
            _rollback_safely(db, trace_id=trace_id)
            return _query_error_response(exc, trace_id)

        notification_projection = _map_notification_insert(notification_row, trace_id=trace_id)
        if notification_projection is None:
            _rollback_safely(db, trace_id=trace_id)
            return _internal_error(trace_id)
        notification_id, created_at = notification_projection
        notification_ids.append(notification_id)

        # Chỉ `data` đầu tiên biểu diễn trực tiếp Notification; metadata giữ đủ batch IDs.
        if first_notification is None:
            try:
                first_notification = AdminNotificationResponse(
                    id=notification_id,
                    title=request_data.title,
                    content=request_data.content,
                    channels=request_data.channels,
                    status="QUEUED",
                    created_at=created_at,
                )
            except ValidationError:
                _rollback_safely(db, trace_id=trace_id)
                logger.error("Admin notification response projection failed; trace_id=%s", trace_id)
                return _internal_error(trace_id)

        # Ghi delivery QUEUED cho từng channel để batch chỉ được accepted sau commit.
        for channel in request_data.channels:
            try:
                delivery_row = query_one(
                    db,
                    INSERT_ADMIN_NOTIFICATION_DELIVERY,
                    {"notification_id": notification_id, "channel": channel},
                )
            except SQLAlchemyError as exc:
                _rollback_safely(db, trace_id=trace_id)
                return _query_error_response(exc, trace_id)
            if not _map_delivery_insert(delivery_row, trace_id=trace_id):
                _rollback_safely(db, trace_id=trace_id)
                return _internal_error(trace_id)

    if first_notification is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin notification batch has no notification rows; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Validate direct Notification response and derived batch metadata before committing.
    try:
        envelope = CreateAdminNotificationEnvelope.model_validate(
            success_response(
                business_code="DESIGN_OPERATION_ACCEPTED",
                message="Notification dispatch was queued.",
                trace_id=trace_id,
                data=first_notification.model_dump(exclude_none=True),
                meta={
                    "operation_id": operation_id,
                    "notification_ids": notification_ids,
                },
            )
        )
    except ValidationError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin notification envelope mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Commit toàn bộ Notification và outbox row trước khi trả HTTP 202 accepted.
    try:
        db.commit()
    except SQLAlchemyError as exc:
        _rollback_safely(db, trace_id=trace_id)
        return _query_error_response(exc, trace_id)

    return envelope.model_dump(mode="json", exclude_none=True)


def create_admin_notification(
    *,
    authorization: str | None,
    raw_body: bytes,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, kiểm tra explicit audience và chấp nhận batch API #93."""

    # Chạy shared ADMIN guard trước khi parse body, truy vấn user hoặc ghi notification.
    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Notification could not be accepted.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    admin_id, _roles = authentication

    # Parse body chỉ sau auth; AudienceSegment chưa có enum/predicate nên bị validator từ chối.
    normalized_request = validate_create_admin_notification_request(
        raw_body,
        trace_id=trace_id,
    )
    if isinstance(normalized_request, JSONResponse):
        return normalized_request

    return _create_notification_batch(
        request_data=normalized_request,
        admin_id=admin_id,
        db=db,
        trace_id=trace_id,
    )
