"""Lưu SQL constant dùng cho mutation API #70."""

UPDATE_ADMIN_USER = """
UPDATE users
SET
    full_name = :full_name,
    phone = :phone,
    avatar_url = :avatar_url,
    role = :role,
    updated_at = CURRENT_TIMESTAMP
WHERE id = :user_id
RETURNING
    id,
    full_name,
    email,
    role,
    avatar_url,
    phone,
    status,
    created_at,
    updated_at
"""
