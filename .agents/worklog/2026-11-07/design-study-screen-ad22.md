---
task_id: "2026-11-07-design-study-screen-ad22"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-37; API #97; reported discussion list and AD-23 moderation handoff"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-22

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs logs selected of 227; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Separate expected/current behavior; inspect Study Web source and current route; keep AC permission separate from local `ADMIN`; distinguish mockup metrics/actions from API fields and do not claim runtime/tests.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Preserve source assets; trace AC/API/source/auth/query/effects/response/errors; API local source `R` does not make API DD final; UI-only DD has no canonical skill; fake DB evidence is not live schema/deployment.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Do not infer audit/identity/action data from mockup; preserve API catalog vs local behavior; retain permission, PII, lifecycle and Study Web `UNWIRED` blockers; do not claim tests/runtime were run.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-22 only; review current assets, inventory, AC-37, API #97 and relevant current source; save `AD-22_PLAN.md` before markers/annotation/DD; preserve original assets; create ordered marker map and annotated image; author A–F DD with traceable elements/events/API/errors/states/navigation; update inventory/API reverse index/global plan and worklog; stop before AD-23.
- Inventory row 80: AD-22 “Danh sách thảo luận bị báo cáo”, candidate `/admin/discussions/reported`, AC-37, API #97; queue by severity/reason with pagination and pending priority; GET #97 then AD-23; no invented Student report endpoint; expected `loading/empty/ready/error`; P1; current tracker says D and no Student POST report API.
- AC-37 and API #97 contract/source must be compared before defining row fields, actions, ordering, permissions, and AD-23 handoff.

## CURRENT_BEHAVIOR

- AD-22 is documented in [`AD-22.md`](../../../apps/study-client/docs/screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/AD-22.md) with [`AD-22_PLAN.md`](../../../apps/study-client/docs/screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/AD-22_PLAN.md), 48-marker JSON/SVG, and a 2× annotated PNG. Original screenshot/HTML retained unchanged; SHA-256: PNG `5f53d5edfae7390b49259cbb7896447ebbfa3ef6bd4ac742ba325870b9d2d303`; HTML `043318fa9b192bc31d70652c3152d5e73b25971085d581d4cce174f198909980`.
- Prototype remains static: search/selects have no listener; refresh only animates for 700 ms; no fetch/XHR, pagination or 60-second timer. Static metrics, statuses and policy copy are not data/behavior.
- Current local API #97 route/source is documented with exact guard/query/projection/error/read-only behavior and DERIVED details separated from direct catalog. Report writer and live schema/deployment remain unverified; response lacks report metadata required by visible columns.
- AC-37 expects #97 → #98 report/thread detail. Current #98 source does not read reports and its DD says `UNWIRED / NOT_FOUND`; #99/#100 remain outside AD-22 source implementation. AC Admin permission vs local `ADMIN` remains unresolved.
- Study Web remains UNWIRED; candidate route is not runtime evidence. No application tests/runtime were run.

## SOURCE_TRACE

Expected flow: AC-37 Admin opens the reported-content queue → GET #97 with optional `reason`, `severity`, and `page` → read reports plus Discussion summary → select a Discussion and open AD-23/#98. The catalog has no search/status parameter or report metadata in `Page<Discussion>`; inventory's “pending priority” is not specified by #97's catalog. Expected Admin permission is not proven equivalent to local `ADMIN`.

Current source flow: static prototype only; no Study Web route or API call. If called directly, local #97 authorizes `ADMIN`, validates only page (1..int32 max; default 1), reads derived open/in-review reports and returns Discussion summaries without report fields. Current #98 accepts the Discussion int64 ID but does not read report records. No current source implements the AC-37 action/audit/delete steps #99/#100.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Screenshot search, status filter, metrics, report columns and 60-second copy | No corresponding #97 params/fields/handlers; HTML is static except local refresh spinner. | DOCUMENTED DISCREPANCY | Do not specify them as working behavior or map them to API data. |
| #97 queue grain/filter/order/page size/title/comments | Current source uses Discussion grain, OPEN/IN_REVIEW, exact reason/severity, latest report order, page size 20, derived title and empty comments; catalog does not specify most of these. | SOURCE-BACKED WITH DERIVED DETAILS; API DD DRAFT | Recorded as current local behavior; product/API confirmation needed before treating as approved. |
| Report ingestion and storage | Candidate table/migration exists; no current report writer found; live schema unknown. | DOCUMENTED BLOCKER | Do not imply the queue has production records or that Student reports can be created. |
| #97 response vs screenshot/AC-37 | `Page<Discussion>` has no reason/severity/count/reporter/report time. | DOCUMENTED DISCREPANCY / BLOCKER | The displayed report columns cannot be populated from #97 response without contract change. |
| Report-to-detail handoff | #97 Discussion ID is positive int64 and #98 path takes int64; current #98 does not return/read report details despite AC-37. | PARTIAL SOURCE SUPPORT / DOCUMENTED DISCREPANCY | ID can identify a Discussion, but report evidence handoff is incomplete; preserve AD-23 blocker. |
| Authorization | AC-37 actor Admin; local shared `ADMIN` role guard; finer permission/tenant policy unverified. | DOCUMENTED OPEN QUESTION | Do not claim role equivalence or final access policy. |
| Study Web/runtime | Editable `src` tree/router/API client absent. | UNWIRED | Candidate route is not implemented/runtime verified. |

## CHANGES

- Files changed: this worklog; AD-22 plan/DD/markers JSON/SVG/annotated PNG; `apps/study-client/docs/list_screen.md`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`.
- Trackers: inventory row 80 now records local #97 source status R and blockers; API reverse index #097 changed D→R with local-source/DERIVED caveat; API #97 DD remains Draft. Global plan row AD-22 records `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` and has a 75/83 progress checkpoint.
- CONTEXT_UPDATES: none; no `.agents/` context page was changed.
- Context pages changed: none.
- Assumptions: none. Prototype behavior, direct catalog contract, local source behavior and unresolved decisions remain separate.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Router/context/worklog preflight | `.agents/AGENTS.md`, `.agents/context-map.md`, worklog README/template read; selector READY 3/227; AD-01/02/03 reviewed in full. | VERIFIED_PREFLIGHT |
| Goal objective | Read `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`. | VERIFIED |
| AD-22 source/contract review | Compared inventory row 80, AC-37 diagram, #97 direct catalog, route/module/query/validator/models, #97 DD open questions, candidate DDL/migration, #98 DD/source discrepancy, Study Web tracked source tree, prototype and screenshot. | VERIFIED_STATIC_REVIEW |
| Plan before artifacts | Saved `AD-22_PLAN.md` before marker JSON/SVG, annotated image and DD. | VERIFIED |
| Marker/artifact audit | Python static audit: 48 sequential unique IDs; all points in 1280×1148 bounds; plan/JSON/SVG/DD coordinates and element IDs aligned; 10 event sections; relative links resolve. | PASS |
| Annotated image | `identify .../screen_annotated.png` → PNG 2560×2296; reviewed visually; 2× source ratio preserved. | PASS |
| Original source integrity | `sha256sum screen.png code.html` matched pre-edit PNG `5f53d5...d2d303` and HTML `043318...09980`. | PASS |
| Inventory/folder/artifact coverage | Static audit → inventory IDs 83; matching folders 83; complete core artifact sets 75/83. | PASS |
| Whitespace check | `git diff --check -- apps/study-client/docs/list_screen.md apps/study-client/docs/screen_stitch/dd_screens/PLAN.md apps/study-client/docs/screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao .agents/worklog/2026-11-07/design-study-screen-ad22.md` → no output, exit 0. | PASS |
| Application tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining AD-22 work: none. Continue only with a separate AD-23 session under the one-Screen-ID rule.
- Remaining blockers: report writer/live schema; report fields absent from #97 response; search/status/metrics/count/reason/time UI contract; #98 report detail; AC permission vs `ADMIN`; Study Web router/client absent.
- Stop after AD-22; AD-23 is a separate-session screen.

