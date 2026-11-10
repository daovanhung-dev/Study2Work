# AD-22 — Detailed Design Plan

## 1. Scope and order

- Screen: AD-22, “Danh sách thảo luận bị báo cáo” (inventory row 80).
- Primary work: document the reported-discussion queue, prototype interactions, direct API #97 contract, current local #97 behavior, and AD-23/#98 handoff.
- Scope boundary: AD-22 only. #99 moderation and #100 delete remain AD-23/API work; do not define their UI here.
- Required order: source and contract review → this plan → marker map/overlay and annotated image → A–F screen DD → inventory/API reverse index/global plan → static audit.
- No application tests or runtime verification are planned.

## 2. Evidence and source hashes

| Evidence | Use | Status |
|---|---|---|
| [`screen.png`](./screen.png), 1280×1148 | Original visual source; keep unchanged. | Source asset |
| [`code.html`](./code.html), 261 lines | Prototype DOM and event inventory. | Static prototype only |
| Inventory row 80 in [`list_screen.md`](../../../list_screen.md) | Candidate route, AC/API links, expected states and blocker. | Design requirement |
| AC-37 in [`AC_04_ADMIN_MANAGEMENT.drawio`](../../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) | Queue → #97 → read report/thread → #98 handoff and later moderation flow. | Expected flow |
| [`list_api.md`](../../../../../../docs/lists/list_api.md), #97/#98 | Direct API contract. | Catalog contract |
| Study Server router and `api_97_admin_discussions_reported` module | Local authentication, validation, query, projection, errors and side effects. | Current source; some choices are DERIVED |
| #97 `OPEN_QUESTIONS.md` and #98 DD/source | Report writer/live schema and report-field/detail gaps. | Open contract questions / discrepancy |
| [web-study design](../../../../../../.agents/web-study/design.md) | Shared visual/accessibility guidance. | Design convention; prototype is not silently restyled |

Original hashes captured before changes:

- `screen.png`: `5f53d5edfae7390b49259cbb7896447ebbfa3ef6bd4ac742ba325870b9d2d303`
- `code.html`: `043318fa9b192bc31d70652c3152d5e73b25971085d581d4cce174f198909980`

## 3. Plan for element coverage and annotation

Create 48 sequential markers, each mapped to one row in `AD-22.md` §C. Coordinates below are circle centers in original 1280×1148 screenshot pixels. Place markers at component edges, whitespace, or lower header strips to keep meaningful copy readable; render the annotation at 2× (2560×2296), retaining original aspect ratio. Record identical IDs and source-coordinate centers in JSON and SVG.

| # | Planned component | Marker center (x,y) |
|---:|---|---:|
| 1 | Study2Work brand / portal mark | 12, 28 |
| 2 | Navigation: Tổng quan | 239, 28 |
| 3 | Navigation: Người dùng | 345, 28 |
| 4 | Navigation: Khóa học & Nội dung | 454, 28 |
| 5 | Navigation: Kiểm duyệt | 632, 28 |
| 6 | Navigation: Báo cáo | 753, 28 |
| 7 | System Normal badge | 848, 28 |
| 8 | Notifications bell | 1007, 28 |
| 9 | Admin identity/avatar | 1071, 28 |
| 10 | Global breadcrumb | 12, 75 |
| 11 | RBAC verification badge | 1096, 75 |
| 12 | Local moderation breadcrumb | 18, 136 |
| 13 | Page title | 18, 176 |
| 14 | “SẠCH VI PHẠM” badge | 846, 174 |
| 15 | Supporting description | 18, 222 |
| 16 | Outstanding queue metric | 961, 188 |
| 17 | Approved in 24h metric | 1103, 188 |
| 18 | Search input | 48, 272 |
| 19 | Severity filter | 548, 272 |
| 20 | Reason filter | 728, 272 |
| 21 | Status filter | 952, 272 |
| 22 | Toolbar refresh button | 1120, 272 |
| 23 | Table column: Discussion ID | 46, 354 |
| 24 | Table column: Topic title | 179, 354 |
| 25 | Table column: Creator | 452, 354 |
| 26 | Table column: Report count | 625, 354 |
| 27 | Table column: Flag reason | 770, 354 |
| 28 | Table column: Reported time | 944, 354 |
| 29 | Table column: Action | 1160, 354 |
| 30 | Empty-state shield icon | 702, 550 |
| 31 | Empty-state title | 900, 626 |
| 32 | Empty-state explanatory copy | 900, 680 |
| 33 | Empty-state refresh button | 778, 740 |
| 34 | Static “60 giây” analysis claim | 810, 793 |
| 35 | Pagination result summary | 300, 908 |
| 36 | Current page summary | 370, 908 |
| 37 | First-page control | 880, 878 |
| 38 | Previous-page control | 972, 878 |
| 39 | Current page button | 1042, 878 |
| 40 | Next-page control | 1096, 878 |
| 41 | Last-page control | 1188, 878 |
| 42 | Strict-processing policy card | 200, 943 |
| 43 | Response-SLA policy card | 640, 943 |
| 44 | Audit-trail policy card | 1080, 943 |
| 45 | Footer copyright text | 250, 1080 |
| 46 | Footer privacy link | 786, 1080 |
| 47 | Footer RBAC link | 954, 1080 |
| 48 | Footer support link | 1160, 1080 |

## 4. Event inventory to specify

| Event | Trigger | Planned treatment |
|---|---|---|
| EV-01 — Initial queue load | Screen entry / future `Load` | Describe expected #97 request separately from current static render; no invented retry, cache, timeout or polling policy. |
| EV-02 — Search | Search input | No HTML handler; API #97 has no `q`; document as unsupported pending contract. |
| EV-03 — Severity filter | Select change | API accepts a free-form string; current local source exact-matches it. Prototype options are not an approved taxonomy. |
| EV-04 — Reason filter | Select change | API accepts a free-form string; current local source exact-matches it. Prototype options are not an approved taxonomy. |
| EV-05 — Status filter | Select change | API #97 has no status parameter; current local query includes OPEN/IN_REVIEW only. |
| EV-06 — Toolbar refresh | Button click | Current handler only animates icon 700 ms; no fetch. |
| EV-07 — Empty-state refresh | Button click | Same local animation; no fetch. |
| EV-08 — Pagination | Pagination control | Controls are disabled; API only exposes page. Current local page size is DERIVED 20; no client page transition exists. |
| EV-09 — Open discussion | Hypothetical non-empty row selection | Inventory/AC route to AD-23/#98 using Discussion ID. No visible row/action exists in prototype; do not invent report ID or detail behavior. |
| EV-10 — Shell, bell and footer navigation | Anchor/button click | Anchors use `#`; bell has no handler. No current route transition. |

## 5. DD authoring and static verification

1. Write `AD-22.md` sections A–F with 48 element rows and EV-01…EV-10.
2. Separate expected AC/catalog behavior, prototype behavior, current Study Server source, and unresolved assumptions.
3. Record #97's direct catalog response/errors separately from local DERIVED page/filter/order/422 details; identify missing report fields and writer/live-schema gates.
4. Record #98 ID handoff as technically type-compatible (`int64`) but report details as unavailable in current response/source. Keep #99/#100 outside this screen.
5. Create `AD-22_markers.json`, `AD-22_markers_overlay.svg`, and `screen_annotated.png` after this plan. Review annotation visually and move any marker that obscures meaningful copy.
6. Update inventory row 80 and API reverse-index row #097 from D to R, keeping #97 DD Draft and AD-22 DD blocked. Append the global progress checkpoint; do not start AD-23.
7. Static audit: sequential/unique IDs 1–48; in-bounds coordinates; coordinate agreement across JSON/SVG/DD; all A–F sections and events; relative links resolve; annotated dimensions 2560×2296; source image/HTML hashes unchanged; inventory/folders 83/83; core artifacts 75/83; `git diff --check`.

## 6. Known blockers to carry into the DD

- No approved/current Student report-write endpoint or writer found; candidate `discussion_reports` DDL/migration and live deployment are unverified.
- Catalog #97 response and current local projection do not supply report count/reason/severity/reporter/time needed by the screenshot/AC summary.
- Search, status filtering, pending-priority order, displayed metrics, and the claimed 60-second analysis interval are not defined by #97/current prototype behavior.
- Local `ADMIN` guard does not prove AC-37's Admin permission/tenant policy.
- Current #98 source/DD conflict and report detail is not read by current #98 source; #99/#100 are outside the source-backed runtime boundary.
- Study Web editable route/API client is absent. No runtime state or production data can be claimed.
