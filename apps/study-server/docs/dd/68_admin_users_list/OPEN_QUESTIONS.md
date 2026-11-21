# Câu hỏi còn mở — API #68

Trạng thái tài liệu: Draft — Needs Confirmation. Runtime đã được triển khai theo fallback DERIVED để hiện thực hóa flow list/pagination; các quyết định nghiệp vụ/schema dưới đây vẫn cần owner xác nhận trước khi coi contract là approved.

1. **Live schema và model được triển khai:** Runtime hiện đọc legacy BIGINT `users` theo checked-in DDL. Live schema chưa được kiểm tra; V1-PILOT UUID identity/profile model không tương thích trực tiếp. Xác nhận relation/column mapping thực tế trước deploy.
2. **Quyền Admin:** Runtime yêu cầu claim `ADMIN` bằng shared JWT guard trước DB access. DDL không có permission relation hoặc tenant boundary riêng. Xác nhận claim này đủ cho user management hay cần policy/scope khác.
3. **Role/status values:** Filter dùng exact match trên string lưu trong `users.role` và `users.status`; không whitelist enum vì source không liệt kê thành viên. Reusable `UserRole`/`UserStatus` enum cần danh sách giá trị chuẩn.
4. **PII và audit:** Response tái sử dụng projection API #04 gồm email/phone khi có; password hash không được query. Xác nhận quyền xem PII, logging/audit access và null-versus-omit policy.
5. **Visibility và lifecycle:** Legacy candidate không có `deleted_at`; không có deletion predicate. Xác nhận visibility của suspended/deleted/anonymized users và cách #71/#72 ảnh hưởng list/detail/session.

## Fallback đã dùng cho implementation

- `ApiEnvelope<Page<UserProfile>>` được đồng bộ vào catalog và AC-31 diagram để khớp bước lấy danh sách có pagination.
- `page` mặc định 1, fixed page size 20, `id ASC`; page ngoài int32 dương trả 422 `DESIGN_VALIDATION_ERROR`.
- `role`/`status` exact match; keyword trim/lowercase và literal substring trên `full_name` hoặc `email`.
- Các lựa chọn trên là DERIVED từ diagram, source pattern và API #07 precedent; không phải quyết định nghiệp vụ đã được owner duyệt.

Không có câu hỏi triển khai nào chặn local source/tests. Không có migration được thêm; live schema/deployment chưa xác minh.
