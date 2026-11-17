FIND_NOTIFICATION_OPERATION = """
SELECT
    n.operation_id AS id,
    n.sender_id AS owner_id,
    MIN(n.created_at) AS submitted_at,
    MAX(COALESCE(d.updated_at, n.created_at)) AS updated_at,
    CASE
        WHEN COUNT(d.id) = 0 OR COUNT(d.id) FILTER (WHERE d.status = 'QUEUED') > 0 THEN 'QUEUED'
        WHEN COUNT(d.id) FILTER (WHERE d.status = 'FAILED') > 0 THEN 'FAILED'
        ELSE 'SENT'
    END AS status,
    CASE
        WHEN COUNT(d.id) > 0 AND COUNT(d.id) FILTER (WHERE d.status = 'QUEUED') = 0
        THEN MAX(COALESCE(d.updated_at, n.created_at))
        ELSE NULL
    END AS completed_at
FROM notifications AS n
LEFT JOIN notification_deliveries AS d ON d.notification_id = n.id
WHERE n.operation_id = :operation_id
  AND n.sender_id = :owner_id
GROUP BY n.operation_id, n.sender_id
LIMIT 1
"""
