"""Câu SQL tĩnh khóa, phê duyệt Content và append review audit cho API #80."""

LOCK_ADMIN_CONTENT_FOR_APPROVAL = """
SELECT id, status
FROM contents
WHERE id = :content_id
  AND deleted_at IS NULL
FOR UPDATE
"""

APPROVE_ADMIN_CONTENT = """
UPDATE contents
SET status = 'APPROVED'
WHERE id = :content_id
  AND deleted_at IS NULL
  AND status = 'PENDING_REVIEW'
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

INSERT_ADMIN_CONTENT_REVIEW_AUDIT = """
INSERT INTO content_review_audit_logs (
    content_id,
    actor_user_id,
    previous_status,
    new_status,
    reason
)
VALUES (
    :content_id,
    :actor_user_id,
    :previous_status,
    :new_status,
    :reason
)
"""
