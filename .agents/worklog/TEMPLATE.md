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

## READ_PLAN

Declare each file path and the exact section/range needed before opening or
searching its content. Add newly discovered paths before reading them.
Use status `PLANNED`, `READ`, `READ_FROM_CONTEXT`, `CHECKED_BY_TOOL` or `SKIPPED`.

| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `<path>` | `<section, lines, or bounded query>` | `<why this evidence is needed>` | `PLANNED` |

## LEAF_TARGET_PLAN

List the independently verifiable operations displayed as active rows in
`.agents/target.md`. Split multi-action targets; do not add parent/epic rows.

| Target | Single operation | Acceptance evidence |
|---|---|---|
| `<target name>` | `<one action and its result>` | `<observable completion evidence>` |

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

## TARGET_UPDATES

Record each target creation, verified progress change, blocker that affects
progress, and completion evidence. `.agents/target.md` is the sole live progress
source; do not duplicate its current value in a milestone table.

| Target | From → to | Evidence / reason |
|---|---:|---|
| `<target name>` | `0% → 0%` | `<initial target and acceptance basis>` |

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
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| | | |

## HANDOFF

- Remaining blockers:
- Next owner/action:
