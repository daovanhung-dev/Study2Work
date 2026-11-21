# GS-07 — API Integration

> **T041/current-source update (2026-11-20):** GS-07 calls #12. PUBLIC resources require a valid direct HTTP(S) URL and no auth; PRIVATE resources require a Student Bearer, a published parent course and ACTIVE enrollment, then receive a signed URL with TTL 300 seconds. Response includes `visibility`. Local source includes 401/403/404/500/503 handling; live schema/storage/runtime is not verified. The catalog/API DD still needs contract synchronization; the historical source claims below are superseded where they conflict.

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `GS-07-API-001` | #12 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #12
- Orchestration/data notes: GET #12 on entry; do not persist signed URL beyond the resource session or expose internal storage keys.
- BE/source status and gate: **#12 source-backed and called; T041 access policy approved; implementation partial; runtime unverified.** MIME-specific preview/expiry UI, resource producer/schema and live storage remain open. Prototype/design-guide fidelity and accessibility measurement remain incomplete.
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Luồng dự kiến sau khi contract được chốt

1. GS-06 hoặc ST-12 truyền `resourceId` và query return context (`courseId` hoặc `lessonId`).
2. Client accepts positive decimal IDs within signed-int64 range; it retains the exact route string for the request.
3. Client shows loading and calls `GET /api/v1/resources/{resource_id}`. It uses Student Bearer transport when a Student session exists, otherwise the public transport.
4. Server validates the resource ID, loads the resource and requires a non-deleted lesson plus published parent course when the resource has a lesson. PRIVATE resources without a parent course are hidden as 404.
5. PRIVATE requires valid Student auth and an ACTIVE enrollment for the parent course; the server signs the storage key for 300 seconds. PUBLIC returns only a valid stored HTTP(S) URL.
6. Client validates success code, exact requested ID, required fields, visibility and an HTTP(S) URL without credentials; it renders metadata and opens the original URL in a new tab using `noopener noreferrer`. MIME-specific preview, expiry UI and automatic retry are not implemented.
7. Return link uses `courseId` to go back to GS-06 resources, or `lessonId` to return to ST-12. Without either, it links to `/courses`.

### Trích từ DD nguồn: API #12 request/response và error mapping

| Chủ đề | Declared contract / expected | Current source evidence |
|---|---|---|
| Method/path | `GET /api/v1/resources/{resource_id}`; signed-int64 path; no query/body. | Route composed in `app/api/v1.py`, receives raw path string and validates to signed-int64. Authorization is optional at route level and required only for PRIVATE resources. |
| Success | `ApiEnvelope<Resource>`; local response `id/name/type/url/visibility/lesson_id`; 200 `DESIGN_RESOURCE_RETRIEVED`. | PUBLIC uses direct stored HTTP(S) URL; PRIVATE uses 300-second signed URL. |
| Not found | Declared 404 `DESIGN_RESOURCE_NOT_FOUND`. | Invalid/out-of-range ID, missing resource, missing/deleted lesson, unpublished parent, PRIVATE without a parent, or missing storage key return 404. |
| Internal failure | Declared 500 `DESIGN_INTERNAL_ERROR`. | SQLAlchemy query error rollback và trả safe 500; Pydantic mapping error trả safe 500. |
| Access and URL | T041-approved PUBLIC/PRIVATE rule; private access requires ACTIVE enrollment and short-lived signed URL. | PRIVATE requires Student role/token, published parent and ACTIVE enrollment; 403 when not enrolled; object storage signer TTL is 300s. PUBLIC URL must pass HTTP(S) validation. |
| API DD/runtime label | API DD #12 `Draft — Needs Confirmation`; có dòng `RUNTIME_STATUS: ... DECLARED_NOT_RUNNABLE`. | `v1.py` compose #12 và test source tồn tại; đây là documentation/source discrepancy về local composition. Test source không được chạy; production/deployment/browser runtime vẫn chưa xác minh. |

Catalog, API DD và current source không hoàn toàn cùng một mức bảo đảm. `resources.url`/`lesson_id` của legacy DDL khác nullable flags của model/contract; V1-PILOT DDL không có generic `resources` table. Live schema vẫn chưa xác minh.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/02_guest_discovery/GS-07_xem-tai-tai-nguyen/GS-07.md)
