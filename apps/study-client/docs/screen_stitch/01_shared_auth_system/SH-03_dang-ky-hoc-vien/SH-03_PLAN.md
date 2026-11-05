# Kế hoạch màn hình — SH-03 Đăng ký học viên

> **Trạng thái:** KẾ_HOẠCH_ĐÃ_XONG / DD_BẢN_NHÁP_ĐÃ_XONG · **Phạm vi phiên:** chỉ SH-03 · **Đợt:** W0 · **Ưu tiên:** P0.

## 1. Mục tiêu và nguồn căn cứ

- **Mục tiêu:** cho Khách tạo tài khoản học viên bằng họ tên, email và mật khẩu, rồi chuyển sang SH-04 theo luồng F01.
- **Định tuyến trong danh mục:** `/register` là đường dẫn đề xuất, chưa được xác nhận là đường dẫn đang hoạt động.
- **Tiêu chí liên quan:** AC-01. Danh mục yêu cầu POST API #01; sau thành công, SH-04 mới gửi yêu cầu API #02. Email/OTP/CAPTCHA không được tự thêm vào biểu mẫu.
- **Mã nguồn API hiện tại:** `POST /api/v1/auth/register` được nối trong Study Server. API #01 kiểm tra dữ liệu, tìm email trùng, băm mật khẩu Argon2id, chèn tài khoản vai trò `STUDENT`, commit và trả hồ sơ công khai với HTTP 201. Đây là bằng chứng mã nguồn/mã kiểm thử cục bộ, không phải xác nhận triển khai hoặc lược đồ cơ sở dữ liệu đang chạy.
- **Mã nguồn giao diện hiện tại:** `apps/study-client/src` và trang bộ định tuyến Study Web không có trong bản làm việc. `code.html` là bản mẫu: biểu mẫu có `onsubmit` chặn gửi mặc định; không có lời gọi API. Không mô tả giao diện hoặc đường dẫn như đã được triển khai.
- **Tài liệu thiết kế:** dùng ảnh và HTML SH-03 để ghi nhận bố cục hiện hữu; dùng `apps/study-client/docs/screen_stitch/90_reference/study2work-lms-design-system/DESIGN.md` làm tham khảo thị giác; tuân theo `.agents/web-study/design.md` làm đích chuẩn Study Web. Không thêm phông chữ hoặc tài nguyên CDN từ xa theo HTML mẫu.

## 2. Trạng thái nguồn và điểm sai khác

| Hạng mục | Bằng chứng | Cách ghi trong DD |
|---|---|---|
| Ảnh gốc | `screen.png`, 1280×1056, có giao diện đầy đủ. SHA-256 `67eef666cf7ebf48db44b2b721b13a40632237a165ff11ca6b5a2040a32d079e`. | Giữ nguyên; chú thích lên ảnh này, không tạo ảnh dựng thay thế. |
| HTML gốc | `code.html`, 10.173 byte. SHA-256 `bd0123dee4571caff1920804b4ce8508d2f20f53ce8e113afcb766874c8334a3`. | Giữ nguyên. Tài liệu là thiết kế tĩnh; mã gửi biểu mẫu chỉ gọi `preventDefault()`. |
| Trường mật khẩu | Đoạn trợ giúp ẩn của HTML nói tối thiểu 8 ký tự; bộ kiểm tra API #01 chỉ từ chối mật khẩu rỗng/toàn khoảng trắng. | Không coi giới hạn 8 là hợp đồng. Đánh dấu sai khác và yêu cầu thống nhất câu chữ với máy chủ. |
| Tên trường | HTML dùng `name="fullname"`; JSON API nhận `full_name`. | Bản đồ dữ liệu phải ánh xạ rõ `fullname` → `full_name`. |
| Kết quả tạo tài khoản | API #01 trả `data.id`, `data.email`; API #02 nhận `user_id`, `email`. | Luồng sang SH-04 ánh xạ `data.id` → `user_id`; không đặt ID hoặc email trong URL. Kênh truyền trạng thái tạm giữa các đường dẫn cần được chốt khi triển khai. |
| Gửi email | API #01 không gọi API #02. Bộ gửi thư mặc định của API #02 trả `status="accepted"`, không gửi thư thật, không tạo token và không xác nhận địa chỉ email. | SH-03 chỉ hoàn thành tạo tài khoản. SH-04 phải nói rõ “đã tiếp nhận yêu cầu” thay vì “đã xác minh”. |
| Trạng thái tài khoản | SQL chèn của API #01 không ghi cột `status`; tệp `DB.sql` được lưu trong kho khai báo mặc định `ACTIVE`; API #03 chỉ cho đăng nhập khi `status` là `ACTIVE`. Chưa kiểm chứng lược đồ đang chạy thực tế. | Ghi thành điều kiện cần rà soát: không tuyên bố email đã xác minh; chủ sở hữu sản phẩm/bảo mật cần xác nhận quy tắc kích hoạt trước khi phát hành. |
| Kiểu chữ | HTML/ảnh sử dụng Plus Jakarta Sans từ Google Fonts; hướng dẫn Study ưu tiên Inter có sẵn hoặc sans-serif hệ thống và cấm thêm phông chữ tải từ xa. | Tách nhận diện ảnh gốc khỏi quyết định phụ thuộc phông chữ khi triển khai. |

## 3. Bố cục và danh sách marker

Giữ bố cục một cột, căn giữa theo chiều ngang: thương hiệu và lời giới thiệu ở trên, biểu mẫu trên thẻ trắng, liên kết đăng nhập ở cuối thẻ. Ở màn hình hẹp, giữ lề ngoài tối thiểu 16px và cho phép cuộn dọc; không ẩn trường hoặc nút chính.

| # | Vùng cần chú thích | Thành phần / vai trò | Hành vi đích |
|---:|---|---|---|
| 1 | Logo S2W và chữ Study2Work | Nhận diện sản phẩm | Nội dung tĩnh; không tự gắn liên kết chưa có trong danh mục. |
| 2 | Tiêu đề và câu giới thiệu | Hướng dẫn mục tiêu của trang | Nội dung tĩnh, thứ tự tiêu đề có ngữ nghĩa. |
| 3 | Nhãn “Họ và tên” và ô nhập | Trường `full_name` | Cắt khoảng trắng hai đầu, bắt buộc có nội dung, tối đa 150 ký tự theo API. |
| 4 | Nhãn “Địa chỉ email” và ô nhập | Trường `email` | Kiểm tra định dạng; API cắt khoảng trắng và giới hạn 255 ký tự. |
| 5 | Nhãn “Mật khẩu” và ô nhập | Trường `password` | Bắt buộc; giữ nguyên giá trị gửi. Không áp dụng ngưỡng 8 ký tự cho tới khi hợp đồng được chốt. |
| 6 | Nút “Tạo tài khoản” | Tác vụ chính | Khóa gửi lặp khi yêu cầu đang chờ; gọi API #01 đúng một lần cho mỗi lần gửi của người dùng. |
| 7 | Dải chân thẻ “Đã có tài khoản? Đăng nhập” | Điều hướng thứ cấp | Tới SH-02 `/login`; không gửi biểu mẫu. |

Các tọa độ trong `SH-03_markers.json` tính theo pixel của ảnh gốc 1280×1056. Mỗi số đặt sát mé trái của vùng được đánh dấu để tránh che nhãn hoặc giá trị người dùng nhập.

## 4. Bản đồ trường và hợp đồng dữ liệu

| Trường trên giao diện | Tên trong HTML | Trường yêu cầu API #01 | Kiểu / giới hạn theo mã nguồn | Xử lý |
|---|---|---|---|---|
| Họ và tên | `fullname` | `full_name` | Chuỗi bắt buộc; sau khi cắt khoảng trắng hai đầu dài 1–150 ký tự. | Gửi `full_name`; không tự suy ra tên riêng/họ. |
| Địa chỉ email | `email` | `email` | Chuỗi email; sau chuẩn hóa tối đa 255 ký tự. | Gửi email sau khi cắt khoảng trắng/kiểm tra theo API; giữ bản hiển thị người dùng khi cần sửa. |
| Mật khẩu | `password` | `password` | Chuỗi bắt buộc, không chỉ gồm khoảng trắng; API không áp giới hạn tối thiểu 8 ký tự. | Gửi nguyên văn; không log, lưu ở URL hay thêm vào dữ liệu điều hướng. |

JSON yêu cầu chỉ có `{ "email": ..., "password": ..., "full_name": ... }`. Không thêm trường đồng ý điều khoản, `role`, token, mã OTP hay CAPTCHA vì chưa có hợp đồng cho các trường đó.

## 5. Chuỗi sự kiện dự kiến

1. Khách mở đường dẫn đề xuất `/register`. Vì bộ định tuyến Study Web chưa có trong bản làm việc, đây là đích thiết kế, chưa phải trang hoạt động.
2. Khách điền ba trường và chọn “Tạo tài khoản”. Kiểm tra phía giao diện phục vụ trải nghiệm; API vẫn là nguồn quyết định cuối cùng.
3. Chặn thao tác lặp trong khi đang gửi; tạo JSON đúng ba trường theo bảng ở §4; gửi `POST /api/v1/auth/register` không kèm `Authorization`.
4. Máy chủ tạo hồ sơ và trả HTTP 201 cùng `businessCode="DESIGN_RESOURCE_CREATED"`. Lấy `data.id` và `data.email` để chuyển tiếp sang SH-04. Không gửi lại yêu cầu nếu kết quả mạng chưa rõ vì chưa có khóa chống lặp.
5. SH-04, không phải SH-03, gọi `POST /api/v1/auth/verify-email/send` với `{user_id: data.id, email: data.email}`. HTTP 202 hiện chỉ xác nhận bộ gửi thư giả lập đã tiếp nhận yêu cầu.
6. Nếu API #01 trả 409, giữ nội dung biểu mẫu, đánh dấu email và hiển thị thông báo “Email đã tồn tại.”; Khách có thể sửa email hoặc mở SH-02.
7. Nếu trả 422, đọc `meta.fieldErrors`, nối lỗi với trường khi có `field`; không áp câu “tối thiểu 8 ký tự” từ HTML mẫu khi máy chủ chưa thực thi quy tắc này.
8. Với HTTP 500 hoặc lỗi mạng, giữ dữ liệu để người dùng xem lại, hiển thị thông báo an toàn. Lỗi mạng sau khi gửi được xem là kết quả chưa rõ; không tự gửi lại.

## 6. Trạng thái và tiêu chí xử lý

| Trạng thái giao diện | Vào trạng thái khi | Nội dung / thao tác |
|---|---|---|
| Ban đầu | Mở trang | Ba trường rỗng; nút khả dụng. |
| Đang kiểm tra | Khách gửi biểu mẫu | Kiểm tra bắt buộc, định dạng email, họ tên sau khi cắt khoảng trắng còn 1–150 ký tự; không thêm quy tắc mật khẩu chưa có hợp đồng. |
| Đang gửi | Dữ liệu hợp lệ và yêu cầu đã bắt đầu | Nút báo đang xử lý và không nhận gửi lặp. |
| Lỗi dữ liệu `422` | API từ chối dữ liệu | Lỗi chung và lỗi theo trường từ `meta.fieldErrors`; đưa tiêu điểm tới trường lỗi đầu tiên nếu có thể. |
| Email đã dùng `409` | `DESIGN_STATE_CONFLICT` | Hiển thị cảnh báo cạnh email, giữ các trường đã nhập, cho phép sửa hoặc sang SH-02. |
| Lỗi máy chủ `500` | `DESIGN_INTERNAL_ERROR` | Thông báo chung có thể thử lại sau; không lộ chi tiết cơ sở dữ liệu/bộ gửi thư. |
| Kết quả mạng chưa rõ | Không nhận được phản hồi | Giữ dữ liệu, cảnh báo kết quả chưa xác định; yêu cầu người dùng kiểm tra trước khi gửi lại. |
| Tạo thành công `201` | `DESIGN_RESOURCE_CREATED` | Chuyển sang SH-04 với ID/email trong trạng thái điều hướng tạm; không hiển thị trạng thái email đã xác minh. |

## 7. Điều kiện chặn và câu hỏi cần quyết định

1. Chưa có bộ định tuyến Study Web, thành phần giao diện hoặc lớp gọi API; chỉ được hoàn thiện DD mục tiêu, không khẳng định giao diện đang hoạt động.
2. Cần giải quyết chênh lệch giới hạn mật khẩu 8 ký tự trong HTML và validator API trước khi dùng câu trợ giúp lỗi.
3. Cần duyệt kênh truyền `data.id`/`data.email` sang SH-04 sao cho không lộ dữ liệu trong URL và không phụ thuộc vào lưu trữ bền vững chưa được duyệt.
4. Cần xác nhận vòng đời tài khoản: SQL API #01 không đặt `status`; tệp DDL `DB.sql` đặt mặc định `ACTIVE`; API #02 không xác minh email. Không được coi email là điều kiện kích hoạt hiện hữu.
5. Cần xử lý thống nhất kiểu chữ khi đưa mẫu vào mã: ảnh dùng Plus Jakarta Sans tải từ xa, hướng dẫn Study ưu tiên phông chữ có sẵn tại chỗ.

## 8. Tiêu chí hoàn tất tài liệu SH-03

- Có một DD tiếng Việt cho SH-03 và một kế hoạch tiếng Việt riêng được tạo trước DD.
- Ảnh `screen.png` và HTML `code.html` không đổi; ảnh `screen_annotated.png` khớp 7 marker trong bảng §3 và tệp JSON.
- DD thể hiện rõ ranh giới `fullname` → `full_name`, `data.id` → `user_id`, và API #02 chỉ thuộc bước SH-04.
- DD nêu riêng HTTP 201/409/422/500 của API #01 và trạng thái mã nguồn/giao diện đích; không tuyên bố email được gửi hoặc đã xác minh.
- Các liên kết tương đối mở đúng nguồn và không có phần tử giao diện được mô tả là tương tác nếu HTML không có bằng chứng.
