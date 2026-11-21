-- APIs #11, #12 and #26: fail closed for legacy resources and support private object signing.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_namespace WHERE nspname = 'nguyen_anh_duc'
    ) THEN
        RAISE EXCEPTION 'Required schema nguyen_anh_duc does not exist';
    END IF;
END;
$$;

ALTER TABLE nguyen_anh_duc.resources
    ADD COLUMN IF NOT EXISTS visibility VARCHAR(16) NOT NULL DEFAULT 'PRIVATE';

ALTER TABLE nguyen_anh_duc.resources
    ADD COLUMN IF NOT EXISTS storage_key TEXT NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conrelid = 'nguyen_anh_duc.resources'::regclass
          AND conname = 'chk_resources_visibility'
    ) THEN
        ALTER TABLE nguyen_anh_duc.resources
            ADD CONSTRAINT chk_resources_visibility
            CHECK (visibility IN ('PUBLIC', 'PRIVATE'));
    END IF;
END;
$$;
