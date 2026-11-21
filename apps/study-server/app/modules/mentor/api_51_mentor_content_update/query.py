"""Câu SQL tĩnh để lock, archive và cập nhật Content cho API #51."""

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

ARCHIVE_CONTENT_VERSION = """
INSERT INTO content_versions (
    content_id,
    version_no,
    course_id,
    content_type,
    title,
    payload,
    status,
    parent_id,
    content_order,
    archived_by
)
SELECT
    :content_id,
    COALESCE(MAX(version_no), 0) + 1,
    :course_id,
    :content_type,
    :title,
    CAST(:payload AS JSONB),
    :status,
    :parent_id,
    :content_order,
    :archived_by
FROM content_versions
WHERE content_id = :content_id
RETURNING version_no
"""

UPDATE_CONTENT = """
UPDATE contents
SET
    content_type = :content_type,
    title = :title,
    payload = CAST(:payload AS JSONB),
    status = 'PENDING_REVIEW'
WHERE id = :content_id
  AND deleted_at IS NULL
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
