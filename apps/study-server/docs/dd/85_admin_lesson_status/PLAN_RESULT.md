# Kết quả plan — API #85 Đổi trạng thái lesson

- Status tài liệu: `Draft — Needs Confirmation`.
- Implementation status: local route/module/tests and migration source are wired; live schema/deployment is not verified.
- Output folder: `apps/study-server/docs/dd/85_admin_lesson_status/`.
- Basis: Catalog #85 and AC-34; direct contract covers PATCH path, Bearer/Admin, int64 path, direct Lesson envelope, 200 and exact 401/403/404/422/500 errors. Diagram n9/n10/n13 defines status + audit then list reload.
- DERIVED fallback: strict body `{status}` with `DRAFT`, `PUBLISHED`, `SUSPENDED` from adjacent Admin Course API #76; no transition matrix; same-status is a no-op.
- Physical fallback: update legacy BIGINT `lessons.status/updated_at` and append `lesson_status_audit_logs` from migration 012 with lesson/actor BIGINT keys and previous/new status. Update and audit share one Session transaction.
- Sources reviewed: project router/context map, selected coding worklogs #74–#76 plus #84, server-study route/auth/DB/test conventions, catalog/reusable Lesson, AC-34, APIs #82–#86, legacy DB.sql, V1-PILOT DDL and audit patterns #76/#80.
- Schema boundary: legacy BIGINT runtime mapping and V1-PILOT UUID/versioned schema remain separate; migration 012 source does not prove live DB state.
- Authorization boundary: shared ADMIN role guard is wired; AC-34 fine-grained lesson-management permission remains unimplemented/unverified.
- Transaction: row lock, status update, audit insert, Lesson mapping, then commit. Query/audit/map/commit errors rollback; no-op skips audit and commits to release lock.
- Verification: focused suite 28 passed; linked #09/#47/#48/#82–#85 regression 132 passed; full Study suite 1078 passed; Ruff passes; OpenAPI 50 paths/56 operations. DD package: 11 files, 8/8 template appendix suffixes match, 37 Markdown tables/430 rows, 18 balanced fence markers, 4 JSON blocks parse, 40 local links resolve, no trailing whitespace. `git diff --check` passes. Context validator reports only pre-existing missing DB Admin scope/source and unavailable baseline commit; no API #85 path issue was reported.
