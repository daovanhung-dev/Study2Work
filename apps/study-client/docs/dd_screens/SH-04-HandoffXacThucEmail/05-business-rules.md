# SH-04 — Business Rules

> **Current source (2026-11-20):** The implementation uses a user-initiated trigger and one-use in-memory handoff as a conservative client choice; this does not resolve the product-level dispatch-owner/feature-gate question. It never retries automatically. UI wording must distinguish the stub's accepted response from email delivery and account verification. No OTP/confirmation flow exists.

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `SH-04-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Hiển thị trạng thái yêu cầu gửi email; chưa có API xác nhận OTP/link.
- Gate/status (giữ nguyên): **S**; email delivery and account verification remain **BLOCKED** because the provider is a stub and no confirm endpoint exists. The #02 caller itself is source-wired.
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 9. Bảo mật, riêng tư và điều kiện tích hợp

- API #02 được gọi công khai và không dùng phiên cơ sở dữ liệu; không cần gửi Bearer token.
- Địa chỉ thư điện tử và `user_id` được gửi qua phần thân JSON theo hợp đồng; không đưa vào URL hoặc lệnh cURL gắn cứng trong tài liệu công khai.
- API #02 là public và không có DB ownership check; abuse control/rate limit còn mở trong API DD. Không tự thêm auth, rate limit hoặc chống lạm dụng khác vào hành vi hiện tại.
- Bộ gửi thư hiện tại bỏ dữ liệu đầu vào. Không ghi nội dung rằng thông tin đã được xếp hàng, gửi ra dịch vụ ngoài hay lưu lại.
- Không tạo/lưu token xác minh phía trình duyệt; API hiện tại không tạo token hoặc `confirm_url`.
- Không đặt `user_id`, địa chỉ thư điện tử hoặc `traceId` trong nhật ký hiển thị cho người dùng. Nếu nhóm sản phẩm cần che một phần địa chỉ, phải duyệt định dạng trước khi triển khai.
- Mẫu lệnh sao chép trong HTML đang sai điểm cuối API và thiếu trường bắt buộc; bỏ khỏi giao diện người dùng hoặc sửa theo hợp đồng được duyệt trước khi sử dụng.
- API #02 không kiểm tra `user_id` có khớp địa chỉ thư điện tử. Không dùng phản hồi 202 để kết luận người dùng đã chứng minh quyền sở hữu địa chỉ.

### Trích từ DD nguồn: 12. Điểm cần quyết định trước khi triển khai

1. Product owner must approve whether the current explicit-click trigger and in-memory handoff satisfy F01; current source uses these as conservative UI choices, not as an approved product rule.
2. Confirm whether losing the handoff on refresh/direct entry is acceptable; current source fails closed and sends no request in those cases.
3. Nhóm sản phẩm có chấp nhận màn hình chỉ thông báo bộ gửi thư giả lập đã tiếp nhận, hay cần ẩn thao tác gọi API tới khi dịch vụ gửi thư thật sẵn sàng?
4. Cần triển khai dịch vụ gửi thư thật và điểm cuối xác nhận OTP/liên kết nào trước khi gọi đây là luồng xác minh thư điện tử hoàn chỉnh?
5. Có nên loại thẻ trạng thái kỹ thuật, bộ chọn giả lập và nút sao chép lệnh khỏi giao diện Khách? Bản mẫu hiện trình bày dữ liệu nội bộ không khớp phản hồi thật.
6. Cần thống nhất token của `DESIGN.md` với hướng dẫn Study trước khi tái sử dụng màu/phông chữ trong giao diện triển khai.
7. Chốt miền int64 của user_id và semantics/allowlist cho ActionResult.status, reason trước khi client map response.
8. Chốt điều kiện bật verification, public abuse control và cách xử lý khi provider nhận status chưa biết.
9. API #01 bỏ qua status, checked-in DDL default ACTIVE, API #03 đòi ACTIVE: cần chốt live schema và quy tắc nào gắn email verification với trạng thái tài khoản; không kết luận người chưa xác minh được login hay không.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
