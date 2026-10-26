"""Câu SQL tĩnh được API #34 dùng cho quyền course và metadata upload."""

FIND_ACTIVE_STUDENT_ENROLLMENT = """
SELECT e.id
FROM enrollments AS e
WHERE e.user_id = :student_id
  AND e.course_id = :course_id
  AND e.status = 'ACTIVE'
LIMIT 1
"""

FIND_MENTOR_OWNED_COURSE = """
SELECT c.id
FROM courses AS c
WHERE c.id = :course_id
  AND c.mentor_id = :mentor_id
LIMIT 1
"""

INSERT_UPLOAD_ASSET = """
INSERT INTO uploads (
    owner_id,
    purpose,
    course_id,
    storage_key,
    file_name,
    url,
    content_type,
    size_bytes,
    status
)
VALUES (
    :owner_id,
    :purpose,
    :course_id,
    :storage_key,
    :file_name,
    :url,
    :content_type,
    :size_bytes,
    'UPLOADED'
)
RETURNING id
"""
