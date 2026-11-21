# PLAN â€” Study login session (temporary implementation)

## Metadata and approval

- Task: `2026-11-17-study-fe-auth-session`
- Base SPEC: [`SPEC.md`](./SPEC.md)
- Approved SPEC SHA256: `A1C7E4CFC765F8F717B56571AE2952F601D00DD78375067570A5C7360B03E08E`
- PLAN revision SHA256: recorded in the approval receipt and worklog (external to this file).
- Approval: `PENDING_APPROVAL`; source edits are authorized only after approval of this exact PLAN revision.
- Verification constraint: do not add/edit test files or run tests/build unless the user separately asks for verification, per the approved SPEC and active instruction.
- Worktree constraint: preserve all pre-existing modifications and untracked files; stage nothing.

## Implementation order and dependencies

1. Recheck the exact current source and worktree before edits; only touch paths listed below.
2. Implement backend cookie/Origin behavior and source-only logout first, reusing existing refresh-token hash persistence and rotation. Do not change schema or apply DB migrations.
3. Implement the FE in-memory session, interceptor and Student route guard against those endpoint contracts. Keep the FE and BE contract changes in the same release set because the current refresh body and login payload will change.
4. Reconcile only SH-02, API #03, API catalog and FE registry statements directly affected by this implementation. Preserve unrelated DD open questions.
5. Perform the approved non-test handoff checks: inspect scoped diffs, confirm no secrets/token values were added, run `git diff --check` on tracked modifications and a whitespace check of new artifacts, inspect `git status` to confirm unrelated files remain untouched. Do not claim runtime/deployment verification.

## Implementation steps

| Step | Weight | Requirements | Files / owners | Change and acceptance |
|---|---:|---|---|---|
| P01 â€” BE auth cookie and Origin boundary | 25% | REQ-AUTH-04, REQ-AUTH-05 | `apps/study-server/app/api/v1.py`; `app/modules/guest/api_03_auth_login/view.py`, `models.py`, `validate.py`, `query.py`; `app/utils/auth.py`; `app/core/config.py` and `app/core/constants.py` only for explicit cookie Secure configuration | Read Origin on login/refresh/logout and require exact membership in configured `cors_origins` before DB access. Set/clear the refresh cookie with the approved attributes. API #03 and R-X01 return access token/profile data without refresh-token fields. Make R-X01 bodyless while preserving atomic token rotation. Add bodyless source-only R-X02 logout that revokes the cookie token using existing query/transaction helpers, clears cookie, and assigns no numeric API ID. No schema change. |
| P02 â€” FE session and transport | 20% | REQ-AUTH-02, REQ-AUTH-03 | `apps/study-client/src/app/core/auth/` (new auth service, interceptor and guard); `core/http/study-api.service.ts`; `core/constant/api.constants.ts`; `app.config.ts` | Own access token and auth state in one per-tab service. Add R-X02 and credentialed auth request support to typed descriptors/transport. Attach Bearer through the interceptor without replacing an existing Authorization header; exclude auth endpoints from recursion. Share one in-flight refresh and retry each protected request at most once. |
| P03 â€” Student login, guard and cross-tab behavior | 20% | REQ-AUTH-01, REQ-AUTH-03, REQ-AUTH-06 | `features/shared/SH02/pages/SH-02-login-page.ts`; `SH-02-login.service.ts`; `SH-02-login.models.ts`; `features/student/student.route.ts`; new `core/auth/` files | Type the approved login response. Keep only Student session; call #04 before navigating to `/student`. Guard Student routes and restore with R-X01 on entry/reload. Broadcast secret-free session replacement/logout events; sibling tabs clear in-memory/user-specific state and reload to resolve the shared cookie session. Do not read/write token Web Storage. |
| P04 â€” Contract and DD reconciliation | 20% | REQ-AUTH-06 | `docs/lists/list_api.md`; `apps/study-client/docs/list_endpoint.md`; SH-02 `00-overview.md`, `03-data-flow.md`, `04-api-integration.md`, `07-test-cases.md`; API #03 `02_Overview.md`, `03_Request.md`, `04_Response.md`, `05_Data_Mapping.md`, `07_table.md`, `OPEN_QUESTIONS.md`; FE API registry | Update only contract statements affected by approved login/refresh/logout behavior. Keep #03 at HTTP 200, document R-X01/R-X02 as source-only without inventing a numeric ID, close only the approved auth questions, and retain unrelated unresolved DD gaps. Mark runtime/deployment as unverified. |
| P05 â€” Scoped static review and handoff | 15% | All requirements | Approved FE/BE/DD paths above; worklog | Review scoped source and documentation changes; confirm browser-readable storage contains no token, cookie attributes and Origin checks match SPEC, Student routes are guarded, cross-tab messages carry no secrets, no unrelated dirty files were changed, and no tests/build were run. Run whitespace/status inspection only. Report unverified runtime/topology and any blocked static check accurately. |

## File-level guardrails

- No `localStorage`, `sessionStorage`, IndexedDB, URL, logging, or analytics use for access/refresh token values.
- Do not add auth headers to arbitrary external URLs; interceptor is limited to the Study API base path.
- Do not refresh after 403 or retry login/refresh/logout. The original request is retried no more than once.
- Do not decode client JWT claims to grant roles. API #04 and all protected BE endpoints remain authoritative.
- Do not introduce an API numeric ID for refresh/logout. Use the explicitly source-only registry markers `R-X01` and `R-X02` and preserve that status in docs.
- Origin matching is exact against configured CORS origins. Do not enable wildcard credentialed CORS or accept a missing Origin on cookie-auth routes.
- Production cookie `Secure` must remain enabled. Disabling it is permitted only by explicit local-development configuration; deployment values are not verified here.
- The refresh cookie policy assumes FE and API are same-site. A cross-site deployment is blocked pending a separately approved cookie/CSRF design.
- Preserve all unrelated changes visible in the current dirty worktree; do not reset, stage, or commit files.

## Risks and compatibility

- API #03 currently returns refresh token fields in JSON and R-X01 currently accepts a JSON body. The approved contract removes those fields/body. No in-repository FE refresh consumer exists, but external consumers were not checked; deploy FE and BE contract changes together and do not claim external compatibility.
- A cookie shared by same-origin tabs means concurrent accounts in one browser profile are unsupported. Cross-tab notifications carry no credentials and force sibling tabs to resolve the current account.
- `SameSite=Lax` plus Origin allowlisting assumes same-site deployment. Runtime CORS origins, TLS termination, browser behavior and database availability are not verified.
- Existing refresh-token database artifacts are source evidence only; no live schema or migration is inspected/changed in this plan.
- No tests/build will be run and no test files will be changed under the current instruction. Consequently this task will not claim automated regression coverage or runtime correctness.

## Verification and approval

- Tests/build: `NOT_RUN` and test files unchanged unless the user separately requests verification.
- Runtime/browser/DB: `NOT_RUN`; deployment topology and live schema remain unverified.
- Context validator: run only if implementation edits registered `.agents` context pages; otherwise report not applicable. Worklog update alone does not change scope context pages.
- Status: `PENDING_APPROVAL`
- Approver: pending
- Approved revision SHA256: pending
- Decision date: pending
