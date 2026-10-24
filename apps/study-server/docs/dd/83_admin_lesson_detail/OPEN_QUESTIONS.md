# Câu hỏi còn mở — API #83

Trạng thái tài liệu: Draft — Needs Confirmation. Các câu hỏi sau ảnh hưởng contract, data access hoặc triển khai.

1. **Dependencies trong AC-34:** Node n5 ghi “Đọc lesson + dependencies”. Cụ thể dependencies nào cần trả cho UI, field/count nào, và ở `Lesson`, `meta` hay response riêng? Nếu chỉ dùng trước delete, xác nhận API #86 tự kiểm tra quan hệ hiện tại.
2. **Active schema/live DB:** API dùng legacy BIGINT `lessons` hay V1-PILOT UUID/versioned lessons? Live schema và migration state chưa được xác minh.
3. **`course_id` nullability:** Legacy DDL cho phép NULL, reusable Lesson bắt buộc int64. Row NULL cần data correction, 500 hay contract/schema change?
4. **Admin authorization:** JWT Admin claim, lesson-management permission, scope/policy source và cách phân biệt 401/403 được triển khai ở đâu? Study hiện chỉ có Student guard.
5. **LessonStatus:** Các giá trị hợp lệ và casing là gì? DDL ghi default `DRAFT`, nhưng không có enum list chuẩn.
6. **Malformed `lesson_id`:** Catalog có int64 và error 404 nhưng không có 422. Có chấp nhận custom mapping path không parse được thành 404 như proposal không? Framework middleware hiện có thể phát 422 `VALIDATION_ERROR` nếu route không xử lý.
7. **Soft-delete visibility:** API #86 đề xuất soft-delete nhưng chưa có marker/schema được chọn. Xác nhận #82 loại lesson đã xóa khỏi list, #83 trả 404 hay chi tiết, và #84/#85 từ chối hay xử lý mutation trên lesson đã xóa ra sao.
8. **Optional field serialization:** Có chấp nhận `content:null` và `video_url:null` khi source NULL như API #09 model/test precedent, hay cần omit?
9. **Error envelope/integration:** Khi wire #83, thêm route path vào `DESIGN_CONTRACT_PATHS` và điều chỉnh helper để `data:null` theo API guideline hay dùng behavior `{}` hiện tại?

## Ranh giới proposal

- DIRECT: method/path, Bearer JWT, role Admin, required `lesson_id:int64`, `ApiEnvelope<Lesson>`, HTTP 200 và errors 401/403/404/500.
- DERIVED: lookup theo ID, no public `PUBLISHED` filter, absent row -> 404, malformed path -> 404, optional NULL serialization.
- SOURCE_REQUIRED: dependency output, live schema, nullability repair, Admin guard, LessonStatus enum, soft-delete policy and middleware/error integration.

## Kết quả macro-review AC-34

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` — đã đối chiếu tài liệu #82–#86; đây không phải owner approval hoặc runtime verification.
- Dependency, delete-visibility và ranh giới API được ghi trong [báo cáo macro-review](../86_admin_lesson_delete/VERIFICATION_REPORT.md#ac-34-macro-review).
