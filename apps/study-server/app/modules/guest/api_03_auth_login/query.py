"""SQL statements for auth login and refresh-token persistence."""

LOGIN_USER = """
SELECT
    id,
    full_name,
    email,
    password_hash,
    role,
    avatar_url,
    phone,
    status,
    created_at,
    updated_at
FROM users
WHERE email = :email
LIMIT 1
"""

REFRESH_SESSION = """
SELECT
    rt.id AS refresh_token_id,
    u.id,
    u.full_name,
    u.email,
    u.role,
    u.avatar_url,
    u.phone,
    u.status,
    u.created_at,
    u.updated_at
FROM refresh_tokens AS rt
JOIN users AS u ON u.id = rt.user_id
WHERE rt.token_hash = :token_hash
  AND rt.revoked_at IS NULL
  AND rt.expires_at > CURRENT_TIMESTAMP
LIMIT 1
"""

INSERT_REFRESH_TOKEN = """
INSERT INTO refresh_tokens (
    user_id,
    token_hash,
    expires_at,
    created_at
)
VALUES (
    :user_id,
    :token_hash,
    :expires_at,
    CURRENT_TIMESTAMP
)
RETURNING id
"""

REVOKE_REFRESH_TOKEN = """
UPDATE refresh_tokens
SET revoked_at = CURRENT_TIMESTAMP
WHERE id = :refresh_token_id
  AND revoked_at IS NULL
RETURNING id
"""
