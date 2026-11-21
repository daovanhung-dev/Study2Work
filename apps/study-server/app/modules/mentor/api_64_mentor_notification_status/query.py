"""Các SQL constant đọc notification và aggregate delivery outbox cho API #64."""

FIND_NOTIFICATION_STATUS = """
SELECT
    n.id AS notification_id,
    n.operation_id,
    n.sender_id,
    n.created_at AS submitted_at,
    COUNT(d.id)::BIGINT AS delivery_count,
    COUNT(d.id) FILTER (WHERE d.status = 'QUEUED')::BIGINT AS queued_count,
    COUNT(d.id) FILTER (WHERE d.status = 'SENT')::BIGINT AS sent_count,
    COUNT(d.id) FILTER (WHERE d.status = 'FAILED')::BIGINT AS failed_count,
    MAX(d.updated_at) AS updated_at
FROM notifications AS n
LEFT JOIN notification_deliveries AS d
    ON d.notification_id = n.id
WHERE n.id = :notification_id
GROUP BY n.id, n.operation_id, n.sender_id, n.created_at
LIMIT 1
"""
