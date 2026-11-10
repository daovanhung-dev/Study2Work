# SH-04 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `SH-04-EV-001` | `Source heading` / 6.1. Gửi yêu cầu | See source event detail below |
| `SH-04-EV-002` | `Source heading` / 6.2. Phản hồi thành công hiện tại | See source event detail below |
| `SH-04-EV-003` | `Source heading` / 6.3. Phản hồi lỗi | See source event detail below |
| `SH-04-EV-004` | `Source heading` / 6.4. Đặc tả sự kiện ổn định | See source event detail below |
| `SH-04-EV-005` | `SH04-EV-01` / `SH04-EV-01` — Mở route và đọc handoff | See source event detail below |
| `SH-04-EV-006` | `SH04-EV-02` / `SH04-EV-02` — Dispatch API #02 với handoff hợp lệ | See source event detail below |
| `SH-04-EV-007` | `SH04-EV-03` / `SH04-EV-03` — API trả accepted | See source event detail below |
| `SH-04-EV-008` | `SH04-EV-04` / `SH04-EV-04` — API trả lỗi dữ liệu 422 | See source event detail below |
| `SH-04-EV-009` | `SH04-EV-05` / `SH04-EV-05` — Provider/API trả lỗi 500 | See source event detail below |
| `SH-04-EV-010` | `SH04-EV-06` / `SH04-EV-06` — Timeout, lỗi mạng hoặc body không hợp lệ | See source event detail below |
| `SH-04-EV-011` | `SH04-EV-07` / `SH04-EV-07` — Quay lại SH-02 | See source event detail below |
| `SH-04-EV-012` | `SH04-EV-08` / `SH04-EV-08` — Điều khiển mock/copy cURL trong HTML nguồn | See source event detail below |
| `SH-04-EV-013` | `SH04-EV-09` / `SH04-EV-09` — Provider trả status/reason chưa được ánh xạ | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 6. Chuỗi sự kiện và ánh xạ phản hồi API

### 6.1. Gửi yêu cầu

| Thuộc tính | Đặc tả |
|---|---|
| Tác nhân kích hoạt | Theo F01, bước gửi xảy ra sau đăng ký thành công; thao tác cụ thể chưa được chốt. |
| Phương thức / đường dẫn | `POST /api/v1/auth/verify-email/send` (API #02). |
| Yêu cầu | `Content-Type: application/json`; phần thân gồm `user_id` lấy từ `data.id` và `email` lấy từ `data.email`. Không kèm `Authorization`. |
| Ví dụ phần thân | `{"user_id":1001,"email":"student@example.com"}`; giá trị chỉ để minh họa cấu trúc. |
| Thứ tự xử lý phía máy chủ | FastAPI đọc `VerifyEmailSendRequest` → bộ kiểm tra dữ liệu kiểm tra `user_id` nguyên nghiêm ngặt và chuẩn hóa địa chỉ → `VerificationEmailProvider.dispatch(user_id, email, trace_id)` → dựng cấu trúc phản hồi thành công/lỗi. |
| Cơ sở dữ liệu / tác động phụ | Không mở phiên cơ sở dữ liệu. Bộ gửi thư mặc định bỏ `user_id`, `email`, `trace_id`; không gửi thư, ghi hàng đợi, tạo OTP/liên kết hoặc cập nhật tài khoản. |
| Chống gửi lặp | Chưa có khóa chống yêu cầu trùng hoặc chính sách thử lại trong hợp đồng API. Giao diện không tự gửi lại khi chờ lâu hay khi kết quả mạng chưa rõ. |

### 6.2. Phản hồi thành công hiện tại

HTTP `202 Accepted` với cấu trúc phản hồi chuẩn:

```json
{
  "success": true,
  "businessCode": "DESIGN_OPERATION_ACCEPTED",
  "message": "Yêu cầu gửi email xác thực đã được chấp nhận.",
  "data": {
    "status": "accepted"
  },
  "meta": {},
  "traceId": "<mã do máy chủ cấp>"
}
```

Bộ gửi thư mặc định không trả `reason`, vì vậy `data` chỉ có `status`. Không thêm `delivery`, `provider`, `dispatched`, `otp_generated` hoặc `confirm_url` vào hợp đồng giao diện khi API chưa trả các trường này. 202 chỉ xác nhận bộ gửi thư đã tiếp nhận lời gọi.

View cũng thêm `data.reason` khi một provider trả giá trị này. Contract chưa định nghĩa enum hoặc cách hiển thị `reason`; ví dụ response ở trên là đúng với provider mặc định. Không render `reason` chưa được duyệt như một thông báo gửi thư.

### 6.3. Phản hồi lỗi

| HTTP | Mã nghiệp vụ | Nguồn | Xử lý trên giao diện đích |
|---:|---|---|---|
| 422 | `DESIGN_VALIDATION_ERROR` | Phần thân yêu cầu thiếu/sai kiểu hoặc địa chỉ thư điện tử không hợp lệ; lỗi chuẩn có `meta.fieldErrors` khi bộ kiểm tra dữ liệu tạo danh sách lỗi. | Hiển thị thông báo phù hợp; không ghi nhận là đã tiếp nhận. Vì không có ô nhập trên màn hình, cần rà soát lỗi bàn giao từ SH-03 thay vì tự tạo biểu mẫu OTP hoặc thư điện tử. |
| 500 | `DESIGN_INTERNAL_ERROR` | Bộ gửi thư phát sinh ngoại lệ; chi tiết từ dịch vụ bên ngoài được ẩn. | Hiển thị lỗi chung và cho phép điều hướng an toàn; không hiển thị 503, `SERVICE_OFFLINE` hoặc thông tin nội bộ từ HTML mẫu. |
| Không có HTTP phản hồi | Lỗi kết nối phía trình duyệt, nếu triển khai. | Nêu kết quả chưa xác định; không tự gửi lại. Hành vi này chưa có mã giao diện để xác minh. |

Không có bằng chứng API #02 trả HTTP 503 khi bộ gửi thư lỗi. Trạng thái “cổng xác nhận từ chối/lỗi bắt tay” trong HTML là mô phỏng cục bộ.

### 6.4. Đặc tả sự kiện ổn định

#### `SH04-EV-01` — Mở route và đọc handoff

- **Element / loại:** `SH04-EL-01`, `SH04-EL-03..05`, `SH04-EL-08..12` · route load.
- **Điều kiện tiên quyết:** Khách mở route đề xuất `/register/verification`. Route chưa được đăng ký trong Study Web source.
- **Đầu vào:** path và dữ liệu handoff dự kiến từ SH-03 gồm `data.id` và `data.email`; không nhận hai giá trị qua URL. Kênh truyền chưa được quyết định.
- **Xử lý:** 1) Nhận route và state chỉ từ kênh handoff được duyệt. 2) Kiểm tra đủ data.id/data.email và kiểu tương thích trước khi bật dispatch. 3) Không đọc/cất dữ liệu từ URL, local storage hoặc session storage theo giả định.
- **Đầu ra:** màn hình ở trạng thái chờ dispatch khi handoff đủ; nếu thiếu dữ liệu, không gọi API #02 và dùng fallback route/message sau khi sản phẩm chốt. Không có trạng thái runtime hiện tại.
- **Kết quả / ngoại lệ:** thiếu route hoặc handoff không hợp lệ → không dispatch; fallback chưa được duyệt. Event này không có API response.

#### `SH04-EV-02` — Dispatch API #02 với handoff hợp lệ

- **Element / loại:** transition vào SH-04, kết quả được trình bày ở `SH04-EL-03..04`, `SH04-EL-09` · API request.
- **Điều kiện tiên quyết:** API #01 trước đó trả HTTP 201 `DESIGN_RESOURCE_CREATED`; handoff gồm `data.id` và `data.email`; component sở hữu và thời điểm trigger được BA/BE/FE xác nhận. F01 giao dispatch cho SH-04 nhưng API DD Q-02-01 còn mở.
- **Đầu vào:** `user_id: int` lấy từ `data.id`, `email: string` lấy từ `data.email`; không lấy từ người dùng và không gửi `Authorization`.
- **Xử lý:** 1) Gửi một lần POST /api/v1/auth/verify-email/send với Content-Type application/json và body {user_id: data.id, email: data.email}, không kèm Authorization. 2) Route parse request; validator đòi user_id là JSON integer thô, trim/kiểm tra email, nhưng không áp miền int64 của catalog. 3) Với input hợp lệ, view gọi provider đồng bộ, không mở DB và không kiểm tra user/email binding. 4) View map provider status và reason tùy chọn vào data; provider mặc định trả accepted, không có reason. 5) Không có idempotency key, queue hoặc retry worker.
- **Đầu ra:** chuyển tới event response tương ứng theo HTTP/body. Không retry tự động khi timeout vì acceptance có thể không xác định. Dispatch trigger vẫn là blocker; không coi mock HTML là proof đã gọi API.
- **Kết quả / ngoại lệ:** HTTP 202 với status đã ánh xạ → response mapping; 422 → EV-04; provider exception → HTTP 500/EV-05; timeout/body không đọc được → EV-06; provider status chưa biết → EV-09. Không tuyên bố email đã gửi hoặc xác minh.

#### `SH04-EV-03` — API trả accepted

- **Element / loại:** response hiển thị ở `SH04-EL-03`, `SH04-EL-04`, `SH04-EL-09` · API response mapping.
- **Điều kiện tiên quyết:** HTTP 202, `success=true`, `businessCode="DESIGN_OPERATION_ACCEPTED"`, `data.status="accepted"`.
- **Đầu vào:** envelope API #02; `meta` mặc định rỗng, `traceId` do server cấp.
- **Xử lý:** 1) Kiểm tra HTTP 202, success, businessCode và data.status. 2) Chỉ khi status là accepted, đặt UI state accepted. 3) Hiển thị câu giải thích provider stub đã nhận lời gọi; bỏ qua reason chưa được duyệt. 4) Không suy ra delivery, queue, OTP/link, ownership hoặc email verification.
- **Đầu ra:** trạng thái “được bộ thử nghiệm tiếp nhận; thư chưa được gửi thật”; nút quay lại SH-02 vẫn khả dụng theo route được duyệt.
- **Kết quả / ngoại lệ:** body khớp → accepted; body thiếu/sai shape → EV-06; data.status khác accepted → EV-09. Không ghi trạng thái vào account hoặc xác minh email.

#### `SH04-EV-04` — API trả lỗi dữ liệu 422

- **Element / loại:** `SH04-EL-03..04`, `SH04-EL-09` · API error mapping.
- **Điều kiện tiên quyết:** HTTP 422 `DESIGN_VALIDATION_ERROR` do trường thiếu/sai kiểu hoặc email không hợp lệ.
- **Đầu vào:** error envelope và `meta.fieldErrors` nếu được tạo.
- **Xử lý:** 1) Phân loại HTTP 422 và DESIGN_VALIDATION_ERROR. 2) Đọc meta.fieldErrors nếu có để chẩn đoán handoff; không có ô chỉnh email/ID trên màn hình. 3) Xóa trạng thái pending; không retry request sai. 4) Không tự điều hướng tới SH-03 vì fallback route chưa được duyệt.
- **Đầu ra:** trạng thái dữ liệu handoff/request không hợp lệ; không gửi request tiếp theo.
- **Kết quả / ngoại lệ:** hiện lỗi an toàn và giữ outcome là thất bại validation; không hiển thị accepted. Nếu envelope không đọc được thì dùng EV-06.

#### `SH04-EV-05` — Provider/API trả lỗi 500

- **Element / loại:** `SH04-EL-03..04`, `SH04-EL-09` · API error mapping.
- **Điều kiện tiên quyết:** HTTP 500 `DESIGN_INTERNAL_ERROR`; provider `dispatch` ném exception.
- **Đầu vào:** safe error envelope, trace ID/header nếu có.
- **Xử lý:** 1) Phân loại HTTP 500/DESIGN_INTERNAL_ERROR. 2) Hiển thị lỗi chung, không render exception, provider detail, mock 503 hoặc SERVICE_OFFLINE. 3) Không tự gọi lại vì không có retry/idempotency contract.
- **Đầu ra:** trạng thái xử lý thất bại; điều hướng quay lại SH-02 vẫn là lựa chọn riêng, không biểu thị email đã gửi.
- **Kết quả / ngoại lệ:** lỗi provider được chuyển thành HTTP 500 an toàn; nếu không nhận được response thì dùng EV-06. Không ghi delivery hoặc verification success.

#### `SH04-EV-06` — Timeout, lỗi mạng hoặc body không hợp lệ

- **Element / loại:** `SH04-EL-03..04`, `SH04-EL-09` · transport/parser failure.
- **Điều kiện tiên quyết:** không nhận được response đáng tin cậy, hoặc 202/body thiếu `businessCode`/`data.status` cần thiết.
- **Đầu vào:** transport failure hoặc envelope không đúng shape; có thể không có `traceId`.
- **Xử lý:** 1) Phân biệt transport failure với response hợp lệ; body thiếu businessCode/data.status không được coi là success. 2) Giữ state kết quả chưa rõ. 3) Không tự retry vì API hiện không khai báo idempotency.
- **Đầu ra:** trạng thái kết quả chưa xác định; hành động retry/khôi phục cần quyết định sản phẩm.
- **Kết quả / ngoại lệ:** timeout, mất mạng hoặc body lỗi → unknown; không chuyển sang accepted khi body không parse được. Hướng xử lý lại cần được duyệt.

#### `SH04-EV-07` — Quay lại SH-02

- **Element / loại:** `SH04-EL-06` · click/navigation.
- **Điều kiện tiên quyết:** link quay lại hiển thị và router tương lai đăng ký `/login`.
- **Đầu vào:** không truyền `user_id`, email, password hoặc API response vào URL.
- **Xử lý:** 1) Nhận click trên link. 2) Điều hướng tới route /login của SH-02 nếu route được đăng ký. 3) Không gửi user_id, email hoặc response trong URL; không gọi API #02 và không thay đổi account state.
- **Đầu ra:** SH-02 theo route đề xuất. API #03 hiện từ chối user có `status != ACTIVE`; API #01 không đặt status, DDL mặc định ACTIVE chỉ là artifact checked-in và chưa có endpoint xác minh cập nhật status. Không khẳng định tài khoản chưa xác minh được phép hoặc bị chặn đăng nhập.
- **Kết quả / ngoại lệ:** route tồn tại → mở SH-02; route chưa có → runtime chưa thực hiện được và cần router/fallback được duyệt. Không coi điều hướng là login success.

#### `SH04-EV-08` — Điều khiển mock/copy cURL trong HTML nguồn

- **Element / loại:** `SH04-EL-02`, `SH04-EL-07`, `SH04-EL-10` · click mock-only.
- **Điều kiện tiên quyết:** chỉ trong HTML mẫu đang có; đây không phải hành vi product.
- **Đầu vào:** lựa chọn trạng thái giả hoặc lệnh cURL hard-coded.
- **Xử lý:** 1) Click mock control làm JavaScript đổi DOM/JSON cục bộ hoặc copy snippet. 2) Không phát network request. 3) Snippet có URL/body sai contract, nên loại khỏi product UI.
- **Đầu ra:** loại các controls khỏi giao diện khách; không coi mock 200/503/delivery/artifact fields là API response.
- **Kết quả / ngoại lệ:** chỉ thay đổi bản trình diễn tĩnh; không có server result. Không duy trì các nút QA này như hành vi người dùng.

#### `SH04-EV-09` — Provider trả status/reason chưa được ánh xạ

- **Element / loại:** SH04-EL-03, SH04-EL-04, SH04-EL-09 · API response mapping.
- **Điều kiện tiên quyết:** API trả envelope HTTP 202 hợp lệ nhưng data.status khác accepted. Nếu response có data.reason thì không hiển thị giá trị đó vì semantics chưa được duyệt. Contract khai báo status là string và reason tùy chọn; enum chưa có.
- **Đầu vào:** data.status:string, data.reason tùy chọn, businessCode DESIGN_OPERATION_ACCEPTED, traceId.
- **Xử lý:** 1) Không gán status ngoài allowlist hiện chưa tồn tại sang “đã gửi”, “đã xếp hàng” hoặc “đã xác minh”. 2) Không hiển thị reason thô cho Khách. 3) Đặt trạng thái nội bộ unmapped; lưu trace theo chính sách đã duyệt nếu cần chẩn đoán. 4) Không retry tự động.
- **Đầu ra:** trạng thái provider chưa ánh xạ; câu chữ người dùng và mapping cụ thể cần product/API owner duyệt trước khi triển khai.
- **Kết quả / ngoại lệ:** giữ outcome không xác định, không claim delivery/verification. Default stub không đi vào nhánh này; nhánh tồn tại do contract hiện cho phép chuỗi tự do.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
