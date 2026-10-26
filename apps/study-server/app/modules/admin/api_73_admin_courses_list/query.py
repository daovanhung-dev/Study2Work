"""Câu SQL tĩnh đếm và đọc trang khóa học cho API #73."""

COUNT_ADMIN_COURSES = """
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE m.id IS NULL) AS missing_mentor_count
FROM courses AS c
LEFT JOIN users AS m ON m.id = c.mentor_id
WHERE (:status IS NULL OR c.status = :status)
  AND (:mentor IS NULL OR c.mentor_id = :mentor)
"""

LIST_ADMIN_COURSES = """
SELECT
    c.id,
    c.name AS title,
    c.description,
    c.thumbnail_url,
    c.price,
    c.status,
    m.id AS mentor_id,
    m.full_name AS mentor_full_name,
    m.avatar_url AS mentor_avatar_url
FROM courses AS c
LEFT JOIN users AS m ON m.id = c.mentor_id
WHERE (:status IS NULL OR c.status = :status)
  AND (:mentor IS NULL OR c.mentor_id = :mentor)
ORDER BY c.id ASC
LIMIT :limit OFFSET :offset
"""
