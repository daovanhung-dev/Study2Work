# SH-04 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [SH-04_markers.json](../../screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/SH-04_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `SH-04-EL-001` | `SH04-EL-01` | Mã SH-04 và đường dẫn đề xuất |
| #2 | `SH-04-EL-002` | `SH04-EL-02` | Các trạng thái mô phỏng trong bản mẫu (QA-only) |
| #3 | `SH-04-EL-003` | `SH04-EL-03` | Biểu tượng và nhãn phản hồi API |
| #4 | `SH-04-EL-004` | `SH04-EL-04` | Tiêu đề và phần giải thích kết quả |
| #5 | `SH-04-EL-005` | `SH04-EL-05` | Giới hạn xác minh: chưa có OTP/link/endpoint |
| #6 | `SH-04-EL-006` | `SH04-EL-06` | Điều hướng quay lại SH-02 |
| #7 | `SH-04-EL-007` | `SH04-EL-07` | Nút sao chép lệnh mẫu không đúng hợp đồng |
| #8 | `SH-04-EL-008` | `SH04-EL-08` | Thẻ tham chiếu hợp đồng API #02 |
| #9 | `SH-04-EL-009` | `SH04-EL-09` | Các hàng trạng thái giao thức và xác minh |
| #10 | `SH-04-EL-010` | `SH04-EL-10` | Khung JSON mock, không phải response API |
| #11 | `SH-04-EL-011` | `SH04-EL-11` | Ghi chú quy tắc thiết kế/WCAG chưa kiểm định |
| #12 | `SH-04-EL-012` | `SH04-EL-12` | Chân trang mã màn hình và đường dẫn |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 4. Bản đồ phần tử và dữ liệu trên màn hình

Ảnh nguồn có hai cột trên màn hình rộng: thẻ thông báo chính bên trái; thẻ thông tin API bên phải; ghi chú thiết kế ở dưới cột phải; chân trang chạy hết chiều ngang. HTML dùng một cột dưới mốc Tailwind `lg` và bố cục 7/12 + 5/12 từ mốc này trở lên. Giữ thứ tự đọc: ngữ cảnh trang → thông báo → giới hạn xác minh → điều hướng → chi tiết kỹ thuật.

| # / Element ID | Tên, loại và nội dung | Nguồn/điều kiện hiển thị | Trạng thái | Event / kết quả |
|---|---|---|---|---|
| 1 / `SH04-EL-01` | Mã SH-04 và route đề xuất · nhãn tĩnh. | Nội dung thiết kế; `/register/verification` chưa có router; hiển thị trang. | Default. | `SH04-EV-01`; không tự tạo link/API. |
| 2 / `SH04-EL-02` | Bộ chọn `Accepted / Stub Spec / No-Delivery / Error Handshake` · QA controls trong mock. | HTML/JavaScript cục bộ; không phải trạng thái API. Loại khỏi giao diện Khách. | Chỉ tồn tại trong mock; không có product state. | `SH04-EV-08`; không gọi API. |
| 3 / `SH04-EL-03` | Biểu tượng thư và nhãn phản hồi · trạng thái. | Dữ liệu state từ response; chỉ render `accepted` khi HTTP 202, business code đúng và `data.status="accepted"`. | Pending, accepted, validation error, provider error, unmapped, network unknown. | `SH04-EV-03..06, SH04-EV-09`; 202 không chứng minh delivery/verification. |
| 4 / `SH04-EL-04` | Tiêu đề và giải thích kết quả · heading/status text. | Nội dung đích theo API response; không hiển thị “đã vào hàng đợi”. Không hiển thị `reason` provider cho người dùng trước khi semantics được duyệt. | Pending, accepted, error, unmapped. | `SH04-EV-03..06, SH04-EV-09`; nói rõ email chưa gửi thật. |
| 5 / `SH04-EL-05` | Khung giới hạn xác minh · informational notice. | Nội dung tĩnh theo catalog/source: chưa có OTP, link hoặc confirm endpoint. | Visible; không điều khiển. | `SH04-EV-01`; không tạo OTP/input/countdown. |
| 6 / `SH04-EL-06` | Quay lại đăng nhập · anchor. | `href="/login"` trong HTML; SH-02 route đề xuất, runtime chưa xác nhận. | Default/focus. | `SH04-EV-07`; điều hướng, không gọi API. |
| 7 / `SH04-EL-07` | Copy Test cURL · button trong mock. | JavaScript dựng URL ngoài thiếu `/api/v1` và body thiếu `user_id`; không đưa vào product UI. | Chỉ mock; không dùng được. | `SH04-EV-08`; không copy/gửi lệnh. |
| 8 / `SH04-EL-08` | Thẻ tham chiếu hợp đồng API #02 · heading/card. | Nhãn tĩnh; không khẳng định telemetry live. | Visible. | `SH04-EV-01`; không có API riêng. |
| 9 / `SH04-EL-09` | Các hàng HTTP/delivery/auth/confirmation · status summary. | HTTP/body đã parse; delivery/verify chưa có nguồn phản hồi riêng; provider status ngoài `accepted` chưa có semantics. | Pending/accepted/error/unmapped/network unknown. | `SH04-EV-03..06, SH04-EV-09`; không hiển thị mock 200/503 như server response. |
| 10 / `SH04-EL-10` | JSON block · preformatted mock payload. | HTML hard-code `contract`, `delivery`, `artifacts`, `otp_generated`, `confirm_url`; các field này không có trong API response. Ẩn khỏi product UI. | Chỉ mock; không trình bày như response. | `SH04-EV-08`; ví dụ contract thực ở §6.2. |
| 11 / `SH04-EL-11` | Design rule card và nhãn `PASS WCAG AA`. | Ghi chú tĩnh; nhãn không có báo cáo kiểm định hỗ trợ. Bỏ tuyên bố đạt chuẩn khi triển khai. | Visible trong mẫu; chưa xác minh. | `SH04-EV-01`; không tương tác. |
| 12 / `SH04-EL-12` | Chân trang mã màn hình/route/protocol/auth label. | Nội dung HTML tĩnh; `Engineering Verification Protocol v2.4`/`Stub S-02` không phải trạng thái runtime đã xác nhận. | Default. | `SH04-EV-01`; không điều hướng/xác thực. |

Không có trường nhập liệu nào trên SH-04. Tên trường `user_id` và `email` chỉ là dữ liệu yêu cầu API, không phải ô để Khách tự sửa trên trang này. Marker JSON ghi tọa độ theo ảnh gốc 1600×1280 với gốc trên-trái và pixel; Element ID `SH04-EL-01..12` ánh xạ một-một tới số 1–12.

## 4. Conditional UI & state variations
- States theo inventory: accepted/stub/no-delivery/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/SH-04.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
