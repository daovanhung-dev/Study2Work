---
task_id: "2026-10-23-refresh-study-api-dd-implementation-counts"
date: "2026-10-23"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Refresh Study API DD and implementation counts

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-23/create-study-api41-dd.md`
    - carry_forward: API #41 DD exists; Study API DD output is Markdown-only and endpoint implementation must be checked against current source.
  - path: `.agents/worklog/2026-10-23/create-study-api42-dd.md`
    - carry_forward: API #42 DD exists; prior inventory counted through #41 and needs a fresh count after #42.
  - path: `.agents/worklog/2026-10-23/create-study-api43-dd.md`
    - carry_forward: API #43 has an in-progress worklog only; do not count it as a created DD until its folder/files exist.
- shortage: `none` (63 matching worklogs available; 3 selected and read)

## EXPECTED_BEHAVIOR

- Requirement: Determine the number of Study API DDs created/not created and APIs programmed/not programmed.
- Canonical denominator: `docs/lists/list_api.md` states 103 unique designed APIs and 113 API-card occurrences; count by unique API ID.

## CURRENT_BEHAVIOR

- DD artifacts: `apps/study-server/docs/dd/` contains 47 numbered folders, #01–#47. Every folder has sheets `00_Cover.md` through `06_Error.md` and a `07_*.md` sheet. Folders #01–#12 lack the three reports; folders #13–#47 have all 11 required Markdown files.
- Implementation source: `app/api/v1.py` has route handlers for API IDs #01–#09 and #12–#14; each has a matching module `view.py`. This is 12 programmed/wired unique API IDs. API #03 exposes login and refresh routes but is counted once by catalog ID.
- Unimplemented catalog IDs: 91 have no current route-plus-module-view implementation in the Study router.
- Runtime evidence: API #08/#09 source and test modules exist but merged-tree import/HTTP behavior remains unverified. API #02 uses a development stub and does not send real email.
- Runnable tests: Not run; this is a static inventory task.

## SOURCE_TRACE

```text
list_api.md unique API rows (1–103) -> numbered DD folders and required sheets -> app/api/v1.py API route IDs -> matching guest module view.py files
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| DD folders #01–#12 | Core sheets exist; `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md` are missing | `INCOMPLETE_DELIVERABLES` | Count as DDs created, while distinguishing 35 full 11-file packs from 12 incomplete packs. |
| API #08/#09 runtime proof | Route/module/test source exists; post-merge runtime verification is not recorded | `SOURCE_PRESENT / RUNTIME_UNVERIFIED` | Count as programmed in source, not as runtime-verified. |
| API #02 external delivery | Current provider is a development stub | `PARTIAL_EXTERNAL_BEHAVIOR` | Route is programmed; real email delivery is not implemented. |
| Catalog versus implementation | Catalog has 103 unique IDs; route-plus-view source covers 12 IDs | `DISCREPANCY` | 91 IDs have no current Study route-plus-view implementation. |

## CHANGES

- Files changed: This refreshed inventory worklog only. The related API #47 DD/report/worklog update is recorded separately in `create-study-api47-dd.md`.
- CONTEXT_UPDATES: None; no runtime, DD, catalog, schema, or context-page changes.
- Assumptions: “Programmed” means registered in `app/api/v1.py` with a matching current module `view.py`; this does not assert runtime verification or complete external integrations.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector and review | Selected and read three `docs` worklogs; no shortage. | `VERIFIED` |
| Catalog count | Endpoint rows in sections GUEST through ADMIN contain 103 contiguous unique IDs, #01–#103; catalog summary says 113 API-card occurrences. Count uses unique API IDs, not error-code rows or repeated operation cards. | `VERIFIED` |
| DD folder/sheet inventory | 47 folders #01–#47; no missing core sheets; 12 lack the three reports; 35 have all 11 files. | `VERIFIED` |
| Router/module inventory | Route ID set equals module `view.py` ID set: #01–#09, #12–#14 (12 IDs); 91 catalog IDs have no route-plus-view pair. | `VERIFIED` |
| Study runtime tests | Not run; not requested. #08/#09 remain runtime-unverified after merge. | `NOT_RUN` |
| Context validator | `node` is unavailable; Deno compatibility run completed and reported pre-existing missing DB Admin context/source roots and unavailable baseline commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`. | `BLOCKED_UNRELATED_REPO_CONTEXT` |

## HANDOFF

- Remaining blockers: None for static counting; this does not prove merged-tree runtime behavior.
- Next owner/action: Continue creating DDs from API #48 onward; separately complete the missing report files for DDs #01–#12 if full packs are required.

## CURRENT REQUEST REFRESH — 2026-10-23

- Re-ran the docs worklog selector; it selected #41, #42 and #43. All three worklogs were read in full; no shortage.
- Re-counted only endpoint rows in the catalog sections GUEST through ADMIN: 103 unique IDs (#01–#103). The catalog's 113 card occurrences are not the denominator.
- Current DD count: 47 folders (#01–#47), all with the eight core sheets; 56 catalog IDs (#48–#103) have no DD folder. 35 folders (#13–#47) also have the three reports; #01–#12 remain report-incomplete.
- Current source count: 12 route-plus-`view.py` IDs (#01–#09, #12–#14) and 91 catalog IDs without that source pair. #08/#09 are source-backed but post-merge runtime-unverified; #02 still uses a delivery stub.
- `deno run --allow-read --allow-env scripts/validate-agent-context.mjs` returned `AGENT_CONTEXT_INVALID` for missing DB Admin context/source roots and missing baseline commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`; these unrelated paths do not affect the static Study API counts.
- No application tests were run. The result is a static source/document inventory only.
