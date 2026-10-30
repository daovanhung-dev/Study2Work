"""Các SQL constant đếm và đọc notification có delivery trong API #92."""

COUNT_ADMIN_NOTIFICATIONS = """
WITH delivery_summary AS (
    SELECT
        d.notification_id,
        ARRAY_AGG(d.channel ORDER BY d.channel) AS channels,
        COUNT(*)::BIGINT AS delivery_count,
        COUNT(*) FILTER (WHERE d.status = 'QUEUED')::BIGINT AS queued_count,
        COUNT(*) FILTER (WHERE d.status = 'SENT')::BIGINT AS sent_count,
        COUNT(*) FILTER (WHERE d.status = 'FAILED')::BIGINT AS failed_count
    FROM notification_deliveries AS d
    GROUP BY d.notification_id
),
notification_rows AS (
    SELECT
        n.id,
        n.title,
        n.content,
        n.created_at,
        ds.channels,
        CASE
            WHEN ds.queued_count > 0 THEN 'QUEUED'
            WHEN ds.failed_count > 0 THEN 'FAILED'
            WHEN ds.sent_count = ds.delivery_count THEN 'SENT'
            ELSE NULL
        END AS status
    FROM notifications AS n
    JOIN delivery_summary AS ds ON ds.notification_id = n.id
    WHERE ds.delivery_count > 0
)
SELECT COUNT(*)::BIGINT AS total
FROM notification_rows AS n
WHERE (:status IS NULL OR n.status = :status)
  AND (:channel IS NULL OR :channel = ANY(n.channels))
"""

LIST_ADMIN_NOTIFICATIONS = """
WITH delivery_summary AS (
    SELECT
        d.notification_id,
        ARRAY_AGG(d.channel ORDER BY d.channel) AS channels,
        COUNT(*)::BIGINT AS delivery_count,
        COUNT(*) FILTER (WHERE d.status = 'QUEUED')::BIGINT AS queued_count,
        COUNT(*) FILTER (WHERE d.status = 'SENT')::BIGINT AS sent_count,
        COUNT(*) FILTER (WHERE d.status = 'FAILED')::BIGINT AS failed_count
    FROM notification_deliveries AS d
    GROUP BY d.notification_id
),
notification_rows AS (
    SELECT
        n.id,
        n.title,
        n.content,
        n.created_at,
        ds.channels,
        CASE
            WHEN ds.queued_count > 0 THEN 'QUEUED'
            WHEN ds.failed_count > 0 THEN 'FAILED'
            WHEN ds.sent_count = ds.delivery_count THEN 'SENT'
            ELSE NULL
        END AS status
    FROM notifications AS n
    JOIN delivery_summary AS ds ON ds.notification_id = n.id
    WHERE ds.delivery_count > 0
)
SELECT n.id, n.title, n.content, n.channels, n.status, n.created_at
FROM notification_rows AS n
WHERE (:status IS NULL OR n.status = :status)
  AND (:channel IS NULL OR :channel = ANY(n.channels))
ORDER BY n.created_at DESC, n.id DESC
LIMIT :limit OFFSET :offset
"""
