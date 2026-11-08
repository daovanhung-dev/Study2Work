# AD-20 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-20-EV-001` | `Source heading` / EV-01 — Mở trang / khởi tạo | See source event detail below |
| `AD-20-EV-002` | `Source heading` / EV-02 — Điều hướng breadcrumb, shell, quay lại và footer | See source event detail below |
| `AD-20-EV-003` | `Source heading` / EV-03 — Nhập tiêu đề và đồng bộ preview | See source event detail below |
| `AD-20-EV-004` | `Source heading` / EV-04 — Chọn audience/segment | See source event detail below |
| `AD-20-EV-005` | `Source heading` / EV-05 — Chọn delivery channel | See source event detail below |
| `AD-20-EV-006` | `Source heading` / EV-06 — Nhập nội dung và toolbar | See source event detail below |
| `AD-20-EV-007` | `Source heading` / EV-07 — Chọn priority | See source event detail below |
| `AD-20-EV-008` | `Source heading` / EV-08 — Lưu bản nháp | See source event detail below |
| `AD-20-EV-009` | `Source heading` / EV-09 — Gửi thông báo ngay | See source event detail below |
| `AD-20-EV-010` | `Source heading` / EV-10 — Xem trước / mở chi tiết | See source event detail below |
| `AD-20-EV-011` | `Source heading` / EV-11 — Accepted/Correlation/Delivered panel | See source event detail below |
| `AD-20-EV-012` | `Source heading` / EV-12 — Health, bell, account và footer status | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### EV-01 — Mở trang / khởi tạo

- **Element/type:** Route entry `/admin/notifications/new`; `Load`.
- **Precondition:** Expected: authenticated Admin có notification-management permission. Current: Study Web route/router/auth guard không có source.
- **Input:** Candidate route; không có path/query/state/session data source được xác minh.
- **Xử lý hiện tại:** Browser tải HTML prototype; không gọi API, không preload danh sách recipient hay thông tin SMTP.
- **API:** Không có request hiện tại. Future #93 chỉ sau khi request/permission contract được duyệt; không gọi #92 mặc định vì inventory/AC không khai báo preload bắt buộc cho form.
- **Output/state:** Form tĩnh với all-users, In-app và Normal được chọn; preview chứa sample content. Đây là trạng thái artifact, không phải runtime-ready default.
- **Ngoại lệ/điều hướng:** Route not found/session expiry/forbidden chưa có frontend mapping. Backend #93 có 401/403 nhưng chưa có route client để hiển thị. AD-19 là predecessor dự kiến; link hiện inert.

### EV-02 — Điều hướng breadcrumb, shell, quay lại và footer

- **Element/type:** #2–6, #10, #12–13, #43, #52–54; click.
- **Precondition/input:** Người dùng click một anchor đang hiển thị; không có route param/state contract.
- **Xử lý hiện tại:** Các liên kết dùng `href="#"`; không điều hướng tới màn hình ứng dụng. #13 có label AD-19 nhưng không có route handler. #43 không có `notification_id`.
- **API/output:** Không gọi API; vị trí/trạng thái hiện tại không đổi ngoài hành vi mặc định của anchor.
- **Luồng mong đợi:** Quay lại AD-19 theo inventory; chuyển AD-21/SH-07 chỉ theo contract tương ứng. Safe-return/history behavior và target footer chưa được xác định; không truyền dữ liệu tự tạo.

### EV-03 — Nhập tiêu đề và đồng bộ preview

- **Element/type:** #20 → #41/#45; `input`.
- **Precondition/input:** Người dùng nhập chuỗi trong `#notice-title`; giá trị HTML là string. Không có frontend validation event ngoài preview.
- **Bước 1–3:** Script gọi `.trim()` và hiển thị chuỗi đã trim bằng `textContent`. Nếu sau trim rỗng thì hiển thị `[Tiêu đề thông báo mẫu sẽ hiển thị tại đây]`.
- **API:** Không gọi. Khi submit sau này, catalog #93 chỉ yêu cầu `title:string`; local validator bổ sung nonblank và max 200 như fallback chưa duyệt.
- **Output/lỗi:** Preview heading đổi đồng bộ; model/query/cache không đổi. Không có error state, max-length UI, debounce hay persistence.

### EV-04 — Chọn audience/segment

- **Element/type:** #22–25; radio `change`.
- **Precondition/input:** Một trong `all`, `students`, `staff` được chọn; default `all`. Các value/descriptions thuộc mockup.
- **Xử lý hiện tại:** Browser cập nhật radio selection. Không truy vấn user/course/role; không tạo recipients ID; technical note tĩnh không đổi.
- **API/validation:** #93 design cho recipients? hoặc segment?, nhưng AudienceSegment enum/predicate và XOR rule chưa xác định. Current local validator từ chối mọi request có key `segment` (kể cả null) và yêu cầu `recipients` rõ ràng. Không chuyển `all/students/staff` thành ID list hoặc token tự đặt.
- **Output/ngoại lệ:** Selection chỉ là DOM state; không có count, empty-audience warning hay permission filter. Tính năng gửi bị block tới khi Product/API định nghĩa audience resolver và eligibility.

### EV-05 — Chọn delivery channel

- **Element/type:** #27–28; checkbox `change`.
- **Precondition/input:** Mockup mặc định `app` checked; `email` disabled.
- **Xử lý hiện tại:** Native checkbox state; không có SMTP probe, channel validation hoặc preview binding.
- **API/validation:** Catalog `channels:NotificationChannel[]` chưa liệt kê token. Local API chỉ chấp nhận exact `PUSH`/`EMAIL`, không rỗng/không trùng. `app` không được tự map thành `PUSH`; Email disabled copy không chứng minh backend/provider state.
- **Output/ngoại lệ:** Không gọi API. Khi API contract được xác nhận, lựa chọn channel không hợp lệ cần hiển thị 422 theo business code, nhưng thông điệp/selector repair flow chưa được duyệt.

### EV-06 — Nhập nội dung và toolbar

- **Element/type:** #30–31 → #42/#45; textarea `input`; toolbar `click`.
- **Precondition/input:** Body là plain string; toolbar trình bày B/I/link/list affordances.
- **Xử lý hiện tại:** `input` đọc textarea, trim và hiển thị chuỗi đã trim; blank thì phục hồi sample snippet. Toolbar buttons không có listener và không thay đổi body.
- **API/validation:** Không gọi. #93 catalog yêu cầu `content:string`; local validator chỉ từ chối whitespace-only, không thêm max length. Không gửi HTML/markup vì editor schema, escaping và sanitizer chưa được xác định.
- **Output/ngoại lệ:** Preview hiển thị text bằng `textContent`; không có autosave, formatting state, persistence hoặc lỗi nhập liệu.

### EV-07 — Chọn priority

- **Element/type:** #33–34; radio `change`.
- **Precondition/input:** `normal` checked; `urgent` là option khác.
- **Xử lý hiện tại:** Native selection đổi; preview priority badge #44 vẫn ghi “Bình thường”.
- **API:** Không có `priority` trong catalog/local #93 body. Không thêm field hoặc suy ra queue/provider priority.
- **Output/ngoại lệ:** Chỉ DOM selection; ảnh hưởng nghiệp vụ chưa được định nghĩa. Cần Product/API quyết định trước khi UI giữ control này trong luồng gửi.

### EV-08 — Lưu bản nháp

- **Element/type:** #36; button click.
- **Precondition/input:** Không có handler; form có thể chứa title/content và native choices.
- **Xử lý hiện tại:** Click không tạo side effect, không có loading/success/error state.
- **API:** Không có draft-create endpoint/field được xác nhận. #93 không có `action`, `status` hoặc `scheduled_at`; #94 update draft/scheduled không xác định cách tạo draft mới.
- **Output/ngoại lệ:** Không có dữ liệu được lưu. Không hiển thị thành công. Chức năng bị block tới khi owner chỉ rõ API/body/lifecycle của draft.

### EV-09 — Gửi thông báo ngay

- **Element/type:** #37; click/submit dự kiến.
- **Precondition hiện tại:** Button `disabled`; không có handler. Điều kiện title, recipients, segment, channels và confirmation chưa được implement.
- **Request contract theo catalog:** `POST /api/v1/admin/notifications`; `Authorization: Bearer <JWT>`; catalog role Admin. Body: `recipients?:int64[]`, `segment?:AudienceSegment`, required `title:string`, `content:string`, `channels:NotificationChannel[]`. Catalog liệt kê 202 `DESIGN_OPERATION_ACCEPTED`, 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 503 `DESIGN_DEPENDENCY_UNAVAILABLE`, 500 `DESIGN_INTERNAL_ERROR`. Không có idempotency field/header được #93 row khai báo.
- **Current local fallback request:** route yêu cầu body title/content/channels; validator yêu cầu recipients IDs explicit, positive unique int64; reject segment; nonblank title/content; title ≤200; nonempty unique `PUSH|EMAIL`. Query chỉ xác nhận ID tồn tại; không lọc role/status/course/tenant.
- **Xử lý current source nếu được gọi ngoài UI:** shared ADMIN guard trước parse body; query recipients; insert một notification per recipient và delivery `QUEUED` per channel; tạo UUID chung; validate `ApiEnvelope` projection; commit toàn batch; trả 202 `DESIGN_OPERATION_ACCEPTED`, `data` là notification đầu tiên, `meta.operation_id` UUID và `meta.notification_ids` int64[]. Không tạo Operation row hoặc gọi provider/worker.
- **Response discrepancy:** catalog/AC-36 ghi data Notification; phần operation tracking tổng quát ghi data Operation. Không tự xử lý `meta.operation_id` như API #18 ID vì #18 path row là int64 còn UUID metadata/schema là UUID, và route #18 chưa tồn tại.
- **Lỗi/đầu ra:** 401/403 auth; 422 body/segment/recipient/channel/unknown recipient; 503 DB operational/unavailable fallback; 500 query/projection/commit khác. Source cố rollback lỗi batch. Chỉ local 202 sau commit; không đồng nghĩa gửi/delivered. Client retry policy, timeout/idempotency và message display chưa được duyệt, nên không tự retry.
- **Điều hướng:** Không mở SH-07 đến khi operation response field/type, #18 contract/runtime, owner scope và lifecycle được thống nhất. Không mở AD-21 chỉ từ metadata hiện tại.

### EV-10 — Xem trước / mở chi tiết

- **Element/type:** #38–45; preview local; click #43.
- **Input/xử lý:** Title/body từ EV-03/EV-06 được mirror; source/time/channel/priority và “Xem chi tiết” là static copy. Link `#` không mang notification ID.
- **API/output:** Không gọi #92/#96; không có notification persisted. Không dùng preview để khẳng định channel/priority/date thực tế.

### EV-11 — Accepted/Correlation/Delivered panel

- **Element/type:** #46–50; static status copy.
- **Input/xử lý:** Không có backend response, timer, queue event, polling, SSE hoặc status mapping. Các ba bước là narrative/mockup.
- **API/output:** Không gọi #18, #96 hoặc provider. Không tự chuyển trạng thái accepted→delivered theo thời gian. Local #93 only commits queued intent/outbox fallback; delivery worker/provider chưa được chứng minh.

### EV-12 — Health, bell, account và footer status

- **Element/type:** #1, #7–9, #11, #51; shell status/copy/control.
- **Input/xử lý:** Nội dung tĩnh; bell/profile không có handler hoặc source dữ liệu; RBAC/health labels không được xác minh.
- **API/output:** Không có request/auth/session-health source trong Study Web. Không đưa ra claim health, quyền hay phiên đăng nhập từ các nhãn này.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
