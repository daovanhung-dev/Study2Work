# Câu hỏi còn mở — API #70

Trạng thái tài liệu: Draft — Needs Confirmation. Không dùng các candidate dưới đây làm implementation contract trước khi chốt.

1. **Request body:** Body của PUT #70 gồm field nào? PUT là full replacement hay chỉ cập nhật field hiện có? Requiredness của `full_name`, `phone`, `avatar_url`, `role` là gì?
2. **Null/omission:** `phone` và `avatar_url` bị omit, null hoặc chuỗi rỗng thì giữ, xóa hay từ chối? Có normalize như API #14 không?
3. **Role policy:** Các UserRole hợp lệ và transition được phép là gì? Admin có thể gán mọi role hay cần permission riêng/step-up auth?
4. **Admin identity:** JWT claim/policy nào xác nhận Admin và quyền user management; có tenant/scope boundary không?
5. **Persistence:** API #70 dùng legacy BIGINT `users` hay schema V1-PILOT UUID? Live relation, columns và transaction boundary đã xác minh chưa?
6. **Validation:** Có dùng lại API #14 rules cho full_name/phone/avatar_url không? Rule và error detail nào thuộc 422?
7. **bio:** UserProfile có bio nhưng legacy users/API #14 query không persist. Có schema source được duyệt nào cung cấp bio không?
8. **Role token effect:** Sau khi đổi role, access/refresh sessions hiện có được revoke hoặc giữ đến expiry? AC-31 chỉ nhắc session revoke ở #71.
9. **Audit/PII:** Role/profile change cần audit event, actor, reason, masking hoặc field-level permission nào? Email/phone response policy là gì?
10. **Not-found/soft deletion:** User đã bị API #72 soft-delete/anonymize có trả 404 hay projection khác ở #70?
11. **Error envelope:** Lỗi dùng `data:null` theo guideline hay `{}` theo helper hiện tại? Cần sửa middleware allowlist/helper trước khi wire không?
12. **Kết quả macro-review AC-31:** Đã rà document-level nhóm #68–#72. Profile/role không overlap status/delete; role/session effects, PII/audit, deleted-user visibility và response projection vẫn cần owner quyết định; xem [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).

## Ranh giới proposal

- Candidate UPDATE trên legacy users và zero-row → 404 là DERIVED, không phải SQL/runtime hiện tại.
- Candidate body fields là DERIVED từ #70 intent/API #14; exact contract cần xác nhận.
- Không đổi catalog, diagram, schema hoặc runtime trong task này.
- Không coi API #68 list response discrepancy hoặc API #69 detail candidate là đã giải quyết bởi API #70.
