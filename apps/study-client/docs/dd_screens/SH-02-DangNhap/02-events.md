# SH-02 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `SH-02-EV-001` | `SH02-EV-01` / SH02-EV-01 — Mở SH-02 và kiểm tra đích quay lại | See source event detail below |
| `SH-02-EV-002` | `SH02-EV-02` / SH02-EV-02 — Nhập email và mật khẩu | See source event detail below |
| `SH-02-EV-003` | `SH02-EV-03` / SH02-EV-03 — Bật/tắt hiện mật khẩu | See source event detail below |
| `SH-02-EV-004` | `SH02-EV-04` / SH02-EV-04 — Gửi đăng nhập | See source event detail below |
| `SH-02-EV-005` | `SH02-EV-05` / SH02-EV-05 — Xử lý lỗi kiểm tra trường #03 (422) | See source event detail below |
| `SH-02-EV-006` | `SH02-EV-06` / SH02-EV-06 — Xử lý thông tin đăng nhập sai (401) | See source event detail below |
| `SH-02-EV-007` | `SH02-EV-07` / SH02-EV-07 — Xử lý tài khoản không hoạt động (403) | See source event detail below |
| `SH-02-EV-008` | `SH02-EV-08` / SH02-EV-08 — Xử lý API 500, mất mạng hoặc phản hồi sai cấu trúc | See source event detail below |
| `SH-02-EV-009` | `SH02-EV-09` / SH02-EV-09 — Xử lý đăng nhập thành công theo nguồn và phân nhánh vai trò | See source event detail below |
| `SH-02-EV-010` | `SH02-EV-10` / SH02-EV-10 — Tải hồ sơ học viên hiện tại (#04) | See source event detail below |
| `SH-02-EV-011` | `SH02-EV-11` / SH02-EV-11 — Đánh giá #04/401 và chỉ khôi phục có điều kiện qua R-X01 | See source event detail below |
| `SH-02-EV-012` | `SH02-EV-12` / SH02-EV-12 — Xử lý #04 trả 403 / 500 | See source event detail below |
| `SH-02-EV-013` | `SH02-EV-13` / SH02-EV-13 — Chuyển tới đăng ký | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 5. Chi tiết sự kiện và xử lý dữ liệu

### SH02-EV-01 — Mở SH-02 và kiểm tra đích quay lại

- **Kích hoạt / loại:** Router điều hướng tới `/login` / Load.
- **Điều kiện tiên quyết:** Route công khai SH-02 được cấu hình; hiện chưa có router Study Web để xác minh.
- **Đầu vào:** Path `/login`, query hoặc route state do luồng bảo vệ cung cấp, gồm `returnTo` nếu có.
- **API / đầu ra:** Không gọi API. Hiển thị form rỗng và chỉ giữ đích quay lại sau khi kiểm tra theo chính sách allowlist còn chờ duyệt.

1. Router tương lai mở /login đề xuất. Router Study Web hiện không có, nên chưa xác nhận route chạy được.
2. Nếu route cần bảo vệ chuyển tới đây, chỉ đọc returnTo từ router state đáng tin cậy hoặc query tương đối qua danh sách cho phép. Từ chối URL tuyệt đối/tương đối mạng và đích ngoài danh sách route an toàn của vai trò đã xác thực.
3. Không sao chép token, mật khẩu hoặc email trong query vào route state. HTML gốc không có handler returnTo; đây là hành vi đích trong danh mục, không phải hành vi HTML hiện tại.
4. Hiển thị biểu mẫu ở trạng thái rảnh. screen.png trống; chỉ dùng bản dựng HTML sạch làm bằng chứng thiết kế.

**Kết quả / ngoại lệ:** Form rỗng được hiển thị; đích quay lại không có hoặc không qua allowlist thì bị bỏ và người dùng ở lại `/login`. Router hiện chưa có trong app source để xác minh.

### SH02-EV-02 — Nhập email và mật khẩu

- **Kích hoạt / loại:** Người dùng nhập hoặc chỉnh SH02-EL-04/SH02-EL-05 / Input, Change.
- **Điều kiện tiên quyết:** Form đang hiển thị và không bị khóa bởi request đang gửi.
- **Đầu vào:** Chuỗi email và mật khẩu do người dùng nhập; trạng thái mặc định của hai trường là rỗng.
- **API / đầu ra:** Không gọi API khi gõ. Cập nhật giá trị UI cục bộ; chuẩn hóa/kiểm tra cuối cùng theo #03 khi gửi.

1. Người dùng nhập vào điều khiển SH02-EL-04 và SH02-EL-05; trạng thái biểu mẫu ở cục bộ tới khi gửi.
2. required/type=email của trình duyệt có thể chặn dữ liệu hiển nhiên chưa đầy đủ. Không thêm quy tắc độ phức tạp hoặc sửa mật khẩu.
3. Khi gửi, đưa email vào yêu cầu #03. Máy chủ hiện loại khoảng trắng/kiểm tra định dạng và <=255 ký tự. Client có thể loại khoảng trắng email nếu kết quả giữ đúng hành vi hiện tại; DD này không khẳng định xử lý chữ hoa/thường.
4. Giữ nguyên byte/chuỗi mật khẩu. Máy chủ chỉ kiểm tra password.strip() để phát hiện chuỗi toàn khoảng trắng, sau đó xác minh nguyên giá trị với hash đã lưu.
5. Không lưu hai trường vào returnTo, log, sự kiện analytics hay ảnh chụp. Việc xóa mật khẩu sau kết quả là quyết định chính sách phiên/quyền riêng tư cần chốt trước khi triển khai.

**Kết quả / ngoại lệ:** Giá trị ở trạng thái form cục bộ và chưa phát sinh request; validation gốc của trình duyệt có thể chặn submit. Thời điểm xóa mật khẩu sau kết quả vẫn chờ policy.

### SH02-EV-03 — Bật/tắt hiện mật khẩu

- **Kích hoạt / loại:** Bấm hoặc nhấn phím kích hoạt SH02-EL-06 / Click, Keyboard.
- **Điều kiện tiên quyết:** Nút hiện mật khẩu được hiển thị và có thể thao tác.
- **Đầu vào:** Trạng thái hiển thị hiện tại của trường #5 và giá trị mật khẩu đang giữ.
- **API / đầu ra:** Không gọi API. Đổi thuộc tính hiển thị giữa `password` và `text`, giữ nguyên giá trị và focus hợp lý.

1. Bấm hoặc kích hoạt bằng bàn phím marker #6.
2. Đổi kiểu hiển thị trường mật khẩu giữa password và text; giữ nguyên chính xác giá trị.
3. Cập nhật tên/trạng thái trợ năng và focus mà không gửi biểu mẫu.
4. Không có yêu cầu API hay thay đổi trạng thái máy chủ. HTML hiện tham chiếu togglePasswordVisibility() nhưng không định nghĩa; đây mới là placeholder của bản mẫu.

**Kết quả / ngoại lệ:** Khi có handler, chỉ thay cách hiển thị và giữ nguyên giá trị/focus. HTML hiện gọi hàm chưa định nghĩa, nên chưa xác nhận tương tác runtime.

### SH02-EV-04 — Gửi đăng nhập

- **Kích hoạt / loại:** Submit form qua SH02-EL-07 hoặc Enter trong trường / Submit.
- **Điều kiện tiên quyết:** Không có request #03 đang chờ; kiểm tra cục bộ của trình duyệt cho phép gửi. Tài khoản/quyền vẫn do server quyết định.
- **Đầu vào:** `email: string`, `password: string` từ #4/#5; email chuẩn hóa theo validator nguồn khi gửi, mật khẩu giữ nguyên.
- **API / đầu ra:** `POST /api/v1/auth/login`, public/no Bearer, JSON `{email,password}`; request/response hiện tại và sai khác chuẩn được mô tả tại §3.1–3.2. Loading khóa submit; kết quả phân sang SH02-EV-05..09. Không tự retry khi timeout không rõ kết quả.

1. Chặn gửi lặp khi yêu cầu đang chờ. Tạo JSON chỉ từ hai trường biểu mẫu có tên: {email,password}.
2. Gửi POST /api/v1/auth/login tới địa chỉ gốc Study API sẽ được cấu hình trong tương lai. Checkout này chưa có địa chỉ gốc client; không tự điền vào DD.
3. Không gửi thông tin đăng nhập trong query và không gắn Authorization vào yêu cầu đăng nhập công khai này.
4. Máy chủ kiểm tra/chuẩn hóa email, từ chối mật khẩu chỉ có khoảng trắng, tìm người dùng theo email chuẩn hóa, xác minh mật khẩu, kiểm tra status == ACTIVE, cấp JWT + refresh token opaque, lưu hash refresh rồi commit. Xác thực thuộc máy chủ; quyết định vai trò phía client không thay thế được.
5. Ánh xạ phản hồi theo §3.2 và giữ nguyên sai khác chuẩn/nguồn. Không ghi giá trị nhạy cảm vào log/tóm tắt lỗi.
6. Nếu client mất phản hồi sau khi gửi, kết quả không xác định vì nguồn không có khóa idempotency cho đăng nhập. Không tự gửi lại POST; cần hành động khôi phục an toàn và chính sách thử lại do Sản phẩm/máy chủ duyệt.

**Kết quả / ngoại lệ:** Submit hợp lệ tạo một POST đang chờ; validation cục bộ không hợp lệ thì không gửi. Timeout không tự retry; phản hồi 200 hiện tại vẫn bị chặn bởi discrepancy hợp đồng #03.

### SH02-EV-05 — Xử lý lỗi kiểm tra trường #03 (422)

- **Kích hoạt / loại:** Nhận response HTTP 422 từ lần gửi #03 / API response.
- **Điều kiện tiên quyết:** SH02-EV-04 đã gửi request và chưa xử lý kết quả.
- **Đầu vào:** Envelope lỗi nguồn hiện tại, gồm `meta.fieldErrors[]` với `field`, `code`, `message` nếu được cung cấp và `traceId`.
- **API / đầu ra:** Không gọi API tiếp. Gắn lỗi vào SH02-EL-04/SH02-EL-05 hoặc vùng SH02-EL-03; giữ email, không nhắc lại mật khẩu, cho phép sửa và submit mới do người dùng chủ động.

1. Đọc meta.fieldErrors[] từ envelope lỗi Study hiện tại; mỗi chi tiết có thể gồm field, code, message.
2. Gắn lỗi email với #4, mật khẩu với #5; focus trường sai đầu tiên, giữ giá trị không bí mật.
3. Nếu không có ánh xạ trường, hiển thị lỗi cấp biểu mẫu ở #3. Không tự đặt chính sách mật khẩu hoặc thay mã máy chủ bằng quy tắc đoán.
4. error_response hiện tuần tự hóa data lỗi bị lược thành JSON null, đồng thời gửi traceId trong body và header X-Trace-Id. Giao diện có thể hiện trace ID trong phần trợ giúp, không đưa stack/DB nội bộ ra màn hình.

**Kết quả / ngoại lệ:** Field error hợp lệ được ánh xạ về trường; thiếu hoặc không ánh xạ được thì dùng lỗi chung. Không hiển thị body sai cấu trúc hoặc thông báo nội bộ thô.

### SH02-EV-06 — Xử lý thông tin đăng nhập sai (401)

- **Kích hoạt / loại:** Nhận HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED` từ #03 / API response.
- **Điều kiện tiên quyết:** Đang xử lý kết quả SH02-EV-04; đây là 401 credential của login, không phải 401 từ API được bảo vệ.
- **Đầu vào:** Envelope lỗi #03; nguồn dùng cùng thông báo cho email không tồn tại và mật khẩu sai.
- **API / đầu ra:** Không gọi refresh hoặc API khác. Hiện lỗi chung tại SH02-EL-03, không tiết lộ trường/tài khoản; cho người dùng sửa và gửi lại.

1. #03 hiện dùng cùng HTTP 401 DESIGN_AUTHENTICATION_REQUIRED và thông báo chung “email hoặc mật khẩu không đúng” cho email không tồn tại và mật khẩu sai.
2. Hiện một lỗi chung cấp biểu mẫu. Không tiết lộ trường/tài khoản nào tồn tại và không gọi refresh: 401 của thông tin đăng nhập #03 không phải token truy cập hết hạn.
3. Có thể giữ email theo chính sách; chỉ xóa mật khẩu sau khi kết quả nếu chính sách phiên/quyền riêng tư được duyệt. Bản mẫu chưa có logic trạng thái.
4. Cho phép người dùng sửa và chủ động gửi lại; không tự thử lại.

**Kết quả / ngoại lệ:** Hiện lỗi credential chung, không tiết lộ tài khoản và không gọi refresh; giữ/xóa email hoặc mật khẩu theo chính sách riêng tư được duyệt.

### SH02-EV-07 — Xử lý tài khoản không hoạt động (403)

- **Kích hoạt / loại:** Nhận HTTP 403 `DESIGN_ACCESS_DENIED` từ #03 / API response.
- **Điều kiện tiên quyết:** #03 đã xác minh credential nhưng account status khác `ACTIVE` theo nguồn hiện tại.
- **Đầu vào:** Envelope lỗi #03; không có hồ sơ được trả về trong nhánh này.
- **API / đầu ra:** Không gọi #04/R-X01. Hiện thông báo an toàn tại SH02-EL-03 và ở lại SH-02; đường hỗ trợ chỉ dùng khi được duyệt.

1. #03 hiện trả 403 DESIGN_ACCESS_DENIED khi mật khẩu đúng nhưng trạng thái tài khoản khác ACTIVE.
2. Hiện thông báo khác với 401 theo yêu cầu danh mục nhưng dùng câu chữ đã duyệt, không tiết lộ dữ liệu tài khoản. Không gọi #04/R-X01 và không chuyển theo vai trò.
3. Giữ kết quả trên SH-02 hoặc chỉ đưa đường hỗ trợ đã duyệt; hợp đồng màn hình chưa có API khôi phục.

**Kết quả / ngoại lệ:** Hiện lỗi trạng thái tài khoản an toàn và ở lại SH-02; câu chữ/đích hỗ trợ không có contract nên không tự thêm.

### SH02-EV-08 — Xử lý API 500, mất mạng hoặc phản hồi sai cấu trúc

- **Kích hoạt / loại:** HTTP 500, lỗi transport/timeout, hoặc body không phân tích được sau SH02-EV-04 / API response, Network error.
- **Điều kiện tiên quyết:** Request #03 đã được gửi; với timeout, không biết chắc server đã commit refresh-token row hay chưa.
- **Đầu vào:** HTTP status/body nếu có, lỗi transport và trace ID nếu nguồn gửi.
- **API / đầu ra:** Không retry tự động. Hiện lỗi an toàn tại SH02-EL-03; body thành công sai shape không được dùng để lưu token. Cho phép lần gửi mới chỉ sau khi hết loading và do người dùng chủ động.

1. Hiển thị lỗi biểu mẫu an toàn ở #3, thêm trace ID nếu được gửi và không đưa chi tiết máy chủ thô ra ngoài.
2. Giữ email; không nhắc lại mật khẩu/token.
3. Với yêu cầu đăng nhập có kết quả gửi không rõ, không tự gửi lại. Chỉ cho gửi mới do người dùng chủ động sau khi xóa trạng thái chờ.
4. Nếu phản hồi không khớp hợp đồng chuẩn lẫn nguồn hiện tại, dừng xử lý phiên, không lưu trường có vẻ là token và báo lỗi hợp đồng để điều tra.

**Kết quả / ngoại lệ:** Giữ ở SH-02 với lỗi an toàn và trace ID nếu có; body không hợp lệ/unknown không được hiển thị thô và không kích hoạt gửi lại tự động.

### SH02-EV-09 — Xử lý đăng nhập thành công theo nguồn và phân nhánh vai trò

- **Kích hoạt / loại:** Nhận HTTP 200 thành công từ #03 / API response.
- **Điều kiện tiên quyết:** Body parse được theo nguồn hiện tại; chuẩn 201/UserProfile-only vẫn đang mâu thuẫn và chưa có quyết định hợp đồng.
- **Đầu vào:** `data` hồ sơ, `role`, `access_token`, `refresh_token`, `token_type`, thời hạn token theo response hiện tại.
- **API / đầu ra:** Không gọi API trước khi chốt contract và session policy. Ghi nhận kết quả là DISCREPANCY; nếu policy được duyệt thì STUDENT có thể tiếp tục SH02-EV-10, MENTOR/ADMIN dừng theo G-02.

1. Thành công nguồn hiện tại là HTTP 200 success=true, businessCode=DESIGN_RESOURCE_RETRIEVED; data có hồ sơ và trường Bearer token. Danh mục chuẩn vẫn ghi 201/chỉ hồ sơ. Ghi nhận DISCREPANCY; không tự chọn hợp đồng để sinh mã.
2. Trước khi lưu access/refresh token, cần duyệt chính sách lưu phiên và refresh cho Study Web. Mã apps/study-client hiện không có cơ chế lưu. Không tự chọn localStorage, sessionStorage, cookie hoặc bộ nhớ.
3. Nếu vai trò hồ sơ nguồn hiện tại là STUDENT và chính sách phiên được duyệt, tiếp tục SH02-EV-10.
4. Nếu vai trò là MENTOR hoặc ADMIN, dừng trước #04. G-02 chưa có endpoint hồ sơ tương thích hay route được duyệt. Không gọi endpoint /users/me dành cho học viên và không chuyển tới /student.
5. Nếu thiếu/không rõ vai trò hoặc trường token khác envelope nguồn hiện tại, không đánh dấu đăng nhập hoàn tất; hiện lỗi hợp đồng/phiên an toàn và không giữ token ngoài bộ quản lý phiên được duyệt.

**Kết quả / ngoại lệ:** Không lưu token hoặc điều hướng trước khi thống nhất contract/session policy. STUDENT chỉ có thể tiếp tục #04 sau phê duyệt; MENTOR/ADMIN dừng tại G-02.

### SH02-EV-10 — Tải hồ sơ học viên hiện tại (#04)

- **Kích hoạt / loại:** SH02-EV-09 đã xác nhận role STUDENT và bộ quản lý phiên được duyệt chấp nhận token / API request.
- **Điều kiện tiên quyết:** Có access token hợp lệ theo session policy; route/default destination chưa được triển khai.
- **Đầu vào:** Access token đã được bộ quản lý phiên cấp cho request; không có query/body/path params.
- **API / đầu ra:** `GET /api/v1/users/me`, `Authorization: Bearer <access_token>`, chỉ role STUDENT; HTTP 200 ánh xạ profile an toàn theo §3.3 và tiếp tục đích allowlist sau khi duyệt. Không tạo `permissions`/`bio`.

1. Sau khi bộ quản lý phiên chấp nhận token, gửi GET /api/v1/users/me với đúng một header Authorization: Bearer <access_token>.
2. Guard hiện kiểm tra chữ ký/claim, sub dạng số và roles có STUDENT trước khi truy vấn DB.
3. Với HTTP 200, ánh xạ id, full_name, email, role, avatar_url, phone, status, created_at, updated_at. Để trống permissions và bio vì #04 hiện không trả chúng.
4. Chỉ đối chiếu data.role với vai trò xác thực theo chính sách được duyệt sau này. Nguồn hiện không so sánh role/status DB với claim JWT; không âm thầm thêm luật phân quyền ở màn hình.
5. Đích: ưu tiên returnTo cùng miền đã kiểm tra theo danh sách cho phép; nếu không có thì /student là đích /student đề xuất cho học viên trong danh mục. Cả hai đều chưa có trong mã client hiện tại.

**Kết quả / ngoại lệ:** HTTP 200 ánh xạ đúng allowlist hồ sơ #04; đích vẫn chưa được duyệt/triển khai. #04/401 đi tới đánh giá có điều kiện ở EV-11; #04/403, 500 hoặc mạng đi tới EV-12.

### SH02-EV-11 — Đánh giá #04/401 và chỉ khôi phục có điều kiện qua R-X01

- **Kích hoạt / loại:** API #04 trong SH02-EV-10 trả HTTP 401 / API response.
- **Điều kiện tiên quyết:** Quyết định được duyệt cho phép refresh với mọi #04/401, hoặc API trả căn cứ phân loại lỗi đủ để xác định refresh phù hợp; chỉ khi đó mới cần refresh token trong bộ quản lý phiên được duyệt.
- **Đầu vào:** Response #04 hiện dùng HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED` cho cả auth/claim không hợp lệ và profile không tồn tại; nếu policy cho phép refresh thì body nguồn R-X01 là `{refresh_token: string}`.
- **API / đầu ra:** Mặc định chưa gọi API tiếp do nguyên nhân 401 không phân biệt được. Chỉ theo policy/contract được duyệt mới gọi `POST /api/v1/auth/refresh` (R-X01, chưa có ID catalog) tối đa một lần; nếu thành công thì retry #04 đúng một lần. Hậu quả cuối của thất bại theo policy phiên, hiện chưa được quyết định.

1. Đọc status, business code và thông điệp. Theo source hiện tại, auth helper và nhánh profile không tồn tại đều trả cùng HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`; không có signal trong response để phân biệt hai nguyên nhân.
2. Nếu chưa có server-side discriminator và policy được duyệt chưa cho refresh mọi #04/401, không gọi R-X01, không xóa/đổi token và không kết luận phiên hết hạn. Hiện trạng thái xác thực/profile không xác định an toàn và giữ nhánh chờ quyết định.
3. Chỉ khi contract phân loại hoặc policy cho phép refresh mọi #04/401, dùng token trong bộ quản lý phiên gửi R-X01 đúng một lần. Nguồn hiện kiểm tra refresh token/tài khoản ACTIVE, xoay dòng cũ, lưu hash mới và commit cùng giao dịch.
4. Nếu refresh được chấp nhận theo policy, thay cặp token trong bộ quản lý phiên rồi thử #04 đúng một lần. Không chạy song song hoặc lặp vô hạn.
5. Nếu refresh lỗi/401 hoặc #04 retry vẫn 401, chỉ dọn phiên/quay về SH-02 theo policy đã duyệt; hành vi đó hiện chưa được quyết định.
6. R-X01 có bằng chứng source nhưng chưa có ID API trong catalog; không coi nhánh là contract hoàn chỉnh.

**Kết quả / ngoại lệ:** Chưa có kết quả refresh tự động được xác nhận: #04/401 hiện không phân biệt auth không hợp lệ với profile thiếu. Chỉ refresh khi có căn cứ phân loại hoặc policy được duyệt cho phép áp dụng cho mọi 401.

### SH02-EV-12 — Xử lý #04 trả 403 / 500

- **Kích hoạt / loại:** API #04 trả 403/500 hoặc lỗi mạng / API response, Network error.
- **Điều kiện tiên quyết:** SH02-EV-10 đã gọi API #04 với bearer token của luồng STUDENT.
- **Đầu vào:** HTTP status, envelope/trace ID nếu có, hoặc lỗi transport.
- **API / đầu ra:** Không refresh với 403; dừng quyền/vai trò. Với 500/mạng hiện lỗi tải hồ sơ; retry #04 chỉ khi session policy được duyệt. Không gửi lại #03.

1. Với 403, không refresh; hiển thị trạng thái vai trò/quyền an toàn và dừng điều hướng. Nếu token lẽ ra thuộc vai trò học viên, chuyển sai khác khởi tạo vai trò cho máy chủ/Sản phẩm.
2. Với 500/mạng, hiển thị lỗi tải hồ sơ an toàn; không gửi lại #03. Chỉ cho thử lại #04 nếu session policy được duyệt.
3. Nếu response có traceId, giữ/hiển thị khi phù hợp; không ghi mật khẩu/token vào chẩn đoán.

**Kết quả / ngoại lệ:** 403 dừng quyền/vai trò và không refresh; 500/mạng hiển thị lỗi hồ sơ an toàn, không retry nếu chưa có policy. Không gửi lại #03.

### SH02-EV-13 — Chuyển tới đăng ký

- **Kích hoạt / loại:** Người dùng chọn SH02-EL-08 / Click, Keyboard.
- **Điều kiện tiên quyết:** Link SH-03 đang hiển thị và router Study tương lai đăng ký `/register`.
- **Đầu vào:** Không có dữ liệu form được gửi; đích route `/register` theo HTML/inventory.
- **API / đầu ra:** Không gọi API. Điều hướng tới SH-03; #01 đăng ký thuộc màn hình đó. Route runtime hiện chưa có.

1. Khi link được kích hoạt bằng pointer hoặc bàn phím, router tương lai nhận đích `/register` từ HTML/inventory.
2. Điều hướng tới SH-03; không chuyển email/mật khẩu hoặc token trong URL/state. SH-02 không gọi #01; đăng ký thuộc SH-03.
3. Nếu router/route SH-03 chưa được nối, không khẳng định điều hướng runtime thành công; hiện source app chưa có router Study Web.

**Kết quả / ngoại lệ:** Điều hướng dự kiến tới SH-03 `/register` mà không gọi #01 hoặc mang theo credential. Router Study Web chưa có nên route chưa được xác minh.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
