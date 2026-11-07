---
task_id: "2026-11-07-design-study-screen-ad03"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AD-03 Study Web /admin/users/:userId ↔ API #69; AC-31 handoff from AD-02/#68 and downstream AD-04/#70, AD-05/#71/#72"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-03

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 208; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Preserve expected/current separation; inspect Study Web routing every session; keep static prototype claims separate from API fields; trace caller, authorization, query/effects, response and tests; don't claim tests/runtime/live schema verified.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Keep AC-31 user-management permission separate from the local `ADMIN` claim fallback; preserve PII/audit/lifecycle and live-schema blockers; use API #68 list only as the AD-03 handoff, and do not infer detail fields/actions from a mockup.
  - path: `.agents/worklog/2026-11-07/design-study-screen-me17.md`
    - carry_forward: Do not infer numeric identity carriers or privacy policy from route/mockup; distinguish current source from catalog/AC contract; fake DB test evidence does not establish live deployment/schema.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-03 only in this session; inspect current inventory/AC/API/source; write `AD-03_PLAN.md` before creating markers, annotation, or DD; preserve original assets; create ordered one-to-one markers and annotated image; author A–F screen DD with traceable fields/events/API/errors/states/navigation/open decisions; update `list_screen.md`, `dd_screens/PLAN.md`, and this worklog; distinguish DD readiness, implementation block, and runtime verification.
- Inventory row 61: AD-03 “Chi tiết người dùng”, proposed route `/admin/users/:userId`, AC-31, API #69; show account/status/role/audit only when backend returns the data; GET #69; do not display hash or private email beyond permission/contract; linked to AD-04 and AD-05; states `loading/ready/404/403`; P1; inventory gate `D`.
- API catalog row 69 declares `GET /api/v1/admin/users/{user_id}` for Admin and an `ApiEnvelope<UserProfile>` response. Verify direct catalog/AC/API-DD fields and current route/auth/path parsing/query/response/error/test source before finalizing mapping. Do not invent audit fields, editable actions, privacy rules, or role policy.

## CURRENT_BEHAVIOR

- Target folder contains the unchanged source `screen.png` (1600×1456) and `code.html`, plus `AD-03_PLAN.md`, `AD-03_markers.json`, `AD-03_markers.svg`, `screen_annotated.png` (3200×2912), and `AD-03.md` authored in this session.
- Study Web root currently contains `dist/`, `docs/`, `node_modules/`, and `tsconfig.tsbuildinfo`; no editable `src/`, package manifest, router, or API client. Scope remains `UNWIRED`.
- API #69 route is wired to `get_admin_user`. Shared auth guard checks Bearer/JWT and claim `ADMIN` before raw signed-int64 path parsing or querying. Query reads a safe profile allowlist from checked-in legacy `users`; successful envelope maps `UserProfile`; malformed/out-of-range and no-row use 404, query/mapping failure uses safe 500. Permission mapping, path/no-row mapping and legacy query target remain `DERIVED`/draft; live DB/deployment is not verified.
- API #69 focused test source was inspected (safe projection, auth-before-DB, path/no-row 404, 500 mapping, OpenAPI); tests were not run. Prototype HTML is static, has disabled AD-04/AD-05 buttons and placeholder links, and displays unsupported sync/204/audit/retention/RBAC claims.

## SOURCE_TRACE

```text
Expected: AC-31 selects a user from AD-02/#68 → pass `items[].id` as #69 `user_id` → render approved UserProfile/status/role data → hand off to AD-04/#70 or AD-05/#71/#72 only as allowed.
Current: API #69 route/module/query/model/auth/error source and focused test source exist locally; GET uses `ADMIN` claim fallback before path parse/query, reads legacy `users` safe profile columns, returns UserProfile/401/403/404/500. Study Web route/client is UNWIRED. Prototype uses fragment/# links, disabled mutation buttons, a static no-selected-user state and unsupported `204 / NULL_PAYLOAD` plus audit/retention/RBAC copy.
DISCREPANCY: catalog success is 200 `ApiEnvelope<UserProfile>`; current source also implements that success. Prototype's 204/null empty/sync state is not a #69 contract or runtime behavior. Audit data is absent from #69.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #69 detail mapping | Catalog/AC/API DD compared with current route, validation, query, response, shared profile model and focused test source. | SOURCE-BACKED LOCALLY; API DD DRAFT | Use exact current UserProfile fields and status/error set; safe legacy query and path/no-row mappings remain DERIVED; live schema/deployment not verified. |
| Identity, Admin permission, and PII | AD-02/#68 handoff uses numeric `items[].id`; shared guard requires claim `ADMIN`; email/phone are in response. | PARTIAL; POLICY OPEN | Preserve numeric ID handoff, but do not equate ADMIN with approved user-management policy or assume unmasked PII visibility. |
| Audit/sync claims | Prototype has audit count/empty state, retention 180 days, sync and RBAC assertions; #69 has only profile data and read-only behavior. | UNSUPPORTED BY #69 | No audit endpoint/event feed, retention policy or sync success is inferred; prototype 204/NULL_PAYLOAD conflicts with API #69. |
| Study Web route/runtime | Current root tree rechecked; no editable app source/router/package manifest/client. | UNWIRED | Do not claim route implementation or runtime verification. |

## CHANGES

- Files changed: this worklog, `AD-03_PLAN.md`, marker JSON/SVG, `screen_annotated.png`, `AD-03.md`, `apps/study-client/docs/list_screen.md`, and `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`.
- `AD-03_PLAN.md` was written after source/contract trace and before marker JSON/SVG, annotation, or screen DD. Original `screen.png` and `code.html` were preserved.
- API #69 source classification changed `D→R` in the screen inventory/API index because route/module/query/model/auth/test source is present. API DD remains Draft; no Study Server implementation/contract was modified.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective, root router, context map, worklog contract/template reviewed; exact docs selector READY 3/208; AD-01, AD-02, ME-17 fully reviewed; manifest confirms API DD skill excludes web-UI-only DD. | VERIFIED |
| Inventory/tracker | AD-03 inventory/API source rows and global-plan row updated; global tracker records independent DD, implementation, and runtime statuses. | VERIFIED |
| API #69/AC-31/source review | Catalog, AC-31 diagram, API DD/open questions, route/module/query/profile model, shared auth/response helper, checked-in legacy DDL, source-status context, and focused tests reviewed. Test source only; not run. | VERIFIED_SOURCE_REVIEW |
| Screen asset/interaction review | `screen.png` and `code.html` inspected; source hashes recorded; static DOM has no request/event code; Study Web tree rechecked. | VERIFIED |
| Original asset hashes | `screen.png` SHA-256 `3b8add69a0c7dd2cbaaf8620d0d0d51c821a8f6819bd858cfa9ecab745d9abdf`; `code.html` SHA-256 `cd6e5d3dd4a49d3b61f13792c3d59da96388aefafba28a9c743c741974b10bb1`; unchanged. | VERIFIED |
| Marker/DD static audit | 32 ordered unique in-bounds markers; JSON/SVG parse; marker coordinates match plan; 32 element rows match one-to-one; A–F present; local Markdown links resolve; annotated PNG 3200×2912 from 1600×1456 original and visually reviewed. | VERIFIED |
| Artifact inventory | 83 unique IDs in `list_screen.md`, 83 matching screen folders; 56/83 contain all six core files including screen assets, DD, plan, annotation and marker JSON. | VERIFIED |
| Whitespace / diff checks | Scoped `git diff --check` on changed tracked inventory/tracker passed; trailing-whitespace scan of authored plan/DD/worklog/JSON/SVG found none. | VERIFIED |
| Plan and trackers | Plan preceded markers/DD; inventory/API #69 status updated `D→R`; global tracker/checkpoint updated with `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`. | VERIFIED |
| Application tests/runtime | Not run; local #69 test source was inspected and fake DB tests do not prove live schema/deployment. | NOT_RUN |

## HANDOFF

- Remaining blockers: Admin permission mapping, live schema/deployment, PII/enum/lifecycle rules, audit source/retention, Study Web route/client and design-system alignment.
- Session outcome: AD-03 artifacts and trackers complete; API #69 `SOURCE-BACKED LOCALLY (R)`; screen `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Next owner/action: AD-04 is the next screen in this flow, to be handled in a separate session. Do not start another Screen ID in this session.
