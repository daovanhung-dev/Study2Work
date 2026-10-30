LIST_MENTOR_COURSES = """
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
WHERE c.mentor_id = :mentor_id
ORDER BY c.created_at DESC, c.id ASC
LIMIT :limit OFFSET :offset
"""

LIST_MENTOR_COURSES_BY_STATUS = """
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
WHERE c.mentor_id = :mentor_id
  AND c.status = :status
ORDER BY c.created_at DESC, c.id ASC
LIMIT :limit OFFSET :offset
"""

COUNT_MENTOR_COURSES = """
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE m.id IS NULL) AS missing_mentor_count
FROM courses AS c
LEFT JOIN users AS m ON m.id = c.mentor_id
WHERE c.mentor_id = :mentor_id
"""

COUNT_MENTOR_COURSES_BY_STATUS = """
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE m.id IS NULL) AS missing_mentor_count
FROM courses AS c
LEFT JOIN users AS m ON m.id = c.mentor_id
WHERE c.mentor_id = :mentor_id
  AND c.status = :status
"""
