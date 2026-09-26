---
task_id: "2026-09-26-refactor-study-api4-validation"
date: "2026-09-26"
primary_task_type: "coding"
secondary_task_types: ["test", "context-maintenance"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Refactor validation Study API #4 vào utils

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-26/load-study-server-coding-context.md`
    - carry_forward: Giữ boundary Study hiện tại, dùng `.venv` để verification và không suy diễn live DB từ artifact.
  - path: `.agents/worklog/2026-09-26/refactor-study-api3-validation.md`
    - carry_forward: Shared validators nằm trong `app/utils/validate.py`; module-local wrapper không giữ lại nếu không có logic riêng.
  - path: `.agents/worklog/2026-09-23/split-study-api-dd-folders.md`
    - carry_forward: Giữ namespace API-ID, route/response/query/transaction contract hiện tại.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Đưa `extract_bearer_token` và `validate_access_claims` vào `app/utils/validate.py` để tái sử dụng.
- API #4 import trực tiếp shared validators; xóa module-local `validate.py` và cập nhật context manifest/pages.
- Giữ nguyên header Bearer, claim shape, ValueError/message, role `STUDENT`, response và auth flow.

## CURRENT_BEHAVIOR

- `api_04_users_me/validate.py` hiện chứa cả hai hàm pure validator.
- `api_04_users_me/view.py` là caller runtime duy nhất; view giữ orchestration, query và response mapping.
- `app/utils/validate.py` đã là boundary cho shared pure validators của API #3.

## SOURCE_TRACE

```text
Authorization header
-> app/utils.validate.extract_bearer_token
-> access_token decoder
-> app/utils.validate.validate_access_claims
-> STUDENT authorization
-> current-user query/response in API #4 view
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #4 validator location | Current source keeps both functions in module-local `validate.py`; requirement moves them to shared utils | RESOLVED_FOR_IMPLEMENTATION | Update imports, tests and context; delete exact unused module path |
| Public behavior | Existing API4 tests cover Bearer parsing, claims, 401/403/500 and profile response | NO_DISCREPANCY | Preserve runtime behavior and response contract |
| Live database | Not involved in pure validation refactor | OUT_OF_SCOPE / LIVE_NOT_VERIFIED | No DB, query or migration changes |

## CHANGES

- Moved `extract_bearer_token` and `validate_access_claims` to
  `apps/study-server/app/utils/validate.py` with the existing signatures,
  messages and behavior.
- Exported both validators from `app/utils/__init__.py`; API #4 view now imports
  them directly from shared utils.
- Deleted `apps/study-server/app/modules/guest/api_04_users_me/validate.py`.
- Added utility coverage for Bearer parsing, claim validation, role
  normalization and invalid claim/header cases.
- Updated `.agents/server-study/AGENTS.md`, `architecture.md`,
  `modules/README.md` and `.agents/context-manifest.json` for the new boundary.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected and read 3 matching coding worklogs | VERIFIED |
| `.venv/bin/pytest tests/modules/guest/api_04_users_me/test_users_me.py tests/utils/test_validate.py -q` | 41 passed; existing Starlette/httpx deprecation warning | VERIFIED |
| `.venv/bin/pytest -q` | 154 passed; existing Starlette/httpx deprecation warning | VERIFIED |
| `.venv/bin/ruff check app tests` | All checks passed | VERIFIED |
| `.venv/bin/mypy app` | No issues found in 58 source files | VERIFIED |
| `git diff --check` | No whitespace errors | VERIFIED |
| legacy import/path checks | No `api_04_users_me.validate` reference; deleted path absent; validators defined only in shared utils | VERIFIED |
| composition/shared-export check | API #4 route remains in OpenAPI; both shared exports import and behave correctly | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |

## HANDOFF

- API #4 validator boundary is now shared and verified. The existing
  repository-wide full context validator drift status remains outside this
  task; the requested `--skip-drift` validation passed.
