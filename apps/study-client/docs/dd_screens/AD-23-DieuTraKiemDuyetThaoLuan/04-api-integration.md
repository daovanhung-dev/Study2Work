# AD-23 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-23-API-001` | #98 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-23-API-002` | #99 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-23-API-003` | #100 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #98, #99, #100
- Orchestration/data notes: GET #98 → PATCH #99 với action/reason hoặc DELETE #100 → refresh #97.
- BE/source status và gate: **R #98** local route/module/query/model/validator/view/test source; API DD #98 stale `UNWIRED`; #99/#100 **D** catalog/Draft only, no local route. **DD BLOCKED; IMPLEMENTATION BLOCKED:** #98 report projection, #99 action/audit, #100 soft-delete policy, dismissal branch, target grain, Admin permission mapping and Study Web remain unresolved/unwired
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Blockers requiring contract decisions

1. Specify report persistence/writer and a #98 response that includes the report context AC-37 requires; decide report grain, reason/severity/reporter/count/time fields, and live-schema/deployment evidence.
2. Reconcile API #98 DD's stale `UNWIRED / NOT_FOUND` label with registered local route/module/test source; approve catalog/direct response mapping and whether local projection satisfies the final API contract.
3. Define #99 action tokens, allowed state transitions, target scope, validation for reason, authorization, audit actor/table/fields/retention and transaction atomicity; implement and test the route before enabling controls.
4. Define the no-violation dismissal behavior and endpoint, or revise AC-37 through its owner. Do not overload #99 without a contract.
5. Define #100 eligibility, soft-delete representation/timestamp, `DeleteResult` mapping, audit preservation/linkage, child/reply/report retention and visibility, repeat/concurrency/idempotency behavior, plus its UI trigger/confirmation.
6. Resolve whether a report targets a root Discussion or a reply and which comments are visible; confirm how AD-22 hands the correct ID/context to AD-23.
7. Approve mapping between AC Admin permission and local `ADMIN`, actor identity, tenant scope, and policies for #99/#100.
8. Implement the Study Web route/client, including response/error mapping, loading states and return/refresh behavior, then verify with runtime tests.

Until those decisions are source-backed, keep moderation/delete controls locked, preserve the prototype discrepancy, and retain `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/AD-23.md)
