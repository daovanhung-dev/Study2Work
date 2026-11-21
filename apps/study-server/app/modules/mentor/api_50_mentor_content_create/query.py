"""Câu SQL tĩnh để kiểm tra quyền và tạo Content cho API #50."""

LOCK_MENTOR_COURSE = """
SELECT
    id,
    mentor_id
FROM courses
WHERE id = :course_id
LIMIT 1
FOR UPDATE
"""

NEXT_ROOT_CONTENT_ORDER = """
SELECT GREATEST(COALESCE(MAX(content_order::BIGINT) + 1, 0), 0) AS next_order
FROM contents
WHERE course_id = :course_id
  AND parent_id IS NULL
  AND deleted_at IS NULL
"""

INSERT_CONTENT = """
INSERT INTO contents (
    course_id,
    content_type,
    title,
    payload,
    status,
    parent_id,
    content_order
)
VALUES (
    :course_id,
    :content_type,
    :title,
    CAST(:payload AS JSONB),
    :status,
    NULL,
    :content_order
)
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
