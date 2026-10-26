"""Các SQL constant xác minh recipient scope và ghi notification delivery outbox."""

FIND_COMMON_MENTOR_COURSE_FOR_RECIPIENTS = """
SELECT
    c.id AS course_id,
    COUNT(DISTINCT u.id)::BIGINT AS matched_count
FROM courses AS c
JOIN enrollments AS e ON e.course_id = c.id
JOIN users AS u ON u.id = e.user_id
WHERE c.mentor_id = :mentor_id
  AND e.status = 'ACTIVE'
  AND u.role = 'STUDENT'
  AND u.id = ANY(:recipient_ids)
GROUP BY c.id
HAVING COUNT(DISTINCT u.id) = :recipient_count
ORDER BY c.id ASC
LIMIT 1
"""

INSERT_NOTIFICATION = """
INSERT INTO notifications (
    user_id,
    sender_id,
    title,
    content,
    type,
    is_read,
    created_at,
    operation_id
)
VALUES (
    :user_id,
    :sender_id,
    :title,
    :content,
    NULL,
    FALSE,
    CURRENT_TIMESTAMP,
    :operation_id
)
RETURNING id, created_at
"""

INSERT_NOTIFICATION_DELIVERY = """
INSERT INTO notification_deliveries (
    notification_id,
    channel,
    status,
    queued_at,
    updated_at
)
VALUES (
    :notification_id,
    :channel,
    'QUEUED',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
RETURNING id
"""
