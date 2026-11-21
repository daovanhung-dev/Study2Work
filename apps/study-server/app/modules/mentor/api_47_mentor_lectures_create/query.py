"""Câu SQL tĩnh dùng để kiểm tra course, resolve assets và tạo lecture API #47."""

FIND_LECTURE_COURSE = """
SELECT id, mentor_id
FROM courses
WHERE id = :course_id
LIMIT 1
"""

FIND_LECTURE_ASSETS = """
SELECT id, file_name AS name, url, content_type, size_bytes, status
FROM uploads
WHERE id = ANY(CAST(:asset_ids AS BIGINT[]))
  AND owner_id = :mentor_id
  AND purpose = 'LECTURE'
  AND course_id = :course_id
"""

INSERT_LECTURE = """
INSERT INTO lessons (
    course_id,
    name,
    content,
    sort_order,
    status,
    created_at,
    updated_at
)
VALUES (
    :course_id,
    :title,
    :content,
    :order,
    'PUBLISHED',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
RETURNING id, course_id, name, content, sort_order, status
"""

INSERT_LECTURE_ASSET_LINKS = """
INSERT INTO lesson_uploads (lesson_id, upload_id, asset_position)
SELECT :lecture_id, requested.upload_id, requested.ordinality - 1
FROM UNNEST(CAST(:asset_ids AS BIGINT[])) WITH ORDINALITY
    AS requested(upload_id, ordinality)
RETURNING upload_id
"""
