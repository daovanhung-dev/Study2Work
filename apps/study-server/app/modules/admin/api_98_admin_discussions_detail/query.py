"""Các câu SQL tĩnh đọc Discussion đích và comment trực tiếp cho API #98."""

FIND_ADMIN_DISCUSSION_DETAIL = """
SELECT
    d.id,
    d.course_id,
    d.content,
    d.status,
    u.id AS author_id,
    u.full_name AS author_full_name,
    u.avatar_url AS author_avatar_url
FROM discussions AS d
LEFT JOIN users AS u ON u.id = d.user_id
WHERE d.id = :discussion_id
"""

LIST_ADMIN_DISCUSSION_DETAIL_COMMENTS = """
SELECT
    child.id,
    child.parent_id AS discussion_id,
    child.content,
    child.created_at,
    u.id AS author_id,
    u.full_name AS author_full_name,
    u.avatar_url AS author_avatar_url
FROM discussions AS child
LEFT JOIN users AS u ON u.id = child.user_id
WHERE child.parent_id = :discussion_id
ORDER BY child.created_at ASC, child.id ASC
"""
