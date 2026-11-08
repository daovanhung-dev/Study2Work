# AD-21 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-21-EV-001` | `Source heading` / `EV-01` — Initial route/load và status read | See source event detail below |
| `AD-21-EV-002` | `Source heading` / `EV-02` — Shell navigation và breadcrumb | See source event detail below |
| `AD-21-EV-003` | `Source heading` / `EV-03` — Mở Notifications từ header | See source event detail below |
| `AD-21-EV-004` | `Source heading` / `EV-04` — Quay lại AD-19 | See source event detail below |
| `AD-21-EV-005` | `Source heading` / `EV-05` — Cập nhật bản nháp (#94) | See source event detail below |
| `AD-21-EV-006` | `Source heading` / `EV-06` — Hủy bỏ phát hành / DELETE #95 | See source event detail below |
| `AD-21-EV-007` | `Source heading` / `EV-07` — Handoff SH-07 / API #18 | See source event detail below |
| `AD-21-EV-008` | `Source heading` / `EV-08` — Footer policy/support links | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### `EV-01` — Initial route/load và status read

- **Element / loại:** #14/#20/#22, route load; `Load` (future route behavior only).
- **Điều kiện:** Candidate route phải được triển khai; phải có `notificationId` từ caller. Current prototype không có router và ID hợp lệ nên không gửi request.
- **Input:** API catalog path `notification_id:int64!`; Bearer JWT. Không query/body. Không dùng `operation_id` thay `notification_id`.
- **Quy trình:** (1) nhận route param; (2) không tự cấp ID; kiểm tra theo type đã được route contract chốt; (3) kiểm tra auth/authorization ở server, giữ khác biệt AC permission với local role `ADMIN`; (4) nếu source/contract được duyệt, gọi một lần `GET /api/v1/admin/notifications/{notification_id}/status` (#96); (5) parse status/envelope; direct success 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Notification>`; (6) validate `data` rồi map chỉ các field có trong response; (7) hiển thị trạng thái loading/success/error theo UI contract khi được chốt; (8) không poll #18 hoặc gọi provider.
- **Current local #96:** auth guard `ADMIN` chạy trước path parsing; positive signed int64 lookup; malformed/out-of-range ID → 404. Query đọc `notifications` cùng aggregate `notification_deliveries`; no notification/no deliveries → 404. Status precedence local: any `QUEUED` → `QUEUED`; else any `FAILED` → `FAILED`; else all `SENT` → `SENT`. Response có id/title/content/channels/status/created_at, không có recipient/count/per-channel/scheduled_at/read_at. Read-only, không commit.
- **Errors / giới hạn:** Catalog #96 chỉ có 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`. Không thêm 422. UI/client error route mapping, retry/timeout/cache chưa có contract. Do not claim `SENT=delivered`.
- **Kết quả:** Current page không đổi theo API vì không có API client; current display vẫn là static placeholders. Target mapping cần owner approval do inventory enum và local enum khác.

### `EV-02` — Shell navigation và breadcrumb

- **Element / loại:** #2–#6 anchors và #10–#12 breadcrumb text; `Click` nếu có.
- **Điều kiện / input:** Không có route target hay state payload.
- **Current xử lý:** Các nav anchor `href="#"` dẫn fragment rỗng; breadcrumb là text/span. Không có router listener.
- **Kết quả / lỗi:** Không chuyển tới màn hình Study route đã xác nhận; không có API. Nếu app được xây dựng, route map phải được xác định ngoài artifact này.

### `EV-03` — Mở Notifications từ header

- **Element / loại:** #8 button; `Click`.
- **Điều kiện / input:** Button không disabled, accessible label `Notifications`; unread dot là static.
- **Current xử lý:** Không có click handler, destination, menu/modal hoặc API. Không cập nhật dot/count.
- **Kết quả:** Không có kết quả nghiệp vụ; không mô tả nó như notifications inbox.

### `EV-04` — Quay lại AD-19

- **Element / loại:** #13 anchor styled as button; `Click`.
- **Điều kiện / input:** Không yêu cầu ID ở markup. Không có query/filter/scroll state được truyền.
- **Current xử lý:** `href="#"`, không dùng router/back API; anchor chỉ điều hướng fragment rỗng.
- **Kết quả:** AD-19 không được mở bởi current source. Future return route và giữ filter/context cần contract; không tạo `returnTo` hay payload giả định.

### `EV-05` — Cập nhật bản nháp (#94)

- **Element / loại:** #33 button; `Click`/`Submit` trong thiết kế.
- **Điều kiện / input hiện có:** Button disabled; #26/#30 là static `<div>` placeholder `--`, không có `input`/`textarea`; không có title/content để submit. Current flow dừng ở UI.
- **Direct API contract:** `PUT /api/v1/admin/notifications/{notification_id}`; Bearer JWT/Admin; path int64; catalog không khai báo body/query; success 200 `DESIGN_RESOURCE_UPDATED`, `ApiEnvelope<Notification>`; errors 401/403/404/422/500.
- **Current local fallback (DERIVED):** (1) guard `ADMIN` trước validation/DB; (2) validate positive int64 cùng JSON strict `{title, content}`, title max 200 và không blank; (3) lock parent rồi delivery rows theo channel; (4) yêu cầu ≥1 delivery và tất cả `QUEUED`, nếu không trả 422 `DESIGN_VALIDATION_ERROR` / `NOTIFICATION_NOT_EDITABLE`; (5) update chỉ `notifications.title/content`; (6) validate Notification response, gồm channels/status `QUEUED`; (7) commit rồi trả 200. Errors additionally 404 missing, 500 query/projection/commit; rollback khi lỗi DB/mapping.
- **Discrepancy:** Body, field rules và queued-only edit gate không được direct catalog/AC-36 path-only mô tả phê duyệt. Local `QUEUED` không bằng `draft` hay `scheduled`. UI hiện không có field để lấy request body.
- **Kết quả / next:** Không enable button, gửi body hoặc cập nhật cache cho tới khi owner chốt request/status/lifecycle. Không retry mutation tự động hoặc thêm idempotency policy khi catalog chưa có.

### `EV-06` — Hủy bỏ phát hành / DELETE #95

- **Element / loại:** #39 button; `Click`/confirmation dự kiến nhưng không có dialog trong prototype.
- **Điều kiện / input hiện có:** Button disabled; không có ID, confirm state, handler hay API call.
- **Direct API contract:** `DELETE /api/v1/admin/notifications/{notification_id}`; Bearer JWT/Admin; path int64, không body/query; success 200 `DESIGN_RESOURCE_DELETED`, `ApiEnvelope<DeleteResult>`; errors 401/403/404/422/500.
- **Current local fallback (DERIVED):** (1) guard `ADMIN`; (2) validate positive int64; (3) lock parent trước delivery rows; (4) chỉ tiếp tục khi ≥1 delivery và mọi status là `QUEUED`, nếu không 422 `NOTIFICATION_NOT_CANCELLABLE`; (5) delete đúng parent row; candidate DDL cascade delivery rows; (6) validate `{id, status:"deleted", deleted_at}`; (7) commit và trả envelope. Missing/repeat delete → 404; DB/mapping/commit failure → safe 500 và rollback.
- **Tác động / blocker:** AC-36 gọi nhánh DELETE/mark cancelled; local source xóa vật lý một recipient-level legacy BIGINT row, không điều phối scheduler/worker/provider và không chứng minh stop delivery. Chưa chốt delete-vs-soft-delete-vs-cancel, retention, race hoặc repeat semantics. Không gọi endpoint hiện tại từ UI.

### `EV-07` — Handoff SH-07 / API #18

- **Element / loại:** #21/#42/#43; `Click`/navigation được dự kiến.
- **Điều kiện / input:** Nút disabled; Operation ID đang “Chưa liên kết”. Không suy Operation ID từ notification ID.
- **Expected API #18:** `GET /api/v1/operations/{operation_id}`, Bearer JWT, catalog success 200 `DESIGN_OPERATION_RETRIEVED`, `ApiEnvelope<Operation>`, errors 401/403/404/500. Inventory yêu cầu chỉ gọi khi producer cấp ID và dừng theo approved terminal state.
- **Current evidence:** Không có Study #18 route/module/query/test/operations store. API row khai báo `int64`, AC/reusable `Operation.id` khai báo UUID; AD-20 #93 local response có derived `meta.operation_id:UUID`, không tạo generic Operation row. Owner scope/status lifecycle và producer bridge chưa chốt.
- **Kết quả:** Không navigate, không poll/timer/SSE. SH-07 vẫn blocked; #96 notification status không thay API #18.

### `EV-08` — Footer policy/support links

- **Element / loại:** #45–#47 anchors; `Click`.
- **Input / current processing:** Ba anchor đều `href="#"`; không có URLs, router, dialog hay API.
- **Kết quả:** Không mở destination. Không suy ra policy/RBAC/support screens từ text label.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
