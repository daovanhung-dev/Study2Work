# Kết quả plan — API #86 Xóa lesson

- Status: Draft — Needs Confirmation.
- Output folder: apps/study-server/docs/dd/86_admin_lesson_delete/.
- Basis: Catalog #86, reusable DeleteResult và AC-34 diagram; body/query không được khai báo.
- Direct contract: DELETE /api/v1/admin/lessons/{lesson_id}, Bearer JWT/Admin, path lesson_id:int64!, no body/query, ApiEnvelope<DeleteResult>, HTTP 200 DESIGN_RESOURCE_DELETED, exact errors 401/403/404/422/500 theo catalog.
- Direct AC-34 intent: Admin có lesson-management permission; đọc lesson/dependencies, DELETE theo policy, soft-delete option, reload danh sách. Catalog title yêu cầu progress/reference checks.
- Sources reviewed: root/global/scope routers, context map, worklog preflight #48–#50, server-study entry/index/workflow/routes/runtime/database/security/tests, manifest skill/workflow registry, registered createDD-markdown templates, catalog, AC-34 index/diagram, DD #82–#85, precedents #72/#77, current router/auth/middleware/response helper, API guidelines, legacy và V1-PILOT DDL.
- Archive/output: Study scope chỉ giao Markdown; không tạo ZIP.
- Tables read: legacy lessons/resources/lesson_progress; V1-PILOT lessons and restrictive dependent relations, kept separate.
- Tables write: Logical soft-delete recommendation only; physical relation/marker/timestamp SOURCE_REQUIRED.
- Candidate policy: DERIVED recommendation to preserve history with soft-delete; if an approved reference/progress dependency exists, block with existing 422 DESIGN_VALIDATION_ERROR and do not cascade. The exact blocker set needs confirmation.
- Assumptions: Do not add an audit operation to #86; AC-34 explicitly assigns status audit to #85. Do not invent deleted_at column or timestamp source.
- Conflicts: AC-34 permits soft-delete or policy delete; legacy/V1 lesson schemas lack delete marker; DeleteResult requires deleted_at; live DB and Admin guard are unverified.
- Verification: static-only; no application tests or runtime claims.
