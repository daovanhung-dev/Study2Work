# ST-10 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Mô tả luồng hoạt động tổng thể

### Expected flow theo AC-14/15 và inventory

1. Student vào route ST-10 với lessonId được chọn từ ST-09. Route, session guard và ID handoff chưa được nối trong Study Web; ST-09 asset hiện thiếu lesson selection.
2. Yêu cầu Student Bearer JWT theo catalog. Mỗi endpoint phải tự thực thi authorization phía server; việc client gọi #22 trước không thay thế kiểm tra quyền cho một request #23 hoặc #24 độc lập.
3. Gọi GET #22 để kiểm tra quyền lesson. AC-14 nêu enrollment/prerequisite check. Theo flow inventory, nhánh success/allowed mới đi tiếp; nhánh denied không gọi #24 và không tải/phát media. Response status 403 được khai báo, nhưng predicate và reason payload chưa được chốt. Success body ApiEnvelope<Lesson> không có access field riêng.
4. Chỉ sau khi access được chấp thuận, gọi POST #23 để ghi nhận bắt đầu. AC-14 ghi UPSERT lesson_progress với trạng thái IN_PROGRESS; inventory mong chống gửi lặp. Catalog chỉ nói POST, path lesson_id và HTTP 201 ApiEnvelope<Lesson>; semantics khi row đã tồn tại, khóa idempotency, cột cập nhật và retry chưa có quyết định.
5. Sau khi #23 thành công theo contract được duyệt, gọi GET #24 để lấy nội dung. AC-15 yêu cầu quyền xem và kiểm tra publish status, nhưng chưa chốt lesson/course gate hoặc query. Chỉ render content/video khi response #24 được backend xác nhận đã được phép; không lấy media từ #09 public curriculum hoặc từ response #22/#23 theo suy đoán.
6. Nếu #24 trả success, chuyển tới ST-11 với lessonId theo route inventory. Không có client router/runtime để xác minh history, session carry-over hoặc state transfer. ST-11 dự kiến gọi #24 khi vào player, nên việc #24 bị gọi ở cả ST-10 và ST-11 cần Product/FE xác nhận để tránh tải trùng; inventory hiện mô tả cả hai bước.
7. Khi access denied, start/content lỗi, session hết hạn, lesson không tồn tại hoặc mạng lỗi, UI cần state/mapping rõ. Asset chỉ vẽ ba FSM labels tĩnh; không có loading/error/timeout/retry handler hay API call thật.

~~~mermaid
flowchart LR
  ST09[ST-09 lesson selection] -->|lessonId expected; absent in current design| ST10[ST-10 transition]
  ST10 --> AUTH[Student session check]
  AUTH --> A22[GET #22 access]
  A22 -->|denied / error| DENY[No #23, no #24, no media]
  A22 -->|allowed per approved contract| P23[POST #23 start]
  P23 -->|success| G24[GET #24 lesson]
  P23 -->|failure| FAIL[Failure state; retry policy open]
  G24 -->|authorized content success| ST11[ST-11 lesson player]
  G24 -->|403 / 404 / 500| FAIL
~~~

### Current behavior đã kiểm chứng

- PNG/HTML hiển thị gate active, static progress bar 2/5, status text 423_LOCKED, protected-player placeholder, FSM copy và API DESIGN_ONLY badges. Không có dữ liệu API hoặc auth được bind.
- HTML có header/breadcrumb/footer anchors href=#. Nút return ST-09 là anchor placeholder. Nút Start có disabled và aria-disabled=true, title chờ #22; không có click handler.
- Custom API/fetch/event handler không có trong HTML. Script chỉ cấu hình Tailwind và nạp Tailwind CDN.
- Study Web editable source/package/router vắng mặt; ignored dist chỉ có route /. Không có runtime ST-10 để xác minh.
- API search hiện tại: #22/#23/#24 không có Student route/module/query/test. Router có Admin lesson APIs #82–#86 dưới `/api/v1/admin/lessons...`, nhưng role/path khác và không thực hiện Student access/start flow.
- API #22–#24 DD và catalog là declaration. Test files riêng cho ba API không có; không chạy test suite.
- API #09 current source là public, chỉ lấy course/lesson `PUBLISHED`, sắp theo `sort_order,id` và trả `content`/`video_url`; không có JWT/enrollment context. Vì vậy response #09 không thể làm bằng chứng quyền học/media của Student.
- Hai DDL Study đều chưa xác nhận live: `infra/postgres/study-server/DB.sql` có BIGINT `lesson_progress(user_id, lesson_id, status, progress_percent, last_accessed_at, completed_at)` nhưng không khai báo unique `(user_id,lesson_id)`; V1-PILOT `infra/postgres/02_study_db.sql` có UUID `lesson_progress_facts(enrollment_id, lesson_id, status, first_started_at, completed_at)` và unique `(enrollment_id,lesson_id)`. Mô hình identity/field khác nhau; không suy ra API #23 conflict key, write mapping hoặc transaction từ một trong hai.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| State | Điều kiện vào dự kiến | Hành động/đích | Current evidence |
|---|---|---|---|
| Route missing/input unavailable | No wired ST-10 route or lessonId from ST-09 | Stop before API calls; design/client wiring needed | Current Study Web route absent; ST-09 asset lacks lesson selection |
| Checking | Route/auth context valid; #22 pending | No content/media; await access result | Static card only; no request |
| Denied | #22 returns 403 under approved semantics | Do not call #23/#24; keep content hidden; render approved reason | Copy-only denied card; reason payload unresolved |
| Access error | #22 returns 401/404/500 or network failure | No downstream calls; map status after contract; retry policy open | No error screen/handler |
| Starting | #22 allowed; #23 request pending | Prevent duplicate user action if implementation policy is approved | Current button disabled permanently; no request |
| Start failed | #23 returns error or ambiguous network result | Do not call #24 until success; safe retry/dedup needs idempotency contract | No failure UI; retry policy unresolved |
| Content loading | #23 success; #24 pending | Keep media hidden until authorized content response | No API or loading handler |
| Content error | #24 returns 401/403/404/500 or network failure | Remain gated; apply approved error mapping | No error UI or handler |
| Started/ready | #24 authorized success | Navigate to ST-11 with lessonId and approved context | FSM card is static; route absent |
| Session expired | Endpoint returns 401 | Handle per auth/session owner | No client session manager/source |
| Missing/unpublished | #22/#24 returns 404 per eventual semantics | Keep content hidden; distinguish from deny only if contract permits | 404 meaning open |

### Navigation matrix

| From | Trigger/data | To | Gap |
|---|---|---|---|
| ST-09 | Selected lessonId required | ST-10 | Current ST-09 design has no lesson item/ID handoff |
| ST-10 | Return link; intended course context | ST-09 | href=#; courseId/selection/history behavior absent |
| ST-10 | #22 allowed → #23 success → #24 success; pass lessonId | ST-11 | APIs/route absent; #24 is listed both here and in ST-11 load sequence |
| Header/footer | Static labels/data-path slugs | Inventory screens or legal pages | href=#; many destinations lack route contracts |

No current evidence defines browser back-stack behavior, course/lesson selection restoration, tab state, token refresh/redirect, or whether ST-11 reuses or refetches #24. These decisions remain open.

### UI, accessibility và design-system constraints

- Mockup uses Plus Jakarta Sans, primary #004AC6 and max width 1440px. Study UI guide targets Inter/system, ocean-primary #0B5F8A and content width around 1120px. Record as design discrepancy; do not alter the source image in this screen DD.
- Header nav is hidden below md and no mobile menu is present.
- Return anchor has focus:outline-none but no visible focus-ring utility in the markup; keyboard focus visibility needs review.
- Start control is natively disabled and aria-disabled=true, but its explanatory title/copy says permanent lock; that state has no business contract.
- Footer claims WCAG 2.1 AA Compliant without evidence of an audit. Do not treat the badge as verification.
- Screen uses contrast colors/animations but no motion preference handling is evident in static markup. Verify reduced motion, focus, keyboard navigation, screen-reader state announcement, contrast and responsive reflow when runtime exists.
- Course/student labels are hard-coded; do not use them as production data.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #22 → nếu allowed, POST #23 → GET #24 → ST-11; retry/idempotency và #23 auto-vs-click chưa chốt.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ST-10](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/ST-10.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
