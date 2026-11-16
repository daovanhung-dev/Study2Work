---
task_id: "2026-11-13-move-study-api-constants"
date: "2026-11-13"
primary_task_type: "coding"
secondary_task_types: []
project_scopes: ["web-work (Study Web)"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Move Study API registry to `core/constant/api.constants.ts`

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `PATH=/home/daovanhung/.local/opt/node-v22.23.4/bin:$PATH node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 99 exact-type worklogs available; 3 selected and read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-13/study-api-registry.md`
    - carry_forward: The current typed registry contains catalog APIs #1–#103 and source-only R-X01; keep methods, paths, statuses and transport behavior unchanged during relocation.
  - path: `.agents/worklog/2026-11-12/ad01-screen-coding.md`
    - carry_forward: Preserve existing unrelated worktree changes; the context validator has repository-wide baseline findings.
  - path: `.agents/worklog/2026-11-12/ad02-ui-only.md`
    - carry_forward: Study Web has no feature API caller; keep this task limited to shared registry file organization and references.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Create `apps/study-client/src/app/core/constant/api.constants.ts` and move the existing Study API registry there without changing its 103 catalog descriptors, R-X01 descriptor, or behavior. Remove the old `apps/study-client/src/app/core/constants.ts` location and update all active imports and context references.
- Study FE scope: `screens=none; APIs=#1–#103 plus R-X01 (registry relocation only)`.
- Canonical contract: Current registry contents and `StudyApiService` contract are preserved exactly; `list_endpoint.md` contains 103 catalog IDs. This task does not change API data or runtime behavior.

## MILESTONES

Progress started at 0%. Context/source mapping and worklog preflight reached 20%, the unchanged move and reference updates reached 65%, and final verification reached 100%.

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 20% | 20% | Read three exact-type worklogs, Study Web scope/layer rules, both catalogs and architecture guide; inventory current file and references | DONE |
| 45% | 65% | Move the registry unchanged to `core/constant/api.constants.ts`; update service/spec imports, Study Web docs, architecture guide and required source path | DONE |
| 35% | 100% | Verify build, diff and context validator; preserve and report any unrelated baseline findings | DONE |

## CURRENT_BEHAVIOR

- Source/config at task start: `apps/study-client/src/app/core/constants.ts` contained `STUDY_API_BASE_PATH`, descriptor types and 104 entries. The service/spec imported it as `../constants`; Study Web AGENTS/INDEX and `.agents/context-manifest.json` referred to the old path, and `gui/architech.md` did not list a registry folder. Current source is at `apps/study-client/src/app/core/constant/api.constants.ts`, with active imports and context references updated.
- Runnable tests: Vitest is configured. The preceding registry task recorded 17/17 tests passing; this task will use a production build for the import-path change. No test suite is requested for this file relocation.
- Runtime wiring: `StudyApiService` consumes the descriptors; no feature caller exists. API paths and statuses remain unchanged.

## SOURCE_TRACE

```text
StudyApiService + service spec -> ../constant/api.constants -> core/constant/api.constants.ts
Study Web docs + context manifest -> registered source path
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Requested file location | Current source and context use `core/constants.ts`; user requests `core/constant/api.constants.ts` | `EXPECTED_BEHAVIOR` update | Move file and update active references; leave historical worklog as an accurate record of its task-time path. |
| API contract | No API method/path/status changes requested | `UNCHANGED` | Preserve all descriptor values. |

## CHANGES

- Files changed: moved registry unchanged to `apps/study-client/src/app/core/constant/api.constants.ts`; updated `StudyApiService` and spec imports, Study Web AGENTS/INDEX, architecture tree/data flow, and `.agents/context-manifest.json`.
- CONTEXT_UPDATES: Study Web registry path and core directory responsibilities now point to `constant/api.constants.ts`.
- Context pages changed: `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `apps/study-client/gui/architech.md`, `.agents/context-manifest.json`.
- Assumptions: Use the explicitly requested singular directory name `constant`; no barrel file or duplicate registry will be added.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Worklog selector | `READY`; 3/99 exact-type `coding` logs selected and read; no shortage | VERIFIED_PREFLIGHT |
| Study FE catalogs | 83 screens; 103 API IDs; screen scope none and API catalog unchanged | VERIFIED_STATIC |
| Current source/reference inventory | Registry has 104 entries; service/spec/context references point to old path | VERIFIED_STATIC |
| `node scripts/validate-agent-context.mjs` (pre-change baseline) | Exit 1, `AGENT_CONTEXT_INVALID`, 952 output lines; 2 DB Admin, 33 orphan skill resources and 7 scope source-drift headers | BASELINE_INVALID |
| `PATH=/home/daovanhung/.local/opt/node-v22.23.4/bin:$PATH npm run build` in `apps/study-client` | Exit 0; Angular production bundle generated successfully | VERIFIED |
| `git diff --check` | No whitespace errors | VERIFIED |
| Active path reference search | No active references to `core/constants.ts` or `../constants`; historical worklogs intentionally retain task-time paths | VERIFIED |
| `.agents/context-manifest.json` | Valid JSON; includes new registry and service spec paths; old registry path absent | VERIFIED |
| `node scripts/validate-agent-context.mjs` | Exit 1, `AGENT_CONTEXT_INVALID`, 952 output lines, same total as pre-change baseline; no diagnostic mentions new or old registry path | BASELINE_INVALID_NO_REGRESSION |
| Test suite | Not run for this relocation request | NOT_RUN |

## HANDOFF

- Remaining blockers: No blocker for the file move. Repository-wide context validation still has the same baseline findings recorded before implementation; deployment behavior is outside this task.
- Next owner/action: None.
