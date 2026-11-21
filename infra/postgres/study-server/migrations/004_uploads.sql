CREATE TABLE IF NOT EXISTS uploads (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES users(id),
    purpose VARCHAR(20) NOT NULL CHECK (purpose IN ('SUBMISSION', 'LECTURE')),
    course_id BIGINT REFERENCES courses(id),
    storage_key TEXT NOT NULL UNIQUE,
    file_name TEXT NOT NULL,
    url TEXT NOT NULL,
    content_type TEXT NOT NULL,
    size_bytes BIGINT NOT NULL CHECK (size_bytes >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'UPLOADED' CHECK (status = 'UPLOADED')
);

CREATE INDEX IF NOT EXISTS idx_uploads_owner_purpose_course
    ON uploads(owner_id, purpose, course_id);
