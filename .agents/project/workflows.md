# Repository workflow registry

All workflows begin with the root router, global registry, context map, task
classification, and worklog preflight. The selected same-type worklogs must be
read before deep source inspection. The active worklog is updated before source
edits, after source tracing, and after verification.

## Common flow

```text
load `.agents/context-map.md`
-> classify task
-> select/read up to 3 nearest worklogs with the same primary_task_type
-> load exact scope/subcontext
-> load skill/contract registry entries required by the task
-> separate EXPECTED_BEHAVIOR from CURRENT_BEHAVIOR
-> trace caller -> callee -> DB/external side effect -> response -> tests
-> make the smallest scoped change
-> run focused verification and status every blocked command
-> update context and worklog
```

## Task routing

| Workflow | Trigger | Required behavior | Verification |
|---|---|---|---|
| Coding | `coding` | requirement/contract → existing pattern → implementation → tests | scope checks + context validator |
| Fix | `fix`, bug, regression | reproduce → trace → root cause → smallest fix → regression test | reproduction/regression test |
| Test | test/verification request | inspect requirement, implementation, error paths and test convention | focused test then scope test |
| Docs/DD | Web/API DD/documentation | load `createDD-markdown`; preserve API template and mark source gaps | contract and DD validation |
| Docs/DD Mobile | Mobile module DD/documentation | load `create-dd-from-bd-mobile`; follow BD evidence, module template and review gates | mobile DD validator + context validation |
| Cross-scope contract | shared API/event/envelope | identify producer/consumer and status before changing either side | `contracts:validate` + context validator |
| Worklog | every task | run `scripts/select-worklogs.mjs`, read selected same-type logs, record `PRIOR_WORKLOG_REVIEW`, evidence, decisions, changes and verification | required-field checklist + context validator |

## Tool status in the current repository

- `scripts/validate-agent-context.mjs`: active validator; Node is canonical,
  Deno compatibility invocation is accepted when Node is unavailable.
- `scripts/validate-contracts.mjs`: runnable and currently passing.
- `scripts/validate-bd.mjs`: `DECLARED_NOT_RUNNABLE` because `docs/BD/` is
  absent; do not recreate that source from history.
- `scripts/generate_v1_pilot_dd.py`: `DECLARED_NOT_RUNNABLE` because it needs
  `docs/BD/` and currently references the absent `.agent/` template path.
- `.agents/skills/create-dd-mobile/scripts/validate_dd_pack.py`:
  source-backed Mobile module DD validator; use it for Mobile DD packs,
  templates and examples.

Missing tools or missing source must be reported with an explicit status; a
file-presence check is not a runtime verification.
