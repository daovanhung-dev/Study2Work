---
task_id: "2026-11-18-implement-study-auth-session"
date: "2026-11-18"
primary_task_type: "coding"
secondary_task_types: ["test"]
project_scopes: ["web-work"]
cross_scope_dependencies: ["server-study API #03, #04 and R-X01"]
status: "VERIFIED"
---

# Worklog: Study Web auth session

## PRIOR_WORKLOG_REVIEW

- primary_task_type: coding
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - `.agents/worklog/2026-11-15/implement-st11-static-layout.md`: preserve Student layout and route wiring.
  - `.agents/worklog/2026-11-15/implement-st12-st26-static-layouts.md`: Student screens include static and API states.
  - `.agents/worklog/2026-11-13/commit-study-api-registry.md`: consume the typed API registry.
- shortage: none

## EXPECTED_BEHAVIOR

- User request: accept login tokens, send Bearer headers, navigate by role, handle expiry, and logout.
- Source contract: Study Server API #03 returns access/refresh tokens, expiries and role; #04 is STUDENT-only; R-X01 refreshes the session.

## MILESTONES

| Weight | Cumulative | Objective / acceptance | Status |
|---:|---:|---|---|
| 30% | 30% | Verify source payload, routes and storage boundary | DONE |
| 50% | 80% | Implement session, interceptor, guard, login and logout | DONE |
| 20% | 100% | Build, tests and live route check | DONE |

## CURRENT_BEHAVIOR

- Before: SH-02 deliberately discarded a successful login response and Student routes lacked a guard.
- After: frontend auth flow implemented; live backend login remains blocked by missing `refresh_tokens` table in the connected database.

## SOURCE_TRACE

```text
SH-02 -> LoginApi #03 -> AuthSessionService -> API #04 for STUDENT -> router
HttpClient -> authInterceptor -> Bearer / R-X01 -> Study Server
Student route -> studentAuthGuard -> StudentLayout logout -> session clear
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| SH-02 DD success contract versus current server payload | SH-02 DD and `build_auth_payload` | DISCREPANCY | Implementation uses current server source at user's request. |
| Live login | Connected schema lacks `refresh_tokens` | BLOCKED_BACKEND | Cannot finish real login until backend schema is updated. |

## CHANGES

- Files changed: `core/auth/*`, `app.config.ts`, Student route/layout, SH-02 page/service/spec, Study context index, this worklog.
- CONTEXT_UPDATES: Study Web index records source auth wiring and live backend blocker.
- Assumptions: `sessionStorage` scopes the login to one tab; logout clears local state because Study Server has no logout endpoint.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `npm run build` | Passed; pre-existing SH-01 CSS budget warning | VERIFIED |
| `npm test -- --watch=false` | 64/64 after #04, guard and logout/refresh race tests | VERIFIED |
| Browser `/student` without session | Redirected to `/login?returnUrl=%2Fstudent` | VERIFIED |

## HANDOFF

- Remaining blocker: backend schema must provide `refresh_tokens` before live login can complete.
- Next owner/action: rerun full frontend suite and live login after backend repair.


## FINAL_VERIFICATION

- Frontend: 64/64 tests passed; production build passed with the existing SH-01 CSS budget warning.
- Live guest route: /student redirected to /login?returnUrl=%2Fstudent.
- Agent context validator: AGENT_CONTEXT_INVALID from pre-existing missing db-admin pages and broad source drift; not introduced by this auth change.
