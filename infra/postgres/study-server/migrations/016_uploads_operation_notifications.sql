-- APIs #18, #35, #43-45. Keep the legacy BIGINT Study IDs and current #63 outbox shape.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_namespace WHERE nspname = 'nguyen_anh_duc'
    ) THEN
        RAISE EXCEPTION 'Required schema nguyen_anh_duc does not exist';
    END IF;
END;
$$;

CREATE TABLE IF NOT EXISTS nguyen_anh_duc.uploads (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL
        REFERENCES nguyen_anh_duc.users(id) ON DELETE RESTRICT,
    purpose VARCHAR(20) NOT NULL CHECK (purpose IN ('SUBMISSION', 'LECTURE')),
    course_id BIGINT NULL
        REFERENCES nguyen_anh_duc.courses(id) ON DELETE RESTRICT,
    storage_key TEXT NOT NULL UNIQUE,
    file_name TEXT NOT NULL,
    url TEXT NOT NULL,
    content_type TEXT NOT NULL,
    size_bytes BIGINT NOT NULL CHECK (size_bytes >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'UPLOADED' CHECK (status = 'UPLOADED')
);

CREATE INDEX IF NOT EXISTS idx_uploads_owner_purpose_course
    ON nguyen_anh_duc.uploads(owner_id, purpose, course_id);

ALTER TABLE nguyen_anh_duc.notifications
    ADD COLUMN IF NOT EXISTS operation_id UUID NULL;

CREATE INDEX IF NOT EXISTS idx_notifications_operation_id
    ON nguyen_anh_duc.notifications(operation_id)
    WHERE operation_id IS NOT NULL;

CREATE TABLE IF NOT EXISTS nguyen_anh_duc.notification_deliveries (
    id BIGSERIAL PRIMARY KEY,
    notification_id BIGINT NOT NULL
        REFERENCES nguyen_anh_duc.notifications(id) ON DELETE CASCADE,
    channel VARCHAR(16) NOT NULL CHECK (channel IN ('PUSH', 'EMAIL')),
    status VARCHAR(16) NOT NULL DEFAULT 'QUEUED'
        CHECK (status IN ('QUEUED', 'SENT', 'FAILED')),
    queued_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (notification_id, channel)
);

CREATE INDEX IF NOT EXISTS idx_notification_deliveries_status_queued
    ON nguyen_anh_duc.notification_deliveries(status, queued_at, id);

CREATE TABLE IF NOT EXISTS nguyen_anh_duc.notification_recipients (
    notification_id BIGINT NOT NULL
        REFERENCES nguyen_anh_duc.notifications(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL
        REFERENCES nguyen_anh_duc.users(id) ON DELETE CASCADE,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    read_at TIMESTAMPTZ NULL,
    PRIMARY KEY (notification_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_notification_recipients_user_read
    ON nguyen_anh_duc.notification_recipients(user_id, is_read, notification_id);
