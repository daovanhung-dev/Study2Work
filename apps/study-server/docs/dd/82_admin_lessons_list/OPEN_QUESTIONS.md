# Câu hỏi còn mở — API #82

Trạng thái tài liệu: Draft — Needs Confirmation. Các câu hỏi này ảnh hưởng contract, query semantics hoặc khả năng triển khai.

1. **Response cardinality:** Catalog #82 khai báo `ApiEnvelope<Lesson>` nhưng endpoint name và AC-34 mô tả danh sách. Có đổi reusable response thành `ApiEnvelope<Lesson[]>` không? Nếu đúng danh sách, empty result có trả `data: []` không?
2. **Pagination/result limit:** API không khai báo `page`, `size`, `sort` hay maximum rows. Admin list cần giới hạn/ phân trang ở đâu? Không tự thêm query fields trong DD này.
3. **`type` filter:** Lesson được phân loại type bằng field/relation nào, các giá trị hợp lệ là gì, và predicate chính xác ra sao? Reusable Lesson và hai schema artifacts đã kiểm tra không có Lesson `type` tương thích.
4. **Storage model/live schema:** API dùng legacy BIGINT `lessons` hay V1-PILOT UUID lesson/chapter/course-version model? Live database/schema version chưa được xác nhận.
5. **`course_id` nullability:** Legacy DDL cho phép NULL nhưng reusable Lesson bắt buộc int64. Row NULL phải được sửa dữ liệu, loại khỏi kết quả hay gây lỗi? DD không tự chọn.
6. **Course/status filter behavior:** Xác nhận exact-match semantics; khi query vắng mặt có bỏ predicate để Admin xem mọi course/status không?
7. **LessonStatus:** Danh sách giá trị, casing và quy tắc nhận status filter là gì? Không tạo whitelist từ `DRAFT`/`PUBLISHED` của các nguồn không đồng nhất.
8. **Ordering:** Có chấp nhận `course_id ASC, sort_order ASC, id ASC` làm thứ tự mặc định ổn định không?
9. **Admin access policy:** JWT Admin claim, lesson-management permission, policy source và cách phân biệt 401/403 được triển khai ở đâu? Study source hiện chỉ có Student auth helper.
10. **Malformed query errors:** Catalog chỉ liệt kê 401/403/500; parse lỗi int64 thường cần validation response nhưng chưa có status/code được contract khai báo. Cần quyết định cách giữ catalog/error middleware nhất quán.
11. **Envelope error data:** API guideline quy định `data:null`, trong khi helper hiện tại mặc định `{}` khi thiếu data. Chuẩn nào áp dụng khi thêm route Admin?
12. **Deleted lesson visibility:** Nếu policy #86 chọn soft-delete, marker nào biểu thị lesson đã xóa và API #82 có loại lesson đó khỏi danh sách không? Schema hiện chưa có marker tương thích; không tự thêm filter.

## Ranh giới proposal

- DIRECT: method/path, Bearer JWT, role Admin, query field names/types, declared `ApiEnvelope<Lesson>`, HTTP 200, và lỗi 401/403/500.
- DERIVED: equality filters, all-status khi vắng filter, collection response proposal, empty array và default ordering.
- SOURCE_REQUIRED: `type`, active schema/live DB, Admin policy implementation, LessonStatus enum, malformed-query mapping và error envelope integration.

## Kết quả macro-review AC-34

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` — đã đối chiếu tài liệu #82–#86; đây không phải owner approval hoặc runtime verification.
- Các điểm còn mở và ranh giới list/detail/update/status/delete được tổng hợp trong [báo cáo macro-review](./VERIFICATION_REPORT.md#ac-34-macro-review).
