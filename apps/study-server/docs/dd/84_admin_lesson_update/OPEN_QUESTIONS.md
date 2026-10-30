# Câu hỏi còn mở — API #84

Trạng thái: Draft — Needs Confirmation. API đã wire bằng DERIVED fallback theo yêu cầu agent tự chọn cách đơn giản, dễ hiểu. Catalog và AC-34 diagram vẫn chỉ khai báo path; các fallback không được đổi thành direct/approved contract.

## Lựa chọn DERIVED đang chạy

1. `PUT` nhận full-replacement JSON với đủ `title`, `content`, `video_url`, `order`; field thừa bị từ chối.
2. `title` là strict string tối đa 200 ký tự; không trim và không cấm chuỗi rỗng.
3. `content` và `video_url` là required nullable string; null ghi SQL NULL. `video_url` không có URI/scheme/host validation.
4. `order` là strict signed int32; không thêm positivity, uniqueness hoặc reorder-sibling rule.
5. `lesson_id` sai/out-of-range trả 422 theo API PUT catalog; missing UPDATE row trả 404.
6. Một `UPDATE lessons ... RETURNING` sửa name/content/video_url/sort_order/updated_at; giữ nguyên course_id, status, created_at, uploads/resources/progress và audit.
7. View commit sau khi response Lesson hợp lệ; query/no-row/mapping/commit failure rollback.

## Còn cần xác minh ngoài fallback

1. **Canonical request contract:** Catalog/diagram chưa mô tả body. Runtime/OpenAPI expose fallback trên nhưng chưa có owner artifact xác nhận body, requiredness và null semantics.
2. **Schema đang chạy:** Legacy DDL dùng BIGINT `lessons`; V1-PILOT dùng UUID/versioned Lesson. Chưa truy cập live metadata/migration state để xác nhận endpoint nhắm schema nào.
3. **Admin policy:** Shared guard kiểm tra JWT role `ADMIN`. AC-34 nêu lesson-management permission nhưng Study source không có policy riêng; cần source/owner evidence nếu quyền đó phải được enforce riêng.
4. **Response nullability:** Legacy `lessons.course_id` nullable còn reusable `Lesson.course_id` bắt buộc. Row null sẽ rollback và trả 500 an toàn; không có fallback giả như `0`.
5. **Lesson status enum và deleted visibility:** #84 trả status unchanged. Danh sách status và policy row sau khi #86 đánh dấu/xóa chưa được thống nhất cross-API.
6. **Timestamp ownership:** `updated_at` được set theo legacy DDL và API #75 precedent; live DB trigger không được kiểm tra.

## Ranh giới nguồn

- DIRECT: method/path/auth role Admin/path int64/response/status/error code set theo catalog; UPDATE action và list reload theo AC-34.
- DERIVED: request schema, validation limits, legacy mapping, timestamp, 422 path behavior, no-row 404 và transaction behavior.
- SOURCE_REQUIRED: active schema/live policy, owner confirmation cho body, fine-grained permission, trigger và soft-delete visibility.

## Kết quả macro-review AC-34

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`; đây là review tài liệu và source cục bộ, không phải owner approval hay live DB verification.
- #84 chỉ cập nhật metadata; #85 giữ status/audit, #86 giữ deletion/reference policy, AC-34 reload dùng #82.
- Xem [báo cáo macro-review](../86_admin_lesson_delete/VERIFICATION_REPORT.md#ac-34-macro-review).
