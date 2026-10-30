---
task_id: "2026-10-25-load-study-server-context"
date: "2026-10-25"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Nạp context dự án Study Server

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` (`node` không có trong PATH)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/commit-push-study-dd.md`
    - carry_forward: Study DD giao nhận chưa push được trong phiên đó; khi chỉ nạp context không suy ra remote hiện tại.
  - path: `.agents/worklog/2026-10-24/complete-study-api01-dd-package.md`
    - carry_forward: Giữ expected contract tách khỏi current source; API #01 chưa gọi API #02 và profile/schema gaps còn mở.
  - path: `.agents/worklog/2026-10-24/complete-study-api02-dd-package.md`
    - carry_forward: Provider mặc định chỉ là stub; retry, token/link và user/email binding chưa được xác minh hoặc triển khai.
- shortage: `none` (selector có 130 worklog docs, chọn 3)

## EXPECTED_BEHAVIOR

- Requirement: Nạp context canonical của `server-study`; chưa có API, lỗi hoặc thay đổi chức năng cụ thể.
- Canonical contract/approved DD: Root router, `.agents/context-map.md`, manifest và `.agents/server-study/` xác định scope, ownership, trạng thái và load graph.

## CURRENT_BEHAVIOR

- Source/config: Scope hiện là FastAPI + sync SQLAlchemy, route/module/view theo context pages. Working tree `develop...origin/develop` đang dirty: API #46 Mentor courses, error response `data: null`, tests và context/manifest/worklogs có thay đổi chưa commit. Đã đọc diff/source hiện tại của API #46 và response/middleware.
- Runnable tests: Không chạy test trong task nạp context. Worklog ngày 2026-10-24 ghi 261 tests pass sau implementation/refactor API #46; đó là bằng chứng lịch sử, không phải lần chạy hiện tại.
- Runtime wiring: Source hiện khai báo `GET /api/v1/mentor/courses`; API #46 xác thực numeric JWT subject + role `MENTOR`, lọc owner trực tiếp, hỗ trợ status `DRAFT`/`PUBLISHED`, phân trang và dùng CoursePage chung. Chưa chạy import/HTTP probe trong task này. Schema DB live chưa được xác minh.

## SOURCE_TRACE

```text
GET /api/v1/mentor/courses -> Mentor validator -> owner-scoped count/page SQL -> shared course mapping -> success/error envelope
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Live Study schema | Scope/database pages phân biệt DDL/migration artifacts với metadata live; không có live probe trong task này. | `NOT_VERIFIED_HERE` | Không khẳng định bảng/cột đang khả dụng trên DB triển khai. |
| Test/runtime verification | Source/context được đọc; không chạy pytest, import probe hoặc HTTP probe. | `NOT_RUN_THIS_TASK` | Các kết quả test trong worklog trước vẫn là evidence lịch sử. |

## CHANGES

- Files changed: Worklog này.
- CONTEXT_UPDATES: Không sửa scope pages hoặc manifest.
- Context pages changed: None.
- Assumptions: Phạm vi hiện tại chỉ là nạp context; task tiếp theo cần route/page cụ thể để đọc exact contract, source và tests.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `git status --short --branch` | `develop...origin/develop`; giữ nguyên mọi thay đổi đã có trong worktree. | VERIFIED |
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Chọn và đọc đủ 3 worklog docs cùng loại; không thiếu. | VERIFIED |
| Root/global router, context map, manifest, worklog README/template, server-study entry/index/pages/workflow | Đã đọc toàn bộ page graph scope và các trang được manifest đăng ký. | VERIFIED_STATIC_ONLY |
| API #46 route/module và response/middleware diff | Đã đọc source hiện tại và thay đổi chưa commit; không chạy app/test. | VERIFIED_STATIC_ONLY |
| `/home/daovanhung/.local/node-v24.21.0-linux-x64/bin/node scripts/validate-agent-context.mjs` | Exit 1: repository context invalid do thiếu DB Admin pages/source/links và source snapshot drift; Study Server cũng được liệt kê `CONTEXT_STALE` ở nhiều source paths. Không sửa scope ngoài yêu cầu. | CONTEXT_BASELINE |

## HANDOFF

- Remaining blockers: Context validator toàn repo báo thiếu DB Admin pages/source/links và `CONTEXT_STALE` ở nhiều scope, gồm Study Server; chưa có task feature cụ thể; live DB/deployment chưa xác minh.
- Next owner/action: Khi có requirement, tiếp tục từ page đúng API/module, đọc contract/source/test hiện tại và giữ nguyên các thay đổi chưa commit.
