---
task_id: "2026-11-12-load-project-context"
date: "2026-11-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["mobile-work", "web-work", "server-work", "server-study", "server-ai", "db-admin"]
cross_scope_dependencies: ["Work Web -> Work Server HTTP boundary; Study -> Work event schemas; DB Admin -> separate Neon control plane"]
status: "PARTIAL"
---

# Worklog: Nạp context dự án

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 278 worklogs cùng loại; đã chọn và đọc đủ 3.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-12/add-study-web-screen-rules-workflow.md`
    - carry_forward: Study Web hiện là Angular scaffold; catalog/DD là nguồn thiết kế, không chứng minh runtime; Study Web workflow yêu cầu xác định screen/API scope.
  - path: `.agents/worklog/2026-11-12/integrate-agent-control-prompt.md`
    - carry_forward: Agent Control là quy tắc toàn cục; validator có historical baseline 83 findings, nhưng phải chạy lại để biết tình trạng hiện tại.
  - path: `.agents/worklog/2026-11-11/add-study-fe-screen-api-context.md`
    - carry_forward: Study OpenAPI `NOT_FOUND`; giữ expected behavior và current source tách biệt; task không chạm screen/API có thể ghi `none`.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Nạp và tóm tắt project context theo router, context map, manifest, project pages và scope entry/index; ghi rõ context gap hoặc discrepancy thay vì suy đoán.
- Canonical contract/approved DD: Root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/context-manifest.json`, project index/pages và scope page graphs.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 50% | 50% | Hoàn tất phân loại, đọc router/context map, worklog preflight và ba worklog cùng loại. | `DONE` |
| 50% | 100% | Đọc project-wide pages và scope entry/index khả dụng; ghi tóm tắt cùng context gaps vào worklog; chạy context validator. | `DONE` |

## CURRENT_BEHAVIOR

- Source/config: Project context mô tả Study Web là Angular 22 scaffold; Work Web React/Vite; Work API Express/Prisma; Mobile Work dùng Flutter Student/Business flavors, direct Neon/SQLite/Gemini; Study Server FastAPI/sync SQLAlchemy; AI minimal FastAPI/Ollama với copied core `UNWIRED`; DB Admin là Angular/FastAPI control plane riêng. Study OpenAPI là `NOT_FOUND`; Work OpenAPI có `DISCREPANCY`; Study→Work event consumer `DECLARED_NOT_RUNNABLE`. DDL trong repository không chứng minh live schema. `.agents/db-admin/AGENTS.md` và `.agents/db-admin/INDEX.md` được registry/map khai báo nhưng không có trên filesystem.
- Runnable tests: Không chạy; task chỉ nạp context và ghi worklog.
- Runtime wiring: Chỉ dùng trạng thái đã ghi trong context; không kiểm tra source/runtime/test hiện hành cho bất kỳ app cụ thể nào.

## SOURCE_TRACE

```text
AGENTS.md -> .agents/AGENTS.md -> context-map/manifest -> worklog preflight -> project pages -> scope AGENTS/INDEX -> context summary/worklog -> context validator
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| DB Admin scope entry pages | `.agents/AGENTS.md`, `context-map.md` và manifest khai báo `.agents/db-admin/AGENTS.md` + `INDEX.md`; `cat` cả hai đường dẫn trả `No such file or directory`. | `NOT_FOUND / DISCREPANCY` | Scope summary chỉ có thể dựa vào global source-status và project pages; task DB Admin cụ thể cần khôi phục/đối chiếu context page graph trước khi deep work. |
| Study Server endpoint/test counts | `.agents/server-study/AGENTS.md` ghi 58 path templates / 69 operations và 1326 tests; `.agents/project/source-status.md` (refresh 2026-10-26) ghi 57/68 và 1315 tests. | `DISCREPANCY` | Chưa đọc source/test hiện tại để phân xử; không coi một trong hai số là xác nhận runtime hôm nay. |
| Freshness of source status | Global source-status ghi deep-context snapshot 2026-09-18; Study Server refresh 2026-10-26. Current date is 2026-11-12. | `SOURCE_STATUS_NOT_CURRENTLY_REVERIFIED` | Context là routing/evidence baseline; task scope cụ thể phải recheck current source, runnable tests, and executable contracts. |

## CHANGES

- Files changed: `.agents/worklog/2026-11-12/load-project-context.md`.
- CONTEXT_UPDATES: Added the required audit worklog for this context-loading task; no project source or context registry page was changed.
- Context pages changed: none.
- Assumptions: `docs` is the closest registered `primary_task_type` for an information-only project-context load; the task DoD includes surfacing unavailable or conflicting context rather than treating it as complete evidence.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`; 278 matching logs, three selected. | `VERIFIED` |
| Selected three worklogs and `.agents/worklog/TEMPLATE.md` | Read all selected logs and template; carry-forward facts recorded above. | `VERIFIED` |
| Root/global context, project pages, six scope AGENTS/INDEX paths | Read available pages; DB Admin AGENTS and INDEX returned `NOT_FOUND`; Study Server documented counts conflict. | `PARTIAL` |
| `git status --short`; `git branch --show-current`; worklog destination check | Worktree was clean before this file was added, branch `develop`, destination absent. | `VERIFIED` |
| `node scripts/validate-agent-context.mjs` | Exit 1, `AGENT_CONTEXT_INVALID`, 83 repository findings: 32 DB Admin findings, 33 `ORPHAN_SKILL_RESOURCE`, 10 broken context links, 7 `CONTEXT_STALE` scope groups (`server-study`, `server-work`, `web-work`, `web-work/study-web`, `web-work/work-web`, `mobile-work`, `db-admin`), and 1 missing DB Admin local-contract path. | `BASELINE_INVALID` |
| Application tests/build | Not requested or run. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Canonical DB Admin scope pages are missing from the working tree; Study Server status counts conflict between context pages; current app source/tests were not reverified for this general context load.
- Next owner/action: Before a scope-specific task, load its registered pages and verify exact current source/contracts/tests. Restore or update DB Admin context entry/index as a separate context-maintenance task if that scope is needed.
