# T027 — SH-05 safe error presentation slice

Date: 2026-11-17  
Status: `ACTIVE`  
Primary task type: `coding`  
Secondary task types: `docs`, `test`  
Project scopes: `web-work`, `server-study`  
Cross-scope dependency: SH-05 maps the Study Server API #04 error envelope into a bounded Study Web presentation state.

## Objective continuity

Continue the active broad objective recorded by the earlier Study Server / Study Web worklogs: organize APIs by role, implement the 83 Study Client screens, run source-backed API tests while coding, use the current DD/diagram/contracts, and deliver correct UI/API behavior. This continuation is one partial screen slice; it does not narrow or complete that objective. Overall progress remains `20% ACTIVE` until the broad deliverables materially advance.

## PRIOR_WORKLOG_REVIEW

- [T011](implement-study-screens-apis-T011.md): preserve API/UI/DB contract limits and do not count a bounded screen slice as completion of the 83-screen objective.
- [T012](implement-study-screens-apis-T012.md): the broad objective remains active; proceed with a useful bounded implementation while retaining its full scope.
- [T013](implement-study-screens-apis-T013.md): source-supported data-access/presentation code can be implemented while dependent screen actions remain gated.
- Selector: `node scripts/select-worklogs.mjs --type coding --limit 3` returned READY and selected exactly T011, T012, and T013; all three were read in full. No shortage.

## Classification and milestones

```text
primary_task_type: coding
secondary_task_types: docs, test
project_scopes: web-work, server-study
cross_scope_dependencies: API #04 error envelope -> SH-05 normalized presentation state
```

| Milestone | Weight | Completion criteria | Status |
|---|---:|---|---|
| M0 — inspect source and record implementation plan | 10% | Read selected worklogs, current SH-05 DD/Stitch, API #04 source/tests, Study Web HTTP envelope/service, routes, workflow; record baseline and bounded plan. | DONE — cumulative 10% |
| M1 — implement independent SH-05 presentation slice | 65% | Add exactly four screen subfolders; normalize only source-backed 401/403 envelopes; render safe message/real trace only; implement accessible trace copy. Do not add route, API request, refresh, or navigation. | DONE — cumulative 75% |
| M2 — verify and synchronize progress | 25% | Run focused frontend screen tests/build and API #04 tests; record runtime limitation, update this log and `docs/tasks/process.md`, compare context-validator output with baseline. | DONE — cumulative 100% |

Progress at work start: `0%` for T027; overall objective `20% ACTIVE`. After M0: `10%`. After M1: `75%`. After verification: `100% DONE_WITH_LIMITATION`. Overall objective remains `20% ACTIVE`.

## Source evidence

### Expected behavior

- SH-05 DD permits 401 vs 403 state mapping from the response status and known `businessCode`, uses only safe envelope `message` and a real `traceId`, and requires accessible trace-copy feedback.
- A 401 must not be labeled “session expired”: API #04 uses the same `401 DESIGN_AUTHENTICATION_REQUIRED` for invalid authentication and missing profile.
- A 403 must not trigger refresh. 5xx/network/service errors are outside this presentation slice.
- Prototype state selectors, synthetic diagnostics/timestamps/trace IDs, policy copy, login/safe-return actions, and the refresh timer are not production behavior.

### Current behavior

- `apps/study-server/app/modules/student/api_04_users_me/view.py` returns 401 `DESIGN_AUTHENTICATION_REQUIRED` for rejected auth and missing profile, 403 role denial comes from the current-user auth guard, and internal failures map to 500.
- API #04 envelope fields are `success`, `businessCode`, `message`, `data`, `meta`, and `traceId`; the response also uses `X-Trace-Id`.
- `StudyApiService` forwards `HttpClient` responses/errors without a SH-05 mapper. `/forbidden` and an error-context handoff are absent. The Admin session service is ADMIN-only and is not reused.
- SH-05 is currently `DD BLOCKED / IMPLEMENTATION BLOCKED / RUNTIME NOT VERIFIED`; the source Stitch screen is a prototype with synthetic content. User/worktree edits to its DD, plan, and web scope context are preserved and not overwritten.

## Implementation plan (written before app code)

- Screen package: `apps/study-client/src/app/features/shared/SH05/` with exactly `data-access/`, `models/`, `pages/`, `ui/`.
- `data-access/`: a pure mapper from Angular `HttpErrorResponse` to SH-05 presentation state; it performs no HTTP request and accepts only matching 401/`DESIGN_AUTHENTICATION_REQUIRED` or 403/`DESIGN_ACCESS_DENIED` envelopes.
- `models/`: a discriminated 401/403 state carrying only status, safe server message, optional real trace ID, and a trace-source conflict flag. Ignore `data` and all unrecognized fields. If body/header trace IDs conflict, omit the trace instead of choosing.
- `pages/`: standalone `SH05Page` receives an error context from a future host and presents only HTTP status and escaped safe message. It is intentionally not routed until the error-context, production-copy, recovery, and safe-return gates are resolved.
- `ui/`: screen-local trace card with a 44px-or-larger copy control, success/failure live feedback, and selectable trace text. No mock controls or synthetic data.
- Layout: centered, responsive single card using existing Study design tokens; no user-facing route metadata, role diagnostics, raw JSON, or recovery links.
- API/DB: no request, mutation, token handling, refresh, or profile read. Do not change Study Server source.
- Tests: mapper tests for valid 401/403, mismatch/unknown status, ignored payload fields, and trace ID conflict; component tests for presentation/copy feedback. Run API #04 tests because this UI slice maps that exact contract, then Study Web focused tests and build.
- Demo: no route/browser demo is safe because `/forbidden` and error-context transport are unresolved; report runtime as not verified. Do not add a temporary route or fixture.
- Cleanup: no server, DB, or browser fixture/process will be started for this slice.

## Pre-existing worktree changes

At T027 start, `.agents/web-work/study/AGENTS.md`, seven SH-05 DD files, `SH-05.md`, and `SH-05_PLAN.md` were already modified; `docs/tasks/process.md`, the T026 worklog, and `shared.route.ts` were already untracked. These are user/worktree state. T027 does not reset, stage, or overwrite them; it only appends its own process/worklog records and creates new SH05 app files.

## Verification and limitations

- Validator baseline before context/worklog edits: exit 1, output SHA-256 `7496126958d348bb35ec8a7df9ca7228326ba4735b79536b28119e6d26afe9e0` (same as prior T024–T026 baseline; repo-wide findings pre-exist).
- M1 implementation: four required direct folders exist. The normalizer accepts only API #04's exact 401/403 status/business-code pairs, ignores unapproved payload fields, and omits conflicting trace IDs. The page is input-driven and not routed; the UI only shows status, safe message, and an available real trace ID with accessible copy feedback.
- Focused Study Web tests after formatting: `3 files / 9 tests passed` using `npm test -- --include 'src/app/features/shared/SH05/**/*.spec.ts'`.
- Study Server API #04 tests: `17 passed`; one existing Starlette/httpx deprecation warning.
- Study Web production build: passed. It reports the existing CSS budget warnings in `student-layout.css`, `student-static-screen.css`, and `st22-page.css`; SH05 adds no budget warning.
- Prettier check: passed. `git diff --check`: passed.
- Runtime/browser demo: not run because SH-05 still has no approved route or error-context handoff; the page remains input-driven and unrouted. Runtime remains `NOT VERIFIED`.
- Final context-validator result: exit 1 `AGENT_CONTEXT_INVALID`, but output is byte-identical to the pre-edit baseline; SHA-256 `7496126958d348bb35ec8a7df9ca7228326ba4735b79536b28119e6d26afe9e0`. No new T027 finding.
- T027 status: `DONE_WITH_LIMITATION`; SH-05 remains `DD BLOCKED`, implementation is partial and unrouted, runtime is not verified. Broad objective remains `20% ACTIVE`.
- Screen status after this bounded slice must remain `DD BLOCKED`; `IMPLEMENTATION PARTIAL` at most; `RUNTIME NOT VERIFIED`.
- Overall objective progress: `20% ACTIVE` unless evidence from broader deliverables supports a change; a partial component does not complete a screen or the 83-screen deliverable.

