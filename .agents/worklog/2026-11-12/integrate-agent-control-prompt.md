---
task_id: "2026-11-12-integrate-agent-control-prompt"
date: "2026-11-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "mobile-work", "server-work", "server-study", "server-ai", "db-admin"]
cross_scope_dependencies: ["Global .agents agent-control policy routes to every task scope; no application runtime contract dependency"]
status: "COMPLETED"
---

# Worklog: Tích hợp Agent Control Prompt vào agent context

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 277 worklogs cùng loại; đã chọn và đọc đủ 3.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-12/add-study-web-screen-rules-workflow.md`
    - carry_forward: Agent context pages phải được wire vào manifest/context map; Study stack hiện tại là Angular 22; validator có 83 finding baseline, gồm scope drift.
  - path: `.agents/worklog/2026-11-11/add-study-fe-screen-api-context.md`
    - carry_forward: Task không có screen/API phải ghi scope `none`; catalog/DD không chứng minh runtime.
  - path: `.agents/worklog/2026-11-11/list-study-api-endpoints.md`
    - carry_forward: API catalog là thiết kế; giữ discrepancy/source gaps, không suy ra runtime.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Nạp Agent Control Prompt như quy tắc toàn cục trong `.agents`, tự động được route cho mọi scope và dùng cùng progress/worklog model hiện có.
- Canonical contract/approved DD: Người dùng yêu cầu tích hợp `apps/study-client/docs/STUDY2WORK_AGENT_CONTROL_PROMPT.md` vào logic agents; giữ prompt nguồn nguyên trạng và cập nhật Study Web thành Angular 22 trong bản canonical.
- Study FE scope: `screens=none; APIs=none` — đây là thay đổi agent context, không triển khai Study screen/API.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 25% | 25% | Hoàn tất router, worklog preflight, current context và trạng thái worktree; chốt scope/an toàn. | `DONE` |
| 60% | 85% | Tạo canonical agent-control page và wire root context, project index/workflows, worklog contract, context map và manifest. | `DONE` |
| 15% | 100% | Kiểm tra JSON, links, diff, validator; cập nhật worklog và báo baseline còn lại. | `DONE` |

## CURRENT_BEHAVIOR

- Source/config: Prompt nguồn tại `apps/study-client/docs/STUDY2WORK_AGENT_CONTROL_PROMPT.md` đã tracked và sạch ở đầu task; branch `develop` ahead 1 và không có thay đổi worktree có sẵn. `.agents/project/INDEX.md`/manifest chưa có Agent Control page hoặc workflow; global worklog/workflow yêu cầu milestone và grouped receipts, chưa yêu cầu event record cho từng tool call. Current Study Client là Angular 22; prompt nguồn ghi Vue 3.
- Runnable tests: Không có app test/build trong scope; chỉ chạy kiểm tra context/registry và whitespace.
- Runtime wiring: Chưa có context page/workflow cho Agent Control; chưa có source/API/runtime behavior nào được thay đổi.

## SOURCE_TRACE

```text
root AGENTS.md -> .agents/AGENTS.md -> project/agent-control.md -> manifest/context-map/project workflow/worklog -> per-tool Task/Step/Action/Event receipts
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study frontend stack in prompt source | Prompt §2 says Vue 3/TypeScript/Vite; current `apps/study-client/package.json` and Angular source show Angular 22 standalone. | `RESOLVED_IN_CANONICAL / SOURCE_UNCHANGED` | Update only the Study row in canonical `.agents` copy; retain original prompt unchanged and continue to defer to current source. |
| Existing validator baseline | Previous task validator recorded 83 findings across missing DB Admin context/source, orphan DD skill resources, legacy DB Admin links/contracts and stale source snapshots. | `BASELINE_INVALID` | Run validator after changes; distinguish new Agent Control wiring errors from pre-existing findings; do not reset global source commit. |

## CHANGES

- Files changed: `.agents/project/agent-control.md` (copy, Angular 22 row, 10 Markdown hard breaks normalized); `.agents/AGENTS.md`; `.agents/project/INDEX.md`; `.agents/project/workflows.md`; `.agents/worklog/README.md`; `.agents/context-manifest.json`; `.agents/context-map.md`; this worklog.
- CONTEXT_UPDATES: Copied the prompt into the canonical project context and changed the Study Web stack row to Angular 22. Required all scopes to load the control page; registered workflow `agent-control` with `scopeRefs: ["all"]`; synchronized per-tool Event receipts and milestone-based verified progress in the root context, project workflow, worklog instructions and context map. Original prompt remains unchanged.
- Context pages changed: `.agents/project/agent-control.md`; `.agents/AGENTS.md`; `.agents/project/INDEX.md`; `.agents/project/workflows.md`; `.agents/worklog/README.md`; `.agents/context-manifest.json`; `.agents/context-map.md`.
- Assumptions: Keep source prompt unmodified; `.agents/project/agent-control.md` is canonical. The protocol applies to every scope through workflow `scopeRefs: ["all"]`; its verified progress maps to existing worklog milestones without double-counting bootstrap discovery.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Worklog selector and selected logs | `READY`; 3 of 277 `docs` worklogs selected and read. | VERIFIED |
| Root router, global context, project index/workflow, worklog contract, current worktree and prompt | Confirms current page graph, current dirty/untracked state, prompt source, and Study Angular 22 discrepancy. | VERIFIED_STATIC_ONLY |
| Manifest JSON and registry | Parsed successfully; `agent-control` page and workflow are registered, workflow status is `VERIFIED`, and `scopeRefs` contains `all`. | VERIFIED |
| Global wiring links | Canonical page and all required global context/worklog entry files exist and reference Agent Control. | VERIFIED_STATIC_ONLY |
| `git diff --check` and new-file whitespace | Tracked diff returned 0; no-index checks for the canonical page and this worklog returned the expected 1 with no whitespace diagnostics. | VERIFIED |
| Original prompt and canonical comparison | Original prompt remains tracked and unchanged. After ignoring `<br>` hard-break normalization, the only semantic difference is the Study frontend row updated to Angular 22 standalone/TypeScript. | VERIFIED |
| `node scripts/validate-agent-context.mjs` (Node 22.23.4) | Exit 1, `AGENT_CONTEXT_INVALID`; 83 existing findings: db-admin 32, contract 1, `ORPHAN_SKILL_RESOURCE` 33, broken context link 10, `CONTEXT_STALE` 7. No finding mentions `agent-control`. | BASELINE_INVALID; no new Agent Control finding |
| Application tests/build | Not run; documentation/context-only scope and explicitly excluded from the approved verification plan. | NOT_RUN |

## HANDOFF

- Remaining blockers: No task-specific blocker. Repository-wide context validator remains invalid due to the 83 categorized baseline findings above.
- Next owner/action: None for this task. Existing validator baseline findings are outside the approved Agent Control integration scope.
