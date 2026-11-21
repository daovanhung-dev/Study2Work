# ME-14 — Data Flow & State

> **Current source (2026-11-21):** ME-13 router state → validated, one-use selected recipients → text/channel POST #63 → validated accepted UUID → SH-07/#18. #63 does not accept `course_id`; ambiguous submit outcomes block blind resubmission because no idempotency key exists. Provider/browser runtime is unverified. The source DD details below preserve earlier design notes.

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Earlier DD snapshot — 2026-11-08

Các luồng/code excerpts trong phần này mô tả prototype và quyết định lúc tạo DD; current Study Client behavior được ghi ở cuối tài liệu.

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### Luồng hiện tại của artifact

1. Mở `code.html` tĩnh. Không có router/auth guard hoặc gọi dữ liệu.
2. DOM khởi tạo với title/body trống, In-app checked, Email disabled, selection chưa xác thực, send disabled và preview placeholder.
3. Khi title đổi, script hiển thị raw character count `value.length`; preview dùng `trim()` để chọn placeholder hoặc nội dung. Preview được gán bằng `textContent`.
4. Khi body đổi, script đếm các từ sau `trim().split(/\s+/)`; preview được cập nhật bằng `textContent`. Không có markdown/rich text parsing.
5. Toolbar, kênh, đính kèm, lưu nháp, gửi, breadcrumb, navigation, help và footer không có handler/router/API. Anchor dùng `href="#"`; `data-path` là nhãn tĩnh.
6. Không có state persistence. Refresh sẽ trở về giá trị ban đầu của HTML.

### Luồng dự kiến theo AC-25 và giới hạn nguồn hiện tại

1. ME-13 chọn course và Student từ roster #62. ME-13 handoff IDs/course sang ME-14 đang mở; phải thống nhất carrier, ID type và course binding trước khi code.
2. ME-14 nhận title, content, recipients và channels; hiện HTML không có state nhận từ ME-13, validation audience hoặc quy tắc sản phẩm đã được nối.
3. Khi có contract đã duyệt, client cần tạo request #63 theo schema chính xác. Hiện chưa thể ánh xạ `body text → content:int64`, `In-app → PUSH`, hoặc attachment vì source không định nghĩa mapping.
4. #63 strict-validates request model; malformed/missing/type/extra-field input có thể bị framework trả 422 trước khi handler chạy. Với body parse thành công, Mentor auth chạy trước CSV parsing/DB. Sau đó source kiểm tra recipient scope, thực hiện transaction và chỉ trả 202 sau khi tất cả notification/outbox rows commit.
5. Response #63 có một Operation UUID trong `data.id`, cùng các notification int64 IDs trong `meta.notification_ids`. Đây là hai định danh khác mục đích.
6. API #64 đọc status cho từng notification ID. Source tổng hợp `QUEUED` nếu còn delivery queued; nếu không và có failed thì `FAILED`; nếu tất cả sent thì `SENT`. Đây là mapping local `DERIVED`; worker/provider chưa wired nên không đảm bảo chuyển khỏi `QUEUED`.
7. API #18 không có Study route và AC-25 không kết nối endpoint này vào luồng. Không gọi #18 theo `operation_id` ở ME-14.

### Trạng thái giao diện và lỗi

| Trạng thái | Hiện có trong prototype | Hành vi/ghi chú |
|---|---|---|
| Initial/empty | Có | Selection/title/body rỗng; preview dùng placeholder. |
| Recipient blocked | Có | Badge chưa xác thực; Send disabled. |
| Editing title/body | Có | DOM preview/counter được cập nhật. |
| Channel selected/disabled | Có | In-app checked; Email disabled. Không có onChange handler. |
| Uploading/saving/sending/loading | Không | Không có async handler hoặc spinner. |
| Validation error | Không | Dấu `*` là copy; input không có `required`, form hoặc validator. |
| API success/error | Không | Không có fetch/client error mapping. HTTP/API outcomes chỉ mô tả ở E09 để phục vụ tích hợp sau khi blockers được giải quyết. |
| Session expired/unauthorized | Không | Chưa có auth/runtime; nếu tích hợp #63, 401 theo API contract cần xử lý ở app shell. |

### Trích từ DD nguồn: E. Điều hướng và state giữa màn hình

| Handoff | Dữ liệu cần giữ | Current evidence | Quyết định cần có |
|---|---|---|---|
| ME-13 → ME-14 | Course identity và danh sách unique Student int64 IDs; có thể có draft text khi quay lại. | ME-13 DD giữ nguyên ID nhưng carrier/course binding chưa chốt. ME-14 HTML không nhận state. | Phê duyệt carrier nội bộ, duplicate handling, expiry và behavior khi refresh; không đặt IDs trên URL nếu chưa quyết định. |
| ME-14 → accepted send | Title, content, recipients, channels; attachment nếu hỗ trợ. | #63 chỉ khớp title/recipients/channels một phần; body `int64` và không có attachment. | Chốt contract/API before enabling send. |
| Accepted → SH-07 | #63 Operation UUID; notification int64 IDs remain separate for #64. | Current ME-14 routes the accepted UUID to SH-07; SH-07 uses notification-only owner-bound #18. | Queue acceptance is not provider delivery; browser/runtime remains unverified. |

### Ma trận state

| State | Nguồn | Đặc tả |
|---|---|---|
| `draft` | `list_screen.md` expected state | Không được lưu/khôi phục trong source hiện tại. |
| `validating` | `list_screen.md` expected state | Không có validator/loading state trong HTML. |
| `sending` | `list_screen.md` expected state | Không có submit handler; nút send disabled. |
| `accepted` | `list_screen.md` và API #63 | Theo local API source, chỉ sau transaction commit; 202 nghĩa queued, không phải delivered. |
| `error` | `list_screen.md`; #63 error set | UI error panel/toast/retry state chưa được source định nghĩa. Backend status/code được giữ nguyên ở E09. |
| `QUEUED`/`SENT`/`FAILED` | #64 local projection | Trạng thái dispatch API theo từng notification; mapping từ delivery counts là `DERIVED`, worker chưa wired. |

## 4. Luồng đọc (Read)
- Current orchestration: ME-13 passes the selected course and unique Student IDs by router state; ME-14 consumes the handoff and posts text/channels through #63. A valid accepted Operation UUID routes to SH-07/#18. #63 has no `course_id`/idempotency key; #64 remains status per notification ID and is not selected by the current producer flow. Generic operation kinds and AC-25 batch status are not implemented.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ME-14](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## Current Study Client source (2026-11-21)

- ME14 reads the ME13 handoff from Angular router state, removes `courseId` and `recipients` from the current history entry, and validates positive safe-ID course/Student values, unique recipients and string display names. Missing/invalid state is gated with a link back to ME13. The selected values remain only in component memory.
- Title and body are editable in local signal state; preview, title character count and body word count update from that local state. Editing is local only; no draft persistence or #63 request occurs until explicit submit.
- Current source submits trimmed text content and explicit `PUSH`/`EMAIL` values through #63, accepts only a validated HTTP 202 response, and routes the accepted UUID to SH-07. Accepted state locks the form. Ambiguous network or malformed-success outcomes block blind resend for the current page because the API has no idempotency key; a confirmed HTTP failure is shown separately.
- API #63 has no `course_id`, so it cannot bind the recipients to the exact ME-13 course. Focused Mentor tests pass; browser/live API/DB/provider runtime is unverified. Draft persistence is not implemented.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
