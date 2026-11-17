MARK_ALL_USER_NOTIFICATIONS_READ = """
INSERT INTO notification_recipients (notification_id, user_id, is_read, read_at)
SELECT n.id, :user_id, TRUE, CURRENT_TIMESTAMP
FROM notifications n
LEFT JOIN notification_recipients r ON r.notification_id = n.id AND r.user_id = :user_id
WHERE (n.user_id = :user_id OR r.user_id = :user_id)
  AND COALESCE(r.is_read, n.is_read, FALSE) = FALSE
ON CONFLICT (notification_id, user_id)
DO UPDATE SET is_read = TRUE, read_at = COALESCE(notification_recipients.read_at, CURRENT_TIMESTAMP)
WHERE notification_recipients.is_read = FALSE
RETURNING notification_id
"""
