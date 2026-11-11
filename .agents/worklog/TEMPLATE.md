---
task_id: "YYYY-MM-DD-short-name"
date: "YYYY-MM-DD"
primary_task_type: "coding | fix | docs | test | review"
secondary_task_types: []
project_scopes: []
cross_scope_dependencies: []
status: "PLANNED | IN_PROGRESS | VERIFIED | PARTIAL | BLOCKED"
---

# Worklog: <task title>

## PRIOR_WORKLOG_REVIEW

- primary_task_type: <fill>
- selector_command: <fill>
- prior_worklogs_reviewed:
  - path: <fill>
    - carry_forward: <fill>
- shortage: `none | <number> missing`

## EXPECTED_BEHAVIOR

- Requirement:
- Canonical contract/approved DD:

## MILESTONES

Define at least two task-specific milestones with objective/acceptance
criteria. Weights must total 100%; cumulative progress is the sum of completed
weights. Start at 0% and report progress only when a milestone is achieved.
Use `PENDING`, `DONE`, or `BLOCKED` for milestone status.

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| `<weight>%` | `<cumulative>%` | `<milestone objective>` | `PENDING` |
| `<weight>%` | `100%` | `<final acceptance>` | `PENDING` |

## CURRENT_BEHAVIOR

- Source/config:
- Runnable tests:
- Runtime wiring:

## SOURCE_TRACE

```text
caller -> callee -> DB/external side effect -> response -> tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| | | | |

## CHANGES

- Files changed:
- CONTEXT_UPDATES:
- Context pages changed:
- Assumptions:

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| | | |

## HANDOFF

- Remaining blockers:
- Next owner/action:
