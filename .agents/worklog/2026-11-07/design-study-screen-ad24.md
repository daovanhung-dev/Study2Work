---
task_id: "2026-11-07-design-study-screen-ad24"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-38; APIs #101–#102; AD-23 → AD-24 → AD-25 community impact report and export"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-24

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 229; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Preserve expected/current behavior; trace direct contract and source; do not infer KPI mapping or default date range; keep API #101 runtime absent, Admin permission unresolved and Study Web UNWIRED.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Preserve original source assets; no canonical skill exists for web UI-only DD; don't claim tests/runtime/live schema from docs or mockups; keep API source/DD and permission discrepancies explicit.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Distinguish API catalog, AC, local server source and static prototype; do not infer identity, policy, status or data mapping from screenshots; keep UI-only DD skill status and Study Web UNWIRED explicit.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-24 only; inspect current assets, inventory, AC-38, APIs #101/#102 and current source; write `AD-24_PLAN.md` before markers, annotation or DD; preserve original assets; create ordered unique markers and annotated PNG; author A–F DD with traceable elements/events/APIs/states/navigation; update `list_screen.md`, `dd_screens/PLAN.md` and this worklog; distinguish DD readiness, implementation block and runtime verification.
- Inventory row 82: AD-24 “Báo cáo tác động cộng đồng”, candidate `/admin/reports/community-impact`, AC-38, #101/#102; date range, segment, KPI and chart; GET #101 summary and GET #102 by `from/to/segment`; keep filters in URL for export; link AD-25; expected `loading/no-data/partial/ready`; P2; definitions of report metrics unresolved.
- AC-38: Admin must have report/analytics permission. Expected sequence is open dashboard → GET #101 summary → GET #102 community impact → validate range/report permission → aggregate and render dashboard/filter; optional export branch uses #103; view-only ends without export. Diagram order places validation after #102 and needs a sequencing decision.
- Catalog #101: GET `/api/v1/admin/reports/summary`, Bearer JWT/Admin, optional `from?:date`, `to?:date`, no body, `ApiEnvelope<Report>`, 200 `DESIGN_RESOURCE_RETRIEVED`, errors 401/403/500.
- Catalog #102: GET `/api/v1/admin/reports/community-impact`, Bearer JWT/Admin, optional `from?:string`, `to?:string`, `segment?:string`, no body, `ApiEnvelope<Report>`, 200 `DESIGN_RESOURCE_RETRIEVED`, errors 401/403/500. #101 and #102 date types conflict.
- Both API DDs are Draft and runtime `UNWIRED / NOT_FOUND`. Report keys/formulas/populations/date defaults/timezone/empty semantics and report permission remain open. #102 `learning`/`community` segments and legacy-table aggregate metrics are explicitly DERIVED proposals, not approved mappings.

## CURRENT_BEHAVIOR

- Initial target folder: `apps/study-client/docs/screen_stitch/05_admin/AD-24_bao-cao-tac-dong-cong-dong/` contains only `screen.png` and `code.html`; no plan, DD, marker map or annotation yet.
- Original `screen.png`: 1352×1600 sRGB; SHA-256 `180008eeca9721e0820ebfbf794de563b1636673ba447b5ab19cfa846d421332`.
- Original `code.html`: 25,048 bytes; SHA-256 `5f7cbd7214394be0c0f247b9ff8ae0e8cb28818a7a7518287fe499ed3a245656`.
- Initial trackers: inventory row 82 D; global AD-24 D / `CHƯA_BẮT_ĐẦU`; API reverse-index rows #101/#102 D.
- Prototype `code.html` has date inputs `2025-01-01`/`2025-03-31`, select values `all`, `interns`, `graduates`, `alumni`, Apply/Reset, four `--` KPI cards, an empty chart notice, refresh button and four proposed-metric text cards. Export anchor points to `/admin/reports/export` without query parameters; nav/footer links use `#`.
- Prototype JS has no form/fetch/XHR/API client: Apply only toggles opacity for 300 ms; Reset restores hard-coded dates and `all`; Refresh shows “Đang đồng bộ máy chủ...” and blocks pointer events for 900 ms, then restores text. No filter query string, loading data, chart rendering, or server result is used.
- AC-38 diagram explicitly sequences #101 → aggregate KPI → #102 → date/permission validation → aggregate learning/community metrics → render/filter; optional export goes #103, with view-only branch. #103 response/Operation tracking discrepancy is outside this screen's implementation boundary but affects AD-25 handoff.
- Catalog #101 requires date query values; #102 uses strings and adds free-form `segment`. Existing API DDs #101/#102 are Draft. #101's four proposed record-count metrics and #102's four proposed enrollment/completion/topic/reply metrics are DERIVED and do not directly match the screenshot cards (active learners, completion rate, community hours, satisfaction). Screenshot segment taxonomy does not match #102 Draft's proposed `learning`/`community` grouping.
- Current server search found no #101/#102 route/module/query/model/test in `apps/study-server/app` or `tests`; `app/api/v1.py` is composed through #98. Shared auth helper supports explicit role(s) and current Admin APIs use `ADMIN`, contradicting stale API DD statements that the helper is Student-only; this does not wire report APIs or establish report-specific permission.
- Checked-in legacy DDL contains candidate `enrollments` (`user_id`, `enrolled_at`, `completed_at`) and self-referencing `discussions` (`parent_id`); pilot `report_snapshots` is a separate UUID/versioned candidate. These artifacts do not prove a live schema, report writer or approved metric mapping. AC-19's separate Comment model differs from legacy `discussions` replies.
- Study Web recheck: no tracked `apps/study-client/src`; current app tree has docs and ignored `dist` only, with no editable router/package/client. Study Web remains `UNWIRED` and serving/deployment is not verified.
- AD-01 DD states its #101 mockup metric cards have no mapping and its four API-DD proposals do not match them. AD-25 inventory expects exported filters to be retained, while this prototype link passes none; #103 catalog also conflicts with the separate Operation tracking paragraph.

## SOURCE_TRACE

```text
Expected: AD-24 opens from Admin report flow → GET #101 summary (`from/to:date`) → GET #102 community-impact (`from/to/segment:string`) → AC-38 date/report-permission validation and aggregate/render → optional navigation/export branch to AD-25/#103; view-only may end without export. Inventory expects filter state retained for export.
Current: no Study Web caller/router/client → no #101/#102 route/module/query/model/test → no source-backed aggregate or response mapping. Static HTML inputs are local; Apply toggles opacity, Reset writes fixed values, Refresh uses a 900-ms timer, and Export navigates without filters. API #101/#102 catalog and Draft DDs are declared design only.
Candidate DB evidence: legacy enrollment/discussion tables and separate pilot report_snapshots artifacts exist, but metric semantics, live schema, source/writer and authorization remain unverified. AC-38 diagram order and #101/#102 date types conflict/need clarification.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #101/#102 current implementation | Current route/module/test search found no report API source; API DDs say Draft / UNWIRED / NOT_FOUND. | UNWIRED / NOT_FOUND | Catalog is not runtime evidence; no result/error mapping is currently executable. |
| API DD authorization note | API #101/#102 open questions say current helper only has Student guard; current `validate_current_user_request` accepts explicit role(s), and Admin APIs #68–#98 use `ADMIN`. | SOURCE/DD DISCREPANCY | Shared capability exists, but no #101/#102 handler/report permission policy exists; do not claim authorization is verified. |
| KPI semantics and cards | Screenshot cards are active learners, completion rate, community interaction hours and satisfaction; catalog only defines generic `Report.metrics[]`; API-DD candidate metrics differ and remain DERIVED. | OPEN / BLOCKER | Do not map candidate metrics or formulas to screenshot cards. |
| Segment/date contract | Screenshot values `all/interns/graduates/alumni`; #102 catalog is free-form string and DD proposes `learning/community`; #101 date types are `date`, #102 types `string`. | DISCREPANCY / BLOCKER | No normalization, segment mapping or date conversion/error behavior can be finalized. |
| Diagram processing order | AC-38 edges sequence #101 → #102 → “Validate date range + quyền report” → aggregate. | DISCREPANCY / OPEN | Validation timing/owner is unclear; do not reorder or invent endpoint validation behavior silently. |
| Filter and export navigation | Inventory expects URL filters retained for AD-25; prototype export link goes to `/admin/reports/export` with no query. #103 catalog filters/format and Operation tracking disagree. | DISCREPANCY / BLOCKER | Do not invent serialization or claim AD-25 receives current filters. |
| Metric source/schema | Legacy DDL and pilot snapshot artifacts are candidate sources only; no #101/#102 query/writer or live schema evidence. | DERIVED / SOURCE_REQUIRED | Cannot claim reports are populated or compute from a chosen table. |
| Study Web route/client | No editable Study Web source/router/package; ignored `dist` does not establish this page. | UNWIRED | Candidate route and interactions are not runtime verified. |
| Prototype visual system | Remote Plus Jakarta Sans/cobalt tokens differ from Study Web design guide's Inter/system and ocean tokens. | DESIGN DISCREPANCY | Use canonical guide for implementation unless approved exception; preserve screenshot source. |

## CHANGES

- Files changed:
  - `apps/study-client/docs/screen_stitch/05_admin/AD-24_bao-cao-tac-dong-cong-dong/AD-24_PLAN.md` — source-backed per-screen plan and 42 marker coordinates, saved before marker/DD assets.
  - `AD-24_markers.json`, `AD-24_markers_overlay.svg`, `screen_annotated.png` — 42 sequential element markers over a 2× annotation; original source assets remain unchanged.
  - `AD-24.md` — A–F design specification with 42 elements, eight events, states/navigation, API/source trace, discrepancies and explicit blockers.
  - `apps/study-client/docs/list_screen.md` — row 82 blocker/status detail and #101/#102 reverse-index evidence; API statuses remain D.
  - `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` — AD-24 tracker status and 77/83 core-artifact checkpoint.
  - this worklog — source review and static verification results.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none. Design/candidate behavior remains distinct from current source.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective, `.agents/AGENTS.md`, context map, worklog README/template read; selector READY 3/229; AD-01/02/03 worklogs read in full. | VERIFIED_PREFLIGHT |
| Initial inventory/assets | Row 82, global plan row and API #101/#102 index inspected; folder has source image/HTML only; dimensions and hashes recorded. | VERIFIED_INITIAL |
| AD-24 source/contract review | Inventory/assets, AC-38 diagram, catalog #101/#102, API DD/open questions, #101/#102 DDL candidates, current route/auth search, Study Web tree, AD-01 DD and AD-25 inventory/#103 boundary reviewed. No #101/#102 app/test source. | VERIFIED_SOURCE_REVIEW |
| Artifact/static audit | 42 JSON/plan/SVG markers, 42 DD rows, sequential IDs, unique/in-bounds/non-overlapping centers, coordinates aligned; JSON/XML parsed; DD local links resolved; source hashes unchanged; PNG dimensions 1352×1600 and 2704×3200; inventory/folders 83/83 and core artifacts 77/83; full annotated image visually reviewed. | VERIFIED_STATIC |
| `git diff --check` | Scoped tracked changes to `list_screen.md` and `dd_screens/PLAN.md`; new-file whitespace scanned separately. | VERIFIED_STATIC |
| Application tests/runtime | Not run; current Study Web and report endpoints are unwired. | NOT_RUN |

## HANDOFF

- Completed this session: AD-24 plan, annotated screenshot, marker map/overlay, A–F DD, inventory/reverse-index/global-plan updates, worklog and static audit.
- DD status: `DD BLOCKED`; metric/formula/source, date, segment, authorization, schema/writer, AC-38 sequence and export handoff decisions remain open.
- Implementation status: `IMPLEMENTATION BLOCKED`; Study Web and #101/#102 have no local route/client implementation.
- Runtime status: `RUNTIME NOT VERIFIED`; no application tests/runtime were run.
- Stop after AD-24; AD-25 remains a separate session.
