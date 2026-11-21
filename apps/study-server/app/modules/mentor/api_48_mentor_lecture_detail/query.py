"""Câu SQL tĩnh để đọc lecture và UploadAsset liên kết cho API #48."""

FIND_MENTOR_LECTURE = """
SELECT
    l.id,
    l.course_id,
    l.name,
    l.content,
    l.sort_order,
    l.status,
    c.id AS parent_course_id,
    c.mentor_id
FROM lessons AS l
LEFT JOIN courses AS c ON c.id = l.course_id
WHERE l.id = :lecture_id
  AND l.status IS DISTINCT FROM 'DELETED'
LIMIT 1
"""

FIND_LECTURE_UPLOAD_ASSETS = """
SELECT
    lesson_uploads.upload_id,
    uploads.id,
    uploads.file_name AS name,
    uploads.url,
    uploads.content_type,
    uploads.size_bytes,
    uploads.status
FROM lesson_uploads
LEFT JOIN uploads
    ON uploads.id = lesson_uploads.upload_id
   AND uploads.owner_id = :mentor_id
   AND uploads.purpose = 'LECTURE'
   AND uploads.course_id = :course_id
WHERE lesson_uploads.lesson_id = :lecture_id
ORDER BY lesson_uploads.asset_position ASC, lesson_uploads.upload_id ASC
"""
