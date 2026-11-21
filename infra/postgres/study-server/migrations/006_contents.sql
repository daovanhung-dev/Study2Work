CREATE TABLE IF NOT EXISTS contents (
    id BIGSERIAL PRIMARY KEY,
    course_id BIGINT NOT NULL REFERENCES courses(id),
    content_type TEXT NOT NULL,
    title TEXT NOT NULL,
    payload JSONB NOT NULL CHECK (jsonb_typeof(payload) = 'object'),
    status TEXT NOT NULL,
    parent_id BIGINT NULL,
    content_order INTEGER NOT NULL,
    deleted_at TIMESTAMP NULL,
    UNIQUE (id, course_id),
    FOREIGN KEY (parent_id, course_id) REFERENCES contents(id, course_id)
);

CREATE INDEX IF NOT EXISTS idx_contents_course_tree
    ON contents(course_id, parent_id, content_order, id)
    WHERE deleted_at IS NULL;
