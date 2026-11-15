FIND_ADDRESSABLE_NOTIFICATION = """
SELECT n.id FROM notifications n
LEFT JOIN notification_recipients r ON r.notification_id = n.id AND r.user_id = :user_id
WHERE n.id = :notification_id AND (n.user_id = :user_id OR r.user_id = :user_id)
FOR UPDATE OF n
"""

UPSERT_NOTIFICATION_READ = """
INSERT INTO notification_recipients (notification_id, user_id, is_read, read_at)
SELECT n.id, :user_id, TRUE,
       CASE WHEN COALESCE(r.is_read, n.is_read, FALSE) THEN r.read_at ELSE CURRENT_TIMESTAMP END
FROM notifications n
LEFT JOIN notification_recipients r ON r.notification_id = n.id AND r.user_id = :user_id
WHERE n.id = :notification_id AND (n.user_id = :user_id OR r.user_id = :user_id)
ON CONFLICT (notification_id, user_id)
DO UPDATE SET is_read = TRUE, read_at = COALESCE(notification_recipients.read_at, EXCLUDED.read_at)
RETURNING notification_id
"""

GET_READ_NOTIFICATION = """
SELECT n.id, n.title, n.content, n.type,
       COALESCE(r.is_read, n.is_read, FALSE) AS is_read, r.read_at, n.created_at
FROM notifications n
LEFT JOIN notification_recipients r ON r.notification_id = n.id AND r.user_id = :user_id
WHERE n.id = :notification_id AND (n.user_id = :user_id OR r.user_id = :user_id)
LIMIT 1
"""
