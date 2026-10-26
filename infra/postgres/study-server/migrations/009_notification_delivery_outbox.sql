-- API #63 local fallback: UUID groups legacy BIGINT notification rows and
-- delivery rows form a durable queue for a future Push/Email worker.
-- Source artifact only; do not apply without validating the target live schema.

ALTER TABLE notifications
    ADD COLUMN IF NOT EXISTS operation_id UUID NULL;

CREATE INDEX IF NOT EXISTS idx_notifications_operation_id
    ON notifications(operation_id)
    WHERE operation_id IS NOT NULL;

CREATE TABLE IF NOT EXISTS notification_deliveries (
    id BIGSERIAL PRIMARY KEY,
    notification_id BIGINT NOT NULL
        REFERENCES notifications(id) ON DELETE CASCADE,
    channel VARCHAR(16) NOT NULL
        CHECK (channel IN ('PUSH', 'EMAIL')),
    status VARCHAR(16) NOT NULL DEFAULT 'QUEUED'
        CHECK (status IN ('QUEUED', 'SENT', 'FAILED')),
    queued_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (notification_id, channel)
);

CREATE INDEX IF NOT EXISTS idx_notification_deliveries_status_queued
    ON notification_deliveries(status, queued_at, id);
