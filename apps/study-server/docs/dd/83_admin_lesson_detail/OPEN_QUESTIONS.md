# Câu hỏi còn mở — API #83

Trạng thái tài liệu: Draft — Needs Confirmation. Các câu hỏi sau ảnh hưởng contract, data access hoặc triển khai.

1. **Dependencies trong AC-34:** Node n5 ghi “Đọc lesson + dependencies”. Cụ thể dependencies nào cần trả cho UI, field/count nào, và ở `Lesson`, `meta` hay response riêng? Nếu chỉ dùng trước delete, xác nhận API #86 tự kiểm tra quan hệ hiện tại.
2. **Active schema/live DB:** API dùng legacy BIGINT `lessons` hay V1-PILOT UUID/versioned lessons? Live schema và migration state chưa được xác minh.
3. **`course_id` nullability:** Legacy DDL cho phép NULL, reusable Lesson bắt buộc int64. Row NULL cần data correction, 500 hay contract/schema change?
4. **Fine-grained Admin authorization:** AC-34 yêu cầu lesson-management permission. Shared runtime guard xác thực role `ADMIN`; policy permission cụ thể và nguồn claim/scope vẫn chưa được định nghĩa.
5. **LessonStatus:** Các giá trị hợp lệ và casing là gì? DDL ghi default `DRAFT`, nhưng không có enum list chuẩn.
6. **Soft-delete visibility:** API #86 đề xuất soft-delete nhưng chưa có marker/schema được duyệt. Xác nhận #82 loại lesson đã xóa khỏi list, #83 trả 404 hay chi tiết, và #84/#85 từ chối hay xử lý mutation trên lesson đã xóa ra sao.

## Ranh giới proposal

- DIRECT: method/path, Bearer JWT, role Admin, required `lesson_id:int64`, `ApiEnvelope<Lesson>`, HTTP 200 và errors 401/403/404/500.
- DERIVED: lookup theo ID, no public `PUBLISHED` filter, absent row -> 404, malformed path -> 404, optional NULL serialization.
- SOURCE_REQUIRED: dependency output, live schema, nullability repair, fine-grained Admin permission, LessonStatus enum and soft-delete policy.

## Kết quả macro-review AC-34

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` — đã đối chiếu tài liệu #82–#86; đây không phải owner approval hoặc runtime verification.
- Dependency, delete-visibility và ranh giới API được ghi trong [báo cáo macro-review](../86_admin_lesson_delete/VERIFICATION_REPORT.md#ac-34-macro-review).
