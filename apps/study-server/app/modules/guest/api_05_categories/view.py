from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_many
from app.core.responses import ApiError, _ApiError, success_response
from app.modules.guest.api_05_categories.models import (
    DEFAULT_LOCALE,
    Category,
    CategoryPage,
    Pagination,
)
from app.modules.guest.api_05_categories.query import ACTIVE_CATEGORIES
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def find_active_categories(
    db: Session,
    *,
    locale: str,
) -> list[dict[str, Any]]:
    """Truy vấn danh sách category có status ACTIVE và locale khớp chính xác với giá trị truyền
    vào. Trả các hàng dưới dạng dict; transaction vẫn do caller sở hữu."""

    return query_many(
        db,
        ACTIVE_CATEGORIES,
        {
            "status": "ACTIVE",
            "locale": locale,
        },
    )


def get_categories(
    *,
    locale: str | None,
    db: Session,
    trace_id: str,
) -> dict[str, Any]:
    """Chọn locale được yêu cầu hoặc DEFAULT_LOCALE, đọc category đang hoạt động rồi xác thực từng
    hàng bằng model. Hàm dựng metadata một trang, trả envelope thành công kể cả khi danh sách
    rỗng, rollback khi truy vấn lỗi và ánh xạ lỗi dữ liệu thành lỗi nội bộ an toàn."""

    resolved_locale = locale if locale is not None else DEFAULT_LOCALE

    try:
        rows = find_active_categories(db, locale=resolved_locale)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Category lookup failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id) from exc

    try:
        items = [Category.model_validate(row) for row in rows]
        total = len(items)
        page = CategoryPage(
            items=items,
            pagination=Pagination(
                page=1,
                size=total,
                total=total,
                total_pages=1,
            ),
        )
    except ValidationError as exc:
        logger.exception("Category mapping failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id) from exc

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Categories retrieved." if total else "No active categories.",
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )


def _internal_error(trace_id: str) -> _ApiError:
    """Tạo _ApiError HTTP 500 cho lỗi truy vấn hoặc ánh xạ category, kèm business code nội bộ và
    trace ID của request."""
    return ApiError(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Categories could not be retrieved.",
        trace_id=trace_id,
    )
