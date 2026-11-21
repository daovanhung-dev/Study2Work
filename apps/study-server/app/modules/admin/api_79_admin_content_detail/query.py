"""Câu SQL tĩnh đọc projection Content hiện hành cho API #79."""

FIND_ADMIN_CONTENT = """
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
WHERE id = :content_id
  AND deleted_at IS NULL
LIMIT 1
"""
