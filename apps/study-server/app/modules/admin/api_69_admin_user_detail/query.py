"""Câu SQL tĩnh đọc safe profile của một user cho API #69."""

FIND_ADMIN_USER = """
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
