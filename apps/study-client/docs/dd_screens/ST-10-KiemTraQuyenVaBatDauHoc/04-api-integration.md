# ST-10 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## Current caller status — 2026-11-20

ST-10 calls #22 on entry and sends #23 only after an explicit user action when
#22 returns `DESIGN_RESOURCE_RETRIEVED` with the same lesson and
`status=PUBLISHED`. It requires `DESIGN_RESOURCE_CREATED` from #23, validates
response shape/lesson ID, and observes route param changes while cancelling
stale #22 reads. It then navigates to ST-11, which calls #24. Current source
discrepancy: #22 does not filter lesson status, and #23 does not independently
check lesson/course publication. The client gate does not repair that
server-side gap. See [the screen inventory](../../list_screen.md)
and [T038 gap matrix](../../../../.agents/worklog/2026-11-17/T038-screen-gap-matrix.md)
for current caller/source status; the excerpt below preserves design-time
contracts.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-10-API-001` | #22 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-10-API-002` | #23 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-10-API-003` | #24 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #22, #23, #24
- Orchestration/data notes: GET #22 → explicit user click → POST #23 → ST-11 calls GET #24. The current client checks exact #22/#23 success business codes and does not render content/media from #22/#23. Retry/idempotency and product approval of the click trigger remain open.
- BE/source status và gate: **DD BLOCKED; IMPLEMENTATION PARTIAL / SOURCE_WIRED; RUNTIME NOT VERIFIED.** #22–#24 and ST-10 caller source exist; access/payload/retry decisions remain open; public #09 exposes published `content`/`video_url` without enrollment check; BIGINT vs V1-PILOT UUID progress schema mismatch; ST-09 lessonId handoff absent; ST-11 owns #24; `423_LOCKED`/Session Token copy is static.
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API, authorization và bảo mật

| API | Declared contract | Current source | Vai trò trong transition |
|---|---|---|---|
| #22 | GET /api/v1/lessons/{lesson_id}/access; Student Bearer; path int64; no query/body; ApiEnvelope<Lesson>; 200/401/403/404/500. | Route/handler/query/model/test source exists; success is `DESIGN_RESOURCE_RETRIEVED`; checks Student role, published course and active/completed enrollment; does not filter lesson status. | ST10 calls on entry; response has no declared `allowed` or reason field, so client only permits start for a matching PUBLISHED lesson. |
| #23 | POST /api/v1/lessons/{lesson_id}/start; Student Bearer; path int64; no query/body; ApiEnvelope<Lesson>; 201/401/403/404/422/500. | Route/handler/query/model/test source exists; success is `DESIGN_RESOURCE_CREATED`; validates Student, lesson/course and enrollment, writes lesson progress and returns Lesson; does not independently check publication. | ST10 calls after explicit Start click; DB mapping/idempotency and response projection decisions remain open. |
| #24 | GET /api/v1/lessons/{lesson_id}; Student Bearer; path int64; no query/body; ApiEnvelope<Lesson>; 200/401/403/404/500. | Route/handler/query/model/test source exists; checks Student, published parent course and enrollment; Lesson response can include content/video fields. | ST11 owns the post-handoff request; direct-call/publish/projection decisions remain open. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/ST-10.md)
