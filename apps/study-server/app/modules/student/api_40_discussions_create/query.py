FIND_ACTIVE_ENROLLMENT = """
SELECT id FROM enrollments
WHERE user_id = :user_id AND course_id = :course_id AND status = 'ACTIVE'
LIMIT 1
"""

INSERT_ROOT_DISCUSSION = """
INSERT INTO discussions (course_id, user_id, parent_id, title, content, status, created_at, updated_at)
VALUES (:course_id, :user_id, NULL, :title, :content, 'ACTIVE', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
RETURNING id, course_id, title, content, status, created_at
"""

FIND_DISCUSSION_AUTHOR = """
SELECT id AS author_id, full_name AS author_full_name, avatar_url AS author_avatar_url
FROM users WHERE id = :user_id
LIMIT 1
"""
