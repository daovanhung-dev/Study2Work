"""Câu SQL tĩnh đếm và đọc trang user an toàn cho API #68."""

COUNT_ADMIN_USERS = """
SELECT COUNT(*) AS total
FROM users AS u
WHERE (CAST(:role AS VARCHAR) IS NULL OR u.role = CAST(:role AS VARCHAR))
  AND (CAST(:status AS VARCHAR) IS NULL OR u.status = CAST(:status AS VARCHAR))
  AND (
      CAST(:keyword AS TEXT) IS NULL
      OR POSITION(CAST(:keyword AS TEXT) IN LOWER(u.full_name)) > 0
      OR POSITION(CAST(:keyword AS TEXT) IN LOWER(u.email)) > 0
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
WHERE (CAST(:role AS VARCHAR) IS NULL OR u.role = CAST(:role AS VARCHAR))
  AND (CAST(:status AS VARCHAR) IS NULL OR u.status = CAST(:status AS VARCHAR))
  AND (
      CAST(:keyword AS TEXT) IS NULL
      OR POSITION(CAST(:keyword AS TEXT) IN LOWER(u.full_name)) > 0
      OR POSITION(CAST(:keyword AS TEXT) IN LOWER(u.email)) > 0
  )
ORDER BY u.id ASC
LIMIT :limit OFFSET :offset
"""
