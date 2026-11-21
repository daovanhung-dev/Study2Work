# Repository workflow registry

Every workflow starts from the supplied root router: classify the task, declare
the bootstrap read-set, then load the global registry and context map before
selecting a scope. Load the context manifest and
[`agent-control.md`](agent-control.md) from that declared set. Before opening
any other file content, add its path, required section/range and reason to
`READ_PLAN`. Decompose the task into independently verifiable leaf operations
and keep those active rows in `.agents/target.md`. Record sources, decisions,
changes, verification and target updates in the worklog. Do not emit unsolicited
chat content or duplicate milestone progress.

## Common flow

```text
classify task from user request and supplied root router
-> declare bootstrap read-set before repository file reads
-> load `.agents/AGENTS.md`
-> load `.agents/context-map.md` before final scope selection
-> load context manifest and Agent Control sections from the declared read-set
-> initialize worklog READ_PLAN and LEAF_TARGET_PLAN; finalize project scope
-> select same-type worklogs; declare returned paths before opening their bodies
-> record PRIOR_WORKLOG_REVIEW and decompose plan into LEAF_TARGET_PLAN
-> create/update one active target row per independently verifiable operation
-> load exact scope/subcontext and only required skill/contract/source paths
-> separate EXPECTED_BEHAVIOR from CURRENT_BEHAVIOR
-> trace caller -> callee -> DB/external side effect -> response -> tests
-> make the smallest scoped change
-> run focused verification and status every blocked command
-> update target only when verified progress changes
-> record evidence and target changes in the worklog
```

## Context validator baseline

When a task changes `.agents` pages, the context manifest, or registered
workflow/skill/contract wiring, establish a validator baseline before the first
context edit and run the validator again after all context and worklog edits:

```bash
node scripts/validate-agent-context.mjs
```

Capture the exit status and findings for both runs, then compare findings by
their identity and target rather than by the total count alone. Record which
findings were already present, which were resolved, and which were introduced
by the task. Fix findings caused by the task. If unchanged baseline findings
remain, report `BASELINE_INVALID` with their categories and affected scope; do
not call that a pass and do not expand into unrelated scopes unless the user
requested that work. Run the final comparison after updating the active
worklog, since it is also part of agent context.

## Task routing

| Workflow | Trigger | Required behavior | Verification |
|---|---|---|---|
| Agent Control | every task | one active target per leaf operation; predeclare file reads; keep evidence in worklog; suppress unsolicited chat | target structure + leaf plan + read plan + context validator |
| Coding | `coding` | requirement/contract → existing pattern → implementation → tests | scope checks + context validator |
| Study Web screen coding | implement/fix/test/demo one `apps/study-client` screen | load the registered `study-web-screen-coding` workflow; read full DD/images, plan, implement in the Study Web structure, then test/demo and clean isolated fixtures | focused Angular tests + local demo + fixture cleanup + context validator |
| Fix | `fix`, bug, regression | reproduce → trace → root cause → smallest fix → regression test | reproduction/regression test |
| Test | test/verification request | inspect requirement, implementation, error paths and test convention | focused test then scope test |
| Code review | explicit review request | load `code-review`; inspect the requested diff or named path/module against scope rules, contracts, source, call sites and test source; report only evidenced/actionable findings without editing or executing tests | read-only scope/evidence audit + worklog |
| Docs/DD | Web/API DD/documentation | load `createDD-markdown`; preserve API template and mark source gaps; for `server-study`, follow its [Markdown-only deliverable rule](../server-study/workflows/README.md) | contract and DD validation |
| Docs/DD Mobile | Mobile module DD/documentation | load `create-dd-from-bd-mobile`; follow BD evidence, module template and review gates | mobile DD validator + context validation |
| Cross-scope contract | shared API/event/envelope | identify producer/consumer and status before changing either side | `contracts:validate` + context validator |
| Worklog | every task | create `READ_PLAN`/`LEAF_TARGET_PLAN`; run selector, declare selected paths before body reads, record `PRIOR_WORKLOG_REVIEW`, evidence and `TARGET_UPDATES` | required-field checklist + declared path order + leaf target evidence + context validator |

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
