"""Câu SQL tĩnh để khóa Content và đổi publication status cho API #52."""

LOCK_MENTOR_CONTENT = """
SELECT
    content.id,
    content.course_id,
    course.mentor_id,
    content.content_type,
    content.title,
    content.payload,
    content.status,
    content.parent_id,
    content.content_order AS "order"
FROM contents AS content
JOIN courses AS course
    ON course.id = content.course_id
WHERE content.id = :content_id
  AND content.deleted_at IS NULL
LIMIT 1
FOR UPDATE OF content, course
"""

UPDATE_PUBLICATION_STATUS = """
UPDATE contents
SET status = :target_status
WHERE id = :content_id
  AND deleted_at IS NULL
  AND status = :expected_status
RETURNING
    id,
    course_id,
    content_type,
    title,
    payload,
    status,
    parent_id,
    content_order AS "order"
"""
