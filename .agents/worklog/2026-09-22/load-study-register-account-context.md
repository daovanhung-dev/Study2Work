---
task_id: "2026-09-22-load-study-register-account-context"
date: "2026-09-22"
primary_task_type: "docs"
secondary_task_types: ["context-loading", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["Study API v1 router", "users table", "core database/responses/security"]
status: "VERIFIED"
---

# Worklog: Nạp context Study register_account

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-22/load-project-context.md`
    - carry_forward: Ưu tiên current source khi context snapshot drift; giữ riêng EXPECTED_BEHAVIOR/CURRENT_BEHAVIOR và status `CONTEXT_STALE`.
  - path: `.agents/worklog/2026-09-21/update-root-readme.md`
    - carry_forward: Không suy diễn runtime từ docs thiếu nguồn; ghi rõ toolchain/working-tree blocker khi có.
  - path: `.agents/worklog/2026-09-20/load-mobile-work-context.md`
    - carry_forward: Dùng source-backed evidence và không coi file tồn tại là runtime wiring; Deno là compatibility runner khi Node vắng.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Nạp context và current source cho module `apps/study-server/app/modules/guest/register_account`.
- Canonical context: `.agents/server-study/{AGENTS,INDEX}.md`, `modules/README.md`, `modules/register-account.md`, Study workflow/core pages và current source/tests.

## CURRENT_BEHAVIOR

- Source/config: `register_account` có `models.py`, `validate.py`, `query.py`, `view.py`; route public là `POST /api/v1/auth/register`.
- Runtime wiring: `v1.py` gọi `create_user`; request model normalize email/full name, reject blank password; view kiểm tra duplicate email, Argon2id hash, insert `users`, commit và trả safe envelope.
- Runnable tests: Focused register test sẽ được chạy bằng `apps/study-server/.venv/bin/pytest`; live DB/schema availability không được suy ra từ static source.

## SOURCE_TRACE

```text
POST /api/v1/auth/register
-> RegisterRequest (models.py)
-> app.utils.validate.strip_email/reject_blank_password
-> create_user (view.py)
-> find_user_by_email/insert_user (query.py)
-> users table + Argon2id + caller-owned commit/rollback
-> success_response/error ApiError + register tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| `register_account/validate.py` | File exists but current source has no special validation logic/caller | EMPTY/UNWIRED | Không coi file này là validation runtime; model validators và shared utils là current path |
| `users` schema | Query/source and checked-in DB design exist; live metadata chưa verify | SOURCE_REQUIRED | Không tự thêm field/table/migration từ docs |
| Context snapshot | Full validator trước đó báo Study source drift | CONTEXT_STALE | Nếu coding tiếp, phải ưu tiên current source/test |
| Register test path | Current runnable test nằm ở `tests/modules/auth/test_register.py` nhưng imports `app.modules.guest.register_account.*` | CURRENT_SOURCE | Không đổi namespace chỉ vì tên thư mục test |

## CHANGES

- Files changed: Chỉ thêm worklog này; không sửa source/module.
- CONTEXT_UPDATES: Không có runtime change.
- Context pages changed: Không có.
- Assumptions: Người dùng chỉ yêu cầu nạp context, không yêu cầu sửa/đổi behavior register.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Chọn 3/20 worklog docs và đã đọc đủ | VERIFIED |
| Đọc server-study routing/module/workflow/core pages và register source | Đã nạp module graph và source trace | VERIFIED |
| `./.venv/bin/pytest tests/modules/auth/test_register.py -q` | 15 passed, 1 Starlette/httpx deprecation warning | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | Pending final check | IN_PROGRESS |

## HANDOFF

- Remaining blockers: Live DB metadata chưa xác minh; full context validator có thể tiếp tục báo source drift ngoài task.
- Next owner/action: Nếu coding register, trace lại caller/callee/DB/response/test trước khi sửa và giữ transaction trong `view.py`.
