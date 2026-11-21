"""Câu SQL tĩnh để kiểm tra course và đọc cây Content cho API #49."""

FIND_MENTOR_COURSE = """
SELECT
    id,
    mentor_id
FROM courses
WHERE id = :course_id
LIMIT 1
"""

LIST_COURSE_CONTENTS = """
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
WHERE course_id = :course_id
  AND deleted_at IS NULL
ORDER BY parent_id NULLS FIRST, content_order ASC, id ASC
"""
