# GS-01 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `GS-01-API-001` | #05 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `GS-01-API-002` | #06 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #05, #06
- Orchestration/data notes: GET #5 cache-first locale → GET #6 page=1,size=20; reset page sau sort/filter; không gửi category đến khi BE hỗ trợ.
- BE/source status và gate: **R**; **BLOCK:** Category chỉ hiển thị metadata; filter category chưa hoạt động
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: 10. Nguồn truy vết

- Inventory, AC link, F02 và UI-state requirements: [`list_screen.md`](../../list_screen.md) (GS-01, F02, API 005/006 và G-05).
- Canonical API catalog/schema: [`list_api.md`](../../../../../docs/lists/list_api.md) (API #05/#06 rows and `Category`/`Course` definitions); [`AC-03 diagram`](../../../../study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) (Guest actor, pre/postconditions and #05→#06 order).
- Kế hoạch và marker coordinates trước DD: [`GS-01_PLAN.md`](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/GS-01_PLAN.md); ordered marker map: [`GS-01_markers.json`](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/GS-01_markers.json).
- Study Web status context: [`study-web index`](../../../../../.agents/web-work/study/INDEX.md) and [`entry`](../../../../../.agents/web-work/study/AGENTS.md), both registered `UNWIRED`; they do not establish runtime.
- Target UI guidance: [`design.md`](../../../../../.agents/web-study/design.md).
- Route registration: [`v1.py`](../../../../study-server/app/api/v1.py); API #05 [`models.py`](../../../../study-server/app/modules/guest/api_05_categories/models.py), [`validate.py`](../../../../study-server/app/modules/guest/api_05_categories/validate.py), [`query.py`](../../../../study-server/app/modules/guest/api_05_categories/query.py), [`view.py`](../../../../study-server/app/modules/guest/api_05_categories/view.py).
- API #06 [`models.py`](../../../../study-server/app/modules/guest/api_06_courses/models.py), [`validate.py`](../../../../study-server/app/modules/guest/api_06_courses/validate.py), [`query.py`](../../../../study-server/app/modules/guest/api_06_courses/query.py), [`view.py`](../../../../study-server/app/modules/guest/api_06_courses/view.py); shared mapping/model [`helpers.py`](../../../../study-server/app/modules/guest/_shared/course_catalog/helpers.py), [`models.py`](../../../../study-server/app/modules/guest/_shared/course_catalog/models.py), sort [`constants.py`](../../../../study-server/app/modules/guest/_shared/course_catalog/constants.py), [`validate.py`](../../../../study-server/app/utils/validate.py), envelopes [`responses.py`](../../../../study-server/app/core/responses.py).
- Relevant source tests (read, not run): [`API #05 tests`](../../../../study-server/tests/modules/guest/api_05_categories/test_categories.py), [`API #06 tests`](../../../../study-server/tests/modules/guest/api_06_courses/test_courses.py), and downstream [`API #08 tests`](../../../../study-server/tests/modules/guest/api_08_courses_detail/test_courses_detail.py). API #08 source: [`view.py`](../../../../study-server/app/modules/guest/api_08_courses_detail/view.py).
- Checked-in DDL (not live DB verification): [`DB.sql`](../../../../../infra/postgres/study-server/DB.sql).

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/GS-01.md)
