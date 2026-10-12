# PLAN_RESULT — Study API #30

## Kết quả

- Output: apps/study-server/docs/dd/30_attempts_answers/.
- API: PUT /api/v1/attempts/{attempt_id}/answers.
- DD status: Draft — Needs Confirmation.
- Scope: Source-backed API Detail Design only; no runtime, API catalog, diagram or DB schema changes.
- Package: No ZIP, according to .agents/server-study/workflows/README.md.

## Contract được giữ

Nguồn: docs/lists/list_api.md, API #30 row and reusable schemas.

- Actor/authentication: Student Bearer JWT.
- Input: path attempt_id:int64!; body question_id:int64! and answer(s):string!; no query parameters.
- Success: HTTP 200 DESIGN_RESOURCE_UPDATED, response ApiEnvelope<QuizAttempt>.
- Errors: 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 422 DESIGN_VALIDATION_ERROR; 500 DESIGN_INTERNAL_ERROR.
- No 409 is added because API #30 catalog does not list it.

## Evidence and limits

- AC-16 activity diagram places API #30 after Student answers a question and labels the action UPSERT AttemptAnswer; API #31 follows with submit and automatic grading.
- Candidate physical write target is quiz_answers; ERD/DDL do not define a unique upsert key for (attempt_id, question_id).
- API catalog body answer(s):string! does not resolve to logical QuizAnswer.choice_ids or text_answer.
- Checked-in quiz_answers has one choice_id, is_correct NOT NULL, and score_received DEFAULT 0; API #30 does not define choice conversion or correctness/score values before API #31.
- DB table notes and DDL differ on nullability of quiz-answer foreign keys; live schema is not verified.
- Current Study auth helper parses numeric user ID from JWT sub and checks Student role; API #30 itself is not wired to this helper.
- Current router/module/test scan finds no API #30 route, module, query or test: UNWIRED / NOT_FOUND.

## Sources reviewed

- docs/lists/list_api.md: API #30 row, ApiEnvelope, QuizAttempt, QuizAnswer, error codes.
- contracts/api-guidelines/README.md: envelope and error behavior.
- apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md.
- apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio, AC-16 page.
- apps/study-server/docs/diagrams/DB_UNICA_TABLES.md, quiz_attempts and quiz_answers sections.
- apps/study-server/docs/diagrams/DB_UNICA_ERD.drawio, attempt/answer/question/choice relations.
- infra/postgres/study-server/DB.sql, assessment DDL.
- apps/study-server/app/utils/auth.py; current Study auth helper.
- apps/study-server/app/api/v1.py, app/modules/, and tests/; current wiring scan.
- apps/study-server/docs/dd/29_quizzes_attempts/ and current docs worklogs; adjacent DD precedent.
- .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/; canonical 8-file Markdown template.
- .agents/server-study/workflows/README.md; no-ZIP Study DD policy.

## Tables

- Candidate read: quiz_attempts, quiz_questions; quiz_choices only if choice-based answer semantics are approved.
- Candidate write: quiz_answers.

## Open decisions

See OPEN_QUESTIONS.md for request answer schema, storage/grading compatibility, upsert key/concurrency, attempt ownership/state, response projection/disclosure, and message/trace details.

