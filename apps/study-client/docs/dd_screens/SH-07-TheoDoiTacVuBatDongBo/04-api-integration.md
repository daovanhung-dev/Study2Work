# SH-07 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `SH-07-API-001` | #18 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #18
- Orchestration/data notes: Chỉ GET #18 nếu đã có operation_id do BE xác nhận; không tự sinh ID, stop theo terminal state.
- BE/source status và gate: **D**; **BLOCK:** Operation status enum/ID mapping còn mâu thuẫn
- Contract sources and discrepancies are preserved in the source excerpts below.

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
4. Khi API #18 route/module/response được triển khai và contract đã chốt, client gửi một GET ban đầu. Không gửi query/body; không gọi API #18 hiện tại vì route chưa tồn tại.
5. Client kiểm tra HTTP status, business code, envelope, field types và Operation status/kind theo canonical schema. Hiện các enum/result/ownership field mapping còn SOURCE_REQUIRED.
6. Chỉ khi mapping status được phê duyệt mới render status thật, timestamp và hành động được phép. Không dựng %, countdown, kết quả thanh toán, sent count hoặc download URL nếu API không trả field được contract định nghĩa.
7. Polling/SSE, cache, retry/backoff, interval, visibility/reconnect và điểm dừng phải được quyết định trước. HTML gợi ý hai cách nhưng không tạo contract.
8. Sau terminal state, cập nhật màn hình theo chính payload backend và điều hướng theo caller context đã được duyệt. Hiện `terminal states` và safe-return target chưa được thống nhất.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md)
