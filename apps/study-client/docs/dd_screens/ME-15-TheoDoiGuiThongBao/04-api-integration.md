# ME-15 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-15-API-001` | #18 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ME-15-API-002` | #64 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #18, #64
- Orchestration/data notes: Chỉ gọi #64 với một notification_id sau khi producer/caller chọn rõ ID; không gửi UUID `data.id` vào path. Không gọi #18: Study route/module/query/test chưa có, ID int64/UUID còn mâu thuẫn, và AC-25 node #18 không nối flow. Prototype refresh chỉ timer/toast, channel/report/ACK/real-time claims là static; Study Web UNWIRED.
- BE/source status và gate: **M**; #64 có local route/module/query/model/test, #18 D/UNWIRED. **DD READY; IMPLEMENTATION BLOCKED:** batch ID selection, status mapping/lifecycle, per-channel/recipient report and realtime contract, destination links, Study Web route/auth/client; live schema/provider/runtime chưa verified
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Nguồn truy vết chính

- Screen inventory: `apps/study-client/docs/list_screen.md`, dòng ME-15; kế hoạch tổng: `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`.
- Prototype: `screen.png`, `code.html` trong thư mục này. Original SHA-256 trước khi làm: PNG `6172c259a4dfca9a37a6652ebdae83d3f10831b63dd8b59b5e988a23ea534713`; HTML `ccd0151ae1352662dc006483ff0e00094d9317d35762e76515252c32b7dda70f`.
- Handoff #63: `apps/study-server/app/modules/mentor/api_63_mentor_notifications_create/{models.py,view.py,query.py}` và `apps/study-server/tests/modules/mentor/api_63_mentor_notifications_create/test_mentor_notifications_create.py`.
- API #64: `apps/study-server/app/api/v1.py`; `apps/study-server/app/modules/mentor/api_64_mentor_notification_status/{models.py,validate.py,query.py,view.py}`; API DD `apps/study-server/docs/dd/64_mentor_notifications_status/`.
- Generic #18: `apps/study-server/docs/dd/18_operations/` mô tả design-only; hiện không có route/module/query/test Study. Catalog tại `docs/lists/list_api.md`.
- Activity: `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio`, trang AC-25; connected node `n8` là #64, còn `operation_status` (#18) không có incident edge. SH-07 cũng phân biệt generic #18 với notification-specific #64.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-15_theo-doi-gui-thong-bao/ME-15.md)
