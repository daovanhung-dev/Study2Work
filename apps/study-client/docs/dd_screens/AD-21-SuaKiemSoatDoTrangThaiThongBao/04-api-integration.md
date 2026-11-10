# AD-21 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-21-API-001` | #18 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-21-API-002` | #94 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-21-API-003` | #95 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-21-API-004` | #96 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #18, #94, #95, #96
- Orchestration/data notes: #96 là GET status, không có GET detail riêng và không trả delivery counts/per-channel status; #94 catalog path-only nhưng local body `{title,content}`/QUEUED-only là DERIVED; #95 catalog DELETE trả `deleted`, local source hard-delete row và không dừng provider; chỉ gọi #18 sau khi Operation ID/type/owner/producer mapping được duyệt.
- BE/source status và gate: **R** local #94/#95/#96 routes/modules/query/validator/model/test source; API DDs Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** notification detail/projection, status/lifecycle mapping, AC-36 permission vs `ADMIN`, #94 body/edit gate, #95 cancel/delete/retention/worker coordination, delivery metrics/channel mapping, candidate legacy/live schema, #18 UUID/int64/owner/store, Study Web UNWIRED; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API contract summary

| API | Direct catalog contract | Current Study source | AD-21 implication |
|---|---|---|---|
| #96 status | `GET /api/v1/admin/notifications/{notification_id}/status`; Bearer JWT, role Admin; path int64; no body/query; `ApiEnvelope<Notification>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401/403/404/500. | Registered local route, `ADMIN` guard, positive int64; invalid/missing/no-delivery → 404; aggregate read-only Notification projection. #96 does not provide delivery counts/per-channel state. | Candidate read source only; not separate detail endpoint and not enough for all mockup fields. API DD remains Draft; live schema/runtime unverified. |
| #94 update | `PUT /api/v1/admin/notifications/{notification_id}`; Bearer JWT/Admin; path int64; catalog body not specified; `ApiEnvelope<Notification>`; 200 `DESIGN_RESOURCE_UPDATED`; 401/403/404/422/500. | Registered local route; derived strict `{title,content}`, parent/delivery locks, only nonempty all-QUEUED rows editable; updates title/content; commit on valid response. | Do not treat local body/state policy as approved draft or scheduled editing. |
| #95 delete | `DELETE /api/v1/admin/notifications/{notification_id}`; Bearer JWT/Admin; path int64; no body/query; `ApiEnvelope<DeleteResult>`; 200 `DESIGN_RESOURCE_DELETED`; 401/403/404/422/500. | Registered local route; derived queued-only hard delete of selected legacy row with candidate cascade; returns `status:"deleted"`; no provider cancellation. | UI text “Hủy bỏ phát hành” cannot imply cancellation success. Policy and external dispatch race remain blockers. |
| #18 operation | `GET /api/v1/operations/{operation_id}`; Bearer JWT; row says owner; row path int64; `ApiEnvelope<Operation>`; 200 `DESIGN_OPERATION_RETRIEVED`; 401/403/404/500. | UNWIRED / no Study route, query, store, test. AC/reusable schema use UUID; producer #93 metadata UUID. | Keep SH-07 disabled until ID type, owner, status, producer mapping and runtime are resolved. |

The checked-in DDL has legacy BIGINT `notifications` and delivery rows constrained to `PUSH|EMAIL` / `QUEUED|SENT|FAILED`; the macro-review labels this a local candidate/fallback only. It is not live schema evidence. #94/#95/#96 route/test source exists, but no application tests or runtime were executed in this AD-21 task. Fake-DB tests do not establish deployed behavior.

### Trích từ DD nguồn: B.1. Expected flow — chỉ khi contract và frontend được duyệt

1. AD-19 điều hướng tới candidate route và truyền `notificationId` lấy từ dữ liệu đã xác thực. Không tạo ID ở client. Hiện inventory chưa chốt cách serialize/filter ID; API #94–#96 catalog khai báo int64.
2. Router kiểm tra phiên và quyền theo shared Study policy. Backend phải áp dụng quyền; AC-36 notification-management permission và local shared role `ADMIN` chưa được chứng minh tương đương.
3. Nếu ID hợp lệ và API #96 được chọn làm read source, gửi một `GET /api/v1/admin/notifications/{notification_id}/status` với Bearer JWT, không query/body. Kiểm tra HTTP status, envelope (`success`, `businessCode`, `data`, `traceId`), rồi validate Notification fields trước khi render.
4. #96 có thể cung cấp `id`, `title`, `content`, `channels`, `status`, `created_at` trong current local projection. API không trả recipient, per-channel status, delivery count/progress, schedule hay Operation. Không thể dùng response này để lấp tất cả mockup fields.
5. Chỉ expose edit/delete controls sau khi policy và API contract được duyệt. #94 direct catalog chưa khai báo body; local handler lại yêu cầu `{title, content}` và chỉ sửa các delivery còn `QUEUED`. #95 direct contract là delete result; AC-36 cho phép delete/mark cancelled theo policy, còn local handler hard-delete row và không dừng provider.
6. Chỉ mở SH-07 khi một producer trả Operation ID mà type/field/owner contract tương thích API #18. Hiện AD-20 #93 local `meta.operation_id` là UUID, trong khi API #18 row khai báo int64; reusable schema/AC lại nói UUID và Study #18 chưa wired.
7. Theo từng HTTP/business error đã được contract công bố, render lỗi đã duyệt và không biến 500/network thành not-found. Không có retry, timeout, cache, polling cadence hay refresh policy được xác định trong các API này.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/AD-21.md)
