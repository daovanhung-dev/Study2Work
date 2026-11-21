# Kế hoạch màn hình — SH-04 Bàn giao xác thực thư điện tử

> **Trạng thái kế hoạch:** PLAN REVIEWED / RE-AUDIT COMPLETE · **Ngày rà soát:** 2026-11-07 · **Phạm vi phiên:** chỉ SH-04 · **Đợt:** W0 · **Ưu tiên:** P1.
> **Trạng thái sau rà soát:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. API #02 dispatch owner/trigger and SH-03 handoff transport are unresolved; Study Web runtime, real delivery and verification are also unavailable.

## 1. Mục tiêu và căn cứ

- **Mục tiêu:** cho Khách biết yêu cầu gửi thư xác thực được API #02 tiếp nhận ở mức nào, giải thích rõ rằng bộ gửi thư hiện tại chỉ là bộ thử nghiệm, rồi cung cấp điều hướng quay lại SH-02 theo danh mục màn hình.
- **Đường dẫn trong danh mục:** `/register/verification` là đường dẫn đề xuất; chưa có bộ định tuyến Study Web trong bản làm việc.
- **Tiêu chí và API:** AC-01; `POST /api/v1/auth/verify-email/send` (API #02). Luồng F01 đặt SH-04 sau SH-03 và trước SH-02.
- **Bàn giao dữ liệu dự kiến:** thành công API #01 trả `data.id` và `data.email`; SH-04 ánh xạ `data.id` → `user_id`, `data.email` → `email`. Cơ chế chuyển trạng thái giữa hai màn hình chưa có mã nguồn; không đưa hai giá trị này vào URL và không chọn cơ chế lưu trữ khi chưa có quyết định.
- **Mã nguồn giao diện Study:** không có `apps/study-client/src`, router, `package.json` hoặc kiểm thử giao diện. `dist`/`node_modules` là artifact tạo sẵn/cài đặt, không xác nhận source/runtime cho SH-04. Mọi tương tác giao diện trong kế hoạch này là đích thiết kế, chưa được nối.
- **Tài liệu thiết kế:** ảnh/HTML SH-04 ghi nhận mẫu hiện hữu; `90_reference/study2work-lms-design-system/DESIGN.md` chỉ là tham khảo thị giác. Đích thiết kế Study được quy định tại `.agents/web-study/design.md`; không dùng ảnh mẫu làm căn cứ đảo ngược token chuẩn.

## 2. Trạng thái nguồn và điểm sai khác

| Hạng mục | Bằng chứng hiện hành | Cách xử lý trong DD |
|---|---|---|
| Ảnh gốc | `screen.png`, 1600×1280; SHA-256 `07f88cb51f0c31a990b5f553a828b4f1cba3b3d7e648286f70e3604528aed396`. Ảnh thể hiện biến thể `accepted`. | Giữ nguyên; giữ ảnh chú thích 12 số hiện có và xác minh lại 1:1 với JSON/DD. |
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

### Ánh xạ Element ID ổn định

| # | Element ID | Nhãn ngắn |
|---:|---|---|
| 1 | `SH04-EL-01` | Mã SH-04 và đường dẫn đề xuất |
| 2 | `SH04-EL-02` | Bộ chọn trạng thái mô phỏng (QA-only) |
| 3 | `SH04-EL-03` | Biểu tượng và nhãn phản hồi |
| 4 | `SH04-EL-04` | Tiêu đề và thông báo kết quả |
| 5 | `SH04-EL-05` | Khung giới hạn xác minh |
| 6 | `SH04-EL-06` | Điều hướng quay lại SH-02 |
| 7 | `SH04-EL-07` | Nút sao chép cURL mock (không dùng sản phẩm) |
| 8 | `SH04-EL-08` | Thẻ tham chiếu API #02 |
| 9 | `SH04-EL-09` | Hàng trạng thái HTTP/delivery/verify |
| 10 | `SH04-EL-10` | JSON mock, không phải envelope |
| 11 | `SH04-EL-11` | Quy tắc thiết kế/nhãn WCAG chưa đo |
| 12 | `SH04-EL-12` | Chân trang |

## 4. Dữ liệu và thứ tự sự kiện

1. SH-03 nhận HTTP 201 từ API #01; nguồn hiện tại trả `data.id` và `data.email` trong hồ sơ vừa tạo.
2. Chỉ khi có cả hai giá trị từ bàn giao hợp lệ, SH-04 mới được phép gửi một yêu cầu `POST /api/v1/auth/verify-email/send` với JSON `{ "user_id": <data.id>, "email": <data.email> }`.
3. API #02 được gọi công khai: không cần `Authorization`; API không mở cơ sở dữ liệu và không tra cứu để xác nhận ID thuộc địa chỉ thư điện tử.
4. Bộ kiểm tra dữ liệu trim/kiểm tra địa chỉ thư điện tử. `user_id` phải là số nguyên JSON thô; source chưa kiểm tra miền `int64` theo catalog hoặc `> 0`; thiếu/sai trường hay email không hợp lệ đi vào 422. Không tự thêm giới hạn client như thể đã được server xác nhận.
5. View map provider `status` và `reason` tùy chọn vào `data`; default stub trả HTTP 202, `DESIGN_OPERATION_ACCEPTED`, `data.status="accepted"`, không có `reason`. `meta` mặc định là đối tượng rỗng và response có `traceId`; status/reason ngoài giá trị mặc định chưa có semantics được duyệt.
6. Nếu bộ gửi thư phát sinh lỗi, API trả HTTP 500, `businessCode="DESIGN_INTERNAL_ERROR"` và thông báo an toàn. Nếu không nhận được HTTP phản hồi, giao diện có thể nêu lỗi kết nối nhưng không tự gửi lại.
7. SH-02 là màn hình tiếp theo được danh mục màn hình liệt kê. Nút quay lại chỉ là điều hướng; không khẳng định thư điện tử đã được xác minh hoặc đăng nhập sẽ được chấp nhận.

### Event inventory ổn định cho DD

| Event ID | Element / trigger | Điều kiện và đầu vào | Kết quả cần mô tả trong DD |
|---|---|---|---|
| `SH04-EV-01` | Load/route entry | Mở `/register/verification`; handoff từ SH-03 có thể thiếu nếu mở trực tiếp. | Khởi tạo trạng thái; không gọi API khi thiếu `user_id` hoặc `email`; fallback route/message chưa được duyệt. |
| `SH04-EV-02` | Dispatch API #02 khi handoff hợp lệ | Có `data.id` và `data.email` từ HTTP 201 API #01; dispatch trigger/owner cần xác nhận. | POST công khai `{user_id,email}`; không gửi Authorization; không auto-retry hoặc gọi trùng trong một lượt. |
| `SH04-EV-03` | HTTP 202 accepted | `DESIGN_OPERATION_ACCEPTED`, `data.status="accepted"`. | Hiển thị accepted bởi provider; không nói đã giao email/queue/verify. |
| `SH04-EV-04` | HTTP 422 | `DESIGN_VALIDATION_ERROR`; body sai hoặc email không hợp lệ. | Không hiển thị accepted; không tạo input mới; thông báo/fallback cần duyệt. |
| `SH04-EV-05` | HTTP 500 | `DESIGN_INTERNAL_ERROR`; provider lỗi. | Thông báo an toàn; không lộ upstream detail, không hiển thị 503 giả. |
| `SH04-EV-06` | Timeout/mạng/body không đọc được | Không có response đáng tin cậy sau dispatch. | Kết quả chưa rõ; không retry tự động. |
| `SH04-EV-07` | Click quay lại | Khách chọn #6. | Điều hướng đề xuất SH-02 `/login`; không gọi API. |
| `SH04-EV-08` | QA mock control/copy cURL | Controls #2/#7 trong code.html. | Loại khỏi sản phẩm; chỉ là JavaScript cục bộ, không phải API event. |
| `SH04-EV-09` | Provider response chưa ánh xạ | HTTP 202 có status khác accepted; reason tùy chọn không được hiển thị khi semantics chưa duyệt. | Không gán semantics; không claim delivery/verification; yêu cầu owner duyệt mapping. |

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

- Kế hoạch này được rà soát trước khi cập nhật DD/marker artifact và ghi rõ một màn hình duy nhất.
- DD, kế hoạch, nhật ký công việc và nhãn số chú thích do phiên này tạo dùng tiếng Việt; tên API, trường, giá trị JSON và đường dẫn giữ nguyên chính tả kỹ thuật.
- Có đúng 12 số trên ảnh chú thích; mỗi số khớp bảng tại §3, DD và JSON marker với ID ổn định `SH04-EL-01..12`.
- Có chín Event ID `SH04-EV-01..09`; DD mô tả trigger/type, precondition, input, processing, output và kết quả/ngoại lệ cho từng event.
- PNG/HTML nguồn giữ nguyên SHA-256 nêu tại §2; ảnh chú thích giữ đúng tỷ lệ khung hình.
- DD phân biệt trạng thái API thật với các trạng thái mô phỏng; không tuyên bố gửi thư, vào hàng đợi hoặc xác minh thành công.
- Các liên kết cục bộ hoạt động; bảng theo dõi giữ riêng DD, implementation và runtime status.
- Chỉ rà soát tĩnh; không chạy kiểm thử dự án và không tuyên bố tích hợp/triển khai.

## 7. Trạng thái nguồn sau rà soát

- `screen.png`: 1600×1280; hash được ghi tại §2. `screen_annotated.png`: 3200×2560; 12 marker hiện hữu quan sát rõ, không che nội dung chính. Giữ ảnh chú thích và mở rộng JSON bằng `screen_id`, `element_id`, coordinate basis/origin/unit.
- `code.html`: các nút mock chỉ thay DOM/JSON cục bộ; không có request API. Nút cURL dựng endpoint/body không đúng API #02.
- API #02 route/view/validator/provider/test source hiện diện. Route công khai trả 202 khi provider trả; validator yêu cầu raw JSON integer cho `user_id`, chuẩn hóa email; không có DB, ownership lookup, queue, retry worker hoặc verify endpoint. Provider mặc định trả `accepted` mà không gửi email/tạo token.
- API #02 contract và OPEN_QUESTIONS còn Draft; trigger/owner, 202 semantics, provider/token lifecycle, user-email binding, public abuse control, status/reason enum, email normalization và int64 range chưa khóa.

## 8. Kế hoạch tái rà soát ngày 2026-11-07

### Phát hiện hiện hành trước khi sửa DD

- **Phạm vi phiên:** chỉ SH-04. Rà soát lại `list_screen.md`, F01/AC-01, API catalog #02, source/API DD, SH-03 handoff, asset gốc và bản DD hiện tại. Không sửa API, HTML, ảnh gốc, marker JSON hoặc màn hình khác.
- **Context Study Web:** `.agents/web-work/study/AGENTS.md` và `INDEX.md` hiện tồn tại, được manifest đăng ký; tuy nhiên `apps/study-client/src`, router và `package.json` vẫn vắng mặt. Dòng DD nói context con không tồn tại là tài liệu lỗi thời; runtime UI vẫn `UNWIRED`.
- **API #01 / handoff:** source INSERT trả các field hồ sơ `id`/`email`, commit trước khi ghi log `verification_dispatch_pending`; API #01 không gọi API #02. SH-03 DD đã ghi rõ ánh xạ `data.id`/`data.email` nhưng cơ chế vận chuyển sang SH-04 còn chưa quyết định.
- **Tài khoản và SH-02:** API #01 INSERT không gán `status`; checked-in `infra/postgres/study-server/DB.sql` có default `ACTIVE`; API #03 từ chối login nếu returned status khác `ACTIVE`. Đây không chứng minh live schema hay status được cập nhật bởi verification; không kết luận tài khoản chưa xác minh được phép/bị cấm đăng nhập.
- **API #02 hiện tại:** endpoint public, không mở DB; model nhận `user_id:int` và `email:str`; validator đòi kiểu integer JSON thô, trim/kiểm tra email; module chưa kiểm tra miền `int64` như catalog. View gọi provider đồng bộ, HTTP 202 `DESIGN_OPERATION_ACCEPTED`, map `status` và `reason` tùy chọn; provider mặc định chỉ trả `accepted`. 422 là validation, 500 là lỗi provider đã được làm an toàn.
- **Contract/API discrepancy:** API catalog gọi API #02 khi verification bật; F01/AC-01 đặt dispatch sau đăng ký và diagram có provider/log/retry. API #02 DD Q-02-01/Q-02-02 vẫn để open owner/feature gate, acceptance/retry, còn source không có queue/retry worker. `ActionResult.status` là chuỗi tổng quát và `reason` tùy chọn; semantics chưa chốt. Giữ trạng thái unknown thay vì tự ánh xạ giá trị provider.
- **Artifact audit:** `screen.png` 1600×1280 và `code.html` giữ hash trong plan; `screen_annotated.png` 3200×2560 đã xem; JSON có 12 marker có ID ổn định và tọa độ nguồn. HTML chỉ mô phỏng state/cURL và không có network call. Giữ nguyên ảnh/HTML/overlay/JSON nếu static audit cuối không phát hiện lỗi.
- **DD gap:** bản DD hiện có 12 element và 8 event nhưng chưa có crosswalk A–F; event chưa tách nhãn `Kết quả / ngoại lệ`; §1.1 còn câu context `NOT_FOUND`; link worklog trỏ phiên cũ.

### Thứ tự thay đổi đã ghi trước DD

1. Cập nhật DD: sửa trạng thái context, phân biệt API catalog `int64` với validator source, ghi rõ `reason` tùy chọn và status/reason semantics còn mở; giữ rõ account status/login policy cross-screen chưa xác định.
2. Thêm crosswalk A–F và kết quả/ngoại lệ cho từng event; bổ sung event riêng cho provider status chưa được contract ánh xạ (không thay đổi 12 marker trên ảnh).
3. Giữ `DD BLOCKED` vì trigger/owner, handoff transport và status semantics chưa chốt; giữ riêng `IMPLEMENTATION BLOCKED` và `RUNTIME NOT VERIFIED`.
4. Cập nhật hàng SH-04 và checkpoint trong tracker, hoàn thiện worklog hiện tại.

**Gate trước DD edit:** kế hoạch này đã ghi lại bằng chứng hiện hành và phạm vi thay đổi; chỉ sau điểm này mới cập nhật `SH-04.md`.

### Kết quả tái rà soát và verification

- DD sửa claim sai về context Study Web, bổ sung điều kiện trước/sau và crosswalk A–F; giữ rõ app source/router `UNWIRED`.
- DD ghi current API #02/provider, optional `reason`, int64 validation discrepancy, dispatch owner/trigger, SH-03 handoff, AC-01 queue/retry discrepancy, cùng status/login gate SH-02 chưa thể kết luận.
- DD có 12 element khớp 12 marker và 9 event `SH04-EV-01..09`; từng event có Element/type, precondition, input, processing, output và kết quả/ngoại lệ. Các nhánh status provider chưa được duyệt không bị gán nghĩa.
- `screen.png` và `code.html` giữ nguyên hash; ảnh gốc và annotation được xem lại; JSON bounds/IDs và local DD links hợp lệ. Không sửa screen assets, marker JSON hay HTML.
- Static audit đạt: 12/12 marker-element mapping, coordinates in bounds, hashes, 9/9 event structure, 6/6 A–F rows, local links, `git diff --check` và authored-text whitespace scan.
- Không chạy application tests, Study Web runtime, database hoặc deployment. Trạng thái cuối: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
