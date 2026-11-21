---
task_id: "2026-11-21-implement-sh02-sh07-notification-workflow"
date: "2026-11-21"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies:
  - "SH-02 API #03 current 200 profile/token contract and role sessions"
  - "SH-03 API #01 to SH-04 one-use registration handoff; SH-04 API #02 stub semantics"
  - "SH-05 Student API #04 refresh/replay and normalized 401/403 route handoff"
  - "SH-07 API #18 UUID owner-bound notification lookup fed by APIs #63/#93; AD-20 recipient list via #68"
status: "VERIFIED"
---

# Worklog: Hoàn thiện SH-02 đến SH-07 và notification tracking

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-21/complete-sh01-to-100-T044.md`
    - carry_forward: Keep the approved static four-axis rubric (UI, UX, logic, API at 25 points each) distinct from live runtime; preserve unrelated dirty files; focused tests/build and browser evidence are separate.
  - path: `.agents/worklog/2026-11-21/load-full-project-web-coding-context-T042.md`
    - carry_forward: Follow Study Web page/data-access/model/UI separation and only load true cross-scope dependencies.
  - path: `.agents/worklog/2026-11-21/prepare-study-web-screen-coding-T043.md`
    - carry_forward: Read full screen DD and source assets, trace current caller/API behavior, and keep unavailable or unsupported behaviors explicit.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement the approved plan for SH-02–SH-07 and the approved notification producer handoffs, then update the screen completion report to 100% for SH-02–SH-07 under the repository's static four-axis rubric.
- Canonical contract/approved DD: Keep API #03 aligned to current Study Server HTTP 200 auth payload; no login `returnTo`; API #02 202 is only stub acceptance; refresh/replay API #04 once on 401 and never on 403; SH-06 is a generic 404 shell with `/courses` and `/` links; SH-07 tracks notification operations only via UUID, owner-bound API #18 with manual refresh; connect ME-14/#63 and AD-20/#93, with #63 `content` changed to text and AD-20 recipients explicitly selected through #68.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| `Hoàn thiện SH-02 đến SH-07 và nối luồng notification SH-07` | `0% → 100%` | `screen_complete.md` records SH-02–SH-07 at 100% under the static UI/UX/logic/API rubric; focused Study Web tests pass 11 files/36 tests, and the linked Study Server suites pass 87 tests. Browser/live API/DB/provider remain explicitly unverified. |

## CURRENT_BEHAVIOR

- Source/config after implementation: SH-02 consumes current API #03 HTTP 200 `LoginData`, stores the role session and routes to the role home without `returnTo`; SH-03 calls #01 and passes a one-use in-memory handoff to SH-04; SH-04 calls #02 only on explicit user action and treats HTTP 202 as accepted stub state. SH-05 performs one R-X01 refresh and one safe GET replay after #04 401, skips refresh on 403, and uses an internal back target or `/` fallback. SH-06 renders the minimal 404 and links to `/courses` and `/`; #08 404 maps there while #08 500 remains distinct. SH-07 validates UUIDs and calls owner-bound notification-only #18 on entry and manual refresh, without polling. ME-14/#63 and AD-20/#93 route accepted UUIDs into SH-07; AD-20 recipients come from #68 and are explicitly selected. API #63 accepts text `content`.
- Runnable tests: Focused Study Web run passed 11 files / 36 tests. Combined #03/#18/#63/#68/#93 Study Server run passed 87 tests with one upstream Starlette/httpx deprecation warning; #63 Ruff passed. No live API, DB, provider, or browser behavior is claimed.
- Runtime wiring: Requested Angular routes, data-access calls and local notification/outbox source are wired. Full client build/test remains blocked by pre-existing unrelated GS-06/GS-07/ME-04 compile errors and ST-10 spec setup error recorded in T044; browser tooling/runtime and live service deployments remain unverified.

## SOURCE_TRACE

```text
SH02Page -> SH02LoginService -> StudyApiService #03 -> role session manager -> Student-only StudentApiService #04 -> role route / SH05 error handoff -> tests
SH03Page -> SH03RegistrationService -> StudyApiService #01 -> one-use SH04RegistrationHandoffService -> SH04Page -> SH04VerificationService #02 -> accepted/error state -> tests
StudentApiService #04 -> StudentSessionService R-X01 + one safe GET replay on 401 -> SH05 normalized route state; 403 skips refresh -> tests
ME14Page -> ME14NotificationCreateService #63 -> notification/outbox transaction -> Operation UUID response -> SH07 route -> role-authenticated API #18 -> notification/outbox query owner-bound to JWT subject -> status response -> tests
AD20Page -> AdminApiService #68 explicit recipient pages -> selected IDs -> #93 notification/outbox transaction -> meta.operation_id UUID -> SH07 route -> API #18 -> tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #03 success status/body | Server source is HTTP 200 profile+tokens; catalog/DD says 201 UserProfile-only. | `DISCREPANCY` approved for reconciliation to current server source | Update API #03 and SH-02 DD/catalog evidence; preserve existing server behavior. |
| API #02 delivery | Default provider returns 202 accepted and sends no email; no confirmation API exists. | `SOURCE_BACKED_STUB` approved screen scope | UI must never claim delivered or verified. |
| API #18 generic contract | Current handler is UUID, notification-only, owner-bound; generic payment/export/lifecycle remains absent. | `SCOPE_NARROWED` by user | SH-07 and API #18 DD scoped to source-backed notification status only. |
| API #63 content | Current request model is int64 while ME-14 edits text and storage is TEXT. | `DISCREPANCY` approved for change to text | Update model, validator, view, tests, API DD/catalog and client mapping. |
| SH-06 AC-05 403 | API #08 source supports 404/500; 403 is not returned by #08. | `DISCREPANCY` approved to align DD/AC with source | Route 403 through access-denied behavior, not SH-06. |

## CHANGES

- Files changed: SH-02–SH-07 Shared pages/services/models/specs; ME-14 and AD-20 notification producer pages, data access and specs; Study Server API #63 model/view/tests; API catalog and screen/API DDs for #03/#18/#63/#93; `screen_complete.md`; Study Web and Study Server agent context pages; this worklog.
- CONTEXT_UPDATES: Reconciled current source and test evidence with Study Web/Server context. API #03 documents HTTP 200 profile+tokens; API #18 describes the source-backed notification-only UUID owner lookup while leaving generic lifecycle/result open; API #63 uses `content:string`; AD-20/#93 recipient and UUID metadata flow is recorded. Current-versus-historical screen DD notes were reconciled for SH-07 and its ME-14/AD-20 producers.
- Context pages changed: `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/server-study/AGENTS.md`, `architecture.md`, `apis/declared-routes.md`, `core/runtime.md`, `database.md`, `modules/README.md`, `tests.md`, and `workflows/README.md`; API #03/#18/#63/#93 DD support notes and `docs/lists/list_api.md` were synchronized.
- Assumptions: “100%” is the repository's static four-axis score (UI/UX/logic/API, 25 points each) for SH-02–SH-07, within the user-approved scope. It does not mean browser/live API/DB/deployment/provider runtime is verified. HTTP 202 represents accepted/queued work only.
- Target progress updates and completion evidence: `0% → 100%` after focused UI/API suites passed and screen statuses were updated. The completed target row is removed from `.agents/target.md` per repository control rules.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `cd apps/study-client && npm test -- --include=src/app/features/shared/SH02/**/*.spec.ts --include=src/app/features/shared/SH03/**/*.spec.ts --include=src/app/features/shared/SH04/**/*.spec.ts --include=src/app/features/shared/SH05/**/*.spec.ts --include=src/app/features/shared/SH06/**/*.spec.ts --include=src/app/features/shared/SH07/**/*.spec.ts --include=src/app/features/admin/AD20/**/*.spec.ts --include=src/app/features/mentor/ME14/**/*.spec.ts --include=src/app/core/data-access/student-api.service.spec.ts --include=src/app/core/data-access/mentor-api.service.spec.ts` | 11 files passed; 36 tests passed. | `VERIFIED` |
| `cd apps/study-server && uv run pytest -q tests/modules/guest/api_03_auth_login/test_auth_login.py tests/modules/shared/api_18_operations/test_operations.py tests/modules/mentor/api_63_mentor_notifications_create/test_mentor_notifications_create.py tests/modules/admin/api_68_admin_users_list/test_admin_users_list.py tests/modules/admin/api_93_admin_notifications_create/test_admin_notifications_create.py` | 87 passed; one upstream Starlette/httpx deprecation warning. | `VERIFIED` |
| `cd apps/study-server && uv run ruff check app/modules/mentor/api_63_mentor_notifications_create tests/modules/mentor/api_63_mentor_notifications_create` | All checks passed. | `VERIFIED` |
| Scoped `git diff --check` for SH-02–SH-07, ME-14, AD-20, API #63 and related screen/DD/context files | No whitespace errors. | `VERIFIED` |
| `node scripts/validate-agent-context.mjs` | Exit 1; output is byte-identical to pre-task baseline `/tmp/t043-validator-baseline.log`. Existing missing db-admin scope/source and broad registry/source errors remain baseline issues. | `PREEXISTING_INVALID_BASELINE` |
| Prior full Study Web `npm test` / `npm run build` (recorded in T044, not rerun here) | Unrelated pre-existing GS-06/GS-07/ME-04 compile errors and ST-10 spec setup error; scoped target tests compile and pass. | `BLOCKED_BY_OUT_OF_SCOPE_SOURCE` |
| Browser/live API/DB/deployment/provider checks | Not verified. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Generic API #18 payment/export lifecycle and result contracts, live schema/deployment/provider delivery, browser runtime, and unrelated full-client compile errors remain outside the verified target slice.
- Next owner/action: Target complete; no further SH-02–SH-07 implementation work remains in this task.
