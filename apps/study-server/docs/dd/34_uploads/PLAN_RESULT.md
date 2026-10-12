# Plan Result — Study API #34

## Status

Draft — Needs Confirmation.

## Output

- DD folder: apps/study-server/docs/dd/34_uploads/.
- Sheets: 00_Cover.md, 01_Lich_su.md, 02_Overview.md, 03_Request.md, 04_Response.md, 05_Data_Mapping.md, 06_Error.md, 07_table.md.
- Reports: PLAN_RESULT.md, OPEN_QUESTIONS.md and VERIFICATION_REPORT.md.
- Worklog: .agents/worklog/2026-10-12/create-study-api34-dd.md.
- ZIP: N/A — Study Server workflow does not package DD output as ZIP.

## Basis and sources

- docs/lists/list_api.md — APPROVED_DESIGN_CONTRACT; API #34 method/path, Student/Mentor roles, multipart fields, UploadAsset schema and success/error codes.
- apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md — API #34 is referenced by AC-17 and AC-21.
- apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio — AC-17 upload step for assignment submission and Object Storage file save.
- apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio — AC-21 upload step for lecture/media and Object Storage save.
- apps/study-server/docs/diagrams/DB_UNICA_TABLES.md and DB_UNICA_ERD.drawio — no Uploads table among ERD V1 entities; ERD footer and table notes leave a persistence discrepancy.
- infra/postgres/study-server/DB.sql — checked-in DDL; no Uploads table and not evidence of live schema.
- contracts/api-guidelines/README.md — envelope, data = null on errors, safe field details and trace ID.
- apps/study-server/app/api/v1.py, current route/module/test inventory, and app/utils/auth.py — API #34 is absent; existing auth behavior is not treated as API #34 behavior.
- apps/study-server/docs/dd/13_users_me_avatar/ and app/service/object_storage/avatar.py — separate current Student avatar flow used only as a contrast/reference.
- .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/ — canonical eight-sheet Markdown template and source appendices.

## Tables read

- None assigned to API #34 by the catalog or AC-17/AC-21.
- Any course lookup needed for authorization remains SOURCE_REQUIRED.

## Tables write

- No database table mapping is specified by the current contract/design evidence.
- AC-17/AC-21 specify an Object Storage side effect; provider key, metadata persistence and cleanup are unresolved.

## Request and response basis

- Request: multipart with required file binary, required UploadPurpose purpose, and optional int64 course_id.
- Roles: Bearer JWT; role in Student or Mentor.
- Success: HTTP 201 DESIGN_RESOURCE_CREATED, ApiEnvelope<UploadAsset>.
- Errors: only HTTP 401/403/422/503/500 and their catalog DESIGN codes.
- Response properties: id:int64, name:string, url:uri, content_type:string, size_bytes:int64, status:UploadStatus.
- UploadPurpose and UploadStatus values are not defined in the catalog or diagram; response source for asset ID and metadata is not defined.

## Assumptions and conflicts

- Keep API #34 design-only and preserve the catalog contract without adding request fields, response fields, status codes, enum values or database tables.
- The API #34 row's display name concatenates several phrases; use “Upload file” as the document label while keeping API ID/path unchanged.
- The ERD footer mentions Uploads storing URLs but there is no Uploads entity/table; do not select a physical persistence model.
- Existing API #13 uses JSON Base64 avatar upload and maps storage failure to 500. Do not reuse its role, transport, file limits, object key, URL construction or error behavior for API #34.
- Current router/module/test inventory does not contain API #34; this DD describes expected design only.
