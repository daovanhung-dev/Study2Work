---
task_id: "2026-11-07-design-study-screen-ad02"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AD-02 Study Web /admin/users ↔ API #68; AD-03/API #69 and AD-04/APIs #69/#70; AC-31"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-02

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 207; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected behavior separate from current source; preserve original assets; trace caller, server guard, query/effects, response and tests; keep Study Web `UNWIRED` unless editable route/client code proves otherwise; retain API catalog versus runtime discrepancies and do not claim tests/runtime were verified.
  - path: `.agents/worklog/2026-11-07/design-study-screen-me17.md`
    - carry_forward: Do not infer routes, identity carriers, data mappings, or behavior from mockups; inspect current server caller/callee and errors; keep UI/API contract and local-source differences explicit; distinguish DD, implementation, and runtime status.
  - path: `.agents/worklog/2026-11-07/design-study-screen-me18.md`
    - carry_forward: Use the context registry to determine skill applicability; UI-only DD has no canonical skill; preserve source assets and label prototype interactions as unwired; tests/fake data do not establish runtime or live schema.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-02 only in this session; inspect expected contracts and current source; write `AD-02_PLAN.md` before marker map, annotation, or screen DD; preserve original assets; create ordered one-to-one markers and annotated image; author A–F screen DD with traceable events, APIs, states, navigation and open decisions; update `list_screen.md`, `dd_screens/PLAN.md`, and this worklog; distinguish `DD READY`, `IMPLEMENTATION BLOCKED`, and `RUNTIME VERIFIED`.
- Inventory row 60: AD-02 “Danh sách người dùng”, proposed route `/admin/users`, AC-31, API #68; user table with keyword, status, role, pagination, and admin actions; GET #68 with filters and retained query URL; Admin-only; links AD-03 and AD-04; expected states `loading/empty/ready/filter-error`; P1; inventory gate `D`.
- API catalog row 68 declares `GET /api/v1/admin/users`; the screen inventory initially marked it `D`. Compare catalog/AC with the current route, query, data, auth, response, errors, DB effect, and focused test source before finalizing the screen mapping. Do not invent fields, filter semantics, write actions, or role policy.

## CURRENT_BEHAVIOR

- Source assets: `screen.png` is 1600×1425 RGB, SHA-256 `444e6530086a14607ff097d39a5133c55e6f637146a09ee9ebc8c0e61d61a6e0`; `code.html` SHA-256 `af8433bd009b3e7e2309631b17841488746a26d62edca6420d5d98782f89a57d`. Screenshot is an empty-state prototype with search/role/status controls, user-table headings, export/add buttons, pagination, and audit/security claims.
- Prototype HTML has eight `href="#"` navigation/footer links; role options carry lowercase `student/instructor/admin`, status options `active/locked/pending`, and search copy includes user ID. It contains no API/fetch/XHR, form, or route wiring. The only listener is Reset, which clears three controls and focuses search; Refresh and pagination are disabled. Export, Add user, and guide buttons have no behavior.
- Study Web recheck: current app tree contains docs/assets, ignored `dist/`, and `node_modules/`; editable source, package manifest, and `/admin/users` route are absent. The subcontext remains `UNWIRED`; serving/deployment is unverified.
- API #68 is composed in `app/api/v1.py` and source-backed locally. It calls the shared Bearer/JWT guard for `ADMIN` before DB access, validates `page`, normalizes keyword, then runs matching read-only COUNT and page SQL against the checked-in legacy BIGINT `users` candidate. Role/status are exact-match strings; keyword is a trimmed/lowercase literal substring of `full_name` or `email`; default page is 1, fixed size is 20, order is `id ASC`. The response is `ApiEnvelope<Page<UserProfile>>` with `items` and `pagination{page,size,total,total_pages}`; safe profile fields are `id,full_name,email,role,avatar_url,phone,status,created_at,updated_at`, with no `password_hash` or `bio`. Empty results return 200 with an empty page; malformed/out-of-range page returns 422; auth/role failures return 401/403; query/projection failures return safe 500 after rollback. The handler does not commit or mutate data.
- API #68 focused test source covers authorization before DB access, filters, literal keyword, fixed pagination, empty results, invalid page, nullable safe profile fields, malformed query projections, rollback, trace/envelope and OpenAPI. The context records 15 focused cases passed at a prior checkpoint; test source was read but no test was run in this session. Fake sessions do not establish live schema/deployment.
- The #68 API DD is `Draft — Needs Confirmation`: claim-to-user-management permission, legacy-vs-V1-PILOT live schema, role/status value lists, PII/audit policy, and lifecycle visibility remain open. AC-31 calls for an Admin with user-management permission; mapping that permission to the `ADMIN` JWT claim is DERIVED.

## SOURCE_TRACE

```text
Expected: AC-31 Admin with user-management permission opens AD-02 → GET #68 with role/status/keyword/page → query users + pagination → select a user → GET #69 detail → branch to #70 update, #71 status, or #72 delete → reload list/detail. Inventory expects query URL preservation and links AD-03/AD-04; its role values and filtering UX do not define server filter semantics.
Current: Study Web has no editable route/client caller → `app/api/v1.py:get_admin_users_endpoint` reads raw query/header/session/trace → `get_admin_users` calls shared `ADMIN` JWT guard → page/keyword validation → COUNT and LIST SQL over legacy `users` with same filters → `UserProfile` allowlist + fixed Page metadata → success envelope, or safe 401/403/422/500. Read path has no write/commit; errors roll back. Tests use fake DB sessions; live schema/deployment is unverified.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Search and filter vocabulary | Prototype says keyword includes user ID and uses lowercase role values (`student/instructor/admin`) and status values (`active/locked/pending`). API #68 searches only `full_name/email`, exact-matches stored role/status strings, and defines no allowed enum list. | DISCREPANCY / BLOCKER | Do not map `instructor` to `MENTOR`, `locked` to `SUSPENDED`, or claim ID search without owner-approved contract changes. |
| Create/export/audit and system-status actions | Mockup has Add user, Export report, guide, “system normal,” sync, RBAC/security and audit claims. API #68 is read-only; AC-31 contains #68–#72 but no user-create/export/audit/system-health endpoint. | STATIC_ONLY / UNMAPPED | Keep actions inactive/undetermined; do not imply creation, export, live sync, or audit recording. |
| Data exposure and lifecycle | API #68 returns email/phone behind `ADMIN`; separate user-management permission, PII/audit policy, live schema, and deleted/suspended visibility remain open in the Draft API DD. | DERIVED / BLOCKER | Require owner approval for permission mapping, PII visibility and lifecycle rules before implementation. |
| Study Web route/runtime | Context manifest and current app tree show no editable source/package/router; only ignored `dist` and docs/assets are present. | UNWIRED | No implementation/runtime claim; proposed `/admin/users` is not a current route. |
| Visual design source | Prototype uses a cobalt/Plus Jakarta Sans system; Study Web guide specifies ocean-blue semantic tokens and Inter/system typography, with accessible controls and responsive reflow. | DESIGN DISCREPANCY | Align the final implementation with `.agents/web-study/design.md` or record an approved exception. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02_PLAN.md`, `AD-02_markers.json`, `AD-02_markers.svg`, `screen_annotated.png`, `AD-02.md`; `apps/study-client/docs/list_screen.md`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; this worklog.
- API #68 source classification changed `D→R` in the Study screen inventory because the current route/module/query/model/test source is present; the API DD remains Draft. No Study Server source or API contract changed.
- `AD-02_PLAN.md` was written after source/contract trace and before marker JSON/SVG, annotation, or screen DD. Original `screen.png` and `code.html` were preserved.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective and router/context instructions reviewed; exact docs selector READY 3/207; AD-01, ME-17, and ME-18 worklogs fully reviewed; registry routing confirms API-DD skill excludes web-UI-only DD. | VERIFIED |
| Inventory and source trace | AD-02 inventory row, AC-31 diagram, API #68 catalog/DD/source/test source, user profile model, shared auth guard, DB/security context, database context, test context, Study Web tree and screen HTML/image reviewed. No application tests run. | VERIFIED |
| Source asset hashes | `screen.png` SHA-256 `444e6530086a14607ff097d39a5133c55e6f637146a09ee9ebc8c0e61d61a6e0`; `code.html` SHA-256 `af8433bd009b3e7e2309631b17841488746a26d62edca6420d5d98782f89a57d`; unchanged. | VERIFIED |
| Marker/DD static audit | 38 sequential unique in-bounds markers; 38 element rows exact 1:1; JSON/XML parse; local Markdown links resolve; annotated PNG 3200×2850 from 1600×1425 source; image reviewed directly. | VERIFIED |
| Artifact inventory | 83 screen folders; 55/83 have all four core artifacts after AD-02. | VERIFIED |
| `git diff --check` | Scoped check of modified trackers passed; authored DD/plan/worklog/JSON/SVG have no trailing whitespace. | VERIFIED |
| Application tests/runtime | Not run; local #68 test source and prior context result read only; fake DB tests do not prove live schema/deployment. | NOT_RUN |

## HANDOFF

- Remaining blockers: role/status option vocabulary, search-by-ID, create/export/audit/sync behavior, Admin permission, PII/lifecycle policy, live schema/deployment, and Study Web route/runtime remain unresolved.
- Session outcome: AD-02 artifacts and trackers complete; `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.
- Next owner/action: choose the next Screen ID in a separate session; do not continue beyond AD-02 in this session.
