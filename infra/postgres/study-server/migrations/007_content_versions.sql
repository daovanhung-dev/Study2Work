CREATE TABLE IF NOT EXISTS content_versions (
    content_id BIGINT NOT NULL,
    version_no BIGINT NOT NULL CHECK (version_no > 0),
    course_id BIGINT NOT NULL,
    content_type TEXT NOT NULL,
    title TEXT NOT NULL,
    payload JSONB NOT NULL CHECK (jsonb_typeof(payload) = 'object'),
    status TEXT NOT NULL,
    parent_id BIGINT NULL,
    content_order INTEGER NOT NULL,
    archived_by BIGINT NOT NULL REFERENCES users(id),
    archived_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (content_id, version_no),
    FOREIGN KEY (content_id, course_id) REFERENCES contents(id, course_id),
    FOREIGN KEY (parent_id, course_id) REFERENCES contents(id, course_id)
);
