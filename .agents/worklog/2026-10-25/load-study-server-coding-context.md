---
task_id: "2026-10-25-load-study-server-coding-context"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Nạp context Study Server để chuẩn bị coding

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: API #34 hiện hỗ trợ upload Student/SUBMISSION và Mentor/LECTURE; giữ role-purpose, kiểm tra enrollment/ownership, cleanup transaction hiện có. DB migration và Object Storage thật chưa được xác minh.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: API #47 dùng Mentor trực tiếp sở hữu course, resolve `uploads` theo owner/purpose/course, lưu `content` thành decimal text; live schema và migration chưa xác minh.
  - path: `.agents/worklog/2026-10-25/remove-errordetail-study-server.md`
    - carry_forward: Giữ error envelope, status, business code, field errors và trace behavior. Log này đã được fix sau đó đảo phần bỏ `ErrorDetail`; xem log khôi phục bên dưới và source hiện tại làm baseline.
- additional_relevant_worklog_reviewed:
  - path: `.agents/worklog/2026-10-25/restore-errordetail-study-server.md`
    - carry_forward: `ErrorDetail` hiện được khôi phục trong source/tests/context; giữ `ValueError` prohibition và phân biệt validator repository baseline với lỗi Study Server.
- shortage: `none` (selector tìm thấy 40 coding worklogs và chọn đủ 3)

## EXPECTED_BEHAVIOR

- Requirement: Nạp đầy đủ project router, context map/manifest, coding workflow/worklog rules, ba coding worklog được chọn và page graph của `server-study`; giữ nguyên worktree hiện tại và sẵn sàng nhận coding requirement cụ thể.
- Canonical contract/approved DD: Chưa có API hoặc behavior cụ thể được yêu cầu trong bước chuẩn bị này.

## CURRENT_BEHAVIOR

- Source/config: Scope `server-study` có trạng thái context `DEEP` / `SOURCE_BACKED`; đã đọc entry, index, architecture, declared routes, runtime, DB/security, database, module pages, AI service, tests và workflow. Source scan xác nhận `ErrorDetail` hiện còn được dùng.
- Runnable tests: Không chạy; chưa có implementation target.
- Runtime wiring: Context hiện mô tả 18 `/api/v1` paths, gồm APIs #34, #46, #47. Đây là trạng thái theo context/worklogs gần nhất, không phải kiểm tra runtime mới trong task này.

## SOURCE_TRACE

```text
N/A — chưa có endpoint/function cụ thể để trace; đây là bước nạp context trước coding.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Coding requirement | Người dùng yêu cầu nạp context và chuẩn bị, chưa chỉ định endpoint/function/behavior cần đổi. | `AWAITING_TASK_REQUIREMENT` | Không chỉnh runtime hoặc chạy test cho đến khi có target cụ thể. |
| Existing worktree | `git status --short --branch` cho thấy nhiều thay đổi sẵn có trong Study Server, context, DD/schema và worklogs. | `PRESERVED_BASELINE` | Task tiếp theo phải kiểm tra lại trạng thái và giữ các thay đổi này. |

## CHANGES

- Files changed: Chỉ worklog này.
- CONTEXT_UPDATES: Không sửa scope context; chỉ nạp và đối chiếu trạng thái.
- Context pages reviewed: `.agents/server-study/AGENTS.md`, `INDEX.md`, `architecture.md`, `apis/declared-routes.md`, `core/runtime.md`, `core/database-security.md`, `database.md`, `modules/README.md`, `modules/register-account.md`, `services/ai.md`, `tests.md`, `workflows/README.md`.
- Assumptions: Không có behavior hoặc source target cho tới khi người dùng gửi coding task cụ thể.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | Tìm 40 worklogs cùng type; đã đọc cả ba file selector trả về. | VERIFIED |
| `git status --short --branch` | `develop...origin/develop`; có nhiều thay đổi chưa commit trước task, được giữ nguyên. | VERIFIED |
| Source scan for `ErrorDetail` | Class và các caller hiện vẫn tồn tại trong `apps/study-server/app` và tests; phù hợp với log khôi phục. | VERIFIED_STATIC_ONLY |
| Study Server tests | Không chạy vì chưa có coding target. | NOT_RUN |
| `node scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID`: DB Admin context/source paths are missing and broad source snapshot drift is reported, including `server-study`; no error references this worklog. | BLOCKED_BY_REPOSITORY_BASELINE |

## HANDOFF

- Remaining blockers: Context validator remains invalid due to repository-wide missing DB Admin paths and snapshot drift. Cần coding requirement cụ thể để xác định module/API và exact source cần nạp tiếp.
- Next owner/action: Gửi behavior/API/function cần thực hiện; khi đó chạy preflight mới theo task cụ thể và trace source/test liên quan.
