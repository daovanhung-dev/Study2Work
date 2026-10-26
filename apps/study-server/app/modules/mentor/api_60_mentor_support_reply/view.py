"""Điều phối quyền, persistence và response mapping cho API #60."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.mentor._shared.support_request_projection import (
    append_support_messages,
    map_support_request,
)
from app.modules.mentor.api_59_mentor_support_request_detail.query import (
    LIST_MENTOR_SUPPORT_REQUEST_MESSAGES,
)
from app.modules.mentor.api_60_mentor_support_reply.models import (
    ReplyMentorSupportRequestEnvelope,
    ReplyToMentorSupportRequest,
)
from app.modules.mentor.api_60_mentor_support_reply.query import (
    FIND_REPLY_UPLOADS,
    INSERT_MENTOR_SUPPORT_MESSAGE,
    INSERT_MENTOR_SUPPORT_MESSAGE_UPLOADS,
    LOCK_MENTOR_SUPPORT_REQUEST_FOR_REPLY,
)
from app.modules.mentor.api_60_mentor_support_reply.validate import (
    INT64_MAX,
    parse_attachment_refs,
    parse_support_request_id,
    validate_message,
)
from app.modules.student.api_34_uploads.models import UploadAssetResponse
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho request, write hoặc projection thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Support reply could not be saved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 cho support request hoặc UploadAsset ngoài scope."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Support request or requested assets were not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi request thuộc course của Mentor khác."""

    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction dở mà không lộ hoặc che lỗi gốc."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Mentor support reply rollback failed; trace_id=%s", trace_id)


def _resolve_uploads(
    db: Session,
    *,
    asset_ids: list[int],
    mentor_id: int,
    course_id: int,
) -> list[UploadAssetResponse] | None:
    """Resolve asset metadata trong đúng owner/course/purpose/status và giữ thứ tự."""

    if not asset_ids:
        # Không chạy query uploads khi request chủ động gửi mảng rỗng.
        return []

    # Lọc toàn bộ refs tại DB theo Mentor, course, purpose và trạng thái upload.
    rows = query_many(
        db,
        FIND_REPLY_UPLOADS,
        {"asset_ids": asset_ids, "mentor_id": mentor_id, "course_id": course_id},
    )
    if len(rows) != len(asset_ids):
        return None

    assets_by_id: dict[int, UploadAssetResponse] = {}
    for row in rows:
        # Row không hợp lệ hoặc trùng ID là projection lỗi, không phải asset thiếu.
        if not isinstance(row, Mapping):
            raise TypeError("UploadAsset projection is not a mapping")
        asset_id = row.get("id")
        if type(asset_id) is not int or not 1 <= asset_id <= INT64_MAX:
            raise TypeError("UploadAsset ID projection is invalid")
        if asset_id in assets_by_id:
            raise TypeError("UploadAsset query returned duplicate IDs")
        assets_by_id[asset_id] = UploadAssetResponse.model_validate(row)

    if set(assets_by_id) != set(asset_ids):
        return None
    # Không phụ thuộc thứ tự mà PostgreSQL trả về từ ANY query.
    return [assets_by_id[asset_id] for asset_id in asset_ids]


def _insert_result_is_valid(
    row: Mapping[str, Any],
    *,
    request_id: int,
    mentor_id: int,
    message: str,
) -> bool:
    """Xác nhận INSERT trả đúng khóa, author, nội dung và timestamp."""

    # Giữ strict integer checks để bool không bị chấp nhận như khóa số 0/1.
    return (
        type(row.get("id")) is int
        and 1 <= row["id"] <= INT64_MAX
        and type(row.get("request_id")) is int
        and row.get("request_id") == request_id
        and type(row.get("author_id")) is int
        and row.get("author_id") == mentor_id
        and row.get("content") == message
        and isinstance(row.get("created_at"), datetime)
    )


def _links_match_request(rows: list[dict[str, Any]], asset_ids: list[int]) -> bool:
    """Kiểm tra toàn bộ attachment link và vị trí đã được INSERT trả về."""

    # So sánh cặp upload/position vì thứ tự RETURNING không được đảm bảo.
    if len(rows) != len(asset_ids):
        return False
    returned = {
        (row.get("upload_id"), row.get("asset_position"))
        for row in rows
        if isinstance(row, Mapping)
    }
    expected = {(asset_id, position) for position, asset_id in enumerate(asset_ids)}
    return len(returned) == len(rows) and returned == expected


def reply_to_mentor_support_request(
    *,
    authorization: str | None,
    request_id_value: str,
    reply_request: ReplyToMentorSupportRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, lưu reply cùng links rồi trả SupportRequest đã hydrate."""

    # Guard chung kiểm tra Bearer, JWT, numeric subject và role trước DB access.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Support reply could not be saved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    request_id = parse_support_request_id(request_id_value, trace_id=trace_id)
    if isinstance(request_id, JSONResponse):
        return request_id
    message_error = validate_message(reply_request.message, trace_id=trace_id)
    if message_error is not None:
        return message_error
    asset_ids = parse_attachment_refs(reply_request.attachment_refs, trace_id=trace_id)
    if isinstance(asset_ids, JSONResponse):
        return asset_ids

    try:
        # Khóa request trước khi kiểm tra quyền và tạo message trong cùng transaction.
        request_row = query_one(
            db,
            LOCK_MENTOR_SUPPORT_REQUEST_FOR_REPLY,
            {"request_id": request_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support reply request lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if request_row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(request_row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support reply request projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    support_request = map_support_request(request_row, request_id)
    if support_request is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support reply parent projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if request_row.get("mentor_id") != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    try:
        assets = _resolve_uploads(
            db,
            asset_ids=asset_ids,
            mentor_id=mentor_id,
            course_id=support_request.course_id,
        )
    except (SQLAlchemyError, KeyError, TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support reply asset lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if assets is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)

    try:
        # Predicate owner được lặp lại trong INSERT để bảo vệ write tại statement boundary.
        inserted = query_one(
            db,
            INSERT_MENTOR_SUPPORT_MESSAGE,
            {"request_id": request_id, "mentor_id": mentor_id, "message": reply_request.message},
        )
        if inserted is None:
            # Phân loại lại owner sau race giữa lookup và INSERT; không tạo row nếu scope đổi.
            current = query_one(
                db,
                LOCK_MENTOR_SUPPORT_REQUEST_FOR_REPLY,
                {"request_id": request_id},
            )
            _rollback_safely(db, trace_id=trace_id)
            if current is None:
                return _not_found(trace_id)
            if isinstance(current, Mapping) and current.get("mentor_id") != mentor_id:
                return _access_denied(trace_id)
            logger.error("Mentor support reply insert returned no row; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        if not isinstance(inserted, Mapping) or not _insert_result_is_valid(
            inserted,
            request_id=request_id,
            mentor_id=mentor_id,
            message=reply_request.message,
        ):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Mentor support reply insert mapping failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        message_id = inserted["id"]
        if asset_ids:
            link_rows = query_many(
                db,
                INSERT_MENTOR_SUPPORT_MESSAGE_UPLOADS,
                {"message_id": message_id, "asset_ids": asset_ids},
            )
            if not _links_match_request(link_rows, asset_ids):
                _rollback_safely(db, trace_id=trace_id)
                logger.error("Mentor support reply links were incomplete; trace_id=%s", trace_id)
                return _internal_error(trace_id)

        # Dùng đúng query/projection của #59 để trả trọn thread sau mutation.
        message_rows = query_many(
            db,
            LIST_MENTOR_SUPPORT_REQUEST_MESSAGES,
            {"request_id": request_id, "mentor_id": mentor_id},
        )
        if not append_support_messages(support_request, message_rows, mentor_id=mentor_id):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Mentor support reply thread mapping failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        new_messages = [item for item in support_request.messages if item.id == message_id]
        if (
            len(new_messages) != 1
            or new_messages[0].author.id != mentor_id
            or new_messages[0].content != reply_request.message
            or new_messages[0].created_at != inserted.get("created_at")
            or [asset.id for asset in new_messages[0].attachments] != asset_ids
            or support_request.status != request_row.get("status")
        ):
            _rollback_safely(db, trace_id=trace_id)
            logger.error(
                "Mentor support reply response did not match insert; trace_id=%s",
                trace_id,
            )
            return _internal_error(trace_id)

        envelope = ReplyMentorSupportRequestEnvelope(
            success=True,
            businessCode="DESIGN_RESOURCE_UPDATED",
            message="Support reply saved.",
            data=support_request,
            meta={},
            traceId=trace_id,
        )
        response_data = envelope.data.model_dump(mode="json", exclude_none=True)
        db.commit()
    except (SQLAlchemyError, KeyError, TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support reply transaction failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message=envelope.message,
        trace_id=trace_id,
        data=response_data,
    )
