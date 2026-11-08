# SH-04 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `SH-04-TC-001` | Planning ref / not run | `AC-01` | See source acceptance section | P1 |

## 2. Test planning references

### SH-04-TC-001 — Acceptance planning reference (AC-01)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [SH-04](../../screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/SH-04.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-01`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/SH-04.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 11. Ma trận kiểm tra cho lần triển khai giao diện

Các mục sau là tiêu chí tương lai. Trong phiên soạn DD này chỉ đọc mã kiểm thử API #02; không chạy kiểm thử dự án.

| Nhóm | Trường hợp cần kiểm tra | Bằng chứng hiện có |
|---|---|---|
| Tích hợp API | Phần thân yêu cầu có `user_id` và `email`; không kèm Bearer; hiển thị HTTP 202 là “đã được bộ thử nghiệm tiếp nhận”. | Có đường dẫn API và mã kiểm thử cho API #02; chưa có mã giao diện, chưa chạy kiểm thử. |
| Ánh xạ bàn giao | `data.id` → `user_id`, `data.email` → `email`; không gọi khi thiếu dữ liệu. | Mã nguồn/mã kiểm thử API #01 xác nhận `id`, `email`; chưa có cơ chế giữa hai màn hình. |
| Chuẩn hóa/lỗi dữ liệu | Địa chỉ thư điện tử lỗi hoặc phần thân yêu cầu thiếu/sai kiểu trả 422; không hiện nội dung `accepted`. | Có bộ kiểm tra dữ liệu và mã kiểm thử API #02; chưa chạy kiểm thử. |
| Lỗi bộ gửi thư | Lỗi bộ gửi thư ánh xạ 500 `DESIGN_INTERNAL_ERROR`; không lộ ngoại lệ. | Có lớp điều phối và mã kiểm thử API #02; chưa chạy kiểm thử. |
| Giao thư/xác minh | Không nói đã gửi, không tạo OTP/liên kết và không hiện “đã xác minh”. | Mã nguồn bộ gửi thư không gửi thư/tạo token; chưa có điểm cuối xác nhận trong danh mục API. |
| Giả lập trong HTML | Các nút tự đổi JSON cục bộ; mẫu cURL thiếu `user_id` và sai đường dẫn. | Đã đọc HTML tĩnh; không thực thi JavaScript. |
| Điều hướng | Nút quay lại mở SH-02; truy cập trực tiếp khi thiếu dữ liệu không tự gửi yêu cầu. | Danh mục màn hình chỉ định SH-02; chưa có bộ định tuyến để kiểm tra. |
| Gửi lặp/mạng | Không tự gửi lặp khi chờ lâu hoặc không nhận phản hồi; kết quả chưa rõ. | Chưa có mã giao diện hoặc chính sách chống yêu cầu trùng. |
| Provider status/reason chưa biết | Không ánh xạ status ngoài accepted; không hiển thị reason chưa được duyệt. | Contract status là string, reason tùy chọn; API DD Q-02-05 còn mở. |
| Account/login gate | Không kết luận trạng thái đăng nhập sau SH-04 từ phản hồi API #02. | API #03 yêu cầu ACTIVE; API #01 bỏ qua status; DDL default ACTIVE chỉ là artifact, chưa có live-schema/verification-to-status evidence. |
| Tiếp cận/thích ứng | Bàn phím, tiêu điểm, thông báo trạng thái, chiều rộng 320px, phóng to, giảm chuyển động. | Chưa được kiểm tra trên mã giao diện vì môi trường chạy vắng mặt. |

### Trích từ DD nguồn: 14. Tiêu chí nghiệm thu tài liệu SH-04

- DD, kế hoạch, worklog và nhãn số chú thích do phiên này tạo được viết bằng tiếng Việt; tên API, trường JSON, giá trị/mã phản hồi và đường dẫn giữ nguyên để có thể đối chiếu.
- Có đủ 12 số trên ảnh; từng số ánh xạ một-một tới `SH04-EL-01..12` ở §4 và JSON marker; chín event `SH04-EV-01..09` có trigger/type, precondition, input, processing, output và kết quả/ngoại lệ riêng.
- Crosswalk A–F có đủ sáu mục; tổng quan có điều kiện trước/sau; ma trận trạng thái, route SH-03/SH-02 và blocker không mâu thuẫn.
- Ảnh `screen.png` và HTML `code.html` giữ nguyên hash nguồn; ảnh chú thích giữ đúng tỷ lệ 2×.
- DD nêu đúng API #02: yêu cầu `user_id`/`email`, HTTP 202 `DESIGN_OPERATION_ACCEPTED`, mặc định `status="accepted"`, `reason` tùy chọn, không gửi thật; lỗi bộ gửi thư trả 500 `DESIGN_INTERNAL_ERROR`; dữ liệu lỗi trả 422; discrepancy int64 được đánh dấu.
- Các dữ liệu/mã 200/503, thông tin hàng đợi, OTP/liên kết và lệnh cURL sai trong HTML được đánh dấu là mô phỏng hoặc sai khác, không dùng như hợp đồng.
- Mọi đường dẫn tương đối trong DD mở được trong cây tài liệu hiện tại; bảng tổng ghi riêng DD, implementation và runtime status.
- Chỉ kiểm tra tĩnh; không tuyên bố giao diện chạy, API được gọi từ trình duyệt, thư điện tử được gửi, địa chỉ thư điện tử được xác minh hoặc môi trường đã triển khai.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. Điều kiện chặn và tiêu chí hoàn tất

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

### Trích từ DD nguồn: 7. Trạng thái nguồn sau rà soát

- `screen.png`: 1600×1280; hash được ghi tại §2. `screen_annotated.png`: 3200×2560; 12 marker hiện hữu quan sát rõ, không che nội dung chính. Giữ ảnh chú thích và mở rộng JSON bằng `screen_id`, `element_id`, coordinate basis/origin/unit.
- `code.html`: các nút mock chỉ thay DOM/JSON cục bộ; không có request API. Nút cURL dựng endpoint/body không đúng API #02.
- API #02 route/view/validator/provider/test source hiện diện. Route công khai trả 202 khi provider trả; validator yêu cầu raw JSON integer cho `user_id`, chuẩn hóa email; không có DB, ownership lookup, queue, retry worker hoặc verify endpoint. Provider mặc định trả `accepted` mà không gửi email/tạo token.
- API #02 contract và OPEN_QUESTIONS còn Draft; trigger/owner, 202 semantics, provider/token lifecycle, user-email binding, public abuse control, status/reason enum, email normalization và int64 range chưa khóa.

### Trích từ DD nguồn: 8. Kế hoạch tái rà soát ngày 2026-11-07

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

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
