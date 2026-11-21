COUNT_ROOT_DISCUSSIONS = """
SELECT COUNT(*) AS total
FROM discussions d
WHERE d.parent_id IS NULL AND d.status = 'ACTIVE'
  AND (CAST(:course_id AS BIGINT) IS NULL OR d.course_id = CAST(:course_id AS BIGINT))
  AND EXISTS (SELECT 1 FROM enrollments e WHERE e.user_id = :user_id AND e.course_id = d.course_id AND e.status = 'ACTIVE')
"""

LIST_ROOT_DISCUSSIONS = """
SELECT d.id, d.course_id, d.title, d.content, d.status,
       u.id AS author_id, u.full_name AS author_full_name, u.avatar_url AS author_avatar_url
FROM discussions d
JOIN users u ON u.id = d.user_id
WHERE d.parent_id IS NULL AND d.status = 'ACTIVE'
  AND (CAST(:course_id AS BIGINT) IS NULL OR d.course_id = CAST(:course_id AS BIGINT))
  AND EXISTS (SELECT 1 FROM enrollments e WHERE e.user_id = :user_id AND e.course_id = d.course_id AND e.status = 'ACTIVE')
ORDER BY d.created_at DESC, d.id DESC
LIMIT :limit OFFSET :offset
"""

LIST_ACTIVE_COMMENTS = """
SELECT d.id, d.parent_id AS discussion_id, d.content, d.created_at,
       u.id AS author_id, u.full_name AS author_full_name, u.avatar_url AS author_avatar_url
FROM discussions d
JOIN users u ON u.id = d.user_id
WHERE d.parent_id = :discussion_id AND d.status = 'ACTIVE'
ORDER BY d.created_at ASC, d.id ASC
"""
