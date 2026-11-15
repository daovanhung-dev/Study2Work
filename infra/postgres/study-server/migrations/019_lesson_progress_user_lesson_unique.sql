-- API #23: enforce one progress row per learner and lesson in the approved schema.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_namespace WHERE nspname = 'nguyen_anh_duc'
    ) THEN
        RAISE EXCEPTION 'Required schema nguyen_anh_duc does not exist';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM nguyen_anh_duc.lesson_progress
        WHERE user_id IS NOT NULL AND lesson_id IS NOT NULL
        GROUP BY user_id, lesson_id
        HAVING COUNT(*) > 1
    ) THEN
        RAISE EXCEPTION 'Duplicate lesson progress pairs exist in nguyen_anh_duc.lesson_progress';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conrelid = 'nguyen_anh_duc.lesson_progress'::regclass
          AND conname = 'uq_lesson_progress_user_lesson'
    ) THEN
        ALTER TABLE nguyen_anh_duc.lesson_progress
            ADD CONSTRAINT uq_lesson_progress_user_lesson
            UNIQUE (user_id, lesson_id);
    END IF;
END;
$$;
