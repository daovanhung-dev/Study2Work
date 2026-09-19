---
task_id: "2026-09-19-extract-strip-email-utility"
date: "2026-09-19"
primary_task_type: "coding"
secondary_task_types: ["refactor", "test", "context-maintenance"]
project_scopes: ["server-study"]
cross_scope_dependencies:
  - ".agents/context-manifest.json"
status: "VERIFIED"
---

# Worklog: Tách và tái sử dụng `strip_email`

## PRIOR_WORKLOG_REVIEW

- primary_task_type: coding
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-19/rename-study-auth-guest-namespace.md`
    - carry_forward: Giữ nguyên các thay đổi `auth` → `guest`; full Study suite hiện có 43 test pass; context validator chỉ pass khi skip source drift.
  - path: `.agents/worklog/2026-09-18/configure-local-service-addresses.md`
    - carry_forward: Ghi rõ toolchain/blocker và không dùng source drift làm lý do thay đổi snapshot tùy tiện.
  - path: `.agents/worklog/2026-09-18/work-server-rest-api-hardening.md`
    - carry_forward: Giữ phạm vi source-backed, không mở rộng API/contract ngoài yêu cầu.
- shortage: `none`

## EXPECTED_BEHAVIOR

- User request: đưa logic trim email thành pure helper `app.utils.validate.strip_email(value: object) -> object` và tái sử dụng trong `RegisterRequest`.
- Giữ nguyên email normalization behavior, request/response contract, endpoint, database và `register_account/validate.py`.

## CURRENT_BEHAVIOR

- `app/utils/validate.py` đang rỗng.
- `app/utils/__init__.py` dùng `from validate import strip_email`, gây `ModuleNotFoundError: No module named 'validate'` khi import package.
- `RegisterRequest` đã import `app.utils.validate.strip_email` nhưng vẫn giữ validator method cục bộ, nên chưa thật sự tái sử dụng helper.
- Full Study tests chưa chạy được ở trạng thái hiện tại vì lỗi package import.

## SOURCE_TRACE

```text
app/main.py:create_app
-> app/api/v1.py
-> app.modules.guest.register_account.models:RegisterRequest
-> app.utils.validate:strip_email
-> POST /api/v1/auth/register
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Shared utility implementation | `app/utils/validate.py` empty | NOT_FOUND / INCOMPLETE | Implement pure helper with no Pydantic dependency |
| Package import | `app/utils/__init__.py` imports top-level `validate` | CURRENT_IMPORT_ERROR | Use relative `.validate` import |
| Model reuse | Local `RegisterRequest.strip_email` duplicates intended helper | DISCREPANCY | Bind imported helper directly with `field_validator` |
| Other validation rules | `full_name` and password validators are local; `register_account/validate.py` empty | OUT_OF_SCOPE | Do not generalize or move unrelated validators |

## CHANGES

- Files changed: `app/utils/validate.py`, `app/utils/__init__.py`, `guest/register_account/models.py`, new utility tests, context manifest/pages and this worklog.
- CONTEXT_UPDATES: registered shared normalization utility and documented the distinction between `app/utils/validate.py` and module `register_account/validate.py`.
- Context pages changed: `.agents/context-manifest.json`, `.agents/server-study/AGENTS.md`, `architecture.md`, `modules/register-account.md` and `workflows/README.md`.
- Assumptions: helper returns non-string values unchanged; no backward compatibility alias beyond the package re-export.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected 3 matching coding worklogs; all read | VERIFIED |
| `cd apps/study-server && .venv/bin/python -c 'from app.modules.guest.register_account.models import RegisterRequest; ...'` | Fails with `ModuleNotFoundError: No module named 'validate'` before implementation | CURRENT_FAILURE |
| `cd apps/study-server && .venv/bin/pytest -q tests/modules/guest/test_register.py` | Collection fails at same package import before implementation | CURRENT_FAILURE |
| `cd apps/study-server && .venv/bin/python - <<'PY' ...` | Import smoke, reusable helper identity, model normalization and public route assertions pass | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest -q tests/utils/test_validate.py` | 2 passed, 1 deprecation warning | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest -q tests/modules/guest/test_register.py` | 15 passed, 1 deprecation warning | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest -q` | 45 passed, 1 deprecation warning | VERIFIED |
| `git diff --check` | Passed | VERIFIED |
| `python3 -m json.tool .agents/context-manifest.json` | Manifest parsed successfully | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Existing `CONTEXT_STALE` in Study snapshot and other scopes | CONTEXT_STALE |

## HANDOFF

- Remaining blockers: full context validator remains invalid because the repository snapshot predates current Study/Work/Web/DB Admin source; no runtime blocker remains for this utility extraction.
- Next owner/action: review the combined worktree diff; preserve the pre-existing `auth` → `guest` changes and do not refresh the global source snapshot solely to suppress drift.
