# AD-21 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Mô tả luồng hoạt động tổng thể

### B.1. Expected flow — chỉ khi contract và frontend được duyệt

1. AD-19 điều hướng tới candidate route và truyền `notificationId` lấy từ dữ liệu đã xác thực. Không tạo ID ở client. Hiện inventory chưa chốt cách serialize/filter ID; API #94–#96 catalog khai báo int64.
2. Router kiểm tra phiên và quyền theo shared Study policy. Backend phải áp dụng quyền; AC-36 notification-management permission và local shared role `ADMIN` chưa được chứng minh tương đương.
3. Nếu ID hợp lệ và API #96 được chọn làm read source, gửi một `GET /api/v1/admin/notifications/{notification_id}/status` với Bearer JWT, không query/body. Kiểm tra HTTP status, envelope (`success`, `businessCode`, `data`, `traceId`), rồi validate Notification fields trước khi render.
4. #96 có thể cung cấp `id`, `title`, `content`, `channels`, `status`, `created_at` trong current local projection. API không trả recipient, per-channel status, delivery count/progress, schedule hay Operation. Không thể dùng response này để lấp tất cả mockup fields.
5. Chỉ expose edit/delete controls sau khi policy và API contract được duyệt. #94 direct catalog chưa khai báo body; local handler lại yêu cầu `{title, content}` và chỉ sửa các delivery còn `QUEUED`. #95 direct contract là delete result; AC-36 cho phép delete/mark cancelled theo policy, còn local handler hard-delete row và không dừng provider.
6. Chỉ mở SH-07 khi một producer trả Operation ID mà type/field/owner contract tương thích API #18. Hiện AD-20 #93 local `meta.operation_id` là UUID, trong khi API #18 row khai báo int64; reusable schema/AC lại nói UUID và Study #18 chưa wired.
7. Theo từng HTTP/business error đã được contract công bố, render lỗi đã duyệt và không biến 500/network thành not-found. Không có retry, timeout, cache, polling cadence hay refresh policy được xác định trong các API này.

### B.2. Stitch prototype baseline trong checkout

1. Stitch `code.html` là asset HTML tĩnh; bản thân asset không có router, session manager hay API client. Trạng thái này chỉ mô tả prototype, không mô tả Angular app.
2. HTML render placeholder ID `--`/“Chưa nạp tham số ID hợp lệ”, Operation “Chưa liên kết”, status “Chờ xác thực”, static info banner và channel cards/counters.
3. Không có input hoặc dữ liệu động. No `fetch`, XHR, feature event handler, timer, polling, cache, API response mapping hoặc state transition được thực hiện.
4. “Cập nhật bản nháp”, “Hủy bỏ phát hành” và nút SH-07 đều có `disabled`; click handler không tồn tại. Header notification button không handler; navigation/return/footer anchors dùng `href="#"`.
5. Stitch asset không điều hướng tới AD-19/SH-07 hoặc thực hiện update/delete. Các mô tả về SMTP, “System Normal”, RBAC, completion `0/0`, lock và status là copy của mockup, không chứng minh hệ thống thực.

### B.3. Current Study Web source flow

1. Angular Admin router registers `/admin/notifications/:notificationId` with `AD21Page`; the page reads the route parameter as text and calls GET #96 through `AD21ApiService` and `AdminApiService`.
2. Shared route state renders loading, loaded or error. On success, the page maps only returned Notification fields through `renderNotificationStatusFields`; status values remain raw. The shared error mapper handles 401/403/404 and other failures.
3. The page displays title, content, channels, aggregate status and creation time. Recipient, schedule, delivery counts/per-channel state and Operation ID remain unavailable because #96 does not return them.
4. Edit, delete and SH-07 controls remain disabled. AD-21 does not call #94/#95/#18 and does not poll. The return link is an Angular RouterLink to `/admin/notifications`.
5. Source wiring and local tests do not establish live database, deployment or browser runtime behavior.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

### State matrix — Stitch prototype baseline

| State | Điều kiện / nguồn | UI hiện tại / xử lý được phép |
|---|---|---|
| `STITCH_STATIC` | Static Stitch HTML has no Angular router. | This describes the design asset; current Angular route/page are source-wired. |
| `ID_UNRESOLVED` | Mockup has no valid notification ID; caller contract not implemented. | Show “Chưa nạp tham số ID hợp lệ”; do not call #94/#95/#96. |
| `OPERATION_UNRESOLVED` | #96 returns no Operation ID; #18 is source-wired but type/result/owner contract conflicts remain open. | Show “Chưa liên kết”; keep SH-07 action disabled. |
| `DETAIL_UNAVAILABLE` | Static notice says no separate detail endpoint; #96 response is limited and not bound. | Show placeholder fields only in prototype; no mock response or fabricated recipient/count. |
| `ACTIONS_LOCKED` | HTML disables update/cancel/SH-07 buttons. | No event/network request. Do not convert disabled state to an assumed business eligibility rule. |
| `#96 RESPONSE — QUEUED/FAILED/SENT` | Values are local source fallback over candidate tables, not approved canonical lifecycle. | A future UI must preserve raw value until mapping is approved; do not map `SENT` to `delivered` or `QUEUED` to `draft/scheduled`. |
| `AUTH / ACCESS / NOT_FOUND / VALIDATION / SERVER_ERROR` | Catalog errors per endpoint; #96 has no 422, #94/#95 do. | Future error presentation and SH-05/SH-06 navigation require shared client policy. Preserve HTTP/business code; do not turn network/500 into 404. |
| `DELETED` / `CANCELLED` | #95 local `DeleteResult` says `deleted`; AC wording includes mark cancelled. | No confirmed cancellation/soft-delete transition or post-delete route; wait for policy. |
| `OPERATION_ACTIVE / TERMINAL` | API #18 is source-wired, but generic status/result mapping and terminal transitions are unresolved. | AD-21 has no client handoff/poller; no timer or SSE is implemented. |

Inventory expected states `draft/scheduled/sending/delivered/failed` are not mapped to local `QUEUED/SENT/FAILED`. Do not invent a transition graph or use delivery state to infer `is_read`/publication state.

### Current Angular source mapping

| State | Source evidence | Current behavior |
|---|---|---|
| Route registered | `admin.routes.ts` maps `notifications/:notificationId` to `AD21Page`. | Reachable by Angular router when the Admin shell/session allows it; browser runtime not verified. |
| Loading | `adminRouteState` starts the #96 request in loading state. | Shows the page loading message. |
| Loaded | GET #96 envelope is mapped to source-backed Notification fields. | Shows title, channels, content, aggregate status and created time; keeps the status token unchanged. |
| Error | Shared Admin error mapper handles session/auth/access/not-found/server failures. | Shows an error state; 404 remains distinct from a generic server failure. |
| Mutation / SH-07 | Current template keeps all three action buttons disabled. | No #94/#95 call, no #18 handoff and no poller. |

### Navigation and data handoff

| From / to | Expected handoff | Current status |
|---|---|---|
| AD-19 → AD-21 | `notificationId` from selected row; catalog #96 path is int64. | Angular route is registered; AD-19 row renderer builds the detail route for safe integer IDs. Live navigation is not verified. |
| AD-21 → AD-19 | Return to notification list; filter/page preservation is unspecified. | Current page has a RouterLink to `/admin/notifications`; no filter/context preservation is implemented. |
| AD-20 → AD-21 | Notification IDs may be created by #93; API response and batch-vs-recipient grain must be resolved. | #93 catalog returns Notification; local source adds UUID metadata and multiple notification IDs; no generic operation mapping. |
| AD-21 → SH-07 | Valid backend-issued Operation ID and compatible #18 route/owner contract. | Button disabled; #18 backend source route exists, but AD-21 has no client handoff/poller. UUID/int64 and producer/result conflicts remain. |
| AD-21 → SH-05/SH-06 | Shared auth/not-found route behavior if those screens are adopted. | Candidate screens are design artifacts; endpoint error-to-route policy is not defined here. |
| Browser back | Preserve caller/filter context only under approved router behavior. | Angular routing exists; caller/filter preservation is not implemented or verified. |

No route target, cache key, retry policy, polling frequency, confirmation dialog, history behavior or error-navigation path is inferred by this DD.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: #96 là GET status, không có GET detail riêng và không trả delivery counts/per-channel status; #94 catalog path-only nhưng local body `{title,content}`/QUEUED-only là DERIVED; #95 catalog DELETE trả `deleted`, local source hard-delete row và không dừng provider; chỉ gọi #18 sau khi Operation ID/type/owner/producer mapping được duyệt.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [AD-21](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/AD-21.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
