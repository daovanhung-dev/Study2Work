# Status Model

Use these exact status values in API DDs, checklists, worklogs, and retrospectives. Do not add new status values unless this file is updated.

## DD Status

| Status | Meaning |
|---|---|
| `NOT_STARTED` | The DD has not been created or analysis has not started. |
| `DRAFT` | The DD is being written and is not ready for official coding. |
| `IN_REVIEW` | Waiting for BA/PO/Tech Lead/QA review. |
| `APPROVED` | Approved for coding within the DD scope. |
| `BLOCKED` | Cannot finish because a decision, dependency, or required information is missing. |
| `SUPERSEDED` | Replaced by a newer DD, ADR, or decision. |

## Coding Status

| Status | Meaning |
|---|---|
| `NOT_STARTED` | Coding has not started. |
| `IN_PROGRESS` | Implementation is in progress. |
| `READY_FOR_TEST` | Code is ready for verification, but no passing evidence exists yet. |
| `TEST_FAILED` | A test/check failed or acceptance is not met. |
| `VERIFIED` | Verification evidence exists for the scoped behavior. |
| `DONE` | Coding, verification, docs, checklist, and worklog are complete for the task scope. |
| `BLOCKED` | Work cannot continue because a decision, dependency, or environment is missing. |

## Bug Status

| Status | Meaning |
|---|---|
| `NONE` | No bug recorded for the item. |
| `OPEN` | A bug is recorded but not fully investigated. |
| `INVESTIGATING` | Root cause analysis is in progress. |
| `FIXED` | The bug was fixed but not fully verified. |
| `VERIFIED` | Evidence confirms the bug no longer reproduces. |
| `WONT_FIX` | Not fixed by a traceable decision. |

## Test Status

Checklist test status uses the coding status values:

| Status | Rule |
|---|---|
| `NOT_STARTED` | No test/check has run. |
| `IN_PROGRESS` | Verification is in progress. |
| `READY_FOR_TEST` | Ready to verify but not run yet. |
| `TEST_FAILED` | Test/check failed or acceptance is unmet. |
| `VERIFIED` | Evidence exists: command output, screenshot, report, or review confirmation. |
| `BLOCKED` | Cannot run due to missing environment, dependency, or decision. |

Do not use `VERIFIED` or `DONE` without concrete evidence in a checklist or worklog.

