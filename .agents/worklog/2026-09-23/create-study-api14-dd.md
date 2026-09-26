---
task_id: "2026-09-23-create-study-api14-dd"
date: "2026-09-23"
primary_task_type: "docs"
secondary_task_types: ["api-dd", "context-loading"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["Study API design contract", "AC-11 profile flow", "users schema/profile response"]
status: "PARTIAL"
---

# Worklog: Tạo DD Study API #14 cập nhật hồ sơ cá nhân

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-22/load-project-context.md`
    - carry_forward: Ưu tiên current source khi context snapshot drift; giữ trạng thái `NOT_FOUND`, `UNWIRED`, `DECLARED_NOT_RUNNABLE` và không suy diễn từ DD.
  - path: `.agents/worklog/2026-09-22/load-study-register-account-context.md`
    - carry_forward: Study dùng module flow `models -> validate -> query -> view`; DB helper không commit, view/use-case sở hữu transaction.
  - path: `.agents/worklog/2026-09-21/update-root-readme.md`
    - carry_forward: Study OpenAPI là `NOT_FOUND`; design contract phải tách khỏi runtime source.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown cho API #14 cập nhật hồ sơ cá nhân.
- Canonical contract/approved DD: `docs/lists/list_api.md`, AC-11, AC API index và template `createDD-markdown`.
- Contract: `PUT /api/v1/users/me/profile`, Student + Bearer JWT, `ApiEnvelope<UserProfile>`, HTTP `200 DESIGN_RESOURCE_UPDATED`, lỗi `401/403/422/500`.

## CURRENT_BEHAVIOR

- Source/config: Current Study router chưa đăng ký API #14; chưa có module, query, view, request model hoặc test cho endpoint này.
- Runtime wiring: API #4 hiện chỉ đọc profile an toàn từ `users`; không có API #14 mutation runtime.
- Schema: `users` có `full_name`, `avatar_url`, `phone`, `updated_at`; không có `bio` trong `DB.sql`/ERD hiện hành.
- Runnable tests: Không có test runtime cho API #14; DD validation sẽ là static documentation checks.

## SOURCE_TRACE

```text
list_api.md + AC-11
-> Bearer JWT / Student authorization
-> request body full_name, bio, phone, avatar_url...
-> UPDATE users by JWT.sub
-> commit/rollback boundary theo Study view pattern
-> reload safe UserProfile projection
-> ApiEnvelope<UserProfile> / DESIGN_* errors
-> API #14 runtime route/test: NOT_FOUND
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #14 runtime route/module/test | `app/api/v1.py`, current module tree và tests không có endpoint #14 | `UNWIRED / NOT_FOUND` | DD chỉ là design artifact, không phải runtime implementation |
| `bio` persistence | Contract yêu cầu `bio`, nhưng `infra/postgres/study-server/DB.sql` và ERD không có `users.bio` | `SOURCE_REQUIRED / DISCREPANCY` | Không tạo cột; update mapping chưa hoàn chỉnh |
| `phone` requiredness | Contract đánh dấu required, schema hiện tại cho phép `NULL` | `DISCREPANCY` | Cần khóa null/blank/clear semantics |
| `avatar_url...:uri!` | Literal contract có ellipsis và chưa xác định required/nullable semantics | `SOURCE_REQUIRED` | Giữ literal trong DD và mở question |
| Design business codes | `code_http.md` đánh dấu `DESIGN_*` là proposal, chưa runtime | `DESIGN_PROPOSAL` | Không tạo business-code delta mới |

## CHANGES

- Files changed: DD pack API #14 và worklog này.
- CONTEXT_UPDATES: Không đổi runtime architecture, endpoint registry hoặc schema.
- Context pages changed: Chưa cần cập nhật; task chỉ tạo design artifact cho endpoint chưa wired.
- Assumptions: Giữ `bio` trong contract nhưng đánh dấu `SOURCE_REQUIRED`; không tự thêm `users.bio`; giữ literal `avatar_url...:uri!`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Chọn 3/21 worklog cùng type và đã đọc đủ | `VERIFIED` |
| Đọc `docs/lists/list_api.md` | Đọc toàn bộ file, xác nhận API #14 và reusable schemas | `VERIFIED` |
| Đọc AC-11/API index/DB schema/current API #4 source | Đã tách expected/current và xác nhận `bio` gap, route chưa wired | `VERIFIED` |
| Authoring DD pack | Tạo đủ 8 sheet chuẩn và 3 companion files tại `apps/study-server/docs/dd/14_users_me_profile/` | `VERIFIED` |
| Static DD check | 8 sheets, front matter, relative links, Markdown tables, JSON examples và template fingerprints | `VERIFIED` — `STATIC_VALIDATION_OK` |
| `git diff --check` | Không có whitespace error | `VERIFIED` |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | Context manifest hợp lệ khi bỏ qua drift | `VERIFIED` — `AGENT_CONTEXT_OK` |
| Full `validate-agent-context.mjs` | Báo `CONTEXT_STALE` repository-wide ở nhiều scope hiện hữu | `PARTIAL` — không thuộc phạm vi cập nhật context của DD docs-only |

## HANDOFF

- Remaining blockers: Quyết định persistence cho `bio`, semantics của `avatar_url`, và null/blank behavior của `phone` chưa có source.
- Next owner/action: Review `OPEN_QUESTIONS.md`; sau khi chốt contract/schema, cập nhật DD và chỉ khi approved mới triển khai runtime API.
