"""Các SQL constant kiểm tra recipients và ghi notification delivery outbox API #93."""

FIND_ADMIN_NOTIFICATION_RECIPIENTS = """
SELECT id
FROM users
WHERE id = ANY(:recipient_ids)
ORDER BY id ASC
"""

INSERT_ADMIN_NOTIFICATION = """
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

INSERT_ADMIN_NOTIFICATION_DELIVERY = """
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
