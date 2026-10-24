# Câu hỏi còn mở — API #72

Trạng thái tài liệu: Draft — Needs Confirmation. Các điểm dưới đây cần được chốt trước implementation.

1. **Delete policy:** API chọn soft-delete hay anonymization? Điều kiện áp dụng cho từng loại user và field PII nào được giữ/ẩn?
2. **Persistence:** Policy lưu trạng thái và thời điểm xóa ở relation/column nào? `DeleteResult.deleted_at` lấy từ timestamp nguồn nào?
3. **Dependency checks:** Những quan hệ nào phải kiểm tra; quan hệ nào chặn, được bảo tồn hoặc cần anonymization? Legacy FK list chỉ là DDL artifact.
4. **Blocked mapping:** Nếu policy không cho phép thao tác, dùng 422 `DESIGN_VALIDATION_ERROR` như thế nào; có error detail/reason nào đã được duyệt?
5. **Idempotency/visibility:** User đã soft-delete/anonymized gọi DELETE lần nữa trả success, 404 hay kết quả khác? `deleted_at` gốc có giữ không?
6. **Admin policy:** JWT role/permission claim, tenant/scope boundary, self-delete hoặc last-Admin safeguards nào áp dụng?
7. **Group read behavior:** Sau #72, #68 list và #69 detail có ẩn target, trả profile đã anonymize hay cách khác? #68 response cardinality mismatch vẫn cần giải quyết riêng.
8. **#70/#71 boundary:** PUT #70 hoặc PATCH status #71 với user đã xóa/ẩn danh trả thế nào; có trạng thái lifecycle được phép hay không?
9. **Retention and audit:** Payments, enrollments, progress, submissions, discussions và notifications cần giữ bao lâu; cần audit actor/reason hay event không?
10. **Transaction:** Dependency check và mutation cần cùng transaction/isolation nào; policy có external provider hoặc nhiều store không?
11. **Admin auth/runtime:** Admin guard chưa có trong Study; middleware contract path và error data null-vs-empty phải được đồng bộ trước wiring.
12. **AC-31 macro-review:** Document-level review #68–#72 đã hoàn thành. Các gap trên vẫn cần owner quyết định; xem [PLAN_RESULT.md](./PLAN_RESULT.md) và các open questions của [#68](../68_admin_users_list/OPEN_QUESTIONS.md), [#69](../69_admin_user_detail/OPEN_QUESTIONS.md), [#70](../70_admin_user_update/OPEN_QUESTIONS.md), [#71](../71_admin_user_status/OPEN_QUESTIONS.md).

## Ranh giới proposal

- Không hard-delete hoặc cascade được suy ra từ HTTP method hay legacy FK artifact.
- `deleted_at` là field trực tiếp của DeleteResult nhưng physical source chưa được xác định.
- Không đổi catalog, diagram, schema hoặc runtime trong task tạo DD.
