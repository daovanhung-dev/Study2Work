from __future__ import annotations

from typing import Any

from app.core.database import query_many
from sqlalchemy.orm import Session

ACTIVE_CATEGORIES = """
SELECT
    c.id,
    c.name,
    c.slug,
    c.description
FROM categories AS c
WHERE c.status = :status
  AND c.locale = :locale
ORDER BY c.id ASC
"""


def find_active_categories(
    db: Session,
    *,
    locale: str,
) -> list[dict[str, Any]]:
    """Return active categories for one exact locale."""

    return query_many(
        db,
        ACTIVE_CATEGORIES,
        {
            "status": "ACTIVE",
            "locale": locale,
        },
    )
