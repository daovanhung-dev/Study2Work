FIND_STUDENT_SUBMISSION = """
SELECT s.id, s.assignment_id, s.user_id, s.content, s.status, s.submitted_at,
       CASE WHEN UPPER(s.status) = 'GRADED' THEN s.score ELSE NULL END AS score,
       CASE WHEN UPPER(s.status) = 'GRADED' THEN s.feedback ELSE NULL END AS feedback,
       u.id AS file_id, u.file_name AS file_name, u.url AS file_url,
       u.content_type AS file_content_type, u.size_bytes AS file_size_bytes,
       u.status AS file_status
FROM assignment_submissions s
LEFT JOIN assignments a ON a.id = s.assignment_id
LEFT JOIN uploads u ON u.url = s.file_url AND u.owner_id = s.user_id
  AND u.purpose = 'SUBMISSION' AND u.course_id = a.course_id
WHERE s.id = :submission_id AND s.user_id = :user_id
LIMIT 1
"""
