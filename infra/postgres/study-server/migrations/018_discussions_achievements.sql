-- APIs #37-42: lesson awards projection and titled legacy discussions.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_namespace WHERE nspname = 'nguyen_anh_duc'
    ) THEN
        RAISE EXCEPTION 'Required schema nguyen_anh_duc does not exist';
    END IF;
END;
$$;

ALTER TABLE nguyen_anh_duc.discussions
    ADD COLUMN IF NOT EXISTS title TEXT NOT NULL DEFAULT '';

CREATE TABLE IF NOT EXISTS nguyen_anh_duc.user_achievements (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL
        REFERENCES nguyen_anh_duc.users(id) ON DELETE CASCADE,
    course_id BIGINT NULL
        REFERENCES nguyen_anh_duc.courses(id) ON DELETE SET NULL,
    achievement_code VARCHAR(80) NOT NULL,
    title VARCHAR(200) NOT NULL,
    awarded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_achievements_user_course_awarded
    ON nguyen_anh_duc.user_achievements(user_id, course_id, awarded_at DESC, id DESC);
