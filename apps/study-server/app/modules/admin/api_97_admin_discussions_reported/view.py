"""Điều phối auth Admin, read-only queries và Discussion Page cho API #97."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_97_admin_discussions_reported.models import (
    AdminDiscussionAuthor,
    AdminReportedDiscussion,
    AdminReportedDiscussionsPage,
    AdminReportedDiscussionsQuery,
    GetAdminReportedDiscussionsEnvelope,
)
from app.modules.admin.api_97_admin_discussions_reported.query import (
    COUNT_ADMIN_REPORTED_DISCUSSIONS,
    LIST_ADMIN_REPORTED_DISCUSSIONS,
)
from app.modules.admin.api_97_admin_discussions_reported.validate import (
    validate_admin_reported_discussions_request,
)
from app.modules.guest._shared.course_catalog.models import Pagination
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
DEFAULT_PAGE_SIZE = 20
MAX_INT64 = 2**63 - 1
MAX_INT32 = 2**31 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi truy vấn hoặc ánh xạ Discussion thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Reported discussions could not be retrieved.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc lỗi mà không che phản hồi lỗi ban đầu."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin reported discussions rollback failed; trace_id=%s", trace_id)


def _query_parameters(query: AdminReportedDiscussionsQuery) -> dict[str, Any]:
    """Gom filter exact-match dùng chung cho count và list query."""

    return {"reason": query.reason, "severity": query.severity}


def _normalize_count_row(count_row: Any, *, trace_id: str) -> int | None:
    """Kiểm tra COUNT projection và miền int64 của PageMeta.total."""

    if not isinstance(count_row, Mapping):
        return None
    total = count_row.get("total")
    if type(total) is not int or not 0 <= total <= MAX_INT64:
        logger.error("Admin reported discussions count mapping failed; trace_id=%s", trace_id)
        return None
    return total


def _discussion_title(content: str, *, discussion_id: int) -> str:
    """Lấy tiêu đề queue tối đa 120 ký tự từ nội dung đã gộp khoảng trắng."""

    normalized_content = " ".join(content.split())
    if not normalized_content:
        return f"Thảo luận #{discussion_id}"
    return normalized_content[:120]


def _map_discussion_row(
    row: Mapping[str, Any],
    *,
    trace_id: str,
) -> AdminReportedDiscussion | None:
    """Kiểm tra khóa và author bắt buộc rồi dựng Discussion summary."""

    discussion_id = row.get("id")
    course_id = row.get("course_id")
    content = row.get("content")
    status = row.get("status")
    author_id = row.get("author_id")
    author_full_name = row.get("author_full_name")
    author_avatar_url = row.get("author_avatar_url")
    if (
        type(discussion_id) is not int
        or not 1 <= discussion_id <= MAX_INT64
        or type(course_id) is not int
        or not 1 <= course_id <= MAX_INT64
        or not isinstance(content, str)
        or not isinstance(status, str)
        or type(author_id) is not int
        or not 1 <= author_id <= MAX_INT64
        or not isinstance(author_full_name, str)
        or (author_avatar_url is not None and not isinstance(author_avatar_url, str))
    ):
        logger.error("Admin reported discussion row mapping failed; trace_id=%s", trace_id)
        return None

    try:
        return AdminReportedDiscussion(
            id=discussion_id,
            course_id=course_id,
            title=_discussion_title(content, discussion_id=discussion_id),
            content=content,
            author=AdminDiscussionAuthor(
                id=author_id,
                full_name=author_full_name,
                avatar_url=author_avatar_url,
            ),
            status=status,
            comments=[],
        )
    except (TypeError, ValidationError):
        logger.error("Admin reported discussion projection failed; trace_id=%s", trace_id)
        return None


def _map_page(
    rows: Any,
    *,
    total: int,
    query: AdminReportedDiscussionsQuery,
    trace_id: str,
) -> AdminReportedDiscussionsPage | None:
    """Map các item và metadata Page theo size cố định của queue."""

    if not isinstance(rows, list) or len(rows) > DEFAULT_PAGE_SIZE:
        return None

    # Từ chối row sai dạng hoặc thiếu author/course thay vì trả Discussion giả.
    items: list[AdminReportedDiscussion] = []
    for row in rows:
        if not isinstance(row, Mapping):
            return None
        item = _map_discussion_row(row, trace_id=trace_id)
        if item is None:
            return None
        items.append(item)

    total_pages = (total + DEFAULT_PAGE_SIZE - 1) // DEFAULT_PAGE_SIZE if total else 0
    if total_pages > MAX_INT32:
        logger.error("Admin reported discussions page count exceeds int32; trace_id=%s", trace_id)
        return None
    try:
        return AdminReportedDiscussionsPage(
            items=items,
            pagination=Pagination(
                page=query.page,
                size=DEFAULT_PAGE_SIZE,
                total=total,
                total_pages=total_pages,
            ),
        )
    except (TypeError, ValidationError):
        return None


def get_admin_reported_discussions(
    *,
    authorization: str | None,
    reason_value: str | None,
    severity_value: str | None,
    page_value: str | None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN rồi trả trang Discussion có report còn mở."""

    # Xác thực role trước khi parse page hoặc truy cập database.
    validated_query = validate_admin_reported_discussions_request(
        authorization,
        reason_value=reason_value,
        severity_value=severity_value,
        page_value=page_value,
        trace_id=trace_id,
    )
    if isinstance(validated_query, JSONResponse):
        return validated_query

    # Dùng cùng filter cho COUNT và lấy hai mươi Discussion có report mới nhất.
    base_parameters = _query_parameters(validated_query)
    page_parameters = {
        **base_parameters,
        "limit": DEFAULT_PAGE_SIZE,
        "offset": (validated_query.page - 1) * DEFAULT_PAGE_SIZE,
    }
    try:
        count_row = query_one(db, COUNT_ADMIN_REPORTED_DISCUSSIONS, base_parameters)
        rows = query_many(db, LIST_ADMIN_REPORTED_DISCUSSIONS, page_parameters)
    except SQLAlchemyError:
        # GET chỉ đọc; rollback khi DB lỗi trước khi dựng lỗi an toàn.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin reported discussions query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Không trả Page nếu count hoặc bất kỳ Discussion projection nào sai dạng.
    total = _normalize_count_row(count_row, trace_id=trace_id)
    if total is None:
        _rollback_safely(db, trace_id=trace_id)
        return _internal_error(trace_id)
    page = _map_page(
        rows,
        total=total,
        query=validated_query,
        trace_id=trace_id,
    )
    if page is None:
        _rollback_safely(db, trace_id=trace_id)
        return _internal_error(trace_id)

    # Trả Page kể cả khi không có report hoặc page nằm ngoài phạm vi.
    try:
        envelope = GetAdminReportedDiscussionsEnvelope.model_validate(
            success_response(
                business_code="DESIGN_RESOURCE_RETRIEVED",
                message=(
                    "Reported discussions retrieved."
                    if page.items
                    else "No reported discussions found."
                ),
                trace_id=trace_id,
                data=page.model_dump(mode="json", exclude_none=True),
            )
        )
    except ValidationError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin reported discussions envelope failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Không commit hoặc cập nhật report/discussion trong endpoint GET này.
    return envelope.model_dump(mode="json", exclude_none=True)
