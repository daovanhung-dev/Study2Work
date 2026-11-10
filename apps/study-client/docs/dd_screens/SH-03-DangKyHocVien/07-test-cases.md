# SH-03 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `SH-03-TC-001` | Planning ref / not run | `AC-01` | See source acceptance section | P0 |

## 2. Test planning references

### SH-03-TC-001 — Acceptance planning reference (AC-01)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [SH-03](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/SH-03.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-01`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/SH-03.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 9. Ma trận kiểm tra cần có khi triển khai giao diện

Các mục dưới đây là tiêu chí kiểm thử trong tương lai. Trong phiên soạn tài liệu này chỉ đọc mã kiểm thử, không chạy kiểm thử.

| Nhóm | Trường hợp cần kiểm tra | Bằng chứng hiện có |
|---|---|---|
| Thành công API | JSON hợp lệ, HTTP 201, dữ liệu chỉ có hồ sơ công khai, giao dịch được xác nhận một lần. | Có trong `test_register.py`; chưa chạy kiểm thử trong phiên này. |
| Chuẩn hóa/kiểm tra API | Cắt khoảng trắng email và `full_name`; email lỗi; họ tên rỗng/quá 150; mật khẩu rỗng/toàn khoảng trắng; HTTP 422. | Có trong `test_register.py`; chưa chạy kiểm thử trong phiên này. |
| Trùng email API | Email tồn tại trước khi chèn và tranh chấp ràng buộc duy nhất đều thành HTTP 409; có gọi `rollback`. | Có trong `test_register.py`; chưa chạy kiểm thử trong phiên này. |
| Lỗi API | Lỗi cơ sở dữ liệu/lỗi ngoài dự kiến trả 500 an toàn, không lộ chi tiết ngoại lệ. | Có trong `test_register.py`; chưa chạy kiểm thử trong phiên này. |
| Giao diện gửi | JSON chỉ có `email`, `password`, `full_name`; không có Bearer; khóa gửi lặp; ánh xạ `fullname` đúng. | Chưa có mã giao diện hoặc kiểm tra giao diện trong bản làm việc. |
| Giao diện lỗi | `meta.fieldErrors` nối đúng trường; 409 giữ biểu mẫu; 500/mạng không để lộ chi tiết và không tự gửi lại. | Chưa có mã giao diện hoặc kiểm tra giao diện trong bản làm việc. |
| Chuyển tiếp | HTTP 201 đưa `data.id`/`data.email` tới SH-04; API #02 không bị gọi từ SH-03. | Luồng hiện chỉ có trong danh mục; phía giao diện chưa có. |
| Trợ năng/thích ứng | Bàn phím, tiêu điểm, vùng thông báo, chiều rộng 320px, phóng to, giảm chuyển động. | Chưa được kiểm tra bằng mã giao diện. |

### Trích từ DD nguồn: 11. Tiêu chí nghiệm thu tài liệu SH-03

- [x] Kế hoạch, DD, nhãn marker và nội dung chú thích viết bằng tiếng Việt; tên API/trường/mã nguồn giữ nguyên chính tả để đối chiếu.
- [x] Có đủ 7 marker tuần tự trên ảnh; từng số ánh xạ một-một tới 7 hàng element ở §4.
- [x] Tài sản gốc giữ nguyên SHA-256; ảnh chú thích giữ đúng tỷ lệ 2×.
- [x] API #01/#02 được đối chiếu với source/catalog/AC; sai khác và blocker được ghi rõ; không mô tả API #02 là gửi email thật.
- [x] Có crosswalk A–F; đủ 8 event với trigger/type, điều kiện, input, xử lý, output và kết quả/ngoại lệ.
- [x] Local links mở được; tracker/worklog phân biệt DD READY, IMPLEMENTATION BLOCKED và RUNTIME NOT VERIFIED.
- [x] Không chạy kiểm thử dự án trong phiên này; test source được ghi nhận là đã đọc, chưa chạy.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. Trạng thái và tiêu chí xử lý

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

### Trích từ DD nguồn: 8. Tiêu chí hoàn tất tài liệu SH-03

- Có một DD tiếng Việt cho SH-03 và một kế hoạch tiếng Việt riêng được rà soát trước khi cập nhật artifact.
- Ảnh `screen.png` và HTML `code.html` không đổi; ảnh `screen_annotated.png` khớp 7 marker trong bảng §3 và tệp JSON. Marker JSON giữ mảng tương thích với renderer và ánh xạ từng số tới `SH03-EL-01..07`.
- DD thể hiện rõ ranh giới `fullname` → `full_name`, `data.id` → `user_id`, và API #02 chỉ thuộc bước SH-04.
- DD nêu riêng HTTP 201/409/422/500 của API #01 và trạng thái mã nguồn/giao diện đích; không tuyên bố email được gửi hoặc đã xác minh.
- Các liên kết tương đối mở đúng nguồn và không có phần tử giao diện được mô tả là tương tác nếu HTML không có bằng chứng.
- Bảy marker map tới bảy Element ID ổn định `SH03-EL-01..07`; tám Event ID `SH03-EV-01..08` đều có trigger/type, precondition, input, xử lý và output/API mapping.
- Giữ riêng `DD READY`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`; không chạy application tests trong phiên tài liệu.

### Trích từ DD nguồn: 9. Kết quả rà soát tĩnh

- Bảy marker có `screen_id`, `element_id`, tọa độ pixel theo gốc trái trên của `screen.png` 1280×1056; từng phần tử có Element ID ổn định trong DD.
- Tám sự kiện `SH03-EV-01..08` có element/loại, điều kiện tiên quyết, đầu vào, xử lý và đầu ra/API mapping trong DD.
- Crosswalk A–F được thêm; từng event có kết quả/ngoại lệ riêng và ghi rõ fallback hoặc policy còn mở.
- DD truy vết tới danh mục màn hình, AC-01, API catalog, route/module/query/provider/tests/open questions, DDL tham khảo và hướng dẫn Study Web.
- Static checks và hash ảnh/HTML được ghi ở worklog. Application tests và runtime không chạy; `RUNTIME NOT VERIFIED`.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
