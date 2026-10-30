# Câu hỏi còn mở — API #70

Trạng thái tài liệu: Draft — Needs Confirmation. Runtime sử dụng các fallback `DERIVED` dưới đây; chúng chưa trở thành contract được owner duyệt.

1. **Body contract:** Catalog/diagram chỉ liệt kê path. Có chấp nhận full-replacement body bắt buộc `full_name`, `phone`, `avatar_url`, `role` như OpenAPI hiện tại không?
2. **Role policy:** Runtime cho phép `STUDENT`, `MENTOR`, `ADMIN` dựa trên role labels hiện có. Role transitions nào được phép; Admin có thể tự đổi role hoặc tạo Admin khác không?
3. **Admin permission:** Có cần permission relation, tenant boundary, MFA/step-up hoặc account-status lookup ngoài JWT claim `ADMIN` đang dùng không?
4. **Token effect:** Role change hiện không revoke session; access JWT tiếp tục dùng role claim đến expiry. Có yêu cầu vô hiệu hóa access/refresh token ngay không, và cơ chế nào được duyệt?
5. **Persistence:** Runtime dùng checked-in legacy BIGINT `users`; live relation, grants, column types và deployment chưa xác minh. V1-PILOT UUID model không được nối ngầm.
6. **Profile contract:** Runtime dùng API #14 normalization, required nullable keys cho phone/avatar, không kiểm tra URL syntax, và omit `bio`. Có profile/schema source khác hoặc null/URL rule chính thức không?
7. **PII/audit:** Email/phone được trả trong `UserProfile` sau ADMIN claim. Có cần masking, audit actor/reason, event hoặc field-level permission không?
8. **Lifecycle visibility:** Runtime không lọc `status` và legacy source không có `deleted_at`; suspended/deleted/anonymized target vẫn có thể được cập nhật nếu row còn tồn tại. #71/#72 behavior nào phải áp dụng?
9. **AC-31 macro-review:** Document-level review #68–#72 đã hoàn tất; role/session, PII/audit, deleted-user visibility và Admin policy gaps vẫn cần owner quyết định. Xem [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).

## Fallback đã dùng cho local implementation

- Shared `validate_current_user_request(..., role="ADMIN")` trước path parsing và DB access.
- PUT full-replacement với đúng bốn keys; extra keys bị từ chối. Full name/phone/avatar reuse API #14 rules; role allowlist là `STUDENT`, `MENTOR`, `ADMIN`.
- Signed-int64 path sai/out-of-range trả 422; hợp lệ nhưng không có row trả 404.
- Một UPDATE bound trên legacy `users`, giữ email/status/created_at, cập nhật profile/role/updated_at, trả safe `UserProfile`; không audit/revoke session.
- Mọi fallback trên là DERIVED từ diagram intent, legacy DDL và current Study source; không chứng minh schema/deployment hoặc policy approval.
