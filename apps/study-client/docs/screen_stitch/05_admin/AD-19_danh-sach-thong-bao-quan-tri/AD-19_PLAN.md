# AD-19 — Kế hoạch đặc tả danh sách thông báo quản trị

## Mục tiêu và phạm vi

Hoàn thiện riêng AD-19 theo inventory row 77, AC-36 và API #92. Giữ nguyên ảnh nguồn và HTML; ghi rõ expected/current; lập marker map trước khi tạo annotation/DD; mô tả điều kiện gọi #92 và các hành vi prototype chỉ là mockup. Không xử lý AD-20 hay AD-21.

| Thuộc tính | Expected / nguồn thiết kế | Current evidence |
|---|---|---|
| Actor / quyền | AC-36: Admin có notification-management permission. | Local #92 gọi shared guard role ADMIN; fine-grained permission và visibility scope chưa có contract. |
| Route / handoff | Inventory candidate /admin/notifications; mở AD-20 để soạn và AD-21 để sửa/trạng thái. | Study Web không có editable source/router/API client. CTA trong HTML trỏ /admin/notifications/create, khác AD-20 /admin/notifications/new. |
| List API | Catalog #92: GET /api/v1/admin/notifications, Bearer/Admin; status?, channel?, page?; direct ApiEnvelope<Notification>; 200, 401, 403, 503, 500. AC-36 n2 gọi #92 rồi query notifications. | Local route wired; raw filter exact-match, page default 1, positive int32, fixed page size 20, sort created_at DESC/id DESC. Local result là ApiEnvelope<Page<Notification>> (DERIVED/discrepant), không phải direct singleton catalog response. |
| Item model | Reusable catalog Notification: id, title, content, channels, status, optional read_at/scheduled_at, created_at. | Legacy BIGINT notification + delivery aggregate; only rows with at least one delivery. Local channels EMAIL/PUSH; statuses QUEUED/FAILED/SENT; response omits read_at/scheduled_at. Does not expose recipient or scheduled send time. |
| Search / filters | Inventory requests title search and draft/scheduled/sent list, with status/channel controls. | Catalog has no search; local source only exact status/channel strings and does not normalize. Prototype offers channel app/email/system and status draft/scheduled/published. These values are not mapped to catalog/local enums. |
| Metrics / table | Prototype shows total/published/scheduled/drafts, recipient, send time. | #92 returns a paged item projection only; no metrics API and no recipient/send-time fields. Do not derive counts from current page. |
| UI events | Inventory states loading/empty/ready/error; AC-36 reloads management after create/update/delete/status branches. | HTML has no fetch/XHR. Reset only clears controls; refresh only animates for 800 ms; pagination buttons disabled; static empty-state copy. |
| Runtime | — | DD can document candidate behavior and blockers; Study Web route, live DB/migration, permissions and production behavior remain unverified. |

## Source review and order

1. Inventory row 77, API reverse index #092 and G-12 in apps/study-client/docs/list_screen.md; global AD-19 row and 71/83 checkpoint in dd_screens/PLAN.md.
2. AC-36 admin management diagram and direct API catalog row #92 in docs/lists/list_api.md.
3. API #92 Draft DD, open questions and AC-36 macro-review; preserve owner-confirmation status.
4. Current implementation trace: apps/study-server/app/api/v1.py → api_92_admin_notifications_list/validate.py → query.py/models.py → view.py; check focused test source, not run it.
5. Checked-in legacy DDL and migration 009 only as schema candidates; keep V1-PILOT UUID model separate.
6. Inspect current Study Web tree, exact HTML handlers/links and source screenshot; compare only to .agents/web-study/design.md for design rules.
7. Source review is recorded in the active worklog. This plan must be saved before creating marker JSON/SVG, annotated PNG or AD-19.md.

## Sơ đồ vùng và marker map

Source coordinate space: 1600×1411 pixels, origin top-left. Each number identifies one visible component/field/control group. Shell nav entries and the seven table columns receive distinct markers; repeated decorative glyphs inside a component do not become separate elements. Place badges at the planned coordinates in the low-content edge/padding of each component; for compact controls, place the badge just above the control border so its label remains readable. Annotated output is planned at 2× (3200×2822).

| # | Element / region | Planned marker point (x,y) |
|---:|---|---:|
| 1 | Brand / LMS header | 12,65 |
| 2 | Shell navigation — Tổng quan | 356,65 |
| 3 | Shell navigation — Người dùng | 491,65 |
| 4 | Shell navigation — Khóa học & Nội dung | 660,65 |
| 5 | Shell navigation — Kiểm duyệt | 856,65 |
| 6 | Shell navigation — Báo cáo | 982,65 |
| 7 | System Normal status copy | 1154,65 |
| 8 | Header notifications icon | 1281,65 |
| 9 | Admin identity/avatar | 1460,65 |
| 10 | Global breadcrumb | 20,110 |
| 11 | RBAC assurance badge/copy | 1580,110 |
| 12 | Local breadcrumb | 390,151 |
| 13 | Screen title | 720,174 |
| 14 | Screen description | 872,266 |
| 15 | Create notification CTA (AD-20 candidate) | 1543,194 |
| 16 | Metric card — total notifications | 392,301 |
| 17 | Metric card — published | 777,301 |
| 18 | Metric card — scheduled | 1162,301 |
| 19 | Metric card — draft | 1545,301 |
| 20 | Search title input | 879,489 |
| 21 | Channel select | 925,459 |
| 22 | Status select | 1198,459 |
| 23 | Reset filters button | 1421,459 |
| 24 | Table column — notification ID | 78,568 |
| 25 | Table column — title | 270,568 |
| 26 | Table column — recipient | 610,568 |
| 27 | Table column — delivery channel | 858,568 |
| 28 | Table column — send time | 1076,568 |
| 29 | Table column — status | 1282,568 |
| 30 | Table column — actions | 1485,568 |
| 31 | Empty-state illustration | 861,724 |
| 32 | Empty-state title | 555,837 |
| 33 | Empty-state explanatory copy | 1086,875 |
| 34 | Refresh list button | 633,965 |
| 35 | Result count summary | 291,1110 |
| 36 | Pagination — first page | 1277,1114 |
| 37 | Pagination — previous page | 1329,1114 |
| 38 | Pagination — current/total display | 1394,1114 |
| 39 | Pagination — next page | 1456,1114 |
| 40 | Pagination — last page | 1508,1114 |
| 41 | Policy banner information icon | 74,1234 |
| 42 | Policy banner title | 567,1234 |
| 43 | Policy banner description | 1189,1234 |
| 44 | Policy / guideline link | 1532,1234 |
| 45 | Footer copyright/system label | 64,1352 |
| 46 | Footer privacy link | 1020,1352 |
| 47 | Footer RBAC standards link | 1221,1352 |
| 48 | Footer technical support link | 1430,1352 |

## Event và dữ liệu cần đặc tả trong DD

1. EV-01 — Initial load: candidate route requires an authenticated Admin; call GET #92 only after contract mapping/permission is approved. Direct catalog has no page metadata; do not assume local Page is the approved client contract. Document exact request and separate the 200 direct-catalog response from current local Page projection.
2. EV-02 — Search title: user text is local HTML input only; no catalog query parameter or listener exists. Do not send a guessed query. Search behavior is blocked pending API/owner contract.
3. EV-03 — Change channel/status: prototype values are app/email/system and draft/scheduled/published; local accepted source values are EMAIL/PUSH and FAILED/QUEUED/SENT with raw exact-match. No safe translation. Keep controls as static/unwired until enum and mapping are approved.
4. EV-04 — Reset filters: current handler clears input/selects without calling API. If implemented later, reset semantics, default page and fetch trigger require an approved client rule.
5. EV-05 — Refresh: current handler only disables/spins for 800 ms then restores the icon; no request. A future reload is conditional on #92 response/permission contract.
6. EV-06 — Create CTA: HTML path /admin/notifications/create conflicts with inventory AD-20 /admin/notifications/new; neither is a wired Study Web route. Do not claim navigation works.
7. EV-07 — Open row/action: screenshot is empty and HTML supplies no row handler. Inventory links AD-21, whose route needs a positive int64 notification ID; #92 local response supplies id, but #96/local detail mapping is not confirmed. No inferred row action.
8. EV-08 — Pagination: visual controls are disabled in HTML. Catalog page query has no size/metadata contract; local Page uses page 1+, size 20. Do not make controls actionable until Page/empty/out-of-range semantics are approved.
9. EV-09 — Policy link: href /admin/guidelines/notifications has no inventory row or router target; target and 30-minute review policy are unsupported by #92/AC-36.
10. EV-10 — Shell/footer links and notification icon: anchors are # or have no handler. Static shell copy is not evidence of health, authorization, audit, or navigation state.

## Blocker cần giữ mở

- Catalog #92 says ApiEnvelope<Notification>; local source returns Page<Notification>. API DD remains Draft — Needs Confirmation.
- Direct catalog omits search, metric, page-size/metadata and enum values. UI values do not match local status/channel source.
- AC-36 notification-management permission vs local ADMIN guard; global/tenant/sender visibility and Admin notification grain are unresolved.
- Legacy recipient-oriented model/outbox is only a checked-in candidate; live DB/migration deployment and campaign model are unverified. Draft/scheduled items without delivery rows are excluded by current query.
- No mapping exists for recipient, send time, total/published/scheduled/draft metrics.
- AD-20 CTA path differs from inventory. Guidelines path and shell/footer targets are not in inventory/source.
- #93 Operation correlation is unresolved; do not infer it into AD-19. AD-21 detail/status action depends on unresolved item/route contract.
- Study Web has no editable source, route or API client; screenshot style also needs review against the Study Web design guide.

## Acceptance audit to perform

- [x] Keep source screen.png and code.html hashes unchanged.
- [x] Create sequential unique markers with in-bounds coordinates and one row per marker.
- [x] Ensure JSON, SVG and DD coordinates agree; annotated PNG is 3200×2822 and visually reviewed.
- [x] Complete DD sections A–F with ordered event flows, exact catalog contract, separate local-source behavior and blockers.
- [x] Validate all relative links and element/event IDs; verify inventory/folder count remains 83/83 and core artifact count advances 71/83 → 72/83.
- [x] Update inventory row 77, reverse #092, G-12 and global plan/checkpoint; do not edit AD-20/AD-21 screen files.
- [x] Run static artifact checks and git diff --check; no application tests/runtime in this documentation turn.
