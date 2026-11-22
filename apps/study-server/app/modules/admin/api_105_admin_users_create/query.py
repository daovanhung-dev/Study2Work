"""Câu SQL tĩnh kiểm tra email và tạo profile user cho API #105."""

CHECK_ADMIN_USER_EMAIL = """
SELECT id
FROM users
WHERE email = :email
"""

INSERT_ADMIN_USER = """
INSERT INTO users (
    full_name,
    email,
    password_hash,
    role,
    status,
    created_at,
    updated_at
)
VALUES (
    :full_name,
    :email,
    :password_hash,
    :role,
    'ACTIVE',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
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
