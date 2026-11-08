# AD-01 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-01-API-001` | #101 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #101
- Orchestration/data notes: GET #101 với from/to; không tự bịa KPI từ bảng nếu BE chưa trả.
- BE/source status và gate: **D**; **BLOCK:** #101 chưa có route/module/query/model/test; thiếu Admin self-profile endpoint; KPI/date semantics và status/audit sources chưa xác nhận; Study Web UNWIRED
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

### Trích từ DD nguồn: Nguồn truy vết

- [Master screen inventory](../../list_screen.md), [global DD plan](../../screen_stitch/dd_screens/PLAN.md)
- [API catalog](../../../../../docs/lists/list_api.md), [AC-38 index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-38 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API #101 cover](../../../../study-server/docs/dd/101_admin_reports_summary/00_Cover.md), [request](../../../../study-server/docs/dd/101_admin_reports_summary/03_Request.md), [response](../../../../study-server/docs/dd/101_admin_reports_summary/04_Response.md), [data mapping](../../../../study-server/docs/dd/101_admin_reports_summary/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/101_admin_reports_summary/06_Error.md), [open questions](../../../../study-server/docs/dd/101_admin_reports_summary/OPEN_QUESTIONS.md)
- [Current Study router](../../../../study-server/app/api/v1.py), [shared JWT/role helper](../../../../study-server/app/utils/auth.py), [Admin #68 validator](../../../../study-server/app/modules/admin/api_68_admin_users_list/validate.py), [Student-only #04 profile](../../../../study-server/app/modules/guest/api_04_users_me/view.py), [health readiness source](../../../../study-server/app/main.py)

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/AD-01.md)
