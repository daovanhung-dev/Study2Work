# SH-03 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [SH-03_markers.json](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/SH-03_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `SH-03-EL-001` | `SH03-EL-01` | Logo S2W và nhận diện Study2Work |
| #2 | `SH-03-EL-002` | `SH03-EL-02` | Tiêu đề đăng ký và câu giới thiệu |
| #3 | `SH-03-EL-003` | `SH03-EL-03` | Trường họ và tên, ánh xạ tới full_name |
| #4 | `SH-03-EL-004` | `SH03-EL-04` | Trường email |
| #5 | `SH-03-EL-005` | `SH03-EL-05` | Trường mật khẩu |
| #6 | `SH-03-EL-006` | `SH03-EL-06` | Nút tạo tài khoản |
| #7 | `SH-03-EL-007` | `SH03-EL-07` | Liên kết đăng nhập tới SH-02 |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 4. Thuộc tính phần tử được đánh số

Số marker khớp [ảnh chú thích](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/screen_annotated.png) và [bản đồ marker](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/SH-03_markers.json). Kích thước ảnh nguồn là 1280×1056. Marker xác định vùng thiết kế, không khẳng định phần tử đã có xử lý khi chạy.

| # / Element ID | Tên và loại | Vị trí, thuộc tính, dữ liệu và điều kiện hiển thị | Trạng thái | Sự kiện liên kết / đầu ra |
|---|---|---|---|---|
| 1 / `SH03-EL-01` | Logo S2W và chữ Study2Work · nhận diện tĩnh | Phía trên thẻ, căn giữa; ảnh có biểu tượng `S2W` và chữ Study2Work. Không có href trong HTML; luôn hiển thị. | Default; không có trạng thái tải/lỗi. | `SH03-EV-01`; không điều hướng và không gọi API. |
| 2 / `SH03-EL-02` | Tiêu đề và câu giới thiệu · nội dung tĩnh | Đầu trang trong thẻ; H1 mục tiêu “Đăng ký tài khoản học viên” và câu mô tả; nguồn là nội dung thiết kế, không lấy từ API. | Default; luôn hiển thị. | `SH03-EV-01`; không có thao tác trực tiếp. |
| 3 / `SH03-EL-03` | Họ và tên · text input | `label for="fullname"`; `id/name="fullname"`; gợi ý “Nhập họ và tên”. Người dùng nhập; trường yêu cầu của API là `full_name`, sau trim dài 1–150. HTML hiện không khai báo `required`, `maxlength`, `autocomplete`; điều kiện đích là bắt buộc và hiển thị lỗi cạnh trường khi có. | Default, focus, validation error, submitting; enabled trừ khi biểu mẫu đang gửi. | `SH03-EV-02`, `SH03-EV-03`, `SH03-EV-06`; map `fullname` → `full_name`. |
| 4 / `SH03-EL-04` | Địa chỉ email · email input | `label for="email"`; `id/name="email"`; gợi ý `example@domain.com`. Người dùng nhập; API trim, kiểm tra định dạng và giới hạn 255 ký tự. HTML hiện không khai báo `required`, `maxlength`, `autocomplete`; điều kiện đích là bắt buộc. | Default, focus, validation error, conflict 409, submitting; enabled trừ khi đang gửi. | `SH03-EV-02`, `SH03-EV-03`, `SH03-EV-05`, `SH03-EV-06`; output JSON `email`. |
| 5 / `SH03-EL-05` | Mật khẩu · password input | `label for="password"`; `id/name="password"`; gợi ý “Nhập mật khẩu”. Giá trị nhạy cảm do người dùng nhập, bắt buộc theo request; API chỉ từ chối giá trị rỗng/toàn khoảng trắng và băm Argon2id. HTML có thông báo ẩn “tối thiểu 8 ký tự” không khớp API; không dùng thông báo đó làm rule. | Default, focus, validation error, submitting; che ký tự; enabled trừ khi đang gửi. Không có nút hiện/ẩn trong ảnh/HTML. | `SH03-EV-02`, `SH03-EV-03`, `SH03-EV-06`; gửi nguyên giá trị trong `password`, không lưu vào handoff. |
| 6 / `SH03-EL-06` | “Tạo tài khoản” · submit button | Nút toàn chiều rộng cuối biểu mẫu, `type="submit"`. Đầu vào là ba trường #3–#5. Chỉ hoạt động khi không có request đang chờ; HTML mẫu chặn submit và không có tích hợp API. | Default, focus, submitting/disabled, lỗi còn trên biểu mẫu; thành công chuyển trang. | `SH03-EV-03` và các kết quả `SH03-EV-04..07`; gửi API #01 một lần cho mỗi submit chủ ý. |
| 7 / `SH03-EL-07` | “Đã có tài khoản? Đăng nhập” · anchor | Cuối thẻ, `href="/login"`; nội dung tĩnh và route đề xuất tới SH-02. Không mang dữ liệu biểu mẫu. | Default, hover/focus; luôn hiển thị. | `SH03-EV-08`; điều hướng tới SH-02, không gọi API. |

Thẻ trắng bo góc và nền trang là vùng trình bày, không được đánh số riêng vì không có sự kiện. HTML mẫu còn chứa đoạn mô phỏng lỗi dùng cho kiểm tra chất lượng nhưng đang rỗng; hàm `setFormState` tham chiếu `alert-409` và các nút trạng thái nhưng các phần tử đó không tồn tại trong tài liệu. Không coi bộ mô phỏng này là bộ xử lý lỗi thực.

## 4. Conditional UI & state variations
- States theo inventory: validating/submitting/409/422/201
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/SH-03.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
