---
task_id: "2026-09-20-load-study-server-auth-login-context"
date: "2026-09-20"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Nạp context Study Server và DD API auth login

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-19/2026-09-19-create-mobile-dd.md`
    - carry_forward: Context phải source-backed; không suy diễn runtime từ tên file hoặc DD thiếu nguồn.
  - path: `.agents/worklog/2026-09-19/2026-09-19-upgrade-agent-workflow-worklog.md`
    - carry_forward: Deno là compatibility runner khi Node không có; selector/worklog/validator là workflow bắt buộc.
  - path: `.agents/worklog/2026-09-19/create-agent-context-map.md`
    - carry_forward: Manifest, page graph và validator phải được xem cùng nhau; context-map không thay thế source evidence.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Chỉ nạp context `server-study` và DD API `apps/study-server/docs/dd/03_auth_login`.
- Canonical contract/approved DD: Bộ DD auth login gồm Cover, lịch sử, overview, request, response, data mapping, error và table.

## CURRENT_BEHAVIOR

- Source/config: Context page hiện đánh dấu `POST /api/v1/auth/login` là `UNWIRED`; source route hiện tại chỉ source-backed cho register và health/utility routes.
- Runnable tests: Chỉ đọc status/context; không chạy test vì user yêu cầu không coding.
- Runtime wiring: Login/refresh/me orchestration chưa được expose trong Study runtime; access/refresh token helpers tồn tại nhưng chưa có login flow.

## SOURCE_TRACE

```text
DD 03_auth_login -> expected auth-login contract
current app/api/v1.py -> current route surface
server-study context -> runtime/security/database/test boundaries
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Auth login DD vs current route | DD mô tả API login; current `app/api/v1.py` không expose route | DISCREPANCY / UNWIRED | Chỉ ghi nhận, không reconcile hay code |
| Live DB schema | Context chỉ có schema/design evidence, live metadata chưa xác minh | SOURCE_REQUIRED | Không coi table DD là runtime proof |
| DD normative source | DD tham chiếu `apps/study-server/docs/lists/list_api.md`; path hiện không tồn tại | NOT_FOUND | Không xác nhận thêm contract ngoài DD hiện có |
| DD maturity | Cover ghi `Draft — Needs Confirmation`, reviewed/approved TBD | EXPECTED_BEHAVIOR | Không coi DD là approved implementation contract |
| Context registry vs current source | Validator báo thiếu `apps/study-server/app/utils/__init__.py` và `app/utils/validate.py` | CONTEXT_STALE / NOT_FOUND | Không sửa context/source trong task read-only |

## CHANGES

- Files changed: Chỉ thêm worklog; không sửa source/DD.
- CONTEXT_UPDATES: Chưa có.
- Context pages changed: Không có.
- Assumptions: “Nạp context” chỉ yêu cầu đọc và tóm tắt; không author/review DD và không implement login.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Chọn 3/16 docs worklogs; đã đọc đủ | VERIFIED |
| Đọc `.agents/context-map.md`, `server-study/AGENTS.md`, `server-study/INDEX.md` và các page liên quan | Đã nạp page graph Study Server | VERIFIED |
| Đọc `apps/study-server/docs/dd/03_auth_login/*` | Đã nạp đủ 7 file DD: Cover, History, Overview, Request, Response, Data Mapping, Error, table | VERIFIED |
| Đọc current `app/api/v1.py`, `app/main.py`, security helpers và Study tests | Xác nhận login route chưa wired; helper token/password có nhưng chưa orchestration | VERIFIED |
| `find apps/study-server/docs/lists -maxdepth 1 -type f` | Không có thư mục/file `docs/lists/list_api.md` tại path DD tham chiếu | NOT_FOUND |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_INVALID`: thiếu hai source path Study đã đăng ký | CONTEXT_STALE |

## HANDOFF

- Remaining blockers: DD còn draft/unapproved; normative source `docs/lists/list_api.md` không tồn tại; login runtime chưa wired.
- Next owner/action: Dùng context đã nạp cho task kế tiếp; nếu triển khai login, cần contract/schema được xác nhận trước và phải xử lý discrepancy 201 vs 200, error 401/403, token response và `UserProfile.bio`.
