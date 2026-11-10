# SH-03 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `SH-03-API-001` | #01 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #01
- Orchestration/data notes: POST #1 → nhận user_id,email → SH-04; 409 email trùng trở lại form.
- BE/source status và gate: **R**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: 3. Truy vết API và dữ liệu

### 3.1. API #01 — Tạo tài khoản

| Thuộc tính | Giá trị theo mã nguồn hiện tại |
|---|---|
| Phương thức và đường dẫn | `POST /api/v1/auth/register` |
| Xác thực | Công khai; không cần `Authorization` |
| JSON bắt buộc | `email: string`, `password: string`, `full_name: string` |
| Phản hồi tạo thành công | HTTP `201`, `businessCode="DESIGN_RESOURCE_CREATED"` |
| Nhánh lỗi đã có nguồn | `409 DESIGN_STATE_CONFLICT`, `422 DESIGN_VALIDATION_ERROR`, `500 DESIGN_INTERNAL_ERROR` |
| Tác động dữ liệu | Tìm email trùng, băm mật khẩu Argon2id, chèn tài khoản vai trò `STUDENT`, rồi gọi `commit`. Giao dịch do lớp điều phối API #01 sở hữu. |
| Gửi email | Không gọi API #02; view chỉ ghi log rằng bước gửi xác minh bị trì hoãn. |

Dữ liệu JSON gửi đi chỉ có ba trường. `fullname` từ điều khiển HTML phải được đổi tên thành `full_name` khi dựng JSON:

```json
{
  "email": "<email người dùng>",
  "password": "<mật khẩu người dùng>",
  "full_name": "<họ và tên người dùng>"
}
```

Quy tắc theo bộ kiểm tra hiện tại:

- `email`: cắt khoảng trắng hai đầu, kiểm tra định dạng và giới hạn độ dài chuẩn hóa tối đa 255 ký tự. Không áp quy tắc miền email riêng hoặc tự đổi chữ hoa/thường.
- `full_name`: cắt khoảng trắng hai đầu; sau cắt phải dài 1–150 ký tự.
- `password`: chuỗi chỉ gồm khoảng trắng bị từ chối; khi hợp lệ, mật khẩu gốc được đưa đi băm Argon2id. API không đặt giới hạn tối thiểu 8 ký tự như thông báo ẩn trong HTML.
- Các trường thiếu hoặc sai kiểu được FastAPI ánh xạ thành HTTP 422 `DESIGN_VALIDATION_ERROR`; validator nghiệp vụ cũng trả HTTP 422 với `meta.fieldErrors`.

### 3.2. Phản hồi API #01

Khung phản hồi thành công theo `success_response` có `success`, `businessCode`, `message`, `data`, `meta` và `traceId`. `data` được trả từ hàng `RETURNING` của câu chèn và có các trường công khai sau:

```text
id, full_name, email, role, avatar_url, phone, status, created_at, updated_at
```

Mật khẩu và `password_hash` không được đưa vào phản hồi. API không trả access token hoặc refresh token. SQL hiện gán `role='STUDENT'`, nhưng bỏ cột `status`; giá trị `status` phụ thuộc lược đồ thực tế. `DB.sql` có giá trị mặc định `ACTIVE`, song tệp này không xác nhận lược đồ cơ sở dữ liệu đang chạy.

Để mở SH-04, luồng đích cần ánh xạ `data.id` thành `user_id` và dùng `data.email`. Danh mục yêu cầu hai giá trị này nhưng chưa khóa cơ chế truyền phía giao diện. Đây là hợp đồng dữ liệu bàn giao, chưa phải quyết định transport; không đưa email/ID vào query string hoặc lưu trữ bền vững khi chưa có policy. Mã giao diện/router vắng mặt nên không có pattern Vue được xác minh.

### 3.3. Lỗi API #01 và xử lý trên SH-03

| HTTP | Mã nghiệp vụ | Phản hồi/ý nghĩa theo mã nguồn | Cách xử lý đích |
|---:|---|---|---|
| 201 | `DESIGN_RESOURCE_CREATED` | Tài khoản đã được chèn và giao dịch đã gọi `commit`; `data` chứa hồ sơ công khai. | Chuyển sang SH-04 với `data.id` và `data.email`; không hiển thị trạng thái xác minh email. |
| 409 | `DESIGN_STATE_CONFLICT` | Email đã tồn tại; trường hợp vi phạm ràng buộc duy nhất trong lúc chèn cũng được ánh xạ thành mã này. | Giữ nội dung biểu mẫu, đánh dấu trường email và cung cấp liên kết SH-02. Thông báo hiện tại trong mã nguồn: “Email đã tồn tại.” |
| 422 | `DESIGN_VALIDATION_ERROR` | JSON/trường không hợp lệ; lỗi trường được đưa vào `meta.fieldErrors`. | Giữ dữ liệu, gắn lỗi với trường theo `field`; không hiện lời khuyên 8 ký tự nếu máy chủ chưa có quy tắc đó. |
| 500 | `DESIGN_INTERNAL_ERROR` | Lỗi cơ sở dữ liệu hoặc lỗi nội bộ; chi tiết nhạy cảm không được trả về phía giao diện. | Hiển thị thông báo chung, giữ dữ liệu và không đưa chi tiết lỗi máy chủ lên giao diện. |
| Không có phản hồi | Không có mã HTTP | Không biết yêu cầu đã tạo tài khoản hay chưa. API không khai báo khóa chống gửi lặp. | Thông báo kết quả chưa xác định; không tự gửi lại POST. Cho người dùng chọn bước tiếp theo có kiểm soát. |

Khung lỗi gồm `success=false`, `businessCode`, `message`, `data=null`, `meta` và `traceId`; lớp trung gian gắn `X-Trace-Id`. Không hiển thị thông tin cơ sở dữ liệu, dấu vết ngăn xếp hoặc nội dung mật khẩu.

### 3.4. API #02 — Ranh giới tại SH-04

SH-03 không gọi API này. Theo luồng F01, SH-04 mới gửi:

```http
POST /api/v1/auth/verify-email/send
Content-Type: application/json

{"user_id": <data.id>, "email": "<data.email>"}
```

API #02 hiện công khai, không phụ thuộc cơ sở dữ liệu và không kiểm tra sự tồn tại/sở hữu cặp `user_id`/`email`. Bộ gửi thư mặc định là `StubVerificationEmailProvider`, trả HTTP `202` với `businessCode="DESIGN_OPERATION_ACCEPTED"` và `data={"status":"accepted"}`; response từ provider khác có thể kèm `reason` tùy chọn. Điều này chỉ xác nhận bộ giả lập đã nhận yêu cầu; không có email thật, mã/liên kết xác minh, thời hạn, lần thử lại, thay đổi `users.status` hay đường dẫn hoàn tất xác minh. Nếu bộ gửi thư lỗi, API trả HTTP `500 DESIGN_INTERNAL_ERROR` an toàn.

### 3.5. Liên kết truy vết nguồn

| Chủ đề | Nguồn được đối chiếu |
|---|---|
| Screen ID, F01 và route đề xuất | [Danh mục màn hình](../../list_screen.md) |
| Luồng nghiệp vụ AC-01 | [Sơ đồ AC-01 Guest Account](../../../../study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) |
| API catalog và schema `UserProfile` | [Danh mục API](../../../../../docs/lists/list_api.md) |
| Đăng ký: route/request/response | [Router API v1](../../../../study-server/app/api/v1.py), [models](../../../../study-server/app/modules/guest/api_01_auth_register/models.py), [validator](../../../../study-server/app/modules/guest/api_01_auth_register/validate.py), [view](../../../../study-server/app/modules/guest/api_01_auth_register/view.py), [SQL query](../../../../study-server/app/modules/guest/api_01_auth_register/query.py) |
| Gửi email xác minh tại SH-04 | [API #02 validator](../../../../study-server/app/modules/guest/api_02_auth_verify_email_send/validate.py), [API #02 view](../../../../study-server/app/modules/guest/api_02_auth_verify_email_send/view.py), [provider mặc định](../../../../study-server/app/service/email/provider.py) |
| Kiểm thử nguồn (đã đọc, không chạy trong phiên này) | [API #01 tests](../../../../study-server/tests/modules/guest/api_01_auth_register/test_register.py), [API #02 tests](../../../../study-server/tests/modules/guest/api_02_auth_verify_email_send/test_verify_email_send.py) |
| Hợp đồng và câu hỏi chưa chốt | [API #01 open questions](../../../../study-server/docs/dd/01_auth_register/OPEN_QUESTIONS.md), [API #02 open questions](../../../../study-server/docs/dd/02_auth_verify_email_send/OPEN_QUESTIONS.md) |
| Khai báo DB trong repository; không phải live schema evidence | [Study Server DB.sql](../../../../../infra/postgres/study-server/DB.sql) |
| Quy tắc giao diện Study đích | [Study Web design guide](../../../../../.agents/web-study/design.md) |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/SH-03.md)
