UPDATE_CURRENT_USER_PROFILE = """
UPDATE users
SET
    full_name = :full_name,
    phone = :phone,
    avatar_url = :avatar_url,
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
