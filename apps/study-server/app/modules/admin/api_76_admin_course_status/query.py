"""Câu SQL tĩnh khóa/cập nhật status và ghi audit candidate cho API #76."""

LOCK_ADMIN_COURSE_STATUS = """
SELECT status
FROM courses
WHERE id = :course_id
FOR UPDATE
"""

UPDATE_ADMIN_COURSE_STATUS = """
UPDATE courses
SET
    status = :status,
    updated_at = CURRENT_TIMESTAMP
WHERE id = :course_id
RETURNING id, status
"""

INSERT_ADMIN_COURSE_STATUS_AUDIT = """
INSERT INTO course_status_audit_logs (
    course_id,
    actor_user_id,
    previous_status,
    new_status
)
VALUES (
    :course_id,
    :actor_user_id,
    :previous_status,
    :new_status
)
"""
