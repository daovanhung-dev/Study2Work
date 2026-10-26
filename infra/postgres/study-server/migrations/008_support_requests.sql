-- API #58 fallback: numeric Study identities and course ownership.
-- Source artifact only; applying this migration to a live database is a separate operation.

CREATE TABLE IF NOT EXISTS support_requests (
    id BIGSERIAL PRIMARY KEY,
    course_id BIGINT NOT NULL REFERENCES courses(id) ON DELETE RESTRICT,
    student_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status VARCHAR(24) NOT NULL DEFAULT 'OPEN'
        CHECK (status IN ('OPEN', 'IN_PROGRESS', 'WAITING_LEARNER', 'RESOLVED', 'CANCELLED')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMPTZ NULL
);

CREATE INDEX IF NOT EXISTS idx_support_requests_course_status_created
    ON support_requests(course_id, status, created_at DESC, id DESC);

CREATE TABLE IF NOT EXISTS support_messages (
    id BIGSERIAL PRIMARY KEY,
    request_id BIGINT NOT NULL REFERENCES support_requests(id) ON DELETE RESTRICT,
    author_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_support_messages_request_created
    ON support_messages(request_id, created_at, id);

CREATE TABLE IF NOT EXISTS support_message_uploads (
    message_id BIGINT NOT NULL REFERENCES support_messages(id) ON DELETE RESTRICT,
    upload_id BIGINT NOT NULL REFERENCES uploads(id) ON DELETE RESTRICT,
    asset_position BIGINT NOT NULL CHECK (asset_position >= 0),
    PRIMARY KEY (message_id, upload_id),
    UNIQUE (message_id, asset_position)
);

CREATE INDEX IF NOT EXISTS idx_support_message_uploads_message_position
    ON support_message_uploads(message_id, asset_position);
