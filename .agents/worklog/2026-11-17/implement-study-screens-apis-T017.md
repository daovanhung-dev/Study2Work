---
task_id: "2026-11-17-implement-study-screens-apis-T017"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work (Study Web)", "server-study (API contract/source/tests)"]
cross_scope_dependencies: ["SH-02 login -> Study Server API #03 login and #04 current Student profile; login/role session handoff"]
status: "DONE"
---

# Worklog: Continue coding Study Web screens — T017 (SH-02)

## PRIOR_WORKLOG_REVIEW

- `primary_task_type`: `coding`
- `selector_command`: `node scripts/select-worklogs.mjs --type coding --limit 3`
- `selector_result`: `READY`; T011, T012 and T013 selected; no shortage.
- `prior_worklogs_reviewed`:
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md`
    - carry-forward: AD-22/#97 is a bounded read-only slice; #98 remains downstream; retain report source/schema/permission gates.
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md`
    - carry-forward: broad goal remains role-aligned APIs plus all 83 Study Web screens; GS01/GS03 are source-wired and fake-session tests do not verify live runtime.
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T013.md`
    - carry-forward: do not wire a screen across unresolved API/DD decisions; GS04/#09 access, display, timing and layout gates remain open.
- `shortage`: `none`.
- Additional prior slice: T016 SH-01 completed with DD/API approval and live API/DB limitations recorded; overall objective remains 20% ACTIVE.

## EXPECTED_BEHAVIOR

- Full objective remains: organize Study Server API packages by role (`admin`, `student`, `mentor`, `guest`, `shared`); implement all 83 Study Web screens from DD, Stitch and catalogs; verify/fix/add APIs only when requirements and source support them; resolve conflicts by tracing DD/BD; deliver source-backed UI/UX connected to backend; write a detailed plan before changes.
- Current bounded candidate: SH-02 `Đăng nhập`, `/login`, P0, APIs #03 and #04 per `list_screen.md`.
- `Study FE scope: screens=SH-02 Đăng nhập (/login); APIs=#03 POST /api/v1/auth/login, #04 GET /api/v1/users/me`. #02 is excluded because it belongs to SH-04 verification handoff and is currently an email dispatch stub.
- Cross-scope dependency: API #03/#04 Study Server request/response/auth/error behavior and tests. Preserve catalog/DD/source disagreements; no token/session, role redirect, credential persistence or auth claims may be invented.
- Overall objective remains **20% ACTIVE** at T017 start.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 10% | 10% | Complete required context/worklog preflight; read current screen/API catalogs and route source; select and record a bounded next screen/API scope. | `DONE` |
| 65% | 75% | Read full SH-02 DD/Stitch/image/HTML/marker evidence, API #03/#04 DD and current source/tests; write a pre-edit plan; implement the largest behavior-complete subset supported by verified contracts without inventing auth/session/role policy. | `DONE` |
| 25% | 100% | Run focused frontend/backend verification and build; demonstrate the local route safely; synchronize current-source docs/context, run required validator and diff check, and update tracker/worklog with remaining blockers. | `DONE` |

**Current T017 progress: 100%. Overall objective: 20% ACTIVE.**

## CURRENT_BEHAVIOR

- Current Angular route: root route lazy-loads `shared.route.ts`; `/login` mounts `SH02Page` inside `SharedLayout`.
- Current SH02 component provides a responsive required email/password form, password visibility toggle, accessible unavailable state and prevents native submission; it has no API caller.
- API #03 is a public Guest endpoint. Current source returns HTTP 200 with safe profile and access/refresh tokens, while the normative list/DD contract remains HTTP 201 `UserProfile` with only 422/500. The view persists only a refresh-token hash and commits after token issuance.
- API #04 is Student-only; its current source rejects non-Student roles and uses the same 401 code for invalid authentication and missing profile.
- `AdminSessionService` calls #03 and keeps token material in tab memory only for Admin routes. It does not establish Student/shared session policy.
- Current source wires `/register` to `SH03Page`; local direct-route Chrome smoke rendered `study-sh03-page` and the registration form. Deployed runtime is not verified.

## SOURCE_TRACE

```text
SH-02 /login -> SH02Page -> (caller not wired in current page source)
candidate: screen-local data-access -> StudyApiService #03 -> FastAPI login
candidate: #03 result -> role/session handoff -> optional Student-only #04
candidate: verified API response/error -> page state -> approved destination
```

Caller-to-DB/response trace: #03 looks up `users.email`, verifies `password_hash`, checks `status == ACTIVE`, issues tokens, inserts the refresh-token hash and commits; #04 validates Bearer/JWT claims and STUDENT role before querying the public profile fields. The SH02 page currently calls neither API.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #03 contract | `list_api.md`/DD expect HTTP 201 `UserProfile` and 422/500; AC-02 and current view use HTTP 200, 401/403, profile plus token pair. | `DISCREPANCY / VERIFIED` | Do not enable an auth success flow until response/status and session contract are approved. |
| API #04 audience | Current source guard and DD restrict #04 to STUDENT; same 401 is used for invalid auth and missing profile. | `SOURCE_BACKED / VERIFIED` | Do not call #04 for Mentor/Admin or use every 401 as a refresh signal. |
| SH-02 design assets | Original `screen.png` is blank; numbered/rendered images derive from `code.html`; markers #1–#8 map to SH02-EL-01..08. | `PROVENANCE_VERIFIED` | Treat as a documented visual reference, not a production approval. |
| SH-03 navigation | `shared.route.ts` maps `/register` to `SH03Page`; local Chrome direct-route smoke rendered the page/form; SH-02 DD had stale unwired claims. | `RESOLVED_LOCAL_ROUTE` | Correct current-source notes; deployed runtime remains unverified. |
| Role/session handoff | Catalog includes “safe token storage” and remembered destination; current approved storage/redirect contract has not yet been verified. | `OPEN` | Do not persist credentials, create redirects, or enable an incomplete success path by assumption. |

## PRE_EDIT_PLAN

1. Keep current SH02 source: the verified display/validation/accessibility subset already exists, and no additional interaction can be completed without choosing an unapproved API/session/role/redirect policy.
2. Correct SH-02 DD current-source statements that say `/register` is unwired; preserve expected-flow statements and label browser runtime unverified.
3. Run focused SH-02 UI and API #03/#04 source tests, then Study Web production build and a safe `/login` route smoke/demo. Do not use live credentials or a live database.
4. Record verification, run `git diff --check`, update T017 and `docs/tasks/process.md`, and retain auth/session decisions as explicit blockers.

### Verification plan

- `cd apps/study-client && npm test -- --include=src/app/features/shared/SH02/pages/sh02-page.spec.ts`
- `cd apps/study-server && uv run pytest -q tests/modules/guest/api_03_auth_login/test_auth_login.py tests/modules/student/api_04_users_me/test_users_me.py`
- `cd apps/study-client && npm run build`
- Start the local Study Web dev server and inspect `/login` through a browser; do not submit credentials.
- Run `node scripts/validate-agent-context.mjs` because the T017 package current-source notes and progress/worklog were changed; compare with the repo-wide baseline recorded in T016.
- Run `git diff --check` and search SH-02 DD for remaining claims that `/register` is unwired.

## CHANGES

- Files changed: T017 worklog, T017 row in `docs/tasks/process.md`, and current-source notes in SH-02 `01-ui-elements.md`, `02-events.md`, `03-data-flow.md`, `05-business-rules.md`, and `06-navigation.md`. No SH02 component source changed because remaining auth behavior is contract-gated.
- `CONTEXT_UPDATES`: no `.agents` router/context manifest page changed. SH-02 DD package current-source notes were synchronized in the five files listed above; `/register` is locally rendered, while deployment remains unverified.
- Assumptions: SH-02 is the next P0 Shared screen after SH-01, confirmed by the current screen catalog and `/login` route source. This is a bounded continuation, not a replacement for the all-83-screen/API goal.

## VERIFICATION

| Command / evidence | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | `READY`; T011–T013 selected and read in full. | `VERIFIED_PREFLIGHT` |
| Current screen/API catalogs | 83 screen rows; SH-02 P0 `/login`, APIs #03/#04; API #03 catalog response discrepancy and #04 Student audience recorded. | `VERIFIED_CANDIDATE` |
| Current route/page source | `shared.route.ts` registers `/login` -> `SH02Page`; form submit is currently disabled/prevented. | `VERIFIED_ROUTE_ONLY` |
| Full SH-02/API audit | Read the eight SH-02 DD sections, Stitch plan/HTML/markers/images, API #03/#04 DD and source, caller chain, and source tests. Individual rereads confirmed conclusions after one batched output was truncated. | `VERIFIED_M1` |
| `npm test -- --include=src/app/features/shared/SH02/pages/sh02-page.spec.ts` | SH02 page: 3/3 tests passed. | `PASS` |
| `uv run pytest -q tests/modules/guest/api_03_auth_login/test_auth_login.py tests/modules/student/api_04_users_me/test_users_me.py` | 32 passed; one Starlette/httpx deprecation warning. Fake sessions do not verify live DB/deployment. | `PASS_SOURCE_TESTS` |
| `npm run build` | Production build passed. Three existing Student CSS budget warnings for `student-static-screen.css`, Student layout, and ST22; no SH02 warning. | `PASS_WITH_EXISTING_WARNINGS` |
| Local route smoke and visual review | `/login` and `/register` direct routes rendered with HTTP 200; headless Chrome DOM includes `study-sh02-page`, `study-sh03-page`, form headings, unavailable note and registration link. `/login` screenshots at 1365×900 and 390×844 rendered after a 5s virtual-time budget. Initial immediate captures were blank before Angular hydration and were discarded. | `PASS_LOCAL_RENDER` |
| SH-02 DD stale-route search | `rg` found no remaining claims that `/register` is unwired. | `PASS` |
| `node scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID`, exit 1 with 1,431 output lines, matching T016 baseline; repo-wide DB Admin missing source/context, orphan resources and stale context findings remain. | `KNOWN_BASELINE_FAILURE` |
| `git diff --check` | No whitespace errors. | `PASS` |

## HANDOFF

- Remaining blockers: API #03 normative response/status versus current-source token/status discrepancy; approved session/refresh/logout policy; Mentor/Admin bootstrap; #04 Student-only usage and 401 discriminator; approved `returnTo` and role destinations. The clean Stitch PNG is blank, so the rendered HTML remains a provenance-backed visual reference.
- Next action: begin the next screen under a new coding worklog. SH-02 is display-complete and submit-gated; implementation of authentication requires API/session/role policy decisions outside this source-only slice.
