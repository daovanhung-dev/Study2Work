-- API #80 DERIVED fallback: append Admin decisions for legacy BIGINT Content rows.
-- AC-33 requires approval audit; this source artifact does not prove live deployment.
CREATE TABLE IF NOT EXISTS content_review_audit_logs (
    id BIGSERIAL PRIMARY KEY,
    content_id BIGINT NOT NULL REFERENCES contents(id) ON DELETE RESTRICT,
    actor_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    previous_status TEXT NOT NULL,
    new_status TEXT NOT NULL,
    reason TEXT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_content_review_audit_logs_content_recorded
    ON content_review_audit_logs(content_id, recorded_at DESC, id DESC);

CREATE INDEX IF NOT EXISTS idx_content_review_audit_logs_actor_recorded
    ON content_review_audit_logs(actor_user_id, recorded_at DESC, id DESC);
