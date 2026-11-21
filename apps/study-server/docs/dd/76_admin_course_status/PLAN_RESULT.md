# Kết quả implementation plan — API #76

## Phạm vi

Implement `PATCH /api/v1/admin/courses/{course_id}/status` theo API catalog và AC-32. Scope gồm module/route, middleware error-template registration, candidate legacy audit migration/DDL, API #76 Markdown DD và server-study context. Không đổi catalog, AC diagram, business code hoặc #75/#77 behavior.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Context/preflight | Đọc root/context-map/scope instructions; Deno coding selector trả 69 worklogs và chọn #74/#75/#34; đọc đủ cả ba, shortage none. |
| Source precedence | Đọc AC-32 diagram/index → legacy/V1-PILOT DDL/ERD/table guide → API catalog #76 → DD #76 và source/test APIs #71/#73–#75/#77. |
| Diagram | STATUS flow gọi #76 → update status + audit log → reload management. |
| Catalog | Giữ exact method/path, int64 path, `ApiEnvelope<Page<Course>>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, errors 401/403/404/422/500. Catalog không khai báo body. |
| Schema | Legacy `courses/users` BIGINT phù hợp API path và numeric JWT sub. Legacy schema không có audit relation; V1-PILOT `audit_events` UUID không khớp. |
| Pre-code plan | Worklog ghi classification, expected/current behavior, source trace, discrepancies, detailed plan trước application/schema/DD/context edits. |
| DERIVED fallback | Strict `{status}` body; uppercase DRAFT/PUBLISHED/SUSPENDED; shared ADMIN role; direct target assignment; same-status no-op; singleton Page; `course_status_audit_logs` migration/DDL. |
| Transaction | Row lock, status/timestamp update, audit insert cùng transaction, readback + Course mapping trước commit; lỗi rollback. |
| Route integration | PATCH route có OpenAPI metadata; middleware nhận distinct `/admin/courses/{course_id}/status` template để body errors dùng DESIGN envelope. |
| Schema docs | Legacy Study DDL + migration 010 + DB table guide + ERD mô tả candidate audit relation, đánh dấu DERIVED/live-unverified. |
| DD/context | Đồng bộ #76 sheets/reports; giữ 11 Markdown files, template appendices và `Draft — Needs Confirmation`; cập nhật server-study route/schema/test/source status. |
| Macro-review | Rà ranh giới #73–#77; #75 metadata-only, #76 status/audit, #77 soft-delete. |

## Giới hạn

Fake DB HTTP tests xác nhận local route/orchestration/error/response; chúng không xác nhận PostgreSQL syntax trên live database, migration rollout, permission policy, hoặc deployed API. Audit table và body/status policy là local DERIVED choices để có implementation dễ đọc theo diagram/catalog, chờ owner confirmation.
