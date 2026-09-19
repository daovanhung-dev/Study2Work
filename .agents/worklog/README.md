# Agent worklog contract

Every coding, fix, docs, or test task creates or updates a worklog entry under
`docs/devs/worklogs/YYYY-MM-DD/<task-id>.md`. The worklog is an audit trail;
source code, tests and contracts remain the source of truth for behavior.

## Required order

1. Classify `primary_task_type`, secondary types, scopes and dependencies.
2. Record `EXPECTED_BEHAVIOR` from the latest requirement and canonical
   contract/approved DD.
3. Record `CURRENT_BEHAVIOR` from current source, runnable tests and config.
4. Trace caller → callee → database/external side effect → response → tests.
5. Record every `DISCREPANCY`, `UNWIRED`, `NOT_FOUND` and
   `DECLARED_NOT_RUNNABLE` result.
6. After changes, record files changed, focused/full verification, context
   pages updated and remaining blockers.

Use `TEMPLATE.md`; do not mark a command `VERIFIED` when it was not run.
Unavailable tools, missing dependencies and absent source are explicit status
values, not implicit passes.
