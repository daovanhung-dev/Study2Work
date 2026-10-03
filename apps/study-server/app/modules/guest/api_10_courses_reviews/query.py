GET_PUBLISHED_COURSE = """
SELECT
    c.id,
    c.status
FROM courses AS c
WHERE c.id = :course_id
  AND c.status = 'PUBLISHED'
"""


LIST_COURSE_REVIEWS = """
SELECT
    d.id,
    d.course_id,
    d.user_id,
    d.content,
    d.status,
    d.created_at,
    u.id AS author_id,
    u.full_name AS author_full_name,
    u.avatar_url AS author_avatar_url
FROM discussions AS d
INNER JOIN users AS u ON u.id = d.user_id
WHERE d.course_id = :course_id
  AND d.parent_id IS NULL
  AND d.status = 'ACTIVE'
ORDER BY d.created_at DESC, d.id DESC
LIMIT :limit OFFSET :offset
"""

LIST_REVIEW_REPLIES = """
SELECT
    r.id,
    r.parent_id,
    r.user_id,
    r.content,
    r.created_at,
    cu.id AS author_id,
    cu.full_name AS author_full_name,
    cu.avatar_url AS author_avatar_url
FROM discussions AS r
INNER JOIN users AS cu ON cu.id = r.user_id
WHERE r.parent_id IN ({review_id_placeholders})
  AND r.status = 'ACTIVE'
"""


COUNT_COURSE_REVIEWS = """
SELECT
    COUNT(*) AS total
FROM discussions AS d
WHERE d.course_id = :course_id
  AND d.parent_id IS NULL
  AND d.status = 'ACTIVE'
"""