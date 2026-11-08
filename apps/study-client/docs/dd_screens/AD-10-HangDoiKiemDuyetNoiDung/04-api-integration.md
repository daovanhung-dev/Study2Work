# AD-10 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-10-API-001` | #78 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #78
- Orchestration/data notes: GET #78 → chọn content_id mở AD-11.
- BE/source status và gate: **R** local #78 route/module/query/model/validator/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** catalog/AC singular Content vs local Page; pagination/order/422 và type enum còn DERIVED; thiếu course title, author, submitted time, version; stale/deleted visibility, moderation permission, live schema/deployment chưa chốt; Study Web UNWIRED. **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Nguồn truy vết

- [Screen inventory](../../list_screen.md) · [Global screen plan](../../screen_stitch/dd_screens/PLAN.md) · [AC-33 Admin flow](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) · [API catalog](../../../../../docs/lists/list_api.md)
- [API #78 route](../../../../study-server/app/api/v1.py) · [#78 model](../../../../study-server/app/modules/admin/api_78_admin_content_pending/models.py) · [#78 validator](../../../../study-server/app/modules/admin/api_78_admin_content_pending/validate.py) · [#78 view](../../../../study-server/app/modules/admin/api_78_admin_content_pending/view.py) · [#78 query](../../../../study-server/app/modules/admin/api_78_admin_content_pending/query.py)
- [#78 focused test source](../../../../study-server/tests/modules/admin/api_78_admin_content_pending/test_admin_content_pending.py) · tests are source evidence only; none were run for AD-10.
- [#78 overview](../../../../study-server/docs/dd/78_admin_content_pending/02_Overview.md) · [request](../../../../study-server/docs/dd/78_admin_content_pending/03_Request.md) · [mapping](../../../../study-server/docs/dd/78_admin_content_pending/05_Data_Mapping.md) · [errors](../../../../study-server/docs/dd/78_admin_content_pending/06_Error.md) · [open questions](../../../../study-server/docs/dd/78_admin_content_pending/OPEN_QUESTIONS.md)
- [API #79 route and model](../../../../study-server/app/api/v1.py) · [#79 Content model](../../../../study-server/app/modules/admin/api_79_admin_content_detail/models.py) · [legacy candidate DDL](../../../../../infra/postgres/study-server/DB.sql) · [migration 006 contents](../../../../../infra/postgres/study-server/migrations/006_contents.sql) · [migration 007 content versions](../../../../../infra/postgres/study-server/migrations/007_content_versions.sql)
- [Study Web design target](../../../../../.agents/web-study/design.md) · [Study Web scope index](../../../../../.agents/web-work/study/INDEX.md)

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10.md)
