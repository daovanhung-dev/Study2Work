# AD-01 — Dashboard quản trị · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-01` |
| Module | Admin |
| Route | `/admin` — current Admin router maps this route to `AD01Page` inside `AdminLayout`; runtime deployment chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); current source: **IMPLEMENTATION PARTIAL** (AD-01 calls #101 and renders its source-backed count metrics; KPI/date/UI approval and report-specific permission remain blocked) · **Runtime:** `RUNTIME NOT VERIFIED`. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-01.md](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/AD-01.md), [AD-01_PLAN.md](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/AD-01_PLAN.md), [AD-01_markers.json](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/AD-01_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Tổng quan hệ thống theo khoảng ngày: học viên, khóa, tác động và các KPI.
- In-scope: GET #101 với from/to; không tự bịa KPI từ bảng nếu BE chưa trả.
- Out-of-scope: No KPI, service-health, audit, date-range or report-permission behavior without a source contract; do not treat UI state or route presence as runtime evidence.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-38 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Tổng quan hệ thống theo khoảng ngày: học viên, khóa, tác động và các KPI. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #101
- Liên kết màn hình dự kiến: [AD-02](../AD-02-DanhSachNguoiDung/00-overview.md), [AD-06](../AD-06-DanhSachKhoaHocQuanTri/00-overview.md), [AD-24](../AD-24-BaoCaoTacDongCongDong/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/partial/no-data/error |
| Current source | `admin.routes.ts`, `AdminLayout`, `AD01Page`, `AD01ReportService`, #101 route/module | `/admin` is source-routed; AdminLayout gates the page on an in-memory Admin session; the page calls #101 and renders validated returned count metrics for its selected date range. The DD remains blocked on whether these KPIs/presets satisfy the approved design. |
| Runtime | Worklog/context Study Web | `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-01 source screen.png](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/screen_annotated.png))
- Luồng: GET #101 với from/to; không tự bịa KPI từ bảng nếu BE chưa trả.
- Current source: the route/layout/page and three safe shortcut links are wired. `AD01Page` calls #101, computes inclusive Vietnam-calendar date ranges for three presets, validates the report envelope/period/four metric keys, and renders returned counts. #101 route/module/query/model/validator/test sources exist locally. Audit/service-health data is not supplied. API DD/metric semantics, preset approval, report-specific permission, and live runtime remain unresolved.
- Priority: P1; Gate/source status: **R / IMPLEMENTATION PARTIAL**; **BLOCK:** #101 DD and UI/KPI mapping remain pending confirmation despite local source wiring.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

> Current-source note (2026-11-27): the Study Web Admin route/layout/page and #101 caller exist locally. The layout accepts an in-memory Admin session from #03 only when the profile role is `ADMIN`; API #101 also enforces the `ADMIN` role. AD01Page currently requests and renders four source-backed record counts for an inclusive date range. The original source excerpt below predates this implementation and is historical where it says the route, caller, date controls, or API #101 source are absent. Report-specific permission and KPI/date/preset approval remain open.

# AD-01 — Dashboard quản trị

> **DD status:** `DD BLOCKED` for report/KPI behavior · **Implementation:** `PARTIAL` (#101 caller and source exist; design mapping and authorization remain open) · **Runtime:** `RUNTIME NOT VERIFIED`
> Screen UI DD, không phải bằng chứng API/client đã chạy. Mockup và API #101 còn các contract gap ngăn mapping KPI, ngày báo cáo, identity và status an toàn.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | `AD-01` — Dashboard quản trị |
| Mục tiêu kỳ vọng | Cho Admin xem tổng quan hệ thống theo kỳ, tiếp cận KPI và điều hướng tới các khu vực quản trị/báo cáo. Các KPI cụ thể chưa được định nghĩa trong contract. |
| Actor | `Admin`. AC-38 yêu cầu Admin có quyền xem report/analytics. API catalog #101 khai báo Bearer JWT, role Admin. Report-specific permission policy chưa được xác nhận. |
| Route đề xuất | `/admin`; inventory route, không phải route runtime đã đăng ký. |
| Điều kiện vào | Phiên Admin hợp lệ và được phép truy cập dashboard; cần định nghĩa nguồn principal/profile. Không có Study Web router hoặc Admin profile route hiện hành. |
| API nghiệp vụ | API #101 `GET /api/v1/admin/reports/summary`; direct design contract xem dưới đây. Current local route/module/query/model/validator/test sources and a Web caller exist; API DD remains `Draft — Needs Confirmation`. |
| Handoff | AD-02 users, AD-06 courses, AD-10 moderation là ba quick link trong HTML. Inventory cũng liên kết AD-24; AC-38 tiếp tục #102, và có thể gọi #103 export. Không có bằng chứng các route UI này đã hoạt động. |
| Kết quả | Khi có contract và client mapping được duyệt, dashboard hiển thị report theo kỳ. Không có side effect được xác nhận; #101 được mô tả là read-only trong API DD. |

### Contract API #101 — expected behavior

| Mục | Contract trực tiếp từ catalog/AC/API DD |
|---|---|
| Method / endpoint | `GET /api/v1/admin/reports/summary` |
| Authentication / authorization | `Authorization: Bearer <JWT>`; catalog ghi role `Admin`; AC-38 đòi quyền xem report/analytics. Report permission/claim mapping chưa được duyệt. |
| Query | `from?:date`, `to?:date`; không path parameter, không request body. Không gửi `segment`, `filters`, `format`, `page` hoặc `size` tới #101. |
| Success | HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Report>`. `Report = {period:{from:date,to:date}, metrics:ImpactMetric[], generated_at:date-time}`; mỗi metric có `{key:string,value:decimal-string,label:string}`. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR`. Catalog không khai báo 400/422 cho date input. |
| Kỳ báo cáo / metric | `from` và `to` đều optional nhưng `Report.period` cần cả hai. Default range, timezone, inclusive/exclusive boundary, metric keys/formulas, population, unit, thứ tự và empty/partial semantics còn mở. |

API #101 DD hiện `Draft — Needs Confirmation`. Bốn metric `user_records_created`, `course_records_created`, `enrollment_records_created`, `discussion_records_created` và default 30 ngày trong DD chỉ là proposal `DERIVED`; chưa được phê duyệt và không khớp trực tiếp bốn card trên ảnh. Không dùng chúng để tự gán card.

### Tách expected behavior và current behavior

| Chủ đề | Expected behavior | Current evidence |
|---|---|---|
| Dashboard load | Admin mở `/admin`, chọn kỳ và nhận #101 summary theo AC-38. | Current `/admin` route renders AD01Page inside AdminLayout after an in-memory Admin login session; the page calls #101 on load and after period/refresh actions. Live API/DB is unverified. |
| KPI | Inventory muốn tổng quan học viên/khóa/tác động/KPI. API #101 currently returns four created-record counts. | The page validates and renders the #101 user/course/enrollment/discussion counts. They do not establish the screenshot's learner-impact/activity KPIs; metric mapping remains unapproved. |
| Khoảng ngày | Inventory yêu cầu #101 với `from`/`to`. | Three active presets compute inclusive calendar dates in `Asia/Ho_Chi_Minh` and send both bounds. The API also defaults omitted bounds to an inclusive trailing 30-day range; preset/default approval remains open. |
| Admin identity | Trang là Admin portal. | AdminLayout displays `full_name`/`role` from the validated #03 login response held in `AdminSessionService`; no separate `/admin/me` endpoint exists. |
| Admin authorization | AC-38 yêu cầu quyền report; API #101 khai báo role Admin. | AdminLayout verifies the `ADMIN` role for the shell and #101 applies the shared `ADMIN` role guard. A separate report/analytics permission rule is not established. |
| Audit và health | Mockup hiển thị activity, security, DB/auth/queue status và các claim tuân thủ. | Không thuộc `Report` #101; trạng thái trong HTML là static. `/health/ready` chỉ báo dependency configured, không probe database. Không có route Admin audit list gắn với dashboard được tìm thấy. |

### Asset và design evidence

- [Ảnh gốc](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/screen.png): 1600×1594, SHA-256 `93304b0a9846047a5e21a90bdb44fb197d4449e9dc725ec13b4239f416a0c25f`.
- [HTML gốc](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/code.html): 26,680 bytes, SHA-256 `e9c678cee115f8ac83b9d73779420005d411ad7918846696ff4c6fe8484df979`.
- [Ảnh đánh số](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/screen_annotated.png), [marker map](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/AD-01_markers.json) và [SVG overlay](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/AD-01_markers.svg) giữ kích thước/tỷ lệ của ảnh gốc.
- [Study Web Design System](../../../../../.agents/web-study/design.md) là visual target; mockup hiện dùng cobalt palette và remote Plus Jakarta Sans, khác token ocean-blue và font Inter/system. Đây là `DESIGN DISCREPANCY`, không được coi screenshot là ngoại lệ đã được duyệt.

### Nguồn truy vết

- [Master screen inventory](../../list_screen.md), [global DD plan](../../screen_stitch/dd_screens/PLAN.md)
- [API catalog](../../../../../docs/lists/list_api.md), [AC-38 index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-38 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API #101 cover](../../../../study-server/docs/dd/101_admin_reports_summary/00_Cover.md), [request](../../../../study-server/docs/dd/101_admin_reports_summary/03_Request.md), [response](../../../../study-server/docs/dd/101_admin_reports_summary/04_Response.md), [data mapping](../../../../study-server/docs/dd/101_admin_reports_summary/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/101_admin_reports_summary/06_Error.md), [open questions](../../../../study-server/docs/dd/101_admin_reports_summary/OPEN_QUESTIONS.md)
- [Current Study router](../../../../study-server/app/api/v1.py), [shared JWT/role helper](../../../../study-server/app/utils/auth.py), [Admin #68 validator](../../../../study-server/app/modules/admin/api_68_admin_users_list/validate.py), [Student-only #04 profile](../../../../study-server/app/modules/student/api_04_users_me/view.py), [health readiness source](../../../../study-server/app/main.py)
