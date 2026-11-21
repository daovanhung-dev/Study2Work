# ME-16 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-16-API-001` | #65 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #65
- Orchestration/data notes: Current client calls #65 with validated route `course_id`; local backend returns one unpaginated derived Student-progress Page while catalog says `Page<Course>`. Validated row Student IDs link to ME-17/#67. #66 belongs to ME-18; AC-26 ordering remains different from inventory.
- BE/source status và gate: **R**; #65 route/module/query/model/focused tests and ME16 caller source exist. **SOURCE-WIRED / PARTIAL:** exact local response checks and route cancellation. **OPEN:** API DD Draft/DERIVED, response/catalog mismatch, course-route provenance/slug mapping, roster bound, filter/search/reminder data, AC-26 ordering, live schema/runtime.
- Contract sources and discrepancies are preserved in the source excerpts below.

> CẦN_XÁC_NHẬN: API detail chưa có section riêng trong DD nguồn; xem API catalog/source references và giữ CẦN_XÁC_NHẬN.

### Current Study Client integration

- The page calls #65 only with a positive int64-safe `courseId`; changing the route cancels the old request. The service sends no query/body because #65 has no pagination/filter inputs.
- The client requires success code `DESIGN_RESOURCE_RETRIEVED`, the local unpaginated pagination shape, unique Student IDs, valid name/avatar projection, nonnegative completed/total counts (`completed≤total`) and percentage 0..100. Optional avatars render only from HTTPS or same-origin HTTP with `no-referrer` and initials fallback.
- The server scopes course to direct owner and ACTIVE Student enrollment, then aggregates published lessons. The catalog says `Page<Course>`; this local response is `Page<MentorStudentProgress>`, so the source-backed caller is not evidence that the Draft catalog conflict is approved.
- No browser/runtime verification or tests were run.


## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/ME-16.md)
