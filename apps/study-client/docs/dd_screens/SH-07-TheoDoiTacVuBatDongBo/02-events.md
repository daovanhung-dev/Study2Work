# SH-07 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `SH-07-EV-001` | `SH07-EV-01` / `SH07-EV-01` — Resolve route và nạp trạng thái gate | See source event detail below |
| `SH-07-EV-002` | `SH07-EV-02` / `SH07-EV-02` — Mở Contract Spec modal | See source event detail below |
| `SH-07-EV-003` | `SH07-EV-03` / `SH07-EV-03` — Đóng Contract Spec modal | See source event detail below |
| `SH-07-EV-004` | `SH07-EV-04` / `SH07-EV-04` — Sao chép Operation ID | See source event detail below |
| `SH-07-EV-005` | `SH07-EV-05` / `SH07-EV-05` — Đọc operation status lần đầu (chưa runnable) | See source event detail below |
| `SH-07-EV-006` | `SH07-EV-06` / `SH07-EV-06` — Làm mới trạng thái / polling (chưa được duyệt) | See source event detail below |
| `SH-07-EV-007` | `SH07-EV-07` / `SH07-EV-07` — Click CTA quay về khóa học | See source event detail below |
| `SH-07-EV-008` | `SH07-EV-08` / `SH07-EV-08` — Click CTA về trang chủ/logo | See source event detail below |
| `SH-07-EV-009` | `SH07-EV-09` / `SH07-EV-09` — Click header nav, login hoặc register | See source event detail below |
| `SH-07-EV-010` | `SH07-EV-10` / `SH07-EV-10` — Click footer nav | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 7. Đặc tả sự kiện

### `SH07-EV-01` — Resolve route và nạp trạng thái gate

- **Trigger/element:** browser navigation tới route đề xuất `/operations/:operationId`; không có marker riêng ngoài breadcrumb/ID element #8/#12.
- **Loại:** route load / page initialization.
- **Input:** pathname; operation ID từ caller/server nếu có; auth/session context của app. Không chấp nhận sample ID từ HTML.
- **Current processing:** inline script tìm `/operations/([^/?#]+)` rồi hiển thị capture; nếu thiếu match thì đặt UUID mẫu. Không xác thực ID, role hoặc owner; không có API call.
- **Target ordering:** (1) lấy path segment; (2) chưa canonicalize/regex validate cho tới khi chủ contract chốt UUID/int64; (3) xác nhận caller đã nhận đúng field từ producer, không map notification ID; (4) nếu endpoint chưa sẵn sàng, render `DESIGN_GATE`/unavailable state đã được product duyệt và không request/poll; (5) không đưa fake fallback vào UI; (6) nếu route param thiếu/hỏng, route fallback policy còn cần xác nhận.
- **Output:** gate view tĩnh trong prototype; không ghi state/cache hoặc tạo side effect.
- **Ngoại lệ:** không tự đổi malformed ID thành not-found; status code/route handling chưa chốt. ID chưa được cấp không được sao chép/hiển thị như thật.

### `SH07-EV-02` — Mở Contract Spec modal

- **Trigger/element:** click button #7.
- **Input:** không payload.
- **Processing:** current inline handler `classList.toggle('hidden')` trên `#tech-specs-modal`; không request/network/state API.
- **Output:** nội dung modal sample hiện ra. Modal mở theo default hidden.
- **Ngoại lệ/accessibility:** không có focus management, semantic dialog, Escape handling hoặc focus return trong source. Sample bên trong giữ nhãn design-only và không được xem là executable schema.

### `SH07-EV-03` — Đóng Contract Spec modal

- **Trigger/element:** close icon hoặc nút “Đóng cửa sổ” trong modal.
- **Input:** không payload.
- **Processing:** current handler `classList.add('hidden')`; không gọi API, không đổi operation state.
- **Output:** quay về trạng thái modal hidden.
- **Ngoại lệ/accessibility:** backdrop/Escape behavior không có trong HTML; chốt cùng modal implementation. Không đặt hành vi đóng dựa trên API.

### `SH07-EV-04` — Sao chép Operation ID

- **Trigger/element:** copy button #13.
- **Input:** text từ `#param-op-id`; current prototype có thể là ID route hoặc UUID fallback giả.
- **Target processing:** chỉ cho phép khi giá trị được producer phát hành và kiểu canonical đã được duyệt; đọc đúng giá trị đã validate; gọi Clipboard API; không gọi API #18. Không copy fallback/mock value.
- **Current result:** gọi `navigator.clipboard.writeText(...)`; không chờ/handle Promise và không feedback thành công/thất bại.
- **Open behavior:** product/FE cần quyết định disable/ẩn khi thiếu ID và accessible feedback cho clipboard failure; không tự tạo error code.

### `SH07-EV-05` — Đọc operation status lần đầu (chưa runnable)

- **Trigger/element:** route initialization sau khi API #18/ID/authorization/producer contract được duyệt. Event này là expected design, không phải current HTML behavior.
- **Input:** `operation_id` từ path; Bearer JWT từ auth layer. Không có query parameter/body.
- **API design:** `GET /api/v1/operations/{operation_id}`; API ID #18; auth Bearer JWT; actor/owner policy disputed; response 200 `DESIGN_OPERATION_RETRIEVED` + `ApiEnvelope<Operation>`; 401/403/404/500 với các mã nêu ở §5.
- **Processing:** (1) lấy path ID đã được upstream phát; (2) không convert kiểu trước khi API contract chốt; (3) backend thực thi auth/authorization; (4) gửi một GET khi endpoint có route; (5) validate envelope/business code/trace ID và field types; (6) map `kind/status/result` chỉ sau khi schema/enum/by-kind result được duyệt; (7) không lưu/cập nhật cache nếu chưa có freshness policy; (8) hiển thị đúng status hoặc branch theo policy.
- **Current behavior:** API #18 không có route/module/query/test; không gửi request. Contract is `D`/Draft, nên call không runnable.
- **Success/error handling:** 200 mapping chưa hoàn tất vì enums/result fields unresolved; 401/403/404 expected design codes, nhưng wrong-owner 403 vs 404 unresolved; 500/network/timeout stay service error and must not become 404. Retry/timeout policy not specified; do not invent.

### `SH07-EV-06` — Làm mới trạng thái / polling (chưa được duyệt)

- **Trigger/element:** timer/refresh transport sau GET đầu; prototype chỉ có note trong hidden modal, không có timer hoặc SSE code.
- **Input:** operation response mới nhất, document visibility/connection state nếu contract sau này yêu cầu.
- **Processing:** hiện không chạy. Chủ API/product cần chốt polling hay SSE, endpoint, interval/backoff, cancellation khi unmount/ẩn tab, retry budget, freshness/cache và terminal states. HTML đề xuất `3000ms + Backoff` hoặc `/operations/{id}/stream`; không có evidence để chọn một.
- **Output:** chưa có response/transition hợp lệ để map; không synthesize percentage/countdown.
- **Dừng polling:** inventory yêu cầu stop theo terminal state nhưng chưa có OperationStatus values/terminal-state set; API #64 `QUEUED/FAILED/SENT` là notification-specific và không được dùng làm generic enum.

### `SH07-EV-07` — Click CTA quay về khóa học

- **Trigger/element:** CTA #19.
- **Input:** không payload; current `href="#"`; prototype đề xuất `data-path="khoa-hoc"`.
- **Target:** `/courses`/GS-01 chỉ là route proposal. Inventory liên kết SH-07 với ST-07/ME-15/AD-21/AD-25, nên generic return-to-courses mâu thuẫn với job origin ở một số flow.
- **Processing/output:** hiện anchor không điều hướng. Chỉ bật route khi product duyệt safe-return/navigation behavior và caller context; không thêm query parameter hoặc history storage tự suy.

### `SH07-EV-08` — Click CTA về trang chủ/logo

- **Trigger/element:** CTA #20 hoặc logo #1/home link #2.
- **Input:** không payload; source `href="#"`.
- **Target:** route `/`/SH-01 là proposal.
- **Processing/output:** không API; runtime router không có. Bật navigation sau khi route target được xác nhận; browser back vẫn theo router policy, chưa có custom return logic.

### `SH07-EV-09` — Click header nav, login hoặc register

- **Trigger/element:** nav #2, link #3, CTA #4.
- **Input:** key của anchor; không có operation ID/request body.
- **Target mapping proposal:** Trang chủ `/`; Khóa học `/courses`; Tìm kiếm `/courses/search`; Đăng nhập `/login`; Đăng ký `/register`.
- **Current processing/output:** tất cả `href="#"`, chỉ có hover CSS; không auth/session guard hoặc router source. Không tự tuyên bố các route đã chạy.

### `SH07-EV-10` — Click footer nav

- **Trigger/element:** footer group #34.
- **Input:** một trong bốn label.
- **Target mapping:** không có route được định nghĩa cho Chương trình đào tạo, Tra cứu chứng chỉ, Quy chế học vụ, Hỗ trợ học viên trong SH-07 inventory/source; `data-path` hiện dùng lại `khoa-hoc`, `tim-kiem`, hoặc `trang-chu` nhưng không đủ căn cứ tạo route.
- **Processing/output:** current `href="#"`; không request. Product xác nhận target hoặc loại link trước implementation.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
