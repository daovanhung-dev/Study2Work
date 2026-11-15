FIND_ASSIGNMENT = """
SELECT a.id, a.course_id, a.due_at
FROM assignments a
WHERE a.id = :assignment_id
LIMIT 1
"""

FIND_ACTIVE_ENROLLMENT = """
SELECT id FROM enrollments
WHERE user_id = :user_id AND course_id = :course_id AND status = 'ACTIVE'
LIMIT 1
"""

FIND_SUBMISSION_UPLOAD = """
SELECT id, file_name AS name, url, content_type, size_bytes, status
FROM uploads
WHERE id = :upload_id AND owner_id = :user_id
  AND purpose = 'SUBMISSION' AND course_id = :course_id AND status = 'UPLOADED'
LIMIT 1
"""

INSERT_SUBMISSION = """
INSERT INTO assignment_submissions (
    assignment_id, user_id, content, file_url, submitted_at, status
)
VALUES (:assignment_id, :user_id, :content, :file_url, CURRENT_TIMESTAMP, 'SUBMITTED')
RETURNING id, assignment_id, user_id, content, status, submitted_at, score, feedback
"""
