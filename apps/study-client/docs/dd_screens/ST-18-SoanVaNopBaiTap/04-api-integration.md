# ST-18 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-18-API-001` | #33 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-18-API-002` | #34 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-18-API-003` | #35 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #33, #34, #35
- Orchestration/data notes: GET #33 → POST #34 cho từng file khi cần → thu asset reference → POST #35 → nhận submission_id. Tách trạng thái upload thành công khỏi submission thành công; F06 chưa chốt giữ draft/nội dung qua lỗi.
- BE/source status và gate: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #33/#35 Student route/module/test NOT_FOUND; #33 access/deadline/rule và GET ownership trùng ST-17/AC-17 chưa chốt; #34 local route/module/provider/test source-backed nhưng không có application size/MIME cap, course_id optional, URL public-base; API index #034 cập nhật R, live DB/storage chưa verify; #35 file-ref key/encoding/cardinality, text constraints, persistence/idempotency, data.id vs submission_id open; draft/URL/checklist/consent and error-retention rules lack contract; candidate legacy BIGINT uploads/assignments/submissions vs V1-PILOT without business tables; #36 is assigned to ST-19 by inventory but AC-17 places read before submitted state; loaded PNG/Guest fallback HTML/hash route and Study Web design target differ; Study Web UNWIRED
- Contract sources and discrepancies are preserved in the source excerpts below.

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
