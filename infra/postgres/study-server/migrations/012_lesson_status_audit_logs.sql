-- API #85 DERIVED fallback: persist legacy BIGINT Lesson status changes.
-- AC-34 requires status + audit; this source artifact does not prove live deployment.
CREATE TABLE IF NOT EXISTS lesson_status_audit_logs (
    id BIGSERIAL PRIMARY KEY,
    lesson_id BIGINT NOT NULL REFERENCES lessons(id) ON DELETE RESTRICT,
    actor_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    previous_status VARCHAR(20) NULL,
    new_status VARCHAR(20) NOT NULL,
    changed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_lesson_status_audit_logs_lesson_changed
    ON lesson_status_audit_logs(lesson_id, changed_at DESC, id DESC);

CREATE INDEX IF NOT EXISTS idx_lesson_status_audit_logs_actor_changed
    ON lesson_status_audit_logs(actor_user_id, changed_at DESC, id DESC);
