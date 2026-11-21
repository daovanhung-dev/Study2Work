# ST-18 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## Current caller status — 2026-11-20

ST-18 calls #33 for assignment context, #34 for one selected upload and #35
with source fields `content` and `upload_id`. Route changes cancel stale #33
reads. The client validates exact success codes and response IDs/shapes,
separates upload from submission success, and blocks blind repeat after an
ambiguous #34/#35 outcome or accepted submission. API #35 checks ACTIVE
enrollment, deadline and selected upload ownership/course/purpose, then returns
`data.id`; the client passes that ID to ST-19. #33 does not enforce enrollment
or visibility, #34 has no application size/MIME cap, and #35 has no idempotency
or persisted recovery. Runtime and tests were not verified.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-18-API-001` | #33 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-18-API-002` | #34 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-18-API-003` | #35 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #33, #34, #35
- Orchestration/data notes: GET #33 → optional POST #34 (one file) → POST #35 with `content`/`upload_id` → navigate to ST-19 with returned `data.id`. Upload success is not submission success.
- BE/source status and gate: **DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED:** #33–#35 route/view/query/model sources and callers exist. #33 lacks assignment owner/enrollment/publication/deadline checks; #34 checks ACTIVE enrollment when `course_id` is supplied (ST-18 sends it), but the generic schema permits omission, which bypasses that lookup; app source applies no size/MIME cap and returns a public-base URL. #35 checks ACTIVE enrollment/deadline/upload ownership, but has no idempotency or client-independent recovery. `data.id` and inventory `submission_id` differ. Multiple files, draft retention, loaded-screen fields, visual state and live schema/storage remain open.
- Contract sources and discrepancies are preserved in the source excerpts below.

> Source-DD excerpts below retain the earlier `UNWIRED`/`NOT_FOUND` snapshot; current source is summarized above.

### Trích từ DD nguồn: A.4. API contract, source và giới hạn

| API | Contract/source hiện có | Giới hạn |
|---|---|---|
| #33 GET assignment | Catalog 200/401/403/404/500; Student Bearer; response Assignment có id, course_id, title, description?, due_at?, max_score. | Catalog/DD only; access/deadline/submission-rule/nullability/serialization/path errors open; route/module/test NOT_FOUND. |
| #34 POST upload | Route/module/provider/source tests exist; Student purpose SUBMISSION; optional course_id; 201 UploadAsset; source errors 401/403/422/503/500. | No app size/MIME restrictions; optional course_id skips enrollment check when absent; public-base URL; test/live provider/schema not verified. |
| #35 POST submission | Catalog 201 ApiEnvelope<Submission>; body text and file refs strings; errors 401/403/404/409/422/500. | DD-only; wire key, encoding, access/deadline, insert/update, idempotency and storage mapping open; route/module/test NOT_FOUND. |
| #36 GET receipt | AC-17/catalog successor for submission detail; inventory assigns it to ST-19. | Current Student route/module/test NOT_FOUND; do not call silently from ST-18. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-18_soan-va-nop-bai-tap/ST-18.md)
