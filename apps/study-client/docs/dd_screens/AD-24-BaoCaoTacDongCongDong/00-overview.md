# AD-24 — Báo cáo tác động cộng đồng · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-24` |
| Module | Admin |
| Route | `/admin/reports/community-impact` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** BLOCKED — metric, date, segment and permission contracts do not support implementation without product/API decisions.<br>; **Implementation status:** BLOCKED — Study Web is UNWIRED and APIs #101/#102 have no local route or query source.<br>; **Runtime status:** NOT VERIFIED — this DD records design assets, catalog/AC and current source inspection only. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-24.md](../../screen_stitch/05_admin/AD-24_bao-cao-tac-dong-cong-dong/AD-24.md), [AD-24_PLAN.md](../../screen_stitch/05_admin/AD-24_bao-cao-tac-dong-cong-dong/AD-24_PLAN.md), [AD-24_markers.json](../../screen_stitch/05_admin/AD-24_bao-cao-tac-dong-cong-dong/AD-24_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Date range, phân khúc, KPI và biểu đồ tác động.
- In-scope: GET #101 tổng quan, GET #102 theo from/to/segment; giữ filter URL cho export.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-38 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Date range, phân khúc, KPI và biểu đồ tác động. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #101, #102
- Liên kết màn hình dự kiến: [AD-25](../AD-25-XuatBaoCaoVaTheoDoiTienTrinh/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/no-data/partial/ready |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-24 source screen.png](../../screen_stitch/05_admin/AD-24_bao-cao-tac-dong-cong-dong/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-24_bao-cao-tac-dong-cong-dong/screen_annotated.png))
- Luồng: GET #101 tổng quan, GET #102 theo from/to/segment; giữ filter URL cho export.
- Priority: P2; Gate/source status: **D**; #101/#102 catalog/Draft-only, không có local route/query/model/test. **DD BLOCKED; IMPLEMENTATION BLOCKED:** KPI formula/population/source; date type/default/validation; segment vocabulary; AC-38 validation order; report permission/live schema; AD-25 filter handoff/#103 response mismatch; Study Web UNWIRED; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-24 — Báo cáo tác động cộng đồng

> **DD status:** BLOCKED — metric, date, segment and permission contracts do not support implementation without product/API decisions.<br>
> **Implementation status:** BLOCKED — Study Web is UNWIRED and APIs #101/#102 have no local route or query source.<br>
> **Runtime status:** NOT VERIFIED — this DD records design assets, catalog/AC and current source inspection only.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | AD-24 — Báo cáo tác động cộng đồng |
| Mục tiêu | Cho Admin xem báo cáo tổng hợp về tương tác học tập và tác động cộng đồng theo khoảng ngày/phân khúc; có thể mở luồng xuất AD-25 theo AC-38. Công thức và dữ liệu cụ thể chưa được xác nhận. |
| Actor | AC-38 và API catalog ghi Admin; điều kiện trước của AC yêu cầu quyền xem report/analytics. Current Study auth helper hỗ trợ kiểm tra role tường minh, nhưng #101/#102 chưa có route/guard hay policy source. |
| Route | `/admin/reports/community-impact` là route candidate từ inventory. Study Web hiện không có editable route/client. |
| Điều kiện trước | Expected: Admin có quyền xem báo cáo/analytics. Current: prototype không xác thực session, không đọc principal, và badge RBAC chỉ là text tĩnh. |
| Điều kiện sau | Current: đổi một số giá trị trong DOM hoặc hiển thị timer giả; không tải report và không có server side effect. Expected: AC-38 hiển thị report tổng hợp sau #101/#102; nhánh export chuyển sang AD-25/#103; view-only có thể kết thúc sau khi render. |
| Liên kết màn hình | AD-01 là dashboard summary dùng #101; AD-24 gắn #102; AD-25 là export candidate. Inventory yêu cầu giữ filter URL cho export. |
| API liên quan | #101 `GET /api/v1/admin/reports/summary`; #102 `GET /api/v1/admin/reports/community-impact`; optional #103 thuộc nhánh xuất/AD-25, không được gọi từ handler hiện tại. Tất cả report endpoints hiện chỉ có catalog/Draft DD. |
| Dữ liệu | Catalog #101/#102 trả generic `ApiEnvelope<Report>`. API DD Draft mô tả `Report.period`, `metrics[]` và `generated_at`; không có response/runtime mapping cho bốn card cụ thể của prototype. |
| Bảo mật | Expected Bearer JWT/Admin và AC report/analytics permission. Current shared helper có thể nhận role và các Admin APIs #68–#98 dùng `ADMIN`; điều này không chứng minh #101/#102 được đăng ký hoặc bảo vệ. |
| Trạng thái hiện tại | Static prototype. Apply, Reset và Refresh chỉ sửa DOM hoặc animation; export là path link; Study Web `UNWIRED`; #101/#102 `D`/Draft, không có current route/query/test. |
| Phụ thuộc chưa hoàn thiện | Metric semantics/source/population/formula, date defaults/validation, segment vocabulary, authorization policy, report writer/schema, filter URL handoff, #103 response/Operation mismatch, Study Web implementation. |

### Nguồn và ranh giới bằng chứng

- **Expected behavior:** inventory row 82, AC-38, API catalog #101/#102 và các API DD Draft. AC diagram mong Admin có report permission, dashboard summary/impact metrics và export tùy chọn.
- **Current prototype:** `code.html` có date values cố định, segment options tĩnh, KPI placeholders `--`, empty chart message và data-definition cards. Script chỉ toggle CSS/text bằng timers; không có fetch/XHR/API client, không có form submit, chart data binding hay URL update.
- **Current Study source:** scoped search trong `apps/study-server/app` và `apps/study-server/tests` không tìm thấy #101/#102 route/module/query/model/test. Current `app/api/v1.py` composes Admin routes through #98. Study Web có 0 tracked `apps/study-client/src` files, không có editable package/router/client; ignored `dist` không chứng minh page runtime.
- **API DD status:** #101/#102 đều `Draft — Needs Confirmation` và ghi `UNWIRED / NOT_FOUND`. #101 open questions nói helper chỉ có Student guard, nhưng current `validate_current_user_request` nhận role hoặc sequence role và API #68–#98 dùng `ADMIN`. Đây là API DD/source discrepancy; chưa có report-specific guard/policy.
- **Candidate database evidence:** checked-in legacy DDL có `enrollments` và self-referencing `discussions`; V1-PILOT DDL riêng có `report_snapshots`. Các artifact này không chứng minh live schema/deployment, metric policy, snapshot writer hay report freshness. AC-19 biểu diễn Comment riêng, khác legacy `discussions.parent_id` reply candidate.
- **No runtime claim:** API catalog, AC diagram, API DD và mockup không chứng minh route hoạt động, quyền report, dữ liệu sản xuất, chart, metric freshness hay export job.

### Source register

| Source | Phạm vi đối chiếu |
|---|---|
| [Screen inventory](../../list_screen.md) | AD-24/AD-25 routes, APIs, expected states and filter-to-export handoff. |
| [AC-38 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio), [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) | Actor/precondition/postcondition, #101→#102 order, validation/render, optional #103/export branch. |
| [API catalog](../../../../../docs/lists/list_api.md) | Direct #101/#102 method/query/role/response/error declarations; #103 and Operation tracking discrepancy. |
| [#101 API DD](../../../../study-server/docs/dd/101_admin_reports_summary/00_Cover.md), [#101 questions](../../../../study-server/docs/dd/101_admin_reports_summary/OPEN_QUESTIONS.md), [#102 API DD](../../../../study-server/docs/dd/102_admin_reports_community_impact/00_Cover.md), [#102 mapping](../../../../study-server/docs/dd/102_admin_reports_community_impact/05_Data_Mapping.md), [#102 questions](../../../../study-server/docs/dd/102_admin_reports_community_impact/OPEN_QUESTIONS.md) | Draft shapes/proposals and explicit open decisions. |
| [Study Server router](../../../../study-server/app/api/v1.py), [shared auth helper](../../../../study-server/app/utils/auth.py), [declared route context](../../../../../.agents/server-study/apis/declared-routes.md) | Current route limit and reusable Admin-capable guard; no report route. |
| [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) | Candidate source relations and separate snapshot candidate only. |
| [AD-01 DD](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/AD-01.md) | Existing #101 card mapping blocker and dashboard-to-#102 relationship. |
| [Study Web design guide](../../../../../.agents/web-study/design.md) | Intended colors, typography, accessibility and interaction rules. |

### Expected versus current discrepancies

| Topic | Expected / prototype | Current evidence | DD treatment |
|---|---|---|---|
| KPI cards | Active learners, completion rate, community interaction hours and satisfaction `/5.0`. | Generic catalog `Report.metrics[]`; #101/#102 Draft candidate metrics differ and are unapproved. | Do not map proposed API metrics or invent formulas/denominators. |
| Planned metric cards | DAU/MAU, Mentor interaction hours, employment-readiness rate and partner NPS. | Static explanatory copy says four items are being validated; no API/source metric maps them. | Treat as proposal copy only, not report output. |
| Segment | Prototype options `all`, `interns`, `graduates`, `alumni`. | #102 catalog permits free string; API DD only proposes `learning`/`community` grouping, marked DERIVED. | No mapping or normalization is approved. |
| Date | Prototype fixed values 2025-01-01 and 2025-03-31; Reset restores them. | #101 query types are `date`; #102 types are `string`; defaults, bounds and error mapping unresolved. | Do not treat static values as approved default period. |
| Apply/Refresh | Copy suggests filter application and server sync. | Apply only toggles opacity 300 ms; Refresh changes text/opacity for 900 ms. No request occurs. | No loading/success/freshness state is claimed. |
| Export | CTA names AD-25. Inventory expects current filters retained. | Prototype href `/admin/reports/export` has no query parameters. #103 row returns Report/202 but Operation tracking says Operation. | Preserve handoff gap; do not serialize filters or claim export acceptance. |
| Authorization | AC requires report/analytics permission; catalog says Admin. | No #101/#102 handler or policy source; generic shared ADMIN helper capability is not a wired route. | Keep policy unresolved; client badge is not an authorization check. |
| Visual design | Screenshot uses cobalt tokens and remote Plus Jakarta Sans. | Study Web guide requires ocean semantic tokens and Inter/system; remote font imports are prohibited by guide. | Preserve original screenshot and record implementation design discrepancy. |
