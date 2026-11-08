# ST-10 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-10-API-001` | #22 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-10-API-002` | #23 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-10-API-003` | #24 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #22, #23, #24
- Orchestration/data notes: GET #22 → nếu allowed, POST #23 → GET #24 → ST-11; retry/idempotency và #23 auto-vs-click chưa chốt.
- BE/source status và gate: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #22–#24 catalog/API-DD Draft, no Student route/module/query/test; AC-14/15 gate and payload gaps; public #09 exposes published `content`/`video_url` without enrollment check; BIGINT vs V1-PILOT UUID progress schema mismatch; ST-09 lessonId handoff absent; ST-10/ST-11 #24 ownership unresolved; Study Web UNWIRED; `423_LOCKED`/Session Token copy is static
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API, authorization và bảo mật

| API | Declared contract | Current source | Vai trò trong transition |
|---|---|---|---|
| #22 | GET /api/v1/lessons/{lesson_id}/access; Student Bearer; path int64; no query/body; ApiEnvelope<Lesson>; 200/401/403/404/500. | NOT_FOUND route/module/query/test; Draft DD. | Expected entitlement/prerequisite decision; response has no declared `allowed` or reason field. |
| #23 | POST /api/v1/lessons/{lesson_id}/start; Student Bearer; path int64; no query/body; ApiEnvelope<Lesson>; 201/401/403/404/422/500. | NOT_FOUND route/module/query/test; Draft DD. | Expected UPSERT progress IN_PROGRESS; conflicting BIGINT/UUID candidate schemas; key/idempotency/state updates unresolved. |
| #24 | GET /api/v1/lessons/{lesson_id}; Student Bearer; path int64; no query/body; ApiEnvelope<Lesson>; 200/401/403/404/500. | NOT_FOUND route/module/query/test; Draft DD. | Expected content retrieval; independent authorization/publish/projection unresolved. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/ST-10.md)
