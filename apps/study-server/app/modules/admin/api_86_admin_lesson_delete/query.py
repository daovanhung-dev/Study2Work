"""SQL constants khóa, kiểm tra liên kết và xóa mềm Lesson API #86."""

LOCK_ADMIN_LESSON_FOR_DELETE = """
SELECT id, status
FROM lessons
WHERE id = :lesson_id
  AND status IS DISTINCT FROM 'DELETED'
FOR UPDATE
"""

CHECK_ADMIN_LESSON_DELETE_DEPENDENCIES = """
SELECT
    EXISTS (
        SELECT 1
        FROM lesson_progress
        WHERE lesson_id = :lesson_id
    ) AS has_progress,
    EXISTS (
        SELECT 1
        FROM resources
        WHERE lesson_id = :lesson_id
    ) AS has_resources,
    EXISTS (
        SELECT 1
        FROM lesson_uploads
        WHERE lesson_id = :lesson_id
    ) AS has_uploads
"""

SOFT_DELETE_ADMIN_LESSON = """
UPDATE lessons
SET
    status = 'DELETED',
    updated_at = CURRENT_TIMESTAMP
WHERE id = :lesson_id
  AND status IS DISTINCT FROM 'DELETED'
RETURNING
    id,
    updated_at AS deleted_at
"""
