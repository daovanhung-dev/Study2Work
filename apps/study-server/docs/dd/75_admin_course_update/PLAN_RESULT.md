# Kết quả plan — API #75

- Trạng thái: `Draft — Needs Confirmation`.
- Folder: `75_admin_course_update/`.
- Direct contract: `PUT /api/v1/admin/courses/{course_id}`, Admin Bearer JWT, path `course_id:int64!`, `ApiEnvelope<Page<Course>>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, lỗi catalog 401/403/404/422/500.
- Direct body/query: catalog và AC-32 diagram chỉ khai báo path; query và body không được chỉ định.
- Body runtime `DERIVED`: strict JSON full replacement gồm `title`, `description`, `thumbnail_url`, `price`; required fields, null handling, title max 200 và price `NUMERIC(12,2)` candidate được ghi trong [03_Request.md](./03_Request.md).
- Persistence runtime `DERIVED`: legacy BIGINT `courses`; UPDATE metadata + `updated_at`, sau đó SELECT Course/mentor projection trong cùng transaction. Không đổi status/mentor, không thêm category/counters/audit.
- Authorization runtime: shared JWT role `ADMIN`; dedicated course-management permission vẫn `SOURCE_REQUIRED`.
- Response runtime: singleton `Page<Course>` theo #74; category omit khi không có relation source-backed. Query/projection/commit errors trả 500 an toàn và rollback; UPDATE không có row trả 404.
- Cross-API review: #74 GET, #75 metadata PUT, #76 status/audit và #77 soft-delete giữ route/mutation boundaries riêng. Visibility sau soft-delete, deleted-target behavior và permission policy vẫn mở.
- Files/API catalog/diagram/schema ngoài phạm vi không được đổi; DDL/migration/live database không được chỉnh.
- Verification: xem [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).
