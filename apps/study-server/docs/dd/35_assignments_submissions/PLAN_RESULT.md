# Plan Result — Study API #35

## Status

Draft — Needs Confirmation.

## Output

- DD folder: apps/study-server/docs/dd/35_assignments_submissions/.
- Sheets: 00_Cover.md, 01_Lich_su.md, 02_Overview.md, 03_Request.md, 04_Response.md, 05_Data_Mapping.md, 06_Error.md, 07_assignment_submissions_insert_update.md.
- Reports: PLAN_RESULT.md, OPEN_QUESTIONS.md and VERIFICATION_REPORT.md.
- Worklog: .agents/worklog/2026-10-12/create-study-api35-dd.md.
- ZIP: N/A — Study Server workflow does not package DD output as ZIP.

## Basis and sources

- docs/lists/list_api.md — APPROVED_DESIGN_CONTRACT; API #35 method/path, Student Bearer, request notation, Submission response and exact status/business-code set.
- apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md — traces API #35 to AC-17.
- apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio — AC-17 precondition, API sequence, assignment access/deadline decision, preceding API #34 upload and INSERT/UPDATE Submission = SUBMITTED step.
- apps/study-server/docs/diagrams/DB_UNICA_TABLES.md and DB_UNICA_ERD.drawio — candidate assignments and assignment_submissions fields/relations.
- infra/postgres/study-server/DB.sql — checked-in design DDL; not live-schema evidence.
- contracts/api-guidelines/README.md — ApiEnvelope, error data=null, trace propagation and Idempotency-Key guidance for retryable mutations.
- apps/study-server/docs/dd/33_assignments_detail/ — adjacent assignment contract and unresolved access/deadline notes.
- apps/study-server/docs/dd/34_uploads/ — preceding UploadAsset/Object Storage contract and unresolved asset identity/persistence notes.
- apps/study-server/app/api/v1.py, app/modules/, app/utils/auth.py and tests/ — current route/helper/test status.
- .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/ — canonical eight-sheet Markdown template and appendices.

## Tables read

- assignments — candidate assignment existence, course_id and due_at lookup.
- assignment_submissions — candidate existing-row lookup only if upsert is approved.
- No exact SQL or authorization join is specified.

## Tables write

- assignment_submissions — candidate INSERT/UPDATE identified by AC-17 and DB design; runtime persistence is not verified.

## Request and response basis

- Request: Bearer JWT; path assignment_id:int64!; required text:string! and file refs:string! catalog notation.
- Success: HTTP 201 DESIGN_RESOURCE_CREATED with ApiEnvelope<Submission>.
- Errors: HTTP 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 404 DESIGN_RESOURCE_NOT_FOUND, 409 DESIGN_STATE_CONFLICT, 422 DESIGN_VALIDATION_ERROR and 500 DESIGN_INTERNAL_ERROR.
- Logical Submission fields follow the reusable schema in list_api.md; UploadAsset fields follow the reusable UploadAsset schema.
- API #35 receives file-reference notation after the API #34 upload flow; the precise reference shape and persistence mapping are unresolved.

## Assumptions and conflicts

- Keep the approved API #35 catalog contract unchanged and use only its error set.
- Preserve file refs exactly as catalog notation; the sample JSON does not establish a final wire key or encoding.
- AC-17 supplies the initial status SUBMITTED and says INSERT/UPDATE; no branch key, retry policy or resubmission rule is inferred.
- Logical Submission.files is UploadAsset[] but candidate assignment_submissions exposes one file_url; no association table is invented.
- Logical content is optional and the candidate physical content column is nullable, while the request requires text.
- DB table notes describe assignment_id/user_id as required; checked-in DB.sql permits NULL foreign keys. Live schema was not checked.
- API #35 has no current route/module/query/test and remains UNWIRED / NOT_FOUND.
