"""Điều phối quyền Mentor, truy vấn và ánh xạ danh sách SupportRequest cho API #58."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_58_mentor_support_requests.models import (
    GetMentorSupportRequestsEnvelope,
    MentorSupportRequestsQuery,
    SupportMessageResponse,
    SupportRequestResponse,
    UserSummaryResponse,
)
from app.modules.mentor.api_58_mentor_support_requests.query import (
    FIND_MENTOR_COURSE,
    LIST_MENTOR_SUPPORT_MESSAGES,
    LIST_MENTOR_SUPPORT_REQUESTS,
)
from app.modules.student.api_34_uploads.models import UploadAssetResponse
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


_REQUEST_FIELDS = ("id", "course_id", "student_id", "status", "created_at")
_MESSAGE_FIELDS = (
    "message_id",
    "author_id",
    "author_user_id",
    "author_role",
    "author_full_name",
    "content",
    "message_created_at",
)
_ASSET_FIELDS = (
    "attachment_id",
    "attachment_name",
    "attachment_url",
    "attachment_content_type",
    "attachment_size_bytes",
    "attachment_status",
)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho query hoặc projection SupportRequest."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Support requests could not be retrieved.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi course được yêu cầu thuộc Mentor khác."""

    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc dở mà không che mất lỗi gốc."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Mentor support requests rollback failed; trace_id=%s", trace_id)


def _map_requests(rows: list[dict[str, Any]]) -> list[SupportRequestResponse] | None:
    """Ánh xạ các hàng request và khởi tạo collection messages cho từng request."""

    requests: list[SupportRequestResponse] = []
    seen_ids: set[int] = set()
    try:
        for row in rows:
            # Kiểm tra tính duy nhất và quan hệ Student trước khi dựng response model.
            if not isinstance(row, Mapping):
                return None
            request_id = row.get("id")
            if type(request_id) is not int or request_id in seen_ids:
                return None
            if row.get("student_user_id") != row.get("student_id"):
                return None
            seen_ids.add(request_id)
            requests.append(
                SupportRequestResponse(
                    id=request_id,
                    course_id=row.get("course_id"),
                    student=UserSummaryResponse(
                        id=row.get("student_user_id"),
                        full_name=row.get("student_full_name"),
                        avatar_url=row.get("student_avatar_url"),
                    ),
                    status=row.get("status"),
                    messages=[],
                    created_at=row.get("created_at"),
                    resolved_at=row.get("resolved_at"),
                )
            )
    except (TypeError, ValidationError):
        return None

    return requests


def _append_messages(
    requests: list[SupportRequestResponse],
    rows: list[dict[str, Any]],
) -> bool:
    """Gom message và asset, đồng thời từ chối projection thiếu hoặc sai scope."""

    requests_by_id = {request.id: request for request in requests}
    messages_by_id: dict[int, tuple[int, SupportMessageResponse]] = {}
    assets_by_message: dict[int, set[int]] = {}

    try:
        for row in rows:
            # Giữ message thuộc đúng request và gom các hàng lặp do LEFT JOIN asset.
            if not isinstance(row, Mapping):
                return False
            request_id = row.get("request_id")
            if type(request_id) is not int or request_id not in requests_by_id:
                return False
            message_id = row.get("message_id")
            linked_upload_id = row.get("linked_upload_id")

            if message_id is None:
                has_message_fields = any(
                    row.get(field) is not None for field in _MESSAGE_FIELDS
                )
                if linked_upload_id is not None or has_message_fields:
                    return False
                if any(row.get(field) is not None for field in _ASSET_FIELDS):
                    return False
                continue

            if type(message_id) is not int:
                return False
            if row.get("author_user_id") != row.get("author_id"):
                return False

            message_entry = messages_by_id.get(message_id)
            if message_entry is None:
                message = SupportMessageResponse(
                    id=message_id,
                    author=UserSummaryResponse(
                        id=row.get("author_user_id"),
                        full_name=row.get("author_full_name"),
                        avatar_url=row.get("author_avatar_url"),
                    ),
                    content=row.get("content"),
                    attachments=[],
                    created_at=row.get("message_created_at"),
                )
                messages_by_id[message_id] = (request_id, message)
                assets_by_message[message_id] = set()
                requests_by_id[request_id].messages.append(message)
            else:
                prior_request_id, prior = message_entry
                if prior_request_id != request_id:
                    return False
                if (
                    prior.author.id != row.get("author_user_id")
                    or prior.author.full_name != row.get("author_full_name")
                    or prior.author.avatar_url != row.get("author_avatar_url")
                    or prior.content != row.get("content")
                    or prior.created_at != row.get("message_created_at")
                ):
                    return False
                message = prior

            if linked_upload_id is None:
                if any(row.get(field) is not None for field in _ASSET_FIELDS):
                    return False
                continue

            # Chỉ gắn asset khi link ID và metadata đều khớp với UploadAsset contract.
            attachment_id = row.get("attachment_id")
            if type(attachment_id) is not int or attachment_id != linked_upload_id:
                return False
            if attachment_id in assets_by_message[message_id]:
                return False
            asset = UploadAssetResponse(
                id=attachment_id,
                name=row.get("attachment_name"),
                url=row.get("attachment_url"),
                content_type=row.get("attachment_content_type"),
                size_bytes=row.get("attachment_size_bytes"),
                status=row.get("attachment_status"),
            )
            assets_by_message[message_id].add(attachment_id)
            message.attachments.append(asset)
    except (TypeError, ValidationError):
        return False

    return True


def get_mentor_support_requests(
    *,
    authorization: str | None,
    support_query: MentorSupportRequestsQuery,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor rồi trả collection support request thuộc các course Mentor sở hữu."""

    # Dùng guard chung để kiểm tra Bearer, JWT, subject và role trước DB access.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Support requests could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    if support_query.course_id is not None:
        try:
            # Kiểm tra riêng course được yêu cầu để trả 403 cho course của Mentor khác.
            course = query_one(
                db,
                FIND_MENTOR_COURSE,
                {"course_id": support_query.course_id},
            )
        except SQLAlchemyError:
            # Hoàn tác transaction nếu truy vấn course bị lỗi trước khi trả response.
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Mentor course lookup failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        if course is not None:
            if (
                not isinstance(course, Mapping)
                or type(course.get("id")) is not int
                or course.get("id") != support_query.course_id
                or type(course.get("mentor_id")) is not int
            ):
                # Không dùng dữ liệu course thiếu hoặc sai kiểu để quyết định quyền.
                _rollback_safely(db, trace_id=trace_id)
                logger.error("Mentor course projection failed; trace_id=%s", trace_id)
                return _internal_error(trace_id)
            if course.get("mentor_id") != mentor_id:
                # Dừng sớm để không tiết lộ request của course thuộc Mentor khác.
                _rollback_safely(db, trace_id=trace_id)
                return _access_denied(trace_id)

    params = {
        "mentor_id": mentor_id,
        "course_id": support_query.course_id,
        "status": support_query.status,
    }
    try:
        # Đọc collection trước; chỉ tải thread khi có request để giảm query thừa.
        request_rows = query_many(db, LIST_MENTOR_SUPPORT_REQUESTS, params)
        message_rows = (
            query_many(db, LIST_MENTOR_SUPPORT_MESSAGES, params) if request_rows else []
        )
    except SQLAlchemyError:
        # Giữ truy vấn collection/thread trong cùng transaction đọc và rollback khi lỗi.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support request lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Ánh xạ request rồi ghép bulk thread; projection lỗi không được trả một phần.
    requests = _map_requests(request_rows)
    if requests is None or not _append_messages(requests, message_rows):
        # Không trả collection đã map một phần nếu projection DB không nhất quán.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support response mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Xác thực envelope hoàn chỉnh trước khi giao dữ liệu cho response helper.
    try:
        envelope = GetMentorSupportRequestsEnvelope(
            success=True,
            businessCode="DESIGN_RESOURCE_RETRIEVED",
            message=(
                "Support requests retrieved."
                if requests
                else "No support requests found."
            ),
            data=requests,
            meta={},
            traceId=trace_id,
        )
    except (TypeError, ValidationError):
        # Lỗi dựng envelope cũng kết thúc an toàn transaction đọc hiện tại.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor support envelope mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # GET không ghi dữ liệu nên không commit transaction tại use case này.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message=envelope.message,
        trace_id=trace_id,
        data=[item.model_dump(mode="json", exclude_none=True) for item in envelope.data],
    )
