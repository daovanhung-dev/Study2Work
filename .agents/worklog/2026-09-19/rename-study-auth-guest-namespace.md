---
task_id: "2026-09-19-rename-study-auth-guest-namespace"
date: "2026-09-19"
primary_task_type: "coding"
secondary_task_types: ["fix", "test", "context-maintenance"]
project_scopes: ["server-study"]
cross_scope_dependencies:
  - ".agents/context-manifest.json"
  - ".agents/project/dependencies.md"
  - ".agents/project/source-status.md"
status: "VERIFIED"
---

# Worklog: Đổi namespace Study `auth` thành `guest`

## PRIOR_WORKLOG_REVIEW

- primary_task_type: coding
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-18/configure-local-service-addresses.md`
    - carry_forward: Study full pytest collection previously bị block bởi stale `app.modules.auth.view`; dùng focused tests và ghi rõ toolchain/blocker.
  - path: `.agents/worklog/2026-09-18/work-server-rest-api-hardening.md`
    - carry_forward: Không mở rộng sang route/contract chưa được source-backed; phân biệt runtime source với DD/contract.
  - path: `.agents/worklog/2026-09-18/work-server-study-style-refactor.md`
    - carry_forward: Khi đổi module boundary phải cập nhật affected context pages và chạy validator với drift status rõ ràng.
- shortage: `none`

## EXPECTED_BEHAVIOR

- User-approved plan: đổi namespace nội bộ `app.modules.auth` thành `app.modules.guest` để đồng bộ module.
- Giữ nguyên public endpoint `/api/v1/auth/register`, request/response, business codes, SQL, DD path và error-path matching.
- Không tạo alias ngược `app.modules.auth`.

## CURRENT_BEHAVIOR

- `app/api/v1.py` và `register_account/view.py` import `app.modules.auth.register_account.*`.
- Register test nằm dưới `tests/modules/auth/` nhưng import các path stale `app.modules.auth.models/view`.
- Context manifest và project/server-study pages còn tham chiếu namespace `auth`.
- Composition root import được; focused Study tests pass; full collection bị stale register import.

## SOURCE_TRACE

```text
app/main.py:create_app
-> app/api/v1.py:router
-> app.modules.auth.register_account.{models,view,query}
-> POST /api/v1/auth/register
-> tests/modules/auth/test_register.py
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Namespace | Current source uses `auth`; approved plan requires `guest` | DISCREPANCY | Update internal imports/path only |
| Public route | Current route and DD use `/api/v1/auth/register` | VERIFIED / PRESERVE | Do not rename endpoint |
| Register test | Imports removed `app.modules.auth.models/view` | DECLARED_NOT_RUNNABLE | Update to `app.modules.guest.register_account.*` and verify collection |
| DB/API contract | No schema or public response change requested | OUT_OF_SCOPE | No migration or contract rewrite |

## CHANGES

- Files changed: renamed Study register module/test directories, updated runtime/test imports, updated manifest, project dependency/source-status pages and server-study pages.
- CONTEXT_UPDATES: registered `guest/register_account`, changed Study test status from collection blocker to verified, and documented that `/auth` remains the public endpoint contract.
- Context pages changed: `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/context-manifest.json`, `.agents/project/dependencies.md`, `.agents/project/source-status.md`, and affected `.agents/server-study/*` pages.
- Assumptions: test directory follows the internal namespace rename; historical worklogs and public `/auth` DD names remain unchanged.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected 3 matching coding worklogs; all read | VERIFIED |
| `grep` internal namespace scan | No `app.modules.auth`, `app/modules/auth`, `tests/modules/auth` or `auth_view` references remain in Study source/tests/context outside historical worklogs | VERIFIED |
| `cd apps/study-server && .venv/bin/python -c 'from app.main import app; ...'` | Import pass; `/api/v1/auth/register` present; `/api/v1/guest/register` absent; guest model import pass | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest --collect-only -q` | 43 tests collected without collection error | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest -q tests/modules/guest/test_register.py` | 15 passed, 1 deprecation warning | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest -q` | 43 passed, 1 deprecation warning | VERIFIED |
| `git diff --check` | Passed | VERIFIED |
| `python3 -m json.tool .agents/context-manifest.json` | Manifest parsed successfully | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Existing `CONTEXT_STALE` for Study snapshot and other scopes | CONTEXT_STALE |

## HANDOFF

- Remaining blockers: full context validator remains invalid because the repository snapshot predates current Study/Work/Web/DB Admin source; no runtime blocker remains for this namespace rename.
- Next owner/action: review the rename diff; do not update the global source snapshot solely to suppress the pre-existing drift.
