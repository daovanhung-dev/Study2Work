COUNT_USER_NOTIFICATIONS = """
SELECT COUNT(*) AS total
FROM notifications n
LEFT JOIN notification_recipients r ON r.notification_id = n.id AND r.user_id = :user_id
WHERE (n.user_id = :user_id OR r.user_id = :user_id)
  AND (NOT :unread_only OR COALESCE(r.is_read, n.is_read, FALSE) = FALSE)
"""

LIST_USER_NOTIFICATIONS = """
SELECT n.id, n.title, n.content, n.type,
       COALESCE(r.is_read, n.is_read, FALSE) AS is_read,
       r.read_at, n.created_at
FROM notifications n
LEFT JOIN notification_recipients r ON r.notification_id = n.id AND r.user_id = :user_id
WHERE (n.user_id = :user_id OR r.user_id = :user_id)
  AND (NOT :unread_only OR COALESCE(r.is_read, n.is_read, FALSE) = FALSE)
ORDER BY n.created_at DESC, n.id DESC
LIMIT :limit OFFSET :offset
"""
