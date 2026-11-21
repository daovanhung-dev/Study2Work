---
task_id: "2026-11-08-design-study-screen-st01-reaudit"
date: "2026-11-08"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-01 dashboard -> Study APIs #20/#21/#38/#43; student identity/session -> dashboard authorization; ST-01 widgets -> ST-08, ST-20, ST-26 and ST-02; AC-13/18/20 orchestration and permission rules"]
status: "IN_PROGRESS"
---

# Worklog: Re-audit Detailed Design màn hình Study ST-01

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 264 exact-type docs worklogs available; three selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-08/design-study-screen-gs07-reaudit.md`
    - carry_forward: Keep work limited to one Screen ID; inventory is current order authority; preserve original assets and distinguish local source from runtime. The previous checkpoint text named GS-08 as next, but current inventory contains no GS-08 and proceeds to ST-01; use current inventory as authority.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current evidence separate; do not infer routes, metrics, mappings or behavior from mockups; trace current backend contracts and retain UI-only DD blockers.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Preserve original assets; trace caller through server guard/query/response/test source; do not treat fake-session tests or API DD as runtime/live DB proof; preserve Study Web `UNWIRED` and API catalog/source discrepancies.
- additional target handoff reviewed: pending full read of `.agents/worklog/2026-11-07/design-study-screen-st01.md`.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Continue the 83-screen objective with ST-01 only in this session. Recheck the existing plan, source assets, annotated image, marker map and DD against current inventory, AC-13/18/20, API catalog/DD, current Study Server source/test declarations, DB candidates and Study Web guide. Update `ST-01_PLAN.md` before editing DD/markers/annotation/shared tracker; preserve original assets; map all markers to element rows; describe event inputs/process/outputs/errors and widget states; update inventory, shared tracker and worklog; leave next screen to a separate session.
- Inventory row 15: ST-01 “Tổng quan học viên (Page)”, proposed `/student`, APIs #20/#21/#38/#43; student dashboard of courses/progress/achievements/notifications with independent widgets; role STUDENT prerequisite; expected links ST-08/ST-20/ST-26/ST-02; P1.
- Canonical UI target: `.agents/web-study/design.md`; requirement/API/UI-only skill routing must be verified via `.agents/context-manifest.json`; do not infer screen behavior from mockup.

## CURRENT_BEHAVIOR

- Source/API/UI wiring: pending current source trace.

## SOURCE_TRACE

```text
Verified Student identity/role -> ST-01 independent dashboard widgets -> APIs #20/#21/#38/#43 as catalog/source allows -> links to ST-08/ST-20/ST-26/ST-02. Exact guards, queries, response projections, side effects, errors and runtime wiring pending source trace.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API, AC and prototype behavior | Existing tracker flags unresolved API/AC/HTML differences; details pending current source and artifact re-audit. | IN_PROGRESS | No assumptions until evidence is collected. |

## CHANGES

- Files changed: this worklog only so far; an incorrect GS-08 draft was created and removed after inventory confirmed no such Screen ID.
- CONTEXT_UPDATES: none planned.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective, context routers and worklog contract read; exact docs selector READY; GS-07, AD-01 and AD-02 worklogs read in full. | VERIFIED |
| ST-01 source/artifact audit | Pending. | IN_PROGRESS |

## HANDOFF

- Remaining blockers: pending ST-01 source and artifact audit.
- Next owner/action: complete ST-01 only, then identify the next inventory Screen ID for a separate session.
