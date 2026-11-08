# SH-07 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

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
4. Khi API #18 route/module/response được triển khai và contract đã chốt, client gửi một GET ban đầu. Không gửi query/body; không gọi API #18 hiện tại vì route chưa tồn tại.
5. Client kiểm tra HTTP status, business code, envelope, field types và Operation status/kind theo canonical schema. Hiện các enum/result/ownership field mapping còn SOURCE_REQUIRED.
6. Chỉ khi mapping status được phê duyệt mới render status thật, timestamp và hành động được phép. Không dựng %, countdown, kết quả thanh toán, sent count hoặc download URL nếu API không trả field được contract định nghĩa.
7. Polling/SSE, cache, retry/backoff, interval, visibility/reconnect và điểm dừng phải được quyết định trước. HTML gợi ý hai cách nhưng không tạo contract.
8. Sau terminal state, cập nhật màn hình theo chính payload backend và điều hướng theo caller context đã được duyệt. Hiện `terminal states` và safe-return target chưa được thống nhất.

### Trích từ DD nguồn: 5. Đặc tả API #18 và database

| Thuộc tính | Expected design | Current source |
|---|---|---|
| Method/endpoint | `GET /api/v1/operations/{operation_id}` | Không có route API #18 trong `apps/study-server/app/api/v1.py`. |
| Authentication | Bearer JWT | Không có endpoint runtime để thực thi auth. |
| Authorization | Catalog row: operation owner; tracking summary thêm Admin; diagrams ghi Student/Mentor/Admin owner-only. | Không có generic guard/predicate. API #64 chỉ chứng minh Mentor sender scope cho notification route riêng. |
| Path | Required `operation_id`; API row int64. | AC diagrams và reusable schema UUID; type conflict mở. Invalid-path status không thể chốt. |
| Query/body | Không khai báo. | Không áp dụng khi endpoint chưa tồn tại. |
| Success | 200 `DESIGN_OPERATION_RETRIEVED`; `ApiEnvelope<Operation>`. | Không có runtime response. #63 response là Operation-like; #93 response là Notification + meta operation id. |
| Response shape | `id`, `kind`, `status`, `owner_id`, `submitted_at`, `updated_at`, optional `completed_at`, optional `result?:Payment`. | Enum, physical mapping, optional field rules, result by operation kind và timestamp semantics chưa chốt. |
| Errors | 401/403/404/500 với business code ở contract. | Không có runtime mapping #18. Wrong-owner 403 vs hidden 404 còn mở. 500/network không được đổi thành 404. |
| Caching/retry | Chưa có rule. GET không làm mutation; không tự thêm retry/idempotency/cache. | Không có client implementation. |
| Polling | Inventory yêu cầu dừng theo terminal; cadence/retry/terminal enum chưa có. | Không poll. 3000ms/backoff và `/operations/{id}/stream` là HTML prototype only. |
| Persistence | Study `Operation` là logical schema. | `DB.sql` không có `operations` table. Migration 009 thêm `notifications.operation_id UUID`/index cho outbox; Work Server `operations` table không phải Study backing store. Live DB chưa xác minh. |

`API #18` DD hiện ở trạng thái Draft/Needs Confirmation. Các câu hỏi Q-18-01…Q-18-05 (ID, owner, storage/enums/lifecycle, per-kind result/producers, 403/404) phải được quyết định ở nguồn contract trước khi SH-07 chuyển sang DD READY.

### Trích từ DD nguồn: 8. Ma trận trạng thái và điều hướng

| State | Điều kiện | UI/data | Chuyển tiếp hoặc route |
|---|---|---|---|
| `DESIGN_GATE` | Current prototype / API #18 chưa wired | Banner `Gated/Unavailable`; không status fetch/poll; lifecycle cards chỉ là reference. | Modal/clipboard CTA; recovery targets còn proposal. |
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

Không có state nào được `RUNTIME VERIFIED`. Ngay cả các state dự kiến từ API #18 cũng chưa thể chuyển thành implementation-ready mapping do contract còn mở.

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
