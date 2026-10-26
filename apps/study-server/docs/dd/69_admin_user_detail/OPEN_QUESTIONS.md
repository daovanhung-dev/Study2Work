# Câu hỏi còn mở — API #69

Trạng thái tài liệu: Draft — Needs Confirmation. Route local đã được triển khai theo fallback DERIVED; các câu hỏi dưới đây cần owner/schema confirmation trước khi xem là contract đã phê duyệt hoặc triển khai live.

1. **Live schema:** Runtime hiện đọc checked-in legacy BIGINT `users`. Xác nhận relation/column mapping và quyền truy cập trên live DB; V1-PILOT UUID identity/profile không được nối ngầm.
2. **Admin policy:** Runtime yêu cầu claim `ADMIN`, theo cùng fallback API #68. Xác nhận có cần permission relation riêng, tenant boundary, MFA hoặc policy bổ sung không.
3. **Profile contract:** Runtime reuse API #04 `UserProfile`, trả avatar/phone null và omit bio vì không có source. Xác nhận omission/null behavior cho các role/profile types khác nhau.
4. **Enum members:** Catalog dùng `UserRole`/`UserStatus` nhưng không liệt kê member; runtime trả nguyên string lưu trong candidate. Cần danh sách enum chuẩn nếu client phải validate.
5. **PII/audit:** Email/phone được trả sau ADMIN guard. Xác nhận masking, audit event, reason logging hoặc giới hạn Admin nào được xem.
6. **Lifecycle visibility:** Runtime không lọc status hoặc `deleted_at`; legacy candidate không có deletion column. Xác nhận #71/#72 cần làm detail 404, trả anonymized profile hay hành vi khác.
7. **Deployment:** Migration không được thêm; fake-session tests không xác minh live metadata, grants hoặc deployment.

## Fallback đã dùng cho local implementation

- Shared `validate_current_user_request(..., role="ADMIN")` chạy trước path parsing và DB query; claim-to-user-management mapping là DERIVED theo API #68.
- Raw path parse signed int64; malformed/out-of-range và no-row cùng trả 404 `DESIGN_RESOURCE_NOT_FOUND` để giữ catalog error set, không thêm 422.
- Query safe projection từ legacy `users.id`; API #04 model serialize nullable avatar/phone thành null, omit unsupported bio, không select `password_hash`.
- Các fallback trên không chứng minh live schema hoặc quyền Admin đã được phê duyệt.
