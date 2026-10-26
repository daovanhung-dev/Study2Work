"""Câu SQL tĩnh đếm và đọc trang user an toàn cho API #68."""

COUNT_ADMIN_USERS = """
SELECT COUNT(*) AS total
FROM users AS u
WHERE (:role IS NULL OR u.role = :role)
  AND (:status IS NULL OR u.status = :status)
  AND (
      :keyword IS NULL
      OR POSITION(:keyword IN LOWER(u.full_name)) > 0
      OR POSITION(:keyword IN LOWER(u.email)) > 0
  )
"""

LIST_ADMIN_USERS = """
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
WHERE (:role IS NULL OR u.role = :role)
  AND (:status IS NULL OR u.status = :status)
  AND (
      :keyword IS NULL
      OR POSITION(:keyword IN LOWER(u.full_name)) > 0
      OR POSITION(:keyword IN LOWER(u.email)) > 0
  )
ORDER BY u.id ASC
LIMIT :limit OFFSET :offset
"""
