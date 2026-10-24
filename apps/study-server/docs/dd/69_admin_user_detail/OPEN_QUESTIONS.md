# Câu hỏi còn mở — API #69

Trạng thái tài liệu: Draft — Needs Confirmation. Chốt các câu hỏi dưới đây trước khi dùng proposal làm implementation contract.

1. **Admin authorization:** JWT role Admin được kiểm tra qua claim/policy nào; quyền user management có permission riêng, tenant boundary hoặc MFA requirement không?
2. **Nguồn dữ liệu:** Chọn legacy BIGINT users hay mô hình UUID V1-PILOT; live schema và quyền truy cập relation nào đã được xác nhận?
3. **UserProfile.bio:** Field optional này có cần trả không; nếu cần, nguồn nào ánh xạ từ int64 user sang learner_profiles UUID mà không ghép danh tính sai?
4. **Enums:** Các member hợp lệ của UserRole và UserStatus là gì; giá trị lưu hiện tại được validate hay trả nguyên trạng?
5. **Optional fields:** avatar_url và phone được trả null hay omit; omission của bio có được chấp nhận cho mọi user role?
6. **PII and audit:** Admin nào được xem email/phone; cần audit event, masking hoặc reason nào khi đọc hồ sơ?
7. **Not-found semantics:** User không tồn tại trả 404 như candidate; user đã soft-delete/anonymize theo API #72 trả 404 hay projection khác?
8. **Path validation:** user_id âm, overflow hoặc malformed được xử lý thế nào khi catalog không có HTTP 422?
9. **Error envelope:** Chuẩn lỗi phải giữ data:null hay theo current helper data:{}; cần đồng bộ helper/guideline ra sao trước khi wire?
10. **Kết quả macro-review AC-31:** Đã rà document-level nhóm #68–#72. Visibility của user đã xóa/ẩn danh, projection/PII/audit, Admin policy và error consistency vẫn cần owner quyết định; xem [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).

## Ranh giới proposal

- Q1 SELECT từ legacy users và nhánh không có row → 404 là candidate DERIVED.
- Không đổi catalog, diagram, schema hoặc runtime trong task này.
- Không coi API #68 list response discrepancy là đã giải quyết bởi API #69 detail response.
