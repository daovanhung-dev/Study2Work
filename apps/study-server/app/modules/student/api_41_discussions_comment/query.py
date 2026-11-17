FIND_ROOT_FOR_COMMENT = """
SELECT d.id, d.course_id, d.title, d.content, d.status, d.user_id,
       u.full_name AS author_full_name, u.avatar_url AS author_avatar_url
FROM discussions d
JOIN users u ON u.id = d.user_id
WHERE d.id = :discussion_id AND d.parent_id IS NULL AND d.status = 'ACTIVE'
  AND EXISTS (SELECT 1 FROM enrollments e WHERE e.user_id = :user_id AND e.course_id = d.course_id AND e.status = 'ACTIVE')
FOR UPDATE
"""

INSERT_DISCUSSION_COMMENT = """
INSERT INTO discussions (course_id, user_id, parent_id, title, content, status, created_at, updated_at)
VALUES (:course_id, :user_id, :parent_id, '', :content, 'ACTIVE', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
RETURNING id
"""

FIND_DISCUSSION_AUTHOR = """
SELECT id AS author_id, full_name AS author_full_name, avatar_url AS author_avatar_url
FROM users WHERE id = :user_id
LIMIT 1
"""
