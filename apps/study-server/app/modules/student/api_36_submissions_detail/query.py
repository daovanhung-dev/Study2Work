FIND_STUDENT_SUBMISSION = """
SELECT s.id, s.assignment_id, s.user_id, s.content, s.status, s.submitted_at,
       CASE WHEN UPPER(s.status) = 'GRADED' THEN s.score ELSE NULL END AS score,
       CASE WHEN UPPER(s.status) = 'GRADED' THEN s.feedback ELSE NULL END AS feedback
FROM assignment_submissions s
WHERE s.id = :submission_id AND s.user_id = :user_id
LIMIT 1
"""

FIND_STUDENT_SUBMISSION_UPLOADS = """
SELECT
    u.id,
    u.file_name AS name,
    u.url,
    u.content_type,
    u.size_bytes,
    u.status
FROM assignment_submission_uploads AS link
JOIN assignment_submissions AS s ON s.id = link.submission_id
JOIN assignments AS a ON a.id = s.assignment_id
JOIN uploads AS u ON u.id = link.upload_id
WHERE s.id = :submission_id
  AND s.user_id = :user_id
  AND u.owner_id = s.user_id
  AND u.purpose = 'SUBMISSION'
  AND u.course_id = a.course_id
  AND u.status = 'UPLOADED'
ORDER BY link.asset_position, link.upload_id
"""
