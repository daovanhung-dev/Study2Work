---
task_id: "2026-10-11-centralize-study-auth-token-helpers"
date: "2026-10-11"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tập trung helper xác thực và token của Study Server

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-04/study-db-schema-per-transaction-reapply.md`
    - carry_forward: Preserve unrelated worktree changes; callers own DB transactions; record context-validator baseline accurately.
  - path: `.agents/worklog/2026-09-28/remove-study-apiresponse.md`
    - carry_forward: Keep the Study scope narrow and use current source/tests as runtime evidence.
  - path: `.agents/worklog/2026-09-28/study-apierror-direct-json.md`
    - carry_forward: Preserve auth status/business-code mappings, keep query and transaction ownership in views, and record context updates.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Place reusable application-level bearer/JWT/refresh-token helpers in `app/utils/auth.py`; update Study Server callers to import through it while preserving current response and business behavior.
- Canonical contract/approved plan: Keep JWT/HMAC primitives in `app/core/security`; keep password helpers, SQL, and API #3 transaction ownership in their existing layers; retain existing behavior tests and update their import/mock targets.

## CURRENT_BEHAVIOR

- Source/config: `utils/auth.py` currently owns token issuance and public auth payload mapping. Bearer parsing and claim validation are in `utils/validate.py`; the Student request guard is in API #4 `validate.py`; API #3 view directly imports `hash_refresh_token` from `core.security`; API #3 refresh input validation duplicates the blank-token check.
- Runnable tests: Existing utility, API #3, API #4, API #14, and core security token tests cover the relevant behaviors. API #4/API #14 tests patch `decode_access_token` through the API #4 validator module.
- Runtime wiring: API #4 and API #14 use the same Student guard; API #3 owns refresh-token database lookup/rotation and transaction boundaries.
- Pre-existing worktree: `D A`, `D FETCH_HEAD`, `D git` are zero-byte paths and `api_14_users_me_profile/validate.py` contains a user-added `#edit` marker on the API #4 guard import. Preserve the unrelated deletions and retain the marker while changing that import target.

## SOURCE_TRACE

```text
API #3 RefreshRequest -> validate_refresh_request -> utils.auth.validate_refresh_token -> error_response or normalized request
API #3 login/refresh view -> utils.auth issue/hash helpers -> caller-owned SQL transaction -> success/error response
API #4/API #14 -> shared utils.auth current-user guard -> core JWT decoder -> profile query/update in view -> response
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Application auth helper ownership is split | Current source places Bearer/claim/current-user checks in `utils/validate.py` and API #4 validator, with a direct API #3 hash import from core security | DISCREPANCY | Consolidate app-facing helpers in `utils/auth.py` without moving cryptographic implementations. |
| Study context assigns auth helpers to `utils/validate.py` | Current context pages and manifest list old ownership/path | CONTEXT_STALE | Update relevant Study pages and required source paths with the code change. |

## CHANGES

- Files changed: `apps/study-server/app/utils/auth.py`, `app/utils/validate.py`, `app/utils/__init__.py`, API #3 validator/view, API #4 view (removed its auth-only validator), API #14 validator, the existing API #3/#4/#14 and utility tests, Study README, `.agents/context-manifest.json`, affected `.agents/server-study/` pages, and this worklog.
- CONTEXT_UPDATES: Moved application-level Bearer/JWT/refresh helper ownership to `utils/auth.py`; removed API #4's redundant validator module; recorded API #14 reuse and updated verified test count to 191.
- Context pages changed: `.agents/server-study/AGENTS.md`, `architecture.md`, `core/database-security.md`, `modules/README.md`, `tests.md`, `workflows/README.md` and `.agents/context-manifest.json`.
- Assumptions: Keep `core/security` primitive implementations and their direct unit tests; preserve user changes outside this task.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected and reviewed three matching coding worklogs; no shortage | VERIFIED |
| Source/import scan before edits | Identified application imports and test patch targets for token/auth helpers | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest tests/utils/test_validate.py tests/modules/guest/api_03_auth_login/test_auth_login.py tests/modules/guest/api_04_users_me/test_users_me.py tests/modules/guest/api_14_users_me_profile/test_users_me_profile.py -q` | 66 passed; one existing Starlette/httpx deprecation warning | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest -q` | 191 passed; one existing Starlette/httpx deprecation warning | VERIFIED |
| `cd apps/study-server && .venv/bin/ruff check app tests` | All checks passed | VERIFIED |
| `git diff --check` | No whitespace errors | VERIFIED |
| Study app auth/token import scan | No app caller imports token functions from `utils/validate.py`, API #4 validator or core token modules; only `utils/auth.py` imports low-level primitives, while `core/security` owns their implementation/exports | VERIFIED |
| `deno run -A scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID`: existing missing DB Admin context/source plus source-drift findings across repository scopes, including Study snapshot drift | CONTEXT_BASELINE |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_INVALID` only for pre-existing missing DB Admin context/source and links; no Study structural error | CONTEXT_BASELINE |

## HANDOFF

- Remaining blockers: Repository-wide context validation remains invalid due to the missing DB Admin context/source baseline; this task did not modify that scope.
- Next owner/action: None for the Study auth/token refactor.
