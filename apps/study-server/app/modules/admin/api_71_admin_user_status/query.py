"""Lưu SQL constants cho API #71; view sở hữu bind parameters và transaction."""

LOCK_ADMIN_USER_STATUS = """
SELECT status
FROM users
WHERE id = :user_id
FOR UPDATE
"""

UPDATE_ADMIN_USER_STATUS = """
UPDATE users
SET
    status = :status,
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

REVOKE_ADMIN_USER_REFRESH_TOKENS = """
UPDATE refresh_tokens
SET revoked_at = CURRENT_TIMESTAMP
WHERE user_id = :user_id
  AND revoked_at IS NULL
  AND expires_at > CURRENT_TIMESTAMP
"""
