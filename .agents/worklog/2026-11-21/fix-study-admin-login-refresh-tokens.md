---
task_id: "2026-11-21-fix-study-admin-login-refresh-tokens"
date: "2026-11-21"
primary_task_type: "fix"
secondary_task_types: ["test"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["Study Admin Web -> Study API #03 -> Study PostgreSQL schema"]
status: "PARTIAL"
---

# Worklog: Sửa lỗi đăng nhập Admin do thiếu refresh_tokens

## READ_PLAN

| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `AGENTS.md` | supplied router instructions | classify task, read-set and mutation requirements | `READ_FROM_CONTEXT` |
| `.agents/AGENTS.md` | global context and read-set rules | route scope and required worklog flow | `READ` |
| `.agents/context-map.md` | canonical load flow, Study Server and contract graph | identify scope/context dependencies | `READ` |
| `.agents/context-manifest.json` | server-study scope and fix workflow entries | verify registered context/workflow | `CHECKED_BY_TOOL` |
| `.agents/project/agent-control.md` | targets, worklog, source protection | track the database change and evidence | `READ` |
| `.agents/target.md` | active target table | create/remove the leaf target | `READ` |
| `.agents/worklog/README.md` | mandatory preflight/read-set | follow worklog workflow | `READ` |
| `.agents/worklog/TEMPLATE.md` | required sections | initialize this worklog | `READ` |
| `scripts/select-worklogs.mjs` | selector invocation | select prior fix worklogs | `CHECKED_BY_TOOL` |
| `scripts/validate-agent-context.mjs` | required registry/context validation | validate the context pages updated for live schema evidence | `CHECKED_BY_TOOL` |
| `.agents/worklog/2026-11-15/fix-st12-st26-visual-match.md` | carry-forward findings | preserve relevant fix conventions | `READ` |
| `.agents/worklog/2026-11-15/fix-st13-playwright-visual-audit.md` | carry-forward findings | preserve relevant verification limits | `READ` |
| `.agents/worklog/2026-11-01/fix-study-api-null-bind-parameters.md` | carry-forward findings | preserve Study Server fix conventions | `READ` |
| `.agents/project/INDEX.md` | database and dependency page routing | confirm cross-scope database ownership | `READ_FROM_CONTEXT` |
| `.agents/project/database.md` | Study DB source/status | identify migration and live-schema evidence | `READ` |
| `.agents/server-study/AGENTS.md` | scope instructions | apply Study Server rules | `READ` |
| `.agents/server-study/INDEX.md` | database/auth/test page graph | route relevant server context | `READ_FROM_CONTEXT` |
| `.agents/server-study/core/database-security.md` | database/security primitives | verify search_path and SQL execution conventions | `READ` |
| `.agents/server-study/database.md` | refresh-token schema status | distinguish migration artifact from live metadata | `READ` |
| `.agents/server-study/workflows/README.md` | fix workflow | follow Study Server verification workflow | `READ` |
| `.agents/project/workflows.md` | fix workflow | follow repository fix/reproduction order | `READ` |
| `apps/study-server/app/modules/guest/api_03_auth_login/view.py` | login transaction | trace credential success to token persistence/error response | `READ_FROM_CONTEXT` |
| `apps/study-server/app/modules/guest/api_03_auth_login/query.py` | refresh-token INSERT | identify required table/columns | `READ_FROM_CONTEXT` |
| `apps/study-server/app/api/v1.py` | API #03 route | verify login route wiring | `READ_FROM_CONTEXT` |
| `apps/study-server/app/core/database.py` | engine/search_path | ensure migration targets the configured schema | `READ_FROM_CONTEXT` |
| `apps/study-server/app/core/config.py` | runtime settings | identify environment/schema safely | `READ_FROM_CONTEXT` |
| `apps/study-server/app/utils/auth.py` | token issuance | distinguish token-config failure from persistence failure | `READ_FROM_CONTEXT` |
| `apps/study-server/app/core/security/password.py` | password verification | understand the successful-login path | `READ_FROM_CONTEXT` |
| `apps/study-server/tests/modules/guest/api_03_auth_login/test_auth_login.py` | success and persistence error cases | confirm expected API behavior | `READ_FROM_CONTEXT` |
| `infra/postgres/study-server/migrations/002_refresh_tokens.sql` | complete migration | apply the existing source-backed migration only | `CHECKED_BY_TOOL` |
| `apps/study-client/src/app/layouts/admin/admin-layout.ts` | error mapping | explain why HTTP 500 appears as generic feedback | `READ_FROM_CONTEXT` |
| `apps/study-client/src/app/layouts/admin/admin-layout.html` | sign-in flow | trace Admin form to handler | `READ_FROM_CONTEXT` |
| `apps/study-client/src/app/core/auth/admin-session.service.ts` | API #03 call and envelope parsing | trace handler to API request | `READ_FROM_CONTEXT` |
| `apps/study-client/src/app/core/http/study-api.service.ts` | request implementation | verify endpoint transport | `READ_FROM_CONTEXT` |
| `docs/prompts/build_server.md` | web launch rows | verify prior Study/Work Web command request is already represented | `READ_FROM_CONTEXT` |

## LEAF_TARGET_PLAN

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Áp dụng migration refresh token vào schema Study hiện hành | Apply the existing migration to the confirmed Study schema | `refresh_tokens` and its expected indexes exist in `dao_van_hung`; migration transaction commits |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `fix`
- selector_command: `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type fix --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-15/fix-st12-st26-visual-match.md`
    - carry_forward: preserve unrelated work and recheck current source.
  - path: `.agents/worklog/2026-11-15/fix-st13-playwright-visual-audit.md`
    - carry_forward: browser visual inspection is not runtime/API acceptance evidence.
  - path: `.agents/worklog/2026-11-01/fix-study-api-null-bind-parameters.md`
    - carry_forward: use current API #03 source/tests and live schema evidence separately.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: an active Admin with valid credentials can sign in; API #03 persists only a refresh-token hash and returns the auth envelope.
- Canonical contract/approved DD: current API #03 login flow and existing migration `002_refresh_tokens.sql`.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Áp dụng migration refresh token vào schema Study hiện hành | `0% → 0%` | Initial leaf target; completion requires the table and indexes in the confirmed runtime schema. |
| Áp dụng migration refresh token vào schema Study hiện hành | `0% → 100%` | Migration transaction committed to `neondb/dao_van_hung`; a new connection confirmed all six columns and four indexes. |

## CURRENT_BEHAVIOR

- Source/config: API #03 inserts into `refresh_tokens`; the relation was absent in `dao_van_hung` and is now present. `issue_tokens()` succeeds. The Admin UI maps 401/403/422/network errors and falls back to generic feedback for server errors.
- Runnable tests: focused API #03 test module passes all 15 cases; fake DB tests do not prove a successful login using the user's password.
- Runtime wiring: the running local Study Server points to database `neondb`, schema `dao_van_hung`; `admin@gmail.com` is `ADMIN/ACTIVE` there.

## SOURCE_TRACE

```text
AdminLayout.signIn -> AdminSessionService.login -> POST /api/v1/auth/login -> verify active user -> issue_tokens -> INSERT refresh_tokens -> SQLAlchemyError/500 when relation is absent -> generic Admin UI fallback
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Runtime schema lacked the table required by current API source | Pre-migration live metadata found no `refresh_tokens`; post-migration metadata confirms the relation and indexes | `FIXED_RUNTIME_VERIFIED` | Valid credential login can now persist the session |

## CHANGES

- Files changed: applied the existing migration to the database; updated this worklog and the active target tracker. No source/API change.
- CONTEXT_UPDATES: recorded the narrow live verification for `refresh_tokens` in `neondb/dao_van_hung`; other Study schema status remains unverified.
- Context pages changed: `.agents/server-study/database.md`, `.agents/project/database.md`.
- Assumptions: target remains `neondb/dao_van_hung`; `APP_ENV=local` is the running Study app configuration.
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `scripts/select-worklogs.mjs --type fix --limit 3` | 3 of 9 matching worklogs selected | `VERIFIED` |
| Read-only live metadata query for `admin@gmail.com` and `refresh_tokens` | Active Admin found; table absent in configured schema | `VERIFIED` |
| Existing migration `002_refresh_tokens.sql` | Committed to `neondb/dao_van_hung`; six columns and four expected indexes verified again using a new connection | `VERIFIED` |
| `./.venv/bin/pytest -q tests/modules/guest/api_03_auth_login/test_auth_login.py` | 15 passed; one upstream Starlette/httpx deprecation warning | `VERIFIED` |
| Live API #03 request with a deliberately invalid diagnostic password | HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`; no credential or token was exposed | `VERIFIED` |
| `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/validate-agent-context.mjs` | Exit 1 `AGENT_CONTEXT_INVALID`; baseline reports missing db-admin context/source, orphan skill resources, and broad stale-context paths. No repo-wide context repair was in scope. | `VERIFIED_WITH_BASELINE_FAILURES` |

## HANDOFF

- Remaining blockers: the positive browser login was not submitted because it requires the user's existing password.
- Next owner/action: user submits the already-open Admin login form and confirms the portal opens; if it fails, share the HTTP status and trace ID only.
