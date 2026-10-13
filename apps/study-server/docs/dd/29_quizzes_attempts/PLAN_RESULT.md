# PLAN_RESULT — Study API #29

## Kết quả

- Output: apps/study-server/docs/dd/29_quizzes_attempts/
- API: POST /api/v1/quizzes/{quiz_id}/attempts
- DD status: Draft — Needs Confirmation.
- Scope: Source-backed API Detail Design only; no runtime, API catalog, diagram or DB schema changes.
- Package: No ZIP, according to the Study Server DD workflow.

## Contract được giữ

Nguồn: docs/lists/list_api.md, API #29 row.

- Actor/authentication: Student Bearer JWT.
- Input: path quiz_id:int64!; no query parameter or request body is defined.
- Success: HTTP 201 DESIGN_RESOURCE_CREATED, ApiEnvelope<QuizAttempt>.
- Errors: 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 422 DESIGN_VALIDATION_ERROR; 409 DESIGN_STATE_CONFLICT; 500 DESIGN_INTERNAL_ERROR.

## Evidence và giới hạn thiết kế

- AC-16 activity diagram specifies the API #29 create-attempt call and labels the inserted attempt IN_PROGRESS.
- AC-16 precondition requires quiz permission and an open quiz. The exact predicate and ownership of the check between API #28 and API #29 are not defined.
- AC-16 labels exhausted/expired cases as 403/409 without assigning each condition to a response code; the API #29 catalog contains both codes.
- DB_UNICA_TABLES.md, DB_UNICA_ERD.drawio and checked-in DB.sql provide candidate quiz_attempts schema only. Table design says quiz_id/user_id are required while DB.sql permits nullable foreign keys. Live metadata is not verified.
- Current Study router/module/test scan has no API #29 route, module or test. Status: UNWIRED / NOT_FOUND.
- Existing untracked API #27/#28 directories and worklogs were preserved.

## Files

- Eight template-derived sheets: 00_Cover.md through 07_table.md.
- OPEN_QUESTIONS.md.
- VERIFICATION_REPORT.md.
- Worklog: .agents/worklog/2026-10-12/create-study-api29-dd.md.

## Open decisions

See OPEN_QUESTIONS.md for eligibility ownership, attempt limit/expiry and 403/409 mapping, authenticated Student-to-user_id mapping, candidate schema constraints, and initial QuizAttempt response values.
