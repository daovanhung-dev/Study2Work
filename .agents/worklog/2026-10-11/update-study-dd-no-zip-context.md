---
task_id: "2026-10-11-update-study-dd-no-zip-context"
date: "2026-10-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Cập nhật context không tạo ZIP cho Study API DD

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` (`node` unavailable)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-11/create-study-api16-dd.md`
    - carry_forward: API DD dùng skill `createDD-markdown`; hiện trạng runtime và thiết kế phải được ghi tách biệt.
  - path: `.agents/worklog/2026-10-11/create-study-api17-dd.md`
    - carry_forward: Skill chung hiện yêu cầu ZIP; Study API DD vẫn thuộc scope của skill đó.
  - path: `.agents/worklog/2026-10-11/create-study-api18-dd.md`
    - carry_forward: API DD cần giữ deliverable Markdown và status rõ ràng; runtime test không áp dụng khi API chưa được wire.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Sửa agent context để Study Server Web/API DD chỉ bàn giao thư mục Markdown, không tạo ZIP mới; giữ nguyên quy ước chung của Work, AI và Web.
- Canonical contract/approved DD: Kế hoạch được người dùng phê duyệt; ngoại lệ phạm vi `server-study` ưu tiên hơn yêu cầu ZIP đầu ra trong skill chung.

## CURRENT_BEHAVIOR

- Source/config: `.agents/project/workflows.md` yêu cầu load `createDD-markdown`; skill dùng chung yêu cầu đóng gói ZIP. Context `server-study` hiện chưa có tuyến API DD hay ngoại lệ đầu ra.
- Runnable tests: Không áp dụng; đây là thay đổi tài liệu context.
- Runtime wiring: Không thay đổi; task không chạm runtime/API.

## SOURCE_TRACE

```text
API DD task -> project docs-dd workflow -> createDD-markdown (generic ZIP rule)
-> server-study context routing/workflow -> Markdown folder only for Study API DD
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| ZIP output for Study DD | Shared skill requires ZIP; user-approved Study-only policy forbids new output ZIPs | `DISCREPANCY` resolved by scoped context override | Keep generic skill unchanged for other scopes; do not create or validate a Study output ZIP. |

## CHANGES

- Files changed: `.agents/server-study/AGENTS.md`, `.agents/server-study/workflows/README.md`, `.agents/project/workflows.md`, this worklog.
- CONTEXT_UPDATES: Added the Study API DD Markdown-only output exception; linked it from the server-study task router and shared Docs/DD workflow.
- Context pages changed: The Study Server router/workflow and shared Docs/DD workflow.
- Assumptions: Existing archives are preserved; input archive inspection rules remain unchanged.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `node` is unavailable; the Deno compatibility command selected three logs, all read. | VERIFIED (fallback) |
| `node scripts/validate-agent-context.mjs` | `node` is unavailable. | BLOCKED (tool unavailable) |
| `deno run --allow-read --allow-env scripts/validate-agent-context.mjs` | Validator reports pre-existing missing `db-admin` context/source paths and unavailable snapshot commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`; it reports no error for the edited Study/project pages. | PARTIAL (baseline invalid) |
| `git diff --check` | No whitespace errors. | VERIFIED |
| Context rule/link review | Study router points to the Study workflow; it forbids new Study DD output ZIPs and ZIP-required checks while retaining source-archive inspection and other-scope policy. Relative workflow target exists. | VERIFIED |
| ZIP/runtime boundary | No ZIP was created or removed; no application tests were run. | VERIFIED |

## HANDOFF

- Remaining blockers: The full context validator cannot pass in this checkout because the registered `db-admin` scope files/source and the recorded baseline commit are absent.
- Next owner/action: Re-run the context validator in a complete checkout containing the registered DB Admin scope and baseline commit.
