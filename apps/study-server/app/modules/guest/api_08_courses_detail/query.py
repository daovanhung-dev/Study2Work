"""Các câu lệnh SQL cho API #8 chi tiết khóa học."""

FIND_PUBLISHED_COURSE_DETAIL = """
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
WHERE c.id = :course_id AND c.status = :status
"""
