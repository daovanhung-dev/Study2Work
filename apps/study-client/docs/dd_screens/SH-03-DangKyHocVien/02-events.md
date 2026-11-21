# SH-03 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `SH-03-EV-001` | `SH03-EV-01` / `SH03-EV-01` — Mở trang đăng ký | See source event detail below |
| `SH-03-EV-002` | `SH03-EV-02` / `SH03-EV-02` — Nhập họ tên, email và mật khẩu | See source event detail below |
| `SH-03-EV-003` | `SH03-EV-03` / `SH03-EV-03` — Gửi yêu cầu tạo tài khoản | See source event detail below |
| `SH-03-EV-004` | `SH03-EV-04` / `SH03-EV-04` — Tạo thành công và chuyển sang SH-04 | See source event detail below |
| `SH-03-EV-005` | `SH03-EV-05` / `SH03-EV-05` — Email đã tồn tại | See source event detail below |
| `SH-03-EV-006` | `SH03-EV-06` / `SH03-EV-06` — Dữ liệu bị từ chối | See source event detail below |
| `SH-03-EV-007` | `SH03-EV-07` / `SH03-EV-07` — Lỗi máy chủ hoặc kết nối | See source event detail below |
| `SH-03-EV-008` | `SH03-EV-08` / `SH03-EV-08` — Mở SH-02 | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Các bước mô tả luồng đích; ghi chú `Current source` bên dưới từng event là bằng chứng hiện trạng.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 5. Sự kiện và xử lý dữ liệu

### `SH03-EV-01` — Mở trang đăng ký

- **Element / loại:** route trang công khai, các phần tử `SH03-EL-01..07` · Load/navigation.
- **Điều kiện tiên quyết:** Khách mở route công khai `/register`. Route hiện được khai báo trong `features/shared/shared.route.ts`; app-route unit test xác nhận trang được render.
- **Đầu vào:** đường dẫn và nguồn điều hướng (nếu có); không có token, query dữ liệu biểu mẫu hoặc dữ liệu API ban đầu.
- **Xử lý:** hiển thị trang và biểu mẫu rỗng theo thiết kế; không phát request.
- **Đầu ra:** trạng thái ban đầu/idle. Không thể xác minh runtime hiện tại.

1. Khách mở đường dẫn đề xuất `/register` từ SH-01, SH-02 hoặc liên kết được duyệt.
2. Giao diện hiển thị các phần tử #1–#7 ở trạng thái ban đầu; không yêu cầu token và không nạp dữ liệu ban đầu.
3. Current Angular source render form presentation; unit test và Chrome headless xác nhận route local ở desktop/mobile. Deployment vẫn chưa được xác minh.

**Kết quả / ngoại lệ:** Kết quả: hiển thị form rỗng, không gọi API lúc tải trang. Current source cho phép submit và gọi API #01 sau khi hợp lệ; route/unit tests không chứng minh browser runtime/deployment.

### `SH03-EV-02` — Nhập họ tên, email và mật khẩu

- **Element / loại:** `SH03-EL-03`, `SH03-EL-04`, `SH03-EL-05` · Input/change.
- **Điều kiện tiên quyết:** biểu mẫu đang idle và các trường được bật.
- **Đầu vào:** `fullname`, `email`, `password` dạng chuỗi do Khách nhập; mật khẩu là dữ liệu nhạy cảm.
- **Xử lý:** giữ nháp trong state cục bộ; có thể kiểm tra sớm theo quy tắc đã nêu, nhưng API #01 vẫn là nguồn quyết định cuối. Không gửi request khi nhập.
- **Đầu ra:** giá trị biểu mẫu cục bộ và lỗi sớm nếu có; không ghi log, URL hoặc analytics.

1. Nhập liệu được giữ trong trạng thái cục bộ của biểu mẫu cho tới khi gửi.
2. Kiểm tra phía giao diện để báo sớm trường trống/sai định dạng email và giới hạn họ tên theo mã nguồn API. API vẫn là thẩm quyền cuối cùng.
3. Không áp quy tắc email theo miền, mật khẩu 8 ký tự, CAPTCHA, OTP hoặc điều khoản khi chưa có hợp đồng.
4. Không ghi các giá trị vào log, URL, sự kiện phân tích hoặc thông báo lỗi. Đặc biệt không lưu mật khẩu vào trạng thái điều hướng sang SH-04.

**Kết quả / ngoại lệ:** Kết quả: các giá trị chỉ ở state biểu mẫu cục bộ; không phát sinh request khi nhập. Ngoại lệ: rule sớm của client không được vượt quá contract; kiểm tra cuối do API #01 quyết định.

### `SH03-EV-03` — Gửi yêu cầu tạo tài khoản

- **Element / loại:** `SH03-EL-06` hoặc submit bằng bàn phím · Submit/API.
- **Điều kiện tiên quyết:** chưa có request đang chờ; đủ ba trường theo request; route công khai. API không yêu cầu `Authorization`.
- **Đầu vào:** `fullname`, `email`, `password`; JSON chỉ gồm `email`, `password`, `full_name`.
- **Xử lý:** khóa submit lặp, ánh xạ `fullname` → `full_name`, gửi `POST /api/v1/auth/register`; API validator trim/kiểm tra, truy vấn trùng, băm Argon2id, insert và commit. Không thêm Bearer, role, status hoặc trường chưa có hợp đồng.
- **Đầu ra:** HTTP 201/409/422/500 hoặc kết quả mạng chưa rõ; xử lý chi tiết tương ứng ở `SH03-EV-04..07`. Không có idempotency key trong contract.

1. Kích hoạt nút #6 hoặc gửi biểu mẫu bằng bàn phím.
2. Chặn thao tác lặp; cắt khoảng trắng hai đầu họ tên, kiểm tra email và tạo JSON `{email, password, full_name}`. Giữ nguyên chuỗi mật khẩu.
3. Gửi `POST /api/v1/auth/register` tới địa chỉ gốc Study API được cấu hình ở phía giao diện. Không có địa chỉ gốc trong bản làm việc; không tự điền giá trị mẫu vào tài liệu.
4. Không thêm Bearer token, cookie/phiên, query string hoặc trường `role` vào yêu cầu.
5. Trong mã nguồn hiện tại, bộ định tuyến tạo `RegisterRequest` rồi gọi `create_user`; lớp điều phối kiểm tra dữ liệu trước truy vấn, tìm email trùng, băm mật khẩu Argon2id, gọi `INSERT_USER`, `commit` và dựng khung phản hồi. Nếu có lỗi, lớp này gọi `rollback` và trả lỗi an toàn.
6. Giao diện chuyển theo §3.3. HTML gốc hiện chỉ gọi `preventDefault()` nên không có yêu cầu mạng nào được gửi từ bản mẫu.

**Kết quả / ngoại lệ:** Kết quả: một POST #01 đang chờ và nút bị khóa; response được chuyển đúng một trong EV-04..07. Ngoại lệ: validation cục bộ không đạt thì không gửi; timeout/mất phản hồi không tự gửi lại do lần đầu có thể đã commit.

**Current source:** `SH03RegistrationService` gọi `StudyApiService` với `STUDY_SERVER_APIS.API_001`; body chỉ gồm `{email, password, full_name}`. Tên/email được trim; mật khẩu được giữ nguyên. Client kiểm tra required, định dạng email sau trim và độ dài tên/email; API vẫn quyết định cuối cùng. Không gửi Bearer, role hay status.

### `SH03-EV-04` — Tạo thành công và chuyển sang SH-04

- **Element / loại:** response từ `SH03-EV-03` · API response/navigation.
- **Điều kiện tiên quyết:** HTTP 201 và `businessCode="DESIGN_RESOURCE_CREATED"`.
- **Đầu vào:** `data.id`, `data.email` trong hồ sơ công khai API #01.
- **Xử lý:** kiểm tra shape; ánh xạ `data.id` → `user_id` và `data.email` → `email`, rồi chuyển sang SH-04 theo transport tạm được duyệt khi quyết định đó có. Không gọi API #02 ở SH-03; không coi account/email đã xác minh.
- **Đầu ra:** route đích đề xuất `/register/verification` cùng contract dữ liệu `user_id`/`email`; transport chưa được chốt. Nếu thiếu field thì dừng an toàn và giữ mã truy vết.

1. Chỉ HTTP 201 cùng `DESIGN_RESOURCE_CREATED` được coi là tạo tài khoản thành công.
2. Lấy `data.id` và `data.email`; không dùng ID từ dữ liệu nhập hoặc URL.
3. Đích là `/register/verification` với payload contract chỉ gồm `user_id` và `email`. Cơ chế truyền tạm và xử lý tải lại/mở trực tiếp cần được chốt trước khi nối hai màn hình; không lưu vào URL.
4. SH-04 gọi API #02. SH-03 không tự gửi yêu cầu thứ hai và không hiển thị “đã gửi email” hay “đã xác minh”.
5. Nếu thiếu `data.id`/`data.email` trong phản hồi dù mã trạng thái báo thành công, không dựng `user_id` thay thế; dừng chuyển tiếp an toàn và ghi mã truy vết để hỗ trợ.

**Kết quả / ngoại lệ:** Kết quả: chỉ 201 `DESIGN_RESOURCE_CREATED` với `data.id` và `data.email` mới đủ dữ liệu bàn giao sang SH-04. Ngoại lệ: thiếu/sai shape thì dừng an toàn; không tạo ID/email thay thế. Cơ chế truyền và xử lý mở trực tiếp/tải lại SH-04 vẫn cần quyết định.

**Current source (2026-11-20):** chỉ HTTP 201 cùng `success=true`, `DESIGN_RESOURCE_CREATED`, `data.id` là số nguyên dương an toàn cho JavaScript và `data.email` là chuỗi không rỗng mới hiển thị trạng thái “Đã tạo tài khoản” tại SH-03 và xóa mật khẩu khỏi form. Sai shape giữ form và hiện thông báo kết quả chưa xác định. Nút tiếp tục đặt ID/email vào one-use in-memory service rồi điều hướng tới SH-04; SH-03 không gọi API #02. Email chưa được xác nhận gửi/xác minh.

### `SH03-EV-05` — Email đã tồn tại

- **Element / loại:** response từ `SH03-EV-03`, trường `SH03-EL-04` · API error mapping.
- **Điều kiện tiên quyết:** HTTP 409, `businessCode="DESIGN_STATE_CONFLICT"`.
- **Đầu vào:** envelope lỗi và `traceId` nếu có; không có mật khẩu trong phản hồi cần ánh xạ.
- **Xử lý:** giữ biểu mẫu, gắn thông báo với email, cung cấp liên kết SH-02; không điều hướng tự động.
- **Đầu ra:** trạng thái conflict có thể sửa hoặc rời trang qua `SH03-EV-08`.

1. Với HTTP 409 `DESIGN_STATE_CONFLICT`, giữ dữ liệu đang có và đánh dấu email.
2. Hiển thị thông báo chung từ API “Email đã tồn tại.”; không xóa mật khẩu tự động nếu chính sách xóa dữ liệu chưa chốt, nhưng không hiển thị lại giá trị mật khẩu ngoài điều khiển nhập.
3. Cho phép sửa email hoặc mở SH-02 bằng liên kết #7. Không tự chuyển người dùng khỏi biểu mẫu.

**Kết quả / ngoại lệ:** Kết quả: lỗi conflict được gắn với email, giữ form và người dùng có thể sửa hoặc mở SH-02. Ngoại lệ: không tự chuyển trang; race ở unique constraint cũng cùng 409 theo source.

**Current source:** HTTP 409 `DESIGN_STATE_CONFLICT` gắn thông báo an toàn “Email đã tồn tại.” với trường email, giữ các giá trị đã nhập và focus email.

### `SH03-EV-06` — Dữ liệu bị từ chối

- **Element / loại:** response từ `SH03-EV-03`, các trường `SH03-EL-03..05` · API error mapping.
- **Điều kiện tiên quyết:** HTTP 422, `businessCode="DESIGN_VALIDATION_ERROR"`.
- **Đầu vào:** `meta.fieldErrors` và thông báo an toàn trong envelope.
- **Xử lý:** ánh xạ tên field API về element tương ứng (`full_name` → #3); hiển thị lỗi có chữ và hỗ trợ truy cập; giữ giá trị sửa được. Không tự thêm rule mật khẩu 8 ký tự.
- **Đầu ra:** trạng thái validation error; không chuyển trang, không phát request phụ.

1. Với HTTP 422 `DESIGN_VALIDATION_ERROR`, đọc danh sách `meta.fieldErrors`.
2. Ánh xạ `full_name`, `email`, `password` vào đúng điều khiển; hiển thị lỗi bằng chữ, biểu tượng chỉ bổ trợ và đặt liên kết trợ năng giữa lỗi với trường.
3. Giữ các giá trị có thể giữ an toàn. Không dùng thông báo HTML “tối thiểu 8 ký tự” cho tới khi yêu cầu và máy chủ cùng xác nhận quy tắc đó.

**Kết quả / ngoại lệ:** Kết quả: lỗi 422 ánh xạ theo `field` và giữ dữ liệu an toàn để sửa. Ngoại lệ: field không ánh xạ được dùng lỗi chung; không áp giới hạn 8 ký tự chỉ có trong HTML.

**Current source:** `meta.fieldErrors` cho `full_name`/`fullname`, `email`, `password` được ánh xạ thành thông báo cục bộ; không render message thô từ server. Nếu không có field ánh xạ được, hiển thị lỗi chung.

### `SH03-EV-07` — Lỗi máy chủ hoặc kết nối

- **Element / loại:** response/network từ `SH03-EV-03` · API error/transport failure.
- **Điều kiện tiên quyết:** HTTP 500, timeout/mất kết nối, hoặc HTTP thành công có body không đủ dữ liệu để bàn giao.
- **Đầu vào:** envelope an toàn/trace ID nếu có; transport failure có thể không chứa response.
- **Xử lý:** giữ biểu mẫu, thông báo lỗi an toàn; không lộ exception; không retry POST tự động vì commit có thể đã xảy ra. Retry do người dùng chủ ý cần được thể hiện rõ khi sản phẩm duyệt.
- **Đầu ra:** trạng thái lỗi máy chủ hoặc kết quả chưa rõ trên SH-03; không chuyển SH-04 nếu thiếu dữ liệu bàn giao.

1. HTTP 500 `DESIGN_INTERNAL_ERROR`: hiển thị thông báo an toàn, không phơi bày lỗi cơ sở dữ liệu, chi tiết bộ gửi thư hoặc dấu vết ngăn xếp.
2. Mất kết nối/timeout sau khi gửi: giữ biểu mẫu và thể hiện rằng kết quả chưa xác định. Không gửi lại tự động; một lần thử lại mù có thể gặp 409 dù lần gửi trước đã tạo tài khoản.
3. Dùng `traceId`/`X-Trace-Id` khi hỗ trợ xử lý lỗi; không đưa thông tin nhạy cảm vào thông báo người dùng.

**Kết quả / ngoại lệ:** Kết quả: lỗi an toàn hiển thị tại SH-03; không đi SH-04 nếu chưa xác nhận có đủ response data. Ngoại lệ: không retry tự động, vì response bị mất có thể xảy ra sau commit; response 2xx sai shape không được xem là thành công.

**Current source:** HTTP 500/nhánh lỗi khác hiển thị thông báo chung. Lỗi mạng status 0 nói rõ kết quả chưa xác định; không tự retry. HTTP 201 có envelope/code nhưng thiếu hoặc sai shape `data.id`/`data.email` cũng giữ form và hiển thị kết quả chưa xác định.

### `SH03-EV-08` — Mở SH-02

- **Element / loại:** `SH03-EL-07` · Click/navigation.
- **Điều kiện tiên quyết:** link hiển thị và route SH-02 `/login` đã được khai báo; route SH-03 local render đã kiểm tra, deployment chưa xác minh.
- **Đầu vào:** không có dữ liệu biểu mẫu hoặc thông tin xác thực được truyền.
- **Xử lý:** điều hướng nội bộ tới SH-02; không gọi API #01/#02 và không đưa giá trị trường vào URL/state.
- **Đầu ra:** SH-02 theo route `/login`; unit tests xác nhận route entries; browser smoke trong lát cắt này chỉ xác minh direct route `/register`, chưa kích hoạt link.

1. Khi kích hoạt liên kết #7, điều hướng tới `/login` theo thiết kế.
2. Không gửi API và không đưa nội dung biểu mẫu vào URL, trạng thái điều hướng hoặc dữ liệu đăng nhập.
3. `/login` được khai báo trong Shared route cùng SH-03; browser smoke chỉ mở `/register`, không kiểm tra tương tác link.

**Kết quả / ngoại lệ:** Kết quả: điều hướng tới route SH-02 `/login`, không gửi API và không chuyển dữ liệu biểu mẫu. Unit tests xác nhận route entries; browser smoke trong lát cắt này chỉ xác minh direct route `/register`, chưa kích hoạt link.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
