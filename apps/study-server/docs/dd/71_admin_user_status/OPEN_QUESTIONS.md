# Câu hỏi còn mở — API #71

Trạng thái tài liệu: Draft — Needs Confirmation. Runtime đã triển khai các fallback DERIVED bên dưới để giữ API #71 hoạt động theo contract hiện có; các lựa chọn này chưa được owner phê duyệt và không trở thành canonical contract chỉ vì đã có code.

1. **Request body:** API #71 nhận `body{status:UserStatus!}` hay một shape khác? Body required và PATCH có semantics set-target-state như candidate không?
2. **Status enum:** `UserStatus` gồm những giá trị nào? Có thể chốt `ACTIVE` để mở và `SUSPENDED` để khóa không? V1-PILOT enum có được phép làm nguồn cho legacy Study không?
3. **Persistence:** Endpoint chạy trên legacy BIGINT `users.status` hay UUID V1-PILOT `identity_projections.account_status`? Live schema và migration nào đã được xác minh?
4. **Admin policy:** JWT claim/policy nào xác nhận Admin và quyền user management; có tenant/scope/MFA boundary không?
5. **Session revoke:** “Revoke session nếu cần” trong AC-31 có bắt buộc khi chuyển sang SUSPENDED không? Revoke mọi refresh tokens, token chưa hết hạn, hay chỉ session đang hoạt động?
6. **Access JWT:** Current Study access-token guard không đọc account status/revocation. Có cần vô hiệu hóa access JWT ngay hay chấp nhận đến expiry? Nếu immediate, token version/denylist/introspection mechanism nào được phê duyệt?
7. **Unlock semantics:** Khi chuyển SUSPENDED → ACTIVE, user có phải login lại không? Candidate giữ nguyên refresh tokens đã revoked và không phục hồi chúng.
8. **Idempotency/no-op:** Gửi status hiện tại có trả 200 success không; có đổi `updated_at` hoặc revoke token thêm lần nữa không?
9. **Self/last Admin:** Admin có được khóa chính mình hoặc Admin cuối cùng không? Chưa có business rule nguồn.
10. **Validation/error envelope:** Invalid status/malformed path map cụ thể ra 422 thế nào? Error `data` là null theo guideline hay `{}` theo current helper?
11. **Soft-delete boundary:** User đã xóa/ẩn danh theo #72 có được #71 mở khóa không, hay phải trả 404/validation? Macro-review xác nhận đây vẫn là policy gap cần owner chốt.
12. **Kết quả macro-review AC-31:** Đã rà document-level nhóm #68–#72. ACTIVE/SUSPENDED và conditional refresh-token revoke vẫn tách khỏi lifecycle delete; access-token, visibility, PII/audit và error gaps còn mở; xem [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).

## Ranh giới proposal

- `ACTIVE`/`SUSPENDED`, body `{status}`, user status UPDATE và revoke refresh-token rows khi khóa là `DERIVED` candidates.
- Candidate refresh-token revoke không có nghĩa access JWT hiện hữu bị vô hiệu ngay.
- Catalog, diagram và schema không được đổi để hợp thức hóa các fallback. Runtime hiện tại được mô tả riêng trong DD; owner cần xác nhận hoặc thay đổi các quyết định DERIVED qua một task có contract rõ ràng.
- AC-31 macro-review document-level đã hoàn tất sau khi API #72 DD được tạo; các policy questions chưa được giải quyết.
