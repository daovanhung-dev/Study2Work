---
task_id: "2026-11-26-load-project-web-context"
date: "2026-11-26"
primary_task_type: "coding"
secondary_task_types: []
project_scopes: ["web-work"]
cross_scope_dependencies: ["Study Web → Study Server API contract/source; exact APIs are task-specific and not selected yet"]
status: "PARTIAL"
---

# Worklog: Nạp context dự án và coding web

## READ_PLAN

| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `.agents/AGENTS.md` | Global context index, scope registry, target/read-set rules, maintenance | Bootstrap and route web coding | `READ` |
| `.agents/context-map.md` | Canonical load flow and web-work graph | Select exact web coding context | `READ` |
| `.agents/context-manifest.json` | web-work scope, coding workflow, registered page references | Verify registered context/workflow wiring | `READ` |
| `.agents/project/agent-control.md` | Target, silent communication, worklog and verification rules | Apply task control requirements | `READ` |
| `.agents/target.md` | Active target table | Preserve existing target and track this task | `READ` |
| `.agents/worklog/README.md` | Read-set discipline, preflight, required order | Create and maintain canonical worklog | `READ` |
| `.agents/worklog/TEMPLATE.md` | Required sections and fields | Match worklog contract | `READ` |
| `scripts/select-worklogs.mjs` | Selector behavior through required command | Run coding preflight | `CHECKED_BY_TOOL` |
| `.agents/worklog/2026-11-21/2026-11-21-study_server_create_admin_context.md` | Carry-forward facts relevant to coding web context | Review selected same-type prior worklog | `READ` |
| `.agents/worklog/2026-11-21/commit-admin-ad-screens.md` | Carry-forward facts relevant to coding web context | Review selected same-type prior worklog | `READ` |
| `.agents/worklog/2026-11-21/complete-ad01-ad25-dd-safe.md` | Carry-forward facts relevant to coding web context | Review selected same-type prior worklog | `READ` |
| `.agents/project/INDEX.md` | Project page graph and page selection | Load the project-wide coding context requested by the user | `READ` |
| `.agents/project/architecture.md` | Ownership and deployable boundaries | Understand the Study Web/Study Server boundary | `READ` |
| `.agents/project/dependencies.md` | Study Web ↔ Study Server API dependency map | Ground the active Study UI/API goal in registered dependencies | `READ` |
| `.agents/project/contracts.md` | Shared/local contract routing and status | Identify where API/UI contract evidence belongs | `READ` |
| `.agents/project/conventions.md` | Repository-wide section and coding workflow/checklists | Load cross-project conventions applicable to web coding | `READ` |
| `.agents/project/design.md` | Work Web/Mobile design guidance | Not applicable to the active Study Web goal; Study-specific design page is used instead | `SKIPPED` |
| `.agents/project/workflows.md` | Common flow and Coding/Study Web workflow routing | Load the registered project coding sequence | `READ` |
| `.agents/web-work/AGENTS.md` | Scope instructions and routing | Load web coding constraints and distinguish Study/Work apps | `READ` |
| `.agents/web-work/INDEX.md` | Page graph for web-work | Choose general coding pages | `READ` |
| `.agents/web-work/architecture.md` | Work Web architecture | Not applicable to Study Web; avoid mixing React and Angular patterns | `SKIPPED` |
| `.agents/web-work/conventions.md` | Work Web conventions | Not applicable to Study Web; avoid mixing React and Angular patterns | `SKIPPED` |
| `.agents/web-work/dependencies.md` | Work Web dependencies | Not applicable to Study Web; Study API boundary is covered by project and Study pages | `SKIPPED` |
| `.agents/web-work/modules/README.md` | Work Web module routing | Not applicable to Study Web; feature context will be selected from Study catalog per task | `SKIPPED` |
| `.agents/web-work/workflows/README.md` | Work Web workflow routing | Not applicable to Study Web; use dedicated Study Web workflow | `SKIPPED` |
| `.agents/web-work/study/AGENTS.md` | Study Web subcontext and coding routing | Load the active Study Web coding context indicated by the current AD-02 target | `READ` |
| `.agents/web-work/study/INDEX.md` | Study Web page graph; current status and mandatory Study FE preflight section | Determine current screen-level context boundaries and task-specific DD/API loading rule | `READ` |
| `.agents/web-study/design.md` | Study Web visual/interaction/accessibility rules | Load mandatory Study Web coding design constraints | `READ` |
| `.agents/web-study/frontend-rules.md` | Study Web screen groups and frontend layer rules | Load mandatory Study Web coding structure | `READ` |
| `.agents/web-work/study/workflows/screen-implementation.md` | Study Web screen implementation workflow | Load registered coding/test/demo process for future screen work | `READ` |
| `apps/study-client/gui/architech.md` | Architecture sections: purpose/boundary, project structure, responsibilities, data flow, UI/accessibility and development/verification rules; exclude screen-specific historical status sections | Load implementation architecture referenced by the Study Web router | `READ` |

## LEAF_TARGET_PLAN

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Nạp context coding web — xác định quy ước và workflow đã đăng ký | Đọc scope web-work cùng workflow coding liên quan | Worklog ghi các page đã đọc, workflow registry và carry-forward facts; target được gỡ khi đủ bằng chứng |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: coding
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-21/2026-11-21-study_server_create_admin_context.md`
    - carry_forward: Context-only task; no source edits/tests. Its selector selected three coding worklogs and it recorded current source/schema discrepancy; not applicable to Web implementation.
  - path: `.agents/worklog/2026-11-21/commit-admin-ad-screens.md`
    - carry_forward: Study Admin implementation series was committed; authenticated browser/live API/DB/deployment remained unverified. Historical commit state does not replace current source inspection.
  - path: `.agents/worklog/2026-11-21/complete-ad01-ad25-dd-safe.md`
    - carry_forward: Study Web AD-01–AD-25 was completed at static DD-safe status with focused Admin specs passing at that time; unresolved behavior stayed gated and runtime remained unverified. Source may have changed, so verify exact current files for any future feature task.
- shortage: `none` (3 of 3 available coding logs reviewed; selector reported 166 available)

## EXPECTED_BEHAVIOR

- Requirement: Nạp project context và Study Web coding context để tiếp tục mục tiêu đang hoạt động: chuẩn hóa toàn bộ Study UI theo DD, API, logic và production readiness.
- Canonical contract/approved DD: Không có DD/feature contract cụ thể trong yêu cầu này; dùng router, manifest và context coding đã đăng ký.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Nạp context coding web — xác định quy ước và workflow đã đăng ký | `0% → 0%` | Target lá tạo từ yêu cầu; hoàn tất khi các page registered đã được đọc và ghi nhận trong worklog. |
| Nạp context coding web — xác định quy ước và workflow đã đăng ký | `0% → 100%` | Đọc router/context map/manifest/Agent Control, 3 coding worklogs, project architecture/dependencies/contracts/conventions/workflow, Study Web entry/index/design/frontend rules/screen coding workflow/scaffold architecture; xác nhận coding workflow registry và ghi rõ current-source blockers/doc discrepancies. |

## CURRENT_BEHAVIOR

- Source/config: Không mở source implementation vì chưa có screen/API cụ thể. Context đã nạp xác định Study Web là Angular 22 SPA; web layer đi qua relative `/api/v1` và Study API. Study OpenAPI còn placeholder (`NOT_FOUND`); production routing/deployment và live API/DB chưa được xác minh trong context.
- Runnable tests: Không chạy test theo yêu cầu context-only. Prior logs ghi focused tests theo từng task trong tháng 11; chúng là bằng chứng lịch sử, không xác minh checkout hiện tại.
- Runtime wiring: Context scope hiện ghi `VERIFIED_WITH_UNWIRED_COMPONENTS`; status này không xác minh mọi screen. Catalog/DD và design mô tả expected behavior; source và test hiện tại phải được kiểm tra riêng cho từng screen/API.

## SOURCE_TRACE

```text
Study screen/page -> screen-local data-access -> core HTTP transport -> relative /api/v1 -> Study API source
Expected: screen DD + API DD/catalog + approved requirement
Current: current Angular/Study API source + runnable tests + executable config (must be inspected per screen/API)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Goal production-ready vs current evidence | User goal requires all Study UI/API/logic production-ready; registered Study context says production routing, live API/DB and deployment remain unverified and notes unwired/gated behavior. No source audit occurred in this context-loading task. | `DISCREPANCY` | Do not treat static DD-safe percentages or this context load as production acceptance; future implementation must close and verify gaps per screen/API. |
| Study architecture page status | `.agents/project/architecture.md` says Guest/Mentor route groups are absent; `.agents/web-work/study/AGENTS.md` and `INDEX.md` record Guest and Mentor routes/callers. `apps/study-client/gui/architech.md` says GS-07 is gate-only with no ID/API #12, while the Study subcontext records GS-07 consuming the route ID and calling #12. No Angular source was inspected here. | `DISCREPANCY` | These architecture descriptions cannot settle current behavior. Recheck exact route/page/service/API source before work on affected screens; do not reconcile from docs alone. |

## CHANGES

- Files changed: `.agents/worklog/2026-11-26/load-project-web-context.md`, `.agents/target.md` (added then removed this task leaf row; preserved prior AD-02 target).
- CONTEXT_UPDATES: Context loading evidence only; no project context page edited.
- Context pages changed: None.
- Assumptions: The active user goal scopes web coding to Study Web; the Work Web React pages were explicitly skipped to avoid mixing app patterns. Feature-specific source/DD is deferred until a concrete screen implementation request.
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | Returned three coding worklogs; all three bodies reviewed and carry-forward facts recorded | `VERIFIED` |
| `node scripts/validate-agent-context.mjs` | Exit 1 `AGENT_CONTEXT_INVALID` with 84 findings, including missing DB Admin pages/source, orphan `create_dd_screen` resources, source inventory/context drift (including missing Study Web `features/auth/.gitkeep`). No finding matched this task's worklog or target tracker. No pre-task validator baseline was captured because this task changed only its worklog and the target tracker, not context pages or registry. | `PARTIAL; INVALID_CURRENT_CONTEXT` |

## HANDOFF

- Remaining blockers: No screen/API IDs were selected, so this context load does not establish behavior or completion for any Study screen.
- Next owner/action: For the active Study UI goal, select the requested screen(s), read both Study catalogs and exact DD/API references, then inspect current Angular and Study Server source/tests before changing UI/API/logic.
