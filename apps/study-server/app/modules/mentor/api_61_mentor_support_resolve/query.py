"""Câu SQL tĩnh khóa và resolve SupportRequest cho API #61."""

LOCK_MENTOR_SUPPORT_REQUEST_FOR_RESOLVE = """
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

UPDATE_MENTOR_SUPPORT_REQUEST_RESOLVED = """
UPDATE support_requests AS request
SET status = 'RESOLVED',
    resolved_at = COALESCE(request.resolved_at, CURRENT_TIMESTAMP)
FROM courses AS course
WHERE request.id = :request_id
  AND course.id = request.course_id
  AND course.mentor_id = :mentor_id
  AND request.status IN ('OPEN', 'IN_PROGRESS', 'WAITING_LEARNER')
RETURNING request.id, request.status, request.resolved_at
"""
