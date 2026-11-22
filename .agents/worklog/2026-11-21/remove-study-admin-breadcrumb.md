---
task_id: "2026-11-21-remove-study-admin-breadcrumb"
date: "2026-11-21"
primary_task_type: "coding"
secondary_task_types: []
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Xóa dải breadcrumb khỏi Study Admin

## READ_PLAN

| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `AGENTS.md` | supplied router instructions | classify task and follow repository read/worklog rules | `READ_FROM_CONTEXT` |
| `.agents/AGENTS.md` | global routing and read-set rules | scope and context flow | `READ` |
| `.agents/context-map.md` | canonical graph and Study Web subcontext | choose the registered Web context | `READ` |
| `.agents/context-manifest.json` | web-work/study-web entries and coding workflow | confirm scope and registered context | `CHECKED_BY_TOOL` |
| `.agents/project/agent-control.md` | leaf target, worklog, preservation rules | track this one UI removal | `READ` |
| `.agents/target.md` | active target table | replace the completed previous target with this task's leaf | `READ` |
| `.agents/worklog/README.md` | read-set and preflight requirements | follow task worklog contract | `READ` |
| `.agents/worklog/TEMPLATE.md` | required worklog fields | initialize this task log | `READ` |
| `scripts/select-worklogs.mjs` | selector invocation | choose prior coding worklogs | `CHECKED_BY_TOOL` |
| `.agents/worklog/2026-11-21/2026-11-21-study_server_create_admin_context.md` | relevant carry-forward | retain Study Admin context and boundaries | `READ` |
| `.agents/worklog/2026-11-21/commit-admin-ad-screens.md` | relevant carry-forward | preserve Admin Web source and verification boundaries | `READ` |
| `.agents/worklog/2026-11-21/complete-ad01-ad25-dd-safe.md` | relevant carry-forward | preserve the Admin portal's approved UI scope | `READ` |
| `scripts/validate-agent-context.mjs` | required context validation | check the updated Study Web context pages | `PLANNED` |
| `.agents/project/workflows.md` | coding workflow | confirm implementation and verification sequence | `READ` |
| `.agents/web-work/AGENTS.md` | Study/Web source scope and rules | follow Web implementation conventions | `READ` |
| `.agents/web-work/INDEX.md` | Web page graph | route to Study Web context | `READ` |
| `.agents/web-work/workflows/README.md` | parent Web workflow | confirm shared layout change workflow | `READ` |
| `.agents/web-work/study/AGENTS.md` | Study Web-specific rules | confirm shared Study Web conventions | `READ` |
| `.agents/web-work/study/INDEX.md` | Study Web context graph | route shared Admin layout source | `READ` |
| `.agents/web-study/frontend-rules.md` | layer/layout constraints | keep the smallest template-only change | `READ` |
| `apps/study-client/src/app/layouts/admin/admin-layout.html` | Admin shell header and breadcrumb row | remove exactly the cropped breadcrumb strip | `READ` |
| `apps/study-client/src/app/layouts/admin/admin-layout.css` | breadcrumb styles and shell spacing | check for spacing left by removing the row | `READ` |
| `apps/study-client/src/app/layouts/admin/admin-layout.ts` | shared layout component | confirm breadcrumb behavior is not generated in TypeScript | `READ` |

## LEAF_TARGET_PLAN

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Xóa dải breadcrumb khỏi layout Admin của Study Web | Remove the cropped breadcrumb path from the Admin layout template | Breadcrumb path no longer exists; session-status row, primary navigation and page outlet remain intact |
| Cập nhật context Study Web cho layout Admin không còn breadcrumb | Update the stale Admin layout description | Registered Study Web context no longer describes a stable workspace breadcrumb |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-21/2026-11-21-study_server_create_admin_context.md`
    - carry_forward: preserve the active dirty worktree and keep this layout-only change independent of the prior Study Server bootstrap task.
  - path: `.agents/worklog/2026-11-21/commit-admin-ad-screens.md`
    - carry_forward: the worktree contains prior Admin screen work; preserve it and keep changes limited to the shared shell and its context description.
  - path: `.agents/worklog/2026-11-21/complete-ad01-ad25-dd-safe.md`
    - carry_forward: the prior Admin context described a stable shell breadcrumb; the user's latest instruction overrides that presentation choice, while page-level breadcrumb content remains intact.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: remove the cropped shell breadcrumb path shown between the Admin navigation and dashboard content; preserve the separate session-status indicator, routed content and page-level breadcrumbs.
- Canonical contract/approved DD: user-provided current screenshot and cropped breadcrumb reference.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Xóa dải breadcrumb khỏi layout Admin của Study Web | `0% → 0%` | Initial leaf target; acceptance is removal of the cropped path while the session-status row remains. |
| Cập nhật context Study Web cho layout Admin không còn breadcrumb | `0% → 0%` | Initial leaf target; acceptance is that both registered Study Web context pages match the layout. |
| Xóa dải breadcrumb khỏi layout Admin của Study Web | `0% → 100%` | Removed the breadcrumb nav/list and its styles; kept the separate session-status row; `rg` found no remaining breadcrumb selector in the Admin layout. |
| Cập nhật context Study Web cho layout Admin không còn breadcrumb | `0% → 100%` | Updated both registered Study Web context pages to state that the shell omits the breadcrumb path, retains session status and leaves page breadcrumbs to routed screens. |

## CURRENT_BEHAVIOR

- Source/config: `AdminLayout` no longer renders the breadcrumb navigation/list or its styles. The session-status row remains in the shell; the dashboard page-level breadcrumb also remains outside the shared layout.
- Runnable tests: no tests requested or run; verification is limited to source search and diff checks.
- Runtime wiring: user screenshot shows the shared Admin shell at `/admin`.

## SOURCE_TRACE

```text
Admin route -> shared AdminLayout template -> breadcrumb-row markup -> visible breadcrumb strip -> dashboard outlet
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Admin shell rendered a shared breadcrumb path the user wanted removed | user screenshot/cropped reference; current template no longer contains the breadcrumb navigation/list | `FIXED` | The cropped path is removed while the session indicator remains |

## CHANGES

- Files changed: `admin-layout.html`, `admin-layout.css`, two Study Web context pages and this worklog. The prior completed database-migration target was cleared before tracking these two leaf targets; the tracker is header-only again after completion.
- CONTEXT_UPDATES: removed stale wording that promised a stable shared shell breadcrumb and recorded that the session-status row remains.
- Context pages changed: `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`.
- Assumptions: remove the shared breadcrumb path across Admin routes because it belongs to the shared Admin layout; preserve the separate session-status row.
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `rg -n 'breadcrumb' apps/study-client/src/app/layouts/admin/admin-layout.html apps/study-client/src/app/layouts/admin/admin-layout.css apps/study-client/src/app/layouts/admin/admin-layout.ts` | exit 1, no matches in the Admin layout files | `VERIFIED_ABSENT` |
| `git diff --check` | exit 0 | `VERIFIED` |
| `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/validate-agent-context.mjs` | Exit 1 `AGENT_CONTEXT_INVALID`; missing db-admin context/source, orphan skill resources and broad stale context findings persist from the prior task baseline. | `VERIFIED_WITH_BASELINE_FAILURES` |

## HANDOFF

- Remaining blockers: rendered-browser visual confirmation was not run; no application tests were requested.
- Next owner/action: refresh `/admin` to see the breadcrumb path removed; the session-status row and page-level dashboard breadcrumb remain.
