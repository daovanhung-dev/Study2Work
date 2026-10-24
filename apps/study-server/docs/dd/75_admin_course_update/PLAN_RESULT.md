# Kết quả plan — API #75

- Trạng thái: `Draft — Needs Confirmation`.
- Folder: `75_admin_course_update/`.
- Contract direct: `PUT /api/v1/admin/courses/{course_id}`, Admin Bearer JWT, path `course_id:int64!`, `ApiEnvelope<Page<Course>>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, errors 401/403/404/422/500 theo catalog.
- Body/query direct: catalog và AC-32 diagram chỉ khai báo path; query không có. Body không được chỉ định.
- Body proposal `DERIVED`: full replacement `title`, `description`, `thumbnail_url`, `price`; không cập nhật status, owner, category hoặc counters.
- Candidate data model: legacy BIGINT `courses`/`users`; V1-PILOT UUID/versioned model giữ tách biệt; live schema chưa xác minh.
- Candidate mutation: UPDATE metadata và `updated_at` theo course ID; zero row → 404; read response projection và commit theo API #14 transaction pattern.
- Response proposal: `Page<Course>` singleton theo #74; category omit nếu không có source; mentor/price nullability discrepancies giữ open.
- Current source: Admin route/module/test/guard chưa có; future middleware path allowlist và error `data` shape cần giải quyết.
- Macro-review AC-32: hoàn tất sau khi DD #77 tồn tại; xác nhận metadata/status/delete boundaries và ghi các gap chung.
- Verification: xem [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).
## Kết quả macro-review AC-32 — 2026-10-24

#75 là metadata-only; #76 là status + audit theo diagram; #77 là soft-delete theo policy. Không API nào sở hữu update owner/category/counters theo DD hiện tại. `Page<Course>` cho #75 và `DeleteResult` cho #77 giữ đúng catalog. Deleted-target handling, visibility, schema và authorization vẫn cần quyết định.
