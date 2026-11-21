"""Điều phối quyền Admin, eligibility và transaction xóa notification API #95."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.modules.admin.api_95_admin_notifications_delete.models import (
    DeleteAdminNotificationEnvelope,
    DeleteResult,
)
from app.modules.admin.api_95_admin_notifications_delete.query import (
    DELETE_ADMIN_NOTIFICATION,
    LOCK_ADMIN_NOTIFICATION_DELIVERIES_FOR_DELETE,
    LOCK_ADMIN_NOTIFICATION_FOR_DELETE,
)
from app.modules.admin.api_95_admin_notifications_delete.validate import (
    validate_admin_notification_delete_path,
)
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1
ALLOWED_CHANNELS = {"EMAIL", "PUSH"}
ALLOWED_DELIVERY_STATUSES = {"QUEUED", "SENT", "FAILED"}


def _error(
    *,
    status_code: int,
    business_code: str,
    message: str,
    trace_id: str,
    field_error: ErrorDetail | None = None,
) -> JSONResponse:
    """Dựng catalog error envelope, thêm field error nếu là 422."""

    errors = [field_error] if field_error is not None else []
    return error_response(
        status_code=status_code,
        business_code=business_code,
        message=message,
        trace_id=trace_id,
        errors=errors,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction thất bại mà không che response lỗi gốc."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin notification delete rollback failed; trace_id=%s", trace_id)


def _not_found(trace_id: str) -> JSONResponse:
    """Trả lỗi catalog khi notification không tồn tại."""

    return _error(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Notification not found.",
        trace_id=trace_id,
    )


def _invalid_state(trace_id: str) -> JSONResponse:
    """Trả 422 nếu không thể xác nhận mọi delivery vẫn đang chờ."""

    return _error(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Notification cannot be deleted in its current delivery state.",
        trace_id=trace_id,
        field_error=ErrorDetail(
            field="notification_id",
            code="NOTIFICATION_NOT_CANCELLABLE",
            message="Chỉ notification có ít nhất một delivery và tất cả đều QUEUED mới được xóa.",
        ),
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Trả lỗi 500 an toàn khi query, mapping hoặc commit thất bại."""

    return _error(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Notification could not be deleted.",
        trace_id=trace_id,
    )


def _notification_row_matches(row: Any, notification_id: int) -> bool:
    """Kiểm tra projection parent đã khóa có đúng notification đích."""

    return (
        isinstance(row, Mapping)
        and type(row.get("id")) is int
        and row.get("id") == notification_id
        and 1 <= row["id"] <= MAX_INT64
    )


def _delivery_projection(rows: Any, notification_id: int) -> tuple[list[str], bool] | None:
    """Kiểm tra các delivery đã khóa và trạng thái queue của từng channel."""

    if not isinstance(rows, list):
        return None
    channels: list[str] = []
    all_queued = True
    for row in rows:
        if (
            not isinstance(row, Mapping)
            or type(row.get("notification_id")) is not int
            or row.get("notification_id") != notification_id
            or not isinstance(row.get("channel"), str)
            or row.get("channel") not in ALLOWED_CHANNELS
            or not isinstance(row.get("status"), str)
            or row.get("status") not in ALLOWED_DELIVERY_STATUSES
        ):
            return None
        channels.append(row["channel"])
        all_queued = all_queued and row["status"] == "QUEUED"
    if len(set(channels)) != len(channels):
        return None
    return channels, all_queued


def _map_delete_result(row: Mapping[str, Any], *, notification_id: int) -> DeleteResult | None:
    """Kiểm tra ID/timestamp từ DELETE RETURNING và dựng schema catalog."""

    result_id = row.get("id")
    deleted_at = row.get("deleted_at")
    if (
        type(result_id) is not int
        or not 1 <= result_id <= MAX_INT64
        or result_id != notification_id
        or not isinstance(deleted_at, datetime)
    ):
        return None
    try:
        return DeleteResult(id=result_id, status="deleted", deleted_at=deleted_at)
    except (TypeError, ValidationError):
        return None


def delete_admin_notification(
    *,
    authorization: str | None,
    notification_id_value: object,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, khóa notification/deliveries và xóa khi còn QUEUED."""

    # Kiểm tra role qua shared guard trước khi parse path hoặc truy vấn dữ liệu.
    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Notification could not be deleted.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    # Validate raw int64 path sau auth để request lỗi không làm lộ resource lookup.
    notification_id = validate_admin_notification_delete_path(
        notification_id_value,
        trace_id=trace_id,
    )
    if isinstance(notification_id, JSONResponse):
        return notification_id

    try:
        # Khóa parent trước để chặn insert delivery mới và đồng bộ với API #94.
        notification_row = query_one(
            db,
            LOCK_ADMIN_NOTIFICATION_FOR_DELETE,
            {"notification_id": notification_id},
        )
        if notification_row is None:
            _rollback_safely(db, trace_id=trace_id)
            return _not_found(trace_id)
        if not _notification_row_matches(notification_row, notification_id):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin notification delete lock projection failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        # Khóa các delivery theo channel và chỉ cho phép trạng thái còn QUEUED.
        delivery_rows = query_many(
            db,
            LOCK_ADMIN_NOTIFICATION_DELIVERIES_FOR_DELETE,
            {"notification_id": notification_id},
        )
        delivery_projection = _delivery_projection(delivery_rows, notification_id)
        if delivery_projection is None:
            _rollback_safely(db, trace_id=trace_id)
            logger.error(
                "Admin notification delete delivery projection failed; trace_id=%s",
                trace_id,
            )
            return _internal_error(trace_id)
        channels, all_queued = delivery_projection
        if not channels or not all_queued:
            _rollback_safely(db, trace_id=trace_id)
            return _invalid_state(trace_id)

        # DDL candidate dùng ON DELETE CASCADE; xóa đúng notification được path chọn.
        deleted_row = query_one(
            db,
            DELETE_ADMIN_NOTIFICATION,
            {"notification_id": notification_id},
        )
        if deleted_row is None:
            _rollback_safely(db, trace_id=trace_id)
            return _not_found(trace_id)
        if not isinstance(deleted_row, Mapping):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin notification delete projection failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        result = _map_delete_result(deleted_row, notification_id=notification_id)
        if result is None:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin notification delete result mapping failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        try:
            # Kiểm tra envelope trước khi commit để lỗi mapping không xóa dữ liệu.
            envelope = DeleteAdminNotificationEnvelope.model_validate(
                success_response(
                    business_code="DESIGN_RESOURCE_DELETED",
                    message="Notification deleted.",
                    trace_id=trace_id,
                    data=result.model_dump(mode="json"),
                )
            )
        except (TypeError, ValidationError):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin notification delete envelope mapping failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        # Commit sau khi đã xác thực đầy đủ DeleteResult và envelope response.
        db.commit()
        return envelope.model_dump(mode="json", exclude_none=True)
    except SQLAlchemyError:
        # Hoàn tác delete/cascade nếu query hoặc commit gặp lỗi database.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin notification delete database operation failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
