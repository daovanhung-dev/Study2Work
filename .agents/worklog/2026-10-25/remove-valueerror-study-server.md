---
task_id: "2026-10-25-remove-valueerror-study-server"
date: "2026-10-25"
primary_task_type: "fix"
secondary_task_types: ["coding", "test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Loại bỏ ValueError khỏi Study Server

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `fix`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type fix --limit 3` (`node` không có trong PATH)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-28/study-middleware-single-exception-path.md`
    - carry_forward: Giữ nguyên status, business code, safe message, trace header và field-error metadata khi sửa đường xử lý lỗi.
  - path: `.agents/worklog/2026-09-27/remove-study-exceptions-module.md`
    - carry_forward: `error_response(...)` là serializer lỗi chuẩn; cập nhật mọi caller/test/context khi đổi helper chung.
  - path: `.agents/worklog/2026-09-18/work-server-constants.md`
    - carry_forward: Work Server là scope riêng; không áp convention Study sang Work.
- shortage: `none` (selector có 3 fix worklogs)

## EXPECTED_BEHAVIOR

- Requirement: Không dùng hoặc tham chiếu built-in `ValueError` trong Python source/tests của `apps/study-server`; API-facing validation/business errors trả qua `error_response(...)`. Lỗi ngoài HTTP tiếp tục dùng cơ chế nội bộ, không biến thành `JSONResponse`.
- Canonical contract/approved plan: Giữ nguyên HTTP status, business code, message, trace ID, field errors và side effects; cập nhật scope context/workflow theo rule mới.

## CURRENT_BEHAVIOR

- Source/config: Built-in `ValueError` đã được loại bỏ khỏi Study Server Python source/tests. Shared auth/validation/course helpers trả `ErrorDetail`, sentinel hoặc dữ liệu kết quả; API validators/views ánh xạ lỗi HTTP bằng `error_response(...)`. Config và lỗi nội bộ tiếp tục đi qua đường xử lý ngoài HTTP.
- Runnable tests: Focused course API #6/#7/#46 suite có 71 tests pass; full Study suite có 271 tests pass. Ruff pass.
- Runtime wiring: API #46 auth/query/mapping, shared auth and normalization, guest API validators/course views, config, trace, JWT/password security và Ollama adapter đều đã chuyển khỏi việc dùng built-in `ValueError`. Thay đổi API #46/error envelope/context có sẵn trước task được giữ nguyên.

## SOURCE_TRACE

```text
request -> route -> shared auth/normalization/course helper -> API validator/view -> error_response/success response -> tests
settings/security/trace/service helper -> non-HTTP caller/test (không được trả JSONResponse chỉ để thay exception)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #46 used `ValueError` before this change | Previous validator/view mapped thrown helper and mapping errors; current validator/view return typed validation results and use existing response helpers. | `RESOLVED_IN_TASK` | 401/403/422/500 mappings and success/error envelope remain covered by tests. |
| Shared Study code used `ValueError` before this change | Initial inventory found references in shared helpers, guest APIs, core config/security/trace and service code; current Python source/tests scan has zero matches. | `RESOLVED_IN_TASK` | Callers/tests were updated and non-HTTP failures remain internal. |
| Existing worktree | API #46 source/tests/context and shared response changes are already uncommitted. | `PRESERVE_EXISTING_CHANGES` | Modify only the requested error flow and canonical context; do not stage or overwrite unrelated edits. |

## CHANGES

- Shared helpers return typed failures (`ErrorDetail`, `None` or a result union); API-facing validators/views map HTTP failures through `error_response(...)` while preserving status, business code, trace and rollback behavior.
- Config validators use Pydantic custom errors and `Settings` sanitizes validation failures as `RuntimeError`; JWT/password/Ollama paths validate input or catch specific dependency errors.
- Bcrypt verification validates canonical hash encoding and password byte length before calling bcrypt; malformed input safely returns `False`.
- Shared course count mapping validates aggregate values without implicit integer parsing failures; API #6/#7/#46 return the existing internal error response for malformed database counts.
- Context pages updated: `.agents/server-study/AGENTS.md`, `modules/README.md`, `workflows/README.md`, `core/database-security.md`, and `tests.md`. Current suite count refreshed to 271.
- Worktree also contains prior uncommitted API #46, route/response-envelope/context and load-context changes; preserved without staging or commit.
- Assumption: no explicit built-in `ValueError` identifier may remain in Study Server Python source/tests; HTTP errors use response helpers, while non-HTTP failures remain internal.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type fix --limit 3` | Selected and read all three available matching fix worklogs. | VERIFIED |
| Initial Python `ValueError` inventory | Source usage identified across API, shared helpers, core and service layers; test references identified in util/config tests. | VERIFIED_STATIC_ONLY |
| `cd apps/study-server && ./.venv/bin/pytest -q tests/modules/guest/api_06_courses/test_courses.py tests/modules/guest/api_07_courses_search/test_courses_search.py tests/modules/mentor/api_46_mentor_courses/test_mentor_courses.py` | 71 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| `cd apps/study-server && ./.venv/bin/pytest -q` | 271 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| `cd apps/study-server && ./.venv/bin/ruff check app tests` | All checks passed. | VERIFIED |
| Python identifier scan under `apps/study-server/app` and `tests` | Scanned 116 Python files; 0 matches. | VERIFIED_STATIC_ONLY |
| `git diff --check` | No whitespace errors. | VERIFIED_STATIC_ONLY |
| `/home/daovanhung/.local/node-v24.21.0-linux-x64/bin/node scripts/validate-agent-context.mjs` | Exit 1. Missing DB Admin context/source paths; `CONTEXT_STALE` compares tracked trees to the older manifest source commit and includes both this task's edits and pre-existing dirty changes. | BLOCKED_BY_BASELINE |
| Same validator with `--skip-drift` | Exit 1. Drift checks are skipped; remaining errors are missing DB Admin context/source entries and broken DB Admin links. No Study Server page-graph errors were reported. | BLOCKED_BY_BASELINE |

## HANDOFF

- Remaining blockers: No implementation or Study Server source/test blocker. Repository-wide context validation remains blocked by missing DB Admin scope files/source; full validation also reports tracked-source drift against the old manifest source commit.
- Next owner/action: Re-run the context validator after the repository's DB Admin context/source baseline is restored and tracked source drift is reconciled; no unrelated scope was changed here.
