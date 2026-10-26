-- API #88 DERIVED fallback: preserve the logical QuizQuestion type and choice order
-- on the legacy BIGINT quiz model. This migration file does not prove deployment.
ALTER TABLE quiz_questions
    ADD COLUMN IF NOT EXISTS question_type VARCHAR(24);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conrelid = 'quiz_questions'::regclass
          AND conname = 'ck_quiz_questions_question_type'
    ) THEN
        ALTER TABLE quiz_questions
            ADD CONSTRAINT ck_quiz_questions_question_type
            CHECK (
                question_type IS NULL
                OR question_type IN ('SINGLE_CHOICE', 'MULTIPLE_CHOICE', 'TRUE_FALSE')
            );
    END IF;
END;
$$;

ALTER TABLE quiz_choices
    ADD COLUMN IF NOT EXISTS sort_order INT NOT NULL DEFAULT 0;
