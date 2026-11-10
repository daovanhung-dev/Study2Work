# Kế hoạch màn hình — SH-03 Đăng ký học viên

> **Trạng thái kế hoạch:** PLAN REVIEWED / RE-AUDIT COMPLETE · **Ngày rà soát:** 2026-11-07 · **Phạm vi phiên:** chỉ SH-03 · **Đợt:** W0 · **Ưu tiên:** P0.
> **Kết quả:** DD READY; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Việc gửi email thật, trạng thái kích hoạt tài khoản và Study Web runtime vẫn là phụ thuộc ngoài màn hình.

## 1. Mục tiêu và nguồn căn cứ

- **Mục tiêu:** cho Khách tạo tài khoản học viên bằng họ tên, email và mật khẩu, rồi chuyển sang SH-04 theo luồng F01.
- **Định tuyến trong danh mục:** `/register` là đường dẫn đề xuất, chưa được xác nhận là đường dẫn đang hoạt động.
- **Tiêu chí liên quan:** AC-01. Danh mục yêu cầu POST API #01; sau thành công, SH-04 mới gửi yêu cầu API #02. Email/OTP/CAPTCHA không được tự thêm vào biểu mẫu.
- **Mã nguồn API hiện tại:** `POST /api/v1/auth/register` được nối trong Study Server. API #01 kiểm tra dữ liệu, tìm email trùng, băm mật khẩu Argon2id, chèn tài khoản vai trò `STUDENT`, commit và trả hồ sơ công khai với HTTP 201. Đây là bằng chứng mã nguồn/mã kiểm thử cục bộ, không phải xác nhận triển khai hoặc lược đồ cơ sở dữ liệu đang chạy.
- **Phản hồi/điều hướng đích:** Hợp đồng API #01 và mã nguồn đều trả HTTP 201 với `data.id`/`data.email`; luồng F01 chuyển hai giá trị này sang SH-04, nơi API #02 mới được gọi. SH-03 không gọi #02.
- **Ranh giới hiện tại/đích:** Current #01 chỉ ghi `verification_dispatch_pending` sau commit, không gọi API #02. API #02 hiện trả 202 khi provider chấp nhận; provider mặc định là stub không gửi thư hoặc tạo token. AC-01 vẽ provider gửi và ghi log/retry, nên đây là `DISCREPANCY`, không phải behavior đang chạy.
- **Trạng thái tài khoản:** `INSERT_USER` không ghi cột `status`. Tệp DDL đã commit có default `ACTIVE`; API #03 yêu cầu `ACTIVE` khi đăng nhập. Live schema, migration state và yêu cầu chờ xác minh email chưa được xác nhận.
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
| 1 | SH03-EL-01 | Logo S2W và chữ Study2Work | Nhận diện tĩnh; không gắn route chưa được duyệt. |
| 2 | SH03-EL-02 | Tiêu đề và câu giới thiệu | Hướng dẫn mục tiêu trang; một tiêu đề H1 có ngữ nghĩa. |
| 3 | SH03-EL-03 | Họ và tên (`fullname`) | Input do người dùng nhập; ánh xạ sang `full_name`, trim/1–150 theo API. |
| 4 | SH03-EL-04 | Email (`email`) | Input do người dùng nhập; kiểm tra API email, trim và tối đa 255 sau chuẩn hóa. |
| 5 | SH03-EL-05 | Mật khẩu (`password`) | Input nhạy cảm; gửi nguyên văn, chỉ từ chối rỗng/toàn khoảng trắng theo API hiện tại. |
| 6 | SH03-EL-06 | Nút “Tạo tài khoản” | Submit form; khóa gửi lặp khi đang chờ, gọi API #01 một lần cho mỗi submit chủ ý. |
| 7 | SH03-EL-07 | Dải chân thẻ “Đã có tài khoản? Đăng nhập” | Điều hướng đề xuất tới SH-02 `/login`; không gửi form. |

Các tọa độ trong `SH-03_markers.json` tính theo pixel của ảnh gốc 1280×1056. Mỗi số đặt sát mé trái của vùng được đánh dấu để tránh che nhãn hoặc giá trị người dùng nhập.

## 4. Bản đồ trường và hợp đồng dữ liệu

| Trường trên giao diện | Tên trong HTML | Trường yêu cầu API #01 | Kiểu / giới hạn theo mã nguồn | Xử lý |
|---|---|---|---|---|
| Họ và tên | `fullname` | `full_name` | Chuỗi bắt buộc; sau khi cắt khoảng trắng hai đầu dài 1–150 ký tự. | Gửi `full_name`; không tự suy ra tên riêng/họ. |
| Địa chỉ email | `email` | `email` | Chuỗi email; sau chuẩn hóa tối đa 255 ký tự. | Gửi email sau khi cắt khoảng trắng/kiểm tra theo API; giữ bản hiển thị người dùng khi cần sửa. |
| Mật khẩu | `password` | `password` | Chuỗi bắt buộc, không chỉ gồm khoảng trắng; API không áp giới hạn tối thiểu 8 ký tự. | Gửi nguyên văn; không log, lưu ở URL hay thêm vào dữ liệu điều hướng. |

JSON yêu cầu chỉ có `{ "email": ..., "password": ..., "full_name": ... }`. Không thêm trường đồng ý điều khoản, `role`, token, mã OTP hay CAPTCHA vì chưa có hợp đồng cho các trường đó.

## 5. Chuỗi sự kiện dự kiến

1. `SH03-EV-01`: Khách mở `/register` đề xuất; public route và form idle là thiết kế, router/client hiện không có.
2. `SH03-EV-02`: Khách nhập họ tên/email/mật khẩu. Giữ state cục bộ; không lưu mật khẩu vào URL, log hoặc dữ liệu điều hướng.
3. `SH03-EV-03`: Submit #6; dựng `{email,password,full_name}`, map `fullname` → `full_name`, không gửi Bearer, gửi `POST /api/v1/auth/register` đúng một lần.
4. `SH03-EV-04`: HTTP 201 `DESIGN_RESOURCE_CREATED`; chuyển `data.id`/`data.email` tạm sang SH-04 theo F01. API #02 không được gọi trong SH-03.
5. `SH03-EV-05`: HTTP 409 `DESIGN_STATE_CONFLICT`; giữ form, gắn lỗi email, cho sửa hoặc chuyển SH-02.
6. `SH03-EV-06`: HTTP 422 `DESIGN_VALIDATION_ERROR`; map `meta.fieldErrors` vào đúng trường, giữ input an toàn, không áp mật khẩu tối thiểu 8 ký tự khi server chưa có rule.
7. `SH03-EV-07`: HTTP 500, timeout/lỗi mạng hoặc response thành công thiếu shape; thông báo an toàn, không retry POST mù vì server có thể đã commit account.
8. `SH03-EV-08`: Chọn link #7; điều hướng đề xuất tới SH-02 `/login`, không gửi API và không truyền form values.

**Phụ thuộc ngoài SH-03:** SH-04 sở hữu POST #02 với `{user_id: data.id, email: data.email}`. Current #02 trả HTTP 202 `DESIGN_OPERATION_ACCEPTED` khi provider nhận yêu cầu, nhưng default provider chỉ là stub. Không mô tả email đã gửi/xác minh.

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

- Có một DD tiếng Việt cho SH-03 và một kế hoạch tiếng Việt riêng được rà soát trước khi cập nhật artifact.
- Ảnh `screen.png` và HTML `code.html` không đổi; ảnh `screen_annotated.png` khớp 7 marker trong bảng §3 và tệp JSON. Marker JSON giữ mảng tương thích với renderer và ánh xạ từng số tới `SH03-EL-01..07`.
- DD thể hiện rõ ranh giới `fullname` → `full_name`, `data.id` → `user_id`, và API #02 chỉ thuộc bước SH-04.
- DD nêu riêng HTTP 201/409/422/500 của API #01 và trạng thái mã nguồn/giao diện đích; không tuyên bố email được gửi hoặc đã xác minh.
- Các liên kết tương đối mở đúng nguồn và không có phần tử giao diện được mô tả là tương tác nếu HTML không có bằng chứng.
- Bảy marker map tới bảy Element ID ổn định `SH03-EL-01..07`; tám Event ID `SH03-EV-01..08` đều có trigger/type, precondition, input, xử lý và output/API mapping.
- Giữ riêng `DD READY`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`; không chạy application tests trong phiên tài liệu.

## 9. Kết quả rà soát tĩnh

- Bảy marker có `screen_id`, `element_id`, tọa độ pixel theo gốc trái trên của `screen.png` 1280×1056; từng phần tử có Element ID ổn định trong DD.
- Tám sự kiện `SH03-EV-01..08` có element/loại, điều kiện tiên quyết, đầu vào, xử lý và đầu ra/API mapping trong DD.
- Crosswalk A–F được thêm; từng event có kết quả/ngoại lệ riêng và ghi rõ fallback hoặc policy còn mở.
- DD truy vết tới danh mục màn hình, AC-01, API catalog, route/module/query/provider/tests/open questions, DDL tham khảo và hướng dẫn Study Web.
- Static checks và hash ảnh/HTML được ghi ở worklog. Application tests và runtime không chạy; `RUNTIME NOT VERIFIED`.

## 10. Kế hoạch và kết quả re-audit ngày 2026-11-07

- **Phạm vi:** chỉ SH-03. Giữ nguyên `screen.png` và `code.html`; không sửa API, HTML mẫu, API #01/#02 contract hoặc màn hình SH-04.
- **Bằng chứng hiện tại đã đọc lại:** inventory SH-03, AC-01, API catalog #01/#02, API DD/open questions, route/module/provider/test source, DB artifact và Study Web design/context. `apps/study-client/src`/router/package manifest vắng mặt; `.agents/web-work/study/AGENTS.md`/`INDEX.md` hiện tồn tại và được manifest đăng ký — dòng DD ghi context `NOT_FOUND` là stale.
- **Ranh giới cần giữ:** #01 POST tạo user trả 201 theo source, insert không đặt `status`; #02 chỉ ở SH-04 theo F01 và default provider là stub. AC-01 đặt dispatch sau insert trong cùng diagram, còn F01 và source hiện tại không có #01→#02 call; giữ `DISCREPANCY`. Không áp ngưỡng mật khẩu 8 từ HTML vào API.
- **Kiểm tra artifact:** xác minh lại hai hash nguồn, kích thước PNG, marker JSON ↔ element row và tọa độ trong bounds, đọc trực quan ảnh chú thích, kiểm tra event coverage và local links.
- **Kết quả static audit trước DD edit:** `screen.png` 1280×1056 và `screen_annotated.png` 2560×2112; cả hai hash nguồn trong plan khớp hiện tại. Bảy marker JSON khớp thứ tự 7 element rows, tọa độ đều trong bounds; 8 event đều có trigger, precondition, input, processing, output và bước tuần tự; chưa có crosswalk A–F hay nhãn kết quả/ngoại lệ riêng từng event. Tất cả liên kết Markdown cục bộ resolve; cả hai ảnh đã được xem trực tiếp.
- **Kế hoạch DD (đã ghi trước khi sửa DD):** sửa nhận định context lỗi thời; thêm crosswalk A–F; thêm kết quả/ngoại lệ cho 8 event; nêu điều kiện trước/sau. Không biến cơ chế truyền `id/email`, activation status, email delivery hoặc password policy chưa duyệt thành hành vi xác nhận.
- **Kết quả DD:** nhận định context đã sửa; crosswalk A–F và 8 event kết quả/ngoại lệ đã thêm; event thành công hiện chỉ cam kết mapping `data.id`/`data.email` và route đích, còn transport tạm được giữ làm blocker cross-screen. DD vẫn `DD READY`; implementation còn bị chặn bởi route/source, handoff, email provider và account activation/schema.
- **Verification gate:** scoped `git diff --check` và authored-text whitespace/link/marker/event audit; không chạy application tests hoặc runtime. Global tracker/worklog cập nhật riêng ba trạng thái DD, implementation và runtime.
