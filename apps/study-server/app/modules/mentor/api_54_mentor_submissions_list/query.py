"""Câu SQL tĩnh kiểm tra quyền course và đọc Submission cho API #54."""

FIND_MENTOR_COURSE = """
SELECT
    id,
    mentor_id
FROM courses
WHERE id = :course_id
LIMIT 1
"""

COUNT_MENTOR_SUBMISSIONS = """
SELECT COUNT(*) AS total
FROM assignment_submissions AS s
JOIN assignments AS a ON a.id = s.assignment_id
JOIN courses AS c ON c.id = a.course_id
JOIN users AS student ON student.id = s.user_id
WHERE c.mentor_id = :mentor_id
  AND (:course_id IS NULL OR a.course_id = :course_id)
  AND (:status IS NULL OR s.status = :status)
"""

LIST_MENTOR_SUBMISSIONS = """
SELECT
    s.id,
    s.assignment_id,
    s.user_id,
    s.content,
    s.status,
    s.submitted_at,
    s.score,
    s.feedback,
    asset.id AS file_id,
    asset.name AS file_name,
    asset.url AS file_url,
    asset.content_type AS file_content_type,
    asset.size_bytes AS file_size_bytes,
    asset.status AS file_status
FROM assignment_submissions AS s
JOIN assignments AS a ON a.id = s.assignment_id
JOIN courses AS c ON c.id = a.course_id
JOIN users AS student ON student.id = s.user_id
LEFT JOIN LATERAL (
    SELECT
        u.id,
        u.file_name AS name,
        u.url,
        u.content_type,
        u.size_bytes,
        u.status
    FROM uploads AS u
    WHERE u.url = s.file_url
      AND u.owner_id = s.user_id
      AND u.purpose = 'SUBMISSION'
      AND u.course_id = a.course_id
    ORDER BY u.id ASC
    LIMIT 1
) AS asset ON TRUE
WHERE c.mentor_id = :mentor_id
  AND (:course_id IS NULL OR a.course_id = :course_id)
  AND (:status IS NULL OR s.status = :status)
ORDER BY s.submitted_at DESC, s.id DESC
LIMIT :limit OFFSET :offset
"""
