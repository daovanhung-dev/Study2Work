# ST-11 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-11-API-001` | #24 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-11-API-002` | #25 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-11-API-003` | #26 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-11-API-004` | #27 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #24, #25, #26, #27
- Orchestration/data notes: GET #24; GET #26 lazy; PATCH #25 khi có biến cố progress hợp lệ; GET #27 sau completed.
- BE/source status và gate: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** asset hiện là fallback, không có player/progress/resource/next controls; #24–#27 chưa có Student route/module/query/test và API DD còn Draft; ST-10/ST-11 cùng gọi #24, ST-09 thiếu lessonId; #25 position/percent/state/storage/aggregate open; #26 `ApiEnvelope<Lesson>` vs Resource payload/visibility/URL open; #27 order/tie-break/no-next open; legacy BIGINT và V1-PILOT UUID DDL khác nhau; Study Web UNWIRED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API, authorization và bảo mật

| API | Declared contract | Current source | Vai trò / open issue |
|---|---|---|---|
| #24 | GET `/api/v1/lessons/{lesson_id}`; Student Bearer; path int64; `ApiEnvelope<Lesson>`; 200/401/403/404/500. | NOT_FOUND Student route/module/query/test; DD Draft. | Lesson retrieval; direct entitlement, publish, projection/null/error/path chưa chốt; fetch ownership đè lên ST-10. |
| #25 | PATCH `/api/v1/lessons/{lesson_id}/progress`; Student Bearer; required int64 path + body `position:int32!`, `percent:int32!`, `completed:boolean!`; `ApiEnvelope<Lesson>`; 200/401/403/404/422/500. | NOT_FOUND Student route/module/query/test; DD Draft. | Progress update + AC aggregate intent; body semantics, storage, identity, update order/idempotency/throttle/retry/transaction unresolved. |
| #26 | GET `/api/v1/lessons/{lesson_id}/resources`; Student Bearer; int64 path; no query/body; `ApiEnvelope<Lesson>`; 200/401/403/404/500. | NOT_FOUND Student route/module/query/test; DD Draft. | Resource retrieval; declared payload conflicts with resource purpose/schema; URL/visibility/cardinality/access open. |
| #27 | GET `/api/v1/lessons/{lesson_id}/next`; Student Bearer; int64 path; no query/body; `ApiEnvelope<Lesson>`; 200/401/403/404/500. | NOT_FOUND Student route/module/query/test; DD Draft. | Next lesson lookup; order/tie-break/access/end-of-curriculum semantics open. |

#### Security decisions and handling

- API catalog declares Student Bearer authentication for #24–#27. The API DD open questions still require the owner to define the entitlement predicate and direct-call behavior for each endpoint; a prior client call to #22 or #24 is not evidence that a later independent request is authorized.
- Keep protected content/media out of UI until a successful #24 response under the approved access policy. Public curriculum API #09 is not a protected-content substitute; do not rely on a client route guard as a security boundary.
- Do not assume `video_url` is signed, public, stream-safe or allowed outside the authorized player; the catalog merely marks it optional URI.
- Do not assume #25 response carries progress or a safe position. Catalog response is Lesson and the position storage is unresolved.
- Do not treat absent resources, terminal next lesson, 403, 404, expired session or network error as interchangeable; mapping is open.
- Do not use either checked-in DDL artifact as live schema or combine their identifiers. Legacy `lesson_progress` has nullable user/lesson IDs and no lesson `position` or user/lesson unique key; V1-PILOT `lesson_progress_facts` is UUID/enrollment-based and also has no `position`/`percent`. Neither artifact provides `resources.visibility`.
- Do not create a token/session field, player URL, signed URL, cache key, retry protocol or telemetry event without a canonical source.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11.md)
