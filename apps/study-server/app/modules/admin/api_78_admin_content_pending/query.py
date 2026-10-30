"""Câu SQL tĩnh đếm và đọc trang Content chờ Admin review API #78."""

COUNT_ADMIN_PENDING_CONTENTS = """
SELECT COUNT(*) AS total
FROM contents
WHERE status = 'PENDING_REVIEW'
  AND deleted_at IS NULL
  AND (:content_type IS NULL OR content_type = :content_type)
  AND (:course_id IS NULL OR course_id = :course_id)
"""

LIST_ADMIN_PENDING_CONTENTS = """
SELECT
    id,
    course_id,
    content_type,
    title,
    payload,
    status,
    parent_id,
    content_order AS "order"
FROM contents
WHERE status = 'PENDING_REVIEW'
  AND deleted_at IS NULL
  AND (:content_type IS NULL OR content_type = :content_type)
  AND (:course_id IS NULL OR course_id = :course_id)
ORDER BY id ASC
LIMIT :limit OFFSET :offset
"""
