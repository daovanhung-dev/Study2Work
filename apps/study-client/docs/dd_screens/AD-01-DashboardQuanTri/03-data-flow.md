# AD-01 — Data Flow & State

> **Current source note (2026-11-20):** `/admin` is registered and renders AD01Page under AdminLayout. AdminSessionService accepts an Admin profile/token from #03 in tab memory. AD01 has no #101 caller; its current page shows unavailable report, audit and service states, disabled date/refresh/audit actions and source-routed shortcuts. The historical prototype-flow excerpt below predates this Angular page.

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### Expected flow — chỉ triển khai sau khi blocker được xử lý

1. Mở route `/admin` từ một shell/router Study Web đã đăng ký; kiểm tra phiên Admin theo policy đã duyệt. Handoff token/profile hiện không có Study Web source để xác định.
2. Khởi tạo trạng thái tải cho kỳ đã được owner chốt. Các nhãn “Hôm nay”, “7 ngày qua”, “30 ngày qua” chưa đủ để suy ra `from`/`to`, timezone hoặc default; không lấy proposal 30 ngày làm mặc định đã duyệt.
3. Gửi một request `GET /api/v1/admin/reports/summary` với Bearer JWT và query `from?:date`, `to?:date`, không body. Chỉ gửi khoảng ngày sau khi date semantics được xác nhận.
4. Backend theo AC-38 phải xác thực Admin/report permission, kiểm tra kỳ và tổng hợp KPI. Hiện #101 không có route, query hoặc data source; API DD chưa chốt aggregate hay report snapshot.
5. Với 200 `DESIGN_RESOURCE_RETRIEVED`, kiểm tra envelope và shape `Report.period`, `metrics[]`, `generated_at`. Mỗi `ImpactMetric.value` là decimal-string. Không thể gán vào bốn card cho đến khi `key`, label, formula, unit, population, empty/partial behavior và thứ tự được phê duyệt.
6. Sau mapping được duyệt, hiển thị dữ liệu và kỳ server trả về; giữ query state chỉ theo router/cache policy được xác nhận. Không tự tính KPI ở client.
7. Xử lý 401/403/500 theo business code; recovery/redirect, error copy, retry, timeout và cache chưa có contract. Invalid date hoặc `from > to` cũng chưa có error mapping; không tự thêm 400/422.
8. Sau summary, AC-38 tiếp tục API #102 cho community impact; nhánh export #103 là optional. Đây là downstream flow, không đồng nghĩa dashboard phải tự gọi #102/#103 hoặc API #18.

### Historical prototype HTML behavior

- Document mở trực tiếp như prototype tĩnh; không có fetch/Axios/XHR, API handler, Study Web route hay state store.
- Date controls và “Xem toàn bộ nhật ký kiểm toán” đang disabled.
- Refresh chỉ thêm class `rotate-180` cho icon, bỏ class sau 700 ms và chặn click lặp trong khoảng timer; không làm mới số liệu.
- Primary nav và footer anchors trỏ `#`; notification button không có listener. Ba quick links là native anchors tới path admin nhưng không có app router để xác nhận đích.
- Các KPI/status/audit/identity trong ảnh không lấy từ API. `--` không được hiểu là 0 hoặc response no-data.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

### Screen states

| State | Điều kiện | UI / chuyển tiếp | Trạng thái chứng cứ |
|---|---|---|---|
| `Report unavailable` | Angular route/page exists; #101 has no current server/client route. | Current page renders safe unavailable metrics and controls without issuing a request. | `SOURCE_PARTIAL / API_UNWIRED`. |
| `Loading` | Candidate khi route/API được wire và request #101 đang pending. | Cần thiết kế spinner/skeleton, timeout và disable duplicate; screenshot không có loading visual. | Inventory candidate; chưa implement/approved. |
| `Ready` | 200 Report và field/card mapping được duyệt. | Hiển thị kỳ, metrics và generated time theo UI format đã duyệt. | Chưa đạt vì KPI mapping/formula chưa chốt. |
| `Partial` | Inventory nêu state này. | API #101 không định nghĩa partial marker, metric-level status hoặc lỗi từng phần; không thể suy ra card nào hidden/failed. | `OPEN / BLOCKER`. |
| `No data` | Candidate khi report không có metrics hoặc nguồn rỗng. | `--` trong ảnh là placeholder; API chưa quyết định empty list, zero, metric omission hay unavailable. | `OPEN / BLOCKER`. |
| `Authentication required` | API #03 login is handled by enclosing AdminLayout. | Unauthenticated entry shows the Admin login form; only an in-memory `ADMIN` session exposes AD01Page. | Current source; #101 remains unwired. |
| `Access denied` | API #101 expected 403 `DESIGN_ACCESS_DENIED`. | No #101 response or report-specific authorization state exists. | Contract expected; policy/report permission unresolved. |
| `Error` | API expected trả 500 `DESIGN_INTERNAL_ERROR`; network/timeout còn chưa có contract UI. | Error copy/retry behavior chưa có thiết kế. Không báo dashboard “ready” khi lỗi. | Contract expected, handling unwired. |
| `Refreshing` | Current Angular refresh button is disabled. | No animation, request or local state change. | Source-gated pending #101/date contract. |

### Điều hướng và dữ liệu

| Từ | Đến | Dữ liệu / điều kiện | Hiện trạng |
|---|---|---|---|
| Admin session → AD-01 | `/admin` | Role `ADMIN` validated from #03; profile is held in tab memory. #101 report permission remains unimplemented. | Source route/page/layout exists; deployment unverified. |
| AD-01 → AD-02 | `/admin/users` | API #68 belongs to destination screen. | Angular `routerLink`; destination route exists. |
| AD-01 → AD-06 | `/admin/courses` | API #73 belongs to destination screen. | Angular `routerLink`; destination route exists. |
| AD-01 → AD-10 | `/admin/content/pending` | API #78 belongs to destination screen. | Angular `routerLink`; destination route exists. |
| AD-01 → AD-24 | `/admin/reports/community-impact` | Inventory liên kết; API #102 yêu cầu date/segment theo contract riêng. | Không có link tương ứng rõ trong quick cards; nav Báo cáo vẫn `href="#"`. |
| AC-38 summary → #102 | `GET /api/v1/admin/reports/community-impact` | AC-38 đặt #102 sau #101; không tự nối segment/query hoặc gộp metric. | Diagram/contract expected; API #102 chưa runtime. |
| AC-38 optional export → #103 / #18 | Endpoint #103, có thể theo dõi operation | Export là nhánh downstream; #103/#18 có discrepancy về operation/result contract. | Không khởi tạo từ AD-01 hiện tại. |

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #101 với from/to; không tự bịa KPI từ bảng nếu BE chưa trả.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [AD-01](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/AD-01.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
