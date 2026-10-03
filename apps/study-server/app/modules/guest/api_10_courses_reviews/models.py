from __future__ import annotations

from pydantic import BaseModel


class CourseReviewsQuery(BaseModel):
    """Khai báo kiểu và mặc định của tham số đánh giá; input rules nằm trong validate.py."""

    page: int | None = None
    rating: str | None = None