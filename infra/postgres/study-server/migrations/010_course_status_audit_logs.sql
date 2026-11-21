-- API #76 DERIVED fallback: persist legacy BIGINT course-status audit entries.
-- The AC-32 diagram requires status + audit; this candidate migration does not prove live deployment.
CREATE TABLE IF NOT EXISTS course_status_audit_logs (
    id BIGSERIAL PRIMARY KEY,
    course_id BIGINT NOT NULL REFERENCES courses(id) ON DELETE RESTRICT,
    actor_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    previous_status VARCHAR(20) NULL,
    new_status VARCHAR(20) NOT NULL,
    changed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_course_status_audit_logs_course_changed
    ON course_status_audit_logs(course_id, changed_at DESC, id DESC);

CREATE INDEX IF NOT EXISTS idx_course_status_audit_logs_actor_changed
    ON course_status_audit_logs(actor_user_id, changed_at DESC, id DESC);
