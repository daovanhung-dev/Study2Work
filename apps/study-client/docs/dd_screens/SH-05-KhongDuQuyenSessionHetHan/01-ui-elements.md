# SH-05 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [SH-05_markers.json](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `SH-05-EL-001` | `SH05-EL-01` | Handoff metadata bar |
| #2 | `SH-05-EL-002` | `SH05-EL-02` | Select HTTP 403 preview state |
| #3 | `SH-05-EL-003` | `SH05-EL-03` | Select HTTP 401 preview state |
| #4 | `SH-05-EL-004` | `SH05-EL-04` | HTTP state summary |
| #5 | `SH-05-EL-005` | `SH05-EL-05` | API #04 role boundary notice |
| #6 | `SH-05-EL-006` | `SH05-EL-06` | Routing diagnostics grid |
| #7 | `SH-05-EL-007` | `SH05-EL-07` | State-dependent recovery action area |
| #8 | `SH-05-EL-008` | `SH05-EL-08` | Copy support code button |
| #9 | `SH-05-EL-009` | `SH05-EL-09` | HTTP response and trace card |
| #10 | `SH-05-EL-010` | `SH05-EL-10` | Copy Trace ID icon button |
| #11 | `SH-05-EL-011` | `SH05-EL-11` | Engineering handoff policy card |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 3. Ảnh và bản đồ marker

- [Ảnh nguồn không chú thích](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/screen.png) giữ nguyên trạng thái 403, kích thước 1600×1280.
- [Ảnh chú thích](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/screen_annotated.png) có 11 marker. Marker #2/#3 là preview controls của prototype; controls 401 chỉ được hiển thị theo state trong HTML, không được đánh dấu như thể đang nhìn thấy trong ảnh 403.
- [Bản đồ marker JSON](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05_markers.json) dùng gốc tọa độ góc trái trên, đơn vị pixel ảnh nguồn. Thứ tự #1–#11 là thứ tự định danh duy nhất.
- [HTML prototype](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/code.html) là nguồn bố cục/mô phỏng, không phải triển khai frontend.

### Trích từ DD nguồn: 4. Đặc tả element

Các kích thước/vị trí dưới đây mô tả vùng trong ảnh nguồn; điều chỉnh responsive theo [Study Web design guide](../../../../../.agents/web-study/design.md). Mọi nội dung `mock` phải được thay bằng state/error context đã chuẩn hóa khi triển khai.

| # / Element ID | Tên, loại, vị trí | Thuộc tính, dữ liệu và validation | Hiển thị / trạng thái | Sự kiện |
|---|---|---|---|---|
| **#1 `SH05-EL-01`** | Thanh metadata hand-off, `aside`; dải trên cùng của prototype. | `Screen ID=SH-05`, route hiển thị `/forbidden`, dòng mô tả API #04. Nội dung tĩnh; không có input. Route là proposal, không phải runtime value. | Prototype: luôn visible. Production user-facing: bỏ metadata kỹ thuật hoặc chuyển sang shell/heading được duyệt. | Không có handler trong HTML. Không thêm hành vi click. |
| **#2 `SH05-EL-02`** | Nút preview `HTTP 403`, `button`; bên trái state selector. | Giá trị nội bộ của prototype `mode=403`; không gửi lên API và không phải lựa chọn người dùng ở runtime. | Prototype: selected mặc định; focus/hover theo CSS. Production: hidden/removed. | `SH05-EV-02` chỉ đổi preview state. |
| **#3 `SH05-EL-03`** | Nút preview `HTTP 401`, `button`; bên phải #2. | Giá trị nội bộ `mode=401`; không gửi request. | Prototype: unselected mặc định; production hidden/removed. | `SH05-EV-02` chỉ đổi preview state. |
| **#4 `SH05-EL-04`** | Tóm tắt lỗi, `section` gồm icon trang trí, status badge, endpoint label, heading và description; đầu thẻ chính. | Nguồn: HTTP status/business code đã chuẩn hóa. 401 dùng ngôn ngữ không thể xác thực; chỉ gọi là “hết phiên” nếu response/policy sau recovery xác nhận. 403 dùng thông báo không đủ quyền. Không dùng role/reason chi tiết từ client. Endpoint hiển thị chỉ là nhãn tĩnh trong prototype; API path đầy đủ là `/api/v1/users/me`. | `UNAUTHORIZED` hoặc `FORBIDDEN`; 5xx/mạng chuyển sang service-error component, không giữ badge 403. Icon không truyền nghĩa duy nhất; text phải nêu state. | `SH05-EV-01`; link/action ở #7. |
| **#5 `SH05-EL-05`** | Banner thông tin quyền, `notice`; dưới mô tả lỗi. | Prototype ghi API #04 chỉ dành cho `STUDENT`, kèm nhận định Mentor/Admin chưa có profile. Backend source xác nhận role guard Student; phần thông tin Mentor/Admin không phải response field/contract. Production chỉ dùng thông điệp đã duyệt, không tiết lộ cấu hình role nội bộ. | Hiện với state 403 nếu nội dung chung được duyệt; ẩn nếu không có explanatory copy cần thiết. Có thể chuyển thành `role="status"` khi cập nhật. | Nhận state từ `SH05-EV-01`; không có action. |
| **#6 `SH05-EL-06`** | Lưới chẩn đoán, `group/card`; bốn ô reason, recovery strategy, refresh constraint, policy. | Các reason strings trong HTML là mock và không có trong backend envelope. Không dùng `meta` như field tùy ý; chỉ đọc field có contract. Không hiển thị stack, permission matrix, claim hoặc session token. | Prototype: visible cả hai preview modes, giá trị thay đổi theo mode. Production chỉ giữ nội dung user-facing đã duyệt; có thể bỏ toàn bộ khối kỹ thuật. | Nội dung state cập nhật sau `SH05-EV-01` / `SH05-EV-03`; không có click event. |
| **#7 `SH05-EL-07`** | Vùng action phục hồi, `group`; gồm link quay lại ở 403, link login và nút preview refresh ở 401. | 403: destination chỉ là relative route allowlisted. 401: `/login` đề xuất; safe `returnTo` không chứa token/PII. Prototype href hiện sai (`/sh-01-dashboard`, `/sh-02-login`). Nút refresh không được gọi lần thứ hai sau khi auth manager đã attempt. | 403: primary safe-back visible. 401: login visible; refresh control chỉ có thể hiện nếu policy cho phép user-triggered attempt và attempt count=0. Disabled trong lúc refreshing; sau attempt không thể kích hoạt lại. | `SH05-EV-03`, `SH05-EV-04`, `SH05-EV-05`; prototype click được ghi trong `SH05-EV-07`. |
| **#8 `SH05-EL-08`** | Nút phụ “Sao chép mã phiên hỗ trợ”, `button`; cạnh action chính. | Hiện gọi cùng `copyTraceId()` như #10; giá trị thực đang copy là mock Trace ID, không có support-session code contract. Không có field hỗ trợ nào để validate. | Prototype: visible. Production: bỏ hoặc đổi nhãn thành “Sao chép Trace ID” sau khi UX duyệt; không giữ hai nút trùng chức năng nếu không có lý do rõ. | `SH05-EV-06`. |
| **#9 `SH05-EL-09`** | Thẻ response/trace, `card`; cột phải phía trên, gồm heading, nhãn sanitized, trace ID, status, JSON sample và explanatory note. | Chỉ render allowlist: status, businessCode, message an toàn, traceId. Backend envelope hiện có `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; response có header `X-Trace-Id`. Không hiển thị `data` profile, stack, SQL hoặc mock `timestamp`. JSON phải wrap/scroll có kiểm soát; không cắt message trọng yếu. | Visible khi error context có ít nhất status/code; không có trace ID thì bỏ giá trị/copy control hoặc thông báo unavailable. Loading không cần spinner riêng cho page; refresh có status tại #7. | `SH05-EV-01`; dữ liệu cấp cho `SH05-EV-06`. |
| **#10 `SH05-EL-10`** | Nút icon copy Trace ID, `button`; cuối hàng trace. | `aria-label` hiện “Sao chép Trace ID”; source 40×40px, nhỏ hơn target tối thiểu 44×44px trong guide. Input là trace ID thật, chuỗi opaque; không tự tạo ID. | Enabled khi có trace ID và clipboard API sẵn dùng; nếu không có ID thì disabled/hidden. Focus visible; target tối thiểu 44×44px; có feedback thành công/lỗi qua live region. | `SH05-EV-06`. |
| **#11 `SH05-EL-11`** | Thẻ policy hand-off, `card/list`; cột phải phía dưới gồm ba mục refresh, role segregation, accessibility. | Nội dung hiện là ghi chú kỹ thuật, không lấy từ API. Refresh limit là rule trong inventory; role/accessibility text cần chuyển thành requirement không lộ nội bộ. Production có thể bỏ thẻ hand-off. | Prototype: visible. Production: chỉ hiển thị phần user-facing được UX duyệt; không đưa cấu hình kỹ thuật/implementation detail vào trang lỗi. | Không có handler; nội dung phải tương thích state từ `SH05-EV-01`. |

## 4. Conditional UI & state variations
- States theo inventory: 401/403/token-refresh-failed
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
