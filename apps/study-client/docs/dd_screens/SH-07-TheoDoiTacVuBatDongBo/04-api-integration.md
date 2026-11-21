# SH-07 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `SH-07-API-001` | #18 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

### Current approved notification-only integration (2026-11-21)

- API #18 is `GET /api/v1/operations/{operation_id}` with a UUID path. It permits Student, Mentor and Admin sessions; query ownership is bound to the authenticated caller. Missing and non-owner operations return 404; invalid role/auth and internal errors retain their source error behavior.
- SH-07 validates the UUID before calling #18, accepts only `NOTIFICATION_DISPATCH` with `QUEUED`, `FAILED` or `SENT`, and renders validated timestamps. It fetches on route entry and only on explicit manual refresh; there is no polling.
- ME-14/#63 submits explicit selected recipients and text `content`; AD-20 obtains explicit Admin recipient choices through #68 and submits them to #93. Both producer responses return an Operation UUID used for SH-07 navigation.
- API #18's general payment/export/result contract remains broader than this screen and stays Draft. API #63/#93 acceptance does not prove provider delivery. Focused UI/API tests pass; live DB/deployment/browser are unverified.

- API refs trong inventory: #18
- Orchestration/data notes: Chỉ GET #18 nếu đã có operation_id do BE xác nhận; không tự sinh ID, stop theo terminal state.
- BE/source status và gate: **D**; **BLOCK:** Operation status enum/ID mapping còn mâu thuẫn
- Current Study Web source (2026-11-21): `API_018` is `WIRED`; SH-07 calls it with an owner-scoped notification Operation UUID from #63 or #93. It displays only the source-backed notification fields/statuses and never presents a payment/export result.
- Contract sources and discrepancies are preserved in the source excerpts below.

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
| Caching/retry | Chưa có rule. GET không làm mutation; không tự thêm retry/idempotency/cache. | Client performs entry/manual GET only; no polling, cache or automatic retry is wired. |
| Polling | Inventory yêu cầu dừng theo terminal; cadence/retry/terminal enum chưa có. | Không poll. 3000ms/backoff và `/operations/{id}/stream` là HTML prototype only. |
| Persistence | Study `Operation` là logical schema. | `DB.sql` không có generic `operations` table. Current query derives notification operations from `notifications` and `notification_deliveries`; migration 009 adds notification `operation_id UUID`. Work Server `operations` table is not used. Live DB chưa xác minh. |

`API #18` DD hiện ở trạng thái Draft/Needs Confirmation. Các câu hỏi Q-18-01…Q-18-05 (ID, owner, storage/enums/lifecycle, per-kind result/producers, 403/404) phải được quyết định ở nguồn contract trước khi SH-07 chuyển sang DD READY.

### Trích từ DD nguồn: Discrepancy và mapping producer

| Nguồn | Current evidence | Ý nghĩa với SH-07 |
|---|---|---|
| API #18 | Catalog row `int64`; global ID convention, reusable `Operation.id` và AC-12/25/36/38 dùng UUID. API #18 DD Draft giữ cả hai. | Không thể chốt parse/validation của route ID hoặc đảm bảo ID từ producer gọi được endpoint. Không ép UUID sang int64 hoặc ngược lại. |
| Payment API #17 | Catalog nói POST trả 202 `ApiEnvelope<Operation>`; hiện không có route/module/test payment #17. | Không có producer runtime chứng minh ID/result cho nhánh ST-06. |
| Mentor notification #63 | Current source sinh UUID, ghi UUID đó vào notification rows, trả 202 `DESIGN_OPERATION_ACCEPTED` với `data:OperationResponse` (`NOTIFICATION_DISPATCH`, `QUEUED`) và `meta.notification_ids`; test source assert UUID. | Đây là source-backed producer shape cho notification Mentor, nhưng không chứng minh generic API #18 tồn tại. |
| Mentor status #64 | Current GET dùng path `notification_id:int64`, kiểm tra MENTOR sender, đọc delivery outbox và trả Operation-like data với UUID ID; local states `QUEUED`, `FAILED`, `SENT`. | #64 không dùng operation UUID làm path và không cung cấp enum tổng quát (`RUNNING/SUCCEEDED/EXPIRED`). Không thay #18 bằng #64. |
| Admin notification #93 | Catalog row khai báo `ApiEnvelope<Notification>`; current source/test trả HTTP 202, `data:Notification`, `meta.operation_id:UUID` và `notification_ids`. Operation-tracking summary lại nói producer trả `data:Operation`. | `data` và `meta` không thống nhất giữa summary với row/source. Chưa thể dùng một response adapter cho tất cả producer. |
| Admin status #96 | Current status route dùng `notification_id:int64` và trả notification/delivery state, không nhận operation UUID. | Không phải API #18. API #96 phù hợp status notification-specific theo ID riêng. |
| Report export #103 | Catalog row khai báo `ApiEnvelope<Report>` HTTP 202; operation-tracking summary nói `Operation`; route/module/test hiện không có. `Operation.result` chỉ chỉ ra `Payment`. | Result/export artifact mapping và download URL chưa có nguồn chuẩn. Không thêm nút tải hoặc `result_url` behavior. |

### Trích từ DD nguồn: 4.2. Luồng mục tiêu chỉ sau khi contract được duyệt

1. Caller (ST-06/ME-14/AD-20/AD-25 theo contract tương ứng) nhận một ID từ backend. Client chỉ điều hướng tới SH-07 sau khi ID field/path và producer response được thống nhất; không tự tạo ID và không suy từ notification ID sang operation ID.
2. Router xác thực format theo kiểu ID đã được contract owner chốt. Hiện không có quyết định giữa UUID và int64; do đó chưa thể viết validator/canonicalizer.
3. Backend phải thực thi Bearer authentication, role/ownership policy và lookup operation. SH-07 không tự xác thực quyền bằng `owner_id` trên client.
4. The notification-only client/API mapping is now implemented: one GET on route entry and explicit manual refresh, with no query/body or polling. Generic ID/kind/result/producer contract questions remain open outside this screen slice.
5. Client kiểm tra HTTP status, business code, envelope, field types và Operation status/kind theo canonical schema. Hiện các enum/result/ownership field mapping còn SOURCE_REQUIRED.
6. Chỉ khi mapping status được phê duyệt mới render status thật, timestamp và hành động được phép. Không dựng %, countdown, kết quả thanh toán, sent count hoặc download URL nếu API không trả field được contract định nghĩa.
7. Polling/SSE, cache, retry/backoff, interval, visibility/reconnect và điểm dừng phải được quyết định trước. HTML gợi ý hai cách nhưng không tạo contract.
8. Sau terminal state, cập nhật màn hình theo chính payload backend và điều hướng theo caller context đã được duyệt. Hiện `terminal states` và safe-return target chưa được thống nhất.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md)
