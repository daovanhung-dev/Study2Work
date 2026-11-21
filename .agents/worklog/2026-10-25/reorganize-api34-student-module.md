---
task_id: "2026-10-25-reorganize-api34-student-module"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Sắp xếp API #34 vào module Student

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Giữ nguyên API #34 cho `STUDENT/SUBMISSION` và `MENTOR/LECTURE`, các check quyền, storage, metadata transaction và response; không sửa API #47 hoặc áp dụng migration.
  - path: `.agents/worklog/2026-10-25/remove-errordetail-study-server.md`
    - carry_forward: Bảo toàn thay đổi worktree sẵn có; giữ API error envelope và response contract.
  - path: `.agents/worklog/2026-10-25/reuse-jwt-role-guard.md`
    - carry_forward: Dùng shared auth guard và giữ nguyên role/error behavior hiện tại.
- shortage: `none` (selector tìm thấy 38 coding worklogs và trả đủ 3)

## EXPECTED_BEHAVIOR

- Requirement: Chuyển package API #34 vào `app/modules/student/api_34_uploads` và bộ test tương ứng vào `tests/modules/student/api_34_uploads`; giữ nguyên hỗ trợ cả Student và Mentor.
- Canonical contract/approved DD: Không đổi `POST /api/v1/uploads`, multipart fields, auth/purpose/course rules, storage/metadata side effects, response hoặc error behavior.

## CURRENT_BEHAVIOR

- Source/config: API router, package và tests còn import `app.modules.api_34_uploads`; DD/context trỏ tới đường dẫn cũ. Namespace `app.modules.student` chưa có.
- Runnable tests: Context ghi nhận 294 tests ở full Study suite và worklog API #34 ghi 18 focused tests; chưa chạy lại ở đầu task.
- Runtime wiring: Router composition đăng ký `/api/v1/uploads` và gọi `create_upload`; chỉ đổi private Python package path và nơi đặt tests.

## SOURCE_TRACE

```text
POST /api/v1/uploads -> router imports Student package -> existing auth/purpose/course flow -> Object Storage and uploads transaction -> unchanged envelope -> relocated API #34 tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Module namespace | Existing API #34 handles both Student and Mentor purposes; user chose to place the whole package under `student`. | `RESOLVED_BY_USER` | Preserve both role flows while changing namespace only. |
| Existing worktree | API #34 and related code/context are pre-existing untracked or modified files. | `PRESERVE` | Limit edits to package/test relocation, imports, exact references and this worklog. |

## CHANGES

- Files changed: API #34 source package and tests moved under `student`; router/internal imports, DD source links and Study Server context paths updated; `student/__init__.py` and this worklog added.
- CONTEXT_UPDATES: Updated the machine-readable source registry, architecture, route, module index, test inventory and API #34 DD source links to the new package/test path.
- Context pages changed: `.agents/context-manifest.json`, `.agents/server-study/apis/declared-routes.md`, `architecture.md`, `modules/README.md`, `tests.md`.
- Assumptions: The Student namespace is an organizational location only; API #34 continues to accept both `STUDENT` and `MENTOR` roles as before.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected the three same-type worklogs above; all were read. | VERIFIED |
| `uv run --group dev pytest tests/modules/student/api_34_uploads/test_uploads.py -q` | 18 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| `uv run --group dev pytest -q` | 294 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| OpenAPI inspection via `uv run python` | `/api/v1/uploads` remains POST multipart/form-data; `file` and `purpose` required, `course_id` optional int64, purpose enum SUBMISSION/LECTURE; response entries 201/422. | VERIFIED |
| `uv run --group dev ruff check app tests` | All checks passed. | VERIFIED |
| `deno run --allow-read --allow-env scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID` from missing DB Admin context/source and unavailable historical snapshot commit; no API #34 stale-path errors after registry update. | BASELINE_FAILURE |
| `deno run --allow-read scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_INVALID` from missing DB Admin pages/source roots and links; no Study Server source-path errors. | BASELINE_FAILURE |
| `git diff --check` and stale API #34 path scan | No whitespace errors; no old package/test path references remain in app, DD and registered context. | VERIFIED |

## HANDOFF

- Remaining blockers: Repository-wide context validation remains invalid from the existing missing DB Admin context/source and unavailable historical snapshot commit; API #34 paths validate after the registry update.
- Next owner/action: No further API #34 relocation work remains; preserve the recorded repository-wide context baseline.
