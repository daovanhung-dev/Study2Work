"""Câu SQL tĩnh kiểm tra quyền course và đọc SupportRequest/thread cho API #58."""

FIND_MENTOR_COURSE = """
SELECT
    id,
    mentor_id
FROM courses
WHERE id = :course_id
LIMIT 1
"""

LIST_MENTOR_SUPPORT_REQUESTS = """
SELECT
    request.id,
    request.course_id,
    request.student_id,
    request.status,
    request.created_at,
    request.resolved_at,
    student.id AS student_user_id,
    student.full_name AS student_full_name,
    student.avatar_url AS student_avatar_url
FROM support_requests AS request
JOIN courses AS course ON course.id = request.course_id
JOIN users AS student ON student.id = request.student_id
WHERE course.mentor_id = :mentor_id
  AND (:course_id IS NULL OR request.course_id = :course_id)
  AND (:status IS NULL OR request.status = :status)
ORDER BY request.created_at DESC, request.id DESC
"""

LIST_MENTOR_SUPPORT_MESSAGES = """
SELECT
    request.id AS request_id,
    request.course_id,
    message.id AS message_id,
    message.author_id,
    author.id AS author_user_id,
    author.role AS author_role,
    author.full_name AS author_full_name,
    author.avatar_url AS author_avatar_url,
    message.content,
    message.created_at AS message_created_at,
    message_upload.upload_id AS linked_upload_id,
    upload.id AS attachment_id,
    upload.file_name AS attachment_name,
    upload.url AS attachment_url,
    upload.content_type AS attachment_content_type,
    upload.size_bytes AS attachment_size_bytes,
    upload.status AS attachment_status
FROM support_requests AS request
JOIN courses AS course ON course.id = request.course_id
LEFT JOIN support_messages AS message ON message.request_id = request.id
LEFT JOIN users AS author ON author.id = message.author_id
LEFT JOIN support_message_uploads AS message_upload ON message_upload.message_id = message.id
LEFT JOIN uploads AS upload
    ON upload.id = message_upload.upload_id
   AND upload.owner_id = message.author_id
   AND upload.course_id = request.course_id
   AND upload.purpose = CASE author.role
       WHEN 'STUDENT' THEN 'SUBMISSION'
       WHEN 'MENTOR' THEN 'LECTURE'
       ELSE NULL
   END
   AND upload.status = 'UPLOADED'
WHERE course.mentor_id = :mentor_id
  AND (:course_id IS NULL OR request.course_id = :course_id)
  AND (:status IS NULL OR request.status = :status)
ORDER BY
    request.created_at DESC,
    request.id DESC,
    message.created_at ASC NULLS FIRST,
    message.id ASC NULLS FIRST,
    message_upload.asset_position ASC NULLS FIRST
"""
