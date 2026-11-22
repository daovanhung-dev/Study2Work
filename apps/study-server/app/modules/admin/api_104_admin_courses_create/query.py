"""Câu SQL tĩnh xác thực Mentor và tạo projection khóa học cho API #104."""

SELECT_ACTIVE_ADMIN_COURSE_MENTOR = """
SELECT id
FROM users
WHERE id = :mentor_id
  AND role = 'MENTOR'
  AND status = 'ACTIVE'
FOR SHARE
"""

INSERT_ADMIN_COURSE = """
INSERT INTO courses (
    mentor_id,
    name,
    description,
    thumbnail_url,
    price,
    status,
    created_at,
    updated_at
)
VALUES (
    :mentor_id,
    :title,
    :description,
    :thumbnail_url,
    :price,
    'DRAFT',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
RETURNING id
"""

GET_CREATED_ADMIN_COURSE = """
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
JOIN users AS m ON m.id = c.mentor_id
WHERE c.id = :course_id
"""
