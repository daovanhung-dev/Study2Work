# SH-03 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `SH-03-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Nhập tên/email/password và xác nhận điều khoản nếu có contract; không tự thêm CAPTCHA/OTP.
- Gate/status (giữ nguyên): **R**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 7. Bảo mật, quyền riêng tư và vòng đời tài khoản

- Giao diện công khai không đồng nghĩa với việc tin dữ liệu phía trình duyệt; API #01 xác thực kiểu/định dạng và tự đặt vai trò `STUDENT`.
- Mật khẩu chỉ truyền trong phần thân HTTPS khi cấu hình môi trường thật, không ghi vào log, URL, dữ liệu phân tích, mã truy vết, thông báo lỗi hoặc trạng thái điều hướng.
- Không lưu token vì API #01 không cấp token. Không gửi `role`, `status`, `password_hash` hoặc trường không có trong hợp đồng yêu cầu.
- API #01 kiểm tra email trùng rồi dựa thêm vào ràng buộc duy nhất; tranh chấp lúc ghi được trả thành HTTP 409. Lớp điều phối sở hữu `commit`/`rollback`.
- API #02 không xác thực quyền sở hữu email và bộ gửi thư mặc định không gửi thư. Tệp `DB.sql` gợi ý trạng thái mặc định `ACTIVE`, còn API #03 cho phép đăng nhập tài khoản `ACTIVE`. Trước khi coi luồng email là biện pháp xác minh, nhóm Sản phẩm/Bảo mật/Máy chủ cần quyết định cách tạo tài khoản chưa xác minh và xác nhận trạng thái lược đồ thực tế.
- Không đưa `user_id` hoặc email vào URL. SH-03→SH-04 cần kênh bàn giao tạm và quy tắc thời hạn/khôi phục được duyệt; hiện chưa có client source hoặc quyết định lưu trữ để xác nhận cơ chế đó.

### Trích từ DD nguồn: 10. Điểm cần quyết định trước khi phát hành

1. Có cần mật khẩu tối thiểu 8 ký tự không? Nếu có, cập nhật hợp đồng/API trước khi dùng lỗi trong HTML; hiện API #01 chưa kiểm tra mức đó.
2. Tài khoản mới có được đăng nhập trước xác minh email không? SQL API #01 không gán `status`, tệp DDL chỉ là tài liệu tham khảo và API #02 chưa có tác động xác minh.
3. Cơ chế điều hướng nào giữ `data.id`/`data.email` tạm tới SH-04, kể cả trường hợp tải lại trực tiếp trang SH-04?
4. Đội sản phẩm chấp nhận thông báo “đã tiếp nhận yêu cầu” từ bộ giả lập ở SH-04 hay cần chặn/ẩn thao tác gửi email cho tới khi bộ gửi thư thật sẵn sàng?
5. Có cần sửa HTML mẫu để bỏ trình mô phỏng lỗi không hoạt động, câu mật khẩu 8 ký tự và các tham chiếu phần tử kiểm tra chất lượng không tồn tại?
6. Cần xác nhận phông chữ triển khai theo hướng dẫn Study (Inter/phông chữ hệ thống), không theo liên kết Google Fonts trong HTML mẫu.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
