# ST-01 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-01-EV-001` | `ST01-EV-01` / ST01-EV-01 — Entry và Student session gate | See source event detail below |
| `ST-01-EV-002` | `ST01-EV-02` / ST01-EV-02 — Load khóa học qua API #20 | See source event detail below |
| `ST-01-EV-003` | `ST01-EV-03` / ST01-EV-03 — Load/ghép tiến độ qua API #21 | See source event detail below |
| `ST-01-EV-004` | `ST01-EV-04` / ST01-EV-04 — Load achievements qua API #38 | See source event detail below |
| `ST-01-EV-005` | `ST01-EV-05` / ST01-EV-05 — Load notifications qua API #43 | See source event detail below |
| `ST-01-EV-006` | `ST01-EV-06` / ST01-EV-06 — Điều hướng tới ST-08 | See source event detail below |
| `ST-01-EV-007` | `ST01-EV-07` / ST01-EV-07 — Điều hướng tới ST-20 | See source event detail below |
| `ST-01-EV-008` | `ST01-EV-08` / ST01-EV-08 — Điều hướng tới ST-26 | See source event detail below |
| `ST-01-EV-009` | `ST01-EV-09` / ST01-EV-09 — Header, breadcrumb và footer navigation | See source event detail below |
| `ST-01-EV-010` | `ST01-EV-10` / ST01-EV-10 — Partial widget, empty, access và API failure states | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết event

Event groups below distinguish proposed behavior from current static prototype. API calls are catalog-only and remain blocked until contracts/source are approved.

### ST01-EV-01 — Entry và Student session gate

- **Trigger / loại:** `Load` route `/student`.
- **Element / điều kiện tiên quyết:** route inventory; ST01-EL-03, EL-04, EL-08. AC-13/18/20 yêu cầu Student đã đăng nhập.
- **Input:** proposed route and authenticated session/role; không có `user_id` request field.
- **Xử lý:** (1) route chưa tồn tại trong Study Web; (2) khi có implementation, chỉ cho gọi widget APIs sau khi shared Student-session policy được nối; (3) current mockup sample name và contract-gate copy không dùng làm auth/data result; (4) không tự chọn redirect/session-expiry policy.
- **Output:** hiện chỉ static page. Intended state sau khi access quyết định chưa thể kiểm tra.
- **Ngoại lệ:** UI route 401/403, session refresh, return route và unauthenticated destination chưa có Study Web source; catalog statuses của endpoint không tự định nghĩa page-level guard.

### ST01-EV-02 — Load khóa học qua API #20

- **Trigger / loại:** widget load sau page entry (`Load`), theo inventory.
- **Element / điều kiện tiên quyết:** ST01-EL-09/10; Student session; #20 contract và route phải được xác nhận.
- **Input:** `GET /api/v1/users/me/courses`, Bearer Student; query catalog `status?:string`, `page?:int32`; no body. Không dùng `/api/v1/courses/enrolled` từ HTML.
- **Xử lý:** (1) không gửi request trong current prototype; (2) catalog response là `ApiEnvelope<UserProfile>` mặc dù AC-13 cần Enrollment/Course list; (3) không chọn status/default/page, không map UserProfile thành course list; (4) không phát sinh empty collection hoặc Course shape.
- **Output:** catalog success 200 `DESIGN_RESOURCE_RETRIEVED` có schema mismatch; widget hiện là static “Chưa nạp được danh sách khóa học”, không phải API empty response.
- **Ngoại lệ:** catalog #20 liệt kê 401/403/422/500; role/validation/query behavior chưa có route source. Empty, page range và status filter semantics đang mở.

### ST01-EV-03 — Load/ghép tiến độ qua API #21

- **Trigger / loại:** widget load (`Load`) và data merge sau #20 nếu AC-13 được giữ.
- **Element / điều kiện tiên quyết:** ST01-EL-12/13; Student session; #21 schema/query, #20 merge key và orchestration phải được thống nhất.
- **Input:** `GET /api/v1/users/me/progress`, Bearer Student; catalog ghi `course_id list hoặc aggregate?:string`; no body. Không chuẩn hóa grammar theo suy đoán.
- **Xử lý:** (1) current prototype không gọi endpoint; (2) AC-13 dự kiến ghép course + progress ở client, nhưng response #21 là `UserProfile` và không có progress DTO/merge key; (3) không tính percent, time, KPI, denominator/rounding hoặc trạng thái completed; (4) giữ AC-18 sequence #21→#37→#38 tách biệt với inventory gọi widget độc lập.
- **Output:** không có progress result hoặc chart; static no-data copy không chứng minh API trả rỗng.
- **Ngoại lệ:** catalog #21 liệt kê 401/403/500; aggregate selection, identity binding, no-progress/no-enrollment và partial failure chưa chốt. Không thêm 422.

### ST01-EV-04 — Load achievements qua API #38

- **Trigger / loại:** widget load/lazy request (`Load`) theo inventory.
- **Element / điều kiện tiên quyết:** ST01-EL-15/16; Student session; award/projection/filter/page semantics đã được duyệt.
- **Input:** `GET /api/v1/users/me/achievements`, Bearer Student, optional `course_id:int64`; no body. Không dùng `/api/v1/achievements` từ HTML.
- **Xử lý:** (1) không gọi API trong static page; (2) catalog `Page<Achievement>` chỉ có logical identity/title/time/course fields; (3) không suy certificate, proof signature, count hoặc KPI; (4) không quyết định course filter, default page/order, empty shape hoặc AC-18 timing.
- **Output:** current widget hiển thị gated/no-certificate copy; không phải evidence rằng Student chưa có award hoặc #38 trả empty.
- **Ngoại lệ:** 401/403/500 theo catalog; award criteria, response source, course access, query parse và empty behavior vẫn mở; không thêm 404/422.

### ST01-EV-05 — Load notifications qua API #43

- **Trigger / loại:** widget load/lazy request (`Load`) theo inventory.
- **Element / điều kiện tiên quyết:** ST01-EL-17/18; Student session; recipient/projection/order contract được thống nhất.
- **Input:** `GET /api/v1/users/me/notifications`, Bearer Student; `unread_only?:boolean`, `page?:int32`; no body. Không dùng `/api/v1/notifications/latest` từ HTML.
- **Xử lý:** (1) current page không gọi #43; (2) catalog mô tả Page, không chốt sort/latest; (3) không tự chọn unread flag, page default/size hoặc map DDL fields vào `channels`, `status`, `read_at`; (4) AC-20 mark-one/all là #44/#45 trong notification center, không chạy trên ST-01.
- **Output:** current gateway-blocked copy là static. Không hiển thị latest item/unread count từ nguồn chưa xác nhận.
- **Ngoại lệ:** 401/403/500 theo catalog; recipient/broadcast, enum, timestamp, pagination/timezone và error-envelope mapping còn mở.

### ST01-EV-06 — Điều hướng tới ST-08

- **Trigger / loại:** click course CTA (anchor).
- **Element / điều kiện tiên quyết:** ST01-EL-11; target inventory ST-08 `/student/courses`; route và role guard phải được wire.
- **Input:** click; không có course ID, status filter hoặc user-supplied identifier.
- **Xử lý:** (1) current `href="#"` không điều hướng; (2) inventory relation xác nhận target screen, không actual href/data handoff; (3) chỉ sau khi route được duyệt mới điều hướng, không tự thêm tham số.
- **Output:** current prototype remains on same document.
- **Ngoại lệ:** route missing, unauthorized entry, return context và focus behavior chưa có policy/source.

### ST01-EV-07 — Điều hướng tới ST-20

- **Trigger / loại:** click progress CTA.
- **Element / điều kiện tiên quyết:** ST01-EL-14; target inventory ST-20 `/student/progress`; Study Web route chưa có.
- **Input:** click; không truyền percentage, course ID hoặc aggregate.
- **Xử lý:** (1) current `href="#"`; (2) không truyền API payload/query theo screenshot; (3) sau route approval chỉ dùng navigation contract được xác nhận.
- **Output:** no current navigation; ST-20 inventory link chỉ là expected relation.
- **Ngoại lệ:** target route, role access, return navigation và duplicate request behavior chưa wired.

### ST01-EV-08 — Điều hướng tới ST-26

- **Trigger / loại:** click notification CTA.
- **Element / điều kiện tiên quyết:** ST01-EL-19; target inventory ST-26 `/student/notifications`.
- **Input:** click; no notification ID or deep-link payload.
- **Xử lý:** (1) current `href="#"`; (2) không thực hiện #44/#45 ở dashboard; (3) deep-link data/return context chờ ST-26 contract.
- **Output:** no current navigation; expected target theo inventory là ST-26.
- **Ngoại lệ:** route/access/deep-link payload và notification list state chưa có current source.

### ST01-EV-09 — Header, breadcrumb và footer navigation

- **Trigger / loại:** click anchor/nav/logo/terms/privacy/help.
- **Element / điều kiện tiên quyết:** ST01-EL-01/02/05/35/36/37; approved route map; Student guard where required.
- **Input:** visible link label; `data-path` values are prototype metadata, current `href="#"`.
- **Xử lý:** (1) phân biệt inventory relationship với actual destination; (2) chỉ ST-08/ST-20/ST-26/ST-02 relationships được inventory nêu; (3) discussions/home/legal/help destinations chưa xác nhận; (4) không truyền session/token qua URL.
- **Output:** current click retains placeholder behavior; no route wired.
- **Ngoại lệ:** direct route, missing destination, session expiry, browser back/focus restoration và external legal/help content chưa được mô tả.

### ST01-EV-10 — Partial widget, empty, access và API failure states

- **Trigger / loại:** API/transport response lifecycle (`Load/Response/Error`) nếu API calls được implement.
- **Element / điều kiện tiên quyết:** ST01-EL-04/08/10/13/16/18; request tương ứng đã được approved và bắt đầu.
- **Input:** per-widget catalog status/error and response. Không có current request/response.
- **Xử lý:** (1) giữ loading/error/empty/403 riêng; (2) partial widget chỉ có thể hiển thị khi từng API có independent state policy; (3) không map server/transport/auth failure thành empty; (4) giữ API status/business codes theo từng catalog row; (5) không tự thêm retry/cache/backoff, toast hoặc bulk fail policy.
- **Output:** inventory yêu cầu independent/partial widget states, nhưng prototype chỉ vẽ gated cards; không có error/loading rendering runtime.
- **Ngoại lệ:** #20 có 422; #21/#38/#43 không khai báo 422. API-specific empty shape và page recovery đều mở. UI-level session redirect và network retry chưa có contract.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
