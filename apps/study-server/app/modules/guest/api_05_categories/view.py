from __future__ import annotations

import logging
from typing import Any

from app.core.responses import ApiError, success_response
from app.modules.guest.api_05_categories.models import (
    DEFAULT_LOCALE,
    Category,
    CategoryPage,
    Pagination,
)
from app.modules.guest.api_05_categories.query import find_active_categories
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def get_categories(
    *,
    locale: str | None,
    db: Session,
    trace_id: str,
) -> dict[str, Any]:
    """Return active categories for the requested or default locale."""

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


def _internal_error(trace_id: str) -> ApiError:
    return ApiError(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Categories could not be retrieved.",
        trace_id=trace_id,
    )
