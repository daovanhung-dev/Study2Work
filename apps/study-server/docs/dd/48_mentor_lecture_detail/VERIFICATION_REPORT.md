# Verification Report — API #48 Tải lại lecture vừa tạo

## Phạm vi

Đối chiếu API #48 với catalog, AC-21/AC-22, checked-in legacy DDL/migrations, API #34/#47 source, runtime route/module và focused HTTP tests. Không kết nối hoặc thay đổi live database, không deploy migration, không xác nhận Object Storage hay assigned-course behavior.

## Deliverable manifest

| File | Vai trò | Trạng thái |
|---|---|---|
| 00_Cover.md | Cover | Draft — Needs Confirmation |
| 01_Lich_su.md | Lịch sử | Updated for local implementation |
| 02_Overview.md | Overview | Updated for route/schema status |
| 03_Request.md | Request | Contract unchanged; raw path parsed in view |
| 04_Response.md | Response projection | Updated for uploads relation and nullable content |
| 05_Data_Mapping.md | Query, mapping and error flow | Updated for Q1/Q2 and runtime branches |
| 06_Error.md | Error mapping | Contract remains catalog 401/403/404/500 |
| 07_table.md | Read-only source mapping | Updated for lessons/courses/lesson_uploads/uploads |
| PLAN_RESULT.md | Plan and macro review | Updated with implementation evidence and remaining gaps |
| OPEN_QUESTIONS.md | Unconfirmed decisions | Updated; deployment/business questions remain |
| VERIFICATION_REPORT.md | Verification evidence | Current report |

## Contract/source checks

| Check | Evidence | Status |
|---|---|---|
| API catalog | GET `/api/v1/mentor/lectures/{lecture_id}`, Mentor Bearer, int64 path, `ApiEnvelope<Lecture>`, 200 and catalog errors 401/403/404/500 | PASS |
| AC-21 / AC-22 boundary | #47 creates the lecture, #48 reloads it; Content CRUD remains separate | PASS |
| API #34 metadata | Local API #34 source and migration 004 persist UploadAsset metadata in legacy `uploads` | SOURCE_BACKED; live DB unknown |
| API #47 relation | Local API #47 validates ordered refs and inserts `lesson_uploads` rows atomically with `lessons`; empty refs skip link insert | SOURCE_BACKED; live DB unknown |
| API #48 projection | Reads one lesson/course row, checks direct owner, reads upload links in position order, scopes metadata by owner/purpose/course | SOURCE_BACKED |
| Nullable content | Shared Lecture response model is `str | None`; API #48 test verifies JSON null | VERIFIED_LOCALLY |
| OpenAPI | Route is wired with `lecture_id` integer/int64 schema and Lecture response | VERIFIED_LOCALLY |
| Focused HTTP tests | API #47 + #48 focused files: `42 passed`, including empty-assets and incomplete-link rollback coverage | VERIFIED_LOCALLY |
| Full Study suite | `uv run pytest -q`: `336 passed` | VERIFIED_LOCALLY |
| Ruff | `uv run ruff check app tests`: all checks passed | VERIFIED_LOCALLY |
| Markdown links and source manifest | 37 local DD links resolve; manifest JSON parses and every required server-study source path exists | VERIFIED_STATIC_ONLY |
| Context validator | Full run reports missing DB Admin context/source and broad historical snapshot drift; `--skip-drift` leaves DB Admin baseline failures only. No API #48 required-source or context-link finding. | BLOCKED_BY_REPOSITORY_BASELINE |
| Checked-in migration | `005_lesson_uploads.sql` references legacy lessons/uploads; migration application not performed | VERIFIED_STATIC_ONLY |
| Assignment and identity | Direct `courses.mentor_id` plus numeric JWT subject follows #46/#47; no assignment relation was found in inspected artifacts | SOURCE_REQUIRED / NOT_IMPLEMENTED |
| Live deployment | No live DB inspection or deployed endpoint call | NOT_VERIFIED |

## Verification boundary

Local TestClient tests and OpenAPI generation establish the checked-in application behavior only. They do not prove live schema compatibility, that migrations 004/005 are applied, deployed authorization policy, or external storage behavior. The suite emitted one existing Starlette/httpx deprecation warning. The DD remains `Draft — Needs Confirmation` until open business and environment decisions are resolved.
