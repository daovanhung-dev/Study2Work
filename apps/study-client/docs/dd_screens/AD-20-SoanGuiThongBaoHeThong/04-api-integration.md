# AD-20 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-20-API-001` | #93 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #93
- Orchestration/data notes: POST #93; chỉ sang SH-07 nếu operation response field/type và #18 mapping được duyệt. Catalog/AC-36 trả Notification; tracking prose nói Operation; local source trả Notification đầu tiên và derived `meta.operation_id:UUID`.
- BE/source status và gate: **R** local #93 route/module/model/validator/query/view/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** response Notification vs Operation; #18 int64 vs UUID/no Study handler/store; local source requires explicit recipients but UI only supplies unresolved segments; app→PUSH/channel, audience predicate/eligibility/grain, permission vs ADMIN, draft/send/priority, legacy live schema and provider delivery unresolved; Study Web UNWIRED; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API #93 và discrepancy

| Nguồn | Hợp đồng/hành vi | Trạng thái |
|---|---|---|
| API catalog #93 và AC-36 n5 | `POST /api/v1/admin/notifications`; Bearer JWT/Admin; body có recipients? hoặc segment?, title/content/channels; HTTP 202 với `ApiEnvelope<Notification>`. | Expected direct contract; API DD vẫn Draft. |
| Phần operation tracking tổng quát trong `list_api.md` | Nói POST #93 trả `data: Operation` ở 202 và client poll #18. | `DISCREPANCY` với row #93 và AC-36 n5. |
| Current local #93 source | Trả `data` là Notification đầu tiên, thêm `meta.operation_id: UUID` và `meta.notification_ids`; `businessCode=DESIGN_OPERATION_ACCEPTED`. UUID metadata là derived fallback, không tạo Operation row. | `CURRENT_SOURCE`; chưa được owner duyệt làm contract. |
| API #18 / SH-07 | API #18 row khai báo path `operation_id:int64`; reusable `Operation.id`, AC diagrams, #93 UUID metadata và SH-07 dùng UUID. Không tìm thấy Study #18 route/query/store. | `DISCREPANCY / BLOCKER`; không thể poll hoặc xác nhận route param. |

### Trích từ DD nguồn: Local #93 fallback (không thay thế contract)

- Route dùng shared `ADMIN` guard trước body parse/database; AC-36 yêu cầu notification-management permission. Hai điều kiện này chưa được xác nhận tương đương.
- Validator yêu cầu `recipients` tường minh, không null/rỗng, ID là int64 dương và không trùng; nếu key `segment` xuất hiện thì trả 422. User IDs được tra trong bảng `users`, không lọc role, trạng thái, khóa học hay tenant.
- `title`/`content` phải là string và không chỉ chứa whitespace; title tối đa 200 ký tự theo local candidate; text hợp lệ được giữ nguyên. `channels` phải không rỗng, không trùng, exact token `PUSH` hoặc `EMAIL`.
- View ghi một legacy notification cho mỗi recipient và một delivery row `QUEUED` cho mỗi notification/channel; dùng một UUID chung và trả tất cả notification IDs trong metadata. Legacy BIGINT DDL/migration là checked-in candidate, không xác nhận live schema hoặc mô hình campaign được duyệt.
- HTTP 202 chỉ trả sau commit của notification/outbox batch. View không tạo Operation record, không gọi provider và không dispatch worker; không chứng minh đã gửi.
- Errors hiện tại: 401 authentication required, 403 access denied, 422 validation/unknown recipient, 503 DB operational/unavailable condition, 500 lỗi persistence/projection/commit khác. Insert/commit failure cố rollback. Không có retry/idempotency rule riêng trong request #93.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/AD-20.md)
