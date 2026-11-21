# Kết quả plan — API #86 Xóa lesson

- Status: Draft — Needs Confirmation.
- Output folder: apps/study-server/docs/dd/86_admin_lesson_delete/.
- Basis: Catalog #86, reusable DeleteResult và AC-34 diagram; body/query không được khai báo.
- Direct contract: DELETE /api/v1/admin/lessons/{lesson_id}, Bearer JWT/Admin, path lesson_id:int64!, no body/query, ApiEnvelope<DeleteResult>, HTTP 200 DESIGN_RESOURCE_DELETED, exact errors 401/403/404/422/500 theo catalog.
- Direct AC-34 intent: Admin có lesson-management permission; đọc lesson/dependencies, DELETE theo policy, soft-delete option, reload danh sách. Catalog title yêu cầu progress/reference checks.
- Sources reviewed: root/global/scope routers, context map, worklog preflight #48–#50, server-study entry/index/workflow/routes/runtime/database/security/tests, manifest skill/workflow registry, registered createDD-markdown templates, catalog, AC-34 index/diagram, DD #82–#85, precedents #72/#77, current router/auth/middleware/response helper, API guidelines, legacy và V1-PILOT DDL.
- Archive/output: Study scope chỉ giao Markdown; không tạo ZIP.
- Tables read: legacy lessons/resources/lesson_progress/lesson_uploads and #85 audit relation; V1-PILOT lessons and restrictive dependent relations, kept separate.
- Tables write: `lessons.status='DELETED'`, `updated_at=CURRENT_TIMESTAMP`; no child, audit, migration or hard-delete write.
- Selected local policy: DERIVED fallback based on the API #77 marker and existing legacy columns. Any progress/resource/lesson-upload reference returns catalog 422; DB `updated_at` maps to `DeleteResult.deleted_at`; repeat delete returns 404.
- Visibility: active reads/writes in Admin #82–#85 and direct Mentor/resource readers #48/#12 exclude/reject the tombstone.
- Assumptions: #86 does not add an audit operation; existing #85 history is retained. Fine-grained AC-34 authorization and live schema remain unverified.
- Verification: API #86 focused tests, linked route regression, full Study suite, Ruff, OpenAPI, DD checks and context validation are recorded in `VERIFICATION_REPORT.md` and the implementation worklog.
