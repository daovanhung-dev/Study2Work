---
task_id: "2026-11-07-design-study-screen-sh07-reaudit"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-07 ↔ API #18; operation ID/status/owner and producer flows across AC-12, AC-25, AC-36, AC-38"]
status: "VERIFIED"
---

# Worklog: Re-audit Detailed Design màn hình Study SH-07

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 256; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Separate expected from current behavior; trace backend and tests; do not infer UI/backend mappings from static mockups; preserve original assets and Study Web `UNWIRED` status.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Keep API contract, source, and runtime status distinct; retain owner/permission/privacy blockers; do not claim test source or fake DB confirms deployment.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Use current source over DD when they disagree; preserve identifiers and privacy boundaries; do not infer missing operation/detail fields from a screen.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh07.md` (supplemental, screen-specific)
    - carry_forward: Recheck SH-07 DD against current source; prior trace found no generic API #18 route/storage/test, ID/owner/status/producer discrepancies, and a 35-element/10-event artifact set. Its subcontext-absence note is stale; current `.agents/web-work/study/` pages exist and are registered `UNWIRED`.
  - path: `.agents/worklog/2026-11-05/design-study-screen-sh07.md` (supplemental, screen-specific)
    - carry_forward: Preserve API #18 and producer distinctions; no test/runtime claims from static source; do not infer UUID/int64, generic lifecycle, result schema, persistence, or polling from the mockup.
  - path: `.agents/worklog/2026-10-27/design-study-screen-sh07.md` (supplemental, historical)
    - carry_forward: One Screen ID per session; plan before edits; Study Web is a design target only; API #18 source/runtime blockers remain until current evidence proves otherwise.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete SH-07 only in this session. Audit current plan/DD/assets and source; update `SH-07_PLAN.md` before any changes to DD, marker map, or images; preserve `screen.png` and `code.html`; verify the ordered marker-to-element mapping and events; update `dd_screens/PLAN.md` and this worklog; keep DD, implementation, and runtime statuses separate.
- Canonical contract/approved DD: `apps/study-client/docs/list_screen.md` SH-07 row; API #18 in `docs/lists/list_api.md`; AC-12, AC-25, AC-36 and AC-38; current Study Server route/module/test source if present. Study OpenAPI is `NOT_FOUND`; Web UI-only DD has no canonical skill per registry.

## CURRENT_BEHAVIOR

- Source/config: The seven-file SH-07 bundle exists. `screen.png` is 1503×1600 (SHA-256 `eb5329637c5942f0ac43b439b2dece09cac071565d1b300efa3405f9628ce110`); `code.html` SHA-256 is `2fb2fdab9c88b9b31c5cde9e61b771e233075ac3339d2d6ed1259f0bd99fa3a3`. Study Web editable source and `package.json` are absent; `.agents/web-work/study/AGENTS.md` and `INDEX.md` exist and are registered `study-web: UNWIRED`.
- Runnable tests: API #63/#64/#93/#96 test sources exist and were inspected, not run. No API #18 test source was found. Application tests were not run.
- Runtime wiring: Study Server has source-backed notification create/status routes #63/#64/#93/#96, but no generic API #18 route/module/query or generic Study `operations` table in checked-in DDL/migrations. Study OpenAPI is `NOT_FOUND`; live deployment/database remain unverified.

## SOURCE_TRACE

```text
Expected SH-07 uses `/operations/:operationId`, AC-12/25/36/38 and API #18. Current trace: #18 catalog row says `operation_id:int64`, while reusable Operation ID, AC diagrams and notification producers #63/#93 use UUID; owner-only vs owner/Admin and generic lifecycle/result remain unresolved. #63 returns an Operation response plus notification IDs; #64 reads `notification_id:int64` and returns notification-specific status. #93 returns Notification data plus UUID `meta.operation_id`; #96 reads `notification_id:int64` and returns Notification. These routes do not implement generic #18. Payment #17 and report export #103 have no current Study route/module/test. Checked-in Study DDL/migration contains notification-specific `notifications.operation_id UUID` and delivery outbox, not generic operations storage. Study Web context pages exist but are `UNWIRED`; editable app/router/package source is absent.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #18 and producer contract | API row int64 conflicts with UUID schema/AC and producer #63/#93; owner policy, generic status/lifecycle/result and producer response mapping remain unresolved. No generic route/module/query/test or Study operations table found. | `UNWIRED` / `DISCREPANCY` | Keep DD and implementation blocked; no inferred conversion or status mapping. |
| Study Web | `src/` and `package.json` absent; context entry/index exist and are registered `UNWIRED`. | `UNWIRED` | Context pages do not establish route, auth/session guard, UI or runtime. |
| SH-07 artifacts | Seven files present; 35 ordered markers match 35 DD rows; SVG labels and coordinates validate; 10 event IDs and local links validate; annotated image inspected. | `VERIFIED` (static) | Original source image/HTML hashes preserved; runtime remains unverified. |

## CHANGES

- Files changed: `SH-07_PLAN.md`, `SH-07.md`, `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`, this worklog. Marker JSON, overlay and source images/HTML were not changed in this re-audit.
- CONTEXT_UPDATES: none; corrected the SH-07 docs to match the already registered `study-web: UNWIRED` context.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router and preflight | Current full goal retained; root router, global router, context map and worklog contract/template loaded; docs selector `READY` 3/256; AD-01/02/03 worklogs fully read. | VERIFIED |
| API #18 and producer source trace | Compared API catalog, AC diagrams, API #18 DD/open questions/verification report, route registration, #63/#64/#93/#96 source and tests, #17/#103, Study DDL/migration and Study Web context registry. Tests were inspected only. | VERIFIED (static source) |
| SH-07 static artifact audit | Seven expected files; original image/HTML hashes unchanged; source and annotation 1503×1600; 35 JSON markers ordered, in bounds and matched 35 DD element rows; SVG parsed with 35 labels; 10 unique event IDs; 23 local DD/plan links resolved; 83/83 inventory and tracker IDs match; no trailing whitespace; scoped `git diff --check` passed. Annotation visually reviewed; #23 does not obscure diagnostic text. | VERIFIED (static) |
| Application tests and live runtime | Not run per scope; live DB/deployment not inspected. | NOT RUN / NOT VERIFIED |
| Context validator | `node scripts/validate-agent-context.mjs` exited 1 with `AGENT_CONTEXT_INVALID`: DB Admin context/source roots are reported missing; stale source snapshots are reported for server-study (458 paths), server-work (64), web-work (3), mobile-work (197), and db-admin (74). Filtered output contained no SH-07-specific diagnostic. Recorded as repository-wide context debt, not attributed to this screen. | FAILED — REPO-WIDE CONTEXT |

## HANDOFF

- Remaining blockers: API #18 is `UNWIRED`; operation ID type, generic kind/status/lifecycle/result, owner/Admin policy, producer mapping, polling/retention, return navigation and user-facing treatment of prototype diagnostics remain unresolved. Study Web UI/router/package source remains absent.
- Next owner/action: SH-07 is statically audited; any next Screen ID must be handled in a separate session.
