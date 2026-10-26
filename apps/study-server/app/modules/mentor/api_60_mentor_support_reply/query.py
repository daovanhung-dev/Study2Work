"""Câu SQL tĩnh lock request, resolve uploads và lưu reply API #60."""

LOCK_MENTOR_SUPPORT_REQUEST_FOR_REPLY = """
SELECT
    request.id,
    request.course_id,
    course.id AS parent_course_id,
    course.mentor_id,
    request.student_id,
    request.status,
    request.created_at,
    request.resolved_at,
    student.id AS student_user_id,
    student.full_name AS student_full_name,
    student.avatar_url AS student_avatar_url
FROM support_requests AS request
LEFT JOIN courses AS course ON course.id = request.course_id
LEFT JOIN users AS student ON student.id = request.student_id
WHERE request.id = :request_id
LIMIT 1
FOR UPDATE OF request
"""

FIND_REPLY_UPLOADS = """
SELECT
    upload.id,
    upload.file_name AS name,
    upload.url,
    upload.content_type,
    upload.size_bytes,
    upload.status
FROM uploads AS upload
WHERE upload.id = ANY(CAST(:asset_ids AS BIGINT[]))
  AND upload.owner_id = :mentor_id
  AND upload.course_id = :course_id
  AND upload.purpose = 'LECTURE'
  AND upload.status = 'UPLOADED'
"""

INSERT_MENTOR_SUPPORT_MESSAGE = """
INSERT INTO support_messages (request_id, author_id, content)
SELECT request.id, :mentor_id, :message
FROM support_requests AS request
JOIN courses AS course ON course.id = request.course_id
WHERE request.id = :request_id
  AND course.mentor_id = :mentor_id
RETURNING id, request_id, author_id, content, created_at
"""

INSERT_MENTOR_SUPPORT_MESSAGE_UPLOADS = """
INSERT INTO support_message_uploads (message_id, upload_id, asset_position)
SELECT :message_id, requested.upload_id, requested.ordinality - 1
FROM UNNEST(CAST(:asset_ids AS BIGINT[])) WITH ORDINALITY
    AS requested(upload_id, ordinality)
RETURNING upload_id, asset_position
"""
