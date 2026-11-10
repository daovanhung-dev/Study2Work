"""Câu SQL tĩnh đếm và đọc trang Content chờ Admin review API #78."""

COUNT_ADMIN_PENDING_CONTENTS = """
SELECT COUNT(*) AS total
FROM contents
WHERE status = 'PENDING_REVIEW'
  AND deleted_at IS NULL
  AND (CAST(:content_type AS TEXT) IS NULL OR content_type = CAST(:content_type AS TEXT))
  AND (CAST(:course_id AS BIGINT) IS NULL OR course_id = CAST(:course_id AS BIGINT))
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
  AND (CAST(:content_type AS TEXT) IS NULL OR content_type = CAST(:content_type AS TEXT))
  AND (CAST(:course_id AS BIGINT) IS NULL OR course_id = CAST(:course_id AS BIGINT))
ORDER BY id ASC
LIMIT :limit OFFSET :offset
"""
