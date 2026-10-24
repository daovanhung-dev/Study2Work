# Kết quả plan — API #74

- Trạng thái: `Draft — Needs Confirmation`.
- Folder: `74_admin_course_detail/`.
- Contract: `GET /api/v1/admin/courses/{course_id}`, Admin Bearer JWT, `ApiEnvelope<Page<Course>>`, success 200, errors 401/403/404/500 theo catalog.
- Basis trực tiếp: catalog #74, AC-32 index và activity diagram, reusable `Course`/`Page`/`PageMeta`/`UserSummary`.
- Query candidate: một row legacy `courses` theo ID, LEFT JOIN `users`; không lọc status; live schema chưa xác minh.
- Tables read candidate: legacy `courses`, `users`.
- Tables write: không có; API read-only.
- `Page<Course>`: đề xuất một item/page metadata 1/1/1/1 theo precedent API #08 (`DERIVED`).
- Counter: diagram có nhắc nhưng response không có field/type; không tự tạo field/query, giữ `SOURCE_REQUIRED`.
- Category: optional trong Course nhưng không có relation; đề xuất omit, giữ mapping `SOURCE_REQUIRED`.
- Admin permission mechanism, live schema, orphan mentor, null/omit và enum còn mở.
- Verification: xem [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).
## Kết quả macro-review AC-32 — 2026-10-24

Đã rà #73–#77 sau khi #77 tồn tại. #74 tiếp tục dùng `Page<Course>` như catalog; singleton page vẫn là proposal. Diagram nhắc counters nhưng reusable response không có counter fields, nên cần product/API owner chốt nếu muốn mở rộng. Deleted-course visibility và hành vi #75/#76 sau soft-delete còn mở; không tạo field/filter. Shared Admin guard, status casing, schema và error integration gaps được ghi trong verification report.
