# AD-22 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-22-EV-001` | `Source heading` / `EV-01` — Khởi tạo hàng đợi | See source event detail below |
| `AD-22-EV-002` | `Source heading` / `EV-02` — Nhập từ khóa tìm kiếm | See source event detail below |
| `AD-22-EV-003` | `Source heading` / `EV-03` — Thay đổi severity | See source event detail below |
| `AD-22-EV-004` | `Source heading` / `EV-04` — Thay đổi reason | See source event detail below |
| `AD-22-EV-005` | `Source heading` / `EV-05` — Thay đổi status | See source event detail below |
| `AD-22-EV-006` | `Source heading` / `EV-06` — Refresh từ thanh công cụ | See source event detail below |
| `AD-22-EV-007` | `Source heading` / `EV-07` — Refresh từ empty state | See source event detail below |
| `AD-22-EV-008` | `Source heading` / `EV-08` — Điều hướng phân trang | See source event detail below |
| `AD-22-EV-009` | `Source heading` / `EV-09` — Mở thảo luận tại AD-23 | See source event detail below |
| `AD-22-EV-010` | `Source heading` / `EV-10` — Shell, notifications, breadcrumb và footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

Các event dưới đây phân biệt hành vi hiện có của HTML với luồng dự kiến khi frontend được wire. Không có retry/timeout/cache contract cho #97; không tự thêm các chính sách đó.

### `EV-01` — Khởi tạo hàng đợi

- **Trigger / loại:** Screen load hoặc route entry; `Load` dự kiến.
- **Điều kiện:** Candidate route được triển khai và auth/authorization policy đã được xác định. Current Study Web chưa có route/client.
- **Input:** Optional `reason:string`, `severity:string`, `page:int32` theo catalog. Nguồn lấy filter từ URL/state/cache chưa được xác định; không tự tạo default khác contract.
- **Expected request:** `GET /api/v1/admin/discussions/reported` + Bearer JWT; no body. Catalog không nêu custom headers khác.
- **Expected sequence:** (1) Kiểm tra session/policy theo shared client/backend rule đã duyệt. (2) Validate query theo contract; catalog không định nghĩa taxonomy hoặc sentinel `all`. (3) Gửi #97. (4) Kiểm tra HTTP/envelope/schema và business code. (5) Ánh xạ đúng Page<Discussion>; chỉ render các field response có. (6) Cập nhật state loading → ready hoặc empty/error theo response.
- **Response/error:** 200 `DESIGN_RESOURCE_RETRIEVED`; 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR`. Local source còn trả 422 `DESIGN_VALIDATION_ERROR` cho page sai; đây là DERIVED và catalog chưa liệt kê. UX destination/message per error chưa được chốt.
- **Current result:** HTML render empty state/0 values trực tiếp, không gọi API, không tạo state. Không có retry, timeout, cache hoặc polling.

### `EV-02` — Nhập từ khóa tìm kiếm

- **Trigger / loại:** Input `#18`, keystroke/input; `Input`.
- **Điều kiện / input:** Prototype nhận text và có placeholder tìm từ khóa/ID. Không có max length, trim, debounce, URL binding hoặc validation trong source.
- **Current processing:** Không có input/change handler; không gọi API; không lọc table.
- **API assessment:** #97 không có query `q`, `keyword` hoặc Discussion ID. Không được thêm tham số hoặc ghép search với reason/severity theo suy đoán.
- **Output / exception:** Hiện chỉ thay đổi giá trị input trong DOM; kết quả không đổi. Cần bổ sung approved API/search contract và UX rules trước khi đặc tả filtering.

### `EV-03` — Thay đổi severity

- **Trigger / loại:** Select `#19`; `Change`.
- **Prototype input:** `all`, `low`, `medium`, `high`. `all` là option có value literal `all`.
- **Current processing:** Không có listener, state update hoặc request. Nếu gọi current #97 trực tiếp, validator giữ nguyên string và query exact-match `r.severity`; không normalize `all` thành `None`. API DD ghi taxonomy free-form/DERIVED, chưa có allowed values.
- **Expected request if approved:** Chỉ `severity?:string` theo #97. Catalog không định nghĩa mapping `all` → omitted query, page reset, filter combination UI hay sort priority; cần quyết định trước khi implement.
- **Output/error:** Current table không đổi. Local API không trả validation error cho severity taxonomy; unmatched value có thể tạo Page rỗng theo query. Do not treat that as approved filter UX.

### `EV-04` — Thay đổi reason

- **Trigger / loại:** Select `#20`; `Change`.
- **Prototype input:** `all`, `spam`, `inappropriate`, `copyright`.
- **Current processing:** Không listener/request. Current #97 exact-match `reason_code` với chuỗi nhận được và kết hợp AND với severity; không xác thực option list. Value `all` hiện không được bỏ filter tự động.
- **Expected request if approved:** Chỉ `reason?:string` được catalog khai báo. Cần chốt taxonomy, sentinel “Tất cả”, kết hợp filter và reset page. Không lấy report reason từ response #97 vì field đó vắng mặt.
- **Output/error:** Không đổi current UI; không taxonomy validation error trong local source. Unmatched reason trả Page có thể rỗng.

### `EV-05` — Thay đổi status

- **Trigger / loại:** Select `#21`; `Change`.
- **Prototype input:** `pending` được chọn ban đầu; options `investigating`, `resolved`.
- **Current processing:** Không listener/request. Catalog #97 không nhận status; current local query luôn chọn report `OPEN` hoặc `IN_REVIEW` và không nhận status param.
- **Expected handling:** Không được gửi status, tự map `pending` sang `OPEN/IN_REVIEW`, hoặc map `resolved` cho đến khi API/business contract xác nhận status taxonomy và semantics.
- **Output:** Prototype giữ giá trị local; không filter server/table.

### `EV-06` — Refresh từ thanh công cụ

- **Trigger / loại:** Click button `#22` / `#btn-refresh`.
- **Điều kiện / input:** Nút không disabled; giữ nguyên query hiện tại (nếu frontend về sau có state, persistence policy cần được xác định).
- **Current processing:** `handleRefreshAction()` thêm class `animate-spin` cho `#refresh-icon`, xóa sau 700 ms. Không fetch/XHR, không reset filter/page, không cập nhật dữ liệu/cache.
- **Expected processing:** Refresh dữ liệu có thể gọi lại #97 chỉ sau khi API client/query-state behavior được duyệt. Không mặc định gọi lại, debounce, retry hoặc phát sinh success toast từ click này.
- **Output/error:** Hiện chỉ thấy spinner; không có network error/success state.

### `EV-07` — Refresh từ empty state

- **Trigger / loại:** Click button `#33`; `Click`.
- **Điều kiện / input:** Button visible trong prototype empty state.
- **Current processing:** Inline `onclick` gọi cùng `handleRefreshAction()`; chỉ spinner icon trong handler đã bind, không gọi API.
- **Expected processing/output:** Tương tự EV-06. Không thể khẳng định có report mới hoặc queue được tải lại. Empty state chỉ được thay đổi sau response mới nếu future client có #97 integration.

### `EV-08` — Điều hướng phân trang

- **Trigger / loại:** Click controls `#37–#41`; `Click` dự kiến.
- **Current precondition:** First/previous/next/last đều `disabled` và `aria-disabled="true"`; current page box `0` là static div; không listener.
- **API contract:** #97 có `page?:int32`, không có `size`. Current local source default page 1, size 20, positive signed-int32; fixed size/order là DERIVED. Catalog chưa quyết định page indexing/default.
- **Expected sequence:** Chưa thể đặc tả next/previous bounds, count display convention (ví dụ `0/0`), page reset khi filter đổi, preservation hoặc active-state semantics mà không có paging rules. Không gửi request từ disabled prototype controls.
- **Current output:** Không đổi page, không request.

### `EV-09` — Mở thảo luận tại AD-23

- **Trigger / loại:** Chọn một hàng/cột action (#23–#29); expected `Click` trên row/action.
- **Current precondition:** Prototype hiện không có row hoặc row action, chỉ empty state và header. Do đó không có event runtime.
- **Expected input/handoff:** Discussion `id` từ một `Page<Discussion>` item là candidate `discussion_id:int64` cho `/admin/discussions/:discussionId/moderate` / #98. Không dùng report ID: #97 không trả report ID. Không có query-state/return-state contract.
- **Expected API detail:** #98 direct catalog là GET với path int64, Bearer JWT, `ApiEnvelope<Page<Discussion>>`, errors 401/403/404/500. AC-37 mong đọc full thread/comments/reports nhưng current #98 source không query report relation; #98 DD lại ghi `UNWIRED / NOT_FOUND`. Handoff chưa đủ dữ liệu để nói “đang xem báo cáo” đã được hỗ trợ.
- **Output/error:** Chỉ điều hướng sau khi #98 route/permission/response và report handoff được thống nhất. #99/#100 actions không thực hiện từ danh sách.

### `EV-10` — Shell, notifications, breadcrumb và footer navigation

- **Trigger / loại:** Click shell nav, breadcrumb, bell hoặc footer anchors.
- **Current behavior:** Shell/footer anchors dùng `href="#"`; breadcrumb không có Study router mapping; bell có `aria-label` nhưng không có handler. Không gọi API hoặc mở screen/modal.
- **Expected output:** Destination của admin shell, policy/RBAC/support pages và notifications inbox chưa được cung cấp trong AD-22 contract. Không gán các phần tử này sang AD-23 hoặc màn hình khác theo suy đoán.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
