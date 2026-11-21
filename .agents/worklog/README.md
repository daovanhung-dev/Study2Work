# Agent worklog contract

Every agent task, including read-only and information-only tasks, creates or
updates a worklog entry under
`.agents/worklog/YYYY-MM-DD/<task-id>.md`. The worklog is an audit trail;
source code, tests and contracts remain the source of truth for behavior.

Live target names and progress are kept only in [`.agents/target.md`](../target.md),
which contains the active three-column table. Do not duplicate its current
progress in chat or in a milestone table. Each worklog records evidence for
`TARGET_UPDATES` (initial target, verified progress changes, and completion
evidence). Completed target rows are removed from `target.md` after their
completion evidence is recorded. Historical worklogs remain unchanged.

Every worklog also contains `READ_PLAN` and `LEAF_TARGET_PLAN`. `READ_PLAN` is
the allowlist for file-content reads: each row names the exact path, needed
section/range and task-specific reason before the agent opens or searches that
content. Track each row as `PLANNED`, `READ`, `READ_FROM_CONTEXT`,
`CHECKED_BY_TOOL` or `SKIPPED`. `LEAF_TARGET_PLAN` decomposes the task into the
same independently verifiable operations shown in the active target table.

## Read-set discipline

1. Before opening repository files, declare the fixed router/bootstrap paths
   and required sections from `AGENTS.md` in a temporary read-set. The root
   router itself may be supplied as context; record it as such rather than
   reopening it.
2. Read only those bootstrap sections, then create the active worklog and copy
   the read-set into `READ_PLAN` before any task-specific source inspection.
3. The selector may inspect worklog metadata under `.agents/worklog/` to return
   same-type candidates. Add the exact returned paths to `READ_PLAN` before
   opening their contents. Do not open unselected worklog bodies.
4. After routing through context map/manifest, add each exact scope page,
   contract, source or test path before reading it. Search commands may inspect
   only paths already listed. A filename-only inventory is bounded to the
   declared directory and does not authorize opening the listed file contents.
5. If evidence reveals a new dependency, append its exact path, needed section
   and reason before reading it. Use line ranges or targeted matches; stop when
   the required evidence is sufficient and do not repeat full-file reads.

The selector and validator are predeclared metadata/validation operations in
the root router. Their scoped machine reads do not authorize loading the
underlying worklog/source bodies into the agent's context.

## Mandatory preflight

Before deep inspection, source edits, test edits, or documentation authoring:

1. Classify `primary_task_type`, secondary types, scopes and dependencies.
2. Build the bootstrap read-set and initialize the worklog from
   `TEMPLATE.md`, including `READ_PLAN` and `LEAF_TARGET_PLAN`, before deep
   inspection.
3. Run the non-mutating selector:

   ```text
   node scripts/select-worklogs.mjs --type <primary_task_type> --limit 3
   ```

   Deno compatibility invocation is allowed when Node is unavailable.
4. Add the exact selected paths to `READ_PLAN` before reading their bodies.
   Selection matches exact `primary_task_type`, ordered by date descending and
   then path ascending.
5. Read selected worklog bodies only. If fewer than three matching logs exist,
   read all available matches and record shortage; do not substitute another
   task type.
6. Record command, selected paths, carry-forward facts and shortage in
   `PRIOR_WORKLOG_REVIEW`.

The selector is a routing aid, not evidence that a file was read. The worklog
entry is the evidence record.

## Required order

1. Classify `primary_task_type`, secondary types, scopes and dependencies.
2. Predeclare the bootstrap read-set, initialize `READ_PLAN`, then complete the
   mandatory worklog preflight and `PRIOR_WORKLOG_REVIEW`.
3. Decompose the approved task plan into `LEAF_TARGET_PLAN`; create one active
   target row per independently verifiable operation.
4. Record `EXPECTED_BEHAVIOR` from the latest requirement and canonical
   contract/approved DD.
5. Record `CURRENT_BEHAVIOR` from current source, runnable tests and config.
6. Trace caller → callee → database/external side effect → response → tests.
7. Record every `DISCREPANCY`, `UNWIRED`, `NOT_FOUND` and
   `DECLARED_NOT_RUNNABLE` result.
8. Update `.agents/target.md` when verified progress changes; record the reason
   and evidence in `TARGET_UPDATES`.
9. After changes, record files changed, focused/full verification, context
   pages updated and remaining blockers.

Use `TEMPLATE.md`; do not mark a command `VERIFIED` when it was not run.
Unavailable tools, missing dependencies and absent source are explicit status
values, not implicit passes.
