# Agent worklog contract

Every agent task, including read-only and information-only tasks, creates or
updates a worklog entry under
`.agents/worklog/YYYY-MM-DD/<task-id>.md`. The worklog is an audit trail;
source code, tests and contracts remain the source of truth for behavior.

For chat/tool visibility, every tool call must use the Event protocol in
[`../project/agent-control.md`](../project/agent-control.md): announce the Event
before the call and record its actual result immediately afterward. Keep the
same Task/Step/Action/Event identifiers and verified progress in chat and the
worklog; the worklog's `MILESTONES` weights are the progress source, and
bootstrap discovery is not counted again.

## Milestones and chat receipts

Before deep work, publish the task classification and at least two task-specific
milestones in chat. Each milestone must name its objective/acceptance criterion
and weight; milestone weights must total 100%. Start reported progress at 0%,
and record the plan and each milestone status under `MILESTONES` in the worklog.

After every tool call, post its Event result. Also summarize paths/sources and
findings after each coherent reading batch. Compact formatting may place
multiple Event receipts in one table, but must not omit or delay an Event.
Report cumulative progress based only on verified milestone weights. If
blocked, report achieved progress and blocker; report 100% only when the task
is complete.

## Mandatory preflight

Before deep inspection, source edits, test edits, or documentation authoring:

1. Classify `primary_task_type`, secondary types, scopes and dependencies.
2. Run the non-mutating selector:

   ```text
   node scripts/select-worklogs.mjs --type <primary_task_type> --limit 3
   ```

   Deno compatibility invocation is allowed when Node is unavailable.
3. Read every selected worklog. Selection matches the exact
   `primary_task_type`, ordered by date descending and then path ascending.
4. If fewer than three matching logs exist, read all available logs and record
   the shortage; do not invent or substitute another task type.
5. Record the command, selected paths, useful carry-forward facts and shortage
   in `PRIOR_WORKLOG_REVIEW` of the active worklog.

The selector is a routing aid, not evidence that a file was read. The worklog
entry is the evidence record.

## Required order

1. Classify `primary_task_type`, secondary types, scopes and dependencies.
2. Complete the mandatory preflight and `PRIOR_WORKLOG_REVIEW`.
3. Record `EXPECTED_BEHAVIOR` from the latest requirement and canonical
   contract/approved DD.
4. Record `CURRENT_BEHAVIOR` from current source, runnable tests and config.
5. Trace caller → callee → database/external side effect → response → tests.
6. Record every `DISCREPANCY`, `UNWIRED`, `NOT_FOUND` and
   `DECLARED_NOT_RUNNABLE` result.
7. After changes, record files changed, focused/full verification, context
   pages updated and remaining blockers.

Use `TEMPLATE.md`; do not mark a command `VERIFIED` when it was not run.
Unavailable tools, missing dependencies and absent source are explicit status
values, not implicit passes.
