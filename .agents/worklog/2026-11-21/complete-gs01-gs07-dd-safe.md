---
task_id: "2026-11-21-complete-gs01-gs07-dd-safe"
date: "2026-11-21"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies:
  - "Study Web GS-01–GS-07 consume public Study Server APIs #05–#12; current server routes/query/response and focused tests provide contract evidence. No server runtime or schema behavior was changed."
status: "VERIFIED"
---

# Worklog: Hoàn thiện Study Web GS-01–GS-07 theo phạm vi DD-safe

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 157 available; 3 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-21/complete-sh01-to-100-T044.md`
    - carry_forward: The screen score is UI/UX/logic/API at 25 points each; keep the static score distinct from live runtime; preserve existing dirty source; Study Web guide is canonical; tests and browser evidence must be reported separately.
  - path: `.agents/worklog/2026-11-21/implement-sh02-sh07-notification-workflow.md`
    - carry_forward: Prior full build/test had GS06/GS07/ME04 compile issues and ST10 spec setup; re-check current files and repair only in-scope GS issues.
  - path: `.agents/worklog/2026-11-21/load-full-project-web-coding-context-T042.md`
    - carry_forward: Study Web is Angular 22 and follows page/UI/data-access/model separation; use registered `study-web-screen-coding`; source and API contracts outrank stale docs; preserve the dirty worktree.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete GS-01–GS-07 under the approved DD-safe scope and repository's static four-axis rubric; implement supported behavior, keep unsupported features gated, and do not change server API/schema behavior.
- User-approved scope: static 100% for UI/UX/logic/API; category/facet/price/rating/enrollment/lesson preview/MIME-specific preview/expiry and unapproved resource production remain gated. Runtime verification is reported separately.
- Canonical sources: `apps/study-client/docs/list_screen.md`, `apps/study-client/docs/list_endpoint.md`, DD packages `GS-01`–`GS-07`, `.agents/web-study/design.md`, `.agents/web-study/frontend-rules.md`, `.agents/web-work/study/workflows/screen-implementation.md`, API catalog/DD #05–#12 and current Study Server source.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| `Hoàn thiện các màn GS-01 đến GS-07 theo phạm vi DD-safe` | `0% → 0%` | Initial target; acceptance requires UI, UX, logic and API evidence across all seven screens. |
| `Hoàn thiện các màn GS-01 đến GS-07 theo phạm vi DD-safe` | `0% → 99%` | Static behavior and focused evidence complete; final diff/context validation remained. |
| `Hoàn thiện các màn GS-01 đến GS-07 theo phạm vi DD-safe` | `99% → 100%` | Focused client specs 37/37, Study APIs #05–#12 119/119, scoped diff check passed, and context-validator output matches the pre-task baseline exactly. The active row is removed on completion per Agent Control. |

## CURRENT_BEHAVIOR

- Source/config: initial tracker had GS-01/02/03/06/07 at 62.5% and GS-04/05 at 50%. GS-04/05/06 are nested under GS-03 tabs; GS-07 is a resource route. Preserve unrelated pre-existing dirty source.
- API callers: GS-01 #05/#06; GS-02 #07; GS-03 #08 and lazy #09/#10/#11; GS-06 #11; GS-07 #12. Current #11 source returns PUBLIC `Resource[]` ordered by ID and `200 []` when empty. Current #12 supports public direct URLs and private Student/ACTIVE-enrollment signed URLs (300 seconds). Live schema/storage remain unverified.
- Unsupported behavior: category/facets, currency formatting, rating/aggregate, enrollment, lesson/media preview, resource expiry UI and resource data producer remain gated by contract/source evidence.
- Runnable tests: initial GS-focused compilation exposed missing GS06/GS07 response-state imports; these in-scope compile issues were repaired. Final focused Guest tests pass 37/37 and Study API #05–#12 fake-source tests pass 119/119.
- Runtime wiring: local routes/callers exist. Browser rendering, live API, DB/storage and deployment were not verified.

## SOURCE_TRACE

```text
Guest routes -> GS01 #05/#06; GS02 #07; GS03 #08 -> lazy GS04 #09 / GS05 #10 / GS06 #11 -> GS07 #12 -> StudyApiService or StudentApiService -> current Study Server routes
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Demo-only fields/actions in DD assets | Current source/contracts do not support category filters, facets, currency, rating aggregate, safe enrollment, lesson preview or MIME preview policy. | `GATED_BY_USER_APPROVED_DD_SAFE_SCOPE` | Only source-backed fields/actions are displayed. |
| API #11/#12 tests and context | Current source #11 returns PUBLIC array/empty array and #12 handles private Student auth/signed URLs; stale tests/context expected singleton/404 and no signer. Tests/context now aligned. | `RESOLVED_IN_TEST_AND_CONTEXT; SOURCE_BEHAVIOR_UNCHANGED` | No Study Server runtime/schema code was modified. Live service remains unverified. |
| Resource producer/live schema | No Study writer for `resources` was found; #47 writes `lesson_uploads`; checked-in schema does not prove deployment. | `NOT_VERIFIED` | Resource availability, schema and storage remain runtime questions. |
| Full Angular production build | `npm run build` reports NG5002 in unrelated `ME04/pages/me04-page.html:304` (unclosed `@else`/EOF); no GS compile errors are reported. | `BLOCKED_OUT_OF_SCOPE_BASELINE` | Leave ME04 unchanged; focused GS Angular test build passes. |

## CHANGES

- GS-01: fail closed on non-PUBLISHED #06 rows; preserve/retry list rows on count/list mismatch and keep unsupported category filters gated.
- GS-02: make result cards navigate to GS-03 by response ID; add retry for API failure and page-one recovery for out-of-range; validate PUBLISHED rows and suppress stale totals/paging on mismatch.
- GS-03/GS-04: validate course route IDs as positive signed-int64 strings; add #08/#09 retry actions; sort curriculum display by `order`; keep title/order only; mount resource tab after published-course verification.
- GS-05: keep returned review rows on count/list mismatch, suppress stale pagination, retry errors/mismatches, and provide page-one recovery when page becomes out-of-range. Do not render unapproved title/rating.
- GS-06/GS-07: validate #11 public resource list and add GS-07 links with return context; call #12 through public or Student API path; distinguish 401/403/404; validate response identity and HTTP(S) URL; retry transient failures and open URLs with `noopener noreferrer`.
- Updated GS-focused tests, replacing stale GS06/GS07 placeholder assertions. Aligned API #11/#12 test expectations to current source and added empty/multi-row/public/private signed-URL/enrollment coverage; no server API/schema behavior changed.
- Updated `apps/study-client/docs/screen_complete.md`, `apps/study-client/docs/list_screen.md`, `.agents/web-work/study/INDEX.md`, and Study Server scope/docs (`AGENTS.md`, `modules/README.md`, `apis/declared-routes.md`, `tests.md`).
- Assumptions: 100% means the static four-axis score for the user-approved DD-safe scope. Browser/live runtime, DB/schema/storage and deployment remain separate and unverified.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | `READY`; three selected prior coding worklogs were read and recorded above. | `VERIFIED_PREFLIGHT` |
| `npm test -- --include=src/app/features/guest/GS01/pages/gs01-page.spec.ts --include=src/app/features/guest/GS02/pages/gs02-page.spec.ts --include=src/app/features/guest/GS03/pages/gs03-page.spec.ts --include=src/app/features/guest/GS05/pages/gs05-page.spec.ts --include=src/app/features/guest/GS06/pages/gs06-page.spec.ts --include=src/app/features/guest/GS07/pages/gs07-page.spec.ts` | 6 files passed; 37 tests passed. GS-04 is covered by GS-03 curriculum panel tests. | `VERIFIED` |
| `uv run pytest -q tests/modules/guest/api_05_categories/test_categories.py tests/modules/guest/api_06_courses/test_courses.py tests/modules/guest/api_07_courses_search/test_courses_search.py tests/modules/guest/api_08_courses_detail/test_courses_detail.py tests/modules/guest/api_09_courses_curriculum/test_courses_curriculum.py tests/modules/guest/api_10_courses_reviews/test_courses_reviews.py tests/modules/guest/api_11_courses_resources/test_courses_resources.py tests/modules/guest/api_12_resources_detail/test_resources_detail.py` | 119 passed, 0 failed; one upstream Starlette/httpx `TestClient` deprecation warning. | `VERIFIED_LOCAL_SOURCE` |
| `uv run ruff check tests/modules/guest/api_11_courses_resources/test_courses_resources.py tests/modules/guest/api_12_resources_detail/test_resources_detail.py` | All checks passed. | `VERIFIED` |
| `npm run build` | Build stops at unrelated `ME04/pages/me04-page.html:304` with NG5002 unclosed `@else`/EOF. No GS compile errors were reported. | `BLOCKED_OUT_OF_SCOPE_BASELINE` |
| `git diff --check -- <GS source/tests, tracker, worklog and updated context paths>` | No output; exit 0. | `VERIFIED` |
| `node scripts/validate-agent-context.mjs` | Exit 1 due existing repository-wide missing db-admin context/source and orphan resource/stale-context findings. Output is byte-for-byte identical to `/tmp/t043-validator-baseline.log`, both with target at 99% and after removing the completed target row. | `BASELINE_FAILURE_NO_NEW_FINDINGS` |

## HANDOFF

- Remaining blockers: live browser/API/DB/storage/deployment are unverified; full Angular build is blocked by unrelated ME-04 template syntax. The approved static GS-01–GS-07 scope is complete.
- Next owner/action: no more local GS implementation is required for this target; handle ME-04 separately if a full-app build is required.
