"""Hằng số truy vấn SQL cho API #21 lấy tiến độ tổng hợp."""

FIND_CURRENT_USER_PROFILE = """
SELECT
    u.id,
    u.full_name,
    u.email,
    u.role,
    u.avatar_url,
    u.phone,
    u.status,
    u.created_at,
    u.updated_at
FROM users AS u
WHERE u.id = :user_id
LIMIT 1
"""

