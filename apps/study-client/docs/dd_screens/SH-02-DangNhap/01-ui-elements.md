# SH-02 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [SH-02_markers.json](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `SH-02-EL-001` | `SH02-EL-01` | Dấu thương hiệu và nhận diện Study2Work |
| #2 | `SH-02-EL-002` | `SH02-EL-02` | Tiêu đề đăng nhập và phần giải thích |
| #3 | `SH-02-EL-003` | `SH02-EL-03` | Vùng cảnh báo chung đang ẩn ban đầu |
| #4 | `SH-02-EL-004` | `SH02-EL-04` | Trường email |
| #5 | `SH-02-EL-005` | `SH02-EL-05` | Trường mật khẩu |
| #6 | `SH-02-EL-006` | `SH02-EL-06` | Điều khiển hiện/ẩn mật khẩu |
| #7 | `SH-02-EL-007` | `SH02-EL-07` | Nút gửi đăng nhập |
| #8 | `SH-02-EL-008` | `SH02-EL-08` | Liên kết đăng ký tới SH-03 |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 4. Thuộc tính phần tử được đánh số

Số khớp [ảnh xem trước có chú thích](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/screen_annotated.png) và [JSON marker](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02_markers.json). Bản dựng sạch, không đánh số, ở [đây](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/screen_rendered.png). Marker xác định vùng thiết kế; chúng không chứng minh bộ xử lý nội tuyến đang hoạt động.

| # | Element ID | Tên / loại | Vị trí / mục đích | Thuộc tính, nguồn, hiển thị và trạng thái | Event ID |
|---:|---|---|---|---|---|
| 1 | SH02-EL-01 | Nhận diện Study2Work / nhóm văn bản + biểu tượng | Đầu thẻ; nhận diện sản phẩm | Tĩnh; biểu tượng trường học trong ô xanh ngọc 40×40, chữ Study2Work và phụ đề STUDY LMS. Font biểu tượng đến từ Material Symbols CDN trong HTML. Không có href/handler nguồn; xem như trang trí, không tương tác cho tới khi duyệt đích. | — |
| 2 | SH02-EL-02 | Tiêu đề và phần giải thích / H1 + đoạn văn | Dưới nhận diện; định hướng tác vụ | Văn bản tĩnh “Đăng nhập” và mô tả; không có input/API/state tương tác. Giữ một H1 có ngữ nghĩa; style hiện tham chiếu Inter/hệ thống và Tailwind. | — |
| 3 | SH02-EL-03 | Vùng cảnh báo / vùng thông báo | Giữa phần giới thiệu và biểu mẫu; trình bày lỗi | `div#alert-box`, `role="alert"`, có tiêu đề/mô tả và biểu tượng; mặc định hidden, hiện khi lỗi được ánh xạ. Nội dung do UI tạo từ response an toàn, không chèn lỗi thô; trạng thái ẩn/hiện và focus theo §6–7. HTML chưa có handler điền vùng này. | SH02-EV-05–SH02-EV-09, SH02-EV-12 |
| 4 | SH02-EL-04 | Email / input | Trường đầu tiên; nhận email tài khoản | `type=email`, `name=email`, `required`, `autocomplete=email`, placeholder `name@example.com`; mặc định rỗng, bản mẫu không đặt `maxlength`. Nguồn là người dùng; trình duyệt có thể kiểm tra email cục bộ; #03 trim/kiểm định và giới hạn email đã chuẩn hóa tối đa 255 ký tự. Trạng thái default/focus/validation-error. | SH02-EV-02, SH02-EV-04–SH02-EV-08 |
| 5 | SH02-EL-05 | Mật khẩu / input nhạy cảm | Trường thứ hai; nhận mật khẩu hiện tại | `type=password`, `name=password`, `required`, `autocomplete=current-password`, placeholder “Nhập mật khẩu”; mặc định rỗng/ẩn. Nguồn là người dùng; client giữ nguyên chuỗi; #03 từ chối chuỗi chỉ có khoảng trắng nhưng xác minh nguyên văn. Không hiển thị lại giá trị trong lỗi/log/route. Trạng thái default/focus/validation-error. | SH02-EV-02, SH02-EV-04–SH02-EV-08 |
| 6 | SH02-EL-06 | Hiện/ẩn mật khẩu / button | Bên trong mép phải trường mật khẩu; đổi cách nhìn giá trị | `type=button`, biểu tượng mắt và nhãn trợ năng; mặc định mật khẩu bị ẩn. Không nhận dữ liệu mới, không gọi API; giữ nguyên giá trị khi đổi `password`/`text`. Enabled khi form hiển thị, có focus bàn phím và trạng thái bật/tắt. HTML gọi `togglePasswordVisibility()` nhưng không định nghĩa hàm. | SH02-EV-03 |
| 7 | SH02-EL-07 | Gửi đăng nhập / submit button | Dưới hai trường; gửi credential | `type=submit`, chữ “Đăng nhập”; mặc định enabled, chuyển trạng thái chờ/disabled để chặn submit lặp khi request đang chạy. Dữ liệu lấy từ #4/#5. HTML gọi `handleLoginSubmit()` nhưng không định nghĩa hàm; behavior loading là đích DD, chưa có runtime. | SH02-EV-04 |
| 8 | SH02-EL-08 | Đăng ký ngay / anchor | Cuối thẻ; mở luồng tạo tài khoản | Văn bản tĩnh, `href="/register"`; không có request tại SH-02. Đích là route SH-03 theo inventory; router Study Web chưa có. Có trạng thái focus/hover theo design system. | SH02-EV-13 |

Thẻ trắng và nền trang là bề mặt bố cục, không phải phần tử tương tác. Bản dựng được căn giữa ở 1280×1024; khả năng thích ứng phải theo hướng dẫn Study chuẩn và chưa được chứng minh bằng lần dựng đơn này.

## 4. Conditional UI & state variations
- States theo inventory: idle/validating/submitting/401/403/network-error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
