# ST-11 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## Current caller status — 2026-11-20

ST-11 calls #24 through `StudentApiService`; it follows route `lessonId`
changes, cancels stale reads, checks `DESIGN_RESOURCE_RETRIEVED`, payload shape
and matching lesson ID, and exposes retry on request failure. API #24 source
checks that the lesson and parent course are `PUBLISHED` and that the Student
has `ACTIVE` or `COMPLETED` enrollment. ST-11 links to ST-12, which calls #26.
ST-11 does not call #25 or #27 and does not play `video_url`; #25's current
request model omits the catalog's `position`, and no approved completion
trigger/terminal flow is implemented. Runtime is not verified. The detailed
source excerpt below preserves the original design snapshot.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-11-API-001` | #24 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-11-API-002` | #25 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-11-API-003` | #26 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-11-API-004` | #27 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #24, #25, #26, #27
- Orchestration/data notes: current ST-11 calls #24 and links to ST-12; it does not call #25/#27. Declared later actions remain design expectations, not implemented screen behavior.
- BE/source status and gate: **DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED:** page/player UI does not match all Stitch states; progress/position and completion rules remain unresolved; #27 does not yet establish a complete authorized/terminal flow; API DDs remain Draft and checked-in candidate DDL does not establish live schema.
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API, authorization và bảo mật

| API | Declared contract | Current source | Vai trò / open issue |
|---|---|---|---|
| #24 | GET `/api/v1/lessons/{lesson_id}`; Student Bearer; path int64; `ApiEnvelope<Lesson>`; 200/401/403/404/500. | Client caller and Study Server route/view/query/model exist; page validates success code, payload and ID. | Backend checks published lesson/course and ACTIVE/COMPLETED enrollment; screen fetch is implemented, player is not. |
| #25 | PATCH `/api/v1/lessons/{lesson_id}/progress`; catalog declares `position`, `percent`, `completed`; current request model has only `percent`, `completed`. | Study Server route/view/query/model exist; ST-11 does not call it. | Persists lesson progress; current code does not update course aggregate and current DDL has no lesson position mapping. |
| #26 | GET `/api/v1/lessons/{lesson_id}/resources`; Student Bearer; response source is `LessonResources` with `resources[]`. | Study Server route/view/query/model exist; ST-12 is the caller. | Checks ACTIVE enrollment and published lesson/course; returns metadata without a URL. |
| #27 | GET `/api/v1/lessons/{lesson_id}/next`; Student Bearer; response source is next-lesson model. | Study Server route/view/query/model exist; ST-11 does not call it. | Uses course/order sorting; current view ignores the authenticated user for entitlement and returns 404 if no next item. |

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
