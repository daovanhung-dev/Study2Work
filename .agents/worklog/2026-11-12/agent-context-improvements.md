---
task_id: "2026-11-12-agent-context-improvements"
date: "2026-11-12"
primary_task_type: "docs"
secondary_task_types: ["review"]
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "IN_PROGRESS"
---

# Worklog: Cải thiện agent từ phiên AD-01/routes

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; đã chọn và đọc đủ 3 worklog cùng loại.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-12/add-study-web-screen-rules-workflow.md`
    - carry_forward: Study Web workflow đã có route/layout, guard, test và browser demo; cần hướng dẫn kiểm tra root content ngoài `RouterOutlet` và route isolation.
  - path: `.agents/worklog/2026-11-12/integrate-agent-control-prompt.md`
    - carry_forward: `.agents/project/agent-control.md` là policy toàn cục; từng ghi nhận 83 validator findings baseline, cần chạy lại và phân biệt finding mới.
  - path: `.agents/worklog/2026-11-12/load-project-context.md`
    - carry_forward: Context DB Admin đang thiếu; lần validator trước có 83 findings và phải xác nhận lại theo trạng thái hiện tại.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Sau khi người dùng duyệt đề xuất, bổ sung đúng ba hướng dẫn đã chốt: gate duyệt khi chỉ yêu cầu phân tích/thay đổi agent-context; checklist tích hợp route Study Web; và cách so sánh validator findings trước/sau khi cập nhật context.
- Canonical contract/approved DD: Kế hoạch được người dùng duyệt trong phiên AD-01/routes. Không tạo workflow mới hoặc thay đổi runtime.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 25% | 25% | Hoàn tất classification, worklog preflight, đọc đủ ba prior worklog và các trang đích; chạy validator baseline. | `DONE` |
| 50% | 75% | Cập nhật đúng ba trang agent hiện có theo nội dung đã duyệt, không sửa runtime hoặc thêm workflow. | `DONE` |
| 25% | 100% | Chạy validator sau sửa, so sánh baseline/findings mới, kiểm tra diff và hoàn tất worklog. | `PENDING` |

## CURRENT_BEHAVIOR

- Source/config: `.agents/project/agent-control.md` nêu plan-first và các gate nhưng chưa có quy tắc tổng quát buộc dừng sau đề xuất agent/context để chờ duyệt. Study Web screen workflow nêu group route/layout, guard/auth và test/demo nhưng chưa nhắc root content ngoài outlet hoặc kiểm tra scaffold không rò qua feature URL. Project workflows có nhắc context validator sau task nhưng chưa quy định chạy trước/sau và so sánh baseline.
- Runnable tests: Không áp dụng; đây là task tài liệu/context.
- Runtime wiring: Không thay đổi runtime, app route, API hoặc auth.

## SOURCE_TRACE

```text
approved proposal -> three existing .agents pages -> context validator before/after -> diff/worklog
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Repository validator baseline | `node scripts/validate-agent-context.mjs` trước chỉnh sửa trả exit 1 với 83 findings: 32 db-admin, 1 contract, 33 orphan skill resources, 10 broken context links, 7 `CONTEXT_STALE` groups. Không finding nào nhắc ba trang đích. | `BASELINE_INVALID` | So sánh lần chạy sau; xử lý finding mới do task tạo, giữ lỗi baseline trong phạm vi ghi nhận và không mở rộng sang scope khác. |

## CHANGES

- Files changed: `.agents/project/agent-control.md`; `.agents/web-work/study/workflows/screen-implementation.md`; `.agents/project/workflows.md`; `.agents/worklog/2026-11-12/agent-context-improvements.md`.
- CONTEXT_UPDATES: Thêm gate duyệt rõ ràng cho đề xuất thay đổi agent/context; checklist route root/feature, outlet, guard/auth và kiểm tra không rò scaffold; quy trình validator baseline trước/sau với phân loại finding mới và baseline.
- Context pages changed: `.agents/project/agent-control.md`; `.agents/web-work/study/workflows/screen-implementation.md`; `.agents/project/workflows.md`.
- Assumptions: Gate duyệt áp dụng khi user chỉ yêu cầu phân tích/đề xuất thay đổi agent hoặc context; không áp dụng khi user đã yêu cầu thực hiện rõ ràng như task hiện tại.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Worklog selector and selected prior logs | `READY`; đọc đủ 3 worklog được chọn cùng loại `docs`. | `VERIFIED` |
| Root instructions, `.agents/AGENTS.md`, context map, worklog contract/template và ba trang đích | Đã kiểm tra load order, vị trí và nội dung hiện có; xác nhận thay đổi có thể nằm trong đúng ba trang đã duyệt. | `VERIFIED_STATIC_ONLY` |
| `node scripts/validate-agent-context.mjs` trước sửa | Exit 1, 83 findings baseline; toàn bộ output lưu tại `/tmp/agent-improvements-validator-before.log`. | `BASELINE_INVALID` |
| Patch ba trang đích | Thêm đúng các mục trong kế hoạch đã duyệt; chưa chạy validator sau sửa. | `IMPLEMENTED_PENDING_VERIFICATION` |

## HANDOFF

- Remaining blockers: Chưa có.
- Next owner/action: Review diff, chạy validator sau sửa và phân loại mọi finding mới so với baseline.
