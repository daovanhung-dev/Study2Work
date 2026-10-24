# Câu hỏi còn mở — API #76

Trạng thái tài liệu: Draft — Needs Confirmation. Body/mapping trong DD là proposal; các điểm sau cần owner/schema/security quyết định trước khi implementation.

1. **Body contract:** PATCH status có nhận body{status:CourseStatus!} không? Content-Type và unknown field behavior là gì?
2. **CourseStatus members/casing:** Catalog ghi draft/published/suspended; legacy/API #06 ghi DRAFT/PUBLISHED; enum CourseStatus không có member list. Chọn exact values/casing nào?
3. **Transition matrix/no-op:** Có cho phép mọi trạng thái đích từ mọi trạng thái hiện tại không? Same-status request có update timestamp và ghi audit event không?
4. **Publish readiness:** Chuyển sang PUBLISHED có cần kiểm tra nội dung/metadata đã sẵn sàng không? AC-32 diagram không có readiness gate; API #52 publish content có gate riêng.
5. **Suspension effects:** Khi SUSPENDED, API public ẩn course; learner đã enroll có tiếp tục xem course/lesson không? Có notify hay cập nhật enrollment nào không?
6. **Audit schema:** Audit event phải ghi action, actor, resource, old/new status, outcome, business code, trace, retention và integrity theo bảng nào? Legacy DDL không có audit table; pilot audit_events dùng UUID không khớp API int64.
7. **Schema/live DB:** API chạy trên legacy BIGINT courses.status hay V1-PILOT UUID/versioned course model? Live relation/permissions/migration đã được xác minh chưa?
8. **Admin authorization:** JWT claim/policy nào xác nhận Admin và course-management permission? Actor ID cho audit lấy từ đâu; tenant/scope có giới hạn không?
9. **Response wrapper:** Giữ ApiEnvelope&lt;Page&lt;Course&gt;&gt; cho PATCH-by-ID và singleton pagination 1/1/1/1 như #74/#75, hay sửa reusable contract?
10. **Projection gaps:** Course.mentor required nhưng legacy mentor_id nullable; price required nhưng nullable; category optional nhưng thiếu relation. Quy tắc với orphan/NULL là gì?
11. **Idempotency:** API guideline yêu cầu Idempotency-Key cho retryable mutations. API #76 cần key để tránh duplicate audit event không? TTL, replay response và key scope nào?
12. **Error integration:** Invalid status/path map cụ thể vào 422 ra sao? Khi wire route, middleware exact path membership sẽ match dynamic course_id bằng cách nào? Có xử lý error data:null theo guideline không?
13. **AC-32 macro-review:** Đã rà #73–#77; status/audit của #76 tách khỏi metadata #75 và soft-delete #77. Enum/visibility, audit schema, deletion/dependency policy và middleware mapping vẫn mở.

## Ranh giới proposal

- Body {status}, uppercase status candidates, direct target assignment, updated_at, atomic update+audit và singleton Page là DERIVED.
- Logical audit intent là DIRECT; physical audit table/SQL là SOURCE_REQUIRED.
- Legacy DDL, V1-PILOT, live schema và Admin runtime không được nhập làm một.
- Không tạo 409 hoặc business code ngoài danh sách #76.
## Rà nhóm AC-32 #73–#77 — 2026-10-24

- #76 là nhánh status + audit intent theo diagram; không mở rộng sang #75 metadata hoặc #77 deletion. Physical audit storage và atomicity vẫn `SOURCE_REQUIRED`/`DERIVED` như đã ghi.
- Status enum/casing và tác động `SUSPENDED` chưa được quyết định. Visibility sau soft-delete thuộc policy #77 và cần filter thống nhất với #73/#74.
- #75/#76 hành vi trên deleted target, Admin guard, schema generation, error `data:null`/helper `{}` và dynamic middleware mapping còn mở.
