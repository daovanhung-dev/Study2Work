---
task_id: "2026-11-05-read-study-screen-design-reference"
date: "2026-11-05"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study screen inventory -> Study API catalog #01-#103"]
status: "PARTIAL"
---

# Worklog: Đọc Study screen design system và inventory

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; đã chọn và đọc đủ 3 worklog trong 143 worklog `docs` khả dụng.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-05/check-study-screen-stitch-coverage.md`
    - carry_forward: Inventory có 83 ID duy nhất, bao phủ trong 84 thư mục artifact do SH-01 có hai variants; screen files là design, không chứng minh runtime.
  - path: `.agents/worklog/2026-11-05/load-study2work-context.md`
    - carry_forward: Study Web runtime/subcontext không có trong checkout; giữ nguyên `screen_stitch/` và kiểm tra source riêng trước khi kết luận wiring.
  - path: `.agents/worklog/2026-11-05/organize-study-screen-stitch.md`
    - carry_forward: Tài liệu `study2work_lms/DESIGN.md` được xếp vào `90_reference/`; 169 nội dung artifact trước đó được kiểm tra không đổi sau khi phân nhóm.
- shortage: `none` (143 worklog docs khả dụng; đã đọc đủ 3 được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Đọc đầy đủ `apps/study-client/docs/screen_stitch/90_reference/study2work-lms-design-system/DESIGN.md` và `apps/study-client/docs/list_screen.md` để nạp design reference và inventory Study.
- Canonical contract/approved DD: `list_screen.md` tự xác định là `DESIGN_BASELINE / NEEDS_CONTRACT_REVIEW`, input cho DD Screen; không xác nhận implementation. `DESIGN.md` là reference design system trong `90_reference`.

## CURRENT_BEHAVIOR

- Source/config: Đã đọc toàn bộ hai file được yêu cầu. `DESIGN.md` mô tả Corporate/Modern EdTech, token YAML, Plus Jakarta Sans, responsive grid 12/8/4, elevation, shapes và controls. `list_screen.md` mô tả 4 actor, 30 UC/AC, 83 UI surfaces và 103 API IDs; gồm route proposal, API orchestration, data mapping, UI state, 16 decision gates và wave tạo DD.
- Runnable tests: Không chạy; đây là yêu cầu đọc tài liệu.
- Runtime wiring: Hai tài liệu là design reference/inventory. Không kiểm tra hoặc khẳng định Study Web runtime/API deployment trong task này.

## SOURCE_TRACE

```text
selected docs worklogs -> DESIGN.md token/style/component reference -> list_screen.md scope and 83 surfaces -> API journey/data/gates/state/waves
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Color token values inside DESIGN.md | YAML lists `primary #004ac6`, `secondary #006c49`, `tertiary #784b00`; prose/components call primary `#2563EB`, secondary `#10B981`, tertiary `#F59E0B`. | `DOC_DISCREPANCY` | Keep both sets explicit until an owner selects the canonical token values. |
| Control hit area | DESIGN.md specifies desktop button height 40px and input height 42px; list_screen §6.3 asks for touch target >=44px. | `DOC_DISCREPANCY / NEEDS_REVIEW` | A future visual implementation needs explicit sizing by platform/viewport. |
| Runtime classifications | list_screen describes its source snapshot as 2026-09-27 and says frontend router only has `/`, API #01–#07 are wired and much of #08–#103 is `D`; newer Study Server context reports source through #98, while current checkout lacks Study Web `src`. | `DOC_CONTEXT_DISCREPANCY / SOURCE_RECHECK` | Use inventory IDs/flows as design baseline; recheck source before relying on its runtime classifications. |

## CHANGES

- Files changed: `.agents/worklog/2026-11-05/read-study-screen-design-reference.md` (this audit entry only).
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: Request was to read and load these two specific documents; no design token reconciliation or artifact edits were requested.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type docs --limit 3` | Selected 3 exact-type worklogs from 143; all three were read. | VERIFIED |
| `apps/study-client/docs/screen_stitch/90_reference/study2work-lms-design-system/DESIGN.md` | Read from frontmatter through specialized EdTech components. | VERIFIED_STATIC_ONLY |
| `apps/study-client/docs/list_screen.md` | Read all sections 0–9, including all 83 surfaces, flows, API index, state rules, gates, DD plan and limits. | VERIFIED_STATIC_ONLY |
| `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/validate-agent-context.mjs` | Exit 1 (`AGENT_CONTEXT_INVALID`) on pre-existing missing Study Web/DB Admin context/source, broken links, and stale `server-study`/`db-admin` snapshots. | FAILED / PRE_EXISTING_CONTEXT_DRIFT |
| Tests/runtime/deployment | Not run or probed. | NOT_RUN |

## HANDOFF

- Remaining blockers: Documentation has color and control-size discrepancies; runtime classifications may be stale against current Study source; repository context validator remains failed on pre-existing missing paths and stale snapshots.
- Next owner/action: Use the inventory as a design baseline. Before implementation or visual sign-off, choose canonical Study tokens and inspect current API/frontend source for the specific screen.
