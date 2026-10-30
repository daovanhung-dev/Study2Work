"""Các SQL constant khóa và xóa notification cho API #95."""

LOCK_ADMIN_NOTIFICATION_FOR_DELETE = """
SELECT n.id
FROM notifications AS n
WHERE n.id = :notification_id
FOR UPDATE OF n
"""

LOCK_ADMIN_NOTIFICATION_DELIVERIES_FOR_DELETE = """
SELECT d.notification_id, d.channel, d.status
FROM notification_deliveries AS d
WHERE d.notification_id = :notification_id
ORDER BY d.channel ASC
FOR UPDATE OF d
"""

DELETE_ADMIN_NOTIFICATION = """
DELETE FROM notifications
WHERE id = :notification_id
RETURNING id, CURRENT_TIMESTAMP AS deleted_at
"""
