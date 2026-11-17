-- APIs #30-31: existing objective answer types from checked-in migration 013.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_namespace WHERE nspname = 'nguyen_anh_duc'
    ) THEN
        RAISE EXCEPTION 'Required schema nguyen_anh_duc does not exist';
    END IF;
END;
$$;

ALTER TABLE nguyen_anh_duc.quiz_questions
    ADD COLUMN IF NOT EXISTS question_type VARCHAR(24);

UPDATE nguyen_anh_duc.quiz_questions
SET question_type = 'SINGLE_CHOICE'
WHERE question_type IS NULL;

ALTER TABLE nguyen_anh_duc.quiz_questions
    ALTER COLUMN question_type SET DEFAULT 'SINGLE_CHOICE',
    ALTER COLUMN question_type SET NOT NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conrelid = 'nguyen_anh_duc.quiz_questions'::regclass
          AND conname = 'ck_quiz_questions_question_type'
    ) THEN
        ALTER TABLE nguyen_anh_duc.quiz_questions
            ADD CONSTRAINT ck_quiz_questions_question_type
            CHECK (question_type IN ('SINGLE_CHOICE', 'MULTIPLE_CHOICE', 'TRUE_FALSE'));
    END IF;
END;
$$;
