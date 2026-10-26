"""Câu SQL tĩnh đọc Submission, course scope và UploadAsset cho API #55."""

FIND_MENTOR_SUBMISSION = """
SELECT
    s.id,
    s.assignment_id,
    s.user_id,
    s.content,
    s.status,
    s.submitted_at,
    s.score,
    s.feedback,
    a.id AS matched_assignment_id,
    a.course_id,
    c.id AS matched_course_id,
    c.mentor_id,
    asset.id AS file_id,
    asset.name AS file_name,
    asset.url AS file_url,
    asset.content_type AS file_content_type,
    asset.size_bytes AS file_size_bytes,
    asset.status AS file_status
FROM assignment_submissions AS s
LEFT JOIN assignments AS a ON a.id = s.assignment_id
LEFT JOIN courses AS c ON c.id = a.course_id
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
WHERE s.id = :submission_id
LIMIT 1
"""
