"""Các SQL constant khóa và cập nhật một notification cùng delivery rows."""

LOCK_ADMIN_NOTIFICATION = """
SELECT n.id, n.title, n.content, n.created_at
FROM notifications AS n
WHERE n.id = :notification_id
FOR UPDATE OF n
"""

LOCK_ADMIN_NOTIFICATION_DELIVERIES = """
SELECT d.notification_id, d.channel, d.status
FROM notification_deliveries AS d
WHERE d.notification_id = :notification_id
ORDER BY d.channel ASC
FOR UPDATE OF d
"""

UPDATE_ADMIN_NOTIFICATION = """
UPDATE notifications
SET title = :title,
    content = :content
WHERE id = :notification_id
RETURNING id, title, content, created_at
"""
