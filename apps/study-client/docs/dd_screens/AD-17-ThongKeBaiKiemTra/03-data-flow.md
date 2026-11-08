# AD-17 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### Luồng dự kiến sau khi contract và frontend được wire

1. Từ AD-15, Admin chọn thao tác xem thống kê cho Quiz. Chỉ định danh Quiz nào được truyền sang route client vẫn cần đối chiếu ID thực tế; API #91 nhận `quiz_id:int64!`.
2. Client kiểm tra trạng thái phiên và quyền màn hình theo policy được duyệt. AC-35 nêu quiz-management permission; API local chỉ có shared `ADMIN`. Không được xem route-level/Admin shell copy là authorization.
3. Client lấy path `quizId`, chuẩn hóa theo contract numeric `int64`, sau đó gọi GET #91 với Bearer token. Direct catalog không khai báo body/query. Hiện không có router hoặc API caller trong Study Web.
4. Backend current source xác thực shared `ADMIN`, parse ID, query aggregate read-only trên legacy Quiz/QuizAttempt candidate. API DD đánh dấu metric/formula là DERIVED. Live schema và policy chưa được xác minh.
5. Với HTTP 200, direct response contract là `ApiEnvelope<Quiz>` nên client không có analytics fields được bảo đảm để ánh xạ. Không được tự tính analytics trên Quiz hoặc dùng local DTO như thể đã được duyệt. Chỉ sau khi response contract được owner chốt mới định nghĩa loading→no-data/ready và mapping.
6. Với 401/403/404/500, hiển thị trạng thái phù hợp theo business code; phần UI/auth-expiry/ retry hiện chưa có implementation hoặc approved interaction. Local source dùng 404 cả cho path malformed và Quiz vắng mặt.
7. Người dùng có thể quay lại AD-15 qua breadcrumb hoặc một trong hai link quay lại; cả ba anchor hiện trỏ tới `/admin/quizzes`. Param cần giữ lại hoặc không phải là quyết định route chưa được đặc tả.
8. Không có bằng chứng AD-17 được cập nhật push sau submit. AC-35 hiện mô tả GET aggregate; câu trong HTML nói tác vụ nền sau submit là static mockup copy.

### Current prototype flow

1. Tải HTML tĩnh, không đọc URL hoặc authentication.
2. Tên Quiz/ID/trạng thái đồng bộ đều là placeholder; không có fetch/XHR.
3. Empty state và hai note card luôn hiển thị như ảnh nguồn.
4. Link quay lại trỏ `/admin/quizzes`; không có client router xác nhận đích.
5. Click “Kiểm tra kết nối dữ liệu” disable nút, bật spinner và đổi label; sau 700 ms hiển thị feedback cố định nói API hoạt động và “Trống Analytics”; sau 3 giây đổi label về cũ và enable nút. Không có request mạng. `syncFeedback` được ẩn ban đầu; HTML không đặt lại nó ở lượt click sau.
6. Shell navigation, notification, footer links dùng `href="#"` hoặc không có handler; không gắn route AD-17.

### Luồng dữ liệu / API

```text
AD-15 (Quiz ID cần xác minh)
  → candidate route /admin/quizzes/:quizId/statistics
  → GET #91 (Bearer JWT, path quiz_id:int64!, không body/query)
  → DIRECT catalog: ApiEnvelope<Quiz> ── không có metric fields
  → LOCAL source: derived AdminQuizStatistics ── chưa được contract duyệt
  → UI no-data/ready mapping: BLOCKED đến khi thống nhất schema và metrics
```

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

### Trạng thái

| State | Điều kiện vào | UI/output | Trạng thái bằng chứng |
|---|---|---|---|
| `unwired-prototype` | Current checked-in HTML loaded | Placeholder Quiz, empty state và CTA tĩnh | Current source |
| `loading` | Future valid route, auth và request #91 | Loading indicator; chưa có thiết kế/loading source cụ thể | Expected candidate; chưa implement |
| `no-data` | Approved response xác nhận zero attempts/metrics absent | Empty view với meaning phân biệt zero, unknown và unavailable | Blocked; semantics chưa có contract |
| `ready` | Approved response có metric fields | Render các metric đã được chốt; không thêm distribution/time/completion nếu response không trả | Blocked; direct `ApiEnvelope<Quiz>` không có metrics |
| `unauthorized` | 401 `DESIGN_AUTHENTICATION_REQUIRED` | Áp dụng auth/session flow chung | API code direct; UI flow chưa xác định |
| `forbidden` | 403 `DESIGN_ACCESS_DENIED` | Access denied; không render stats | API code direct; fine-grained permission chưa chốt |
| `not-found` | 404 `DESIGN_RESOURCE_NOT_FOUND` | Quiz/path unavailable theo message policy | API code direct; local malformed ID cũng map 404 |
| `service-error` | 500 `DESIGN_INTERNAL_ERROR` | Lỗi dịch vụ an toàn, trace ID nếu envelope/header cho phép | API code direct; local handler rollback; UI chưa có |
| `network-error` | Offline/timeout | Không có trạng thái HTTP/business code tương ứng | Cần thống nhất client networking convention |
| `connection-checking` | Click #27 | Spinner/disabled, label “Đang kiểm tra…” | Prototype timer 700 ms, không request |
| `connection-feedback` | Timer hết | Static “API hoạt động/Trống Analytics”; sau 3 s label reset | Prototype-only, không phải kết quả connectivity |

### Điều hướng / dữ liệu truyền

| Từ | Hành động | Đích / dữ liệu | Ghi chú |
|---|---|---|---|
| AD-15 | Chọn statistics cho Quiz | Candidate `/admin/quizzes/:quizId/statistics`; `quizId` cần map sang API `quiz_id:int64` | Inventory/AC-35 handoff; client route/row action chưa có source. |
| AD-17 | Click breadcrumb, top return hoặc primary CTA | `/admin/quizzes` → AD-15 candidate | HTML target verified; router runtime chưa có. Query/filter/page state preservation chưa xác định. |
| AD-17 | Click shell/footer placeholders | `#` hoặc no handler | Không có screen transition xác nhận. |

Không có quyền xác nhận để truyền dữ liệu thống kê từ client sang AD-15; ID route cần được xác nhận từ AD-15 response/selection source. API #91 là GET read-only; không invalidate/write cache từ prototype. Cache duration, retry, polling, auto-refresh và back-stack policy chưa có contract.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #91; direct catalog `ApiEnvelope<Quiz>` không có metric fields; local source trả derived `AdminQuizStatistics` (counts/average/pass metrics). Contract/schema mismatch chặn mapping; local DTO chưa được duyệt.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [AD-17](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/AD-17.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
