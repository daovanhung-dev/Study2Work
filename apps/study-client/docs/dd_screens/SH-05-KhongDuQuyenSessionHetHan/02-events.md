# SH-05 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `SH-05-EV-001` | `SH05-EV-01` / `SH05-EV-01` — Nhận kết quả request được bảo vệ và dựng state | See source event detail below |
| `SH-05-EV-002` | `SH05-EV-02` / `SH05-EV-02` — Chọn state preview 401/403 (prototype only) | See source event detail below |
| `SH-05-EV-003` | `SH05-EV-03` / `SH05-EV-03` — Thử refresh một lần cho 401 (auth manager) | See source event detail below |
| `SH-05-EV-004` | `SH05-EV-04` / `SH05-EV-04` — Click “Đăng nhập lại” | See source event detail below |
| `SH-05-EV-005` | `SH05-EV-05` / `SH05-EV-05` — Quay lại route an toàn sau 403 | See source event detail below |
| `SH-05-EV-006` | `SH05-EV-06` / `SH05-EV-06` — Sao chép Trace ID | See source event detail below |
| `SH-05-EV-007` | `SH05-EV-07` / `SH05-EV-07` — Click refresh trong preview prototype | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 6. Đặc tả sự kiện

Mỗi event mô tả target behavior tách khỏi prototype. Các bước không có bằng chứng triển khai được ghi là yêu cầu đề xuất hoặc blocker, không coi là runtime.

### `SH05-EV-01` — Nhận kết quả request được bảo vệ và dựng state

- **Kích hoạt / loại:** Response từ auth guard/API hoặc route loader; `Load/Response`.
- **Đầu vào:** HTTP status (integer); `businessCode` và `message` an toàn từ envelope; `traceId` từ body/header; route hiện tại và return route nếu auth manager cung cấp. Không nhận role/reason tùy ý từ query string.
- **Điều kiện:** Request được bảo vệ đã kết thúc; response được chuẩn hóa; không phải response giả từ preview selector.
- **Xử lý tuần tự:** (1) Kiểm tra status và parse JSON có kiểm soát; (2) cho phép render field contract, bỏ body không hợp lệ; (3) lấy trace ID response; nếu hai nguồn trace khác nhau, giữ discrepancy thay vì tự chọn; (4) 401 chuyển cho auth manager kiểm tra refresh eligibility theo inventory, nhưng không kết luận nguyên nhân vì API #04 cũng dùng cùng 401 khi profile không tồn tại; (5) 403 đưa thẳng vào `FORBIDDEN`, không gọi refresh; (6) 5xx/network/timeout chuyển service error chung; (7) cập nhật badge, heading, message, response card và action đồng bộ với state.
- **API:** Có thể là API #04 khi nó là request gây lỗi; không gọi API mới chỉ để dựng trang.
- **Thành công / đầu ra:** `UNAUTHORIZED`, `FORBIDDEN` hoặc service error riêng; chỉ render thông điệp an toàn và trace ID thật.
- **Ngoại lệ:** 401/403 code/body mâu thuẫn, lỗi JSON, thiếu status hoặc thiếu trace ID; không tự suy role hay chuyển 5xx thành 403. Missing trace ID không chặn view nhưng tắt copy action.

### `SH05-EV-02` — Chọn state preview 401/403 (prototype only)

- **Kích hoạt / loại:** Click #2 hoặc #3; `Click`.
- **Đầu vào:** `mode` literal `403` hoặc `401` do button prototype đặt.
- **Điều kiện:** Chỉ chạy trong `code.html`; controls không được đưa vào Study Web production.
- **Xử lý:** Reset `refreshAttempts`, cập nhật tab selected, heading/description/reason/recovery text, trace/status/envelope mock, action visibility và refresh alert theo mode. Không validate server response, không gọi #04 hoặc R-X01, không ghi session/cache.
- **Kết quả / ngoại lệ:** Preview state đổi tức thì. Prototype data không được reuse như fixture contract nếu không sửa cho khớp backend source.

### `SH05-EV-03` — Thử refresh một lần cho 401 (auth manager)

- **Kích hoạt / loại:** Auth manager nhận 401 từ request được bảo vệ; `Response/Async request` (không phụ thuộc click riêng của SH-05 trong target runtime).
- **Đầu vào:** Refresh token opaque từ session manager; access token/session metadata; request gốc + method/body; refresh-attempt marker/coordinator. Token không được đọc từ URL hoặc DOM.
- **Điều kiện:** Có refresh token; chưa có attempt cho flow; policy token persistence đã duyệt. R-X01 chỉ được gọi một lần cho flow; nếu token thiếu, không gọi API và chuyển login flow.
- **Xử lý:** (1) `list_screen.md` §1.2 yêu cầu một single-flight coordinator cho request đồng thời; request đang chờ dùng kết quả của refresh đang chạy thay vì xoay cùng refresh token song song; client source hiện không có để xác minh cách thực hiện; (2) với một flow 401, gửi tối đa một POST R-X01 với body `{refresh_token}`; (3) parse status/envelope/trace ID; (4) success: thay cặp token trong session manager theo persistence policy đã duyệt; (5) chỉ retry request gốc tối đa một lần, và chỉ khi request an toàn để replay; #04 là read-only, không replay mutation nếu chưa có contract về side effect/idempotency; (6) nếu retry #04 vẫn 401, dừng flow nhưng không gọi đó là hết phiên vì nguyên nhân có thể là profile không tồn tại; (7) 403 từ refresh ánh xạ tài khoản không `ACTIVE` theo source, không lặp refresh; (8) 5xx/network/timeout không xác nhận token chắc chắn invalid; hành động tiếp theo và cách xử lý rotation outcome mơ hồ cần policy được duyệt.
- **Kết quả / ngoại lệ:** Success thay token pair và có thể retry request an toàn theo policy. 401 từ R-X01 nghĩa token refresh không hợp lệ/hết hạn/đã dùng; 403 từ R-X01 nghĩa tài khoản không `ACTIVE`; 422/500/mạng không ánh xạ nhầm thành 403. Dọn phiên và hiển thị gì sau outcome ambiguous còn blocker.
- **API:** R-X01 mục 5.2; không áp dụng khi response ban đầu là 403.

### `SH05-EV-04` — Click “Đăng nhập lại”

- **Kích hoạt / loại:** Click login link trong #7; `Click/Navigation`.
- **Đầu vào:** Route `/login` đề xuất cho SH-02 và `returnTo` tương đối nội bộ nếu có.
- **Điều kiện:** Recovery policy đã quyết định cần login; login route phải được router xác nhận. Không áp dụng tự động chỉ vì API #04 trả 401 nếu chưa xử lý discrepancy profile-missing.
- **Xử lý:** (1) Loại bỏ absolute/external URL, protocol-relative URL, token và PII; (2) chỉ giữ return route trong allowlist; (3) điều hướng tới `/login`; (4) SH-02 tiếp tục theo flow đăng nhập riêng. Nếu `returnTo` không hợp lệ, không đính kèm.
- **Kết quả / ngoại lệ:** SH-02 hiển thị. Route sau login cần được kiểm tra quyền lại; không tin cậy route đích chỉ vì nó từng xuất hiện trong URL. Không xóa session trên mọi network/5xx error nếu chưa xác định token invalid.

### `SH05-EV-05` — Quay lại route an toàn sau 403

- **Kích hoạt / loại:** Click primary safe-back action trong #7; `Click/Navigation`.
- **Đầu vào:** Previous route từ router history hoặc navigation context; route allowlist; state `FORBIDDEN`.
- **Điều kiện:** Chỉ dùng relative same-origin route đã được router cho phép; không có redirect tới route cần cùng quyền vừa bị từ chối.
- **Xử lý:** Validate đích trước khi điều hướng; bỏ query chứa credential/PII; nếu history không có route hợp lệ thì cần fallback public route được Product xác nhận. Inventory liệt kê SH-01 `/` và SH-02, nhưng chưa chọn fallback cho direct-entry 403.
- **Kết quả / ngoại lệ:** Điều hướng tới safe route nội bộ hoặc giữ SH-05 nếu không có đích an toàn. Không gán role hoặc chuyển sang Mentor/Admin.

### `SH05-EV-06` — Sao chép Trace ID

- **Kích hoạt / loại:** Click #8 hoặc #10; `Click`.
- **Đầu vào:** Trace ID response thật từ #9, chuỗi opaque. Hai button hiện cùng gọi một hàm và cùng dữ liệu.
- **Điều kiện:** Trace ID tồn tại và Clipboard API khả dụng; mục tiêu production nên chỉ giữ một control sau UX review. #10 phải đạt hit target tối thiểu 44×44px.
- **Xử lý:** (1) Không copy mock value; (2) gọi Clipboard API với trace ID đã render; (3) success: live announcement “Đã sao chép Trace ID”; (4) rejection/permission denied: báo lỗi và cho phép chọn/copy thủ công nếu UX duyệt; (5) không đưa trace ID vào URL/log.
- **Kết quả / ngoại lệ:** Feedback accessible, không thay đổi auth state. Không có trace ID thì control disabled/hidden. Prototype hiện `.then()` nhưng không xử lý rejection.

### `SH05-EV-07` — Click refresh trong preview prototype

- **Kích hoạt / loại:** Click nút “Thử làm mới phiên” trong mode 401; `Click/Timer`.
- **Đầu vào:** Biến cục bộ `refreshAttempts`; không có token hoặc HTTP request.
- **Điều kiện:** Chỉ `code.html`; preview đang mode 401.
- **Xử lý:** Lần đầu tăng counter, disable nút, đổi label/icon; sau 1.2 giây bật lại và hiển thị text mô phỏng refresh token hết hạn. Click thêm hiển thị giới hạn attempt. Không gọi R-X01, không thay session/token, không validate response.
- **Kết quả / ngoại lệ:** Chỉ cập nhật DOM preview. Không dùng kết quả này như evidence `RUNTIME VERIFIED` hoặc làm tiêu chí xác nhận server behavior.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
