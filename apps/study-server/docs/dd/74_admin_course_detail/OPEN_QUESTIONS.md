# Câu hỏi còn mở — API #74

Trạng thái tài liệu: `Draft — Needs Confirmation`. Các mục sau cần được chốt trước khi dùng proposal làm implementation contract.

1. **Admin authorization:** JWT Admin claim, course-management permission, scope và guard được xác thực bằng nguồn nào? Study hiện chỉ có Student guard.
2. **Counters trong AC-32:** Counter nào cần đọc, định nghĩa/cách đếm là gì, và thuộc `Course`, `meta` hay response riêng? Catalog hiện không khai báo trường counter.
3. **Response detail wrapper:** Có giữ `ApiEnvelope<Page<Course>>` với đúng một item như API #08, hay cập nhật catalog/reusable contract thành `ApiEnvelope<Course>`? DD giữ nguyên contract hiện tại và đề xuất singleton Page.
4. **Chọn schema:** API #74 dùng legacy BIGINT `courses/users` hay V1-PILOT UUID `courses/course_versions`? Live schema và migration state chưa được xác minh.
5. **Mentor integrity:** Legacy DDL cho phép `courses.mentor_id` NULL trong khi DB table guide ghi bắt buộc và Course.mentor là required. Admin có cần xem/sửa course mồ côi thay vì nhận 500?
6. **Category mapping:** Course có optional `category`, nhưng không có quan hệ course-category trong schema candidate. Có source/schema nào được duyệt để trả field này không?
7. **CourseStatus:** Các giá trị hợp lệ và casing là gì? #76 nêu draft/published/suspended; legacy/API #08 có `DRAFT`/`PUBLISHED`.
8. **Nullable fields:** `description`, `thumbnail_url`, `mentor.avatar_url` được serialize null hay omit? DD đề xuất null theo model #08.
9. **Path error boundary:** ID malformed/overflow/outside int64 nên ánh xạ 404 như API #08 hay xử lý khác trong khi catalog #74 không có 422?
10. **Error integration:** Khi wire API #74, thêm path vào `DESIGN_CONTRACT_PATHS` chưa? Chuẩn hóa error `data:null` theo guideline hay giữ helper hiện tại `{}`?
11. **AC-32 macro-review:** Đã rà #73–#77; owner/counters, response wrapper của #74–#76, status transitions, soft-delete visibility/persistence và enrollment/content policy vẫn cần quyết định.

## Ranh giới proposal

- Query legacy và owner join chỉ là candidate; chưa phải live-schema claim.
- Page singleton, all-status visibility, invalid-path 404 và orphan mentor 500 là proposal `DERIVED`, chưa được phê duyệt.
- Không thay đổi catalog, diagram, schema hoặc runtime trong task này.
## Rà nhóm AC-32 #73–#77 — 2026-10-24

- AC-32 detail yêu cầu course + owner + counters; Course response hiện có owner nhưng reusable schema không định nghĩa counter fields. Không thêm counter vào response/query.
- #74 giữ nguyên `ApiEnvelope<Page<Course>>` theo catalog; singleton Page chỉ là proposal. #77 trả `DeleteResult`, không đổi cardinality của #74.
- Nếu #77 soft-delete course, ẩn khỏi #74 là proposal hợp lý nhưng marker/filter chưa có nguồn. #75/#76 với deleted target cũng chưa được định nghĩa.
- Admin guard, category/mentor/nullability, status casing, schema selection và error middleware còn mở trên toàn nhóm.
