# AD-25 — Detailed Design Plan

## 1. Scope and sequence

- Screen: AD-25, “Xuất báo cáo và theo dõi tiến trình” (inventory row 83).
- Scope: document this static export-manager prototype, its optional AC-38 export branch, API #103 and conditional SH-07/API #18 handoff. Do not author AD-24 or SH-07 in this session.
- Required order: inspect sources/contracts → save this plan → marker JSON/SVG and annotated image → A–F AD-25 DD → inventory/reverse-index/global-plan/worklog updates → static audit.
- Boundary: no export filter serialization, unsupported format behavior, API response selection, operation ID coercion, polling cadence, file URL/TTL, audit event, cleanup, queue/worker, or authorization policy is to be invented. Catalog/API DD open questions remain blockers.
- No application tests or runtime verification are planned; this is a screen DD task and local UI/API implementation is absent.

## 2. Evidence register and original assets

| Evidence | Use | Status |
|---|---|---|
| [`screen.png`](./screen.png), 1368×1600 | Original visual; retain unchanged. | Design asset |
| [`code.html`](./code.html), 27,722 bytes | Labels, selected controls, disabled button, `onsubmit` behavior, inert links and static policy claims. | Static prototype only |
| [Inventory row 83](../../../list_screen.md) and AD-24 row 82 | Candidate route, #103/#18, progress states, filter handoff and neighbor links. | Expected screen requirements |
| [AC-38 diagram](../../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio), [AC/API index](../../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) | Admin/report precondition, optional export decision, #103, generation, temporary storage and display/download. The diagram's #18 node is present without a connecting edge in this AC page. | Expected flow; edge is unresolved |
| [API catalog](../../../../../../docs/lists/list_api.md), #103/#18, reusable schemas and Operation tracking | Declared method, query, role, response/error codes, Operation/ExportAsset schemas and ID convention. | Design catalog; contradictory response/ID details |
| [API #103 DD](../../../../../study-server/docs/dd/103_admin_reports_community_impact_export/00_Cover.md), [request](../../../../../study-server/docs/dd/103_admin_reports_community_impact_export/03_Request.md), [response](../../../../../study-server/docs/dd/103_admin_reports_community_impact_export/04_Response.md), [mapping](../../../../../study-server/docs/dd/103_admin_reports_community_impact_export/05_Data_Mapping.md), [open questions](../../../../../study-server/docs/dd/103_admin_reports_community_impact_export/OPEN_QUESTIONS.md) | Keeps Report/Operation conflict, GET acceptance, filters/format, retries, storage, authorization and report consistency decisions open. | Draft only |
| [API #18 DD](../../../../../study-server/docs/dd/18_operations/00_Cover.md), [overview](../../../../../study-server/docs/dd/18_operations/02_Overview.md), [open questions](../../../../../study-server/docs/dd/18_operations/OPEN_QUESTIONS.md) | Operation ID, owner rule, lifecycle/status/result/persistence gaps. | Draft only |
| [Study Server router](../../../../../study-server/app/api/v1.py), [auth helper](../../../../../study-server/app/utils/auth.py), [route context](../../../../../../.agents/server-study/apis/declared-routes.md) | Current endpoint composition and shared Admin-capable guard boundary. | Source through #98; no #103/#18 route |
| [Legacy Study DDL](../../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../../infra/postgres/02_study_db.sql) | Check possible operation/file/report candidates without assigning an unapproved mapping. | Candidate schema artifacts; live DB not verified |
| [AD-24 DD](../AD-24_bao-cao-tac-dong-cong-dong/AD-24.md), [SH-07 inventory row](../../../list_screen.md) | Filter-state handoff, conditional Operation ID and neighbor routes. | Cross-screen requirement with unresolved mapping |
| [Study Web design guide](../../../../../../.agents/web-study/design.md) | Intended tokens, responsive layout, control/focus and accessibility behavior. | Design target, not runtime evidence |

Original hashes recorded before authoring:

- `screen.png`: `5d90eabc1fcf154433771d58b91e814e6fc6a40e89933ffac9c5b0f35522b722`
- `code.html`: `0cd68b7aba2052a35cf89289241cf125c64ca1c1cce9e23d5d0187c276a861be`

## 3. Expected behavior and current boundary

- Inventory/AC-38 expected flow: Admin with report/analytics access chooses an export branch; #103 is `GET /api/v1/admin/reports/community-impact/export` with optional `filters:string`, `format:string`, Bearer JWT/Admin, HTTP 202 `DESIGN_OPERATION_ACCEPTED`, and catalog errors 401/403/503/500. AC-38 describes generating CSV/XLSX/PDF or a job, temporary server storage if applicable, and displaying a report/download result.
- Contract discrepancy: the #103 endpoint row says HTTP 202 `ApiEnvelope<Report>`; the same catalog's Operation-tracking paragraph says #103 returns `Operation`. API #103 DD preserves both as direct declarations. Do not select one.
- Conditional polling: inventory expects #18 only if a confirmed `operation_id` is supplied. API #18 row takes `int64`; reusable `Operation.id` and AC diagrams use UUID. The row/AC diagram say owner-only while Operation tracking says owner/Admin. `OperationStatus`, storage, lifecycle, per-kind result and export artifact mapping are unresolved. AC-38 has an `operation_status` node but no edge connects it to its export path.
- Current prototype: selected format is `csv`; `scope_course` and `scope_learner` are checked; `scope_impact` is not; `time_range=month` is selected, with `week` and `custom` alternatives and a static GMT+7 note. There are no custom date controls or approved mappings from these names to `filters:string`.
- `onsubmit="event.preventDefault();"` cancels the only form submission; no handler/API call updates the progress panel. The download button is disabled. The SH-07 banner and back anchor are not wired. All progress/worker/security/retention statements are static copy.
- Study Web has no tracked editable `src`, router, package manifest or client. Current Study Server has no #103/#18 route/module/query/model/test, export worker, or download-serving source. The current Admin router composes through #98. Pilot `file_objects`, `report_snapshots` and `evidence_export_requests` are distinct design artifacts and do not prove AC-38 export persistence or live schema.

## 4. Element marker plan

Coordinates are marker centers in source `screen.png` pixels. Use blue, high-contrast circles with white fill at 2× output. Keep markers at margins/blank card edges so labels and controls remain readable.

| # / planned label | Center (x, y) | Target |
|---|---:|---|
| 1 — Study2Work brand / portal mark | 14, 52 | Header brand |
| 2 — Main navigation group | 560, 52 | Header nav links |
| 3 — System Normal badge | 1010, 52 | Static system badge |
| 4 — Notifications button | 1100, 52 | Bell button |
| 5 — Admin identity/avatar | 1353, 52 | Header identity |
| 6 — Global breadcrumb | 14, 94 | Header breadcrumb |
| 7 — RBAC verification badge | 1353, 120 | Static RBAC label |
| 8 — Local report breadcrumb | 380, 150 | Report/export breadcrumb |
| 9 — Screen ID badge | 14, 171 | AD-25 identifier |
| 10 — Back-to-AD-24 anchor | 1353, 175 | Inert return link |
| 11 — Page title | 800, 257 | H1 |
| 12 — Page description | 870, 305 | Supporting copy |
| 13 — Worker-node badge | 1353, 295 | Static worker claim |
| 14 — Export security policy banner | 48, 482 | Banner icon/title/copy |
| 15 — RBAC L3 badge | 575, 346 | Static policy-level badge |
| 16 — Export configuration panel title | 510, 553 | Left panel heading |
| 17 — Step 1/2 badge | 760, 553 | Static progress label |
| 18 — Format section heading/help | 760, 645 | Format selector section |
| 19 — CSV format option | 268, 721 | Selected radio card |
| 20 — Excel/XLSX format option | 501, 721 | Radio card |
| 21 — PDF format option | 733, 721 | Radio card |
| 22 — Dataset scope section heading/help | 760, 777 | Scope section |
| 23 — Course summary scope | 80, 852 | Selected checkbox row |
| 24 — Learner progress scope | 80, 933 | Selected checkbox row |
| 25 — Community impact scope | 80, 1010 | Unselected checkbox row |
| 26 — Time-range section heading/timezone | 760, 1067 | Period selector section |
| 27 — Current week option | 268, 1114 | Radio card |
| 28 — Current month option | 500, 1114 | Selected radio card |
| 29 — Custom period option | 732, 1114 | Radio card; no custom date control shown |
| 30 — Processing-time note | 441, 1229 | Static informational note |
| 31 — Start export task button | 760, 1229 | Submit button |
| 32 — Progress panel heading | 1308, 584 | Right panel heading |
| 33 — Monitor V2 badge | 1318, 553 | Static monitor label |
| 34 — Operation ID card | 1050, 720 | No-ID placeholder and claim |
| 35 — Operation status card | 1290, 720 | Static ready-to-start state |
| 36 — Empty download-result panel | 1289, 1061 | Empty icon/title/copy |
| 37 — Disabled download button | 1180, 1058 | Disabled control |
| 38 — SH-07 queue handoff callout | 1290, 1214 | Static conditional handoff |
| 39 — Export policy section heading | 503, 1324 | Lower section heading |
| 40 — Signed-link policy card | 448, 1460 | Static “120 minutes” claim |
| 41 — Audit-log policy card | 868, 1460 | Static audit/IP/session claim |
| 42 — Temporary-file deletion policy card | 1288, 1460 | Static 24-hour cleanup claim |
| 43 — Footer copyright | 14, 1551 | Static footer text |
| 44 — Privacy-policy footer link | 776, 1535 | Inert anchor |
| 45 — RBAC-standards footer link | 982, 1535 | Inert anchor |
| 46 — System-support footer link | 1210, 1535 | Inert anchor |

## 5. Event inventory

| Event | Trigger | Current behavior | Expected contract boundary / unresolved items |
|---|---|---|---|
| EV-01 Initial display | Page `Load` | HTML renders fixed controls, no-operation state and static policy copy; no data request. | Route, Admin/report guard and query-state initialization depend on absent Study Web source. |
| EV-02 Choose format | #19–#21 radio `change` | Native local radio selection only; default is lowercase `csv`. | #103 only says `format?:string`; values/casing/default/MIME are not approved. |
| EV-03 Choose report scope | #23–#25 checkbox `change` | Native local checkbox state only; two scopes initially checked. | #103 only says `filters?:string`; filter structure and scope vocabulary have no mapping. |
| EV-04 Choose period | #27–#29 radio `change` | Native local selection only; `month` selected; GMT+7 is static and `custom` has no date controls. | #102 date/segment semantics and #103 filters serialization are unresolved; do not add a date range. |
| EV-05 Start export | #31 form `submit` | Inline handler prevents default and performs no action; no API call or state change. | #103 has GET/202, Report-versus-Operation response conflict, no idempotency/retry or durable acceptance contract. |
| EV-06 Download artifact | #37 `click` | Button has `disabled` and `aria-disabled=true`; no URL/href/download handler. | Requires approved Operation result/ExportAsset, authorization, URL expiry and file-serving contract. |
| EV-07 Open SH-07 | #38 conditional callout | Informational panel only; no anchor/button or operation ID. | Inventory says #18 only with a BE-confirmed ID; ID type/auth/lifecycle unresolved and AC-38 has no #18 edge. |
| EV-08 Return to AD-24 | #10 anchor `click` | `href="#"`; does not navigate to AD-24 or preserve filters. | Inventory expects AD-24/AD-25 relation; filter URL serialization is not defined. |
| EV-09 Shell and footer navigation | #2, #4, #6, #8, #44–#46 | Anchors use `#`; notification button has no listener. | Destinations and profile/system feeds are not defined by this screen's API contract. |

## 6. Source trace and blockers to carry into DD

```text
Expected: AD-24 may open AD-25 → GET #103 with filters/format → 202 acceptance → optionally poll #18 if an approved operation ID exists → display/download only an approved completed artifact → return to reporting flow.
Current: no Study Web caller/route/client, #103 handler/worker, #18 route/store/query, or download-serving source. Local HTML controls only change browser state; submit is prevented, download is disabled, and navigation/handoff links do not resolve.
```

- `#103`: response `Report` versus `Operation`; GET side-effect/retry semantics; query serialization and validation; allowed/default format; report-permission source; durable queue acceptance; worker failure; export asset/result; storage/download authorization and expiry; relation to approved #102 metric/filter logic.
- `#18`: `operation_id` int64 versus UUID; owner-only versus owner/Admin; Study storage/query, status enum/lifecycle/terminal state, retention, per-kind result and error semantics.
- AC-38 includes a poll node not connected to the export flow; inventory and mockup imply a conditional SH-07 handoff. Obtain an approved edge/sequence before specifying client polling/navigation.
- Study DB artifacts are candidates only: pilot `file_objects` has generic purpose and URL rules, `report_snapshots` stores report metrics, and `evidence_export_requests` records a distinct signed evidence export. None is an approved AD-25 export-job mapping; live schema/deployment is unverified.
- Mockup claims about Celery/Worker Node 04, RBAC L3, SHA-256 checksum, 120-minute links, audit log/IP/session, browser cache, and 24-hour deletion are static and unsupported by current Study implementation. Preserve them as unresolved design copy, not runtime behavior.
- Study Web design discrepancy: screenshot uses cobalt tokens/Plus Jakarta Sans and a remote Tailwind CDN; the canonical guide uses ocean semantic tokens and Inter/system fonts without remote font imports. Preserve the screenshot; document the design gap.

## 7. Completion and status criteria

- Create marker JSON/overlay/annotated PNG from the exact coordinates above, then visually inspect the final image and adjust the plan first if any marker obscures content.
- Write A–F DD with one row per marker, detailed EV-01…EV-09 behavior/API boundaries, state/navigation matrix, source register and explicit blockers.
- Do not upgrade #103 or #18 from D; do not claim Study Web, API, export, poll or runtime behavior is implemented.
- Planned outcome: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED` until response, ID, permission, filters, storage and flow contracts are approved and code exists.
