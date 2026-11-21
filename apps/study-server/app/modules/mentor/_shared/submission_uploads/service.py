"""Đọc các tệp submission đã liên kết trong đúng phạm vi Mentor."""

from __future__ import annotations

from app.core.database import query_many
from app.modules.mentor._shared.submission_uploads.query import (
    FIND_MENTOR_SUBMISSION_UPLOADS,
)
from sqlalchemy.orm import Session


def find_mentor_submission_uploads(
    db: Session,
    *,
    submission_ids: list[int],
    mentor_id: int,
) -> list[dict[str, object]]:
    """Trả metadata file có thứ tự, chỉ khi Mentor sở hữu course của submission."""

    if not submission_ids:
        return []
    # Giữ quyền owner và điều kiện UploadAsset ngay trong truy vấn file dùng chung.
    return query_many(
        db,
        FIND_MENTOR_SUBMISSION_UPLOADS,
        {"submission_ids": submission_ids, "mentor_id": mentor_id},
    )
