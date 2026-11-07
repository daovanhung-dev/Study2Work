---
task_id: "2026-11-06-design-study-screen-sh04"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-04 consumes SH-03 API #01 handoff and invokes Study API #02; email verification provider and account activation policy"]
status: "VERIFIED"
---

# Worklog: Rà soát Detailed Design màn hình Study SH-04

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selected 3 of 156 docs worklogs; all selected logs read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh01.md`
    - carry_forward: Keep DD, implementation and runtime statuses separate; map every marker to a stable element ID; verify all event metadata and local links.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh02.md`
    - carry_forward: Preserve source assets; record route/client absence separately from API source; surface contract discrepancies rather than reconciling by assumption.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh03.md`
    - carry_forward: SH-03 returns `data.id`/`data.email`; SH-04 owns API #02. Default provider is a stub, account activation and live schema are unresolved, and API #01 does not call #02.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete SH-04 only in this session; review and update its plan before editing its DD or image artifacts; preserve source PNG/HTML; verify annotated markers map one-to-one to stable DD element IDs; trace all events and API #02 behavior to current contracts/source/tests; update tracker and this worklog.
- Canonical contract: Study `list_screen.md` SH-04, AC-01/F01, API #02 catalog and source, SH-03 handoff; `.agents/web-study/design.md` is the UI target, not runtime evidence.

## CURRENT_BEHAVIOR

- Current folder contains `screen.png`, `code.html`, `screen_annotated.png`, `SH-04_markers.json`, `SH-04_PLAN.md`, and tracked `SH-04.md`. `screen.png` is 1600×1280; annotated PNG is 3200×2560. Source hashes match the plan: PNG `07f88cb51f0c31a990b5f553a828b4f1cba3b3d7e648286f70e3604528aed396`; HTML `a524d7d9d5b5640273d9d84900f9ba6a68df8a434d1f0ff189d989e4a2575684`.
- `apps/study-client` has `docs`, generated `dist`, and `node_modules`, but no `src`, router or `package.json`; `.agents/web-work/study/` is absent. Do not use `dist` or installed packages as source/runtime evidence.
- HTML mock changes local DOM/JSON for state controls and copies an example cURL; it does not call API #02. The cURL URL is missing `/api/v1` and body omits `user_id`; mock payload includes fields not in API response.
- API #02 route is registered at `POST /api/v1/auth/verify-email/send`, public, body `user_id:int`/`email:str`, HTTP 202. Validator rejects non-raw-integer `user_id`, normalizes/validates email, and does not enforce int64 bounds or positive ID. View calls injected provider without DB; provider failure maps to safe 500; success maps provider `status` and optional `reason` to `DESIGN_OPERATION_ACCEPTED`.
- Default `StubVerificationEmailProvider` ignores all inputs and returns `status="accepted"`; it neither sends email nor creates a token. No queue, retry worker, ownership check, database lookup, OTP/link confirmation endpoint or delivery callback is present in this flow.
- F01 places API #02 at SH-04 after API #01 success; current API #01 commits the user and logs `verification_dispatch_pending`, but does not call #02. API #02 DD remains Draft with open dispatch owner/gate, acceptance/retry, provider/token lifecycle, identity binding, abuse control, status/reason, email normalization and int64-range questions.

## SOURCE_TRACE

- Expected flow: `apps/study-client/docs/list_screen.md` SH-04 row and F01 → API #02 (`docs/lists/list_api.md`, AC-01 diagram) → current FastAPI route → API #02 validator/view → injected `VerificationEmailProvider` → success/error envelope and focused test source. AC-01 depicts provider send/log/retry, while current source only invokes the provider synchronously and default provider is a stub.
- Cross-screen: SH-03 API #01 source commits account and returns `data.id`/`data.email`, then logs deferred dispatch. SH-04 needs these as `user_id`/`email`; there is no Study Web route state or approved handoff storage/transport source.
- Tests read: `apps/study-server/tests/modules/guest/api_02_auth_verify_email_send/test_verify_email_send.py` covers public dispatch, no DB dependency, 202 accepted, 422 validation, and safe 500 provider failure. Tests were not run.
- Design/status: `.agents/web-study/design.md` is intended Study UI target only; `.agents/context-manifest.json` and `.agents/skills/INDEX.md` show Web UI-only DD has no canonical skill. Missing `.agents/web-work/study/` subcontext is `NOT_FOUND`.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| SH-04 design controls | 12 markers are visually clear and avoid key content; controls/JSON/cURL in HTML are mock-only. | DISCREPANCY | Preserve original/annotation; map mock affordances as QA-only, not product events. |
| Study Web route/client | No `src`, router, package manifest or Study child context; only docs and generated/install artifacts found. | NOT_FOUND / UNWIRED | Runtime not verified; implementation blocked. |
| API #02 source vs AC-01 | AC depicts provider send/log/retry; current API calls provider synchronously, default provider only returns accepted, no queue/retry. | DISCREPANCY | Do not claim delivery, queue, retry or verification. |
| Dispatch owner/trigger | F01 says #02 occurs at SH-04, but API DD Q-02-01 leaves dispatch owner/feature gate open and UI trigger (auto entry vs explicit action) is not approved. | DD BLOCKED | Do not choose trigger by inference; obtain owner decision before implementation. |
| SH-03 handoff channel | #01 returns `data.id`/`data.email`; no client route/state source or approved transport found. | IMPLEMENTATION BLOCKED | Do not place identifiers in URL or select persistence by assumption. |
| Provider/verification lifecycle | Stub has no delivery/token/confirm endpoint; #03 active-account policy is separately unresolved. | IMPLEMENTATION BLOCKED | Do not show sent/verified or claim end-to-end verification. |

## CHANGES

- Files changed: `SH-04_PLAN.md` reviewed first and marked artifact update complete; `SH-04_markers.json` now has stable element IDs and coordinate provenance; `SH-04.md` has separate statuses, 12 element contracts, eight event specifications and source links; global `dd_screens/PLAN.md` updated with status and SH-05 handoff; this worklog completed.
- Original `screen.png`, `code.html` and existing `screen_annotated.png` were retained. The source image and annotation were visually reviewed; all 12 markers remain visible and clear.
- CONTEXT_UPDATES: None anticipated; no runtime contract or schema change is in scope.
- Context pages changed: None anticipated.
- Assumptions: None. Dispatch trigger, handoff transport and provider behavior are recorded as unresolved decisions rather than selected defaults.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` and selected-file review | Selected and read 3 exact-type worklogs of 156; no shortage. | VERIFIED |
| Scoped source/API review | Current route, validator, view, provider, tests, API DD open questions, SH-03 source handoff, AC-01/F01 and Study Web design target read. | VERIFIED (source read only) |
| SH-04 static artifact audit | PNG dimensions 1600×1280 and 3200×2560; PNG/HTML source hashes match plan; 12 ordered markers map one-to-one to `SH04-EL-01..12`; 8 ordered events have trigger/element, prerequisites, input, processing and output; all local DD/plan links resolve; tracker status and SH-05 handoff match. | VERIFIED |
| `git diff --check` (task files) | No whitespace errors. | VERIFIED |
| Tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining blockers: SH-04 DD BLOCKED by unresolved dispatch owner/trigger and SH-03 handoff transport; implementation also blocked by absent Study Web source/runtime and stub-only email provider with no verification endpoint. Account activation policy remains unresolved.
- Final screen status: DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED.
- Next owner/action: SH-05 in a separate session; do not start another Screen ID in this session.
