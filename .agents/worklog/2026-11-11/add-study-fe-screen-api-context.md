---
task_id: "2026-11-11-add-study-fe-screen-api-context"
date: "2026-11-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study FE task scope -> screen inventory/DD -> Study API catalog/DD"]
status: "VERIFIED"
---

# Worklog: Bổ sung quy tắc context cho Study FE

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 273 worklog cùng loại; đã chọn và đọc đủ 3.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-11/list-study-api-endpoints.md`
    - carry_forward: `list_endpoint.md` là catalog thiết kế/DD 103 API, không chứng minh runtime; các khoảng trống/mâu thuẫn contract được đánh dấu `DISCREPANCY`/`NOT_FOUND`.
  - path: `.agents/worklog/2026-11-11/load-study-server-context.md`
    - carry_forward: Study OpenAPI là `NOT_FOUND`; giữ expected DD và current source tách biệt; kiểm tra source/runtime cụ thể khi task cần.
  - path: `.agents/worklog/2026-11-10/load-project-context.md`
    - carry_forward: Context registry phải được kiểm tra để bảo đảm trang hướng dẫn có thể được agent định tuyến; validator hiện có baseline `AGENT_CONTEXT_INVALID`.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Mọi task chạm `apps/study-client`, gồm coding/docs/test/review/config, phải đọc `list_screen.md` và `list_endpoint.md`, xác định screen/API trong phạm vi, ghi vào worklog; sau đó đọc DD screen liên quan và DD API khi task phụ thuộc contract/hành vi API.
- Canonical contract/approved DD: User-approved plan; Study screen inventory, endpoint catalog và DD packages là nguồn thiết kế, không xác nhận runtime.

## CURRENT_BEHAVIOR

- Source/config: Study Web router và index đã được context registry định tuyến. Index có liên kết `list_screen.md` và `dd_screens/screen-index.md`, nhưng chưa liệt kê `list_endpoint.md`; router chưa quy định bắt buộc đọc hai catalog hoặc ghi rõ screen/API scope. Các DD API nằm dưới `apps/study-server/docs/dd/`.
- Runnable tests: Không chạy app tests; task chỉ sửa context/documentation.
- Runtime wiring: Study FE vẫn là `SKELETON_ONLY`; catalog/DD chỉ là design/reference evidence.

## SOURCE_TRACE

```text
web-work router -> Study FE inventory + endpoint catalog -> task screen/API scope -> relevant screen/API DD -> current source/tests when runtime behavior matters
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Context validator baseline | Selected worklogs record repo-wide `AGENT_CONTEXT_INVALID` from unrelated DB Admin, orphan skill-resource, broken-link and stale-snapshot findings. | `BASELINE_INVALID` | Run validator and confirm this task adds no finding tied to the edited context/worklog. |

## CHANGES

- Files changed: `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, worklog này.
- CONTEXT_UPDATES: Study FE router nay yêu cầu đọc hai catalog cho mọi task, chọn và ghi scope screen/API, rồi tải DD liên quan; index liệt kê authority/giới hạn của catalog và chỉ dẫn tra DD. Không thêm entry registry vì entry/index đã được đăng ký.
- Context pages changed: `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`.
- Assumptions: Task có thể không có screen hoặc API; khi đó worklog ghi `none`. Chỉ đọc API DD tương ứng khi contract/hành vi của API ảnh hưởng task.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` và đọc 3 log đã chọn | `READY`, đủ 3 log cùng loại; đã ghi carry-forward facts trong `PRIOR_WORKLOG_REVIEW`. | VERIFIED |
| Context router/index và Study screen DD index | Đã xác nhận entry/index hiện được registry định tuyến; link screen package qua `dd_screens/screen-index.md`. | VERIFIED_STATIC_ONLY |
| Markdown/link/`git diff --check` | Link tương đối trong hai trang context và worklog resolve; newline/whitespace hợp lệ; `git diff --check` không báo lỗi. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | Exit 1 `AGENT_CONTEXT_INVALID`, 83 baseline findings: 33 DB Admin, 33 `ORPHAN_SKILL_RESOURCE`, 10 broken DB Admin context links và 7 scope snapshots stale. Không finding nào nhắc hai trang đã sửa hoặc worklog này. | BASELINE_INVALID_UNRELATED |
| App tests/build | Không thuộc phạm vi thay đổi documentation/context. | NOT_RUN |

## HANDOFF

- Remaining blockers: Validator repo-wide còn baseline invalid không liên quan tới thay đổi này.
- Next owner/action: Không còn việc bắt buộc cho quy tắc Study FE; xử lý baseline validator ở task bảo trì context riêng.
