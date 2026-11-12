# Repository workflow registry

All workflows begin with the root router, global registry, Agent Control,
context map, task classification, and worklog preflight. Every task must load and follow
[`agent-control.md`](agent-control.md); announce each tool call as an Event
before it runs and record its actual result immediately afterward. The selected
same-type worklogs must be read before deep source inspection. The active
worklog is updated before source edits, after source tracing, and after
verification.

## Chat progress and read/action updates

For every task, including read-only tasks, publish the task classification and
at least two task-specific milestones before deep work. Each milestone has an
objective/acceptance criterion and a percentage weight; weights total 100%.
Record the milestones in the active worklog and start reported progress at 0%.

Every tool call has a Task → Step → Action → Event ID and a before/after
receipt. Each receipt names operation, target, purpose, actual result, evidence,
and file effects when relevant. Compact tables may group presentation, but must
retain each Event separately. Summarize paths and findings after coherent read
batches as well. When a milestone is verified, report cumulative progress using
the same weights recorded in the worklog. If blocked, report achieved progress
and blocker; reserve 100% for completed tasks. Bootstrap discovery is not
counted again in execution progress.

## Common flow

```text
publish Bootstrap Plan and announce the first Event before tool calls
-> load `.agents/AGENTS.md` and `.agents/project/agent-control.md`
-> load `.agents/context-map.md` before final scope/subcontext selection
-> classify task and finalize project scope
-> publish task-specific milestones and 0% starting progress in chat
-> select/read up to 3 nearest worklogs with the same primary_task_type
-> report each coherent reading batch with paths and findings
-> load exact scope/subcontext
-> load skill/contract registry entries required by the task
-> separate EXPECTED_BEHAVIOR from CURRENT_BEHAVIOR
-> trace caller -> callee -> DB/external side effect -> response -> tests
-> make the smallest scoped change
-> report meaningful action batches and completed-milestone percentages
-> run focused verification and status every blocked command
-> update context and worklog
```

## Task routing

| Workflow | Trigger | Required behavior | Verification |
|---|---|---|---|
| Agent Control | every task and every tool call | load the global control page; use Task/Step/Action/Event IDs, pre-call START and post-call END, verified progress and compact event receipts | event/plan consistency + context validator |
| Coding | `coding` | requirement/contract → existing pattern → implementation → tests | scope checks + context validator |
| Study Web screen coding | implement/fix/test/demo one `apps/study-client` screen | load the registered `study-web-screen-coding` workflow; read full DD/images, plan, implement in the Study Web structure, then test/demo and clean isolated fixtures | focused Angular tests + local demo + fixture cleanup + context validator |
| Fix | `fix`, bug, regression | reproduce → trace → root cause → smallest fix → regression test | reproduction/regression test |
| Test | test/verification request | inspect requirement, implementation, error paths and test convention | focused test then scope test |
| Code review | explicit review request | load `code-review`; inspect the requested diff or named path/module against scope rules, contracts, source, call sites and test source; report only evidenced/actionable findings without editing or executing tests | read-only scope/evidence audit + worklog |
| Docs/DD | Web/API DD/documentation | load `createDD-markdown`; preserve API template and mark source gaps; for `server-study`, follow its [Markdown-only deliverable rule](../server-study/workflows/README.md) | contract and DD validation |
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
