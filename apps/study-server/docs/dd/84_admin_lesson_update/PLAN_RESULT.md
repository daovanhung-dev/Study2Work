# Kết quả plan — API #84 Cập nhật lesson

- Status: Draft — Needs Confirmation; local implementation and source/test evidence are complete.
- Output folder: `apps/study-server/docs/dd/84_admin_lesson_update/` (11 Markdown files).
- Direct basis: catalog #84 and AC-34 specify PUT path, Bearer/Admin, signed int64 path, `ApiEnvelope<Lesson>`, 200 `DESIGN_RESOURCE_UPDATED`, and exact 401/403/404/422/500 codes. Diagram says UPDATE lesson and reload list; neither source declares a request body.
- DERIVED fallback selected for this task: strict full-replacement JSON body `{title, content, video_url, order}`; title max 200, content/video_url nullable, order signed int32. One bound legacy `lessons` UPDATE/RETURNING sets metadata and `updated_at`; course_id/status/created_at/dependency/audit records are preserved.
- Runtime: route shares #83's path template, uses shared `ADMIN` role auth, maps raw invalid path to 422, returns direct Lesson, commits after valid mapping and rolls back on no-row/query/mapping/commit failure. FastAPI validates typed body before calling the view, so a malformed body can return 422 before authorization.
- Schema boundary: code follows the checked-in legacy BIGINT mapping used by APIs #09/#82/#83; V1-PILOT UUID/versioned lessons and live schema are not claimed equivalent. Nullable legacy `course_id` conflicts with required Lesson and maps safely to 500.
- Sources reviewed: router/context map/worklog preflight; selected #74/#75/#76 logs and API #83 worklog; server-study workflow/scope/manifest; catalog #84/reusable Lesson; AC-34 diagram; DD #82/#83/#75/#85/#86 boundaries; current auth/response/middleware/database helpers; APIs #09/#47/#48/#75/#82/#83; legacy and V1-PILOT DDL.
- Tables read: legacy `lessons` and lesson-upload relationships; V1-PILOT Lesson model compared as a distinct schema.
- Tables written: legacy `lessons.name/content/video_url/sort_order/updated_at` fallback; no new table, migration or DDL change.
- Verification: API #84 focused suite 23 passed; linked #09/#47/#48/#82–#84 regression 104 passed; full Study suite 1050 passed; full Ruff passed. Fake sessions do not prove live DB/deployment.
- Remaining evidence gaps: canonical body approval, active live schema, timestamp trigger state, fine-grained AC-34 permission and deleted-row visibility with #86.
