# Plan Result — Study API #36

## Status

Draft — Needs Confirmation.

## Output

- DD folder: apps/study-server/docs/dd/36_submissions_detail/.
- Sheets: 00_Cover.md, 01_Lich_su.md, 02_Overview.md, 03_Request.md, 04_Response.md, 05_Data_Mapping.md, 06_Error.md and 07_table.md.
- Reports: PLAN_RESULT.md, OPEN_QUESTIONS.md and VERIFICATION_REPORT.md.
- Worklog: .agents/worklog/2026-10-12/create-study-api36-dd.md.
- ZIP: N/A — Study Server workflow does not package DD output as ZIP.

## Basis and sources

- docs/lists/list_api.md — APPROVED_DESIGN_CONTRACT; API #36 method/path, Student Bearer, path type, Submission response and exact status/business-code set.
- apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md — maps API #36 to AC-17.
- apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio — AC-17 precondition, API #36 summary read and submitted-status display.
- apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio — AC-23 Mentor read/grade/feedback flow; does not define Student disclosure timing.
- apps/study-server/docs/diagrams/DB_UNICA_TABLES.md and DB_UNICA_ERD.drawio — candidate assignment_submissions fields and relations.
- infra/postgres/study-server/DB.sql — checked-in design DDL only; not live-schema evidence.
- contracts/api-guidelines/README.md — ApiEnvelope fields, error data=null and trace propagation.
- apps/study-server/docs/dd/33_assignments_detail/, 34_uploads/ and 35_assignments_submissions/ — adjacent API contracts and unresolved access/asset notes.
- apps/study-server/app/api/v1.py, app/utils/auth.py, modules/ and tests/ — current route/helper/test inventory; API #36 is not wired.
- .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/ — canonical eight-sheet template and appendix baseline.

## Tables read

- assignment_submissions — candidate lookup by id and candidate response fields.

## Tables write

- N/A — GET API; no write operation is defined.

## Request and response basis

- Request: Student Bearer JWT and path submission_id:int64!; no query or body is declared.
- Success: HTTP 200 DESIGN_RESOURCE_RETRIEVED with ApiEnvelope<Submission>.
- Errors: HTTP 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 404 DESIGN_RESOURCE_NOT_FOUND and 500 DESIGN_INTERNAL_ERROR.
- Submission fields follow the reusable schema in list_api.md. UploadAsset fields follow the reusable UploadAsset schema.
- Candidate physical response fields follow DB_UNICA_TABLES.md and checked-in DB.sql only where directly mapped; files[] remains unresolved against file_url.

## Assumptions and conflicts

- Keep API #36 design-only and preserve the exact catalog contract/error set.
- Candidate SELECT is by assignment_submissions.id; access predicate and 403-versus-404 policy remain open.
- score and feedback remain in the logical schema; no visibility/release rule is inferred from AC-23.
- DB nullability, SubmissionStatus lifecycle and timestamp timezone remain unresolved.
- Do not alter runtime code, catalog, diagrams, DDL, or existing DD/worklog #27–#35.
