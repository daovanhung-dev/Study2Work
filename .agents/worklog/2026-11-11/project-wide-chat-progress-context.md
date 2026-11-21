---
task_id: "2026-11-11-project-wide-chat-progress-context"
date: "2026-11-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["mobile-work", "web-work", "server-work", "server-study", "server-ai", "db-admin"]
cross_scope_dependencies: ["root/global context -> project workflow -> worklog template/registry -> context validator"]
status: "VERIFIED"
---

# Worklog: Chuẩn hóa cập nhật tiến độ trong chat cho mọi task

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 274 worklog cùng loại; đã chọn và đọc đủ 3.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-11/add-study-fe-screen-api-context.md`
    - carry_forward: Context instructions phải nằm trong router/index được registry dùng; task Study FE gần nhất xác nhận context validator có baseline invalid unrelated.
  - path: `.agents/worklog/2026-11-11/list-study-api-endpoints.md`
    - carry_forward: Giữ design/DD status riêng runtime; đánh dấu `DISCREPANCY`, `NOT_FOUND`, `UNWIRED` thay vì suy diễn.
  - path: `.agents/worklog/2026-11-11/load-study-server-context.md`
    - carry_forward: Study OpenAPI là `NOT_FOUND`; validator baseline gồm lỗi DB Admin, orphan skill resources, broken links và stale scope snapshots.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Mọi task bắt đầu bằng mục tiêu và các milestone task-specific có trọng số phần trăm, tối thiểu hai mốc và tổng trọng số 100%. Sau mỗi nhóm đọc, báo các file/nguồn cùng điều rút ra; sau mỗi nhóm thao tác, báo hành động và kết quả; khi hoàn tất milestone, cập nhật phần trăm tích lũy trong chat. Nếu bị chặn, báo phần trăm đạt được và blocker; chỉ báo 100% khi task hoàn thành.
- Canonical contract/approved DD: User-approved plan; root/global agent context, common workflow, worklog contract/template và manifest registry.

## CURRENT_BEHAVIOR

- Source/config: Qua lần rà soát plan, context đã yêu cầu phân loại task, worklog preflight, cập nhật worklog và validator; chưa có quy tắc chung để báo nội dung đọc/hiểu/thao tác trong chat hoặc tỷ lệ milestone cho mọi task. Cần kiểm tra lại file đích trước khi sửa.
- Runnable tests: Không thuộc phạm vi; chỉ sửa context/workflow.
- Runtime wiring: Thay đổi hướng dẫn và audit format; không ảnh hưởng runtime ứng dụng.

## SOURCE_TRACE

```text
root AGENTS -> global context -> project workflow -> worklog README/template -> manifest requiredFields -> context validator
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Context validator baseline | Recent docs worklogs report `AGENT_CONTEXT_INVALID` from unrelated DB Admin context/source, orphan skill resources, broken links and stale scope snapshots. | `BASELINE_INVALID` | Record current counts and confirm no finding is introduced by this task. |

## MILESTONES

| Weight | Cumulative target | Objective / acceptance | Status |
|---:|---:|---|---|
| 20% | 20% | Read worklog preflight and inspect current global context, workflow, template, manifest and validator. | DONE |
| 35% | 55% | Add mandatory global chat/read/action updates and milestone behavior to root/global workflow context. | DONE |
| 25% | 80% | Update worklog README/template and make `milestones` a validator-required template field. | DONE |
| 20% | 100% | Verify links/Markdown/context validator, classify baseline, and finish this worklog. | DONE |

## CHANGES

- Files changed: `AGENTS.md`, `.agents/AGENTS.md`, `.agents/project/workflows.md`, `.agents/context-map.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`, `.agents/context-manifest.json`, worklog này.
- CONTEXT_UPDATES: Root/global context, common workflow và context map quy định phân loại+mốc ở đầu task, receipts theo nhóm đọc/thao tác, tiến độ tích lũy khi đạt mốc và báo blocker. Worklog README/template quy định cách ghi milestone; manifest yêu cầu field `milestones`.
- Context pages changed: `AGENTS.md`, `.agents/AGENTS.md`, `.agents/project/workflows.md`, `.agents/context-map.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`, `.agents/context-manifest.json`.
- Assumptions: Chat updates follow coherent read/action groups, with source paths and concise findings. Progress percentages are cumulative from milestone weights and advance only when a milestone is complete.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` and selected worklogs | `READY`, 3 selected worklogs read; no shortage. | VERIFIED |
| Root/global/workflow/worklog/manifest/validator inspection | Đã đọc đủ file/section cần thiết; không có rule chat/progress hiện hành, template thiếu milestone, validator kiểm tra template theo manifest `requiredFields`. | VERIFIED_STATIC_ONLY |
| Root/global workflow/context-map edits | Thêm quy tắc bắt buộc và chèn các cập nhật chat/mốc vào load/common flow. | UPDATED |
| Worklog README/template + manifest JSON | README quy định receipts/milestone; template có bảng MILESTONES; manifest yêu cầu `milestones`; JSON parse và required field/template check pass. | VERIFIED_STATIC_ONLY |
| JSON/template/Markdown/link checks and `git diff --check` | Manifest parses; `milestones` is registry-required and present in template; edited files have final newlines/no trailing whitespace; new path references resolve; `git diff --check` passes. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | Exit 1 with the same 917-line output as the pre-change baseline: no added or removed findings. Baseline has 83 findings (33 DB Admin, 33 orphan skill resources, 10 broken context links, 7 stale scopes); no task-specific registry/worklog finding. | BASELINE_INVALID_UNRELATED |
| Application tests/build | Không thuộc phạm vi context/workflow. | NOT_RUN |

## HANDOFF

- Remaining blockers: Repo-wide context validator baseline remains invalid, unchanged by this task.
- Next owner/action: Không còn việc bắt buộc; xử lý validator baseline trong task bảo trì context riêng.
