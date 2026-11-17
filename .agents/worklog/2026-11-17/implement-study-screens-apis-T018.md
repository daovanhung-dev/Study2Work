---
task_id: "2026-11-17-implement-study-screens-apis-T018"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work (Study Web)", "server-study"]
cross_scope_dependencies: ["SH-03 registration form -> Study Server API #01 POST /auth/register; API #02 is separate SH-04 handoff"]
status: "DONE"
---

# Worklog: Continue coding Study Web screens — T018 (SH-03)

## PRIOR_WORKLOG_REVIEW

- `primary_task_type`: `coding`
- `selector_command`: `node scripts/select-worklogs.mjs --type coding --limit 3`
- `selector_result`: `READY`; T011, T012 and T013 selected; no shortage.
- `prior_worklogs_reviewed`:
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md` — preserve API/DD discrepancies, source versus browser/live runtime evidence, and do not assume downstream behavior beyond source contracts.
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md` — broad goal remains all 83 screens and role-aligned Study APIs; preserve user dirty state and use focused FE/API tests with accurate runtime limits.
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T013.md` — do not wire unresolved Guest UI behavior merely because an API is source-wired; preserve DD gates and exact ID handling.
- `shortage`: `none`.

## EXPECTED_BEHAVIOR

- The broad active objective remains: organize Study Server API modules by role, code all 83 Study Web screens from DD/Stitch/catalogs, verify only source/contract-supported backend behavior, and keep `docs/tasks/process.md` current.
- T018 is the next bounded screen slice, SH-03 student registration at `/register`, API #01 only. API #02 belongs to the separate SH-04 email verification handoff and is not a SH-03 caller.
- Overall objective remains **20% ACTIVE**; this slice does not redefine the 83-screen/API goal.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 15% | 15% | Complete coding preflight; confirm SH-03 catalog row, route, DD locator and API ownership; read T011–T013 worklogs. | `DONE` |
| 65% | 80% | Read complete SH-03 DD/Stitch/design assets and API #01 DD/source/tests; trace current caller and implement the behavior-complete, contract-supported SH-03 slice below. | `DONE` |
| 20% | 100% | Run focused FE/API tests and build; safely demonstrate local route; update DD/context/tracker and worklog, run required validator/diff checks, record remaining gates. | `DONE` |

**Current T018 progress: 100%. Overall objective: 20% ACTIVE.**

## M0_CANDIDATE

- `list_screen.md` row 03 defines SH-03 `/register`, P0, API #01. Expected flow is POST #01 then a handoff to SH-04; current inventory says #01 caller is wired, 201 status is shown at SH-03, and SH-04 handoff remains blocked.
- `list_endpoint.md` rows #01/#02 separate POST `/auth/register` from POST `/auth/verify-email/send`; API #02 is not used by SH-03.
- `shared.route.ts` declares `/register` -> `SH03Page`; local Chrome direct-route smoke rendered `study-sh03-page` and its registration form. Production deployment remains unverified.
- Source file `SH03/pages/sh03-page.ts` exists and injects `SH03RegistrationService`; M1 will verify the complete DD, service/transport, backend, tests and current UI before choosing code changes.

## M1_SOURCE_TRACE

- Screen contract: the 8-file SH-03 DD and its Stitch plan require early email-format validation; API #01 remains the final validator. A successful result requires HTTP 201, `success=true`, `DESIGN_RESOURCE_CREATED`, and both `data.id` and `data.email`. Missing/wrong-shape fields must stop safely without claiming success or attempting a SH-04 handoff.
- Current caller chain: `/register` → `SH03Page.submit()` → `SH03RegistrationService.register()` → `StudyApiService.requestWithResponse()` descriptor `API_001` → public `POST /api/v1/auth/register`. Before T018, the page validated required/trimmed lengths only, trusted its compile-time result type and did not retain status; T018 adds trimmed email validation plus explicit 201/body runtime checks.
- API #01 source: FastAPI route returns HTTP 201; `validate_register_request` uses shared `EmailStr` normalization and max 255; `create_user` checks duplicates, hashes password, inserts/commits and returns the public row. It does not call API #02. DB status/default and account lifecycle remain a separate discrepancy.
- API #01 tests: `tests/modules/guest/api_01_auth_register/test_register.py` covers normalized inputs, malformed email before DB, 201 public response including `data.id`, 409 duplicate/race, 422 `meta.fieldErrors`, and safe 500/rollback. These are fake-session tests, not live DB/deployment evidence.
- API #01 DD is Draft and has unresolved profile/schema/account lifecycle questions. Those do not block the local email check, response-shape check, or existing #01 request contract. API #02 remains SH-04-owned.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| SH-03 / SH-04 handoff | Screen catalog/DD place API #02 at SH-04; transport and account lifecycle are unresolved. | `BLOCKED` | Do not call #02 or invent verification navigation from SH-03. |
| API #01 contract/current source | API route/view/validator and fake-session tests confirm 201, response fields, duplicate 409, validation 422 and safe 500; DD remains Draft. | `VERIFIED_SOURCE` / `DD DRAFT` | Use only source-backed response/error contracts; no live DB/deployment claim. |
| Existing SH-03 implementation | T018 adds email-format validation after trim, a response-aware request path, HTTP 201 and response-shape checks; focused tests/build pass. | `IMPLEMENTED` pending final diff/doc checks | API #01 remains authoritative; malformed success retains the form and password. |

## PRE_EDIT_PLAN

1. Read the full SH-03 8-section screen DD, source Stitch Markdown, plan/HTML/markers and both images; compare current form and success/error states to source-backed expectations.
2. Trace `SH03Page -> SH03RegistrationService -> StudyApiService/API_001 -> server route/view/validator/query/response -> database effects`; read API #01 DD, fake-session tests and relevant auth/security context.
3. Read the relevant route/page specs and current catalogs. Keep API #02 and SH-04 navigation separate unless #01's approved contract explicitly requires a handoff.
4. **Execution plan recorded before source edits:**
   - Add trimmed email-format validation through Angular's built-in email validator; preserve required and max-255 checks and do not add a password policy. A whitespace-padded valid email must continue to submit after trimming.
   - Add a response-aware request path to `StudyApiService` for the existing SH-03 caller, so the UI can validate the HTTP status as well as the body. Only HTTP 201 with `success`, `DESIGN_RESOURCE_CREATED`, positive integer `data.id`, and nonblank string `data.email` is created; otherwise retain the form/password and show the existing safe unresolved-result message. Do not store ID/email, navigate, or call API #02.
   - Add Angular regressions for malformed email causing no POST, whitespace-padded valid email still being trimmed/sent, malformed 201 payloads (missing ID/email) and a non-201 success envelope not claiming success or clearing password; retain the valid-201 regression.
   - Update only SH-03 current-source notes in screen DD, Stitch plan, screen inventory and test evidence after implementation; preserve DD Draft, API/account-lifecycle discrepancies and SH-04 handoff blocker.
5. Verify with focused Angular/API tests, production build, local browser route, context validation if context changes, and `git diff --check`.

## CHANGES

- `apps/study-client/src/app/core/http/study-api.service.ts`: add `requestWithResponse()` while preserving existing body-only callers, allowing SH-03 to read the transport status.
- `apps/study-client/src/app/features/shared/SH03/pages/sh03-page.ts`: validate trimmed email with Angular's email validator; treat response data as untrusted and require HTTP 201, `success`, success business code, positive integer `id` and nonblank `email` before entering created state or clearing password.
- `apps/study-client/src/app/features/shared/SH03/data-access/sh03-registration.service.ts`: return `HttpResponse<ApiEnvelope<unknown>>` from API #01 so runtime status/body checks are possible.
- `apps/study-client/src/app/features/shared/SH03/pages/sh03-page.spec.ts`: add invalid-email/no-request plus missing-id, missing-email and non-201-success regressions; existing padded-valid-email and valid-201 cases remain.
- `apps/study-client/docs/dd_screens/SH-03-DangKyHocVien/`: update overview, UI element, event, data-flow, API integration and test evidence to match current source and distinguish local render from deployment/live API.
- `apps/study-client/docs/list_screen.md` and SH-03 Stitch plan: update current-source notes, current test counts and local render evidence; keep the SH-04 blocker.
- T018 worklog and `docs/tasks/process.md`: record audit findings, pre-edit plan, M1/M2 progress; M2 verification remains until final diff checks.
- `CONTEXT_UPDATES`: none; source/DD state changes do not alter agent context pages.

## VERIFICATION

| Command / evidence | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | `READY`; T011–T013 selected; all three worklogs read in full. | `VERIFIED_PREFLIGHT` |
| Screen/API candidate inventory | SH-03 row 03 is P0 `/register` with #01; #02 belongs to SH-04. | `VERIFIED_CANDIDATE` |
| Current route/page presence | `/register` maps to `SH03Page`; page injects `SH03RegistrationService`. | `SOURCE_PRESENT` |
| Local route smoke | Direct Chrome route rendered `study-sh03-page` and the registration form. | `VERIFIED_LOCAL_RENDER` |
| `npm test -- --include src/app/features/shared/SH03/pages/sh03-page.spec.ts --include src/app/app.routes.spec.ts --include src/app/core/http/study-api.service.spec.ts` | 3 files, 27 tests passed. Covers invalid email, trim/body, valid/malformed 201, non-201 success body, mapped errors and API wrapper status response. | `VERIFIED` |
| `uv run pytest -q tests/modules/guest/api_01_auth_register/test_register.py` (from `apps/study-server`) | 16 passed; one Starlette/httpx deprecation warning; fake DB sessions. | `VERIFIED_SOURCE_TESTS` |
| `npm run build` | Passed; three existing Student CSS budget warnings (`student-static-screen.css`, `st22-page.css`, `student-layout.css`). | `VERIFIED_BUILD` |
| `GET /register` + Chrome headless | HTTP 200; hydrated local route and form rendered at desktop 1365×900/mobile 390×844; no submit. | `VERIFIED_LOCAL_RENDER`; live API/deployment not verified |
| `git diff --check` | Passed with no whitespace errors. Explicit trailing-whitespace scan of changed TypeScript/worklog/process paths returned no matches. | `VERIFIED_CLEAN` |

## HANDOFF

- Remaining gates outside this slice: SH-04 handoff transport/account lifecycle; email delivery and confirmation; live schema/API/deployment. API #01 DD remains Draft.
- Next action: continue the broad all-screens/API objective with the next source-supported screen slice; overall objective remains 20% ACTIVE.
