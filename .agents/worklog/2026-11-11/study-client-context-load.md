---
task_id: "2026-11-11-study-client-context-load"
date: "2026-11-11"
primary_task_type: "coding"
secondary_task_types: []
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Nạp context Study Web (`study-client`)

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 94 exact-type worklogs available; selected and read all 3.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-10/study-web-api-service.md`
    - carry_forward: Study Web dùng Angular 22; `StudyApiService` là transport generic cùng proxy `/api/v1`; API theo feature, auth và production routing chưa được xác nhận.
  - path: `.agents/worklog/2026-11-09/init-study-angular.md`
    - carry_forward: Chỉ root scaffold hiện có; thiết kế/DD không chứng minh route hoặc hành vi runtime; source hiện tại cần được kiểm tra lại.
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Giữ riêng contract với fallback; bảo toàn thay đổi worktree có sẵn; không khẳng định schema/API ngoài bằng chứng source.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Nạp context dự án cho phần `apps/study-client/` để dùng trong các yêu cầu tiếp theo.
- Canonical contract/approved DD: `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/web-study/frontend-rules.md`, `.agents/web-study/design.md`, `apps/study-client/gui/architech.md`; đây là quy tắc và mục tiêu thiết kế, không phải bằng chứng tính năng đã chạy.

## CURRENT_BEHAVIOR

- Source/config: Angular 22 standalone SPA. `app.routes.ts` hiện rỗng; root hiển thị thông báo scaffold. `StudyApiService` gửi request tương đối `/api/v1`, hỗ trợ GET/POST/PUT/PATCH/DELETE cùng params/body/headers và trả `ApiEnvelope<T>`; `app.config.ts` đăng ký `provideHttpClient()`. `proxy.conf.json` chuyển `/api/v1` tới `http://127.0.0.1:3003` cho dev server.
- Runnable tests: Không chạy test theo yêu cầu nạp context; `package.json` hiện không khai báo script test. Worklog 2026-11-10 ghi nhận Angular test target chưa có.
- Runtime wiring: Chưa có route/màn hình nghiệp vụ, feature API call, auth/token storage hoặc deployment API routing được xác nhận. Manifest đánh dấu Study OpenAPI `NOT_FOUND` và Study Web `SKELETON_ONLY`.

## SOURCE_TRACE

```text
browser -> empty Angular routes -> root scaffold
feature caller (chưa có) -> StudyApiService -> HttpClient -> /api/v1 dev proxy -> Study API -> ApiEnvelope<T>
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study API OpenAPI | `.agents/context-manifest.json` khai báo contract `study-openapi` ở trạng thái `NOT_FOUND`. | `NOT_FOUND` | Chưa thể xác nhận endpoint/DTO nghiệp vụ từ tài liệu OpenAPI; cần trace Study Server khi task nối feature. |
| Production API routing | Study Web context và kiến trúc hiện tại chỉ xác nhận proxy của Angular dev server. | `NOT_FOUND / UNVERIFIED` | Không suy diễn host hoặc cấu hình production. |

## CHANGES

- Files changed: `.agents/worklog/2026-11-11/study-client-context-load.md`.
- CONTEXT_UPDATES: Không sửa context router hoặc source; ghi lại context đã nạp và source snapshot hiện tại.
- Context pages changed: none.
- Assumptions: `primary_task_type` được đặt là `coding` để thực hiện preflight cùng loại cho context Study Web phục vụ công việc tiếp theo; task hiện tại chỉ nạp/đối chiếu context.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | `READY`; 94 cùng loại; ba worklog đã được đọc. | `VERIFIED_PREFLIGHT` |
| Context/source inspection | Đọc web-work và Study Web routers/indexes/rules/design/architecture, manifest entries, active HTTP/config files, app routes/root, package scripts và worklog history. | `VERIFIED_STATIC` |
| `git status --short` (trước worklog) | Không có thay đổi đang chờ trong worktree. | `VERIFIED` |
| Automated tests/build | Không chạy; yêu cầu chỉ nạp context. | `NOT_RUN_BY_SCOPE` |
| `node scripts/validate-agent-context.mjs` | Exit 1, `AGENT_CONTEXT_INVALID`. Findings include missing DB Admin context/source, orphan `create_dd_screen` resources, and stale source snapshots; Study Web is `CONTEXT_STALE` against the 2026-10-26 manifest snapshot, including legacy Vue paths. No new Study Web registry/worklog structure error was reported. | `BASELINE_INVALID` |

## HANDOFF

- Remaining blockers: Repository context validator is already invalid from missing DB Admin context/source, orphan skill resources, and source drift. Study Web itself is marked `CONTEXT_STALE`; current Angular source was read directly. Study API OpenAPI is `NOT_FOUND` and production routing is unverified, which only affects feature integration/deploy tasks.
- Next owner/action: Dùng context Study Web đã nạp; với task cụ thể, chạy preflight mới và kiểm tra source/contract hiện hành theo feature.
