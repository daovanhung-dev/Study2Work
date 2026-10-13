# PLAN_RESULT — Study API #31

## Kết quả

- Output: apps/study-server/docs/dd/31_attempts_submit/
- API: POST /api/v1/attempts/{attempt_id}/submit.
- DD status: Draft — Needs Confirmation.
- Scope: Source-backed API Detail Design only; no runtime, API catalog, diagram or database schema changes.
- Package: No ZIP, according to .agents/server-study/workflows/README.md.
- Mapping sheets: quiz_attempts update and quiz_answers update are separate because the candidate mutations target two physical tables.

## Contract được giữ

Nguồn: docs/lists/list_api.md, API #31 row and reusable schemas.

- Actor/authentication: Student Bearer JWT.
- Input: required path attempt_id:int64!; no query parameter or request body is defined.
- Success: HTTP 200 DESIGN_RESOURCE_UPDATED, response ApiEnvelope<QuizAttempt>.
- Errors: 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 422 DESIGN_VALIDATION_ERROR; 409 DESIGN_STATE_CONFLICT; 500 DESIGN_INTERNAL_ERROR.
- No new status or business code is added.

## Evidence and limits

- AC-16 activity diagram says API #31 updates the attempt to SUBMITTED and performs automatic grading.
- AC-16 says the attempt becomes PENDING_GRADE if a question needs manual grading; otherwise it becomes GRADED.
- DB_UNICA_TABLES.md identifies quiz_attempts as API #31 UPDATE target and quiz_answers as the SELECT/update grading target. quiz_questions.score and quiz_choices.is_correct are candidate grading inputs only.
- The grading algorithm, manual-question predicate, unanswered-answer behavior, score scale/rounding, response projection, owner/state policy and transaction semantics are not specified.
- Checked-in DB.sql requires quiz_answers.is_correct NOT NULL, while API #30 does not define a pre-submit correctness value. Logical QuizAnswer supports choice_ids/text_answer, but physical design stores one choice_id per row and has no text answer column.
- DB table design/ERD/DDL are design artifacts; live schema is not verified.
- Current Study router/module/test scan finds no API #31 route, module or test: UNWIRED / NOT_FOUND.

## Sources reviewed

- docs/lists/list_api.md: API #31, ApiEnvelope, QuizAttempt, QuizAnswer and business codes.
- apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md and AC_02_STUDENT_LEARNING.drawio: AC-16 actor, precondition, submit and grading branches.
- apps/study-server/docs/diagrams/DB_UNICA_TABLES.md and DB_UNICA_ERD.drawio: candidate attempt/answer/question/choice relationships.
- infra/postgres/study-server/DB.sql: checked-in assessment DDL.
- contracts/api-guidelines/README.md: envelope/error/trace rules.
- apps/study-server/app/api/v1.py, app/modules/ and tests/: current wiring scan.
- apps/study-server/docs/dd/29_quizzes_attempts/ and 30_attempts_answers/: adjacent DD precedent.
- .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/: canonical eight-file template.
- .agents/server-study/workflows/README.md: no-ZIP Study DD policy.

## Tables

- Candidate reads: quiz_attempts, quiz_answers, quiz_questions and quiz_choices.
- Candidate writes: quiz_attempts status/submitted_at/score and quiz_answers is_correct/score_received.
- Exact predicates, update order, scoring and response mapping remain open; see OPEN_QUESTIONS.md.
