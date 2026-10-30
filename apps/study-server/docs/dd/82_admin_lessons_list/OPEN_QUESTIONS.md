# Câu hỏi còn mở — API #82

Trạng thái tài liệu: Draft — Needs Confirmation. Runtime có fallback cục bộ nhưng các điểm dưới đây cần owner/schema authority trước khi coi contract được duyệt.

1. **Response cardinality:** Catalog #82 khai báo `ApiEnvelope<Lesson>`, còn endpoint/AC-34 thể hiện danh sách. Runtime trả `ApiEnvelope<Lesson[]>` theo fallback DERIVED; cần xác nhận catalog đổi sang array hay ý định thực sự là singleton.
2. **Pagination/result limit:** API không khai báo `page`, `size`, `sort` hay maximum rows. Runtime hiện trả toàn bộ kết quả khớp filter; cần chốt có phân trang/giới hạn hay không.
3. **`type` filter:** Legacy candidate không có type. Runtime trả 422 `DESIGN_VALIDATION_ERROR`/`UNSUPPORTED_FILTER` nếu query được gửi; cần xác nhận desired mapping/semantics hoặc bỏ query khỏi contract.
4. **Storage model/live schema:** Runtime query dùng legacy BIGINT `lessons` candidate. Live database/schema version chưa được xác nhận; V1-PILOT UUID schema không tương đương.
5. **Required projection nullability:** Legacy DDL cho phép `course_id`, `sort_order`, `status` NULL, còn reusable Lesson yêu cầu các giá trị này. Runtime trả 500 nếu row không map được; cần xác nhận dữ liệu/schema thực tế hoặc policy xử lý row.
6. **LessonStatus:** Danh sách giá trị và casing chưa đầy đủ. Runtime dùng exact string match, không whitelist.
7. **Ordering:** Runtime dùng `course_id ASC NULLS LAST, sort_order ASC NULLS LAST, id ASC`; default order chưa có trong catalog/diagram.
8. **Admin access policy:** Runtime shared guard yêu cầu role `ADMIN`; AC-34 nêu thêm lesson-management permission nhưng chưa có policy source/executable check.
9. **Deleted lesson visibility:** API #86 chưa chốt deletion marker/visibility. #82 không loại row theo deleted marker.

## Ranh giới contract

- DIRECT: method/path, Bearer JWT, role Admin, query field names/types, catalog singleton `ApiEnvelope<Lesson>`, HTTP 200 và lỗi 401/403/500.
- DERIVED/local fallback: array response, exact course/status filters, all-status default, empty array, stable order, 422 malformed `course`, 422 unsupported `type`.
- SOURCE_REQUIRED: live schema, fine-grained Admin permission, LessonStatus enum, pagination/result cap, deleted lesson visibility và việc sửa catalog cardinality.

## Kết quả macro-review AC-34

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` — đối chiếu tài liệu #82–#86; đây không phải owner approval hoặc runtime verification cho các API khác.
- API #82 list/reload runtime đã wired và test cục bộ; #83–#86 vẫn có trạng thái riêng trong báo cáo macro-review.
- Các ranh giới list/detail/update/status/delete tổng hợp tại [báo cáo macro-review](./VERIFICATION_REPORT.md#ac-34-macro-review).
