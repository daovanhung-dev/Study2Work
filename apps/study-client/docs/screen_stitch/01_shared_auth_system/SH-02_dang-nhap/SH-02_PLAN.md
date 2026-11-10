# Kế hoạch màn hình — SH-02 Đăng nhập

> **Trạng thái kế hoạch:** PLAN REVIEWED / DD AND ARTIFACT AUDIT COMPLETE · **Ngày rà soát:** 2026-11-07 · **Phạm vi phiên:** chỉ SH-02 · **Đợt danh mục:** W0.
> **Trạng thái sau rà soát nguồn:** DD BLOCKED · IMPLEMENTATION BLOCKED · RUNTIME NOT VERIFIED. Chặn DD bởi sai khác hợp đồng thành công #03 và chính sách phiên/vai trò chưa được duyệt; không coi đây là chức năng đã chạy.

## 1. Hợp đồng và bằng chứng nguồn

- **Tác nhân / màn hình:** Khách mở trang đăng nhập công khai; Trang /login, AC-02, P0.
- **Luồng trong danh mục:** POST #03 → chính sách token phiên → GET #04 chỉ khi vai trò trả về là STUDENT; người hướng dẫn/quản trị viên không có endpoint khởi tạo hồ sơ tương thích. #04 hiện dùng 401 chung cho auth/claim không hợp lệ và không có profile; không thể tự xác định nguyên nhân để quyết định refresh. R-X01 chỉ được xem là nhánh khôi phục có điều kiện sau khi có policy/contract được duyệt. Liên kết đăng ký đi tới SH-03.
- **Trạng thái nguồn:** Mã route/view của #03 và #04 tồn tại (RUNTIME_SOURCE). R-X01 /auth/refresh có trong mã nguồn hiện tại nhưng chưa có ID API trong danh mục (SOURCE_BACKED_UNCATALOGUED). Route/client/lưu phiên Study Web ở trạng thái UNWIRED vì apps/study-client/src không tồn tại.
- **Ảnh nguồn hiện tại:** `screen.png` trong thư mục này, kích thước 1280×1024 và có vẻ trống. Giữ nguyên; SHA-256 hiện tại là 5c3cb8e59c1b645c4338ce527d5fd2c7a2288568fc04982481865d422ec4e323.
- **HTML nguồn:** code.html mô tả thẻ đăng nhập căn giữa gồm thương hiệu, tiêu đề, vùng cảnh báo, trường email/mật khẩu, nút hiện mật khẩu, nút chính và liên kết đăng ký. Tệp tải Tailwind/font/icon từ CDN bên ngoài. Các bộ xử lý nội tuyến gọi handleLoginSubmit() và togglePasswordVisibility() nhưng HTML không định nghĩa hai hàm này. Giữ nguyên HTML; SHA-256 hiện tại là 6e848c7bbab66b13f0486eb397b9da8a0e2059f3d9b169287b8359b8c1aad595.
- **Bản xem sạch phát sinh:** Dựng HTML thành screen_rendered.png bằng Chrome headless, cho phép tài nguyên Tailwind/font ngoài mà trang đang tham chiếu, khung nhìn 1280×1024, thời gian chụp 10 giây. Đây là bản xem từ nguồn thiết kế, không phải ảnh khi chạy. Chú thích lên bản dựng này thành screen_annotated.png; giữ screen.png trống làm bằng chứng nguồn.
- **Đích chuẩn:** `.agents/web-work/study/AGENTS.md` và `INDEX.md` hiện tồn tại, được khai báo trong context map và đăng ký trong manifest. Ngữ cảnh xác nhận Study Web vẫn UNWIRED vì thiếu editable source/package manifest; không coi trang context là bằng chứng runtime.
- **Sai khác hợp đồng API:** DD/danh mục API #03 quy định 201 DESIGN_RESOURCE_CREATED, UserProfile không có trường token và lỗi 422/500. Mã nguồn hiện tại và AC-02 ghi 200 DESIGN_RESOURCE_RETRIEVED, hồ sơ cùng trường token truy cập/làm mới và lỗi 401/403/500. Giữ cả hai vế ở trạng thái DISCREPANCY; không tự chọn một vế trong DD màn hình.
- **Điều kiện mở G-02:** #04 chỉ chấp nhận STUDENT; AC-02 còn đề cập permissions nhưng mô hình phản hồi hiện tại của #03/#04 không có trường này. Không suy diễn cách khởi tạo người hướng dẫn/quản trị viên.

## 2. Luồng đích và quyết định

1. Mở /login; chỉ chấp nhận returnTo tương đối cùng miền nếu router tương lai đưa qua danh sách cho phép. Từ chối đích ngoài miền, chuyển hướng mở, token hoặc dữ liệu riêng tư trong URL.
2. Nhập email/mật khẩu. required/type=email của HTML chỉ tiện kiểm tra; API #03 là nguồn quyết định. Chuẩn hóa email theo phía máy chủ hiện tại nhưng giữ nguyên mật khẩu (phía máy chủ chỉ kiểm tra đầu vào toàn khoảng trắng mà không viết lại giá trị gửi).
3. Gửi đúng một lần. Tạo JSON {email,password}. Khóa gửi lặp khi đang chờ; không tự gửi lại POST đăng nhập khi kết quả không rõ vì mã nguồn chưa có khóa chống lặp/hợp đồng và thao tác thành công tạo một dòng refresh-token.
4. Phân nhánh theo nguồn hiện tại: #03 trả 422 → lỗi trường; 401 → lỗi thông tin đăng nhập chung; 403 → tài khoản không khả dụng; 500/mạng → quyết định thử lại an toàn và trace ID. Không tiết lộ tài khoản tồn tại từ 401, không gọi refresh khi 401 do thông tin đăng nhập.
5. Khi nguồn hiện tại trả HTTP 200, phân tích envelope cùng trường token/hồ sơ thực tế và ghi nhận hợp đồng chuẩn khác biệt. Mã nguồn Study Web chưa quy định cách lưu/lifetime token; dừng ở điều kiện chờ duyệt chính sách phiên trước khi triển khai lưu trữ an toàn. Không tự chọn localStorage/cookie.
6. Nếu chính sách lưu phiên được duyệt và data.role == STUDENT, gọi #04 với Authorization: Bearer <access_token>. #04 kiểm tra JWT/vai trò trước khi truy vấn DB và trả trường hồ sơ an toàn hiện có. Không trả permissions hoặc bio.
7. Với #04 trả 401, mã nguồn không phân biệt credential/claim không hợp lệ với không tìm thấy profile. Không tự kết luận 401 là token hết hạn. Chỉ gọi R-X01 tối đa một lần nếu hợp đồng nguồn cung cấp căn cứ phân loại hoặc policy xác thực dùng chung được duyệt cho phép refresh mọi 401; nếu không, dừng tại nhánh chờ quyết định. Không refresh sau 403.
8. Nếu vai trò là MENTOR/ADMIN hoặc #04 từ chối vai trò, không gọi endpoint /users/me dành cho học viên và không chuyển tới /student. Chặn luồng cho tới khi đường dẫn/vỏ giao diện theo vai trò được duyệt.
9. Khi hồ sơ học viên được xác minh, chuyển tới returnTo an toàn đã cho phép; nếu không có thì /student chỉ là đích mặc định đề xuất, chờ router/sản phẩm duyệt. Liên kết đăng ký → SH-03.

## 3. Truy vết nguồn API hiện tại

### #03 POST /api/v1/auth/login

~~~text
v1.authenticate
  -> api_03_auth_login.view.login
  -> validate_login_request
  -> query_one(LOGIN_USER theo email)
  -> verify_password(hash đã lưu)
  -> yêu cầu users.status == ACTIVE
  -> auth_utils.issue_tokens
  -> INSERT_REFRESH_TOKEN (lưu HMAC hash của refresh token) + commit
  -> success_response(build_auth_payload(hồ sơ + token thô))
~~~

- Mô hình yêu cầu hiện có hai chuỗi: email và password.
- Bộ kiểm tra hiện chuẩn hóa email, kiểm tra định dạng và giới hạn 255 ký tự; từ chối mật khẩu rỗng sau .strip(), nhưng chuyển nguyên giá trị mật khẩu ban đầu sang bước xác minh.
- Thành công hiện tại: HTTP 200; businessCode=DESIGN_RESOURCE_RETRIEVED; data có các trường hồ sơ được cho phép cùng access_token, refresh_token, token_type="bearer", expires_in, refresh_expires_in.
- Refresh token thô được trả về client; chỉ HMAC hash được lưu trong refresh_tokens. Giao dịch đăng nhập chỉ commit sau khi cấp token và chèn hash refresh thành công.
- Email không tồn tại và sai mật khẩu cùng trả HTTP 401 DESIGN_AUTHENTICATION_REQUIRED với cùng thông báo chung. Người dùng không ACTIVE trả 403 DESIGN_ACCESS_DENIED. Lỗi kiểm tra đầu vào trả 422 DESIGN_VALIDATION_ERROR; lỗi DB/lưu token trả 500 DESIGN_INTERNAL_ERROR an toàn.

### #04 GET /api/v1/users/me

~~~text
v1.current_user
  -> api_04_users_me.view.get_current_user
  -> validate_current_user_request(Authorization, role="STUDENT")
  -> giải mã JWT, yêu cầu sub dạng số và roles có STUDENT
  -> truy vấn CURRENT_USER_PROFILE theo user_id
  -> mô hình UserProfile -> envelope thành công
~~~

- Yêu cầu có đúng một header Authorization: Bearer <jwt>; không có body/query/path.
- Mã nguồn kiểm tra vai trò trước khi đọc DB. JWT không phải học viên trả 403; token thiếu/sai/không hợp lệ và không có hồ sơ người dùng trả 401; lỗi SQL/ánh xạ trả 500 an toàn.
- data hiện trả id, full_name, email, role, avatar_url có thể null, phone có thể null, status, created_at, updated_at. Không có bio, permissions, token hay password hash.
- Claim hiện dùng sub + roles; sơ đồ AC-02 dùng user_id + vai trò. #04 lấy role/status từ DB nhưng không đối chiếu vai trò với claim JWT hay từ chối trạng thái tài khoản đã đổi. Ý nghĩa này còn mở.

### R-X01 POST /api/v1/auth/refresh

- Route hiện có xoay refresh token dạng opaque: chỉ tìm hash chưa thu hồi/chưa hết hạn và người dùng ACTIVE; thu hồi dòng cũ; chèn token mới đã băm trong cùng giao dịch; trả cặp access/refresh mới và hồ sơ.
- R-X01 có trong mã nguồn khi chạy nhưng không thuộc danh mục 103 API. Token sai/hết hạn/đã xoay trả 401. Không đưa token thô vào ví dụ DD, log hoặc query string.

## 4. Kế hoạch marker chú thích

Tọa độ tính bằng pixel CSS trên bản dựng sạch 1280×1024 từ code.html. SH-02_markers.json điều khiển bộ dựng. Không chú thích ảnh screen.png trống như thể giao diện có trong ảnh.

| # | Element ID | Phần tử đích | Vùng trên ảnh | Sự kiện / nguồn dữ liệu |
|---:|---|---|---|---|
| 1 | SH02-EL-01 | Dấu thương hiệu và nhận diện Study2Work | Đầu thẻ đăng nhập | HTML không quy định liên kết/trang chủ; giữ bất hoạt nếu chưa duyệt |
| 2 | SH02-EL-02 | Tiêu đề và phần giải thích | Khối tiêu đề thẻ | Nội dung tĩnh đã duyệt; không gọi API |
| 3 | SH02-EL-03 | Vùng cảnh báo/lỗi chung | Giữa phần giới thiệu và biểu mẫu; ban đầu ẩn | Nhận lỗi API/truyền tải đã ánh xạ an toàn, không chứa chi tiết phía máy chủ thô |
| 4 | SH02-EL-04 | Trường email | Ô nhập có nhãn đầu tiên | Đầu vào người dùng → #03 email; chuẩn hóa/kiểm tra theo nguồn hiện tại |
| 5 | SH02-EL-05 | Trường mật khẩu | Ô nhập có nhãn thứ hai | Đầu vào người dùng → #03 password; giữ nguyên chuỗi |
| 6 | SH02-EL-06 | Điều khiển hiện/ẩn mật khẩu | Nút mắt trong trường mật khẩu | Chỉ đổi kiểu hiển thị tại chỗ; togglePasswordVisibility() hiện chưa được định nghĩa |
| 7 | SH02-EL-07 | Nút gửi đăng nhập | Nút toàn chiều rộng | Gửi #03 một lần; bận/vô hiệu hóa trong lúc chờ |
| 8 | SH02-EL-08 | Liên kết đăng ký | Chân thẻ | Tới SH-03 /register; không gọi API tại đây |

## 5. Kế hoạch trạng thái/sự kiện và nghiệm thu

Các Event ID phải giữ ổn định trong DD và liên kết về Element ID ở bảng trên: SH02-EV-01 mở màn hình/kiểm tra returnTo; SH02-EV-02 nhập dữ liệu; SH02-EV-03 hiện/ẩn mật khẩu; SH02-EV-04 gửi #03; SH02-EV-05 ánh xạ 422; SH02-EV-06 ánh xạ 401; SH02-EV-07 ánh xạ 403; SH02-EV-08 ánh xạ 500/mạng/body sai; SH02-EV-09 xử lý đăng nhập thành công và vai trò; SH02-EV-10 tải hồ sơ #04; SH02-EV-11 đánh giá #04/401 và chỉ refresh R-X01 nếu policy/contract cho phép; SH02-EV-12 xử lý #04/403/500; SH02-EV-13 đi tới SH-03. Giữ đầy đủ điều kiện, input, thứ tự xử lý, API, output và ngoại lệ trong từng sự kiện DD.

- Giữ riêng giá trị email/mật khẩu sau 422/401; không đưa mật khẩu vào cảnh báo/log.
- Email có thể dùng kiểm tra gốc của trình duyệt. meta.fieldErrors phía máy chủ ánh xạ vào trợ giúp trường; envelope hiện đặt lỗi trường trong meta.fieldErrors, mỗi lỗi có thể gồm {field?,code,message}. Với 401, hiển thị một lỗi thông tin đăng nhập chung, không chỉ rõ trường sai.
- Hiển thị khác nhau cho 401 và 403. Thông báo tài khoản ở 403 vẫn phải khái quát; chưa truy vấn hồ sơ trước khi kiểm tra vai trò.
- Nút đăng nhập chuyển sang trạng thái chờ và chặn bấm lặp. Timeout mạng sau khi gửi tạo kết quả không rõ; không gửi lại mù cho tới khi có chính sách chống lặp/khôi phục được duyệt.
- Nút hiện mật khẩu chỉ đổi kiểu input; không đổi giá trị. Cần tên trợ năng/trạng thái nhấn và thao tác bằng bàn phím.
- Luồng học viên chỉ gọi #04 sau khi chính sách token phiên được duyệt. Luồng người hướng dẫn/quản trị viên dừng tại G-02; không lặp kiểm tra học viên.
- Không thêm quên mật khẩu, ghi nhớ đăng nhập, xác minh email, MFA hay đăng nhập mạng xã hội: các mục này không có trong hợp đồng thiết kế/API hiện tại.
- Không biến font/Tailwind từ xa của HTML mẫu thành phụ thuộc bắt buộc. Hướng dẫn Study quy định dùng Inter có sẵn tại chỗ, nếu không thì sans-serif hệ thống; không thêm thư viện/font từ xa.

## 6. Quyết định còn mở

1. Giải quyết sai khác HTTP/body/lỗi của API #03 giữa list_api.md, AC-02 và mã nguồn; chủ sở hữu BA/máy chủ.
2. Duyệt cách lưu token an toàn phía client, phối hợp refresh và chính sách đăng xuất/phiên; chủ sở hữu Security/máy chủ/Frontend.
3. Giải quyết G-02: khởi tạo hồ sơ/định tuyến người hướng dẫn/quản trị viên và nguồn permissions; chủ sở hữu Auth/Sản phẩm/máy chủ.
4. Xác nhận danh sách cho phép returnTo và đích mặc định học viên; chủ sở hữu Sản phẩm/Frontend.
5. Làm rõ vì sao luồng gọi #04 sau khi #03 đã trả hồ sơ và trường hồ sơ/quyền nào có thẩm quyền; chủ sở hữu BA/máy chủ.
6. Cung cấp ảnh SH-02 thật hoặc xác nhận PNG nguồn trống là không hợp lệ và bản dựng HTML là đầu vào hình ảnh được chấp nhận; chủ sở hữu tài sản screen-stitch.
7. Triển khai/duyệt handler hiện mật khẩu và gửi biểu mẫu; HTML hiện gọi nhưng không định nghĩa cả hai; chủ sở hữu Design/Frontend.
8. Quyết định câu chữ/ngôn ngữ lỗi; giữ riêng thông báo máy chủ và hợp đồng chuẩn cho tới khi được duyệt.
9. #04 trả cùng 401 cho token/claim không hợp lệ và profile không tồn tại; xác nhận mã lỗi/metadata phân biệt hoặc policy có chủ đích refresh mọi 401 trước khi SH-02 tự động gọi R-X01.

## 7. Danh sách kiểm tra tĩnh

- Hash screen.png và code.html do người dùng cung cấp không đổi.
- screen_rendered.png là bản dựng HTML sạch, không đánh số, 1280×1024; đã ghi nguồn gốc và tài nguyên ngoài được dùng.
- screen_annotated.png lấy bản dựng sạch ở tỉ lệ 2×, giữ nguyên tỉ lệ khung hình và có marker #1–#8.
- SH-02_markers.json và DD SH-02 có đúng tám dòng, ID SH02-EL-01..08 khớp một-một theo số marker; mọi sự kiện SH02-EV-01..13 ánh xạ tới nguồn/API hiện tại hoặc điều kiện chặn rõ ràng.
- Liên kết cục bộ mở được; tài sản gốc không đổi; không chạy kiểm thử dự án trừ khi có yêu cầu.

## 8. Re-audit ngày 2026-11-07

- Xác nhận `.agents/web-work/study/AGENTS.md` và `INDEX.md` có mặt, được khai báo trong `.agents/context-map.md` và đăng ký trong `.agents/context-manifest.json`; sửa nhận định NOT_FOUND cũ. Trạng thái ứng dụng vẫn UNWIRED do thiếu source/package manifest.
- Audit tĩnh xác nhận PNG gốc 1280×1024 và HTML gốc giữ nguyên hash đã ghi; bản dựng sạch 1280×1024; ảnh marker 2560×2048; JSON có 8 ID duy nhất khớp 8 hàng element; DD có đủ 13 Event ID; các liên kết Markdown cục bộ resolve.
- Ảnh chú thích được xem trực quan: marker #1–#8 nằm trên các vùng thiết kế tương ứng; #3 chỉ đánh dấu vùng cảnh báo đang ẩn mặc định.
- DD đã thêm crosswalk A–F, kết quả/ngoại lệ cho đủ 13 event, state `PROFILE_AUTH_FAILURE_UNCLASSIFIED`, blocker SH02-D09 và checklist nghiệm thu. Không tự động refresh #04/401 khi chưa có classifier hoặc policy cho phép.
- Kiểm tra tĩnh sau cập nhật: 8 marker ID khớp đúng thứ tự với 8 element row; 13 event đều có trigger, precondition, input, API/output, bước xử lý và kết quả/ngoại lệ; 6 dòng crosswalk A–F; toàn bộ local Markdown links resolve; hash PNG/HTML vẫn khớp.
- Ảnh chú thích đã xem trực quan. `git diff --check` theo phạm vi SH-02 đạt. Không chạy test ứng dụng, không xác minh runtime, DB hay deployment. Trạng thái cuối vẫn DD BLOCKED / IMPLEMENTATION BLOCKED / RUNTIME NOT VERIFIED.
