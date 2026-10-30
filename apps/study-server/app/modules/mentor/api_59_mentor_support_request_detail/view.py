"""Điều phối quyền Mentor và dựng chi tiết SupportRequest cho API #59."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.mentor._shared.support_request_projection import (
    append_support_messages as _append_messages,
)
from app.modules.mentor._shared.support_request_projection import (
    map_support_request as _map_request,
)
from app.modules.mentor.api_59_mentor_support_request_detail.models import (
    GetMentorSupportRequestEnvelope,
)
from app.modules.mentor.api_59_mentor_support_request_detail.query import (
    FIND_MENTOR_SUPPORT_REQUEST,
    LIST_MENTOR_SUPPORT_REQUEST_MESSAGES,
)
from app.modules.mentor.api_59_mentor_support_request_detail.validate import (
    parse_support_request_id,
)
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho truy vấn hoặc projection SupportRequest."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Support request could not be retrieved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 cho request ID không hợp lệ hoặc không tồn tại."""

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


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc dở mà không che lỗi gốc hoặc lộ nội bộ."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Mentor support request rollback failed; trace_id=%s", trace_id)


def get_mentor_support_request(
    *,
    authorization: str | None,
    request_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, kiểm tra quyền sở hữu và trả một request cùng toàn bộ thread."""

    # Guard chung kiểm tra Bearer, JWT, numeric subject và role trước DB access.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Support request could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Giữ path dạng chuỗi để trả 404 catalog cho input sai hoặc tràn signed-int64.
    request_id = parse_support_request_id(request_id_value)
    if request_id is None:
        return _not_found(trace_id)

    try:
        # Đọc request và required parent projections trước khi phân loại quyền.
        row = query_one(db, FIND_MENTOR_SUPPORT_REQUEST, {"request_id": request_id})
    except SQLAlchemyError:
        # Kết thúc transaction đọc lỗi và chỉ ghi lỗi an toàn theo trace.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support request lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if row is None:
        # Missing request được phân loại trước owner mismatch theo contract đã chọn.
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(row, Mapping):
        # Không dùng row có dạng bất ngờ để quyết định quyền truy cập.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support request projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    support_request = _map_request(row, request_id)
    if support_request is None:
        # Parent/data projection sai định dạng là lỗi nội bộ, không trả response một phần.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support request parent projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if row.get("mentor_id") != mentor_id:
        # Request tồn tại nhưng course thuộc Mentor khác nên trả catalog 403.
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    try:
        # Luôn đọc bằng owner-scoped query, kể cả thread rỗng để kiểm tra parent lần hai.
        message_rows = query_many(
            db,
            LIST_MENTOR_SUPPORT_REQUEST_MESSAGES,
            {"request_id": request_id, "mentor_id": mentor_id},
        )
    except SQLAlchemyError:
        # Rollback nếu đọc conversation hoặc attachment metadata thất bại.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support request thread lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if not _append_messages(support_request, message_rows, mentor_id=mentor_id):
        # Bỏ toàn bộ kết quả nếu bất kỳ message/asset projection nào không nhất quán.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support request thread projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    try:
        envelope = GetMentorSupportRequestEnvelope(
            success=True,
            businessCode="DESIGN_RESOURCE_RETRIEVED",
            message="Support request retrieved.",
            data=support_request,
            meta={},
            traceId=trace_id,
        )
    except (TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support request envelope mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # GET chỉ đọc; serialize exclude_none theo response convention của API #58.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message=envelope.message,
        trace_id=trace_id,
        data=envelope.data.model_dump(mode="json", exclude_none=True),
    )
