# ST-06 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-06-API-001` | #17 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-06-API-002` | #18 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #17, #18
- Orchestration/data notes: POST #17 → nhận operation_id → GET #18 theo điều kiện chốt; client callback không phải bằng chứng đã paid.
- BE/source status và gate: **#17/#18 D; DD BLOCKED**; **BLOCK:** Order/provider handoff, gateway/payment verification, Operation UUID/int64 + owner policy/lifecycle/polling, retry/idempotency chưa chốt; Study Web và #17/#18 UNWIRED; prototype không có payment action, return link thiếu ID
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API boundary

| API | Request / quyền | Success | Errors | Runtime/effect boundary |
|---|---|---|---|---|
| #17 | `POST /api/v1/payments`; Bearer JWT; role Student; body `{order_id:int64!, provider:string!}` | 202 `DESIGN_OPERATION_ACCEPTED`; `ApiEnvelope<Operation>` | 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 503 `DESIGN_DEPENDENCY_UNAVAILABLE`, 500 `DESIGN_INTERNAL_ERROR` | Catalog/Draft only. DB design labels payment insert/external payment `DESIGN_ONLY`; current Study route/module/query/test absent. Physical Order link, ownership, provider, amount/currency, transaction and gateway behavior unresolved. |
| #18 | `GET /api/v1/operations/{operation_id}`; Bearer JWT; path ID is `int64!` in row; owner actor in row | 200 `DESIGN_OPERATION_RETRIEVED`; `ApiEnvelope<Operation>` | 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR` | Catalog/Draft only. UUID in shared Operation schema/AC conflicts with row int64. Owner/Admin policy, storage, lifecycle and poll rules unresolved; current route/module/query/test absent. |

No client-originated callback or gateway redirect parameter is a trusted payment confirmation source in the available contracts. API #18’s presence in catalog does not establish that #17 returns a pollable ID of the same type.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-06_thuc-hien-thanh-toan/ST-06.md)
