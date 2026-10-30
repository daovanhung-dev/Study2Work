"""Điều phối ADMIN auth, read-only queries và Discussion Page cho API #98."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_98_admin_discussions_detail.models import (
    AdminDiscussionAuthor,
    AdminDiscussionComment,
    AdminDiscussionDetail,
    AdminDiscussionDetailPage,
    GetAdminDiscussionDetailEnvelope,
)
from app.modules.admin.api_98_admin_discussions_detail.query import (
    FIND_ADMIN_DISCUSSION_DETAIL,
    LIST_ADMIN_DISCUSSION_DETAIL_COMMENTS,
)
from app.modules.admin.api_98_admin_discussions_detail.validate import (
    MAX_INT64,
    parse_admin_discussion_detail_id,
)
from app.modules.guest._shared.course_catalog.models import Pagination
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng 404 cho path ID sai hoặc Discussion không tồn tại."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Discussion was not found.",
        trace_id=trace_id,
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi query hoặc ánh xạ Discussion thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Discussion detail could not be retrieved.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc lỗi mà không che phản hồi lỗi ban đầu."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin discussion detail rollback failed; trace_id=%s", trace_id)


def _discussion_title(content: str, *, discussion_id: int) -> str:
    """Tạo title fallback nhất quán với API #97 từ content legacy không có title."""

    normalized_content = " ".join(content.split())
    if not normalized_content:
        return f"Thảo luận #{discussion_id}"
    return normalized_content[:120]


def _map_author(
    row: Mapping[str, Any],
    *,
    trace_id: str,
) -> AdminDiscussionAuthor | None:
    """Kiểm tra author projection bắt buộc và dựng UserSummary."""

    author_id = row.get("author_id")
    full_name = row.get("author_full_name")
    avatar_url = row.get("author_avatar_url")
    if (
        type(author_id) is not int
        or not 1 <= author_id <= MAX_INT64
        or not isinstance(full_name, str)
        or (avatar_url is not None and not isinstance(avatar_url, str))
    ):
        logger.error("Admin discussion author mapping failed; trace_id=%s", trace_id)
        return None
    try:
        return AdminDiscussionAuthor(
            id=author_id,
            full_name=full_name,
            avatar_url=avatar_url,
        )
    except (TypeError, ValidationError):
        logger.error("Admin discussion author projection failed; trace_id=%s", trace_id)
        return None


def _map_comment(
    row: Mapping[str, Any],
    *,
    discussion_id: int,
    trace_id: str,
) -> AdminDiscussionComment | None:
    """Kiểm tra child row và ánh xạ vào DiscussionComment của catalog."""

    comment_id = row.get("id")
    parent_id = row.get("discussion_id")
    content = row.get("content")
    created_at = row.get("created_at")
    if (
        type(comment_id) is not int
        or not 1 <= comment_id <= MAX_INT64
        or type(parent_id) is not int
        or parent_id != discussion_id
        or not isinstance(content, str)
        or not isinstance(created_at, datetime)
    ):
        logger.error("Admin discussion comment row mapping failed; trace_id=%s", trace_id)
        return None

    author = _map_author(row, trace_id=trace_id)
    if author is None:
        return None
    try:
        return AdminDiscussionComment(
            id=comment_id,
            discussion_id=parent_id,
            content=content,
            author=author,
            created_at=created_at,
        )
    except (TypeError, ValidationError):
        logger.error("Admin discussion comment projection failed; trace_id=%s", trace_id)
        return None


def _map_discussion(
    row: Mapping[str, Any],
    *,
    discussion_id: int,
    comments: list[AdminDiscussionComment],
    trace_id: str,
) -> AdminDiscussionDetail | None:
    """Kiểm tra Discussion và map các field bắt buộc theo reusable schema."""

    course_id = row.get("course_id")
    content = row.get("content")
    status = row.get("status")
    if (
        type(row.get("id")) is not int
        or row.get("id") != discussion_id
        or type(course_id) is not int
        or not 1 <= course_id <= MAX_INT64
        or not isinstance(content, str)
        or not isinstance(status, str)
    ):
        logger.error("Admin discussion row mapping failed; trace_id=%s", trace_id)
        return None

    author = _map_author(row, trace_id=trace_id)
    if author is None:
        return None
    try:
        return AdminDiscussionDetail(
            id=discussion_id,
            course_id=course_id,
            title=_discussion_title(content, discussion_id=discussion_id),
            content=content,
            author=author,
            status=status,
            comments=comments,
        )
    except (TypeError, ValidationError):
        logger.error("Admin discussion projection failed; trace_id=%s", trace_id)
        return None


def _map_page(
    row: Any,
    comment_rows: Any,
    *,
    discussion_id: int,
    trace_id: str,
) -> AdminDiscussionDetailPage | None:
    """Map một Discussion, direct-child comments và metadata one-item Page."""

    if not isinstance(row, Mapping) or not isinstance(comment_rows, list):
        return None

    # Giữ mọi status để Admin xem được nội dung phục vụ moderation.
    comments: list[AdminDiscussionComment] = []
    for comment_row in comment_rows:
        if not isinstance(comment_row, Mapping):
            return None
        comment = _map_comment(
            comment_row,
            discussion_id=discussion_id,
            trace_id=trace_id,
        )
        if comment is None:
            return None
        comments.append(comment)

    # One-item Page được suy ra từ path ID và response catalog; report không có field để ánh xạ.
    discussion = _map_discussion(
        row,
        discussion_id=discussion_id,
        comments=comments,
        trace_id=trace_id,
    )
    if discussion is None:
        return None
    try:
        return AdminDiscussionDetailPage(
            items=[discussion],
            pagination=Pagination(page=1, size=1, total=1, total_pages=1),
        )
    except (TypeError, ValidationError):
        logger.error("Admin discussion page mapping failed; trace_id=%s", trace_id)
        return None


def get_admin_discussion_detail(
    *,
    authorization: str | None,
    discussion_id_value: object,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN rồi trả Discussion cùng các comment trực tiếp."""

    # Xác thực role trước path parsing và mọi truy cập database.
    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Discussion detail could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    # Catalog không có 422 cho endpoint này; ID sai dùng 404 như các detail Admin cùng nhóm.
    discussion_id = parse_admin_discussion_detail_id(discussion_id_value)
    if discussion_id is None:
        return _not_found(trace_id)

    try:
        # Đọc đúng Discussion và author; LEFT JOIN để lỗi integrity không biến thành 404 giả.
        row = query_one(
            db,
            FIND_ADMIN_DISCUSSION_DETAIL,
            {"discussion_id": discussion_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin discussion detail lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Không tồn tại target trả 404 mà không đọc child rows.
    if row is None:
        return _not_found(trace_id)

    try:
        # API Admin đọc mọi comment con trực tiếp theo thứ tự ổn định, không lọc status Student.
        comment_rows = query_many(
            db,
            LIST_ADMIN_DISCUSSION_DETAIL_COMMENTS,
            {"discussion_id": discussion_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin discussion comments query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Ánh xạ chặt chẽ để không trả thread thiếu author/course bắt buộc của catalog.
    page = _map_page(
        row,
        comment_rows,
        discussion_id=discussion_id,
        trace_id=trace_id,
    )
    if page is None:
        _rollback_safely(db, trace_id=trace_id)
        return _internal_error(trace_id)

    try:
        envelope = GetAdminDiscussionDetailEnvelope.model_validate(
            success_response(
                business_code="DESIGN_RESOURCE_RETRIEVED",
                message="Discussion detail was retrieved.",
                trace_id=trace_id,
                data=page.model_dump(mode="json", exclude_none=True),
            )
        )
    except (TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin discussion detail envelope failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # GET chỉ đọc; report fields không được thêm vì schema Discussion chưa khai báo chúng.
    return envelope.model_dump(mode="json", exclude_none=True)
