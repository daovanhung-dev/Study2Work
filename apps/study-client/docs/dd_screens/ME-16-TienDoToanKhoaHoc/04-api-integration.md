# ME-16 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-16-API-001` | #65 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #65
- Orchestration/data notes: #65 local source trả derived student progress page nhưng catalog còn Page<Course>; numeric course_id cần mapping; chỉ handoff student_id sang ME-17/#67 khi có row; #66 thuộc ME-18, AC-26 ordering khác inventory.
- BE/source status và gate: **R**; #65 route/module/query/model/focused tests có local source. **DD READY; IMPLEMENTATION BLOCKED:** API DD Draft/DERIVED, response/catalog mismatch, slug→int64, roster bound, filter/search/reminder data, AC-26 ordering, live schema và Study Web UNWIRED; RUNTIME NOT VERIFIED
- Contract sources and discrepancies are preserved in the source excerpts below.

> CẦN_XÁC_NHẬN: API detail chưa có section riêng trong DD nguồn; xem API catalog/source references và giữ CẦN_XÁC_NHẬN.


## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/ME-16.md)
