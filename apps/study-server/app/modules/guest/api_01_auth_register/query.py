CHECK_DUPLICATE = "SELECT id FROM users WHERE email = :email"
INSERT_USER = """
INSERT INTO users (
    full_name,
    email,
    password_hash,
    role,
    avatar_url,
    phone,
    created_at,
    updated_at
)
VALUES (
    :full_name,
    :email,
    :password_hash,
    'STUDENT',
    NULL,
    NULL,
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
