# ME-11 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-11-EV-001` | `ME11-E01` / ME11-E01 — Tải danh sách support request | See source event detail below |
| `ME-11-EV-002` | `ME11-E02` / ME11-E02 — Chọn status tab | See source event detail below |
| `ME-11-EV-003` | `ME11-E03` / ME11-E03 — Chọn khóa học | See source event detail below |
| `ME-11-EV-004` | `ME11-E04` / ME11-E04 — Làm mới inbox | See source event detail below |
| `ME-11-EV-005` | `ME11-E05` / ME11-E05 — Mở request ở ME-12 | See source event detail below |
| `ME-11-EV-006` | `ME11-E06` / ME11-E06 — Header/footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### ME11-E01 — Tải danh sách support request

- **Trigger/type:** route enter / `Load`; không có current frontend handler.
- **Element:** page body `ME11-EL-20`; trigger từ route đề xuất `/mentor/support`.
- **Precondition:** session hợp lệ và role Mentor; URL/query không chứa unapproved defaults. App route/session owner chưa tồn tại.
- **Input/source:** Bearer token từ approved session manager; optional query `course_id:int64` và `status:string` chỉ khi UI mapping được duyệt. Không có request body.
- **Xử lý tuần tự:** (1) Đọc session và role từ auth owner; không dùng header sample. (2) Nếu session thiếu/expired thì route guard hiển thị auth-required/session-expired theo shared Study UI contract còn chờ; không gửi raw token. (3) Khi có quyền, GET #58. (4) Xử lý 200 envelope; kiểm tra `success`, `businessCode`, `data` type; giữ `traceId` phục vụ support mà không log message content. (5) `data=[]` → empty state; `data` có item → loaded state còn block bởi thiếu row design. (6) Chỉ map projection fields có trong contract; không giả lập title, unread, SLA, counter hoặc last update. (7) Giữ dữ liệu hiện tại nếu refresh sau đó thất bại theo quyết định UI cần duyệt.
- **API/result:** #58 như B.1. Error map: 401 → auth-required; 403 → access denied; 422 → invalid query/filter (xác nhận query UI trước khi gửi); 500/network/timeout → list error; error `data` là null. Không retry tự động nếu chưa chốt idempotent GET retry/backoff policy; GET không tạo mutation.
- **Current source:** prototype không gọi API; API backend code/test source hiện có. AC-24 starts #58. Empty state screenshot/AC precondition discrepancy vẫn mở.

### ME11-E02 — Chọn status tab

- **Trigger/type:** click/keyboard activation trên `ME11-EL-15`…`ME11-EL-17`; `Click`/`Change` theo tab semantics.
- **Precondition/input:** selected tab ID; HTML hiện chỉ có `all/open/resolved`; counts là static `0`. Không có approved filter mapping.
- **Current handler:** thay `aria-selected` và classes/style; không thay list/count và không gọi API.
- **Expected implementation pending contract:** chuẩn hóa selection thành confirmed filter (hoặc local predicate trên loaded data); chốt “Open” grouping gồm những status nào và xử lý CANCELLED; xác định count source. Nếu server filter dùng `status`, gửi đúng exact status string. Không gọi API với nhãn “Open” như status literal nếu contract chưa nêu value.
- **Result/errors:** current result chỉ visual selection. Future result cập nhật selected tab và data atomic sau khi filter success; lỗi giữ filter/data trước đó theo UX decision. Loading, rapid clicks, count facets, focus/keyboard behavior cần design.

### ME11-E03 — Chọn khóa học

- **Trigger/type:** change `ME11-EL-19`.
- **Input/current:** `all`, `fe-adv`, `be-node`, `fullstack-capstone` hardcoded values và sample labels.
- **Current handler:** none; không fetch, không filter.
- **Expected implementation pending contract:** chốt option source, label field và positive-int64 `course_id` mapping. API #46 có source-backed paged Mentor course list nhưng chưa là dependency inventory của ME-11; không tự thêm request. `all` sentinel cần map thành omit `course_id`, khi đã được duyệt.
- **Validation/result:** không gửi slug/zero/non-int64; #58 enforces 1..2^63−1. Existing foreign course → 403; nonexistent positive ID → 200 empty. Invalid integer → 422. Chốt loading/error/selection retention của option source.

### ME11-E04 — Làm mới inbox

- **Trigger/type:** click `ME11-EL-24`; `Click`.
- **Current input/behavior:** không đọc filter/data; button bị disable và có spinner trong khoảng 650 ms; sau đó script ghi browser time vào `lastUpdatedTime`. Không có fetch/poll/push.
- **Future implementation pending contract:** đọc filters đã xác nhận, gửi lại #58, áp dụng response theo E01. Chống double-click bằng in-flight state; timeout/retry/backoff và hủy request khi unmount chưa được contract định nghĩa.
- **Output/errors:** 200 → cập nhật list/empty state; 401/403 theo E01; 422 filter invalid giữ filter và yêu cầu xử lý mapping; 500/network → giữ last successful rows nếu có, hiển thị refresh failure/stale indicator chỉ sau khi UI được duyệt. Không cập nhật “just now” nếu response không xác nhận timestamp/server freshness.

### ME11-E05 — Mở request ở ME-12

- **Trigger/type:** click/keyboard activation trên loaded request row; **row không tồn tại trong PNG/HTML** nên chưa có marker riêng.
- **Precondition/input:** cần một item từ #58 response, `requestId = data[i].id` positive int64; Mentor vẫn có session hợp lệ.
- **Current behavior:** không có row hoặc navigation handler.
- **Expected handoff:** sau khi product duyệt row layout, chuyển đúng `requestId` sang proposed `/mentor/support/:requestId`. ME-12 owns #59 detail; E05 của ME-11 không gọi #59/#60/#61 theo flow inventory. Không truyền thread text hoặc attachment URL qua query/navigation state nếu không cần; ME-12 reloads via #59 theo flow F09.
- **Failure/edge:** row stale/deleted/permission changed có thể lỗi tại ME-12; invalid/missing ID handling thuộc ME-12 contract. Back-to-list/filter retention chưa được chốt.

### ME11-E06 — Header/footer navigation

- **Trigger/type:** click/keyboard activation trên link elements `ME11-EL-01`…`ME11-EL-07`, `ME11-EL-31`…`ME11-EL-33`.
- **Current behavior:** tất cả anchor đều `href="#"`; không có route state, data handoff hoặc external destination đã khai báo.
- **Expected behavior pending wiring:** map từng `data-path`/footer link sang route/destination được duyệt, áp dụng shared Mentor auth/role guard, preserve or reset inbox filters according to approved navigation policy. Notification dot không được xem là count/state nếu không có source.
- **Result/errors:** destination-specific. ME-11 không mutate support data khi rời trang. Link access/expired session xử lý theo shared app shell khi tồn tại.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
