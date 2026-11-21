---
task_id: "2026-10-24-inventory-study-api-dd-counts"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Kiểm kê số lượng Study API DD và implementation

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ đúng contract catalog; DD/source là hai loại bằng chứng riêng.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Chỉ tính implementation khi đối chiếu router và module; giữ ranh giới source/runtime.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Kiểm kê trước đó có 103 API và 12 source-wired API; cập nhật từ trạng thái mới nhất thay vì dùng số cũ.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Xác định số API có DD, chưa có DD, đã lập trình và chưa lập trình trong Study Server.
- Canonical contract/approved DD: `docs/lists/list_api.md`; source hiện hành `apps/study-server/app/api/v1.py` và các module `app/modules/**/view.py`; deliverables `apps/study-server/docs/dd/`.

## CURRENT_BEHAVIOR

- Source/config: Catalog hiện có 103 endpoint ID duy nhất #01–#103. Sau API #98 có 98 DD folder #01–#98; năm ID #99–#103 chưa có folder. Cả 98 folder đều có đủ tám sheet lõi; 86 có đủ ba report chuẩn, còn #01–#12 thiếu ba report.
- Runnable tests: Không chạy tests cho inventory/docs-only. Scope context xác nhận #08/#09 có route/module/test source nhưng chưa verify sau merge; #02 dùng email dispatch stub.
- Runtime wiring: Theo tiêu chí route declaration trong app/api/v1.py cộng matching module view.py, 12/103 API ID có source implementation (#01–#09, #12–#14); 91 chưa có cặp route/view. Đây không phải runtime-pass count.

## SOURCE_TRACE

```text
API IDs trong catalog -> DD folders/sheets/reports -> API labels trong router -> module view.py tương ứng -> trạng thái test/runtime theo scope context
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| DD #01–#12 | Tám sheet logic chính có mặt; thiếu ba report chuẩn | `INCOMPLETE_DELIVERABLES` | Tính là có DD; nếu tính full 11-artifact pack thì 12 folder còn thiếu. |
| API #08/#09 runtime | Route/module/test source có; context nói chưa verify sau merge | `SOURCE_PRESENT / RUNTIME_UNVERIFIED` | Tính là đã lập trình theo tiêu chí source/wiring, không khẳng định runtime pass hiện tại. |
| API #10/#11 | Không có router ID tương ứng hoặc `view.py` tương ứng | `UNWIRED / NOT_FOUND` | Tính trong 91 API chưa lập trình. |
| Catalog vs source | Catalog 103 IDs; route + view intersection là 12 IDs | `DISCREPANCY` | 91 API chưa có implementation source/wiring. |

## CHANGES

- Files changed: worklog kiểm kê này được cập nhật sau API #98; các snapshot trước được giữ làm lịch sử.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: “Đã tạo DD” được tính theo numbered folder tồn tại; mức đủ bộ được báo riêng theo tám sheet lõi cộng ba report. “Đã lập trình” nghĩa là API ID có route declaration hiện tại và matching view.py. Đây là source/wiring evidence, không phải runtime verification.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Deno selector trả #48/#49/#50; cả ba log được đọc đầy đủ; không thiếu. | VERIFIED |
| Catalog inventory | 103 API IDs duy nhất, liên tục #01–#103 trong docs/lists/list_api.md. | VERIFIED_STATIC_ONLY |
| DD inventory — recheck after #86 | 86 folders #01–#86, đủ tám sheet lõi; 74 full packages; 12 legacy core-only; #87–#103 thiếu folder (17). | VERIFIED_STATIC_ONLY |
| Router/module inventory | #01–#09 và #12–#14 có route marker và matching view.py (12); 91 không có cặp. | VERIFIED_STATIC_ONLY |
| DD #81 prior static validation | 11/11 files; 8/8 template appendix parity; 4 JSON examples, 41 local links/anchors resolved; no whitespace issues. This is historical DD validation, not a check of API #86. | PASS — STATIC |
| Current count recheck | Catalog rows filtered by HTTP method/path; DD numbered folders and required file roles counted; router API IDs intersected with matching module `view.py` IDs. | VERIFIED_STATIC_ONLY |
| Runtime boundary | Không chạy application tests; #08/#09 chưa post-merge verified; #02 provider là stub. | NOT_RUN / SOURCE_BOUNDARY |
| Context validator | Không đổi context page hoặc registry. | NOT_APPLICABLE |
| Current count recheck after API #90 | 103 endpoint rows #01–#103; 90 numbered DD folders (#01–#90), all with sheet prefixes 00–07; 78 have all three standard reports; 13 missing folders (#91–#103). Router/API marker plus matching view.py intersection is 12 IDs (#01–#09, #12–#14); 91 lack the pair. | VERIFIED_STATIC_ONLY |

## HANDOFF

- Remaining blockers: Runtime validation of #08/#09 is a separate task; #02 stub does not prove live email delivery. This count task does not establish runtime behavior for the other 91 APIs.
- Next owner/action: Continue authoring API #99; after #98, five catalog APIs (#99–#103) remain without DD folders.

## CURRENT RECHECK — 2026-10-24

- Worklog preflight: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` selected #48, #49 and #50; all three were read in this task.
- Catalog recheck: parsed only the endpoint tables from `## GUEST / ACCOUNT & DISCOVERY` through the section before `## Operation tracking`; confirmed 103 endpoint rows with contiguous unique IDs #01–#103.
- DD recheck: 60 folders (#01–#60); each has the eight required sheet prefixes 00–07 (folders with additional DB-mapping sheets remain valid); 48 folders also have all three reports. Thus #61–#103 (43) have no DD folder, and #01–#12 still lack the three reports.
- Source recheck: current `app/api/v1.py` declares API IDs #01–#09 and #12–#14; all 12 have matching `view.py` modules. Under the route-plus-view criterion, 12 are programmed and 91 are not.
- Runtime boundary: no tests were run for this inventory. Existing context says #08/#09 have not been post-merge verified; API #02 uses a dispatch stub and does not prove real email delivery.

## CURRENT RECHECK AFTER API #61 — 2026-10-24

- Catalog: 103 unique API IDs (#01–#103).
- DDs: 61 folders exist (#01–#61); 42 IDs (#62–#103) have no DD folder. All 61 have the eight core sheets; 49 have all 8 sheets plus the 3 standard reports. The remaining 12 (#01–#12) lack the three reports.
- Programming criterion: 12 APIs have both a route declaration in `app/api/v1.py` and a matching module `view.py` (#01–#09, #12–#14); 91 APIs do not have that route+view pair. This is source-presence evidence, not a runtime-pass claim.
- Runtime boundary: no tests run for this documentation/count refresh. Existing context says #08/#09 need post-merge verification; #02's dispatch stub does not prove live email delivery.


## CURRENT RECHECK AFTER API #62 — 2026-10-24

- Catalog: 103 endpoint rows, unique IDs #01–#103, contiguous.
- DDs: 62 folders (#01–#62); all 62 have the eight core sheets. 50 have all 8 sheets plus 3 standard reports; #01–#12 lack those reports. No DD folder exists for #63–#103 (41 APIs).
- Programming criterion: the 12 IDs with both a route/module import in `app/api/v1.py` and a matching module `view.py` are #01–#09 and #12–#14. The other 91 catalog IDs lack that source pair.
- Runtime boundary: this is source-presence evidence, not a runtime-pass claim. Existing Study context says #08/#09 need post-merge verification; #02's dispatch stub does not prove live email delivery. No tests were run for this docs/count refresh.


## CURRENT RECHECK AFTER API #63 — 2026-10-24

- Catalog: `docs/lists/list_api.md` has 103 unique endpoint rows with contiguous IDs #01–#103.
- DDs: 63 folders (#01–#63); all 63 have the eight core sheets (00–06 plus at least one 07_* sheet). 51/63 also have `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`; #01–#12 lack those three reports. No DD folder exists for #64–#103 (40 APIs).
- Programming criterion: source is counted when `app/api/v1.py` declares the API ID and a matching `app/modules/**/api_*/view.py` exists. IDs #01–#09 and #12–#14 meet this criterion (12 APIs); 91 do not. This is source-wiring evidence, not proof that all are currently runtime-verified.
- Runtime boundary: no tests were run for this docs/count refresh. Existing Study context says #08/#09 need post-merge verification; #02 uses a dispatch stub and does not prove live email delivery.


## CURRENT RECHECK AFTER API #64 — 2026-10-24

- Catalog: `docs/lists/list_api.md` has 103 unique endpoint rows, IDs #01–#103.
- DDs: 64 folders (#01–#64); all 64 have the eight core sheets (00–06 plus at least one 07_* sheet). 52/64 also have `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`; #01–#12 lack those three reports. No DD folder exists for #65–#103 (39 APIs).
- Programming criterion: current `app/api/v1.py` declares #01–#09 and #12–#14, each with a matching module `view.py` (12 API IDs); 91 catalog APIs do not have the route+view source pair. This is source-wiring evidence, not runtime verification.
- Runtime boundary: no tests were run for this docs task. Existing context says #08/#09 need post-merge verification; #02 uses a dispatch stub and does not prove real email delivery.

## CURRENT RECHECK — user count request — 2026-10-24

- Worklog preflight: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` selected `.agents/worklog/2026-10-24/create-study-api48-dd.md`, `create-study-api49-dd.md`, and `create-study-api50-dd.md`; all three were read in full.
- Catalog: parsed API rows only between `## GUEST / ACCOUNT & DISCOVERY` and `## Operation tracking`; confirmed 103 unique, contiguous endpoint IDs #01–#103. Catalog footer separately states 113 API-card occurrences; counts here use unique endpoint IDs.
- DD inventory: 64 folders (#01–#64), all 64 with the eight core sheets; 52 have the full 11-file package. IDs #65–#103 have no DD folder (39 APIs). The 12 folders #01–#12 have core sheets but lack the three standard reports.
- Programming criterion: #01–#09 and #12–#14 have both an API ID declaration in `app/api/v1.py` and a matching `app/modules/**/api_*/view.py` (12 APIs). The other 91 catalog APIs lack this route-plus-view pair.
- Runtime boundary: source presence is not runtime verification. No tests were run for this inventory. Scope context records #08/#09 as unverified after merge; #02 uses a dispatch stub and does not prove real email delivery.


## CURRENT RECHECK AFTER API #65 — 2026-10-24

- Catalog: docs/lists/list_api.md has 103 endpoint rows, unique and contiguous IDs #01–#103.
- DDs: 65 folders now exist (#01–#65); all 65 have the eight core sheets. 53 have all 8 sheets plus the 3 standard reports. #01–#12 lack those three reports. #66–#103 have no DD folder (38 APIs).
- Programming criterion: the IDs declared in app/api/v1.py and backed by matching module view.py remain #01–#09 and #12–#14 (12 APIs). The other 91 catalog IDs have no route-plus-view pair.
- Runtime boundary: source presence does not prove runtime verification. No application tests were run for this inventory; context says #08/#09 need post-merge verification and #02 uses a dispatch stub rather than proving real email delivery.
- Count transition for the latest request: before authoring API #65, 64 DDs existed and 39 were missing; after the verified #65 Markdown package, the current totals are 65 created and 38 missing. Programming totals are unchanged.


## CURRENT RECHECK AFTER API #66 — 2026-10-24

- Catalog: 103 unique API endpoint IDs (#01–#103).
- DDs: 66 folders exist (#01–#66); all 66 have the eight core sheets. 54 have all 8 sheets plus 3 standard reports. #01–#12 lack those three reports. #67–#103 have no DD folder (37 APIs).
- Programming criterion: current `app/api/v1.py` route declarations with matching `app/modules/**/api_*/view.py` exist for #01–#09 and #12–#14 (12 APIs); 91 catalog APIs have no route-plus-view pair. This is source-presence evidence, not runtime verification.
- Runtime boundary: no application tests were run for this docs task. Existing context says #08/#09 need post-merge verification; #02 uses a dispatch stub and does not prove real email delivery.
- Next action: create DD #67, then perform the pending AC-26 macro-review across #65–#67.

## CURRENT RECHECK AFTER API #67 — 2026-10-24

- Catalog: 103 unique API endpoint IDs (#01–#103).
- DDs: 67 folders exist (#01–#67); all 67 have the eight core sheets. 55 folders have the full 11-file package; #01–#12 still lack three standard reports. #68–#103 have no DD folder (36 APIs).
- Programming criterion: `app/api/v1.py` route declarations plus matching `app/modules/**/api_*/view.py` remain #01–#09 and #12–#14 (12 APIs); 91 catalog APIs lack the route-plus-view source pair. This is source-presence evidence, not proof of all runtime behavior.
- AC-26 source recheck: no route/module/focused test for #65, #66 or #67; #65–#67 macro-review is complete at document level with open contract/schema/auth/error questions. No application tests were run.
- Next API DD: #68.


## CURRENT RECHECK AFTER API #68 — 2026-10-24

- Catalog: 103 unique, contiguous endpoint IDs (#01–#103).
- DDs: 68 folders exist (#01–#68); all 68 have the eight core sheets. 56 have the full 11-file package; #01–#12 still lack the three standard reports. #69–#103 have no DD folder (35 APIs).
- Programming criterion: route declarations in apps/study-server/app/api/v1.py plus matching module view.py remain #01–#09 and #12–#14 (12 APIs); 91 catalog IDs lack a route-plus-view pair. This is source presence, not runtime proof.
- API #68: DD package is present and statically verified; runtime route/module/Admin guard/test remain absent. AC-31 group review stays pending until #69–#72 are available.
- Runtime boundary: no application tests were run for this docs task. Existing context says #08/#09 need post-merge verification; #02 uses a dispatch stub rather than proving real email delivery.
- Next API DD: #69.

## CURRENT RECHECK AFTER API #69 — 2026-10-24

- Worklog preflight for the #69 docs task selected #48, #49 and #50; all three selected worklogs were read in full before deep inspection.
- Catalog: 103 unique, contiguous endpoint IDs (#01–#103).
- DDs: 69 folders exist (#01–#69); all 69 have the eight core sheets. 57 have the full 11-file package; #01–#12 still lack the three standard reports. #70–#103 have no DD folder (34 APIs). Before #69 authoring, 68 existed and 35 were missing.
- Programming criterion: route declarations in apps/study-server/app/api/v1.py plus matching module view.py exist for #01–#09 and #12–#14 (12 APIs); 91 catalog IDs have no route-plus-view pair. This is source presence, not runtime proof.
- API #69: DD package is statically verified; runtime route/module/Admin guard/test remain absent. AC-31 macro-review remains pending until #70–#72 exist.
- Runtime boundary: no application tests were run. Existing context says #08/#09 were not verified after merge; #02 uses a dispatch stub and does not prove real email delivery.
- Next API DD: #70.


## CURRENT RECHECK AFTER API #70 — 2026-10-24

- Catalog: 103 unique endpoint IDs (#01–#103), contiguous.
- DDs: 70 folders exist (#01–#70); all 70 have the eight core sheets (00–06 plus at least one 07_* sheet). 58 have the full 11-file package; #01–#12 lack three standard reports. #71–#103 have no DD folder (33 APIs).
- Programming criterion: current router declarations with matching module `view.py` remain #01–#09 and #12–#14 (12 APIs); 91 catalog APIs have no route-plus-view pair. API #70 remains `UNWIRED / NOT_FOUND`.
- Runtime boundary: source presence is not runtime proof. No application tests were run for this docs task; existing context says #08/#09 need post-merge verification and #02 uses a dispatch stub rather than proving live email delivery.
- API #70 package: 11 Markdown files, 8/8 template appendices match exactly; static contract, JSON, links/anchors, tables/fences, and `git diff --check` passed.
- AC-31 macro-review remains pending until #71 and #72 DDs exist.


## CURRENT RECHECK AFTER API #71 — 2026-10-24

- Catalog: 103 unique endpoint IDs (#01–#103), contiguous.
- DDs: 71 folders exist (#01–#71); all 71 have the eight core sheets (00–06 plus at least one 07_* sheet). 59 have the full 11-file package; #01–#12 lack three standard reports. #72–#103 have no DD folder (32 APIs).
- Programming criterion: current router declarations with matching module `view.py` remain #01–#09 and #12–#14 (12 APIs); 91 catalog APIs have no route-plus-view pair. API #71 remains `UNWIRED / NOT_FOUND`.
- Runtime boundary: source presence is not runtime proof. No application tests were run for this docs task; #08/#09 still need post-merge verification and #02 uses a dispatch stub rather than proving live email delivery.
- API #71 package: 11 Markdown files, 8/8 template appendices match exactly; catalog contract/error set, candidate status/session boundary, JSON, links/anchors, tables/fences and whitespace passed; `git diff --check` clean.
- AC-31 macro-review remains pending until API #72 DD exists.

## CURRENT RECHECK — user count request — 2026-10-24

- Worklog preflight: Deno selector `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` selected API #48, #49 and #50 worklogs; all three were read in full.
- Catalog: parsed endpoint rows in `docs/lists/list_api.md`; confirmed 103 unique, contiguous API IDs (#01–#103).
- DD inventory: `apps/study-server/docs/dd/` contains 71 numbered folders (#01–#71), all with the eight core sheet prefixes (00–06 and at least one 07_* file). Thus 71 APIs have DD folders and 32 (#72–#103) do not. 59 folders contain the complete 11-file package; #01–#12 have the core sheets but lack the three standard reports.
- Programming criterion: intersected API IDs in `app/api/v1.py` with `app/modules/**/api_*/view.py`; the 12 matched IDs are #01–#09 and #12–#14. The other 91 catalog APIs have no route-plus-view pair.
- Runtime boundary: this is source/wiring inventory, not a claim that all routes currently pass runtime tests. No tests were run; existing scope context still marks #08/#09 as not post-merge verified and #02's dispatch provider as a stub.

## CURRENT RECHECK AFTER API #72 — 2026-10-24

- Catalog: `docs/lists/list_api.md` contains 103 unique, contiguous endpoint IDs (#01–#103), parsed only within the API sections before `## Operation tracking`.
- DDs: 72 numbered folders exist (#01–#72), all with the eight core sheets (00–06 plus at least one 07_* sheet). 60 also include `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`; #01–#12 lack those three reports. No folder exists for #73–#103 (31 APIs).
- Programming criterion: an API is counted as programmed when `app/api/v1.py` declares its API ID and the matching `app/modules/**/api_*/view.py` exists. IDs #01–#09 and #12–#14 meet this criterion (12); 91 do not.
- Runtime boundary: route/module presence is source-wiring evidence, not runtime verification. No application tests were run. Existing context records #08/#09 as unverified after merge and #02's email dispatch as a stub.
- AC-31: APIs #68–#72 received a document-level macro-review; list/pagination mismatch, Admin guard, model/schema selection, profile/PII visibility, status/session effects, deletion policy, dependency mapping, timestamp source, and error-envelope convention remain open.

## CURRENT RECHECK AFTER API #73 — 2026-10-24

- Catalog: `docs/lists/list_api.md` has 103 unique, contiguous endpoint IDs (#01–#103).
- DDs: 73 folders (#01–#73); all 73 have eight core sheets; 61 also have the three standard reports. #01–#12 lack those reports; #74–#103 have no DD folder (30 APIs).
- Programming criterion: router API IDs with matching modules remain #01–#09 and #12–#14 (12); 91 IDs have no route-plus-view pair. API #73 has no route, module or test in current Study source.
- Runtime boundary: source presence is not runtime verification. No application tests were run; #08/#09 are not post-merge verified and #02 email dispatch is a stub.
- API #73 package: 11/11 files; 8/8 template appendix suffixes byte-match; contract codes, JSON, tables, links/anchors, fences and whitespace pass; `git diff --check` clean.
- AC-32 macro-review #73–#77 remains pending until all five DDs exist. Category relation, Admin guard, status casing, pagination defaults and orphan-mentor policy remain open.

## CURRENT RECHECK AFTER API #74 — 2026-10-24

- Catalog: `docs/lists/list_api.md` has 103 unique contiguous endpoint IDs (#01–#103).
- DDs: 74 numbered folders (#01–#74); all 74 have eight core sheets; 62 have the complete 11-file package. #01–#12 still lack three reports; #75–#103 remain absent (29 APIs).
- Programming criterion: API ID declaration in `app/api/v1.py` plus matching module `view.py`; #01–#09 and #12–#14 remain the 12 source-wired IDs. 91/103 have no route/view pair.
- API #74: no route, module or test source; remains `UNWIRED / NOT_FOUND`. Its DD is docs-only and preserves catalog success/error codes.
- API #74 package: 11/11 files; 8/8 template appendix suffixes byte-match; contract/schema coverage, 2 JSON examples, 32 tables, 39 local links/anchors and whitespace checks pass. Output fingerprint is recorded in the DD verification report.
- Runtime boundary: no application tests were run. Source wiring counts do not imply current runtime pass; #08/#09 post-merge status and #02 stub boundary remain unchanged.
- AC-32 macro-review #73–#77 remains pending until #77 exists; counters, Admin authorization, schema selection, category relation, status casing and mentor integrity remain open.


## CURRENT RECHECK AFTER API #75 — 2026-10-24

- Worklog preflight: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` selected `.agents/worklog/2026-10-24/create-study-api48-dd.md`, `create-study-api49-dd.md`, and `create-study-api50-dd.md`; all three were read in full.
- Catalog: parsed endpoint rows in `docs/lists/list_api.md`; confirmed 103 unique, contiguous IDs (#01–#103).
- DD inventory: `apps/study-server/docs/dd/` contains 75 numbered folders (#01–#75), all with the eight core sheets. 63 also include `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, and `VERIFICATION_REPORT.md`; #01–#12 have the core sheets but lack those three reports. Thus 75 APIs have DDs and 28 (#76–#103) do not.
- Programming criterion: counted an API when its ID is declared in `app/api/v1.py` and a matching `app/modules/**/api_*/view.py` exists. The matched IDs are #01–#09 and #12–#14 (12 programmed); the other 91 catalog APIs have no route-plus-view pair.
- Runtime boundary: this is a source/wiring inventory, not a runtime-pass claim. No tests were run. Existing scope context says #08/#09 were not verified after merge; #02 uses a dispatch stub and does not prove real email delivery.
- Scope: no DD, source, schema, router, catalog, or context page changed; only this count worklog was refreshed. AC-32 #73–#77 remains pending macro-review until #77 DD exists.

## CURRENT RECHECK AFTER API #76 — 2026-10-24

- Worklog preflight: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` selected `.agents/worklog/2026-10-24/create-study-api48-dd.md`, `create-study-api49-dd.md`, and `create-study-api50-dd.md`; all three were read in full.
- Catalog: `docs/lists/list_api.md` contains 103 unique, contiguous endpoint IDs (#01–#103).
- DDs: 76 numbered folders exist (#01–#76); all 76 have the eight core sheets. 64 have the complete 11-file Markdown package; #01–#12 have the core sheets but lack `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`. Thus 76 APIs have DD folders and 27 (#77–#103) do not.
- Programming criterion: an API counts as programmed when `app/api/v1.py` declares its catalog ID and a matching `app/modules/**/api_*/view.py` exists. IDs #01–#09 and #12–#14 meet this criterion (12 programmed); 91 catalog IDs do not.
- Runtime boundary: route/view source presence is not runtime verification. No application tests were run for this count/DD task. Scope context marks #08/#09 as not verified after merge; #02 uses a dispatch stub and does not prove live email delivery.
- API #76 DD: exact 11-file package; all 8 template appendix suffixes byte-match; 2 JSON examples parse; 32 Markdown tables, 8 code fences, 26 local links and 10 anchors checked with no static issues. Template fingerprint `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`; DD payload fingerprint `9ffb9af4a6a06b41fb4ca58a73f7a0325e9ae35c7f026ec311c024fa4c8a2457`.
- API #76 remains `Draft — Needs Confirmation`; body/status casing and enum, Admin guard, transition policy, physical audit mapping/live schema and response envelope/cardinality need owner confirmation. AC-32 document-level macro-review remains pending until #77 exists.

## CURRENT RECHECK AFTER API #77 — 2026-10-24

- Catalog: `docs/lists/list_api.md` có 103 endpoint IDs duy nhất/liên tục (#01–#103).
- DD: 77 folder numbered (#01–#77), tất cả đủ 8 sheet cốt lõi; 65/77 có full 11-file package. #01–#12 vẫn thiếu 3 report chuẩn. #78–#103 chưa có DD: 26 API.
- Programming criterion: ID được khai báo trong `apps/study-server/app/api/v1.py` và có matching `apps/study-server/app/modules/**/api_*/view.py`. IDs #01–#09, #12–#14 meet criterion: 12 programmed; 91 chưa có route+view pair.
- Runtime boundary: source wiring không chứng minh runtime pass. Không chạy application tests; context hiện có #08/#09 unverified sau merge và #02 email dispatch dùng stub.
- API #77: exact 11-file Markdown package, 8/8 template suffix parity; 2 JSON examples, 28 core-sheet tables, 7 code fences, 36 local links/19 anchors và whitespace kiểm tra tĩnh. AC-32 #73–#77 macro-review hoàn tất với các open questions được giữ lại.
- Next DD: API #78.

## CURRENT RECHECK AFTER API #78 — 2026-10-24

- Catalog: `docs/lists/list_api.md` contains 103 unique, contiguous API IDs (#01–#103).
- DDs: 78 numbered folders exist (#01–#78), all with the eight core sheets. 66 have the complete 11-file Markdown package. #01–#12 still lack `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, and `VERIFICATION_REPORT.md`; #79–#103 have no DD folder (25 APIs).
- Programming criterion: an API counts as programmed when `apps/study-server/app/api/v1.py` declares its ID and a matching `apps/study-server/app/modules/**/api_*/view.py` exists. IDs #01–#09 and #12–#14 match (12); the other 91 catalog APIs do not.
- Runtime boundary: source wiring is not runtime verification. No application tests were run for this docs task. Existing Study context marks #08/#09 as not post-merge verified; #02's email dispatch remains a stub.
- API #78: exact 11-file Markdown package, 8/8 template appendix parity, 3 JSON examples parsed, 24 core tables and six fenced blocks checked, 38 local links/17 anchors resolved, whitespace clean. Direct response cardinality discrepancy and schema/auth/error gaps remain explicit; AC-33 macro-review waits for #79–#81.
- Next DD: API #79.


## CURRENT RECHECK AFTER API #79 — 2026-10-24

- Catalog: docs/lists/list_api.md contains 103 unique, contiguous API IDs (#01–#103).
- DDs: 79 numbered folders exist (#01–#79), all with the eight core sheets. 67 have the complete 11-file Markdown package. #01–#12 still lack OPEN_QUESTIONS.md, PLAN_RESULT.md, and VERIFICATION_REPORT.md; #80–#103 have no DD folder (24 APIs).
- Programming criterion: an API counts as programmed when apps/study-server/app/api/v1.py declares its ID and a matching apps/study-server/app/modules/**/api_*/view.py exists. IDs #01–#09 and #12–#14 match (12); the other 91 catalog APIs do not.
- Runtime boundary: source wiring is not runtime verification. No application tests were run for this docs task. Existing Study context marks #08/#09 as not post-merge verified; #02's email dispatch remains a stub.
- API #79: exact 11-file Markdown package; 8/8 template appendix parity, 2 JSON examples parsed, 26 tables/five code fences checked, 32 local links/16 anchors resolved, whitespace clean. AC-33 metadata response discrepancy and Content/version/author persistence gaps remain explicit. Group macro-review #78–#81 waits for #80/#81.
- Next DD: API #80.


## CURRENT RECHECK AFTER API #80 — 2026-10-24

- Worklog preflight: Deno selector selected create-study-api48-dd.md, create-study-api49-dd.md and create-study-api50-dd.md; all three were read; no shortage.
- Catalog: docs/lists/list_api.md has 103 unique contiguous API IDs #01–#103.
- DD folders: apps/study-server/docs/dd/ has 80 numbered folders #01–#80; 23 IDs #81–#103 remain without a folder. All 80 have the eight core sheet roles; 68 also have OPEN_QUESTIONS.md, PLAN_RESULT.md and VERIFICATION_REPORT.md. #01–#12 are the 12 core-only legacy packs.
- Source programming criterion: route API ID in app/api/v1.py plus matching app/modules/**/api_*/view.py. Matched IDs remain #01–#09 and #12–#14 (12 programmed); 91 catalog IDs have no route/view pair.
- Runtime boundary: no application tests were run for this docs/count task. #08/#09 source and tests are present but not verified after merge; #02 dispatches through a stub provider.
- API #80: DD folder has eight registered template sheets and three reports; exact catalog/error set and eight Content fields retained; 3 JSON examples parsed; 35 tables, 4 fences, 34 links and 9 anchors passed static checks; 8/8 template appendix suffixes byte-match.
- AC-33 group macro-review remains pending until #81 DD exists. No source, schema, catalog or diagram changed.

## CURRENT RECHECK AFTER API #81 — 2026-10-24

- Catalog: `docs/lists/list_api.md` contains 103 unique, contiguous API IDs (#01–#103).
- DDs: 81 numbered folders exist (#01–#81), all with the eight core sheet roles. 69 also have the complete 11-file package. #01–#12 remain the 12 core-only legacy packs; #82–#103 have no DD folder (22 APIs).
- Programming criterion: an API is counted as source-programmed when its ID is declared in `apps/study-server/app/api/v1.py` and a matching `apps/study-server/app/modules/**/api_*/view.py` exists. IDs #01–#09 and #12–#14 match (12); the other 91 do not.
- Runtime boundary: route/view presence is not runtime verification. No application tests were run. Existing scope context marks #08/#09 as not post-merge verified; #02 uses a dispatch stub and does not prove live email delivery.
- API #81: exact 11-file package, 8/8 template appendix parity, six exact catalog business codes, eight Content fields, 4 JSON examples and 41/41 local links/anchors passed static checks. Group macro-review #78–#81 completed; unresolved response cardinality, version identity, state/audit, Admin guard, persistence and lifecycle questions are recorded in the group report.
- No runtime/source/schema/catalog/diagram edits were made.

## CURRENT RECHECK AFTER API #82 — 2026-10-24

- Catalog: parsed endpoint rows containing `/api/v1/` with API IDs 1–103; confirmed 103 unique, contiguous IDs (#01–#103).
- DDs: 82 numbered folders exist (#01–#82); all 82 have the eight core template sheets. 70 have the complete 11-file Markdown package; #01–#12 remain the 12 core-only legacy packs. #83–#103 have no DD folder (21 APIs).
- Programming criterion: `apps/study-server/app/api/v1.py` route declaration plus matching `apps/study-server/app/modules/**/api_*/view.py`. IDs #01–#09 and #12–#14 match (12 source-programmed); 91 catalog APIs have no route-plus-view pair.
- Runtime boundary: source wiring is not runtime verification. No application tests were run. Existing scope context marks #08/#09 as not post-merge verified; #02 uses a dispatch stub and does not prove live email delivery.
- API #82: exact 11-file package; 8/8 template appendix parity, 3 JSON examples parsed, 29 Markdown tables, 14 code fences and 32 local links/anchors passed static checks; `git diff --check` clean. DD remains `Draft — Needs Confirmation` for response cardinality, `type` filter mapping, schema selection/nullability, Admin guard, status enum/casing and error-envelope behavior.
- AC-34 macro-review #82–#86 remains pending until #86 DD exists. No runtime/source/schema/catalog/diagram changes were made.
- Next DD: API #83.

## CURRENT RECHECK AFTER API #83 — 2026-10-24

- Catalog: parsed API endpoint table rows containing `/api/v1/` and IDs 1–103; confirmed 103 unique, contiguous IDs (#01–#103).
- DDs: 83 numbered folders exist (#01–#83); all 83 have the eight core template sheets. 71 have the complete 11-file Markdown package; #01–#12 remain the 12 core-only legacy packs. #84–#103 have no DD folder (20 APIs).
- Programming criterion: router API ID in `apps/study-server/app/api/v1.py` plus matching `apps/study-server/app/modules/**/api_*/view.py`. IDs #01–#09 and #12–#14 match (12 source-programmed); 91 catalog APIs have no route-plus-view pair.
- Runtime boundary: route/view source presence is not runtime verification. No application tests were run. Existing context marks #08/#09 as not post-merge verified; #02 uses a dispatch stub and does not prove live email delivery.
- API #83: exact 11-file package; 8/8 template appendix parity, 3 JSON examples parsed, 29 tables, 12 code fences and 35 local links/anchors passed static checks; `git diff --check` clean. DD remains `Draft — Needs Confirmation` for AC-34 dependency output, schema/nullability, Admin guard, LessonStatus, path mapping, soft-delete visibility and error integration.
- AC-34 macro-review #82–#86 remains pending until #86 DD exists. No runtime/source/schema/catalog/diagram changes were made.
- Next DD: API #84.

## CURRENT RECHECK AFTER API #84 — 2026-10-24

- Catalog: parsed endpoint table rows by HTTP method/path; confirmed 103 unique contiguous API IDs (#01–#103).
- DDs: 84 numbered folders exist (#01–#84); #85–#103 have no DD folder (19 APIs). All 84 folders have the eight sheet roles (the seventh mapping sheet may use a table-specific filename). 72 have the complete 11-file package; #01–#12 remain the 12 legacy/incomplete packs.
- Programming criterion: API ID declared in `apps/study-server/app/api/v1.py` plus matching `apps/study-server/app/modules/**/api_*/view.py`. IDs #01–#09 and #12–#14 match (12 source-programmed); 91 catalog IDs have no route/view pair.
- Runtime boundary: route/view source is not runtime verification. No application tests were run; #08/#09 remain unverified after merge in current context, and #02 uses a stub provider.
- API #84: exact 11-file package; 8/8 template appendix suffixes byte-match; catalog success and five error codes match; 4 JSON examples parsed, 209 Markdown table rows, 7 code fences and 36 local links checked; whitespace and `git diff --check` clean. DD remains `Draft — Needs Confirmation` for body/PUT semantics, live schema, Admin policy, nullability/status, timestamp/transaction and error integration.
- AC-34 macro-review #82–#86 remains pending until #86 DD exists. No runtime/source/schema/catalog/diagram changes were made.
- Next DD: API #85.

## CURRENT RECHECK AFTER API #85 — 2026-10-24

- User count request rechecked against the live checkout: `docs/lists/list_api.md` has 103 unique endpoint IDs (#01–#103).
- DDs: 85 numbered folders exist (#01–#85); 18 IDs (#86–#103) have no DD folder. All 85 folders have the eight core template sheets; 73 have the complete 11-file Markdown package. #01–#12 remain the 12 legacy packs without the three standard reports.
- Programming criterion: route API ID declared in `apps/study-server/app/api/v1.py` plus matching `apps/study-server/app/modules/**/api_*/view.py`. IDs #01–#09 and #12–#14 meet it (12 source-programmed); 91 catalog APIs do not have a route-plus-view pair.
- Runtime boundary: source wiring does not prove deployment/runtime pass. No application tests were run for this documentation task. Scope context marks #08/#09 as unverified after merge; #02 uses a dispatch stub.
- API #85: exact 11-file package; all 8 appendix suffixes match the registered template; exact catalog success/error set; 4 JSON blocks parse, 39 Markdown tables / 410 data rows have consistent widths, 14 fences are balanced, 28 local links and 13 anchors resolve, whitespace clean, and `git diff --check` clean. API remains Draft — Needs Confirmation for body, LessonStatus values/transitions, Admin policy, active schema, physical audit mapping, transaction and error integration.
- AC-34 macro-review #82–#86 remains pending until #86 DD exists. No source, schema, catalog, diagram or context page changed.
- Next DD: API #86.

## CURRENT RECHECK — user count request after API #86 — 2026-10-24

- Worklog preflight: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` selected `.agents/worklog/2026-10-24/create-study-api48-dd.md`, `create-study-api49-dd.md`, and `create-study-api50-dd.md`; all three were read in full. No shortage.
- Catalog: parsed endpoint rows by HTTP method/path in `docs/lists/list_api.md`; confirmed 103 unique, contiguous IDs #01–#103. The catalog footer also reports 113 API-card occurrences; this count uses unique endpoint IDs.
- DD inventory: `apps/study-server/docs/dd/` contains 86 numbered folders (#01–#86). All 86 have the eight core sheet roles; 74 also contain `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`. Thus 86 APIs have a DD folder and 17 (#87–#103) do not; #01–#12 are the 12 folders missing the three standard reports.
- Programming criterion: intersected API ID comments in `apps/study-server/app/api/v1.py` with matching `apps/study-server/app/modules/**/api_*/view.py`. IDs #01–#09 and #12–#14 match (12 source-programmed); the other 91 catalog APIs lack a route-plus-view pair.
- Runtime boundary: route/view source presence is not a runtime-pass claim. No application tests were run. Scope context marks #08/#09 as not verified after merge; #02 uses a dispatch stub and does not prove live email delivery.
- Scope: this count task changed only this worklog. No API DD content, router, runtime source, schema, catalog, diagram, or context page was changed. Context validator was not applicable.


## USER COUNT REQUEST RECHECK — VERIFIED (2026-10-24)

- Classification: `primary_task_type: docs`; scope `server-study`; no cross-scope dependencies.
- Worklog preflight: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` selected API #48, #49, #50 worklogs; all three were read in full.
- Catalog: parsed rows whose endpoint cell contains an HTTP method and `/api/v1/`; 103 unique, contiguous API IDs (#01–#103). The catalog separately states 113 API-card occurrences; this count is unique endpoint IDs.
- DD inventory: 86 numbered folders (#01–#86); all 86 have the eight core sheets. 74 have the full 11-file package. Therefore 17 IDs (#87–#103) have no DD folder; #01–#12 have core sheets but lack the three standard reports.
- Programming criterion: API ID comment in `app/api/v1.py` plus matching `app/modules/**/api_*/view.py`. Matched IDs: #01–#09 and #12–#14 (12); 91 catalog IDs lack the route-plus-view pair.
- Runtime boundary: this is source/wiring presence, not runtime-pass or deployment evidence. No app tests were run. Scope context marks #08/#09 as not verified after merge; #02 uses a dispatch stub, so real email delivery is not established.
- Files changed: this inventory worklog only. Existing DD/source worktree changes were preserved. No context page or registry changed; context validator was not applicable.


## CURRENT RECHECK — after API #87 DD — 2026-10-24

- Catalog: `docs/lists/list_api.md` contains 103 unique, contiguous endpoint IDs (#01–#103).
- DD inventory: 87 numbered folders (#01–#87); all retain the eight core sheet roles. 75 folders contain the three standard reports and thus the full report package; #01–#12 are the 12 core-only legacy packs. Therefore 87 APIs have a DD folder and 16 (#88–#103) do not.
- Programming criterion: intersected API ID comments in `apps/study-server/app/api/v1.py` with matching `apps/study-server/app/modules/**/api_*/view.py`. IDs #01–#09 and #12–#14 match (12 source-programmed); 91 catalog APIs lack a route-plus-view pair.
- Runtime boundary: source/wiring presence does not establish test, runtime, deployment, or external-side-effect success. API #87 remains unwired; no application tests were run. #02 dispatch stub and #08/#09 merge verification boundary remain as noted in prior recheck.
- DD #87 static validation: 11 Markdown files, 8/8 template appendix suffixes, 4 JSON blocks parsed, 450 table lines column-consistent, 5 balanced code fence pairs, 32 local links including 15 anchors resolved, whitespace clean.
- Scope: this recheck updates this inventory worklog and the API #87 DD task worklog/package. No app source, router, schema, catalog, diagram, or context page changed. Context validator is not applicable.

## CURRENT RECHECK — after API #88 DD and user count request — 2026-10-24

- Catalog: parsed only endpoint table rows containing an HTTP method and `/api/v1/`; 103 unique, contiguous API IDs (#01–#103).
- DD inventory: 88 numbered folders (#01–#88); all have the eight core sheet roles. 76 folders have all three standard reports; #01–#12 are the 12 core-only legacy folders. Thus 88 APIs have a DD folder and 15 (#89–#103) do not. API #88 has 13 Markdown files because it includes three table-mapping sheets plus the 3 reports.
- Programming criterion: API ID comment in `apps/study-server/app/api/v1.py` plus matching `apps/study-server/app/modules/**/api_*/view.py`. IDs #01–#09 and #12–#14 match: 12 source-wired APIs. The other 91 catalog IDs lack that route-plus-view pair.
- Runtime boundary: route/view presence is source evidence only, not runtime, deployment, or acceptance verification. No application tests were run for this docs/count task; current context still marks #08/#09 as not post-merge verified and #02 as using a dispatch stub.
- API #88 package: exact 13-file manifest; 10/10 template appendix suffixes match; 4 JSON blocks parsed with embedded config/questions decoded; 45 tables / 544 lines consistent; 4 balanced code-fence pairs; 39 local links / 19 anchors resolved; whitespace clean. Fingerprint: `c968202b7c1ecdbc658a83dc1ec5e3a85c2cbe6f268f9c907f3c2fc434803814`.
- Source scan: no #88 route/module/test marker under `apps/study-server/app` or `apps/study-server/tests`; #88 remains unwired.
- Scope: updated the count worklog, API #88 DD verification report and API #88 task worklog. No runtime source, schema, catalog, diagram, or context page changed; context validator is not applicable.


## CURRENT RECHECK — after API #89 DD — 2026-10-24

- Catalog: parsed endpoint table rows by HTTP method/path in `docs/lists/list_api.md`; 103 unique, contiguous IDs (#01–#103).
- DD inventory: 89 numbered folders (#01–#89); 77 include `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`. The 12 folders #01–#12 are core-sheet legacy packs without these three reports. Therefore 89 APIs have a DD folder and 14 (#90–#103) do not.
- Programming criterion: API ID comment in `apps/study-server/app/api/v1.py` plus a matching `apps/study-server/app/modules/**/api_*/view.py`. IDs #01–#09 and #12–#14 match (12 source-wired); 91 catalog APIs lack the route-plus-view pair.
- Runtime boundary: route/view presence is source evidence, not runtime, deployment, or acceptance verification. No application tests were run. Existing context marks #08/#09 not verified after merge; #02 uses a dispatch stub.
- API #89 DD: 15 Markdown files; 12/12 template appendix suffixes match; direct catalog contract retained; three JSON examples parse; 46 tables / 592 rows consistent; four code-fence pairs balanced; 56 local links and 27 anchors resolve; whitespace clean. Fingerprint: `e01159b0e27df6ad1ee4d3986e1e1a55022cba9619360df560734c00ddff62f7`. API #89 remains `UNWIRED` and DD `Draft — Needs Confirmation`.
- Source scan: no API #89 route/module/test marker under `apps/study-server/app` or `apps/study-server/tests`.
- Scope: updated this count worklog plus the API #89 DD and task worklog. No runtime source, schema, catalog, diagram, or context page changed; context validator is not applicable.


## CURRENT RECHECK — after API #90 DD — 2026-10-24

- Catalog: parsed endpoint table rows by method/path in `docs/lists/list_api.md`; 103 unique contiguous API IDs (#01–#103).
- DD inventory: 90 numbered folders (#01–#90); 78 include `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`. #01–#12 remain the 12 legacy folders without these three reports. Therefore 90 APIs have a DD folder and 13 (#91–#103) do not.
- Programming criterion: API ID comment in `apps/study-server/app/api/v1.py` plus a matching `apps/study-server/app/modules/**/api_*/view.py`. IDs #01–#09 and #12–#14 match (12 source-wired); 91 catalog APIs lack the route-plus-view pair.
- Runtime boundary: route/view presence is source evidence, not runtime/deployment/acceptance verification. No application tests were run. Existing context marks #08/#09 as not post-merge verified; #02 uses a dispatch stub.
- API #90 DD: 14 Markdown files; 11/11 template appendix suffixes match; direct catalog contract retained; AC-35 soft-delete-if-attempt branch and AC-16 #29–#32 history reviewed; 2 JSON blocks, 34 tables / 407 rows, 4 balanced fences, 37 local links / 12 anchors and whitespace passed. Output fingerprint: `9254b0a3f946a2d376b4130e87d994c9af8d7817fe24c4d10659175726c560ec`. API #90 remains `UNWIRED`; DD status `Draft — Needs Confirmation`.
- Source scan: no #90 route/module/test marker under `apps/study-server/app` or `apps/study-server/tests`.
- Scope: updated this inventory worklog plus API #90 DD and task worklog. No runtime source, schema, catalog, diagram or context page changed; context validator is not applicable.


## CURRENT RECHECK — user count request after API #90 — 2026-10-24

- Worklog preflight: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` selected `.agents/worklog/2026-10-24/create-study-api48-dd.md`, `create-study-api49-dd.md`, and `create-study-api50-dd.md`; all three were read in full. Their carry-forward rules were to keep catalog/DD/source evidence separate, match route IDs with module views, and avoid claiming runtime verification from source presence.
- Context loaded: root router, `.agents/AGENTS.md`, `.agents/context-map.md`, `server-study/AGENTS.md`, `INDEX.md`, `apis/declared-routes.md`, `workflows/README.md`, test-status page, and registered `createDD-markdown` skill. Scope remains docs/server-study; no cross-scope dependency.
- Catalog: counted only endpoint rows whose first cell is an API ID and whose row contains an HTTP method plus `/api/v1/`; result is 103 unique contiguous IDs #01–#103. This avoids counting HTTP business code `202` in the introductory code table as an endpoint ID.
- DD inventory: 90 numbered folders #01–#90; every folder has numbered sheet prefixes 00–07. 78 also contain `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`; #01–#12 are the 12 legacy folders missing these reports. Thus 90 APIs have a DD folder and 13 (#91–#103) do not.
- Programming criterion: intersected API ID comments in `apps/study-server/app/api/v1.py` with matching `apps/study-server/app/modules/**/api_*/view.py`; 12 IDs match (#01–#09, #12–#14), and the other 91 catalog IDs lack the route-plus-view pair.
- Runtime boundary: source/wiring evidence is not runtime-pass, deployment, or acceptance evidence. No application tests were run. API #08/#09 still require post-merge verification; API #02 uses a dispatch stub, so real email delivery is not established.
- Scope/change: updated this inventory worklog only. No API source, test, schema, catalog, diagram, or context page changed; context validator is not applicable.


## CURRENT RECHECK — user count request after API #90 — 2026-10-24

- Classification: `primary_task_type: docs`; `project_scopes: [server-study]`; no cross-scope dependencies.
- Worklog preflight: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` selected `.agents/worklog/2026-10-24/create-study-api48-dd.md`, `create-study-api49-dd.md`, and `create-study-api50-dd.md`; all three were read in full.
- Catalog: parsed endpoint rows in `docs/lists/list_api.md`; 103 unique, contiguous IDs #01–#103.
- DD inventory: `apps/study-server/docs/dd/` has 90 folders (#01–#90), all with the eight core sheet roles. 78 have the full 11-file package; #01–#12 have the core sheets but lack `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`. Thus 90 APIs have a DD folder and 13 (#91–#103) do not.
- Programming criterion: an API is counted when its ID comment is present in `apps/study-server/app/api/v1.py` and the matching `apps/study-server/app/modules/**/api_*/view.py` exists. IDs #01–#09 and #12–#14 match (12); 91 catalog IDs do not.
- Runtime boundary: source/wiring presence is not runtime, deployment, or acceptance verification. No app tests were run. Scope context marks #08/#09 as not post-merge verified; #02 uses a dispatch stub, so real email delivery is not established.
- Files changed: this inventory worklog only. Existing DD/source worktree changes were preserved; no API DD, source, test, schema, catalog, diagram, or context page changed.
- Context validator: `node scripts/validate-agent-context.mjs` could not start because Node.js is not installed. Deno compatibility run with read/env/git permissions returned `AGENT_CONTEXT_INVALID`: registry-referenced `db-admin` context/source is missing and multiple scopes, including `server-study`, are marked `CONTEXT_STALE`. No out-of-scope context repair was made.

## CURRENT RECHECK — after API #97 DD — 2026-10-24

- Classification: `primary_task_type: docs`; scope `server-study`; no cross-scope dependency.
- Worklog preflight: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` selected `.agents/worklog/2026-10-24/create-study-api48-dd.md`, `create-study-api49-dd.md`, and `create-study-api50-dd.md`; all were read in full.
- Catalog: 103 unique contiguous endpoint IDs (#01–#103).
- DD inventory after this task: 97 numbered folders (#01–#97), each with the eight core sheets; 85 have the full 11-file package. The 12 folders #01–#12 have the core sheets but lack the three standard reports. Six APIs (#98–#103) do not yet have a DD folder.
- Programming criterion: intersected API ID comments in `apps/study-server/app/api/v1.py` with matching `apps/study-server/app/modules/**/api_*/view.py`; IDs #01–#09 and #12–#14 match (12 source-programmed), while 91 catalog APIs lack the route-plus-view pair.
- Runtime boundary: route/view presence is source evidence, not runtime-pass/deployment evidence. No application tests were run. Current context marks #08/#09 unverified after merge; #02 uses a dispatch stub and does not prove live email delivery.
- API #97 package: exact 11-file manifest; all 8 template appendix suffixes match; request/response fields and exact catalog errors checked; JSON examples parse; local links/anchors, table widths, fences and whitespace pass; `git diff --check` passes. API #97 remains `UNWIRED / NOT_FOUND`, DD status `Draft — Needs Confirmation`.
- Scope: updated this inventory worklog and created API #97 DD plus its task worklog. No runtime source, tests, schema, catalog, diagram, or context page changed. Context validator is not applicable.
- Next DD: API #98. AC-37 macro-review remains pending until #100 exists.

## CURRENT RECHECK — after API #98 DD — 2026-10-24

- Classification: `primary_task_type: docs`; scope `server-study`; no cross-scope dependency.
- Worklog preflight: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` selected `.agents/worklog/2026-10-24/create-study-api48-dd.md`, `create-study-api49-dd.md`, and `create-study-api50-dd.md`; all were read in full.
- Catalog: 103 unique contiguous endpoint IDs (#01–#103).
- DD inventory after this task: 98 numbered folders (#01–#98), each with the eight core sheets; 86 have the full 11-file package. The 12 folders #01–#12 retain core sheets but lack the three standard reports. Five APIs (#99–#103) do not have a DD folder.
- Programming criterion: API ID declaration in `apps/study-server/app/api/v1.py` plus matching `apps/study-server/app/modules/**/api_*/view.py`. IDs #01–#09 and #12–#14 match (12 source-programmed); 91 catalog APIs lack the route-plus-view pair.
- Runtime boundary: route/view presence is source evidence, not runtime-pass/deployment evidence. No application tests were run. Current context marks #08/#09 unverified after merge; #02 uses an email dispatch stub.
- API #98 package: exact 11-file manifest; 8/8 template appendix suffixes match; request/response fields and exact catalog errors checked; JSON parses; local links/anchors, table widths, fences and whitespace pass; `git diff --check` passes. API #98 remains `UNWIRED / NOT_FOUND`, DD status `Draft — Needs Confirmation`.
- Scope: updated the inventory worklog and created API #98 DD plus its task worklog. No runtime source, tests, schema, catalog, diagram or context page changed. Context validator is not applicable.
- Next DD: API #99. AC-37 macro-review remains pending until #100 exists.

## CURRENT RECHECK — after API #99 DD — 2026-10-24

- Classification: `primary_task_type: docs`; scope `server-study`; no cross-scope dependency.
- Worklog preflight: Deno selector selected #48/#49/#50; all three `docs` worklogs were read in full for the API #99 task.
- Catalog: 103 unique contiguous endpoint IDs (#01–#103) in `docs/lists/list_api.md`.
- DD inventory: 99 numbered folders (#01–#99); all 99 have the eight core sheets. 87 also have `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`; the 12 folders #01–#12 still lack those reports. Four APIs (#100–#103) do not have a DD folder.
- Programming criterion: route ID declared in `apps/study-server/app/api/v1.py` plus matching module `view.py`. IDs #01–#09 and #12–#14 match (12 source-programmed); 91 catalog IDs do not have that pair.
- Runtime boundary: this is source/wiring inventory, not runtime/deployment/acceptance proof. No application tests were run. Context still marks #08/#09 unverified after merge; #02 uses a dispatch stub.
- API #99 package: exact 11-file manifest; 8/8 template appendix suffixes match; catalog contract/error set and 32 envelope/Page/Discussion/UserSummary/DiscussionComment response fields checked; 2 JSON blocks parse; local links, table widths, fences and whitespace pass; `git diff --check` has no diagnostics. API #99 remains `UNWIRED / NOT_FOUND`, DD status `Draft — Needs Confirmation`.
- Scope: updated this inventory worklog and created API #99 DD plus its task worklog. No runtime source, tests, schema, catalog, diagram, or context page changed. Context validator is not applicable.
- Next DD: API #100. AC-37 macro-review across #97–#100 remains pending until #100 exists.

## CURRENT RECHECK — after API #100 DD and AC-37 macro-review — 2026-10-24

- Classification: `primary_task_type: docs`; scope `server-study`; no cross-scope dependency.
- Catalog: 103 unique contiguous endpoint IDs (#01–#103) in `docs/lists/list_api.md`.
- DD inventory: 100 numbered folders (#01–#100); all 100 have the eight core sheets. 88 have all three standard reports; #01–#12 still have core sheets only. Three APIs (#101–#103) do not have a DD folder.
- Programming criterion: API ID comment/declaration in `apps/study-server/app/api/v1.py` plus matching module `view.py`. IDs #01–#09 and #12–#14 match (12 source-programmed); 91 catalog IDs do not have that route-plus-view pair.
- Runtime boundary: route/view presence is source inventory, not proof of runnable runtime, deployment, production behavior or acceptance. No application tests were run. Current context still marks #08/#09 unverified after merge; #02 uses a dispatch stub.
- API #100 package: exactly 11 Markdown files; 8/8 appendix suffixes match registered templates; exact contract/error set, request/response/mapping rows, JSON, local links, table widths, fences, whitespace and `git diff --check` pass. API #100 remains `UNWIRED / NOT_FOUND`, DD status `Draft — Needs Confirmation`.
- AC-37 macro-review #97–#100: flow order and reason-field separation are consistent. Report relation/response, Discussion projection, Admin guard, moderation/audit persistence, soft-delete timestamp, child/report handling and deleted-item visibility remain open; no contract/schema/runtime change was made.
- Scope: added API #100 DD/worklog and refreshed connected #97–#99 reports/worklogs with macro-review results. No runtime source, tests, schema, catalog, diagram or context page changed.
- Next DD: API #101.


## CURRENT RECHECK — after API #101 DD — 2026-10-24

- Classification: `primary_task_type: docs`; `project_scopes: [server-study]`; no cross-scope dependency.
- Catalog: 103 unique contiguous API IDs (#01–#103) in `docs/lists/list_api.md`.
- DD inventory: 101 numbered folders (#01–#101); all 101 have core sheet roles 00–06 plus a `07_*.md` table mapping. 89 have all three standard reports. The 12 folders #01–#12 remain core-only; #102–#103 are the 2 IDs without a DD folder. API #101 now has all 8 sheets and 3 reports.
- Programming criterion: an API is counted source-programmed when its ID marker is declared in `apps/study-server/app/api/v1.py` and a matching `apps/study-server/app/modules/**/api_*/view.py` exists. IDs #01–#09 and #12–#14 match (12); 91 catalog IDs lack the pair.
- Runtime boundary: source/wiring presence does not prove runtime, deployment, production or acceptance. No application tests were run. Existing context still marks #08/#09 as not post-merge verified; #02 uses a dispatch stub.
- API #101 DD: 11 Markdown files; 8/8 template suffixes; exact catalog contract/error set; one valid JSON example; 18 local links resolved; 513 table rows consistent; 3 code-fence pairs; whitespace and `git diff --check` pass. Fingerprints are recorded in `apps/study-server/docs/dd/101_admin_reports_summary/VERIFICATION_REPORT.md`. API #101 remains `UNWIRED / NOT_FOUND`.
- Scope: added API #101 Markdown and refreshed this inventory plus its task worklog. No application source, tests, schema, catalog, diagram or context page changed; context validator is not applicable.
- Handoff: **101 DD folders / 2 missing**; **12 source-programmed / 91 without a route+view pair**. Next DD is #102; AC-38 macro-review #101–#103 remains pending until #103 is complete.


## CURRENT RECHECK — after API #102 DD — 2026-10-24

- Classification: `primary_task_type: docs`; `project_scopes: [server-study]`; no cross-scope dependency.
- Catalog: parsed endpoint rows containing an API ID plus HTTP method and `/api/v1/`; 103 unique contiguous API IDs (#01–#103).
- DD inventory: `apps/study-server/docs/dd/` has 102 numbered folders (#01–#102); each has all 8 core sheet roles. 90 have the full 11-file package; #01–#12 have the core sheets but lack the 3 standard reports. Only API #103 has no DD folder.
- Programming criterion: an API counts as source-programmed when its ID marker is declared in `apps/study-server/app/api/v1.py` and a matching `apps/study-server/app/modules/**/api_*/view.py` exists. IDs #01–#09 and #12–#14 match (12); the other 91 catalog IDs lack the route-plus-view pair.
- Runtime boundary: route/view presence is source evidence, not runtime, deployment, production or acceptance verification. No application tests were run. Existing scope context marks #08/#09 as not post-merge verified; #02 uses an email dispatch stub.
- API #102 package: 11 Markdown files; exact template suffixes 8/8; catalog contract/error set preserved; 3 JSON examples parse; 23 local links resolved, no anchors; 523 table rows width-consistent; 5 fence pairs balance; whitespace and `git diff --check` pass. API #102 remains `UNWIRED / NOT_FOUND`.
- Scope: added API #102 Markdown/worklog and this inventory snapshot; corrected the #101 template fingerprint after recomputing against the registered template directory. No runtime source, tests, schema, catalog, diagram or context page changed; context validator is not applicable.
- Handoff: **102 DD folders / 1 missing (#103)**; **12 source-programmed / 91 without a route+view pair**. Next DD is #103; AC-38 macro-review #101–#103 remains pending until #103 is complete.

## CURRENT RECHECK — after API #103 DD and AC-38 macro-review — 2026-10-24

- Catalog: 103 unique, contiguous API IDs (#01–#103) in `docs/lists/list_api.md`.
- DD inventory: 103/103 numbered API folders exist and all have the eight core sheet roles. 91 have the full 11-file package; #01–#12 have the eight core sheets but lack `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`. Missing DD folders: 0.
- Programming criterion: a source-programmed API has an API ID declaration in `apps/study-server/app/api/v1.py` and a matching module `view.py`. IDs #01–#09 and #12–#14 meet this criterion (12); the other 91 IDs do not. This is source/wiring evidence, not runtime verification.
- Runtime boundary: no application tests were run for this docs/count refresh. Context still marks #08/#09 as not post-merge verified; #02 uses a dispatch stub, not evidence of live email delivery.
- AC-38 macro-review: #101 summary → #102 community dashboard/filter → optional #103 export/view-only; date types differ (#101 `date`, #102 `string`); #103 `Report`/`Operation` response conflict and API #18 ID/auth/result/storage/lifecycle gaps remain open. #101–#103 are `UNWIRED / NOT_FOUND`.
- Scope: created API #103 DD, refreshed connected AC-38 DD reports/open questions/worklogs and this inventory. No runtime, test, schema, catalog, diagram, or context page changed.

## CURRENT RECHECK — after API #01 package completion — 2026-10-24

- Classification: `primary_task_type: docs`; `project_scopes: [server-study]`; no cross-scope dependency. Preflight selected #100/#101/#102 docs worklogs; all three were read; shortage `none`.
- Catalog: 103 unique contiguous endpoint IDs (#01–#103) in `docs/lists/list_api.md`.
- DD inventory: 103 numbered folders and all 103 have the eight core sheet roles; 92 have the full 11-file package. #02–#12 remain core-only and lack the three standard report files. Missing DD folders: 0.
- Programming criterion: router API ID plus matching `app/modules/**/api_*/view.py`. IDs #01–#09 and #12–#14 match (12); 91 catalog IDs have no pair. This is source/wiring evidence, not runtime verification.
- API #01 package: added three reports, repaired two broken source links, whitespace and four registered-template appendix tails; 11 files, 8/8 appendix parity, 3 JSON examples, 426 consistent table rows, 36 local links/anchors, custom hygiene and `git diff --check` passed.
- AC-01 group boundary: design calls #02 after registration; current #01 only logs a pending marker. Current #02 calls provider synchronously, returns 500 on provider exception, has no retry worker, and default stub does not send email. This discrepancy is recorded in #01; API #02 package is the next one-DD session.
- Runtime boundary: API #01 tests were inspected but not run in this docs task; no deployment/live DB assertion.
- Scope: API #01 DD Markdown and worklogs only; no runtime, tests, schema, catalog, diagram, client or context-page changes.

## CURRENT USER REQUEST — COUNT RECHECK PLAN — 2026-10-24

- Classification: `primary_task_type: docs`; `project_scopes: [server-study]`; no cross-scope dependencies.
- Worklog preflight: selector `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` selected `.agents/worklog/2026-10-24/complete-study-api01-dd-package.md`, `create-study-api100-dd.md`, and `create-study-api101-dd.md`; all three were read in full. Carry-forward: count catalog API IDs, DD folders/core sheets/full report package, and source route-plus-view separately; source presence is not runtime verification.
- Context loaded: root router, `.agents/AGENTS.md`, `context-map.md`, Study Server AGENTS/INDEX/declared-routes/workflow, `worklog/TEMPLATE.md`, skills registry/manifest, and registered `createDD-markdown` skill sections for template and source traceability. Study DD output is Markdown-folder-only.
- Expected behavior: answer how many catalog APIs have a DD, how many do not, how many have implementation source, and how many lack it; state criteria and preserve runtime boundary.
- Previous current snapshot to recheck: after API #01 package completion, 103 folders/core DDs, 92 full 11-file packages, 11 folders #02–#12 missing the three reports, and 12 route-plus-view source pairs.
- Plan: (1) recount unique catalog IDs; (2) check numbered DD folders, eight core sheet roles, and the three standard reports; (3) intersect catalog IDs, router API markers, and matching module `view.py`; (4) report folder/DD completion separately from source implementation and runtime verification. No application, DD, schema, catalog, diagram, or test files will be changed.

## CURRENT USER REQUEST — VERIFIED COUNT RECHECK — 2026-10-24

- Catalog: `docs/lists/list_api.md` has 103 unique, contiguous endpoint IDs (#01–#103), counting rows with an HTTP method and `/api/v1/` path.
- DD folders: 103/103 numbered folders exist and all have the eight core sheet roles. Thus 103 APIs have a DD folder and 0 have no DD folder.
- Standard package: 92/103 folders have all three reports (`PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`) in addition to the core sheets. The 11 incomplete packages are #02–#12; they have core DD sheets but lack the standard reports.
- Source implementation: #01–#09 and #12–#14 have both an API ID marker in `app/api/v1.py` and a matching module `view.py`: 12/103. The other 91 lack that route-plus-view pair.
- Runtime boundary: route/view source presence is not runtime verification. No application tests or runtime checks were run. Scope context marks #08/#09 as not verified after merge; API #02's default email provider is a stub and does not prove delivery.
- Verification: catalog IDs, folder IDs, core sheet roles, report presence and router/view ID intersection were recounted from the current checkout; `git diff --check` passed for this worklog.
- Files changed: this inventory worklog only. No DD, source, test, schema, catalog, diagram or context page changed in this count task.
- Handoff: report both counts separately: DD folder 103 created / 0 absent; full standard package 92 complete / 11 report-incomplete; source-programmed 12 / 91 without a route-plus-view pair. Resume the active API #02 package completion after reporting these counts.

## CURRENT RECHECK — after API #02 package completion — 2026-10-24

- Catalog: 103 unique, contiguous endpoint IDs (#01–#103).
- DD inventory: all 103 numbered folders exist and all 103 have the eight core sheet roles. 93 folders have all three standard reports; #03–#12 (10 folders) remain report-incomplete. No catalog API is missing a DD folder.
- Programming criterion: API ID marker in `apps/study-server/app/api/v1.py` plus matching module `app/modules/**/api_*/view.py`; #01–#09 and #12–#14 match (12 source-programmed), while 91 catalog IDs lack the pair.
- API #02 package completion: 11 Markdown files; 8/8 template appendices; 4 valid JSON examples; 42 local links/anchors; 31 tables/370 table rows consistent; code fences, whitespace, final newline and `git diff --check` pass. No application tests were run.
- Runtime boundary: route/view presence is source wiring, not runtime/deployment/acceptance verification. #08/#09 remain unverified after merge according to scope context; API #02 default provider is still a non-sending stub.
- Files changed in the count/DD task: inventory worklog and API #02 Markdown/worklog only. No runtime source, tests, database/schema, catalog, diagram, client or context page changed.
- Handoff: **103 DD folders / 0 absent; 93 full packages / 10 report-incomplete; 12 source-programmed / 91 without route-plus-view pair.** Next DD is API #03.

## CURRENT RECHECK — after API #03 package completion — 2026-10-24

- Worklog preflight for API #03: selector `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` selected API #01, API #02 and API #100 docs worklogs; all three were reviewed in full; shortage `none`.
- Catalog: 103 unique, contiguous API IDs (#01–#103) in `docs/lists/list_api.md`.
- DD inventory: 103/103 numbered folders exist and all have the eight core sheet roles. 94 have all three standard reports; #04–#12 (9 APIs) have core sheets but are report-incomplete. Missing DD folders: 0.
- Programming criterion: router API ID marker plus matching module `view.py`. IDs #01–#09 and #12–#14 match (12 source-programmed); 91 catalog IDs lack the route-plus-view pair.
- API #03 package: 11 Markdown files; 8/8 front matter and workbook-source appendix structure; catalog contract/error set preserved; 4 JSON examples; 42 local links; 35 tables/453 table rows; balanced fences, clean whitespace/newlines, output fingerprint `c88270b0c62420e16fcff5ca7248c72dea209e52b27016ea400b25feb693ab9d`; `git diff --check` clean for tracked scope.
- Runtime boundary: no application tests, live DB, deployment or runtime checks were run. Source route/view presence is not runtime verification; API #08/#09 post-merge verification and API #02 real email delivery remain outside this task.
- Scope: API #03 Markdown and this/inventory worklog only; no runtime, tests, schema, catalog, diagram, API #04 DD or context page changed.
- Handoff: **103 DD folders/core DDs / 0 missing; 94 full packages / 9 report-incomplete; 12 source-programmed / 91 without a route-plus-view pair.** API #04 is next.

## CURRENT RECHECK — after API #04 package completion — 2026-10-24

- Worklog preflight: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` selected API #01, #02 and #03 package worklogs; all three were read in full; shortage `none`.
- Catalog: 103 unique, contiguous endpoint IDs (#01–#103).
- DD folders/core sheets: 103/103 numbered API folders exist and all have the 8 core sheet roles. No API is missing a core DD folder.
- Standard package completeness: 95/103 folders have all 3 standard reports in addition to 8 core sheets. #05–#12 (8 APIs) remain report-incomplete; API #04 now has its full 11-file package.
- Programming criterion: router API marker plus matching module `api_*/view.py`. IDs #01–#09 and #12–#14 match (12 source-programmed); 91 catalog IDs lack the pair.
- API #04 package checks: 11 Markdown files; 8/8 front matter and workbook appendix; 4 JSON blocks valid; 63 local links/anchors resolve; 33 tables with 384 data rows (450 table lines); balanced fences and clean whitespace/newlines; output fingerprint `3a49273b98ec9b9e287ff2807107a34852a1453cbf2f5f8ab9f8e0b44d35eb08`.
- AC-02 and AC-11 macro-review completed at document level. API #14 report source status was corrected to `SOURCE_PRESENT`; no application tests were run and no runtime pass was added.
- Runtime boundary: route/view presence is source/wiring evidence, not runtime verification. No application tests, live DB, deployment or production checks were run.
- Scope: API #04 Markdown, API #14 `PLAN_RESULT.md`/`VERIFICATION_REPORT.md`, and worklogs. No runtime source, tests, schema, catalog, diagram, client or scope context changed.
- Handoff: **103 DD folders/core DDs / 0 missing; 95 full packages / 8 report-incomplete; 12 source-programmed / 91 without a route-plus-view pair.** API #05 is next.

## CURRENT USER REQUEST — VERIFIED RECOUNT — 2026-10-24

- Classification: `primary_task_type: docs`; `project_scopes: [server-study]`; no cross-scope dependencies.
- Worklog preflight: `node scripts/select-worklogs.mjs --type docs --limit 3` was unavailable (`node: command not found`); Deno fallback `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` selected `complete-study-api01-dd-package.md`, `complete-study-api02-dd-package.md`, and `complete-study-api03-dd-package.md`. All three were read in full; shortage `none`.
- Context loaded: root `AGENTS.md`, `.agents/AGENTS.md`, `context-map.md`, server-study AGENTS/INDEX/workflow, manifest skill registry and worklog README. The Study DD deliverable is a Markdown folder, without a new ZIP.
- Catalog: parsed API endpoint table rows between `## GUEST / ACCOUNT & DISCOVERY` and `## Operation tracking`; 103 unique contiguous IDs (#01–#103).
- DD folders/core sheets: 103 numbered folders exist and every folder has all 8 core sheet roles (00–06 plus a 07_* mapping sheet). Therefore 103 APIs have a core DD and 0 are missing a DD folder.
- Standard package completeness: 94/103 folders contain all three standard reports in addition to the 8 core sheets. #04–#12 (9 APIs) have core DDs but are missing the three reports; #01–#03 and #13–#103 have the full 11-file package.
- Programming criterion: an API counts as source-programmed when its API ID is declared in `apps/study-server/app/api/v1.py` and its matching `app/modules/**/api_*/view.py` exists. IDs #01–#09 and #12–#14 match (12/103); the other 91 do not have that route-plus-view pair.
- Runtime boundary: this is source/wiring inventory, not proof of runtime, deployment, production behavior or acceptance. No application tests or runtime checks were run. Scope context still marks #08/#09 as not verified after merge; API #02's default provider is a stub.
- Verification: recounted catalog IDs, numbered folders, core sheets, report roles and router/view ID intersection from the current checkout. No DD, source, test, schema, catalog, diagram or context page changed; this worklog is the only file updated for the count request.
