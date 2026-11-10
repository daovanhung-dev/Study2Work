---
task_id: "2026-11-07-design-study-screen-sh05-reaudit"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-05 Study Web auth/session recovery ↔ Study API #04 and R-X01; return/navigation to SH-02 or a safe prior route"]
status: "VERIFIED"
---

# Worklog: Re-audit Detailed Design màn hình Study SH-05

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 254; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected behavior separate from current source; preserve original assets; trace authorization, effects, response and tests; keep Study Web `UNWIRED` unless editable route/client source proves otherwise; UI-only DD has no canonical skill.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Do not infer route, filters, data mappings, permissions or behavior from mockups; distinguish API catalog from current route/query/response; fake DB tests do not establish live schema or deployment.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Keep API source status separate from draft contract and screen implementation; inspect current route/auth/error handling; do not infer identity, PII, audit or runtime behavior.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh05.md` (supplemental, screen-specific)
    - carry_forward: Existing SH-05 has an 11-marker annotation; #04 source maps malformed/missing auth and missing profile to the same 401, role mismatch to 403; R-X01 rotates server-side refresh tokens, but no Study Web client/session implementation exists; preserve source hashes and keep recovery policy blockers explicit.
  - path: `.agents/worklog/2026-11-05/study-screen-dd-sh-05.md` (supplemental, screen-specific)
    - carry_forward: Expected behavior calls for at most one refresh attempt and a safe return path, while current source proves only server refresh behavior; verify current assets and source again.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete SH-05 only in this session. Review the existing plan/DD and current source; write/update `SH-05_PLAN.md` before changing DD artifacts; preserve `screen.png` and `code.html`; verify ordered one-to-one marker mapping and A–F/event completeness; update the global tracker and this worklog; keep DD, implementation and runtime statuses separate.
- Canonical contract/approved DD: Current `list_screen.md` SH-05 row, AC-02/AC-11, API #04 and R-X01 catalog/source, linked SH-02 contract, and `.agents/web-study/design.md`. OpenAPI Study contract is `NOT_FOUND`; HTML is prototype evidence only.

## CURRENT_BEHAVIOR

- Source/config: Study Web has no `apps/study-client/src/` or `package.json`; screen files are design artifacts. Current API #04 is composed in `apps/study-server/app/api/v1.py`: its view invokes the shared Bearer/JWT guard with `role="STUDENT"`, queries `CURRENT_USER_PROFILE`, validates the safe `UserProfile`, and returns 200; invalid/missing auth or profile returns 401, non-Student role returns 403 before DB access, and DB/model failure returns safe 500. R-X01 is a separate `POST /api/v1/auth/refresh` route in the API #03 module; it validates and hashes the opaque token, finds a valid refresh session, requires ACTIVE account status, issues a replacement pair, revokes the old row, inserts the new hash and commits. Error paths include 401/403/422/500.
- Runnable tests: Read API #04 test source for successful safe projection, malformed/missing Bearer, invalid JWT/claims, role denial, missing profile and DB/model errors; read API #03 test source for refresh validation, rotation, inactive account and invalid token. No application tests were run and no prior test result is asserted as current verification.
- Runtime wiring: Study Web UI/auth caller/router remains `UNWIRED`; Study Server source declares both API #04 and R-X01. Local source/test evidence does not verify deployed service, live schema or frontend runtime.

## SOURCE_TRACE

```text
Study Web caller/session manager `NOT_FOUND` -> API #04 route in `app/api/v1.py` -> `get_current_user` -> `validate_current_user_request(role="STUDENT")` -> `CURRENT_USER_PROFILE` read -> `UserProfile` projection -> 200 / 401 / 403 / safe 500; on an eligible 401, expected client may call R-X01 (single-flight/max one retry per inventory) -> refresh validation/hash -> `REFRESH_SESSION` lookup -> ACTIVE check -> token issuance -> old-token revoke + new-hash insert + commit -> 200 or 401/403/422/500. Current tests cover server branches via local test source; no client call is present, tests were not run, and live DB/runtime is unverified.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #04 uses one 401 for invalid/missing auth and missing profile | `get_current_user` maps both shared-auth rejection and missing profile to `401 DESIGN_AUTHENTICATION_REQUIRED`; API #04 tests assert both paths. | `DISCREPANCY / BLOCKER` | A 401 alone does not prove expiry; behavior after refresh-success then #04-401 must stop after the one retry and follow an owner-approved outcome. |
| Single-flight refresh requirement vs current client | `list_screen.md` §1.2 requires max one refresh/retry and single-flight for concurrent requests; Study Web editable source/router/package is absent. | `EXPECTED_BEHAVIOR / UNWIRED` | Keep the requirement explicit in DD, but do not claim it is implemented or tested. |
| R-X01 contract boundary | Current Study Server has separate refresh route and transactional token rotation; R-X01 is outside API catalog, and SH-02 owns G-14 #03 catalog/source response discrepancy. | `SOURCE_BACKED LOCALLY / CONTRACT GAP` | SH-05 may describe current server behavior but cannot define client persistence, ambiguous timeout recovery or SH-02 response parsing. |
| Safe-return and production UI | Inventory proposes `/forbidden`, `/login`, `/` and other screen routes; prototype includes technical metadata and synthetic error fields; no Study Web route or approved user-facing copy exists. | `BLOCKER / PROTOTYPE_ONLY` | Keep safe-route fallback, user-facing composition and route wiring open; do not reuse mock reason/status/timestamp as API data. |

## CHANGES

- Files changed: This worklog; `SH-05_PLAN.md` re-audit plan/result; `SH-05.md` A–F crosswalk, refresh expectation/client status and route-candidate wording; global `dd_screens/PLAN.md` SH-05 row and checkpoint. Original `screen.png`, `code.html`, markers and annotation retained.
- CONTEXT_UPDATES: none; no source/contract/page ownership change was made. Repository context validator reports unrelated missing DB Admin context/source roots and source drift.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective and repository preflight | Objective read; root router supplied by user and `.agents/AGENTS.md`, context map, worklog README/template reviewed. | VERIFIED |
| Docs worklog selector and review | `READY`, 3/254 exact-type logs; AD-01, AD-02 and AD-03 fully read; SH-05 logs from 2026-11-05/06 read as supplemental history. | VERIFIED |
| Current Study API source trace | Re-read API #04/R-X01 route and view source, API #04 query/model, shared auth/response/trace helper and focused #04/#03 test source; read only, no tests run. | VERIFIED_SOURCE_REVIEW |
| Expected contract/context | Read `list_screen.md` SH-05/shared auth rules, AC-02/AC-11 diagrams, API #04 catalog/DD discrepancy, project boundary/context pages, Study Web design target and manifest skill/workflow registry. UI-only DD has no canonical skill. | VERIFIED_DOCUMENT_REVIEW |
| Asset visual/source review | `screen.png` 1600×1280 SHA-256 `f13f4da1e7717ccafbf93155af94e526e8a5f865d63e207c21165118c16cd23f`; `code.html` SHA-256 `cd0f2cb849d8a39aae842c08f5602fc24718b2d34e9f446d56041c1017b8ad7a`; annotation viewed; prototype refresh uses local timer only. Final hashes match. | VERIFIED |
| Focused static verification | 11 ordered unique markers map 1:1 to 11 DD elements; center/target bounds and PNG dimensions match JSON; all 7 events have trigger/input/precondition/process/outcome/exception; A–F crosswalk present; local DD/plan links resolve. Original source hashes unchanged. | VERIFIED |
| `git diff --check -- apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` | Exit 0. Authored-text whitespace scan returned no matches. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | Exit 1 (`AGENT_CONTEXT_INVALID`): repository-wide missing DB Admin context/source roots and stale deep-scope source manifests; filtered rerun found no SH-05/worklog diagnostics. Same global failure was recorded in the prior SH-04 session. | PRE-EXISTING_REPOSITORY_FAILURE |
| Application tests / frontend runtime / live DB | Not run; no Study Web source/runtime exists in this checkout. | NOT_RUN |

## HANDOFF

- Remaining blockers: API #04 401 cause ambiguity (including profile missing after a successful refresh), client token persistence/security and ambiguous rotation outcome, implementation of required single-flight/max-one retry, safe-return fallback, production UI/copy composition, and SH-02 G-14 login contract.
- Session result: Static docs re-audit complete; `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Next owner/action: SH-06 is the next candidate, in a separate session only.
