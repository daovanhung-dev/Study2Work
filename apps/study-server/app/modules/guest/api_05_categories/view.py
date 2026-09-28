from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_many
from app.core.responses import ApiError, success_response
from app.modules.guest.api_05_categories.models import (
    Category,
    CategoryPage,
    Pagination,
)
from app.modules.guest.api_05_categories.query import ACTIVE_CATEGORIES
from app.modules.guest.api_05_categories.validate import resolve_category_locale
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

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


# API #05 categories
def get_categories(
    *,
    locale: str | None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Chọn locale được yêu cầu hoặc DEFAULT_LOCALE, đọc category đang hoạt động rồi xác thực từng
    hàng bằng model. Hàm dựng metadata một trang, trả envelope thành công kể cả khi danh sách
    rỗng, rollback khi truy vấn lỗi và ánh xạ lỗi dữ liệu thành lỗi nội bộ an toàn."""

    resolved_locale = resolve_category_locale(locale)

    try:
        rows = find_active_categories(db, locale=resolved_locale)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Category lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

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
    except ValidationError:
        logger.exception("Category mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Categories retrieved." if total else "No active categories.",
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Return a safe API #5 internal-error response with the request trace ID."""
    return ApiError(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Categories could not be retrieved.",
        trace_id=trace_id,
    )
