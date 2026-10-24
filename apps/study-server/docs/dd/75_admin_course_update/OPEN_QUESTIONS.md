# Câu hỏi còn mở — API #75

Trạng thái tài liệu: `Draft — Needs Confirmation`. Body và mutation bên dưới chỉ là proposal `DERIVED`; không dùng làm implementation contract trước khi các câu hỏi này được chốt.

1. **Request body:** API catalog và AC-32 chỉ có path, trong khi node diagram ghi `UPDATE course metadata`. Body gồm `title`, `description`, `thumbnail_url`, `price` có đúng phạm vi không?
2. **PUT semantics:** Bốn field có bắt buộc trong full replacement không? Có hỗ trợ partial update hay omission giữ giá trị hiện tại?
3. **Null/omission:** `description` và `thumbnail_url` có nhận `null` để xóa không? Omit, null và chuỗi rỗng được xử lý thế nào?
4. **Title validation:** Có rule trim, nonblank hoặc giới hạn ký tự nào không? Legacy `courses.name VARCHAR(200)` chỉ là candidate, không xác nhận live constraint.
5. **Thumbnail URL:** URI scheme, host allowlist, URL length và nullable policy là gì?
6. **Price:** Body dùng decimal-string? Precision/scale, min/max, số âm, rounding và nullability nào được duyệt? Legacy `NUMERIC(12,2)` cho phép NULL.
7. **Admin authorization:** JWT claim nào xác nhận Admin và course-management permission? Có scope/tenant boundary, guard hoặc policy source nào được dùng?
8. **Schema/persistence:** Chọn legacy BIGINT `courses` hay V1-PILOT UUID `courses`/`course_versions`? Live relation, columns, permissions và migration state đã được xác minh chưa?
9. **Response owner/category:** `Course.mentor` bắt buộc nhưng legacy `mentor_id` nullable; xử lý orphan/NULL thế nào? Có nguồn course-category relation được duyệt hay tiếp tục omit `category`?
10. **Response cardinality:** Có giữ `ApiEnvelope<Page<Course>>` với đúng một item như proposal theo #74, hay cần sửa catalog/reusable contract?
11. **Status/audit boundary:** Xác nhận #75 không đổi `status`/audit vì AC-32 giao status + audit cho #76.
12. **Timestamp/transaction:** Ai sở hữu `updated_at`, transaction boundary và rollback khi Q2 response mapping hoặc commit lỗi?
13. **Counters:** AC-32 detail yêu cầu đọc counters nhưng `Course` response không có counter fields. Có cần mở rộng contract hoặc tiếp tục loại khỏi #75?
14. **Error handling:** Xác nhận error envelope dùng `data:null` theo API guidelines hay `{}` theo helper hiện tại; thêm route Admin vào `DESIGN_CONTRACT_PATHS` khi wire?
15. **Macro-review AC-32:** Đã rà #73–#77; metadata/status/delete boundaries giữ riêng, còn Page singleton, deleted-target behavior, soft-delete policy/visibility và shared Admin/schema gaps cần chốt.

## Ranh giới proposal

- Bốn body fields và full-replacement/null-clear behavior là `DERIVED`; cần xác nhận.
- Legacy Course/User query và columns là candidates; live schema chưa xác minh.
- Page singleton, no-status-change, 404 on unmatched ID và transaction handling là proposals.
- Không thay đổi catalog, diagram, schema, runtime hoặc API #76/#77 trong DD #75.
## Rà nhóm AC-32 #73–#77 — 2026-10-24

- #75 chỉ sở hữu metadata; không đổi `status`, owner/category/counters hoặc audit. #76 giữ status + audit intent; #77 giữ soft-delete intent, không copy audit hoặc child-row mutation.
- Response #75 giữ `ApiEnvelope<Page<Course>>` theo catalog; body full-replacement là proposal `DERIVED`. #77 dùng `DeleteResult`.
- Cần quyết định #75 behavior khi target đã deleted và liệu #73/#74 phải ẩn target sau #77; chưa chọn physical marker/filter.
- Category relation, counters, Admin guard, CourseStatus casing, live schema, middleware và error envelope tiếp tục là blockers chung.
