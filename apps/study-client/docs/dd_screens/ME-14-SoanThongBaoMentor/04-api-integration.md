# ME-14 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-14-API-001` | #62 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ME-14-API-002` | #63 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #62, #63
- Orchestration/data notes: ME-13 → giữ course + unique Student int64 IDs (carrier chưa chốt); POST #63 chỉ sau khi chốt scope/body/channel. #62 thuộc roster ME-13, không refetch ở ME-14. #63 trả Operation UUID và `meta.notification_ids[]`; #64 là status theo từng notification ID. Không gọi #18: Study route chưa wired, ID/lifecycle unresolved và AC-25 không có edge #18.
- BE/source status và gate: **R**; #63 route/module/model/query/test có local source; API DD Draft/DERIVED. **DD READY; IMPLEMENTATION BLOCKED:** ME-13 handoff/course binding, `content:int64` vs free text, title 120 vs 200, In-app↔PUSH/email-worker, attachment và draft persistence chưa có contract; Study Web UNWIRED; runtime chưa verified
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Nguồn truy vết

- Inventory/route/API/dependencies: [list_screen.md](../../list_screen.md), [global DD screen plan](../../screen_stitch/dd_screens/PLAN.md).
- Trước màn hình này: [ME-13.md](../../screen_stitch/04_mentor/ME-13_chon-nguoi-nhan-thong-bao/ME-13.md).
- Expected flow AC-25: `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio` (page AC-25).
- #63 local source: `apps/study-server/app/api/v1.py`; `apps/study-server/app/modules/mentor/api_63_mentor_notifications_create/`; DD `apps/study-server/docs/dd/63_mentor_notifications_create/`; tests `apps/study-server/tests/modules/mentor/api_63_mentor_notifications_create/`.
- #64 local source: `apps/study-server/app/api/v1.py`; `apps/study-server/app/modules/mentor/api_64_mentor_notification_status/`; DD `apps/study-server/docs/dd/64_mentor_notifications_status/`; tests `apps/study-server/tests/modules/mentor/api_64_mentor_notification_status/`.
- #18 design/current-source status: `apps/study-server/docs/dd/18_operations/`; source route/module/test scan found no Study implementation.
- #34 upload source: `apps/study-server/app/modules/student/api_34_uploads/`; DD `apps/study-server/docs/dd/34_uploads/`.
- Screen prototype: `code.html`, `screen.png`; web status `UNWIRED` in `.agents/context-manifest.json` and `.agents/web-study/`.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14.md)
