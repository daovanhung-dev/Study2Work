"""Câu SQL tĩnh lock, grade và resolve UploadAsset cho API #56."""

LOCK_MENTOR_SUBMISSION_FOR_GRADE = """
SELECT
    s.id,
    s.assignment_id,
    s.user_id,
    s.content,
    s.file_url,
    s.submitted_at,
    s.score,
    s.feedback,
    s.status,
    a.id AS matched_assignment_id,
    a.course_id,
    a.max_score,
    c.id AS matched_course_id,
    c.mentor_id
FROM assignment_submissions AS s
LEFT JOIN assignments AS a ON a.id = s.assignment_id
LEFT JOIN courses AS c ON c.id = a.course_id
WHERE s.id = :submission_id
LIMIT 1
FOR UPDATE OF s
"""

UPDATE_MENTOR_SUBMISSION_GRADE = """
UPDATE assignment_submissions AS s
SET
    score = CAST(:score AS NUMERIC(6,2)),
    status = 'GRADED'
WHERE s.id = :submission_id
  AND s.assignment_id = :assignment_id
  AND EXISTS (
      SELECT 1
      FROM assignments AS a
      JOIN courses AS c ON c.id = a.course_id
      WHERE a.id = s.assignment_id
        AND c.mentor_id = :mentor_id
  )
RETURNING
    s.id,
    s.assignment_id,
    s.user_id,
    s.content,
    s.file_url,
    s.submitted_at,
    s.score,
    s.feedback,
    s.status
"""

FIND_GRADED_SUBMISSION_UPLOAD = """
SELECT
    u.id,
    u.file_name AS name,
    u.url,
    u.content_type,
    u.size_bytes,
    u.status
FROM uploads AS u
WHERE u.url = :file_url
  AND u.owner_id = :user_id
  AND u.purpose = 'SUBMISSION'
  AND u.course_id = :course_id
ORDER BY u.id ASC
LIMIT 1
"""
