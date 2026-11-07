# AD-24 — Detailed Design Plan

## 1. Scope and order

- Screen: AD-24, “Báo cáo tác động cộng đồng” (inventory row 82).
- Scope: describe the static community-impact report screen, AC-38 flow, API catalog #101/#102, current absence of report endpoints in Study source, metric/date/segment discrepancies, and the filter handoff to AD-25.
- Boundary: AD-24 only. Do not define or implement report formulas, date defaults, segment mappings, API handlers, export serialization, or AD-25 behavior without an approved contract.
- Required order: source/contract review → this plan → marker map/overlay and annotated image → A–F DD → inventory/API reverse-index/global plan/worklog → static audit.
- No application tests or runtime verification are planned.

## 2. Evidence and source hashes

| Evidence | Use | Status |
|---|---|---|
| [`screen.png`](./screen.png), 1352×1600 | Original visual source; preserve unchanged. | Source asset |
| [`code.html`](./code.html), 270 lines | Prototype labels, controls, hard-coded defaults, local timers and anchors. | Static prototype only |
| [Inventory row 82](../../../list_screen.md) | Candidate route, #101/#102 links, expected states and AD-25 handoff. | Design requirement |
| [AC-38 diagram](../../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) | Expected #101 → #102 → validation/render flow and optional #103 export branch. | Expected flow; sequence needs clarification |
| [API catalog](../../../../../../docs/lists/list_api.md), #101–#103 and Operation tracking | Direct method/query/auth/response/error declarations and export response discrepancy. | Design catalog; not runtime by itself |
| [API #101 DD](../../../../../study-server/docs/dd/101_admin_reports_summary/00_Cover.md), [open questions](../../../../../study-server/docs/dd/101_admin_reports_summary/OPEN_QUESTIONS.md) | Summary contract boundary and unresolved metrics/date/permission/schema questions. | Draft only |
| [API #102 DD](../../../../../study-server/docs/dd/102_admin_reports_community_impact/00_Cover.md), [data mapping](../../../../../study-server/docs/dd/102_admin_reports_community_impact/05_Data_Mapping.md), [open questions](../../../../../study-server/docs/dd/102_admin_reports_community_impact/OPEN_QUESTIONS.md) | Community metric proposals, segment/date gaps and source/model discrepancies. | Draft; proposals are DERIVED |
| Study Server router, [auth helper](../../../../../study-server/app/utils/auth.py), [route index context](../../../../../../.agents/server-study/apis/declared-routes.md) | Recheck current API composition and distinguish shared Admin guard capability from absent report routes. | Current source/context; no #101/#102 route |
| [Legacy Study DDL](../../../../../../infra/postgres/study-server/DB.sql), [pilot DDL](../../../../../../infra/postgres/02_study_db.sql) | Candidate aggregate relations and separate pilot snapshot model. | Schema artifacts; live state unverified |
| [AD-01 DD](../AD-01_dashboard-quan-tri/AD-01.md), AD-25 inventory row | Keep #101 dashboard mapping and export navigation/filter handoff consistent. | Cross-screen design evidence |
| [Study Web design guide](../../../../../../.agents/web-study/design.md) | Intended visual, accessibility and interaction target. | Design target, not runtime evidence |

Original hashes captured before edits:

- `screen.png`: `180008eeca9721e0820ebfbf794de563b1636673ba447b5ab19cfa846d421332`
- `code.html`: `5f7cbd7214394be0c0f247b9ff8ae0e8cb28818a7a7518287fe499ed3a245656`

## 3. Expected flow and current boundary

- AC-38 expected sequence: Admin opens reporting dashboard → GET #101 summary → aggregate KPI summary → GET #102 community-impact → validate date range and report permission → aggregate learning/community metrics → render dashboard/filter → optional export decision. The view-only branch ends after rendering; the export branch calls #103.
- Catalog #101: `GET /api/v1/admin/reports/summary`, Bearer JWT/Admin, optional `from?:date`, `to?:date`, no body, `ApiEnvelope<Report>`, 200 `DESIGN_RESOURCE_RETRIEVED`, errors 401/403/500.
- Catalog #102: `GET /api/v1/admin/reports/community-impact`, Bearer JWT/Admin, optional `from?:string`, `to?:string`, `segment?:string`, no body, `ApiEnvelope<Report>`, 200 `DESIGN_RESOURCE_RETRIEVED`, errors 401/403/500.
- Both APIs are `Draft — Needs Confirmation`; no #101/#102 route/module/query/model/test source was found. #101/#102 date parameter types differ. Neither `Report` contract nor AC approves the mockup's card metrics or segment values.
- Current HTML defaults to `2025-01-01`, `2025-03-31`, segment `all`; its segment options are `all`, `interns`, `graduates`, `alumni`. Apply only changes opacity for 300 ms; reset writes those fixed values; refresh displays fake “Đang đồng bộ máy chủ...” for 900 ms; none of these actions calls a server or updates the URL.
- Current export anchor navigates to `/admin/reports/export` with no query state. Inventory expects filters to be retained for AD-25. API #103's row declares `ApiEnvelope<Report>`/202 while the catalog's Operation tracking paragraph says it returns `Operation`; do not invent filter serialization or poll behavior in AD-24.
- Existing API DDs propose other metrics and `learning`/`community` segment values only as `DERIVED`. The API #102 proposals use legacy enrollment/discussion candidate tables; the separate pilot `report_snapshots` model has no selected report code/writer/mapping. None establishes live schema or approved semantics.
- The Study Web page has no editable route/client source. The screenshot's remote Plus Jakarta Sans/cobalt styling differs from the Study Web guide's Inter/system and ocean tokens; preserve the source image and record the design discrepancy for implementation.

## 4. Plan for element coverage and annotation

Create 42 sequential markers, each mapped one-to-one to a row in `AD-24.md` §C. Coordinates below are circle centers in original 1352×1600 screenshot pixels. Render the annotation at 2× (2704×3200) without changing aspect ratio. Place circles on component edges or whitespace where possible; use identical IDs, labels and source-pixel coordinates in JSON and SVG.

| # | Planned component | Marker center (x,y) |
|---:|---|---:|
| 1 | Study2Work brand / portal mark | 16, 47 |
| 2 | Navigation: Tổng quan | 338, 50 |
| 3 | Navigation: Người dùng | 458, 50 |
| 4 | Navigation: Khóa học & Nội dung | 635, 50 |
| 5 | Navigation: Kiểm duyệt | 754, 50 |
| 6 | Navigation: Báo cáo | 860, 50 |
| 7 | System Normal status badge | 1048, 50 |
| 8 | Notifications bell | 1108, 50 |
| 9 | Admin identity / avatar | 1338, 49 |
| 10 | Global breadcrumb | 16, 80 |
| 11 | RBAC verification badge | 1336, 80 |
| 12 | Local report breadcrumb | 18, 142 |
| 13 | Screen ID badge: AD-24 | 20, 174 |
| 14 | Data-contract status badge | 441, 174 |
| 15 | Screen title | 16, 207 |
| 16 | Screen description | 854, 286 |
| 17 | Export-to-AD-25 CTA | 1334, 227 |
| 18 | From-date control | 357, 426 |
| 19 | To-date control | 693, 426 |
| 20 | Learner-segment select | 1028, 426 |
| 21 | Apply-filters button | 1229, 426 |
| 22 | Reset-filters button | 1274, 426 |
| 23 | Active-learners KPI card | 327, 660 |
| 24 | Completion-rate KPI card | 653, 660 |
| 25 | Community-interaction-hours KPI card | 977, 660 |
| 26 | Overall-satisfaction KPI card | 1302, 660 |
| 27 | Visualization / empty-chart panel | 1302, 720 |
| 28 | Empty-chart icon | 726, 838 |
| 29 | Empty-chart title | 910, 930 |
| 30 | Empty-chart explanatory copy | 1036, 1006 |
| 31 | Refresh-query button | 671, 1110 |
| 32 | Data-contract version badge | 872, 1110 |
| 33 | Planned-metrics section heading/icon | 440, 1252 |
| 34 | Planned-metrics validation-count badge | 1305, 1252 |
| 35 | DAU/MAU specification card | 654, 1362 |
| 36 | Mentor interaction-hours specification card | 1276, 1362 |
| 37 | Employment-readiness specification card | 654, 1470 |
| 38 | Partner NPS specification card | 1276, 1470 |
| 39 | Footer copyright | 380, 1557 |
| 40 | Footer privacy link | 940, 1557 |
| 41 | Footer RBAC standards link | 1151, 1557 |
| 42 | Footer support link | 1338, 1557 |

## 5. Event inventory to specify

| Event | Trigger | Planned treatment |
|---|---|---|
| EV-01 — Load report | Page entry / future `Load` | Record AC-38's #101 then #102 sequence and exact catalog requests separately; no current request exists. Do not supply a default range or metric mapping from the prototype. |
| EV-02 — Change date bounds | Native date input `change` | Current values are local input state only; #101 expects optional `date`, #102 optional `string`; date parsing, default, range validation and mapping are unresolved. |
| EV-03 — Change learner segment | Select `change` | Current options are `all/interns/graduates/alumni`; #102 catalog only says free-form string, Draft proposal says `learning/community`. No mapping is supported. |
| EV-04 — Apply filters | Button click | Current handler only toggles opacity for 300 ms. Inventory/AC expects report filter behavior, but request ordering, URL update, date conversion and segment mapping remain blocked. |
| EV-05 — Reset filters | Button click | Current handler restores two hard-coded 2025 date values and `all`; no API call or URL update. Do not substitute “today” defaults without approval. |
| EV-06 — Refresh query | Button click | Current handler changes label/opacity for 900 ms only. No request, polling or data refresh is wired. |
| EV-07 — Export report | Export anchor click | Current href is `/admin/reports/export` with no query; expected AD-25 handoff should preserve approved filters per inventory, but filter serialization and #103/Operation mapping are unresolved. |
| EV-08 — Shell and footer navigation | Anchor/button click | Main nav/footer use `#`; notification bell has no handler; no target route or UI runtime is wired. |

## 6. DD authoring and static verification

1. Write `AD-24.md` sections A–F with 42 element rows and EV-01…EV-08.
2. Separate expected AC/catalog flow, current static HTML behavior, Draft API-DD proposals, current server source absence, and candidate DB artifacts.
3. Explicitly show that the screenshot's four KPI cards and four proposed metric-description cards have no approved mapping to generic #101/#102 `Report.metrics[]`; leave placeholders/claims static.
4. Record #101 `date` vs #102 `string`, screen taxonomy vs Draft segment proposal, AC validation ordering, no source-backed report permission/endpoint, and AD-25 export-filter handoff gaps.
5. Create `AD-24_markers.json`, `AD-24_markers_overlay.svg`, and `screen_annotated.png` after this plan. Inspect the final image and move any marker that obscures meaningful copy.
6. Update inventory row 82 and API reverse-index #101/#102 with current evidence while retaining `D`; update the AD-24 global plan row/checkpoint. Do not edit AD-25 artifacts.
7. Static audit: IDs 1–42 sequential/unique/in-bounds and aligned across plan/JSON/SVG/DD; no marker overlap; all A–F/events present; local links resolve; JSON/SVG parse; annotation is 2704×3200; original hashes unchanged; inventory/folders remain 83/83; recalculate core artifacts; scoped `git diff --check`.

## 7. Known blockers to carry into the DD

- #101/#102 are catalog/Draft-only with no current Study route/module/query/model/test; no live report data source or report writer is established.
- KPI formulas, populations, units, ordering, empty/partial behavior, date defaults/timezone and invalid-range mapping are unresolved.
- #101 uses `date` while #102 uses `string`; the screenshot uses audience values that do not match #102's unapproved `learning`/`community` proposal.
- AC-38 places date/report-permission validation after the #102 request in its edge order; implementation timing needs clarification.
- AC role and report permission are expected, but no #101/#102 authorization is wired. Current shared ADMIN-capable helper is not evidence of report-specific route security.
- Candidate legacy tables and pilot snapshots do not prove live schema, metric feasibility or consistency; AC-19 Comment persistence differs from the legacy discussion self-reference.
- Export link drops filters; #103 `Report` response conflicts with Operation tracking and the AD-25/operation poll design.
- Study Web is UNWIRED; the prototype also differs from the intended Study Web design tokens/typography.
