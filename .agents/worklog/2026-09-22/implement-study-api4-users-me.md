---
task_id: "2026-09-22-implement-study-api4-users-me"
date: "2026-09-22"
primary_task_type: "coding"
secondary_task_types: ["test", "context-maintenance"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["Study API#3 JWT claims", "users table read contract"]
status: "VERIFIED"
---

# Worklog: Implement Study API#4 users/me

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-20/implement-study-auth-login-refresh.md`
    - carry_forward: Giữ JWT runtime hiện tại, transaction ownership ở module view, query parameterized, không expose password/token; API#3 dùng `sub`/`roles` và đã có focused tests.
  - path: `.agents/worklog/2026-09-20/merge-mobile-flavors.md`
    - carry_forward: Giữ source-backed boundary và không overwrite thay đổi ngoài phạm vi task.
  - path: `.agents/worklog/2026-09-20/publish-develop-to-github.md`
    - carry_forward: Không commit hoặc thay đổi ngoài phạm vi implementation.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement `GET /api/v1/users/me` theo DD API#4 với Bearer JWT, Student authorization, canonical envelope và profile read-only response.
- Contract decision: Giữ current JWT claims `sub` + `roles`; omit `bio` vì không có source column; user-not-found map về `401` theo DD assumption.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py` hiện chưa expose `/users/me`; API#3 decoder validates `sub`/`roles` runtime shape only partially; `users` source schema có profile columns trừ `bio`.
- Runnable tests: Study `.venv` có pytest/ruff/mypy; baseline collection đã đạt 58 tests.
- Runtime wiring: `main.py` composes the v1 router; DB helper is sync SQLAlchemy; query helpers do not commit.

## SOURCE_TRACE

```text
GET /api/v1/users/me
-> route header extraction + trace
-> users_me.validate.py bearer/claim validation
-> core.security.access_token.decode_access_token
-> users_me.query.py SELECT users by sub/user_id
-> users_me.view.py role/error/profile mapping
-> core.responses canonical envelope
-> focused API tests + full Study tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API#4 route/module | Current router has no users/me route or module | UNWIRED | Add the smallest source-backed implementation |
| DD normative source | DD is Draft and references missing `docs/lists/list_api.md` | EXPECTED_BEHAVIOR / NOT_FOUND | Use explicit DD fields and current runtime conventions; do not invent missing fields |
| JWT claims | DD says `user_id`/`role`; API#3 creates `sub`/`roles` | DISCREPANCY | Preserve API#3 runtime claims to avoid breaking login/refresh |
| `users.bio` | DD lists optional `bio`; current users schema has no column | DISCREPANCY | Omit `bio`; do not add schema |
| Live DB metadata | Runtime connection exists but live table status is not verified here | SOURCE_REQUIRED | Add no migration and do not claim live DB verification |

## CHANGES

- Files changed: Added `app/modules/guest/users_me/{__init__,models,validate,query,view}.py`, `tests/modules/guest/test_users_me.py`, and wired `GET /api/v1/users/me` in `app/api/v1.py`.
- CONTEXT_UPDATES: Registered API#4 as source-backed, documented current JWT `sub`/`roles` compatibility, Student-only authorization, public profile projection and test coverage.
- Context pages changed: `.agents/server-study/AGENTS.md`, `apis/declared-routes.md`, `architecture.md`, `modules/README.md`, `tests.md`, `.agents/project/source-status.md`, and Study business/event/HTTP catalogs.
- Assumptions: API is Student-only; role comparison accepts normalized `STUDENT`; no token format change.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected 3/8 coding worklogs; all read | VERIFIED |
| `.venv/bin/pytest --collect-only -q` | 58 tests collected before implementation | VERIFIED |
| `.venv/bin/pytest tests/modules/guest/test_users_me.py tests/modules/guest/test_auth_login.py -q` | 27 passed | VERIFIED |
| `.venv/bin/pytest tests/modules/guest/test_users_me.py -q` | 17 passed | VERIFIED |
| `.venv/bin/pytest -q` | 75 passed, 1 dependency deprecation warning | VERIFIED |
| `.venv/bin/ruff check app tests` | All checks passed | VERIFIED |
| `.venv/bin/mypy app` | No issues found in 37 source files | VERIFIED |
| `git diff --check` | No whitespace errors | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` when run from repository root | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Existing `CONTEXT_STALE` across deep scopes; no map/registry error | CONTEXT_STALE |

## HANDOFF

- Remaining blockers: Live DB schema/table availability is not verified; full context validator still reports pre-existing source drift; test suite emits one Starlette/httpx deprecation warning.
- Next owner/action: Apply/verify the existing Study database schema in the target environment before relying on the endpoint against live data; no code changes remain for API#4.
