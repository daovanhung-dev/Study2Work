-- API #97 DERIVED fallback: store moderation reports beside legacy BIGINT Discussions.
-- This source artifact does not prove live schema, report ingestion, or deployment.
CREATE TABLE IF NOT EXISTS discussion_reports (
    id BIGSERIAL PRIMARY KEY,
    discussion_id BIGINT NOT NULL
        REFERENCES discussions(id) ON DELETE RESTRICT,
    reporter_user_id BIGINT NOT NULL
        REFERENCES users(id) ON DELETE RESTRICT,
    reason_code VARCHAR(80) NOT NULL,
    severity VARCHAR(24) NOT NULL,
    status VARCHAR(24) NOT NULL DEFAULT 'OPEN'
        CHECK (status IN ('OPEN', 'IN_REVIEW', 'RESOLVED', 'DISMISSED')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_discussion_reports_queue_filter_created
    ON discussion_reports(status, reason_code, severity, created_at DESC, discussion_id);

CREATE INDEX IF NOT EXISTS idx_discussion_reports_discussion_status_created
    ON discussion_reports(discussion_id, status, created_at DESC, id DESC);
