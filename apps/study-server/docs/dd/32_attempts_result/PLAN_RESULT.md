# Plan Result — Study API #32

## Status

Draft — Needs Confirmation.

## Output

- DD folder: apps/study-server/docs/dd/32_attempts_result/
- Sheets: 00_Cover.md, 01_Lich_su.md, 02_Overview.md, 03_Request.md, 04_Response.md, 05_Data_Mapping.md, 06_Error.md, 07_table.md.
- Reports: OPEN_QUESTIONS.md and VERIFICATION_REPORT.md.
- ZIP: N/A — Study Server workflow does not package DDs as ZIP.

## Basis and sources

- docs/lists/list_api.md — APPROVED_DESIGN_CONTRACT; API #32 request, response and error set.
- apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md — API-to-AC trace.
- apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio — AC-16 result branches.
- apps/study-server/docs/diagrams/DB_UNICA_TABLES.md and DB_UNICA_ERD.drawio — candidate physical data shape and relations.
- infra/postgres/study-server/DB.sql — checked-in design DDL, not live-schema evidence.
- contracts/api-guidelines/README.md — shared envelope/error convention.
- apps/study-server/app/api/v1.py, app/utils/auth.py, app/modules/ and tests/ — current route, auth, module and test surface.

## Tables read

- Candidate: quiz_attempts.
- Candidate: quiz_answers.

## Tables write

- None; API #32 is GET/read-only.

## Query and response basis

- Candidate attempt lookup by path attempt_id; candidate owner field quiz_attempts.user_id compared with current Student user_id.
- Candidate result fields come from quiz_attempts and quiz_answers. Query shape, answer ordering, ownership masking and field visibility remain open.
- No runtime SQL, live-schema claim, grading calculation, mutation or external call is included.

## Assumptions and conflicts

- API #32 means the Study API DD only, following the user-approved plan.
- Status remains Draft — Needs Confirmation; unresolved policy is recorded in OPEN_QUESTIONS.md.
- AC-16 routes both GRADED and PENDING_GRADE to API #32, but score/null/omit and answer visibility by state are undefined.
- AC-16 mentions feedback; QuizAttempt schema and candidate tables do not define a feedback field.
- Logical QuizAnswer answer shape does not match the single-choice physical design.
- Current Study runtime has no API #32 route/module/test; DD is design-only.
