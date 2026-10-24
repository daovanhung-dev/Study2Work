# Câu hỏi còn mở — API #84

Trạng thái: Draft — Needs Confirmation. Catalog/diagram không mô tả body; candidate dưới đây chưa phải contract được duyệt.

1. **Request body:** API #84 chỉ khai báo path{lesson_id:int64!} nhưng thao tác là PUT/UPDATE. Xác nhận body có title, content, video_url, order không?
2. **PUT semantics:** Bốn field có bắt buộc đồng thời không? Omit có giữ nguyên hay lỗi? Null và chuỗi rỗng nghĩa là gì?
3. **Title/content validation:** Có trim, nonblank, max length hoặc sanitizer rules nào không? Legacy name VARCHAR(200) chỉ là DDL candidate.
4. **Video URL:** Có cho null-to-clear không? Scheme, host và length policy nào được duyệt?
5. **Order:** Có min/max, uniqueness hay yêu cầu reorder sibling lessons không? Có mutation nhiều row không?
6. **Course association:** Có cho phép chuyển lesson sang course khác không? Proposal không nhận course_id vì chưa có rule nguồn.
7. **Status boundary:** Xác nhận #84 không đổi status; #85 riêng xử lý trạng thái và audit.
8. **Active schema/live DB:** Chọn legacy BIGINT lessons hay V1-PILOT UUID/versioned model? Live schema/migration state đã được xác nhận chưa?
9. **Nullability/response:** Legacy course_id nullable, reusable Lesson bắt buộc int64; xử lý row null thế nào? content/video_url serialize null hay omit?
10. **LessonStatus:** Giá trị/casing hợp lệ là gì? #84 chỉ trả status hiện tại.
11. **Admin authorization:** JWT claim nào xác nhận Admin và lesson-management permission? Policy/guard/scope boundary nào được dùng?
12. **Timestamp/transaction:** Ai cập nhật updated_at? Có DB trigger không? Caller nào sở hữu transaction/commit và rollback nếu response mapping thất bại?
13. **404/deleted visibility:** No matching row có trả 404 DESIGN_RESOURCE_NOT_FOUND không? Sau policy soft-delete ở #86, xác nhận #82 loại lesson khỏi list, #83 xử lý detail và #84/#85 coi mutation trên lesson đó là not found hay theo policy khác.
14. **422 behavior:** Validation rules cụ thể và cấu trúc meta.fieldErrors nào được duyệt?
15. **Error envelope:** Guideline yêu cầu data:null; helper hiện defaults data:{}. Chuẩn nào áp dụng khi wire route và thêm path vào middleware allowlist?

## Ranh giới proposal

- DIRECT: method/path/auth/path type/response/success/error set.
- DERIVED: body candidates, full replacement candidate, null-to-clear candidate, legacy one-row UPDATE/RETURNING and no-row 404.
- SOURCE_REQUIRED: approved body/schema/validation, active schema/live DB, Admin policy, status enum, timestamp owner, transaction/error middleware integration.

## Kết quả macro-review AC-34

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` — đã đối chiếu tài liệu #82–#86; đây không phải owner approval hoặc runtime verification.
- Boundary metadata/status/delete, reload về #82 và các câu hỏi soft-delete được tổng hợp trong [báo cáo macro-review](../86_admin_lesson_delete/VERIFICATION_REPORT.md#ac-34-macro-review).
