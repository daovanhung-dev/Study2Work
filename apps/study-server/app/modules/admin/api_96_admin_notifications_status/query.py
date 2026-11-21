"""SQL constant đọc một notification cùng delivery aggregate."""

FIND_ADMIN_NOTIFICATION_STATUS = """
WITH delivery_summary AS (
    SELECT
        d.notification_id,
        ARRAY_AGG(d.channel ORDER BY d.channel) AS channels,
        COUNT(*)::BIGINT AS delivery_count,
        COUNT(*) FILTER (WHERE d.status = 'QUEUED')::BIGINT AS queued_count,
        COUNT(*) FILTER (WHERE d.status = 'SENT')::BIGINT AS sent_count,
        COUNT(*) FILTER (WHERE d.status = 'FAILED')::BIGINT AS failed_count
    FROM notification_deliveries AS d
    WHERE d.notification_id = :notification_id
    GROUP BY d.notification_id
)
SELECT
    n.id,
    n.title,
    n.content,
    ds.channels,
    CASE
        WHEN ds.queued_count > 0 THEN 'QUEUED'
        WHEN ds.failed_count > 0 THEN 'FAILED'
        WHEN ds.sent_count = ds.delivery_count THEN 'SENT'
        ELSE NULL
    END AS status,
    n.created_at
FROM notifications AS n
JOIN delivery_summary AS ds ON ds.notification_id = n.id
WHERE n.id = :notification_id
LIMIT 1
"""
