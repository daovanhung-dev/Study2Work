# Kế hoạch màn hình — SH-04 Bàn giao xác thực thư điện tử

> **Trạng thái:** ĐÃ_LẬP_KẾ_HOẠCH / DD_ĐANG_THỰC_HIỆN · **Phạm vi phiên:** chỉ SH-04 · **Đợt:** W0 · **Ưu tiên:** P1.

## 1. Mục tiêu và căn cứ

- **Mục tiêu:** cho Khách biết yêu cầu gửi thư xác thực được API #02 tiếp nhận ở mức nào, giải thích rõ rằng bộ gửi thư hiện tại chỉ là bộ thử nghiệm, rồi cung cấp điều hướng quay lại SH-02 theo danh mục màn hình.
- **Đường dẫn trong danh mục:** `/register/verification` là đường dẫn đề xuất; chưa có bộ định tuyến Study Web trong bản làm việc.
- **Tiêu chí và API:** AC-01; `POST /api/v1/auth/verify-email/send` (API #02). Luồng F01 đặt SH-04 sau SH-03 và trước SH-02.
- **Bàn giao dữ liệu dự kiến:** thành công API #01 trả `data.id` và `data.email`; SH-04 ánh xạ `data.id` → `user_id`, `data.email` → `email`. Cơ chế chuyển trạng thái giữa hai màn hình chưa có mã nguồn; không đưa hai giá trị này vào URL và không chọn cơ chế lưu trữ khi chưa có quyết định.
- **Mã nguồn giao diện Study:** `apps/study-client/` hiện chỉ có `docs/list_screen.md`, không có mã giao diện (`src`), bộ định tuyến, gói cấu hình hoặc kiểm thử giao diện. Mọi đường dẫn API, hành vi và tương tác giao diện trong kế hoạch này là đích thiết kế, chưa được nối.
- **Tài liệu thiết kế:** ảnh/HTML SH-04 ghi nhận mẫu hiện hữu; `90_reference/study2work-lms-design-system/DESIGN.md` chỉ là tham khảo thị giác. Đích thiết kế Study được quy định tại `.agents/web-study/design.md`; không dùng ảnh mẫu làm căn cứ đảo ngược token chuẩn.

## 2. Trạng thái nguồn và điểm sai khác

| Hạng mục | Bằng chứng hiện hành | Cách xử lý trong DD |
|---|---|---|
| Ảnh gốc | `screen.png`, 1600×1280; SHA-256 `07f88cb51f0c31a990b5f553a828b4f1cba3b3d7e648286f70e3604528aed396`. Ảnh thể hiện biến thể `accepted`. | Giữ nguyên và tạo một ảnh riêng có 12 số chú thích. |
| HTML gốc | `code.html`; SHA-256 `a524d7d9d5b5640273d9d84900f9ba6a68df8a434d1f0ff189d989e4a2575684`. Có bốn nút đổi trạng thái cục bộ và một nút sao chép lệnh. | Giữ nguyên. Mã JavaScript chỉ đổi nội dung trang tại chỗ; không gọi API. |
| Bàn giao từ API #01 | Mã nguồn đăng ký chèn hồ sơ và trả `data.id`, `data.email`; API #01 không gọi API #02. | Ghi ánh xạ sang `user_id`, `email`; không tuyên bố đã có kênh truyền giữa màn hình. |
| API #02 hiện tại | Đường dẫn API công khai nhận `user_id: int`, `email: str`; bộ kiểm tra dữ liệu yêu cầu `user_id` là số nguyên thô và chuẩn hóa địa chỉ thư điện tử. API không mở phiên cơ sở dữ liệu. Bộ gửi thư mặc định bỏ dữ liệu đầu vào và trả `status="accepted"`. | Chỉ biểu diễn HTTP 202 / `DESIGN_OPERATION_ACCEPTED` / `data.status="accepted"` là đã được bộ thử nghiệm tiếp nhận; chưa có gửi thư, hàng đợi, OTP, liên kết hay xác minh. |
| Mô phỏng trạng thái trong HTML | Các nút chuyển `stub`, `no-delivery`, `error` tự dựng HTTP/dữ liệu cục bộ: lần lượt có 200, 202 và 503; nút chuyển lỗi nói về 503. | Không dùng các mã hoặc dữ liệu này làm hợp đồng. Lỗi dịch vụ gửi thư hiện ánh xạ thành HTTP 500 / `DESIGN_INTERNAL_ERROR`; `202` từ bộ giả lập vẫn không chứng minh giao thư. |
| Nội dung xếp hàng | HTML nói yêu cầu đã vào hàng đợi; bộ gửi thư mặc định chỉ bỏ dữ liệu và trả `accepted`. | Đổi câu chữ đích thành “được bộ thử nghiệm tiếp nhận”; không nói đã ghi hàng đợi hoặc đã gửi. Không sửa HTML nguồn trong phiên này. |
| Mẫu lệnh sao chép | HTML tạo URL ngoài thiếu `/api/v1` và phần thân yêu cầu chỉ có `email`; API hiện tại bắt buộc `user_id` và `email`. | Đánh dấu không hợp lệ với hợp đồng hiện tại; không cung cấp nút sao chép lệnh đó như chức năng dùng được. |
| Xác nhận thư điện tử | Không tìm thấy điểm cuối API xác nhận OTP hoặc liên kết trong danh mục API hiện tại. | Không thêm ô OTP, liên kết xác nhận, bộ đếm lùi hoặc trạng thái “đã xác minh”. |
| Hệ thống màu và chữ | Tệp tham khảo có `primary: #004ac6` ở YAML nhưng phần văn xuôi gọi `#2563EB` là màu chính; HTML dùng hai màu ở hai token khác nhau. Hướng dẫn Study dùng `ocean-primary: #0B5F8A`, ưu tiên Inter có sẵn hoặc sans-serif hệ thống, và không tải phông từ xa. | Giữ nguyên ảnh mẫu làm bằng chứng thiết kế; khi triển khai phải dùng hướng dẫn Study và giải quyết token ở nguồn tham khảo trước khi tái sử dụng. |
| Nhãn kiểm định tiếp cận | Ảnh có nhãn đạt WCAG AA; phiên này chưa đo tương phản hoặc kiểm tra thao tác bàn phím. | Không coi nhãn trong ảnh là kết quả kiểm định. |

## 3. Bố cục và danh sách số chú thích

Ảnh hiện tại dùng khung rộng: thanh định danh ở đầu trang; bên dưới là bố cục hai cột gồm thẻ thông báo chính bên trái và thẻ trạng thái API bên phải; thẻ quy tắc cùng chân trang nằm phía dưới. HTML dùng lưới một cột rồi chuyển thành bố cục 7/12 + 5/12 ở mốc `lg`; ở màn hình hẹp, các vùng xếp dọc. Khi triển khai, phải giữ thứ tự đọc từ thông báo chính tới thông tin kỹ thuật và thao tác.

Tọa độ tính bằng pixel trong ảnh gốc 1600×1280. Mỗi số phải khớp một hàng dưới đây, một hàng trong DD và `SH-04_markers.json`.

| # | Vùng chú thích | Vai trò | Hành vi/ghi chú đích |
|---:|---|---|---|
| 1 | Mã màn hình và đường dẫn | Ngữ cảnh trang | Hiển thị SH-04 và đường dẫn đề xuất; không khẳng định đường dẫn trang đang hoạt động. |
| 2 | Cụm chọn trạng thái mô phỏng | Bộ chuyển trạng thái trong HTML mẫu | Không chuyển các nút chuyển giả lập thành lựa chọn người dùng cuối; trạng thái thật do phản hồi API quyết định. |
| 3 | Biểu tượng và nhãn phản hồi | Nhận biết trạng thái bàn giao | Trạng thái mặc định dự kiến là API #02 trả `accepted` từ bộ gửi thư giả lập. |
| 4 | Tiêu đề và nội dung thông báo | Giải thích kết quả cho Khách | Dùng câu chữ trung thực: yêu cầu được bộ thử nghiệm tiếp nhận, thư chưa được gửi thật. |
| 5 | Khung giới hạn xác minh | Nêu điều chưa hỗ trợ | Giữ thông tin không có OTP, không có liên kết và chưa có điểm cuối xác nhận. |
| 6 | Nút quay lại SH-02 | Điều hướng thứ cấp | Mở `/login` theo danh mục màn hình; không suy ra đăng nhập chắc chắn thành công. |
| 7 | Nút sao chép lệnh | Tiện ích kỹ thuật trong HTML mẫu | Đề xuất bỏ/ẩn khỏi giao diện người dùng vì mẫu lệnh hiện sai đường dẫn và thiếu trường bắt buộc. |
| 8 | Tiêu đề thẻ trạng thái API | Tham chiếu hợp đồng | Nêu API #02 và trạng thái đang được mô tả; không gắn nhãn là kiểm chứng trực tiếp. |
| 9 | Các hàng trạng thái HTTP/giao thư/xác minh | Tóm tắt khả năng hệ thống | Phân biệt HTTP 202, giao thư chưa được xác nhận và chưa có xác minh; không hiển thị số giả lập 200/503. |
| 10 | Khung JSON mẫu | Ví dụ hợp đồng | Thay cấu trúc giả `delivery`/`artifacts` bằng cấu trúc phản hồi thật hoặc ghi rõ đây là ví dụ; không đưa trường chưa có từ API. |
| 11 | Thẻ quy tắc thiết kế | Ghi chú về hành vi không được giả lập | Giữ nguyên nguyên tắc không tạo bộ đếm lùi hoặc ô nhập mã giả. |
| 12 | Chân trang nhận diện | Thông tin thiết kế | Chỉ chứa mã màn hình/đường dẫn và thông tin phiên bản nếu được duyệt; không biến nhãn kiểm định trong ảnh thành cam kết. |

## 4. Dữ liệu và thứ tự sự kiện

1. SH-03 nhận HTTP 201 từ API #01; nguồn hiện tại trả `data.id` và `data.email` trong hồ sơ vừa tạo.
2. Chỉ khi có cả hai giá trị từ bàn giao hợp lệ, SH-04 mới được phép gửi một yêu cầu `POST /api/v1/auth/verify-email/send` với JSON `{ "user_id": <data.id>, "email": <data.email> }`.
3. API #02 được gọi công khai: không cần `Authorization`; API không mở cơ sở dữ liệu và không tra cứu để xác nhận ID thuộc địa chỉ thư điện tử.
4. Bộ kiểm tra dữ liệu chuẩn hóa địa chỉ thư điện tử. `user_id` phải là số nguyên thô; thiếu trường hoặc kiểu/định dạng không hợp lệ đi vào phản hồi 422. Không tự thêm quy tắc `user_id > 0` vì mã hiện tại không chứng minh quy tắc đó.
5. Với bộ gửi thư mặc định, phản hồi là HTTP 202, `businessCode="DESIGN_OPERATION_ACCEPTED"`, `data={"status":"accepted"}`. Không có `reason` trong kết quả bộ gửi thư mặc định; `meta` là đối tượng rỗng và có `traceId`.
6. Nếu bộ gửi thư phát sinh lỗi, API trả HTTP 500, `businessCode="DESIGN_INTERNAL_ERROR"` và thông báo an toàn. Nếu không nhận được HTTP phản hồi, giao diện có thể nêu lỗi kết nối nhưng không tự gửi lại.
7. SH-02 là màn hình tiếp theo được danh mục màn hình liệt kê. Nút quay lại chỉ là điều hướng; không khẳng định thư điện tử đã được xác minh hoặc đăng nhập sẽ được chấp nhận.

### Mẫu yêu cầu và phản hồi có căn cứ

```json
{
  "user_id": 1001,
  "email": "student@example.com"
}
```

```json
{
  "success": true,
  "businessCode": "DESIGN_OPERATION_ACCEPTED",
  "message": "Yêu cầu gửi email xác thực đã được chấp nhận.",
  "data": { "status": "accepted" },
  "meta": {},
  "traceId": "<mã do máy chủ cấp>"
}
```

Mẫu dùng `user_id`/`email` minh họa trường API; dữ liệu người dùng thật không được ghi cứng vào giao diện. Mã trạng thái HTTP của phản hồi trên là 202. Kết quả chỉ xác nhận bộ gửi thư hiện tại đã tiếp nhận lời gọi.

## 5. Trạng thái cần mô tả và cách xử lý

| Trạng thái | Bằng chứng/điều kiện | Thể hiện đích |
|---|---|---|
| Đang gửi | Đề xuất giao diện; chưa có mã giao diện. | Nút gửi có trạng thái chờ và khóa thao tác lặp cho cùng lượt gửi. |
| Đã tiếp nhận bởi bộ thử nghiệm | Bộ gửi thư mặc định trả `accepted`; đường dẫn API trả 202. | Nêu thư chưa được gửi thật; không gọi đây là đã vào hàng đợi hay xác minh xong. |
| Chưa gửi thư thật | Hệ quả đã biết của bộ gửi thư mặc định, không phải một phản hồi riêng. | Hiển thị như phần giải thích đi kèm trạng thái `accepted`, không tạo dữ liệu giả `no_delivery`. |
| Dữ liệu không hợp lệ | API #02 có nhánh 422 `DESIGN_VALIDATION_ERROR`. | Không tuyên bố lệnh gửi thành công; thông báo cần sửa/bổ sung dữ liệu theo nguồn lỗi. |
| Lỗi bộ gửi thư | Ngoại lệ bộ gửi thư ánh xạ HTTP 500 `DESIGN_INTERNAL_ERROR`. | Thông báo chung; không hiện lỗi từ dịch vụ ngoài, mã 503 hoặc dữ liệu `handshake_timeout` giả. |
| Lỗi kết nối | Trạng thái phía trình duyệt nếu không nhận được phản hồi; chưa được cài đặt. | Giữ rõ kết quả chưa xác định; không tự thử lại thao tác gửi. |
| Thiếu dữ liệu bàn giao | Điều kiện triển khai chưa được chốt vì cơ chế truyền từ SH-03 chưa có. | Không gọi API #02. Cần quyết định màn hình dự phòng trước khi phát hành; không đặt `user_id`/`email` trong URL. |

## 6. Điều kiện chặn và tiêu chí hoàn tất

### Điều kiện chặn

1. Chưa có mã Study Web được nối khi chạy, nên không có đường dẫn trang, điều hướng, trạng thái tải hay lời gọi API từ trình duyệt để xác minh.
2. Bộ gửi thư mặc định chỉ bỏ dữ liệu đầu vào và trả `accepted`; chưa có gửi thư thật, OTP, liên kết xác nhận hoặc điểm cuối hoàn tất xác minh.
3. Cơ chế SH-03 bàn giao `data.id`/`data.email` sang SH-04 chưa được hiện thực hóa hoặc duyệt.
4. Cần thay các thẻ mô phỏng bằng trạng thái phản hồi có thật; mã 200/503 và dữ liệu giao thư trong HTML không khớp API #02.
5. Mẫu cURL hiện sai điểm cuối API và phần thân yêu cầu; không được tái sử dụng khi triển khai.
6. Cần theo hướng dẫn Study về màu, phông chữ, trạng thái tiêu điểm và khả năng tiếp cận; tệp tham khảo có token nội bộ mâu thuẫn.

### Tiêu chí hoàn tất phiên tài liệu

- Kế hoạch này được tạo trước DD và ghi rõ một màn hình duy nhất.
- DD, kế hoạch, nhật ký công việc và nhãn số chú thích do phiên này tạo dùng tiếng Việt; tên API, trường, giá trị JSON và đường dẫn giữ nguyên chính tả kỹ thuật.
- Có đúng 12 số trên ảnh chú thích; mỗi số khớp bảng tại §3, DD và JSON marker.
- PNG/HTML nguồn giữ nguyên SHA-256 nêu tại §2; ảnh chú thích giữ đúng tỷ lệ khung hình.
- DD phân biệt trạng thái API thật với các trạng thái mô phỏng; không tuyên bố gửi thư, vào hàng đợi hoặc xác minh thành công.
- Các liên kết cục bộ hoạt động; bảng theo dõi ghi trạng thái bản nháp.
- Chỉ rà soát tĩnh; không chạy kiểm thử dự án và không tuyên bố tích hợp/triển khai.
