# AD-01 — API Integration

> **Current source (2026-11-27):** AD-01 now calls #101 from `AD01Page` on load, period change, and refresh. The client descriptor, `AD01_API_BOUNDARY`, Study Server route, validator, query, view, and response model are source-wired locally. The page sends inclusive date bounds for its `today`/`last7`/`last30` presets and validates the four returned count metrics. This does not resolve the Draft metric/date/UI contract, report-specific permission, or live API/DB/runtime status.

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-01-API-001` | #101 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #101
- Orchestration/data notes: GET #101 với from/to; không tự bịa KPI từ bảng nếu BE chưa trả.
- BE/source status và gate: **R, source-wired locally**; #101 has current route/module/query/model/validator/test source and AD-01 caller. API #101 DD remains `Draft — Needs Confirmation`; its current source requires `ADMIN`, validates/defaults an inclusive date range, and counts created users/courses/enrollments/discussions. Report-specific permission, approval of those metric semantics and of the page presets, audit/service-status sources, and live runtime remain unconfirmed.
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Contract API #101 — expected behavior

| Mục | Contract trực tiếp từ catalog/AC/API DD |
|---|---|
| Method / endpoint | `GET /api/v1/admin/reports/summary` |
| Authentication / authorization | `Authorization: Bearer <JWT>`; catalog ghi role `Admin`; AC-38 đòi quyền xem report/analytics. Report permission/claim mapping chưa được duyệt. |
| Query | `from?:date`, `to?:date`; không path parameter, không request body. Không gửi `segment`, `filters`, `format`, `page` hoặc `size` tới #101. |
| Success | HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Report>`. `Report = {period:{from:date,to:date}, metrics:ImpactMetric[], generated_at:date-time}`; mỗi metric có `{key:string,value:decimal-string,label:string}`. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR`. Catalog không khai báo 400/422 cho date input. |
| Kỳ báo cáo / metric | `from` và `to` đều optional nhưng `Report.period` cần cả hai. Default range, timezone, inclusive/exclusive boundary, metric keys/formulas, population, unit, thứ tự và empty/partial semantics còn mở. |

API #101 DD hiện `Draft — Needs Confirmation`. Bốn metric `user_records_created`, `course_records_created`, `enrollment_records_created`, `discussion_records_created` và default 30 ngày trong DD chỉ là proposal `DERIVED`; chưa được phê duyệt và không khớp trực tiếp bốn card trên ảnh. Không dùng chúng để tự gán card.

### Current source and unresolved design mapping

The local #101 handler requires the shared `ADMIN` role before query parsing, defaults an omitted range to the trailing 30 calendar days in `Asia/Ho_Chi_Minh`, rejects invalid/reversed dates with 422, and counts records created in an inclusive range. `AD01Page` sends explicit inclusive bounds for its three presets, validates the exact period and the four count keys, and renders the returned labels/values. These are current implementation facts, not approval of the proposed KPI mapping or period controls. The screenshot's learner-impact, activity, audit, and health claims are not supplied by this response. Browser, deployed API, and DB behavior remain unverified.

### Trích từ DD nguồn: Nguồn truy vết

- [Master screen inventory](../../list_screen.md), [global DD plan](../../screen_stitch/dd_screens/PLAN.md)
- [API catalog](../../../../../docs/lists/list_api.md), [AC-38 index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-38 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API #101 cover](../../../../study-server/docs/dd/101_admin_reports_summary/00_Cover.md), [request](../../../../study-server/docs/dd/101_admin_reports_summary/03_Request.md), [response](../../../../study-server/docs/dd/101_admin_reports_summary/04_Response.md), [data mapping](../../../../study-server/docs/dd/101_admin_reports_summary/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/101_admin_reports_summary/06_Error.md), [open questions](../../../../study-server/docs/dd/101_admin_reports_summary/OPEN_QUESTIONS.md)
- [Current Study router](../../../../study-server/app/api/v1.py), [shared JWT/role helper](../../../../study-server/app/utils/auth.py), [Admin #68 validator](../../../../study-server/app/modules/admin/api_68_admin_users_list/validate.py), [Student-only #04 profile](../../../../study-server/app/modules/student/api_04_users_me/view.py), [health readiness source](../../../../study-server/app/main.py)

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/AD-01.md)
