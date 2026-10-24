# Câu hỏi còn mở — API #68

Trạng thái tài liệu: Draft — Needs Confirmation. Câu hỏi dưới đây cần được chốt trước khi biến proposal thành implementation contract.

1. **Cardinality của response:** Catalog và diagram ghi ApiEnvelope<UserProfile>, còn AC-31/step backend yêu cầu danh sách và pagination. Có sửa catalog đồng bộ sang ApiEnvelope<Page<UserProfile>> không?
2. **Pagination:** Nếu đổi response sang Page<UserProfile>, page có bắt đầu từ 1 không, page size cố định 20 hay cần thêm query size? Page<=0 và page vượt total được xử lý thế nào?
3. **Validation error:** Catalog #68 không liệt kê HTTP 422. Nếu page hoặc filter không hợp lệ, có cập nhật error set/biz code trước implementation không?
4. **Filter:** role và status có so sánh exact match không; giá trị hợp lệ nào được hỗ trợ; keyword tìm full_name, email hay cả hai; có trim, không phân biệt hoa thường và escape wildcard không?
5. **Admin authorization:** JWT role Admin được xác thực bằng claim/policy nào; quyền user management có phải permission riêng; có Admin scope hoặc tenant boundary không?
6. **Nguồn dữ liệu:** Chọn legacy BIGINT users hay V1-PILOT UUID identity/profile/role model? Live schema hiện chưa được xác minh.
7. **UserProfile enum và bio:** Reusable schema dùng UserRole/UserStatus nhưng không liệt kê enum members; current API #4 model dùng string. Bio? cũng chưa có source trong legacy users/API #4. Có định nghĩa enum, thêm source-backed bio hay điều chỉnh reusable schema?
8. **Null và PII:** avatar_url/phone có trả null hay omit; email/phone có được hiển thị cho mọi Admin; có access audit/logging policy không?
9. **Deletion/status visibility:** Khi không truyền status, có bao gồm suspended, deletion-pending hoặc anonymized users không? API #71/#72 có thể đổi trạng thái hoặc xóa/ẩn user.
10. **Kết quả macro-review AC-31:** Đã rà document-level nhóm #68–#72. List/pagination mismatch, deleted-user visibility, projection/PII/audit và status/session effects vẫn cần owner quyết định; xem kết quả trong [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).

## Ranh giới proposal

- Candidate Page<UserProfile>, default page 1, size 20, exact role/status, keyword trên full_name/email và order id ASC đều là DERIVED.
- Các proposal không thay đổi catalog, diagram, schema hoặc runtime.
- Macro-review document-level đã hoàn tất sau khi tạo DD #72; các contract/schema/security gaps vẫn mở.
