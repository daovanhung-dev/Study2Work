-- API #35 stores ordered submission attachments only in schema nguyen_anh_duc.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_namespace WHERE nspname = 'nguyen_anh_duc'
    ) THEN
        RAISE EXCEPTION 'Required schema nguyen_anh_duc does not exist';
    END IF;
END;
$$;

CREATE TABLE IF NOT EXISTS nguyen_anh_duc.assignment_submission_uploads (
    submission_id BIGINT NOT NULL
        REFERENCES nguyen_anh_duc.assignment_submissions(id) ON DELETE CASCADE,
    upload_id BIGINT NOT NULL
        REFERENCES nguyen_anh_duc.uploads(id) ON DELETE RESTRICT,
    asset_position BIGINT NOT NULL CHECK (asset_position >= 0),
    PRIMARY KEY (submission_id, upload_id),
    UNIQUE (submission_id, asset_position)
);

CREATE INDEX IF NOT EXISTS idx_assignment_submission_uploads_order
    ON nguyen_anh_duc.assignment_submission_uploads(submission_id, asset_position);

-- Preserve the existing single-file reference as the first ordered association.
INSERT INTO nguyen_anh_duc.assignment_submission_uploads (
    submission_id,
    upload_id,
    asset_position
)
SELECT DISTINCT ON (s.id)
    s.id,
    u.id,
    0
FROM nguyen_anh_duc.assignment_submissions AS s
JOIN nguyen_anh_duc.assignments AS a ON a.id = s.assignment_id
JOIN nguyen_anh_duc.uploads AS u
    ON u.url = s.file_url
   AND u.owner_id = s.user_id
   AND u.purpose = 'SUBMISSION'
   AND u.course_id = a.course_id
WHERE s.file_url IS NOT NULL
ORDER BY s.id, u.id
ON CONFLICT DO NOTHING;
