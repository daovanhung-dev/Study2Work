---
task_id: "2026-11-21-revise-agent-target-tracking-context"
date: "2026-11-21"
primary_task_type: "docs"
secondary_task_types: ["coding"]
project_scopes: ["mobile-work", "web-work", "server-work", "server-study", "server-ai", "db-admin"]
cross_scope_dependencies: ["Root router -> global agent context -> target tracker, worklog contract, manifest registry, and context validator."]
status: "VERIFIED"
---

# Worklog: Cập nhật quy tắc target và tiến độ cho agent

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 287 available; 3 selected and read fully; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-19/load-full-project-and-web-context.md`
    - carry_forward: Keep Study Web and Work Web scope boundaries explicit; distinguish current source evidence from context claims.
  - path: `.agents/worklog/2026-11-19/load-full-project-context.md`
    - carry_forward: DB Admin context/source and unrelated context-registry gaps already existed; retain explicit discrepancy statuses.
  - path: `.agents/worklog/2026-11-19/update-screen-completion-percent.md`
    - carry_forward: Historical screen percentages are source-specific scores; do not reuse them as task progress.
- shortage: `none`.

## EXPECTED_BEHAVIOR

- Requirement: Use `.agents/target.md` as the only live progress view, with exactly `STT`, `Tên target`, `Tiến độ hoàn thiện`; update it when verified target progress changes, remove completed rows after recording evidence, and suppress automatic chat status, receipts, milestones and final reports.
- Approved plan: Update root and global `.agents/` instructions, worklog contract, context map/workflows/registry, target validator, and mark the old Study2Work control prompt superseded. Keep historical worklogs unchanged and preserve all unrelated dirty user changes.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Cập nhật quy tắc target và tiến độ cho agent | `— → 0%` | Created the active target at task start; acceptance is the context/registry/validator/prompt update and baseline-aware verification. |
| Cập nhật quy tắc target và tiến độ cho agent | `0% → 85%` | Updated active instructions, worklog template, context map/workflows, schema v4 registry, target validator and deprecated prompt; static links and target/manifest shape reviewed. Current validator has 81 unique findings, exactly matching the pre-edit baseline. |
| Cập nhật quy tắc target và tiến độ cho agent | `85% → 95%` | Active guidance search confirms old display requirements are removed; validator comparison reports 0 introduced and 0 resolved findings. Final worklog/target cleanup and post-edit validation remain. |
| Cập nhật quy tắc target và tiến độ cho agent | `95% → 100%` | Completed the approved context, registry and validator changes; recorded completion evidence here and removed the completed row from `.agents/target.md`. Final validator comparison is recorded below. |

## CURRENT_BEHAVIOR

- Source/config: Root `AGENTS.md`, `.agents/AGENTS.md`, context map, project workflow, Agent Control and worklog docs required chat events/milestones. `.agents/target.md` was empty. Manifest schema was 3 and did not register target tracking. The old Study2Work prompt repeated the prior chat/event protocol.
- Runnable tests: Not applicable; this is a context/validator change. Context validator was run before edits and exited 1 with existing DB Admin missing context/source, orphan create_dd_screen resources, broken DB Admin context links and source drift.
- Runtime wiring: Context manifest and `scripts/validate-agent-context.mjs` define the machine-readable context registry and validation.

## SOURCE_TRACE

```text
user request -> AGENTS.md -> .agents/AGENTS.md/context-map -> target/worklog rules -> context-manifest.json -> validate-agent-context.mjs
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Existing validator baseline | Pre-edit validator exited 1; DB Admin pages/source, create_dd_screen skill registration, DB Admin links, and source drift already fail. | `BASELINE_INVALID` | Compare final errors against the captured pre-edit output; do not expand into unrelated scope repairs. |
| Prior chat/milestone policy in historical logs | User-approved plan preserves historical worklogs unchanged. | `HISTORICAL_ONLY` | New active instructions and template supersede the old policy. |

## CHANGES

- Files changed: `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/context-manifest.json`, `.agents/project/INDEX.md`, `.agents/project/agent-control.md`, `.agents/project/workflows.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`, `.agents/target.md`, `apps/study-client/docs/STUDY2WORK_AGENT_CONTROL_PROMPT.md`, `scripts/validate-agent-context.mjs`, and this worklog.
- CONTEXT_UPDATES: Replaced live chat/event/milestone requirements with active target tracking; registered the three-column target table in schema v4; made validator enforce exact header, three cells, sequential STT, unique names, integer active progress 0–99, and no completed rows.
- Context pages changed: root/global agent guidance, context map, project index, workflows, worklog contract/template, and deprecated Study2Work prompt.
- Assumptions: Chat silence applies to automatic agent status; system/developer/tool requirements still take precedence.
- Existing workspace changes preserved: `.agents/context-manifest.json` already had unrelated Study Guest/Student/Admin source path edits; `.agents/server-study/*`, `.agents/web-work/*`, two 2026-11-17 worklogs, and untracked worklog content/directories were already present. `.agents/target.md` was an empty untracked file. No pre-existing server/web context or historical worklog content was overwritten.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`; three selected worklogs read; no shortage. | `VERIFIED` |
| `node scripts/validate-agent-context.mjs` (pre-edit) | Exit 1; 1,784 output lines, captured in `/tmp/study2work-agent-context-baseline.txt`. | `BASELINE_INVALID` |
| Manifest JSON parse | Valid after registry edits. | `VERIFIED_STATIC` |
| `node scripts/validate-agent-context.mjs` (final) | Exit 1; 81 unique findings, 0 introduced, 0 resolved versus the captured pre-edit baseline. Target registry/table checks pass as no target-specific finding was emitted. | `BASELINE_INVALID` |
| `git diff --check` (task paths) | No whitespace findings in task-owned paths. | `VERIFIED` |

## HANDOFF

- Remaining blockers: 81 pre-existing context validation findings remain outside this task's scope.
- Next owner/action: no further action for this target; begin any future task with a new target at 0%.
