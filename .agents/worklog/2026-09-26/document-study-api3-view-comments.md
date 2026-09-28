---
task_id: "2026-09-26-document-study-api3-view-comments"
date: "2026-09-26"
primary_task_type: "docs"
secondary_task_types: ["coding", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["Study API #3 DD", "users/refresh_tokens runtime contract"]
status: "VERIFIED"
---

# Worklog: Bổ sung chú thích DD cho Study API #3

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-23/create-study-api14-dd.md`
    - carry_forward: Tách expected/current behavior; không suy diễn runtime từ DD và ghi rõ source-backed evidence.
  - path: `.agents/worklog/2026-09-23/create-study-api15-enrollment-status-dd.md`
    - carry_forward: Giữ các trạng thái `DISCREPANCY`, `SOURCE_REQUIRED`, `UNWIRED`; docs-only thay đổi không được biến thành runtime behavior.
  - path: `.agents/worklog/2026-09-22/load-project-context.md`
    - carry_forward: Ưu tiên current source khi context/DD drift; Node không có nên dùng Deno cho selector/validator.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Thêm chú thích tiếng Việt cho từng event chính trong `api_03_auth_login/view.py`, bao phủ login và refresh, bám các bước DD API #3.
- Constraint: Chỉ thêm inline comments; không đổi logic, query, response, transaction hoặc các file runtime khác.

## CURRENT_BEHAVIOR

- `login`: source hiện lookup user theo email, verify password, check status, issue tokens, insert refresh-token hash, commit và map success/error response.
- `refresh`: source hiện hash token, lookup session active/unexpired/unrevoked, rotate token trong một transaction và map response/error.
- DD source: `apps/study-server/docs/dd/03_auth_login/05_Data_Mapping.md` mô tả request → validate → lookup → credential/status → token/session → response.

## SOURCE_TRACE

```text
LoginRequest/RefreshRequest đã validate
-> view.login/view.refresh
-> users/refresh_tokens query + password/token helpers
-> transaction/error mapping
-> canonical success/error response
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| DD login read-only vs current refresh-session insert | `02_Overview.md`, `05_Data_Mapping.md` ghi no DB mutation; `view.login` insert refresh token | DISCREPANCY | Comment mô tả current runtime, không sửa behavior |
| DD success 201/profile-only vs current 200/profile+token payload | `list_api.md`/DD và `view.py` khác nhau | DISCREPANCY | Không reconcile trong task comment-only |
| Refresh flow không có DD riêng | `view.py` có `refresh`, API #3 DD tập trung login | CURRENT_SOURCE_EXTENSION | Chú thích refresh theo runtime token-rotation flow, không gán sai DD step |

## CHANGES

- Files changed: Added Vietnamese DD/event comments to `apps/study-server/app/modules/guest/api_03_auth_login/view.py` for login, refresh rotation and `_internal_error`; follow-up compacted the comments from 39 to 26 lines; no executable statements changed.
- CONTEXT_UPDATES: None; inline comments do not change architecture or ownership.
- Assumptions: Comment trước các event/branch chính, không comment từng dòng; giữ nguyên message, status code, rollback, logging và secret-safety behavior.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Selected and read 3 matching docs worklogs | VERIFIED |
| Read API #3 DD files and current `view.py`/auth/security sources | Event map and DD/current discrepancies identified | VERIFIED |
| `git diff` review of `view.py` | 26 short comment-only lines added; no executable statement changes | VERIFIED |
| `.venv/bin/pytest tests/modules/guest/api_03_auth_login/test_auth_login.py -q` | 11 passed; existing Starlette/httpx deprecation warning | VERIFIED |
| `.venv/bin/pytest -q` | 137 passed; existing Starlette/httpx deprecation warning | VERIFIED |
| `.venv/bin/ruff check app tests` | All checks passed | VERIFIED |
| `.venv/bin/mypy app` | No issues found in 59 source files | VERIFIED |
| `git diff --check` | No whitespace errors | VERIFIED |

## HANDOFF

- Remaining blockers: One existing Starlette/httpx deprecation warning; DD/current discrepancies remain intentionally unchanged.
- Next owner/action: No further implementation action for this comment-only request.
