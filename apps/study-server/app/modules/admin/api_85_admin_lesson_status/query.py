"""Câu SQL tĩnh khóa/cập nhật Lesson và ghi status audit cho API #85."""

LOCK_ADMIN_LESSON_STATUS = """
SELECT
    id,
    course_id,
    name AS title,
    content,
    video_url,
    sort_order AS "order",
    status
FROM lessons
WHERE id = :lesson_id
  AND status IS DISTINCT FROM 'DELETED'
FOR UPDATE
"""

UPDATE_ADMIN_LESSON_STATUS = """
UPDATE lessons
SET
    status = :status,
    updated_at = CURRENT_TIMESTAMP
WHERE id = :lesson_id
  AND status IS DISTINCT FROM 'DELETED'
RETURNING
    id,
    course_id,
    name AS title,
    content,
    video_url,
    sort_order AS "order",
    status
"""

INSERT_ADMIN_LESSON_STATUS_AUDIT = """
INSERT INTO lesson_status_audit_logs (
    lesson_id,
    actor_user_id,
    previous_status,
    new_status
)
VALUES (
    :lesson_id,
    :actor_user_id,
    :previous_status,
    :new_status
)
"""
