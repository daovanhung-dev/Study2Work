"""Câu SQL tĩnh để khóa, kiểm tra dependency và soft-delete Content cho API #53."""

LOCK_MENTOR_CONTENT = """
SELECT
    content.id,
    content.course_id,
    course.mentor_id,
    content.status
FROM contents AS content
JOIN courses AS course
    ON course.id = content.course_id
WHERE content.id = :content_id
  AND content.deleted_at IS NULL
LIMIT 1
FOR UPDATE OF content, course
"""

HAS_ACTIVE_CHILD_CONTENT = """
SELECT EXISTS (
    SELECT 1
    FROM contents AS child
    WHERE child.course_id = :course_id
      AND child.parent_id = :content_id
      AND child.deleted_at IS NULL
) AS has_active_child
"""

SOFT_DELETE_CONTENT = """
UPDATE contents
SET deleted_at = CURRENT_TIMESTAMP
WHERE id = :content_id
  AND course_id = :course_id
  AND deleted_at IS NULL
RETURNING id, deleted_at
"""
