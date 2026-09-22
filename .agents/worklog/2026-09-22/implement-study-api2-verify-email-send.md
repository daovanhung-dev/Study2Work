---
task_id: "2026-09-22-implement-study-api2-verify-email-send"
date: "2026-09-22"
primary_task_type: "coding"
secondary_task_types: ["test", "context-maintenance"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study API #2 gửi email xác thực

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-22/implement-study-api4-users-me.md`
    - carry_forward: Giữ canonical envelope, trace handling, namespace `guest`, không expose secret và không suy diễn live DB từ schema/source artifact.
  - path: `.agents/worklog/2026-09-22/implement-study-api5-categories.md`
    - carry_forward: Bảo toàn thay đổi chưa commit của API #5; dùng `apps/study-server/.venv` cho focused/full checks; context validator có thể báo source drift nền.
  - path: `.agents/worklog/2026-09-22/load-study-server-coding-context.md`
    - carry_forward: Workflow coding là registry-backed; ưu tiên current source/test khi context page stale; dùng Deno vì Node không có.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement `POST /api/v1/auth/verify-email/send` theo DD API #2.
- Contract: Public JSON endpoint; request `{user_id, email}`; HTTP `202`; business code `DESIGN_OPERATION_ACCEPTED`; success data `{status: "accepted"}`; validation `422 DESIGN_VALIDATION_ERROR`; internal dispatch failure `500 DESIGN_INTERNAL_ERROR`.
- Approved implementation decisions: injectable Email Provider adapter với development stub; endpoint invocation là explicit verification trigger; không nối register flow; không DB query/mutation/migration.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py` chưa expose API #2; chưa có module `verify_email_send` hoặc email provider boundary; `DESIGN_CONTRACT_PATHS` chưa chứa endpoint.
- Runnable tests: Study test suite có sẵn và API #5 đang có thay đổi chưa commit; focused API #2 tests chưa tồn tại.
- Runtime wiring: Register flow chỉ ghi log `verification_dispatch_pending`; không được thay đổi trong task này.

## SOURCE_TRACE

```text
POST /api/v1/auth/verify-email/send
-> VerifyEmailSendRequest validation
-> injected VerificationEmailProvider
-> stub/provider acceptance result
-> verify_email_send.view response mapping
-> canonical envelope + trace ID
-> focused API #2 tests + full Study checks
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Email Provider thật | DD yêu cầu external dispatch nhưng repository không có provider contract/config/dependency | RESOLVED_FOR_IMPLEMENTATION | Dùng injectable stub; không claim email delivery thật |
| Verification enabled flag | DD không định nghĩa config và cấm thêm request field | RESOLVED_FOR_IMPLEMENTATION | Endpoint invocation là explicit trigger; không thêm flag |
| User existence/email match | DD không xác nhận query/business rule | NOT_FOUND / OUT_OF_SCOPE | Không query DB và không kiểm tra match |
| Token/link/expiry/retry schema | DD đánh dấu TBD; không có source runtime | SOURCE_REQUIRED / OUT_OF_SCOPE | Không thêm field, table, migration hoặc retry worker |
| API #5 working tree | Nhiều file categories đang modified/untracked trước task | USER_CHANGES_PRESERVED | Không overwrite hoặc refactor ngoài phạm vi |

## CHANGES

- Files changed: Added API #2 request/view module, injectable email provider boundary/stub, focused tests, route wiring, contract exception path and Study context updates.
- CONTEXT_UPDATES: Registered API #2 as source-backed with an explicit stub-only boundary; documented no DB access, no real delivery claim and no register-flow integration.
- Context pages changed: `.agents/server-study/AGENTS.md`, `apis/declared-routes.md`, `architecture.md`, `core/runtime.md`, `modules/README.md`, `tests.md`.
- Assumptions: Stub returns acceptance without sending email; provider failure is mapped safely before acceptance; no raw provider detail is logged or returned.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected 3/11 coding worklogs; all 3 read | VERIFIED |
| `./.venv/bin/pytest tests/modules/guest/test_verify_email_send.py -q` | 10 passed; existing Starlette/httpx deprecation warning | VERIFIED |
| `./.venv/bin/pytest -q` | 93 passed; existing Starlette/httpx deprecation warning | VERIFIED |
| `./.venv/bin/pytest --collect-only -q` | 93 tests collected | VERIFIED |
| `./.venv/bin/ruff check app tests` | All checks passed | VERIFIED |
| `./.venv/bin/mypy app` | No issues found in 46 source files | VERIFIED |
| `./.venv/bin/ruff format --check app tests` | Only pre-existing `core/constants.py` and `core/database.py` need formatting | CONTEXT_BASELINE |
| `git diff --check` | No whitespace errors | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Existing `CONTEXT_STALE` across deep scopes; no new actionable registry failure | CONTEXT_STALE |

## HANDOFF

- Remaining blockers: Real Email Provider, verification-token/link generation and retry worker remain undefined; live email delivery is not verified. Full context validator remains stale against the repository source snapshot.
- Next owner/action: Supply a provider contract/config and a verification-token persistence/expiry policy before replacing the stub or integrating API #2 into registration.
