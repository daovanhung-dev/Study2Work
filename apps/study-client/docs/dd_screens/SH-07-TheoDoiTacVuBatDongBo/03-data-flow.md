# SH-07 — Data Flow & State

> **Current source (2026-11-21):** SH-07 reads an accepted UUID through API #18 on route entry and manual refresh only. The handler queries notification/outbox rows for the authenticated owner; no generic `operations` table, payment/export result or polling loop is used. See [API Integration](04-api-integration.md) for exact mapping.

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

> The design excerpt below predates the approved notification-only SH-07 implementation. Current source behavior is summarized at the top of this file and in [API Integration](04-api-integration.md).

### Trích từ DD nguồn: 4. Luồng hoạt động tổng thể

### 4.1. Trạng thái prototype hiện có

1. Browser render HTML prototype, không có router hay API client được xác minh.
2. Inline script đọc `window.location.pathname`; nếu match `/operations/<segment>` thì thay text ID bằng segment đó. Nếu không match, script gán UUID mẫu. Không có validation/auth/owner check.
3. UI hiển thị gate banner, mock environment, ID mẫu hoặc path text, các lifecycle reference cards và developer diagnostic. Không có status fetch, polling, timer, SSE, result download, cache hoặc error mapping.
4. Click “Xem Contract Spec” bật modal; click hai close controls đóng modal. Copy button gọi Clipboard API với text đang hiển thị. Các anchor route đều `href="#"`.

### 4.2. Luồng mục tiêu chỉ sau khi contract được duyệt

1. Caller (ST-06/ME-14/AD-20/AD-25 theo contract tương ứng) nhận một ID từ backend. Client chỉ điều hướng tới SH-07 sau khi ID field/path và producer response được thống nhất; không tự tạo ID và không suy từ notification ID sang operation ID.
2. Router xác thực format theo kiểu ID đã được contract owner chốt. Hiện không có quyết định giữa UUID và int64; do đó chưa thể viết validator/canonicalizer.
3. Backend phải thực thi Bearer authentication, role/ownership policy và lookup operation. SH-07 không tự xác thực quyền bằng `owner_id` trên client.
4. Current source sends one GET to API #18 on route entry and on explicit manual refresh; it sends no query/body and has no polling loop. The current notification-only UUID/owner mapping is implemented; generic per-kind contract questions remain open.
5. Client kiểm tra HTTP status, business code, envelope, field types và Operation status/kind theo canonical schema. Hiện các enum/result/ownership field mapping còn SOURCE_REQUIRED.
6. Chỉ khi mapping status được phê duyệt mới render status thật, timestamp và hành động được phép. Không dựng %, countdown, kết quả thanh toán, sent count hoặc download URL nếu API không trả field được contract định nghĩa.
7. Polling/SSE, cache, retry/backoff, interval, visibility/reconnect và điểm dừng phải được quyết định trước. HTML gợi ý hai cách nhưng không tạo contract.
8. Sau terminal state, cập nhật màn hình theo chính payload backend và điều hướng theo caller context đã được duyệt. Hiện `terminal states` và safe-return target chưa được thống nhất.

### Trích từ DD nguồn: 5. Đặc tả API #18 và database

| Thuộc tính | Expected design | Current source |
|---|---|---|
| Method/endpoint | `GET /api/v1/operations/{operation_id}` | Router wires API #18; OpenAPI declares UUID path. |
| Authentication | Bearer JWT | Shared guard accepts `STUDENT`, `MENTOR`, `ADMIN` per AC diagrams; the missing required role argument was fixed and tested. |
| Authorization | Catalog row: operation owner; tracking summary thêm Admin; diagrams ghi Student/Mentor/Admin owner-only. | Current query binds `operation_id` and authenticated `owner_id`; no Admin ownership bypass. Missing/non-owned rows map to 404 in current source. Contract discrepancy remains open. |
| Path | Required `operation_id`; API row int64. | AC diagrams và reusable schema UUID; type conflict mở. Invalid-path status không thể chốt. |
| Query/body | Không khai báo. | No query/body; current handler performs one owner-bound notification/outbox aggregate query. |
| Success | 200 `DESIGN_OPERATION_RETRIEVED`; `ApiEnvelope<Operation>`. | Local source returns `NOTIFICATION_DISPATCH` with `QUEUED`/`FAILED`/`SENT`; this notification-only DTO does not resolve generic per-kind response shape. #93 still returns Notification + operation metadata. |
| Response shape | `id`, `kind`, `status`, `owner_id`, `submitted_at`, `updated_at`, optional `completed_at`, optional `result?:Payment`. | Enum, physical mapping, optional field rules, result by operation kind và timestamp semantics chưa chốt. |
| Errors | 401/403/404/500 với business code ở contract. | Local tests cover 401/403/404/500. Missing/non-owned operation currently returns 404; catalog semantics and wrong-owner policy remain open. |
| Caching/retry | Chưa có rule. GET không làm mutation; không tự thêm retry/idempotency/cache. | Không có client implementation. |
| Polling | Inventory yêu cầu dừng theo terminal; cadence/retry/terminal enum chưa có. | Không poll. 3000ms/backoff và `/operations/{id}/stream` là HTML prototype only. |
| Persistence | Study `Operation` là logical schema. | `DB.sql` không có generic `operations` table. Current query derives notification operations from `notifications` and `notification_deliveries`; migration 009 adds notification `operation_id UUID`. Work Server `operations` table is not used. Live DB chưa xác minh. |

`API #18` DD hiện ở trạng thái Draft/Needs Confirmation. Các câu hỏi Q-18-01…Q-18-05 (ID, owner, storage/enums/lifecycle, per-kind result/producers, 403/404) phải được quyết định ở nguồn contract trước khi SH-07 chuyển sang DD READY.

### Trích từ DD nguồn: 8. Ma trận trạng thái và điều hướng

| State | Điều kiện | UI/data | Chuyển tiếp hoặc route |
|---|---|---|---|
| `DESIGN_GATE` | Current Angular route/page is gate-only; client descriptor `API_018` remains `UNWIRED` | Static unavailable notice; no ID/status fetch, polling, lifecycle cards or API request. | Existing header routes only; no caller-specific recovery CTA. |
| `INITIAL` | Route vào, ID chưa resolve | Không hiển thị UUID fallback. Caller provenance phải được xác định. | `DESIGN_GATE` nếu API chưa sẵn; nếu đủ contract thì `LOADING`. |
| `LOADING` | Chỉ sau khi #18 source + canonical ID/owner/status contract được duyệt | Loading state; không fake progress. | `RESPONSE_READY`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `OPERATION_NOT_FOUND`, `SERVICE_ERROR`; exact UI mapping awaits shared route policy. |
| `RESPONSE_READY` | HTTP 200 envelope hợp lệ và status/kind đã được chuẩn hóa | Bind fields chỉ theo final schema; hiện không có mapping final. | Approved lifecycle state; stop/refresh rule unresolved. |
| `QUEUED`, `RUNNING`, `SUCCEEDED`, `FAILED`, `EXPIRED` | Chỉ là nhãn trên prototype/lifecycle reference | Không coi là canonical runtime enum. Không hiển thị một trong các trạng thái dựa trên timer hoặc ví dụ. | Không thể xác định terminal state cho tới khi enum/lifecycle owner duyệt. |
| `AUTHENTICATION_REQUIRED` | API #18 dự kiến 401 | Không show operation details; expected navigation/access flow qua SH-05. | SH-05/session policy, chưa có client runtime. |
| `ACCESS_DENIED` | API #18 dự kiến 403 | Không show owner/operation data. Wrong-owner 403 vs hidden 404 chưa chốt. | SH-05/access-denied flow theo shared route policy. |
| `OPERATION_NOT_FOUND` | API #18 dự kiến 404 | Generic not-found copy, không tiết lộ operation/owner existence vượt contract. | SH-06 candidate; exact routing unresolved. |
| `SERVICE_ERROR` | API 500, network/timeout, invalid envelope/JSON | Không convert sang 404, không show raw exception/SQL. Retry policy unknown; trace ID only if approved shared policy. | Shared service-error behavior chưa có route trong Study Web. |
| `INVALID_OR_UNKNOWN_STATE` | ID, kind/status/result không parse theo approved schema | Không tự uppercase/lowercase, không suy status từ notification API. | Hold behind gate; contract owner fixes producer/consumer schema. |
| Return navigation | User dùng CTA hoặc browser back | Inventory caller set ST-07/ME-15/AD-21/AD-25; HTML links GS-01/SH-01. | Safe-return source, history behavior và target route cần Product/FE decision. |

Notification status mapping is source-tested for the notification-only slice. Browser/live API/DB/deployment are not runtime-verified; generic payment/export operation states remain outside this implementation.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: Chỉ GET #18 nếu đã có operation_id do BE xác nhận; không tự sinh ID, stop theo terminal state.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [SH-07](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
