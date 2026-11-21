---
task_id: "2026-10-23-inventory-study-api-dd-implementation-counts"
date: "2026-10-23"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Kiểm kê Study API DD và implementation

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` (Node không có trong PATH)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-23/create-study-api41-dd.md`
    - carry_forward: API #41 DD được tạo; chỉ tính ID catalog một lần, và DD không chứng minh runtime implementation.
  - path: `.agents/worklog/2026-10-23/create-study-api42-dd.md`
    - carry_forward: API #42 DD được tạo; tình trạng source phải kiểm tra từ router/module hiện tại.
  - path: `.agents/worklog/2026-10-23/create-study-api43-dd.md`
    - carry_forward: API #43 DD được tạo; nhóm API #43–#45 vẫn design-only cho đến khi source có route/module.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Báo số Study API có DD, chưa có DD, đã lập trình và chưa lập trình.
- Canonical contract/approved DD: Đếm API ID có endpoint trong `docs/lists/list_api.md`; so với DD folder và route/module `apps/study-server` hiện tại.

## CURRENT_BEHAVIOR

- Source/config: Catalog có 103 API ID (#01–#103). Hiện có 46 DD folder (#01–#46); cả 46 đều có đủ 8 sheet lõi (`00_Cover` đến một `07_*.md`). Có đủ ba report `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` ở 34 folder (#13–#46); #01–#12 thiếu ba report này. Router `app/api/v1.py` tham chiếu API ID #01–#09 và #12–#14; cả 12 ID đều có module `view.py` tương ứng.
- Runnable tests: Không chạy theo yêu cầu kiểm kê. Scope context ghi API #08/#09 có route/module/test source nhưng chưa được xác minh sau merge.
- Runtime wiring: 12/103 API có route + module `view.py` trong source; 91 ID còn lại chưa có route/module source tương ứng. API #10 có thư mục module/test nhưng chỉ chứa bytecode trong `__pycache__`, không có file `.py` hay route, nên không tính là đã lập trình. Bộ đếm lấy ID từ cột đầu các dòng endpoint trong bảng catalog, không lấy HTTP status code hoặc số được nhắc trong phần mô tả.

## SOURCE_TRACE

```text
API catalog IDs -> numbered DD folders and sheets -> app/api/v1.py route imports -> matching module view.py files -> test-source presence (context only)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| DD reports #01–#12 | Mỗi folder có đủ sheet lõi nhưng thiếu ba report chuẩn; #13–#46 có đủ report | `INCOMPLETE_DELIVERABLES` | Tính là có DD; 34/46 pack có đủ ba report. |
| API #08/#09 runtime proof | Route/module/test source có; scope context ghi chưa verify sau merge | `SOURCE_PRESENT / RUNTIME_UNVERIFIED` | Tính là đã lập trình theo tiêu chí source/wiring, không khẳng định runtime đã pass. |
| API #10 | Module/test directories chỉ có bytecode cache; không có file `.py`, `view.py` hoặc route trong `app/api/v1.py` | `CACHE_ONLY / UNWIRED` | Không tính là API đã lập trình. |
| Catalog versus implementation | Catalog 103 ID; source route + view intersection là 12 ID | `DISCREPANCY` | 91 API chưa có implementation source/wiring. |

## CHANGES

- Files changed: This inventory worklog refreshed only; API #46 DD was created and statically verified after the initial 45-folder count; this inventory now reflects 46 folders.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: “Đã tạo DD” means the numbered folder has all eight core sheets; “đã lập trình” means the API ID is referenced by the current Study router and has a corresponding `view.py`. Runtime verification is reported separately.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector and review | Deno-compatible selector selected and three matching `docs` worklogs (#41–#43) were read; no shortage. Node was unavailable. | `VERIFIED` |
| Catalog endpoint-row inventory | Exactly 103 unique IDs, #01–#103, extracted from the ID column of endpoint table rows. | `VERIFIED` |
| DD folder/sheet inventory | 46 numbered folders #01–#46; all 46 have the eight core sheets; 57 IDs #47–#103 have no DD folder. API #46 has 11 expected files including all three reports. | `VERIFIED` |
| DD reports inventory | Three report files exist in 34 folders (#13–#46); #01–#12 lack the three reports. | `VERIFIED` |
| Router/module inventory | `app/api/v1.py` includes route handlers for #01–#09 and #12–#14; each has a matching module `view.py`; 12 source-wired IDs and 91 without matching route/view wiring. | `VERIFIED` |
| Test-source inspection | Python test source exists for APIs #01–#09 and #12–#14. API #10 chỉ có bytecode cache; API #11 không có test source. Tests were not executed. | `VERIFIED_STATIC_ONLY` |
| Runtime tests | Not run; not requested. #08/#09 remain post-merge runtime-unverified per scope context. | `NOT_RUN` |
| Context validator | `node scripts/validate-agent-context.mjs` could not start (`node: command not found`). Deno fallback returned `AGENT_CONTEXT_INVALID` for missing DB Admin pages/source and unavailable baseline commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`; unrelated to this Study inventory. | `BLOCKED_UNRELATED_REPO_CONTEXT` |

## CURRENT REQUEST REFRESH

- Initial current-tree count for the user request found 103 unique endpoint IDs (#01–#103), 45 DD folders and 12 source-wired APIs.
- After completing API #46 in this task, the latest count is 46 core DDs (#01–#46) and 57 APIs without DD. All 46 have the eight core sheets; 34 include all three standard reports, while #01–#12 lack those reports.
- `apps/study-server/app/api/v1.py` labels API IDs #01–#09 and #12–#14; all 12 have a matching module `view.py`. By the route-plus-view criterion, 12 APIs are programmed and 91 are not. API #10 has only bytecode caches, no Python source or route/view, so it is excluded.
- API #08/#09 remain source-wired but post-merge runtime-unverified. No application tests were run for this inventory or DD task.

### Revalidation for the current request

- Re-read `docs/lists/list_api.md`: the endpoint table contains 103 unique IDs, continuously #01–#103; the footer separately notes 113 API-card occurrences, which are not the unique API count.
- Re-counted `apps/study-server/docs/dd/`: 46 folders (#01–#46), all with the eight core sheets; 34 folders (#13–#46) also have all three reports. Therefore 57 catalog APIs (#47–#103) have no DD folder.
- Re-counted route labels in `apps/study-server/app/api/v1.py` and matched them to module `view.py`: exactly #01–#09 and #12–#14 (12 APIs). The remaining 91 IDs do not have this route-plus-view source pair. API #10 has only bytecode caches in its module/test directories and no `.py` source files; API #11 has no module directory or test source.
- Runtime evidence remains separate: APIs #08/#09 have source and test files but are not runtime-verified after merge per `.agents/server-study/tests.md`; no tests were run for this count refresh.
- Re-ran `deno run --allow-read --allow-env scripts/validate-agent-context.mjs`: it remains `AGENT_CONTEXT_INVALID` because the checkout lacks the registered DB Admin context/source paths and baseline commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`; these are outside this Study Server inventory.

### Revalidation for the latest count request — 2026-10-23

- `PRIOR_WORKLOG_REVIEW`: Ran `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` and read `.agents/worklog/2026-10-23/create-study-api41-dd.md`, `create-study-api42-dd.md`, and `create-study-api43-dd.md`; no shortage.
- Re-counted endpoint rows in `docs/lists/list_api.md`: 103 rows, 103 unique IDs, continuous #01–#103.
- Re-counted numbered DD folders: 47 folders, #01–#47, with all eight core sheets; therefore #48–#103 (56 APIs) have no DD folder. Three standard reports exist in 35 folders (#13–#47); #01–#12 lack those reports but still have all eight core sheets.
- Re-read `apps/study-server/app/api/v1.py` and matched unique route API labels with module `view.py` files: #01–#09 and #12–#14, 12 API IDs. By the documented route-plus-view criterion, 12 are programmed and the remaining 91 (#10–#11 and #15–#103) have no matching route/view implementation pair.
- Runtime verification remains separate: #08/#09 are source-wired but post-merge runtime-unverified per `.agents/server-study/tests.md`. No application tests were run for this count request.
- Scope: this worklog only; no runtime, catalog, DD, or schema files changed in this count refresh.

## HANDOFF

- Remaining blockers: This is a source inventory, not an HTTP/runtime readiness audit; #08/#09 need post-merge runtime verification.
- Next owner/action: Continue DD creation with API #48 through #103; separately add the three report files to DD folders #01–#12 if completeness is required.
