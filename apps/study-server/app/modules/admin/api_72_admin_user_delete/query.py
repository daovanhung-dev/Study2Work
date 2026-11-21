"""Lưu SQL constant soft-delete user; view sở hữu bind parameters và transaction."""

SOFT_DELETE_ADMIN_USER = """
UPDATE users
SET
    status = 'DELETED',
    updated_at = CURRENT_TIMESTAMP
WHERE id = :user_id
  AND status IS DISTINCT FROM 'DELETED'
RETURNING
    id,
    updated_at AS deleted_at
"""
