# SH-02 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `SH-02-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Email/password, lỗi tại trường, nhớ route đích, tách thông báo 401 và tài khoản bị chặn.
- Gate/status (giữ nguyên): **R**; **BLOCK:** Role bootstrapping Mentor/Admin chưa hoàn chỉnh
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 8. Bảo mật và quyền riêng tư

- Chỉ gửi thông tin đăng nhập trong JSON qua HTTPS tới Study API đã cấu hình. Không có thông tin đăng nhập DB ở client.
- Không ghi log email/mật khẩu hay token. Không đặt thông tin đăng nhập/token vào query string, returnTo, analytics hoặc nội dung lỗi.
- Email không tồn tại và mật khẩu sai cố ý dùng cùng 401 chung theo nguồn hiện tại; giữ cách xử lý không tiết lộ tài khoản.
- máy chủ hiện chỉ lưu HMAC hash của refresh token nhưng trả access/refresh token thô trong JSON. Chính sách lưu client, thời hạn, xoay token và đăng xuất còn chưa chốt; DD không giả định nơi lưu trong trình duyệt.
- Không gọi API #04 dành cho học viên cho người hướng dẫn/quản trị viên; vai trò trong token không chứng minh phía giao diện có route tương ứng.
- Không để lộ password_hash, chi tiết ngoại lệ DB/nhà cung cấp hoặc trường khác từ dòng người dùng. Phần dữ liệu an toàn #03/#04 không có password hash; #04 cũng không có permissions/bio.

### Trích từ DD nguồn: 10. Quyết định còn mở và bàn giao

| Mã | Quyết định / điều kiện chặn | Chủ sở hữu | Cho tới khi giải quyết |
|---|---|---|---|
| SH02-D01 | API #03 chuẩn 201/chỉ hồ sơ/422+500 khác AC/nguồn 200/hồ sơ+token/401/403/500 | BA / máy chủ | Giữ rõ sai khác; không sinh response pha trộn |
| SH02-D02 | Lưu token an toàn phía client, phối hợp xoay, dọn phiên/đăng xuất và chính sách thử lại đăng nhập không rõ kết quả | Security / Sản phẩm / máy chủ / Frontend | Không tự giả định lưu trữ hay bộ chặn refresh |
| SH02-D03 | G-02: khởi tạo hồ sơ người hướng dẫn/quản trị viên và nguồn permissions | Auth / Sản phẩm / máy chủ | Hiện tại chỉ gọi #04 cho vai trò học viên |
| SH02-D04 | Allowlist returnTo an toàn và route học viên mặc định | Sản phẩm / Frontend | Chỉ dùng route tương đối đề xuất; không mở chuyển hướng |
| SH02-D05 | Mục đích gọi #04 sau khi #03 đã trả hồ sơ; nguồn có thẩm quyền cho vai trò/hồ sơ/permissions | BA / máy chủ | Theo danh mục chỉ với học viên sau khi duyệt chính sách phiên |
| SH02-D06 | PNG nguồn trống: thay tài sản hay chấp nhận bản dựng HTML làm mốc giao diện | Quản lý tài sản screen-stitch | Giữ ảnh gốc trống; ghi nguồn gốc ảnh dựng |
| SH02-D07 | Thiếu các hàm handleLoginSubmit / togglePasswordVisibility trong bản mẫu | Frontend / Design | Chưa xác minh tương tác UI nào |
| SH02-D08 | Editable Study Web source/package manifest/feature route chưa có; context entry/index hiện đã được xác minh và đăng ký | Frontend | Không tuyên bố route hoặc runtime đã được nối |
| SH02-D09 | #04 dùng cùng HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED` cho auth/claim không hợp lệ và profile thiếu; xác nhận response discriminator hoặc policy refresh mọi #04/401 | API/Auth / Security / Product | Không tự động gọi R-X01 hoặc xóa phiên khi chưa có policy; giữ trạng thái lỗi chưa phân loại |

**Điều kiện hoàn tất phiên tài liệu:** có kế hoạch SH-02, DD, bản xem sạch dựng từ HTML hiện tại, ảnh chú thích, bản đồ marker 1–8 khớp, liên kết đã kiểm tra và hash nguồn không đổi. DD vẫn BLOCKED; không coi các điều kiện API/phiên/vai trò còn mở là sẵn sàng triển khai.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
