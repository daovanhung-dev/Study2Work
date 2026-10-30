"""Điều phối quyền Admin, đọc pending Content và dựng Page API #78."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_78_admin_content_pending.models import (
    AdminPendingContentsPage,
    AdminPendingContentsQuery,
)
from app.modules.admin.api_78_admin_content_pending.query import (
    COUNT_ADMIN_PENDING_CONTENTS,
    LIST_ADMIN_PENDING_CONTENTS,
)
from app.modules.admin.api_78_admin_content_pending.validate import (
    validate_admin_pending_query,
    validate_admin_request,
)
from app.modules.guest._shared.course_catalog.models import Pagination
from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
DEFAULT_PAGE_SIZE = 20
MAX_INT64 = 2**63 - 1
MAX_INT32 = 2**31 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho query hoặc ánh xạ hàng chờ Content."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Pending content could not be retrieved.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc lỗi mà không che response lỗi ban đầu."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin pending content rollback failed; trace_id=%s", trace_id)


def _query_parameters(query: AdminPendingContentsQuery) -> dict[str, Any]:
    """Gom filter chung để count và list dùng đúng cùng một tập điều kiện."""

    return {"content_type": query.content_type, "course_id": query.course_id}


def _normalize_count_row(count_row: Any, *, trace_id: str) -> int | None:
    """Kiểm tra projection COUNT và giới hạn total theo PageMeta int64."""

    if not isinstance(count_row, Mapping):
        return None
    total = count_row.get("total")
    if type(total) is not int or not 0 <= total <= MAX_INT64:
        logger.error("Admin pending content count mapping failed; trace_id=%s", trace_id)
        return None
    return total


def _map_content_row(
    row: Mapping[str, Any],
    *,
    query: AdminPendingContentsQuery,
) -> ContentResponse | None:
    """Kiểm tra row thỏa queue/filter rồi ánh xạ reusable Content projection."""

    payload = row.get("payload")
    if (
        row.get("status") != "PENDING_REVIEW"
        or (query.content_type is not None and row.get("content_type") != query.content_type)
        or (query.course_id is not None and row.get("course_id") != query.course_id)
        or not isinstance(payload, Mapping)
    ):
        return None

    try:
        return ContentResponse(
            id=row.get("id"),
            course_id=row.get("course_id"),
            content_type=row.get("content_type"),
            title=row.get("title"),
            payload=dict(payload),
            status=row.get("status"),
            parent_id=row.get("parent_id"),
            order=row.get("order"),
        )
    except (TypeError, ValidationError):
        return None


def _map_page(
    rows: Any,
    *,
    total: int,
    query: AdminPendingContentsQuery,
    trace_id: str,
) -> AdminPendingContentsPage | None:
    """Ánh xạ list rows thành Page, từ chối sai shape hoặc pagination vượt int32."""

    if not isinstance(rows, list) or len(rows) > DEFAULT_PAGE_SIZE:
        return None
    items: list[ContentResponse] = []
    for row in rows:
        if not isinstance(row, Mapping):
            return None
        content = _map_content_row(row, query=query)
        if content is None:
            return None
        items.append(content)

    total_pages = (total + DEFAULT_PAGE_SIZE - 1) // DEFAULT_PAGE_SIZE if total else 0
    if total_pages > MAX_INT32:
        logger.error("Admin pending content page count exceeds int32; trace_id=%s", trace_id)
        return None
    try:
        return AdminPendingContentsPage(
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


# API #78 admin_content_pending
def get_admin_pending_contents(
    *,
    authorization: str | None,
    content_type_value: str | None,
    course_value: str | None,
    page_value: str | None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Yêu cầu role ADMIN rồi trả trang Content active có trạng thái PENDING_REVIEW."""

    # Xác thực Bearer/JWT và role Admin trước khi parse query hoặc truy cập DB.
    authentication = validate_admin_request(authorization, trace_id=trace_id)
    if isinstance(authentication, JSONResponse):
        return authentication

    # Parse các query số từ chuỗi thô để giữ thứ tự auth trước validation.
    validated_query = validate_admin_pending_query(
        content_type=content_type_value,
        course_value=course_value,
        page_value=page_value,
        trace_id=trace_id,
    )
    if isinstance(validated_query, JSONResponse):
        return validated_query

    # Count và page dùng cùng queue/filter predicates, page cố định 20 hàng.
    base_params = _query_parameters(validated_query)
    page_params = {
        **base_params,
        "limit": DEFAULT_PAGE_SIZE,
        "offset": (validated_query.page - 1) * DEFAULT_PAGE_SIZE,
    }
    try:
        count_row = query_one(db, COUNT_ADMIN_PENDING_CONTENTS, base_params)
        rows = query_many(db, LIST_ADMIN_PENDING_CONTENTS, page_params)
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin pending content query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Không trả count hoặc row projection sai như thể đó là một trang hợp lệ.
    total = _normalize_count_row(count_row, trace_id=trace_id)
    if total is None:
        _rollback_safely(db, trace_id=trace_id)
        return _internal_error(trace_id)
    page = _map_page(rows, total=total, query=validated_query, trace_id=trace_id)
    if page is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin pending content page mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # GET chỉ đọc; trả cả trang rỗng hợp lệ mà không commit hay ghi trạng thái.
    page_data = page.model_dump(mode="json", exclude_none=True)
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Pending content retrieved." if page.items else "No pending content found.",
        trace_id=trace_id,
        data=page_data,
    )
