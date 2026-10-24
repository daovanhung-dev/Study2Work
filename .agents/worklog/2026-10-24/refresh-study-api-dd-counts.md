---
task_id: "2026-10-24-refresh-study-api-dd-counts"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Kiểm kê lại số Study API DD và API đã lập trình

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/bin/deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` (Node không có trong PATH)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: DD tính theo 8 sheet nghiệp vụ; phân biệt source có mặt với runtime đã xác minh.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: DD design-only không chứng minh API đã được implement; giữ `UNWIRED`/`NOT_FOUND` theo source.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Catalog API hiện hành là nguồn đếm; router cùng module `view.py` là tiêu chí source implementation.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Báo số Study API có DD, chưa có DD, đã lập trình và chưa lập trình; nêu tiêu chí đếm để không gộp DD với implementation/runtime.
- Canonical contract/approved DD: `docs/lists/list_api.md`; DD dưới `apps/study-server/docs/dd/`; Study router `apps/study-server/app/api/v1.py` và module views hiện tại.

## CURRENT_BEHAVIOR

- Source/config: Catalog có 103 API ID #01–#103. Có 93 thư mục DD #01–#93; tất cả đủ 8 sheet chính. 81/93 thư mục có đủ ba report chuẩn; #01–#12 còn thiếu ba report. Vì vậy #94–#103 chưa có DD.
- Runnable tests: Không chạy test trong lần kiểm kê docs-only. Scope context ghi #1–#7 và #12–#14 đã được xác minh trước merge; #8/#9 có route/module/test source nhưng chưa được xác minh sau merge.
- Runtime wiring: Có 12 API ID khớp giữa router và `view.py`: #1–#9, #12–#14. Theo tiêu chí source implementation này, 12/103 đã lập trình và 91/103 chưa có route + view pair. Router có thêm route `/auth/refresh` mang comment API #03 nhưng catalog row #3 chỉ khai báo login; số liệu được tính theo API ID trong catalog. Đây không phải xác nhận runtime hiện tại.

## SOURCE_TRACE

```text
Catalog endpoint IDs -> DD folders/sheets/reports -> API ID comments in router -> matching module view.py -> runtime verification boundary in server-study context
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| DD completeness | 93 folders (#01–#93) have all 8 core sheets; 12 folders #01–#12 lack the 3 standard reports | `INCOMPLETE_DELIVERABLES` | “Có DD” = 93; “đủ gói chuẩn 11 file tối thiểu” = 81; 10 ID #94–#103 chưa có DD. |
| API #8/#9 | Route, view and test source exist; scope context says no post-merge verification | `SOURCE_PRESENT / RUNTIME_UNVERIFIED` | Counts as programmed by source criterion, not as runtime verified. |
| API implementation count | Router ID and module `view.py` intersection is 12 IDs | `VERIFIED_STATIC_ONLY` | Remaining 91 catalog IDs lack this source pair. |
| Catalog vs route operation | Catalog row #3 declares login; router also declares `/auth/refresh` under API #03 | `DISCREPANCY` | Count by catalog API ID; do not treat the extra route as a 104th catalog ID. |

## CHANGES

- Files changed: `.agents/worklog/2026-10-24/refresh-study-api-dd-counts.md`, refreshed after DD #93 and the latest count request; DD #93 folder and its worklog are also created in the active DD task.
- CONTEXT_UPDATES: None; no architecture or source status changed.
- Context pages changed: None.
- Assumptions: Count API IDs only when a catalog row contains an HTTP method and `/api/` endpoint. Count a DD when its folder contains all 8 core sheets; separately report standard-report completeness. Count programmed APIs when their catalog ID has both a router declaration and a module `view.py`. Router-only extra path `/auth/refresh` under API #03 is not a separate catalog ID.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Worklog selector and review | Selected/read #48, #49 and #50 `docs` worklogs; no shortage. | `VERIFIED` |
| Catalog parser | 103 endpoint rows, unique IDs #1–#103. | `VERIFIED_STATIC_ONLY` |
| DD inventory | 93 folders; 93/93 have 8 core sheets; 81/93 have the standard 11-file minimum; missing DD IDs #94–#103 (10). | VERIFIED_STATIC_ONLY |
| Router/view inventory | Exact intersection #1–#9, #12–#14 = 12 APIs; 91 catalog IDs absent from the intersection. | `VERIFIED_STATIC_ONLY` |
| Catalog/router boundary | Catalog has 103 IDs; `/auth/refresh` is an additional router path under comment API #03, so implementation counts remain by catalog ID. | `VERIFIED_STATIC_ONLY` |
| Runtime/tests | No tests run; #8/#9 not post-merge verified per scope context. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Complete the 3 standard reports for DD #01–#12 if every DD must meet the full standard package; verify API #08/#09 against the merged runtime before claiming current runtime pass.
- Next owner/action: Continue API DD creation at #94; current count is 93 DDs created, 10 not created, 12 source-programmed IDs and 91 without the route plus view source pair.


## CURRENT SESSION — PLAN BEFORE RECHECK

- User request: xác định số DD API đã tạo/chưa tạo và số API đã lập trình/chưa lập trình cho Study Server.
- Scope: `server-study`; primary task type `docs`; no cross-scope dependencies.
- Preflight: selector `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` selected #48, #49 and #50; all three worklogs were read. Also reviewed this inventory worklog, the prior refresh worklog, Study scope instructions/index/route context/workflow, and the current dirty-worktree status.
- Plan: count unique endpoint IDs in `docs/lists/list_api.md`; count numbered DD folders and required sheet/report roles; intersect API ID comments in `app/api/v1.py` with module `view.py` IDs. Report source/wiring counts separately from runtime verification. No tests or application files will be changed.


## CURRENT SESSION — VERIFIED RECHECK AFTER API #91

- Catalog: parsed only rows containing an HTTP method and `/api/v1/` endpoint in `docs/lists/list_api.md`; confirmed 103 unique, contiguous IDs #01–#103. This avoids counting the separate business-code row for HTTP 202 as an endpoint.
- DDs: `apps/study-server/docs/dd/` has 91 numbered folders (#01–#91), all 91 have the eight core sheet roles. 79 also have `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`; #01–#12 are core-only. Missing IDs are #92–#103 (12). API #91 has 11 Markdown files.
- Programming criterion: IDs declared in `apps/study-server/app/api/v1.py` and backed by matching module `view.py` are #01–#09 and #12–#14 (12); the other 91 catalog IDs have no route-plus-view pair. The extra `/auth/refresh` route carries API #03's marker and is not a separate catalog ID.
- Runtime boundary: static source/wiring count only; no application tests run. Scope context says #08/#09 have not been post-merge runtime-verified; #02 uses an email dispatch stub.
- Scope changed: this worklog only; no application source, catalog, schema, DD or context page edited in this count refresh.

## CURRENT USER REQUEST — COUNT RECONFIRMATION (2026-10-24)

- Classification: `primary_task_type: docs`; `project_scopes: [server-study]`; no cross-scope dependencies.
- Worklog preflight: selector `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` selected `create-study-api48-dd.md`, `create-study-api49-dd.md`, and `create-study-api50-dd.md`; all three were read in full.
- Context loaded: root router, `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/server-study/AGENTS.md`, `INDEX.md`, declared-routes page, Study workflow, and machine registry entry wiring `createDD-markdown` to `server-study`. DD creation remains Markdown-folder-only.
- Catalog: parsed endpoint table rows with numeric API ID, HTTP method, and `/api/v1/`; confirmed 103 unique contiguous IDs #01–#103.
- DD inventory: 91 numbered folders (#01–#91); all 91 have core sheet prefixes 00–07. 79 folders contain all three standard reports (`PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`); #01–#12 lack those reports. Therefore 91 APIs have a DD folder and 12 (#92–#103) do not.
- Programming criterion: API ID marker in `apps/study-server/app/api/v1.py` plus matching `apps/study-server/app/modules/**/api_*/view.py`. Matched #01–#09 and #12–#14: 12 source-programmed IDs; 91 catalog IDs have no matching route-plus-view pair. The extra `/auth/refresh` declaration is tagged #03, not a new catalog ID.
- Runtime boundary: this is static source/wiring evidence, not runtime, deployment, or acceptance verification. No app tests were run. Scope context says #08/#09 have not been post-merge verified; #02 uses a dispatch stub, which does not establish real email delivery.
- Scope: updated this worklog only. No DD, runtime source, test, schema, catalog, diagram, or context page changed. Context validator was not applicable.

## CURRENT SESSION — PLAN BEFORE COUNT RECHECK AFTER API #92

- Request: report Study API DD created/not created and API source-programmed/not source-programmed counts; load the `server-study` and `createDD-markdown` context for the next DD task.
- Classification: `primary_task_type: docs`; `project_scopes: [server-study]`; no cross-scope dependencies.
- Preflight: selector `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` selected `create-study-api48-dd.md`, `create-study-api49-dd.md`, and `create-study-api50-dd.md`; all three were reviewed. Loaded root router, context map, Study scope entry/index/route/workflow pages, and verified `createDD-markdown` is wired in the context manifest.
- Carry-forward: DD folder existence is separate from route/view implementation; preserve static-source versus runtime verification boundary; Study DD output is Markdown-folder-only.
- Plan before final check: count catalog IDs only from numbered table rows with HTTP method and `/api/v1/` endpoint; count DDs by numbered folder plus exact eight core sheet filenames; count source-programmed IDs by intersection of catalog IDs, router API markers, and matching module `view.py` IDs. Report the 3 standard-report completion count separately. No source or DD edits; no application tests.

## CURRENT SESSION — VERIFIED COUNT RECHECK AFTER API #92

- Catalog: `docs/lists/list_api.md` contains 103 unique endpoint IDs, contiguous #01–#103.
- DD inventory: `apps/study-server/docs/dd/` contains 92 numbered folders, #01–#92. All 92 have all eight numbered sheet roles (00–07). The three standard reports are present in 80/92; legacy IDs #01–#12 lack them. Therefore DD created = 92; DD not created = #93–#103 (11).
- Programming criterion/result: intersection of catalog IDs, API markers in `apps/study-server/app/api/v1.py`, and corresponding `apps/study-server/app/modules/**/api_*/view.py` is #01–#09 and #12–#14 (12). Thus 91 catalog APIs do not yet have both route marker and matching view source.
- Runtime boundary: this is static source evidence only. No app tests/runtime checks were run. Scope context says #08/#09 remain unverified after merge; #02's default verification-email provider is a stub. The extra `/auth/refresh` path remains tagged #03 and is not a separate catalog ID.
- Verification: catalog IDs contiguous; DD IDs contiguous; all 92 have numbered sheet roles 00–07; 80 have all three reports; source ID intersection exact; worklog has no trailing whitespace.
- Files changed: this count worklog only. No API DD, application source, schema, catalog, test or scope context page changed. `createDD-markdown` is registry-wired to `server-study`; Study DD delivery remains Markdown-folder-only.
- Handoff: counts are 92 DD created / 11 not created and 12 source-programmed / 91 without a route-plus-view pair. Next DD ID is #93. Do not equate source presence with runtime verification.


## CURRENT SESSION — VERIFIED AFTER API #93

- Catalog: 103 unique contiguous endpoint IDs #01–#103.
- DD inventory after this task: 93 numbered folders #01–#93; all 93 contain core sheet roles 00–07. Ten IDs #94–#103 do not yet have DD folders.
- Standard package completeness: 81/93 folders contain all three standard reports; #01–#12 are legacy core-only folders. API #93 has an additional recipient mutation mapping.
- Programming criterion: matching API marker in app/api/v1.py and module api_*/view.py remains #01–#09 and #12–#14: 12/103 source-programmed; 91 IDs lack this route-plus-view pair.
- API #93 is UNWIRED / NOT_FOUND by scoped static scan. This count is not runtime, deployment, or acceptance verification.
- No application tests were run. API #93 docs verification covered template appendix/front matter, exact catalog contract, JSON, tables, fences, local links/anchors and whitespace.
- Handoff: continue DD creation at API #94; preserve AC-36 macro-review as pending until API #96 completes the group.


## CURRENT SESSION — VERIFIED AFTER API #94

- Catalog: 103 unique contiguous endpoint IDs #01–#103. The separate row for HTTP status 202 is not an API ID.
- DD inventory: 94 numbered folders #01–#94; all have the eight core sheet roles (00–06 plus a 07_* mapping sheet). Nine IDs #95–#103 remain without DD.
- Standard package completeness: 82/94 folders contain all three standard reports; legacy #01–#12 remain core-only.
- Programming criterion: matching API marker in app/api/v1.py plus corresponding module api_*/view.py remains #01–#09 and #12–#14: 12/103 source-programmed; 91 catalog IDs lack this route-plus-view pair.
- API #94 is UNWIRED / NOT_FOUND by scoped static scan. This count is not runtime, deployment, or acceptance verification.
- API #94 DD static verification: 12 files, 9/9 template appendices, 9/9 front matter, 2 valid JSON examples, 33 consistent tables, 34 resolved local links, no whitespace defects.
- No application tests/runtime checks were run. No application source, catalog, schema, diagram or context page changed.
- Handoff: counts are 94 DD created / 9 not created and 12 source-programmed / 91 without a route-plus-view pair. Next DD is #95; keep AC-36 macro-review pending until #96.


## CURRENT SESSION — VERIFIED AFTER API #95

- Catalog: 103 unique endpoint IDs #01–#103.
- DD inventory: 95 numbered folders #01–#95; all have the eight core sheet roles (00–06 plus a 07_* mapping sheet). Eight IDs #96–#103 remain without DD.
- Standard package completeness: 83/95 folders contain all three standard reports; legacy #01–#12 remain core-only.
- Programming criterion: matching API marker in app/api/v1.py plus module api_*/view.py remains #01–#09 and #12–#14: 12/103 source-programmed; 91 catalog IDs lack this route-plus-view pair.
- API #95 is UNWIRED / NOT_FOUND by scoped static scan. This is not runtime, deployment or acceptance verification.
- API #95 DD static verification: 12 files, 9/9 template appendices, 9/9 front matter, 1 valid JSON example, 32 consistent tables, 32 resolved local links and no whitespace defects.
- No application tests/runtime checks were run. No application source, catalog, schema, diagram or context page changed.
- Handoff: counts are 95 DD created / 8 not created and 12 source-programmed / 91 without a route-plus-view pair. Next DD is #96; then macro-review AC-36 #92–#96.

## CURRENT USER REQUEST — VERIFIED RECHECK AFTER API #96

- Classification: `primary_task_type: docs`; `project_scopes: [server-study]`; no cross-scope dependencies. The Deno `docs` selector returned #48, #49 and #50; all were read in full as part of the active #96 DD task.
- Catalog: 103 unique endpoint rows, contiguous IDs #01–#103.
- DD inventory after authoring #96: 96 numbered folders (#01–#96), each with core sheet roles 00–07. Seven IDs #97–#103 have no DD folder. 84/96 folders have all three standard reports; legacy #01–#12 have the eight core sheets but no three reports.
- Programming criterion: a catalog API is source-programmed when its route is declared in `apps/study-server/app/api/v1.py` and the matching module `view.py` exists. IDs #01–#09 and #12–#14 meet this criterion: 12/103 programmed; 91 not programmed by this source criterion. `/auth/refresh` remains a second path tagged under #03, not a separate catalog ID.
- Runtime boundary: source/wiring count is not runtime verification. No application tests ran. Context says #08/#09 remain unverified after merge and #02 uses a dispatch stub.
- API #96 has no route/module/test and remains `UNWIRED / NOT_FOUND`; the count task and DD static review do not alter implementation status. AC-36 #92–#96 macro-review completed as `VERIFIED_WITH_OPEN_QUESTIONS`; see `apps/study-server/docs/dd/96_admin_notifications_status/AC-36_MACRO_REVIEW.md`.
- Verification: catalog rows, folder IDs, 8-sheet/3-report roles and router/view intersection checked from current checkout; #96 Markdown package and connected report links statically checked. No tests, deployment, or live DB check.
- Files updated: this count worklog, #96 DD/worklog, and connected #92–#95 DD/worklog macro-review status. No application source, test, schema, catalog, diagram, or scope context page changed.
- Result: **96 DD created / 7 not created**; **12 source-programmed / 91 without the route-plus-view pair**. This does not claim all 12 are runtime verified.
- Handoff: next DD is #97; standard report completion for legacy #01–#12 remains separate from the count of DD folders.
