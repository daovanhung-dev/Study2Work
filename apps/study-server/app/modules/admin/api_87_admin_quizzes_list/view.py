"""Điều phối quyền Admin, truy vấn và ánh xạ Page<Quiz> của API #87."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from decimal import Decimal, InvalidOperation
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_87_admin_quizzes_list.models import (
    AdminQuizResponse,
    AdminQuizzesPage,
    AdminQuizzesQuery,
)
from app.modules.admin.api_87_admin_quizzes_list.query import (
    COUNT_ADMIN_QUIZZES,
    LIST_ADMIN_QUIZZES,
)
from app.modules.admin.api_87_admin_quizzes_list.validate import validate_admin_quizzes_request
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
    """Build a safe internal error response for query or Quiz projection failures."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Quizzes could not be retrieved.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback a failed read transaction without masking its HTTP response."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin quiz list rollback failed; trace_id=%s", trace_id)


def _query_parameters(query: AdminQuizzesQuery) -> dict[str, Any]:
    """Build the shared exact-filter bindings used by both count and page SQL."""

    return {"course_id": query.course_id, "status": query.status}


def _normalize_count_row(count_row: Any, *, trace_id: str) -> int | None:
    """Validate COUNT projection and its reusable PageMeta int64 range."""

    if not isinstance(count_row, Mapping):
        return None
    total = count_row.get("total")
    if type(total) is not int or not 0 <= total <= MAX_INT64:
        logger.error("Admin quiz count mapping failed; trace_id=%s", trace_id)
        return None
    return total


def _decimal_string(value: Any) -> str | None:
    """Format a finite database numeric value as a non-exponent decimal string."""

    if isinstance(value, bool) or value is None:
        return None
    try:
        decimal_value = Decimal(str(value))
    except InvalidOperation:
        return None
    if not decimal_value.is_finite():
        return None
    return format(decimal_value, "f")


def _map_quiz_row(row: Mapping[str, Any]) -> AdminQuizResponse | None:
    """Map one legacy Quiz metadata row and leave unsupported nested schema empty."""

    quiz_id = row.get("id")
    course_id = row.get("course_id")
    title = row.get("title")
    duration_minutes = row.get("duration_minutes")
    passing_score = _decimal_string(row.get("passing_score"))
    if (
        type(quiz_id) is not int
        or not 1 <= quiz_id <= MAX_INT64
        or type(course_id) is not int
        or not 1 <= course_id <= MAX_INT64
        or not isinstance(title, str)
        or (duration_minutes is not None and type(duration_minutes) is not int)
        or (
            duration_minutes is not None
            and not -(2**31) <= duration_minutes <= MAX_INT32
        )
        or passing_score is None
    ):
        return None

    try:
        return AdminQuizResponse(
            id=quiz_id,
            course_id=course_id,
            title=title,
            duration_minutes=duration_minutes,
            passing_score=passing_score,
            questions=[],
        )
    except (TypeError, ValidationError):
        return None


def _map_quiz_page(
    rows: Any,
    *,
    total: int,
    query: AdminQuizzesQuery,
    trace_id: str,
) -> AdminQuizzesPage | None:
    """Map page rows and build a fixed-size Page while validating total-page bounds."""

    if not isinstance(rows, list) or len(rows) > DEFAULT_PAGE_SIZE:
        return None

    items: list[AdminQuizResponse] = []
    for row in rows:
        if not isinstance(row, Mapping):
            return None
        item = _map_quiz_row(row)
        if item is None:
            logger.error("Admin quiz row mapping failed; trace_id=%s", trace_id)
            return None
        items.append(item)

    total_pages = (total + DEFAULT_PAGE_SIZE - 1) // DEFAULT_PAGE_SIZE if total else 0
    if total_pages > MAX_INT32:
        logger.error("Admin quiz total pages exceed int32; trace_id=%s", trace_id)
        return None
    try:
        return AdminQuizzesPage(
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


# API #87 admin_quizzes_list
def get_admin_quizzes(
    *,
    authorization: str | None,
    course_value: str | None,
    status_value: str | None,
    page_value: str | None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Require ADMIN, apply exact filters and return a read-only page of Quiz metadata."""

    # Xác thực role ADMIN trước khi parse filter hoặc truy cập database.
    validated_query = validate_admin_quizzes_request(
        authorization,
        course_value=course_value,
        status_value=status_value,
        page_value=page_value,
        trace_id=trace_id,
    )
    if isinstance(validated_query, JSONResponse):
        return validated_query

    # Dùng cùng bộ filter cho count và page; offset dựa trên trang 1-based và size 20.
    base_parameters = _query_parameters(validated_query)
    page_parameters = {
        **base_parameters,
        "limit": DEFAULT_PAGE_SIZE,
        "offset": (validated_query.page - 1) * DEFAULT_PAGE_SIZE,
    }
    try:
        count_row = query_one(db, COUNT_ADMIN_QUIZZES, base_parameters)
        rows = query_many(db, LIST_ADMIN_QUIZZES, page_parameters)
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin quiz list query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Từ chối count hoặc projection sai để không trả Page thiếu hoặc sai contract.
    total = _normalize_count_row(count_row, trace_id=trace_id)
    if total is None:
        _rollback_safely(db, trace_id=trace_id)
        return _internal_error(trace_id)
    page = _map_quiz_page(
        rows,
        total=total,
        query=validated_query,
        trace_id=trace_id,
    )
    if page is None:
        _rollback_safely(db, trace_id=trace_id)
        return _internal_error(trace_id)

    # GET chỉ đọc; trả Page rỗng hợp lệ mà không commit transaction.
    page_data = page.model_dump(mode="json", exclude_none=True)
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Quizzes retrieved." if page.items else "No quizzes found.",
        trace_id=trace_id,
        data=page_data,
    )
