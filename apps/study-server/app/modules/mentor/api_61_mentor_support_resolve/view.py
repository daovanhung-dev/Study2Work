"""Điều phối quyền, transaction và response mapping cho API #61."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.modules.mentor._shared.support_request_projection import (
    append_support_messages,
    map_support_request,
)
from app.modules.mentor.api_59_mentor_support_request_detail.query import (
    LIST_MENTOR_SUPPORT_REQUEST_MESSAGES,
)
from app.modules.mentor.api_61_mentor_support_resolve.models import (
    ResolveMentorSupportRequestEnvelope,
)
from app.modules.mentor.api_61_mentor_support_resolve.query import (
    LOCK_MENTOR_SUPPORT_REQUEST_FOR_RESOLVE,
    UPDATE_MENTOR_SUPPORT_REQUEST_RESOLVED,
)
from app.modules.mentor.api_61_mentor_support_resolve.validate import (
    INT64_MAX,
    parse_support_request_id,
)
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

_ACTIVE_STATUSES = frozenset({"OPEN", "IN_PROGRESS", "WAITING_LEARNER"})


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho query, update hoặc response mapping thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Support request could not be resolved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 khi SupportRequest không tồn tại."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Support request not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi course của request thuộc Mentor khác."""

    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _invalid_state(trace_id: str) -> JSONResponse:
    """Dựng lỗi 422 cho SupportRequest ở trạng thái không được resolve."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Support request cannot be resolved in its current state.",
        trace_id=trace_id,
        errors=(
            ErrorDetail(
                field="status",
                code="STATE_NOT_RESOLVABLE",
                message="Support request cannot be resolved in its current state.",
            ),
        ),
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction dở mà không che lỗi gốc hoặc lộ chi tiết nội bộ."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Mentor support resolve rollback failed; trace_id=%s", trace_id)


def _update_result_is_valid(row: Mapping[str, Any], *, request_id: int) -> bool:
    """Kiểm tra RETURNING có đúng request, trạng thái và timestamp resolve."""

    return (
        type(row.get("id")) is int
        and 1 <= row["id"] <= INT64_MAX
        and row.get("id") == request_id
        and row.get("status") == "RESOLVED"
        and isinstance(row.get("resolved_at"), datetime)
    )


def _load_resolved_response(
    *,
    db: Session,
    request_row: Mapping[str, Any],
    request_id: int,
    mentor_id: int,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Tải thread, kiểm tra response rồi commit transaction resolve."""

    # Ánh xạ các trường parent bắt buộc bằng model SupportRequest dùng chung.
    support_request = map_support_request(request_row, request_id)
    if support_request is None or support_request.status != "RESOLVED":
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support resolve parent mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    try:
        # Tải thread theo đúng query có kiểm tra owner và thứ tự của API #59.
        message_rows = query_many(
            db,
            LIST_MENTOR_SUPPORT_REQUEST_MESSAGES,
            {"request_id": request_id, "mentor_id": mentor_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support resolve thread lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Từ chối toàn bộ response nếu author, parent hoặc attachment mapping thiếu.
    if not append_support_messages(support_request, message_rows, mentor_id=mentor_id):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support resolve thread mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    try:
        # Kiểm tra success envelope trước khi commit thay đổi.
        envelope = ResolveMentorSupportRequestEnvelope(
            success=True,
            businessCode="DESIGN_RESOURCE_UPDATED",
            message="Support request resolved.",
            data=support_request,
            meta={},
            traceId=trace_id,
        )
    except (TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support resolve envelope mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    try:
        # Chỉ commit sau khi full response vượt qua model validation.
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support resolve commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message=envelope.message,
        trace_id=trace_id,
        data=envelope.data.model_dump(mode="json", exclude_none=True),
    )


def resolve_mentor_support_request(
    *,
    authorization: str | None,
    request_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Resolve request trong course của Mentor và trả full SupportRequest thread."""

    # Xác thực Mentor trước khi parse input hoặc truy cập database.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Support request could not be resolved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Parse path thô để giá trị sai format/overflow dùng business code 422 của catalog.
    request_id = parse_support_request_id(request_id_value, trace_id=trace_id)
    if isinstance(request_id, JSONResponse):
        return request_id

    try:
        # Khóa request trước khi kiểm tra owner/state và thực hiện transition.
        request_row = query_one(
            db,
            LOCK_MENTOR_SUPPORT_REQUEST_FOR_RESOLVE,
            {"request_id": request_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support resolve request lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if request_row is None:
        # Không có row tương ứng nên kết thúc transaction đọc với lỗi 404.
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(request_row, Mapping):
        # Row sai shape không được dùng để quyết định quyền hoặc thay đổi trạng thái.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support resolve row mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Kiểm tra projection course/student bắt buộc trước khi dùng row.
    initial_projection = map_support_request(request_row, request_id)
    if initial_projection is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support resolve parent projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if request_row.get("mentor_id") != mentor_id:
        # Request tồn tại nhưng course thuộc Mentor khác nên trả 403.
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    current_status = request_row.get("status")
    if current_status == "RESOLVED":
        # PATCH lặp là idempotent và giữ nguyên timestamp hiện tại, kể cả giá trị null.
        return _load_resolved_response(
            db=db,
            request_row=request_row,
            request_id=request_id,
            mentor_id=mentor_id,
            trace_id=trace_id,
        )
    if current_status not in _ACTIVE_STATUSES:
        # State ngoài tập active/resolved không được chuyển tiếp trong fallback này.
        _rollback_safely(db, trace_id=trace_id)
        return _invalid_state(trace_id)

    try:
        # Lặp owner predicate ngay tại câu UPDATE để chặn write ngoài scope.
        updated = query_one(
            db,
            UPDATE_MENTOR_SUPPORT_REQUEST_RESOLVED,
            {"request_id": request_id, "mentor_id": mentor_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support resolve update failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if updated is None:
        # Đọc lại sau conditional miss để phân loại owner hoặc state đã đổi đồng thời.
        try:
            current = query_one(
                db,
                LOCK_MENTOR_SUPPORT_REQUEST_FOR_RESOLVE,
                {"request_id": request_id},
            )
        except SQLAlchemyError:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Mentor support resolve recheck failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        if current is None:
            # Recheck không còn tìm thấy request nên trả 404.
            _rollback_safely(db, trace_id=trace_id)
            return _not_found(trace_id)
        if not isinstance(current, Mapping):
            # Không dùng projection bất thường để quyết định scope hoặc lifecycle.
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Mentor support resolve recheck projection failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        current_projection = map_support_request(current, request_id)
        if current_projection is None:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Mentor support resolve recheck mapping failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        if current.get("mentor_id") != mentor_id:
            # Owner đã đổi trong lúc xử lý nên từ chối theo scope hiện tại.
            _rollback_safely(db, trace_id=trace_id)
            return _access_denied(trace_id)
        if current.get("status") == "RESOLVED":
            # Một request song song đã resolve trước; trả resource hiện tại idempotently.
            return _load_resolved_response(
                db=db,
                request_row=current,
                request_id=request_id,
                mentor_id=mentor_id,
                trace_id=trace_id,
            )
        if current.get("status") not in _ACTIVE_STATUSES:
            # State mới không còn resolve được theo transition matrix đã chọn.
            _rollback_safely(db, trace_id=trace_id)
            return _invalid_state(trace_id)
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support resolve conditional update missed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if not isinstance(updated, Mapping) or not _update_result_is_valid(
        updated,
        request_id=request_id,
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support resolve update projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Thay status/timestamp bằng RETURNING, còn các parent fields đã kiểm tra được giữ nguyên.
    resolved_row = dict(request_row)
    resolved_row["status"] = updated["status"]
    resolved_row["resolved_at"] = updated["resolved_at"]
    return _load_resolved_response(
        db=db,
        request_row=resolved_row,
        request_id=request_id,
        mentor_id=mentor_id,
        trace_id=trace_id,
    )
