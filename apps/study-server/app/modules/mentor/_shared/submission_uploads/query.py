"""Câu SQL tĩnh đọc UploadAsset thuộc submission trong phạm vi Mentor."""

FIND_MENTOR_SUBMISSION_UPLOADS = """
SELECT
    s.id AS submission_id,
    u.id AS file_id,
    u.file_name AS file_name,
    u.url AS file_url,
    u.content_type AS file_content_type,
    u.size_bytes AS file_size_bytes,
    u.status AS file_status
FROM assignment_submission_uploads AS link
JOIN assignment_submissions AS s ON s.id = link.submission_id
JOIN assignments AS a ON a.id = s.assignment_id
JOIN courses AS c ON c.id = a.course_id
JOIN uploads AS u ON u.id = link.upload_id
WHERE s.id = ANY(CAST(:submission_ids AS BIGINT[]))
  AND c.mentor_id = :mentor_id
  AND u.owner_id = s.user_id
  AND u.purpose = 'SUBMISSION'
  AND u.course_id = a.course_id
  AND u.status = 'UPLOADED'
ORDER BY s.id, link.asset_position, link.upload_id
"""
