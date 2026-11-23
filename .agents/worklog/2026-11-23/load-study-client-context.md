---
task_id: "2026-11-23-load-study-client-context"
date: "2026-11-23"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Nạp context dự án và apps/study-client

## READ_PLAN

| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `AGENTS.md` | Toàn bộ nội dung được cung cấp trong task context | Router bắt buộc; đã được cấp sẵn, không mở lại | `READ_FROM_CONTEXT` |
| `.agents/AGENTS.md` | Global context index, read-set, worklog và target rules | Xác định luồng context bắt buộc | `READ` |
| `.agents/context-map.md` | Canonical load flow, project tree, web-work/study-web graph | Chọn đúng context cho apps/study-client | `READ` |
| `.agents/context-manifest.json` | Registry worklog, web-work/study-web pages và workflow | Xác minh page/workflow được wire | `READ` |
| `.agents/project/agent-control.md` | Target, silent execution, read-set và worklog rules | Áp dụng quản lý tiến độ và bằng chứng | `READ` |
| `.agents/target.md` | Bảng target hiện tại | Kiểm tra tracker trước khi thêm target | `READ` |
| `.agents/worklog/README.md` | Read-set discipline, preflight, required order | Tạo worklog và chạy selector đúng quy định | `READ` |
| `.agents/worklog/TEMPLATE.md` | Worklog fields and sections | Khởi tạo worklog theo contract | `READ` |
| `scripts/select-worklogs.mjs` | CLI args and exact-type selection | Thực hiện preflight worklog cùng loại | `READ` |
| `scripts/validate-agent-context.mjs` | Run validator only, after task metadata updates | Xác minh cấu trúc context/worklog theo router | `CHECKED_BY_TOOL` |
| `.agents/worklog/2026-11-23/load-study-client-context.md` | Current worklog content created in this task | Selector included the current entry; distinguish it from historical carry-forward logs | `READ_FROM_CONTEXT` |
| `.agents/worklog/2026-11-21/2026-11-21-build-server-web-commands.md` | Summary, current behavior, context updates, verification, handoff | Review selected docs worklog for carry-forward facts | `READ` |
| `.agents/worklog/2026-11-21/document-server-and-script-prompts.md` | Summary, current behavior, context updates, verification, handoff | Review selected docs worklog for carry-forward facts | `READ` |
| `.agents/project/INDEX.md` | Project context page graph | Nạp context dự án và chọn trang liên quan Study Web | `READ` |
| `.agents/project/architecture.md` | Ownership và deployable boundaries liên quan Study Web | Hiểu vị trí apps/study-client trong kiến trúc dự án | `READ` |
| `.agents/project/dependencies.md` | Dependency map liên quan Study Web | Nạp liên kết scope/contract có liên quan | `READ` |
| `.agents/project/source-status.md` | Snapshot, trạng thái source/context, discrepancies | Nạp giới hạn bằng chứng hiện tại của dự án | `READ` |
| `.agents/web-work/AGENTS.md` | Scope rules và route đến Study Web subcontext | Nạp quy tắc scope sở hữu apps/study-client | `READ` |
| `.agents/web-work/INDEX.md` | Web Work page graph và subcontext links | Chọn đúng page Study Web | `READ` |
| `.agents/web-work/study/AGENTS.md` | Study Web scope rules | Nạp quy tắc cụ thể của apps/study-client | `READ` |
| `.agents/web-work/study/INDEX.md` | Study Web context graph and source status | Nạp các nguồn chuẩn cho Study Web | `READ` |
| `apps/study-client/gui/architech.md` | App scaffold, Angular folder and responsibility architecture | Nạp cấu trúc hiện tại của chính apps/study-client theo page graph | `READ` |
| `.agents/web-study/frontend-rules.md` | Frontend architecture, route and layer rules | Nạp quy tắc cấu trúc của apps/study-client | `READ` |
| `.agents/web-study/design.md` | Study Web visual, interaction and accessibility guide | Nạp tiêu chuẩn UX liên quan Study Web | `READ` |
| `.agents/web-work/study/workflows/screen-implementation.md` | Screen implementation workflow | Nạp workflow đã đăng ký cho Study Web | `READ` |

## LEAF_TARGET_PLAN

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Nạp context dự án dùng cho Study Web | Đọc project index và các trang global liên quan | Worklog ghi được ownership, dependency và source-status từ các trang đã đọc |
| Nạp context Study Web cho apps/study-client | Đọc scope entry/index, app architecture và các trang Study Web được registry chỉ định | Worklog ghi được scope rules, app structure, page graph, frontend/design rules và workflow |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-21/2026-11-21-build-server-web-commands.md`
    - carry_forward: Prior source-backed note records Study Web `npm start` at `http://localhost:4200` and its `/api/v1` proxy to Study API `127.0.0.1:3003`; it is historical and must not replace current source checks for implementation work.
  - path: `.agents/worklog/2026-11-21/document-server-and-script-prompts.md`
    - carry_forward: No Study Web-specific carry-forward facts; the entry covers server documentation across server-study, server-work and server-ai.
- selector also returned this task's just-created worklog; it was already available from task context and is not a prior task.
- shortage: `none` (3 matching worklogs available; selector included the current task entry plus two historical entries)

## EXPECTED_BEHAVIOR

- Requirement: Nạp context dự án và phần `apps/study-client`.
- Canonical contract/approved DD: Root router maps `apps/study-client/` to `web-work/study-web`; registry and context map determine the pages to load.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Nạp context dự án dùng cho Study Web | `0% → 100%` | Đã đọc project index, ownership, dependency và source-status pages; ghi nhận Study Web boundary và giới hạn của source-status trong `CURRENT_BEHAVIOR`/`DISCREPANCIES_AND_STATUSES`. |
| Nạp context Study Web cho apps/study-client | `0% → 100%` | Đã đọc scope router/index, app architecture, frontend rules, design guide và registered screen workflow; ghi nhận page graph cùng các mâu thuẫn giữa context pages. |

## CURRENT_BEHAVIOR

- Source/config: Project context identifies `apps/study-client/` as a standalone Angular 22 SPA. Study Web is a separate client boundary using relative `/api/v1`; local context records Angular dev proxy to Study API `127.0.0.1:3003` and client URL `http://localhost:4200`. Production routing/deployment is unverified. `gui/architech.md` documents scaffold/folder architecture, but its Shared and Guest behavior summary conflicts with the later Study Web scope pages. These are context claims; application source was not opened for this context-loading request.
- Runnable tests: Not applicable; no implementation or behavior change requested and no tests were run.
- Runtime wiring: Study Web pages describe Shared, Guest, Student, Mentor and Admin route groups and screen-specific API callers. The root context map and Study Web pages conflict on GS-07/#12; see `DISCREPANCIES_AND_STATUSES`. No runtime claim was revalidated against source.

## SOURCE_TRACE

Not applicable; read-only context loading, no source behavior or runtime path changed.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Shared/Auth route behavior | `apps/study-client/gui/architech.md` says SH-02 is presentation-only and SH-04 is static with no #02 call; `.agents/web-work/study/AGENTS.md` and `.agents/web-work/study/INDEX.md` say SH-02 calls #03 and SH-04 calls the accepted #02 stub after a one-use handoff. | `DISCREPANCY` | Verify current route/page source before work on SH-02–SH-04; the architecture document is not sufficient runtime evidence. |
| Guest route/resource behavior | `.agents/context-map.md` and `apps/study-client/gui/architech.md` say GS-07 is gate-only/no #12 caller and the architecture doc lists only the `?tab=curriculum` GS-03 panel; `.agents/web-work/study/AGENTS.md` and `.agents/web-work/study/INDEX.md` say GS-03 owns curriculum/reviews/resources tabs and GS-07 consumes the route ID/calls #12 with PUBLIC/PRIVATE handling. | `DISCREPANCY` | Verify current `apps/study-client/` and relevant API source before feature work; do not infer runtime behavior from these context pages alone. |
| Study API descriptor count | `.agents/context-map.md` says 103 typed descriptors plus R-X01; `.agents/web-work/study/AGENTS.md` and one section of `.agents/web-work/study/INDEX.md` say #1–#103, while the Study index registry row says 105 descriptors and other sections document #104/#105 callers. | `DISCREPANCY` | Recheck current source/catalog if a task depends on descriptor inventory or #104/#105 wiring. |
| Study Web entry in project source-status page | Search of `.agents/project/source-status.md` found no `Study Web`, `Study client` or `study-client` entry; details are instead in the registered Study Web context pages. | `NOT_FOUND` | Use the scope-specific pages for orientation, then current source for implementation claims. |

## CHANGES

- Files changed: `.agents/target.md`, this worklog only.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: `apps/study-client/` is routed through the registered `web-work/study-web` subcontext.
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`; selected current worklog plus two historical docs worklogs, both historical bodies reviewed; no shortage | `VERIFIED_PREFLIGHT` |
| Read registered project and Study Web context pages listed in `READ_PLAN` | Project ownership/dependencies and Study Web scope guidance loaded; internal status conflicts recorded rather than reconciled without source inspection | `VERIFIED_STATIC` |
| Search Study Web terms in `.agents/project/source-status.md` | No matching Study Web/study-client entry | `CHECKED_BY_TOOL` |
| Tests | Not run; no code or behavior change requested | `NOT_RUN` |
| `node scripts/validate-agent-context.mjs` | Exit 1, `AGENT_CONTEXT_INVALID`: repository-wide missing DB Admin context/source entries, orphan skill resources and stale source inventory; Study Web also reports missing tracked path `apps/study-client/src/app/features/auth/.gitkeep`. No application source/context pages were changed by this task. | `AGENT_CONTEXT_INVALID` |

## HANDOFF

- Remaining blockers: Context pages conflict on Shared/Auth and Guest behavior and API descriptor counts; current app/API source was not inspected because this task only requested context loading.
- Next owner/action: For a concrete Study Web feature, identify screen/API scope, read the mandatory screen catalogs, then verify current source and relevant contracts.
